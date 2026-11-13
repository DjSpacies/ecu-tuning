"""Read-only parser for PCLink ECU-log files (.llg). Layout is sample-observed; see ../formats.md.

The file holds one record per channel: a 32-bit id, a UTF-16 name, a UTF-16 unit, a 64-bit logging interval in seconds,
then (float32 value, float32 time) pairs. Field offsets differ between the two files seen, so the parser finds each
part by content and raises ValueError when it cannot.
"""
import re, struct
from pathlib import Path

NAME_RX = re.compile(rb"(?:[\x20-\x7e]\x00){2,}")
MAGIC = b"lf2"   # the next byte differs between files (0x43, 0x13)
MAGIC3 = b"lf3"  # newer PCLink builds (seen from 5.6.8): a chain of tagged blocks, see ../formats.md

def _parse_lf3(b):
    """Walk [u32 size][3-byte tag] blocks. 'ds3' is a channel: size covers its header only, then u32 count at +7,
    id u32 at +0xd3, UTF-16 name at +0xd7 and unit at +0x19f (200 bytes each), interval double at +0x26c, then
    count (time, value) float32 pairs, logged on change. Raises ValueError if the chain does not end exactly at EOF."""
    o, channels, info, skipped = 0, {}, [], []
    txt = lambda a: b[a:a + 200].decode("utf-16le", "replace").split("\0")[0].strip()
    while o + 11 <= len(b):
        size, tag = struct.unpack_from("<I", b, o)[0], b[o + 4:o + 7]
        if size < 7 or not tag[:2].isalpha(): raise ValueError(f"block chain broken at {o:#x}")
        if tag == b"ds3":
            n = struct.unpack_from("<I", b, o + 7)[0]
            name, unit = txt(o + 0xd7), txt(o + 0x19f)
            cid = struct.unpack_from("<I", b, o + 0xd3)[0]
            dt = struct.unpack_from("<d", b, o + 0x26c)[0]
            p = o + size
            if p + 8 * n > len(b): raise ValueError(f"channel {name!r} runs past the end of the file")
            pairs = [struct.unpack_from("<ff", b, p + 8 * i) for i in range(n)]
            rec = dict(id=cid, unit=unit, interval_s=dt, times=[t for t, _ in pairs], values=[v for _, v in pairs])
            if n == 0: skipped.append(name)
            elif name not in channels: channels[name] = rec
            else:   # the same name is declared twice; the plain name goes to the one that recorded more
                if n > len(channels[name]["values"]): channels[name], rec = rec, channels[name]
                channels[f"{name} #{rec['id']}"] = rec
            o = p + 8 * n
        else:
            if tag in (b"ld2", b"lm1"):
                info += [m.group().decode("utf-16le") for m in NAME_RX.finditer(b, o + 7, o + size)]
            o += size
    if o != len(b): raise ValueError("block chain does not end at the end of the file")
    if not channels: raise ValueError("no channels found")
    return dict(channels=channels, info=info, skipped=skipped, format="lf3")

def _pairs_at(b, o, interval):
    """Number of (value, time) pairs at offset o whose times step by the interval, 0 if it does not look like data."""
    n, last, step = 0, None, max(interval, 1e-4)
    while o + 8 <= len(b):
        v, t = struct.unpack_from("<ff", b, o + 8 * n)
        if not (t == t and v == v) or abs(v) > 1e9 or t < 0: break
        if last is not None and not (0 < t - last < step * 2000): break
        last = t; n += 1
        if o + 8 * (n + 1) > len(b): break
    return n

def _find_data(b, start, limit):
    """Locate the interval (a double 0 < x < 2 s) and the longest run of pairs following it; alignment varies by file."""
    for o in range(start, min(limit, len(b) - 8)):
        dt = struct.unpack_from("<d", b, o)[0]
        if not 1e-4 < dt < 2.0 or round(dt, 4) != round(dt, 12): continue
        best = (0, 0)
        for skip in range(8, 80):
            p = o + skip
            if p + 16 > len(b): break
            n = _pairs_at(b, p, dt)
            if n > best[0] and abs(struct.unpack_from("<f", b, p + 12)[0] - struct.unpack_from("<f", b, p + 4)[0] - dt) < dt * 0.5:
                best = (n, p)
        if best[0] >= 2: return dt, best[1], best[0]
    raise ValueError("could not locate channel data")

def parse_llg(path):
    """Return {'channels': {name: dict(id, unit, interval_s, times, values)}, 'info': [strings from the header]}."""
    b = Path(path).read_bytes()
    if b[4:7] == MAGIC3: return _parse_lf3(b)
    if b[4:7] != MAGIC: raise ValueError("not a recognised log file (magic differs)")
    strings = [(m.start(), m.group().decode("utf-16le")) for m in NAME_RX.finditer(b[:16384])]
    sol = next((i for i, (_, s) in enumerate(strings) if s == "1EOL"), None)
    if sol is None: raise ValueError("end of the marker list not found")
    info = [s for _, s in strings[:sol + 1]]
    first = strings[sol + 1][0] - 4
    channels, pos = {}, first
    skipped = []
    while pos + 16 < len(b):
        m = NAME_RX.match(b, pos + 4)
        if m is None: break
        name_at, name = m.start(), m.group().decode("utf-16le").strip()
        # Newer files hold the name twice, 204 bytes apart, the second preceded by the channel id.
        again = NAME_RX.match(b, name_at + 204)
        if again and again.group().decode("utf-16le").strip() == name: name_at = again.start()
        cid = struct.unpack_from("<I", b, name_at - 4)[0]
        if cid > 100000: break
        um = NAME_RX.match(b, name_at + 200)
        unit = um.group().decode("utf-16le").strip() if um else ""
        ustart = name_at + 400
        try:
            dt, p, n = _find_data(b, ustart, ustart + 300)
        except ValueError:           # a channel can be declared with no samples
            skipped.append(name)
            nxt = NAME_RX.search(b, ustart, ustart + 2048)
            if nxt is None: break
            pos = nxt.start() - 4
            continue
        vals = [struct.unpack_from("<ff", b, p + 8 * i) for i in range(n)]
        channels[name] = dict(id=cid, unit=unit, interval_s=dt, values=[v for v, _ in vals], times=[t for _, t in vals])
        end = p + 8 * n
        nxt = NAME_RX.search(b, end, end + 2048)
        if nxt is None: break
        pos = nxt.start() - 4
    if not channels: raise ValueError("no channels found")
    return dict(channels=channels, info=info, skipped=skipped)
