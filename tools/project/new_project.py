#!/usr/bin/env python3
"""Create a tuning-project workspace for one vehicle, OUTSIDE this repository.

A project holds one car's files and history: tunes, logs, the setup profile, session notes and change history.
The skill repo stays generic; nothing in a project is ever copied back into it.

  python3 -I tools/project/new_project.py ~/tuning-projects/my-car --platform link-g4plus
"""
import argparse, json, sys
from pathlib import Path

SKILL = Path(__file__).resolve().parents[2]

PROFILE = {
    "_note": "Setup profile (docs/SETUP-PROFILE.md). 'unknown' is a valid answer; safety-critical unknowns withhold changes.",
    "vehicle": "", "engine": "", "aspiration": "unknown", "fuel": "unknown", "ethanol_sensor": "unknown",
    "injectors": "", "fuel_system_capacity": "unknown", "wideband_valid": "unknown", "knock_detection": "unknown",
    "live_edits_during_log": "unknown", "tune_matches_log": "unknown",
    "limits": {"_note": "Only values you have a reason for. These can only tighten the defaults in safety/limits.yaml.",
               "max_rpm": None, "max_boost_kpa": None},
}

CLAUDE_MD = """# Tuning project: {name}

This folder is one vehicle's tuning project. Use the ecu-tuning skill at {skill} (read its SKILL.md first).

- Platform: {platform}
- tunes/     every tune file, never overwritten; name them by date and purpose (2026-11-11_after-cams.pclr)
- logs/      every log; one per session, with a line in sessions/ saying what was driven and what changed
- sessions/  dated notes: goal, what was asked, findings, proposals, what the user applied
- profile.json  the setup profile and declared limits for this car
- history.md    a running list of tune changes and why

Rules for the agent:
- Read profile.json and history.md before anything else; ask once for unknowns the task needs.
- Before analysing a log, run the skill's log-capture review and log-health check on it.
- Never modify a tune file. Proposals are diffs for the user to enter; record what they applied in history.md.
- When the user supplies a new tune version, run the skill's tune-diff against the previous one and note it in history.md.
- Nothing from this folder goes into the skill repository.
"""

def main():
    ap = argparse.ArgumentParser(); ap.add_argument("path"); ap.add_argument("--platform", required=True)
    a = ap.parse_args()
    root = Path(a.path).expanduser().resolve()
    if SKILL in root.parents or root == SKILL: sys.exit("a project must live outside the skill repository")
    if not (SKILL / "platforms" / a.platform).is_dir(): sys.exit(f"unknown platform '{a.platform}'")
    if root.exists() and any(root.iterdir()): sys.exit(f"{root} exists and is not empty")
    for d in ("tunes", "logs", "sessions"): (root / d).mkdir(parents=True, exist_ok=True)
    (root / "profile.json").write_text(json.dumps(dict(PROFILE, platform=a.platform), indent=1) + "\n")
    (root / "history.md").write_text("# Tune history\n\n| Date | Tune file | Change | Why | Evidence |\n|---|---|---|---|---|\n")
    (root / "CLAUDE.md").write_text(CLAUDE_MD.format(name=root.name, skill=SKILL, platform=a.platform))
    (root / "AGENTS.md").write_text("See CLAUDE.md.\n")
    print(f"created {root}")

if __name__ == "__main__":
    main()
