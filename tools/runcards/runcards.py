#!/usr/bin/env python3
"""Run-card generator and voice protocol checks (docs/OPERATING-MODES.md). Plans tests; never touches an ECU.

Cards are ordered lowest risk first: steady state before pulls, low load before high load. Every card carries its
conditions and abort list.
"""
import argparse, json, re, sys
from dataclasses import dataclass, asdict, field
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "tools" / "common"))
import miniyaml  # noqa: E402

BASE_ABORTS = [a["id"] for a in miniyaml.load((ROOT / "safety" / "aborts.yaml").read_text(encoding="utf8"))["aborts"]]
MODES = ("road", "dyno")
PRIORITY = ("SAFETY", "ABORT", "INSTRUCTION", "STATUS", "CHAT")
ROAD_CONDITIONS = ["engine warm", "stable temperatures", "valid wideband", "legal, clear and safe road"]
DYNO_CONDITIONS = ["engine warm", "stable temperatures", "valid wideband", "vehicle secured", "cooling fans running"]

@dataclass
class RunCard:
    id: int
    purpose: str
    kind: str
    rpm: float
    load: float
    risk: int
    gear: str = ""
    duration_s: float = 0.0
    throttle: str = ""
    aborts: list = field(default_factory=lambda: list(BASE_ABORTS))
    conditions: list = field(default_factory=list)

def plan(cells, mode, gear="3rd", max_rpm=None, include_pulls=True):
    """cells: [(rpm, load, purpose)] that need data. Pulls need a declared rev limit, because their end point is the risk."""
    if mode not in MODES: raise ValueError(f"mode must be one of {MODES}")
    cond = ROAD_CONDITIONS if mode == "road" else DYNO_CONDITIONS
    gear_txt = gear if mode == "road" else "dyno held"
    cards, n = [], 0
    for rpm, load, purpose in sorted(cells, key=lambda c: (c[1], c[0])):
        n += 1
        cards.append(RunCard(n, purpose, "steady", rpm, load, 1 + int(load > 100), gear_txt, 10.0, f"hold {rpm:.0f} rpm at {load:.0f} kPa", conditions=list(cond)))
    if include_pulls:
        if max_rpm is None: raise ValueError("a full-throttle pull needs a declared rev limit")
        top = max(c[1] for c in cells) if cells else 100.0
        start = 2000.0
        # ramp rate default from methodology/full-load: about 1 second per 500 rpm
        for end in range(int(start) + 1500, int(max_rpm) + 1, 500):
            n += 1
            cards.append(RunCard(n, f"full-load check to {end} rpm", "pull", float(end), top, 3, gear_txt, (end - start) / 500.0, f"full throttle {start:.0f} to {end} rpm", conditions=list(cond)))
    return cards

def card_text(c):
    """What is spoken: the card number, gear and one target. Exact load stays on the written card."""
    if c.kind == "pull": return f"Run card {c.id}: {c.gear}, full throttle to {c.rpm:.0f} rpm."
    feel = "light" if c.load < 70 else "part" if c.load <= 100 else "boost"
    return f"Run card {c.id}: {c.gear}, hold {c.rpm:.0f} rpm, {feel} throttle."

def validate_utterance(text, priority="INSTRUCTION"):
    """Rules for anything spoken to a driver. Returns a list of problems."""
    out = []
    if priority not in PRIORITY: out.append("unknown priority")
    if len(text.split()) > 15: out.append("over 15 words")
    if re.search(r"\|", text) or len(re.findall(r"\d+(?:\.\d+)?", text)) > 3: out.append("too many numbers or a table")
    return out

@dataclass
class VoiceState:
    moving: bool = False
    in_pull: bool = False

def may_speak(priority, state):
    """During a pull only safety and abort calls are allowed."""
    if state.in_pull: return priority in ("SAFETY", "ABORT")
    return True

def may_apply_change(state):
    """No changes while moving (docs/SAFETY.md rule 8; the default, and this skill has no way to enable it)."""
    return not state.moving

def main():
    ap = argparse.ArgumentParser(); ap.add_argument("--mode", required=True, choices=MODES); ap.add_argument("--cells", required=True, help="JSON list of [rpm, load, purpose]")
    ap.add_argument("--max-rpm", type=float); ap.add_argument("--no-pulls", action="store_true")
    a = ap.parse_args()
    print(json.dumps([asdict(c) for c in plan([tuple(x) for x in json.loads(a.cells)], a.mode, max_rpm=a.max_rpm, include_pulls=not a.no_pulls)], indent=1))

if __name__ == "__main__":
    main()
