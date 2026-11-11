#!/usr/bin/env python3
"""Flag runs of consecutive words shared between tracked knowledge files and the private collateral.

Usage: python3 -I tools/verbatim-check/check.py [--n 12] [--selftest]   (exit 1 if anything matches)

Tracked text is broken into n-word shingles (lower case, letters and digits only) and every collateral document is
scanned for them. Prints the tracked file and the shared words only; a shared phrase of this length is short and
tells the author what to rewrite. Run before finishing any ingestion work.
"""
import argparse, re, sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
TRACKED = ["principles", "methodology", "workflows", "platforms", "applications", "safety", "evals", "ingestion", "SKILL.md"]
EXT = {".md", ".yaml", ".txt"}
SKIP_NAMES = {"terms.yaml", "channels.yaml"}     # generated name lists and native channel labels are facts, not prose
WORD = re.compile(r"[a-z0-9]+")

def words(t): return WORD.findall(t.lower())

def tracked_files():
    for t in TRACKED:
        p = ROOT / t
        if p.is_file(): yield p
        elif p.is_dir():
            for f in sorted(p.rglob("*")):
                if f.suffix in EXT and f.is_file() and f.name not in SKIP_NAMES: yield f

def strip_fm(t):
    if t.startswith("---"):
        e = t.find("\n---", 3)
        if e > 0: return t[e + 4:]
    return t

def shingles(tokens, n): return (" ".join(tokens[i: i + n]) for i in range(len(tokens) - n + 1))

def scan(n, tracked, collateral):
    index = {}
    for name, text in tracked:
        for s in shingles(words(strip_fm(text)), n): index.setdefault(s, set()).add(name)
    hits = {}
    for name, text in collateral:
        for s in shingles(words(text), n):
            if s in index:
                for f in index[s]: hits.setdefault(f, set()).add(s)
    return hits

def collateral_docs():
    root = ROOT / "collateral"
    for p in root.rglob("*.md"):
        if {"_index", "_cleaned", "_originals"} & set(p.parts): continue
        yield str(p.relative_to(root)), strip_fm(p.read_text(encoding="utf8", errors="replace"))

def main():
    ap = argparse.ArgumentParser(); ap.add_argument("--n", type=int, default=12); ap.add_argument("--selftest", action="store_true")
    a = ap.parse_args()
    if a.selftest:
        src = "one two three four five six seven eight nine ten eleven twelve thirteen"
        assert scan(12, [("a", "x " + src)], [("c", src)]), "copied run must be found"
        assert not scan(12, [("a", "one two three four five six seven eight nine ten eleven zzz")], [("c", src)]), "11 shared words must pass"
        print("verbatim-check selftest ok"); return
    tracked = [(str(p.relative_to(ROOT)), p.read_text(encoding="utf8", errors="replace")) for p in tracked_files()]
    hits = scan(a.n, tracked, collateral_docs())
    for f, ss in sorted(hits.items()):
        print(f"{f}: {len(ss)} shared {a.n}-word runs")
        for s in sorted(ss)[:5]: print("   ", s)
    print(f"verbatim-check: {len(tracked)} tracked files, {len(hits)} with shared {a.n}-word runs")
    sys.exit(1 if hits else 0)

if __name__ == "__main__":
    main()
