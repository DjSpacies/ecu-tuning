"""Read-only parser for PCLink tune files. Never writes a tune (docs/PLATFORM-ADAPTERS.md requires verification first).

A .pclr file is an encoded container around a LinkStorage XML document; see ../formats.md. The decoding key is the
vendor's and is not stored here: pass `key` (four uint32) or `exe` (a local PCLink.exe to read it from), or give an
already decoded XML document.
"""
import struct
import xml.etree.ElementTree as ET
from pathlib import Path

MASK, DELTA = 0xFFFFFFFF, 0x9E3779B9
KEY_VA = 0x0094DD3C          # re-derived; see ../formats.md

def key_from_exe(exe):
    """Read the key from the build of PCLink.exe that was analysed, by mapping the virtual address through its sections."""
    b = Path(exe).read_bytes()
    pe = struct.unpack_from("<I", b, 0x3C)[0]
    count = struct.unpack_from("<H", b, pe + 6)[0]; opt = struct.unpack_from("<H", b, pe + 20)[0]
    base = struct.unpack_from("<I", b, pe + 24 + 28)[0]
    for i in range(count):
        size, rva, _, off = struct.unpack_from("<IIII", b, pe + 24 + opt + 40 * i + 8)
        if base + rva <= KEY_VA and KEY_VA + 16 <= base + rva + size:
            return struct.unpack_from("<4I", b, off + KEY_VA - base - rva)
    raise ValueError("key address is not in this executable")

def _mix(z, y, total, p, e, key):
    return (((z >> 5 ^ (y << 2) & MASK) + (y >> 3 ^ (z << 4) & MASK)) ^ ((total ^ y) + (key[(p & 3) ^ e] ^ z))) & MASK

def _decode_words(v, key):
    n = len(v)
    if n < 2: raise ValueError("container too short")
    rounds = 6 + 52 // n
    total = (rounds * DELTA) & MASK
    y = v[0]
    while total:
        e = (total >> 2) & 3
        for p in range(n - 1, 0, -1):
            z = v[p - 1]; v[p] = (v[p] - _mix(z, y, total, p, e, key)) & MASK; y = v[p]
        z = v[n - 1]; v[0] = (v[0] - _mix(z, y, total, 0, e, key)) & MASK; y = v[0]
        total = (total - DELTA) & MASK
    return v

def decode_container(data, key):
    if len(data) < 16 or len(data) % 4: raise ValueError("container length is not a whole number of words")
    words = _decode_words(list(struct.unpack(f"<{len(data) // 4}I", data)), key)
    plain = struct.pack(f"<{len(words)}I", *words)
    size = struct.unpack_from("<I", plain, 4)[0]
    if size > len(plain) - 12: raise ValueError("decoded length exceeds the container")
    return plain[12: 12 + size]

def _rows(el): return [[float(x) for x in c.attrib["Value"].split(",") if x != ""] for c in el if c.tag.startswith("Row")]

def parse_xml(text):
    if isinstance(text, bytes): text = text.decode("utf8", errors="replace")
    if "<!DOCTYPE" in text.upper() or "<!ENTITY" in text.upper(): raise ValueError("DTD or entity declarations are refused")
    # One vendor sample holds character references that XML 1.0 rejects, in a label field.
    root = ET.fromstring(text.replace("&#03;", " ").replace("&#23;", " "))
    if root.tag != "LinkStorage": raise ValueError("not a LinkStorage document")
    meta = {c.tag: c.attrib.get("Value") for c in root.find("Memory")}
    scalars, tables = {}, {}
    for el in root.find("Map"):
        i = int(el.attrib["DataId"])
        if "RowCount" in el.attrib: tables[i] = _rows(el)
        else: scalars[i] = el.attrib.get("Value")
    return dict(meta=meta, scalars=scalars, tables=tables)

def parse_tune(path, key=None, exe=None):
    p = Path(path); data = p.read_bytes()
    if data[:5] == b"<?xml" or p.suffix.lower() == ".xml": return parse_xml(data)
    if key is None:
        if exe is None: raise ValueError("a .pclr file needs the decoding key or a local PCLink.exe")
        key = key_from_exe(exe)
    return parse_xml(decode_container(data, key))
