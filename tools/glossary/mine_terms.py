#!/usr/bin/env python3
"""Mine candidate glossary terms from collateral (stdlib only, read-only).

Usage:
  python3 -I mine_terms.py acronyms DIR [DIR ...]            # ALL-CAPS tokens by document count, per vendor
  python3 -I mine_terms.py oov TRANSCRIPT_DIR --vocab DIR [DIR ...] [--dict /usr/share/dict/words]
                                                            # transcript words absent from vendor docs + dictionary
  python3 -I mine_terms.py grep TERM DIR [DIR ...]           # document count of an exact phrase, per vendor
  python3 -I mine_terms.py kwic REGEX DIR [DIR ...] [--n 8]  # keyword in context (case-insensitive regex)

Frontmatter is skipped. Vendor = the frontmatter `vendor:` field (else the parent folder name).
Output is a ranked text list for a human or agent to curate into principles/glossary/terms.yaml and
platforms/<ecu>/terms.yaml; nothing is written to the KB by this script.
"""
import argparse, collections, re, sys
from pathlib import Path

def docs(dirs):
    for d in dirs:
        for p in Path(d).rglob("*.md"):
            t = p.read_text(encoding="utf8", errors="replace")
            vendor = p.parent.name
            if t.startswith("---"):
                end = t.find("\n---", 3)
                m = re.search(r"^vendor:\s*(\S+)", t[:end], re.M)
                if m: vendor = m.group(1)
                t = t[end + 4:]
            yield vendor, p, t

def acronyms(a):
    per = collections.defaultdict(collections.Counter); tot = collections.Counter()
    for v, _, t in docs(a.dirs):
        s = set(re.findall(r"\b[A-Z][A-Z0-9]{1,5}\b", t))
        per[v].update(s); tot.update(s)
    for term, n in tot.most_common(a.top):
        top = ", ".join(f"{v}:{c[term]}" for v, c in sorted(per.items(), key=lambda x: -x[1][term])[:6] if c[term])
        print(f"{n:6d}  {term:8s} {top}")

def words(t): return re.findall(r"[a-z][a-z']+", t.lower())

def oov(a):
    vocab = set()
    for _, _, t in docs(a.vocab): vocab.update(words(t))
    if Path(a.dict).exists():
        vocab.update(w.strip().lower() for w in open(a.dict, encoding="utf8", errors="replace"))
    cnt, files = collections.Counter(), collections.defaultdict(set)
    for _, p, t in docs([a.transcripts]):
        t = re.sub(r"\[\d\d:\d\d(:\d\d)?\]", " ", t)
        for w in words(t):
            w = w.strip("'")
            if w.endswith("'s"): w = w[:-2]
            if len(w) > 2 and w not in vocab: cnt[w] += 1; files[w].add(p.stem[:11])
    for w, n in cnt.most_common(a.top): print(f"{n:5d}  {len(files[w]):3d} files  {w}")

def grep(a):
    rx = re.compile(r"(?<![A-Za-z0-9])" + re.escape(a.term) + r"(?![A-Za-z0-9])", 0 if a.case else re.I)
    per = collections.Counter()
    for v, _, t in docs(a.dirs):
        if rx.search(t): per[v] += 1
    print(a.term, dict(per.most_common()))

def kwic(a):
    rx = re.compile(r"(?P<pre>.{0,%d})(?P<hit>%s)(?P<post>.{0,%d})" % (a.width, a.regex, a.width), re.I); n = 0
    for _, p, t in docs(a.dirs):
        for m in rx.finditer(t.replace("\n", " ")):
            print(f"{p.stem[:11]}  ...{m['pre']}[{m['hit']}]{m['post']}..."); n += 1
            if n >= a.n: return

def main():
    ap = argparse.ArgumentParser(); sp = ap.add_subparsers(dest="cmd", required=True)
    p = sp.add_parser("acronyms"); p.add_argument("dirs", nargs="+"); p.add_argument("--top", type=int, default=300)
    p.set_defaults(f=acronyms)
    p = sp.add_parser("oov"); p.add_argument("transcripts"); p.add_argument("--vocab", nargs="+", required=True)
    p.add_argument("--dict", default="/usr/share/dict/words"); p.add_argument("--top", type=int, default=400)
    p.set_defaults(f=oov)
    p = sp.add_parser("grep"); p.add_argument("term"); p.add_argument("dirs", nargs="+")
    p.add_argument("--case", action="store_true"); p.set_defaults(f=grep)
    p = sp.add_parser("kwic"); p.add_argument("regex"); p.add_argument("dirs", nargs="+")
    p.add_argument("--n", type=int, default=8); p.add_argument("--width", type=int, default=45); p.set_defaults(f=kwic)
    a = ap.parse_args(); a.f(a)

if __name__ == "__main__":
    main()
