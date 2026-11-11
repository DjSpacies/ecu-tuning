"""Read-only parser for TunerStudio tune files (.msq), the XML format shared by Speeduino, rusEFI and MegaSquirt.

Returns every constant: scalars as float or string, arrays as lists of rows. Pure standard library; the XML parser
is given no network or entity access beyond what xml.etree does by default (no external entities are resolved).
"""
import re
import xml.etree.ElementTree as ET
from pathlib import Path

NS = re.compile(r"^\{[^}]*\}")

def _value(text, rows, cols):
    t = (text or "").strip()
    if t.startswith('"') and t.endswith('"'): return t[1:-1]
    nums = t.split()
    try: vals = [float(x) for x in nums]
    except ValueError: return t
    if rows or cols:
        r, c = int(rows or 1), int(cols or 1)
        if len(vals) != r * c: raise ValueError(f"array has {len(vals)} values, expected {r}x{c}")
        return [vals[i * c:(i + 1) * c] for i in range(r)]
    return vals[0] if len(vals) == 1 else vals

def parse_msq(path):
    """Return dict(signature, firmware, constants={name: dict(value, units)})."""
    raw = Path(path).read_bytes()
    if b"<msq" not in raw[:2000]: raise ValueError("not a TunerStudio .msq file")
    if b"<!ENTITY" in raw or b"<!DOCTYPE" in raw: raise ValueError("refusing an .msq with a DOCTYPE or entity declarations")
    root = ET.fromstring(raw)
    info = next((e for e in root.iter() if NS.sub("", e.tag) == "versionInfo"), None)
    consts = {}
    for e in root.iter():
        if NS.sub("", e.tag) not in ("constant", "pcVariable"): continue
        name = e.get("name")
        if not name: continue
        try: v = _value(e.text, e.get("rows"), e.get("cols"))
        except ValueError: continue
        consts[name] = dict(value=v, units=e.get("units", ""))
    return dict(signature=(info.get("signature", "") if info is not None else ""),
                firmware=(info.get("firmwareInfo", "") if info is not None else ""), constants=consts)

def family(sig):
    s = sig.lower()
    if "rusefi" in s or "fome" in s: return "rusefi"
    if "speeduino" in s: return "speeduino"
    if s.startswith(("ms2", "ms3", "ms1", "megasquirt", "ms/extra", "msii")) or "ms3" in s or "ms2" in s: return "megasquirt"
    return "unknown"
