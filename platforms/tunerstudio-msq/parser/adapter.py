"""Translate TunerStudio .msq tunes (Speeduino, rusEFI, MegaSquirt) into the normalised Table model.

Table and axis names per family come from the files seen (see ../README.md). Logs (.mlg/.msl) are not read yet.
"""
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[2]
sys.path[:0] = [str(HERE), str(ROOT / "tools" / "log-schema")]
import msq                     # noqa: E402
from schema import Table       # noqa: E402

# role: (table, x bins, y bins) per family; the first name set present wins.
MAP = {
    "speeduino": {"ve": [("veTable", "rpmBins", "fuelLoadBins")], "ve_2": [("veTable2", "rpmBins4", "fuelLoadBins2")],
                  "ign_base": [("advTable1", "rpmBins2", "mapBins1")], "lambda_target": [("afrTable", "rpmBinsAFR", "loadBinsAFR")],
                  "boost_target": [("boostTable", "rpmBinsBoost", "tpsBinsBoost")]},
    "rusefi": {"ve": [("veTable", "veRpmBins", "veLoadBins")], "ign_base": [("ignitionTable", "ignitionRpmBins", "ignitionLoadBins")],
               "lambda_target": [("lambdaTable", "lambdaRpmBins", "lambdaLoadBins")], "boost_target": [("boostTableOpenLoop", "boostRpmBins", "boostTpsBins")]},
    "megasquirt": {"ve": [("veTable1", "frpm_table1", "fmap_table1")], "ign_base": [("advanceTable1", "srpm_table1", "smap_table1")],
                   "lambda_target": [("afrTable1", "arpm_table1", "amap_table1")]},
}
SCALARS = {
    "speeduino": dict(stoich_ratio="stoich", cylinders="nCylinders", req_fuel_ms="reqFuel", load_algorithm="algorithm", rpm_limit=("hardRevLim", "HardRevLim"), injector_open_ms="injOpen"),
    "rusefi": dict(stoich_ratio="stoichRatioPrimary", cylinders="cylindersCount", displacement_l="displacement", load_algorithm="fuelAlgorithm", rpm_limit="rpmHardLimit", injector_flow_ccmin="injector_flow"),
    "megasquirt": dict(stoich_ratio="stoich", cylinders="nCylinders", req_fuel_ms="reqFuel", load_algorithm="algorithm1", rpm_limit="RevLimNormal2"),
}

def _flat(v): return [r[0] if isinstance(r, list) else r for r in v] if isinstance(v, list) else None

def _y_channel(fam, s, role, ybins_units):
    alg = str(s.get("load_algorithm", "")).lower()
    if role == "boost_target": return "tps"
    if ybins_units == "%" or "tps" in alg or "alpha" in alg: return "tps"
    return "map_kpa"

def load_tune(path, **_):
    d = msq.parse_msq(path); fam = msq.family(d["signature"]); c = d["constants"]
    if fam == "unknown": raise ValueError(f"unrecognised TunerStudio signature '{d['signature'][:40]}'")
    scal = {}
    for k, names in SCALARS[fam].items():
        for n in (names if isinstance(names, tuple) else (names,)):
            if n in c: scal[k] = c[n]["value"]; break
    tables, notes = {}, []
    for role, opts in MAP[fam].items():
        for tname, xn, yn in opts:
            if not all(n in c for n in (tname, xn, yn)): continue
            vals, xa, ya = c[tname]["value"], _flat(c[xn]["value"]), _flat(c[yn]["value"])
            if not (isinstance(vals, list) and xa and ya): continue
            if vals and not isinstance(vals[0], list):   # older files omit rows/cols: reshape only if the sizes agree
                if len(vals) != len(xa) * len(ya): notes.append(f"{tname}: flat array does not fit its bins; left out"); continue
                vals = [vals[i * len(xa):(i + 1) * len(xa)] for i in range(len(ya))]
            # Unused trailing bins repeat or fall; keep the leading increasing part and trim the table to match.
            nx = next((i for i in range(1, len(xa)) if xa[i] <= xa[i - 1]), len(xa)); ny = next((i for i in range(1, len(ya)) if ya[i] <= ya[i - 1]), len(ya))
            rows = [r[:nx] for r in vals[:ny]]
            unit = c[tname]["units"]
            if role == "lambda_target":
                flat = [v for r in rows for v in r]
                if flat and sorted(flat)[len(flat) // 2] > 3:   # stored as AFR: convert with the tune's own ratio
                    st = float(scal.get("stoich_ratio") or 0)
                    if not st: notes.append(f"{tname}: AFR values with no stoichiometric ratio; left out"); break
                    rows = [[v / st for v in r] for r in rows]; unit = "lambda"
                    notes.append(f"{tname}: AFR converted to lambda with the tune's ratio {st}")
            try:
                tables[role] = Table(role, xa[:nx], ya[:ny], rows, unit, "rpm", _y_channel(fam, scal, role, c[yn]["units"]), tname)
            except ValueError as e:
                notes.append(f"{tname}: {e}")
            break
    prot = {"rpm_limit": float(scal["rpm_limit"]) if isinstance(scal.get("rpm_limit"), float) else None, "map_limit_kpa": None}
    return dict(tables=tables, scalars=scal, protections=prot, meta=dict(adapter="tunerstudio-msq", family=fam, firmware=d["firmware"], notes=notes))

def load_log(path):
    raise ValueError("TunerStudio logs (.mlg/.msl) are not supported yet; tunes only")
