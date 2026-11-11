#!/usr/bin/env python3
"""Write KB entries from a Python spec file so frontmatter and section order are always right.

Usage: python3 -I tools/kb-lint/new_entry.py SPEC.py
SPEC.py defines ENTRIES, a list of dicts with id, title, layer, confidence, sources, fuels, engines, depends_on,
claim, why, assumptions, breaks, use, example, disputed, citations; optional extra (dict of heading -> text, placed
after 'use'). Files are written at <id>.md and overwritten."""
import runpy, sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]

def render(e):
    fl = lambda v: "[" + ", ".join(v) + "]"
    head = (f"---\nid: {e['id']}\ntitle: {e['title']}\nlayer: {e['layer']}\nstatus: draft\nconfidence: {e['confidence']}\n"
            f"sources: {fl(e['sources'])}\nverified: {e.get('verified', '2026-11-10')}\n"
            f"applies_to: {{fuels: {fl(e.get('fuels', ['gasoline', 'ethanol', 'methanol']))}, engines: {fl(e.get('engines', ['all']))}}}\n"
            f"depends_on: {fl(e.get('depends_on', []))}\nsupersedes: []\n---\n\n# {e['title']}\n")
    body = [("Claim", e["claim"]), ("Why (derivation)", e["why"]), ("Assumptions", e["assumptions"]), ("Breaks when", e["breaks"]), ("Practical use", e["use"])]
    body += list(e.get("extra", {}).items())
    body += [("Worked example", e["example"]), ("Disputed / conflicts", e.get("disputed", "None recorded.")), ("Citations", e["citations"])]
    return head + "".join(f"\n## {h}\n{t.strip()}\n" for h, t in body)

def main():
    n = 0
    for e in runpy.run_path(sys.argv[1])["ENTRIES"]:
        p = ROOT / (e["id"] + ".md"); p.parent.mkdir(parents=True, exist_ok=True); p.write_text(render(e), encoding="utf8"); n += 1
    print(f"wrote {n} entries")

if __name__ == "__main__":
    main()
