"""Tiny stdlib reader/writer for the YAML subset used by the glossary files.

Supported: comments; top-level `key: scalar`; top-level `key:` followed by a list of flat mappings
(`  - k: v` then `    k: v`); values that are plain/quoted scalars or flow lists `[a, "b, c"]`.
Anything else raises ValueError, so files stay simple enough for any agent or tool to read.
"""
import re

def _scalar(s):
    s = s.strip()
    if s[:1] in "\"'" and s[-1:] == s[:1]:
        return s[1:-1].replace('\\"', '"') if s[0] == '"' else s[1:-1].replace("''", "'")
    if re.fullmatch(r"-?\d+", s): return int(s)
    if re.fullmatch(r"-?\d+\.\d+", s): return float(s)
    return {"true": True, "false": False, "null": None, "~": None}.get(s, s)

def _flow(s):
    inner, items, cur, q = s.strip()[1:-1], [], "", ""
    for ch in inner:
        if q:
            cur += ch
            if ch == q: q = ""
        elif ch in "\"'": q = ch; cur += ch
        elif ch == ",": items.append(cur); cur = ""
        else: cur += ch
    if cur.strip(): items.append(cur)
    return [_scalar(x) for x in items if x.strip()]

def _value(s):
    s = s.strip()
    return _flow(s) if s.startswith("[") else _scalar(s)

def _strip_comment(line):
    q = ""
    for i, ch in enumerate(line):
        if q:
            if ch == q: q = ""
        elif ch in "\"'": q = ch
        elif ch == "#" and (i == 0 or line[i - 1] in " \t"): return line[:i].rstrip()
    return line.rstrip()

def load(text):
    doc, key, item = {}, None, None
    for n, raw in enumerate(text.splitlines(), 1):
        line = _strip_comment(raw)
        if not line.strip(): continue
        m = re.fullmatch(r"([A-Za-z_][\w-]*):(.*)", line)
        if m:
            key, rest = m.group(1), m.group(2)
            doc[key] = _value(rest) if rest.strip() else []; item = None; continue
        m = re.fullmatch(r"  - ([A-Za-z_][\w-]*):(.*)", line)
        if m and key is not None and isinstance(doc[key], list):
            item = {m.group(1): _value(m.group(2))}; doc[key].append(item); continue
        m = re.fullmatch(r"    ([A-Za-z_][\w-]*):(.*)", line)
        if m and item is not None:
            item[m.group(1)] = _value(m.group(2)); continue
        raise ValueError(f"line {n}: unsupported YAML: {raw!r}")
    return doc

def _dump_scalar(v):
    if isinstance(v, bool): return "true" if v else "false"
    if v is None: return "null"
    if isinstance(v, (int, float)): return str(v)
    s = str(v)
    if s == "" or re.search(r"^[\s\-\[\]{}&*!|>%@`'\"?]|[:#,]\s|[:,]$|^\d|^(true|false|null|~)$", s, re.I) or "#" in s or ":" in s:
        return "'" + s.replace("'", "''") + "'"
    return s

def dump_item(d):
    out = []
    for i, (k, v) in enumerate(d.items()):
        val = "[" + ", ".join(_dump_scalar(x) for x in v) + "]" if isinstance(v, list) else _dump_scalar(v)
        out.append(f"{'  - ' if i == 0 else '    '}{k}: {val}")
    return "\n".join(out)
