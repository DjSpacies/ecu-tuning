"""Translate PCLink logs and tunes into the normalised models. The only ECU-specific entry point the core calls."""
import re, sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[2]
sys.path[:0] = [str(HERE), str(ROOT / "tools" / "log-schema"), str(ROOT / "tools" / "glossary")]
import llg, pclr, miniyaml     # noqa: E402
from schema import Log, Table  # noqa: E402

PSI_KPA = 6.894757

def _config(name):
    text = (HERE.parent / name).read_text(encoding="utf8")
    if name == "channels.yaml":   # the flat `limiters:` list sits outside the subset's mapping lists
        head, _, tail = text.partition("\nlimiters:")
        return miniyaml.load(head), [x.strip() for x in tail.strip(" []\n").split(",")]
    return miniyaml.load(text), None

def _convert(rule, unit, values, notes, native):
    if rule == "by_unit_pressure":
        if unit.upper() == "PSI": return [v * PSI_KPA for v in values]
        if unit.lower() == "kpa": return list(values)
        if unit == "Pressure":   # newer logs name the quantity, not the unit; the values seen are kPa (see formats.md)
            notes.append(f"{native}: unit stored as the quantity 'Pressure'; read as kPa, checked against barometric pressure")
            return list(values)
        raise ValueError(f"unknown pressure unit '{unit}' on {native}")
    if rule == "by_unit_lambda":
        active = sorted(v for v in values if v > 0)
        typical = active[len(active) // 2] if active else 0
        if unit.upper() == "AFR" or typical > 3:   # lambda never reaches 3; a blank unit with values like 12 is an AFR display
            notes.append(f"{native}: treated as an AFR display (unit '{unit}', typical value {typical:.1f}) and converted using a 14.7 scale; that scale is an assumption about the sensor's calibration")
            return [v / 14.7 for v in values]
        return list(values)
    return list(values)

HOLE_S = 1.0   # no channel recorded anything for this long: treated as a recording hole (e.g. ECU reconnect), not held

def _resample(raw, notes):
    """Newer logs record each channel only on change. Put every channel on one grid at the logging interval, holding the
    last recorded value, and drop grid points inside recording holes so a held value never stands in for missing data."""
    import bisect
    dt = min(c["interval_s"] for c in raw.values() if c["interval_s"] > 0)
    t0 = max(c["times"][0] for c in raw.values()); t1 = min(c["times"][-1] for c in raw.values())
    every = sorted({t for c in raw.values() for t in c["times"]})
    holes = [(a, b) for a, b in zip(every, every[1:]) if b - a > HOLE_S]
    grid, i, k = [], 0, 0
    while (t := t0 + i * dt) <= t1:
        while k < len(holes) and holes[k][1] <= t: k += 1
        if not (k < len(holes) and holes[k][0] < t < holes[k][1]): grid.append(round(t, 6))
        i += 1
    out = {}
    for name, c in raw.items():
        ts, vs = c["times"], c["values"]
        out[name] = dict(c, times=grid, values=[vs[max(0, bisect.bisect_right(ts, g) - 1)] for g in grid])
    notes.append(f"channels recorded on change; resampled to {1/dt:.0f} Hz holding the last value; {len(holes)} recording hole(s) over {HOLE_S} s left out")
    return out

def load_log(path):
    parsed = llg.parse_llg(path); raw = parsed["channels"]
    cfg, limiters = _config("channels.yaml")
    channels, used, notes = {}, {}, []
    recorded = {k: len(c["values"]) for k, c in raw.items()}
    if parsed.get("format") == "lf3": raw = _resample(raw, notes)
    base = raw.get("Engine Speed")
    if base is None: raise ValueError("log has no engine speed channel")
    times, n = base["times"], len(base["times"])
    for rule in cfg["channels"]:
        rx = re.compile(rule["match"], re.I)
        # A channel declared but never recorded holds two samples; prefer computed channels over raw "AN" inputs.
        hits = [k for k in raw if rx.search(k) and recorded[k] > 2]
        if not hits: continue
        k = min(hits, key=lambda h: (h.startswith("AN"), -recorded[h])); c = raw[k]
        if len(c["values"]) != n: notes.append(f"{k}: sample count differs, skipped"); continue
        channels[rule["canonical"]] = _convert(rule["convert"], c["unit"], c["values"], notes, k)
        used[rule["canonical"]] = k
    # A limiter name can also be declared for its setpoint (e.g. a MAP limit of 235); only small-integer status columns count.
    cands = [k2 for k in limiters for k2 in raw if k2 == k or k2.startswith(k + " #")]
    lim = [raw[k]["values"] for k in cands if len(raw[k]["values"]) == n and all(v == int(v) and 0 <= v <= 15 for v in raw[k]["values"])]
    if lim: channels["limiter_active"] = [any(col[i] for col in lim) for i in range(n)]
    if "baro_kpa" in channels and any(used.get(c) and raw[used[c]]["unit"] == "Pressure" for c in channels):
        b = sorted(channels["baro_kpa"])[len(channels["baro_kpa"]) // 2]
        if not 60 <= b <= 110: raise ValueError(f"pressure channels do not read as kPa (barometric median {b:.1f})")
    meta = dict(native_names=used, notes=notes, adapter="link-g4plus", unmapped=sorted(set(raw) - set(used.values())))
    # The first sample in the logs seen can be all zero, before the ECU has data.
    keep = [i for i in range(n) if channels["rpm"][i] or i > 0]
    return Log([times[i] for i in keep], {k: [v[i] for i in keep] for k, v in channels.items()}, meta)

def _trim_axis(ax):
    """Used zones of an axis: the leading strictly increasing part (unused zones repeat a filler value)."""
    out = [ax[0]]
    for v in ax[1:]:
        if v <= out[-1]: break
        out.append(v)
    return out

def tune_tables(tune):
    cfg, _ = _config("tables.yaml")
    out = {}
    for t in cfg["tables"]:
        i = t["id"]
        if i not in tune["tables"]: continue
        x = tune["tables"].get(t["x_labels"]); y = tune["tables"].get(t["y_labels"])
        if not x or not y: continue
        xs, ys = _trim_axis(x[0]), _trim_axis(y[0])
        if len(xs) < 2 or len(ys) < 2: continue     # an unconfigured table has flat filler axes
        values = [row[:len(xs)] for row in tune["tables"][i][:len(ys)]]
        y_channel = "mgp_kpa" if min(ys) < 0 else "map_kpa"
        out[t["role"]] = Table(t["role"], xs, ys, values, t["unit"], "rpm", y_channel, t["native"])
    return out

def load_tune(path, key=None, exe=None):
    tune = pclr.parse_tune(path, key=key, exe=exe)
    cfg, _ = _config("tables.yaml")
    scalars = {s["name"]: tune["scalars"].get(s["id"]) for s in cfg["scalars"]}
    # Single-row tables; their axes are not 2D, so they stay as raw rows.
    arrays = {a["name"]: tune["tables"][a["id"]][0] for a in cfg["arrays"] if a["id"] in tune["tables"]}
    def active(name): return [v for v in arrays.get(name, []) if v > 0]
    protections = {"rpm_limit": max(active("rpm_limit"), default=None), "map_limit_kpa": max(active("map_limit_kpa"), default=None)}
    return dict(meta=tune["meta"], scalars=scalars, tables=tune_tables(tune), arrays=arrays, protections=protections)
