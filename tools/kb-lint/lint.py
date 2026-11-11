#!/usr/bin/env python3
"""Lint the knowledge base against docs/KB-ENTRY-SCHEMA.md and the platform-agnostic rule in docs/VISION.md.

Usage: python3 -I tools/kb-lint/lint.py [--allow-promoted]   (exit 1 on any error)

Checks entries under principles/ methodology/ applications/ (frontmatter + the eight body sections) and adapter
docs under platforms/ (frontmatter only). Core layers (principles, methodology, workflows, safety) must not name an
ECU, vendor product or vendor file type outside their Citations section and frontmatter.
"""
import argparse, re, sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "tools" / "corpus"))
from taxonomy import PLATFORMS  # noqa: E402

SECTIONS = ["Claim", "Why (derivation)", "Assumptions", "Breaks when", "Practical use", "Worked example",
            "Disputed / conflicts", "Citations"]
FIELDS = ["id", "title", "layer", "status", "confidence", "sources", "verified", "applies_to", "depends_on", "supersedes"]
LAYERS = {"L0", "L1", "L2", "L3", "L4"}; STATUS = {"draft", "reviewed", "established", "disputed", "deprecated"}
CONF = {"low", "medium", "high"}
ENTRY_DIRS = ["principles", "methodology", "applications"]; CORE_DIRS = ["principles", "methodology", "workflows", "safety"]
SKIP = {"README.md"}; SKIP_PARTS = {"glossary", "calculators", "__pycache__"}
# Sources are named only in frontmatter `sources` and the Citations section (or as `registry-id` in backticks), so a
_NAMES = Path(__file__).with_name("private_names.txt")   # staging only; the public build has no named sources
NAMED = re.compile(r"\b(" + "|".join(x.strip() for x in _NAMES.read_text().splitlines() if x.strip() and not x.startswith("#")) + r")\b") if _NAMES.exists() else None
VENDOR = re.compile("|".join(p for v in PLATFORMS.values() for p in v) + r"|\bpclink\b|\.pclr\b|\.llg\b", re.I)

def frontmatter(text):
    if not text.startswith("---\n"): return None, text
    end = text.find("\n---", 3)
    if end < 0: return None, text
    meta = {}
    for ln in text[4:end].splitlines():
        m = re.match(r"([a-z_]+):\s*(.*)$", ln)
        if m: meta[m.group(1)] = m.group(2).strip()
    return meta, text[end + 4:]

def as_list(v):
    v = (v or "").strip()
    if not (v.startswith("[") and v.endswith("]")): return None
    return [x.strip() for x in v[1:-1].split(",") if x.strip()]

def registry_ids():
    return set(re.findall(r"^  - id:\s*(\S+)", (ROOT / "sources" / "registry.yaml").read_text(encoding="utf8"), re.M))

def core_text(text):
    """Body without frontmatter or the Citations section."""
    _, body = frontmatter(text)
    return re.split(r"^## Citations\s*$", body, flags=re.M)[0]

def files(dirs):
    for d in dirs:
        for p in sorted((ROOT / d).rglob("*.md")):
            if p.name not in SKIP and not SKIP_PARTS & set(p.parts): yield p

def check_entry(p, meta, body, reg, ids, a, errs, sections=True):
    rel = p.relative_to(ROOT).as_posix()
    for f in FIELDS:
        if f not in meta: errs.append(f"{rel}: missing field {f}")
    if meta.get("id") != rel[:-3]: errs.append(f"{rel}: id must be {rel[:-3]}")
    if meta.get("layer") not in LAYERS: errs.append(f"{rel}: bad layer {meta.get('layer')}")
    if meta.get("status") not in STATUS: errs.append(f"{rel}: bad status {meta.get('status')}")
    if not a.allow_promoted and meta.get("status") != "draft": errs.append(f"{rel}: status must stay draft until human review")
    if meta.get("confidence") not in CONF: errs.append(f"{rel}: bad confidence {meta.get('confidence')}")
    if not re.fullmatch(r"\d{4}-\d{2}-\d{2}", meta.get("verified", "")): errs.append(f"{rel}: bad verified date")
    srcs = as_list(meta.get("sources"))
    if not srcs: errs.append(f"{rel}: sources must be a non-empty list")
    for s in srcs or []:
        if s not in reg: errs.append(f"{rel}: unknown source {s}")
    for d in as_list(meta.get("depends_on")) or []:
        if d not in ids: errs.append(f"{rel}: depends_on unresolved: {d}")
    if not sections: return
    heads = re.findall(r"^## (.+?)\s*$", body, re.M)
    pos = -1
    for s in SECTIONS:
        if s not in heads: errs.append(f"{rel}: missing section '{s}'"); continue
        i = heads.index(s)
        if i < pos: errs.append(f"{rel}: section '{s}' out of order")
        pos = i
        m = re.search(rf"^## {re.escape(s)}\s*$(.*?)(?=^## |\Z)", body, re.M | re.S)
        if m and not m.group(1).strip(): errs.append(f"{rel}: section '{s}' is empty")
    cit = re.search(r"^## Citations\s*$(.*)\Z", body, re.M | re.S)
    for s in srcs or []:
        if cit and s not in cit.group(1): errs.append(f"{rel}: source {s} has no locator in Citations")

def main():
    ap = argparse.ArgumentParser(); ap.add_argument("--allow-promoted", action="store_true"); a = ap.parse_args()
    reg, errs, n = registry_ids(), [], 0
    parsed = {}
    for p in files(ENTRY_DIRS + ["platforms"]):
        if p.parent.name == "parser" or "tests" in p.parts: continue
        meta, body = frontmatter(p.read_text(encoding="utf8"))
        if meta is None: errs.append(f"{p.relative_to(ROOT)}: no frontmatter"); continue
        parsed[p] = (meta, body)
    ids = {m.get("id") for m, _ in parsed.values()}
    for p, (meta, body) in parsed.items():
        n += 1; check_entry(p, meta, body, reg, ids, a, errs, sections="platforms" not in p.relative_to(ROOT).parts)
    for p in list(files(ENTRY_DIRS + ["platforms", "workflows"])) + [ROOT / "SKILL.md"]:
        if p.parent.name == "parser" or "tests" in p.parts: continue
        text = p.read_text(encoding="utf8")
        body = text.split("\n---\n", 1)[1] if text.startswith("---") and "\n---\n" in text else text
        body = re.split(r"^## Citations\s*$", body, flags=re.M)[0]
        body = re.sub(r"`[a-z0-9.\-]+`", "", body)
        for m in (NAMED.finditer(body) if NAMED else ()):
            errs.append(f"{p.relative_to(ROOT).as_posix()}: names a source outside Citations: '{m.group(0)}'")
    core = 0
    for p in files(CORE_DIRS):
        core += 1; rel = p.relative_to(ROOT).as_posix(); text = p.read_text(encoding="utf8")
        for m in VENDOR.finditer(core_text(text) if text.startswith("---") else text):
            errs.append(f"{rel}: core layer names a platform: '{m.group(0)}'")
    for p in sorted((ROOT / "safety").rglob("*.yaml")):
        for m in VENDOR.finditer(p.read_text(encoding="utf8")): errs.append(f"{p.relative_to(ROOT)}: core layer names a platform: '{m.group(0)}'")
    for e in errs: print(e)
    print(f"kb-lint: {n} entries, {core} core files, {len(errs)} errors")
    sys.exit(1 if errs else 0)

if __name__ == "__main__":
    main()
