#!/usr/bin/env python3
"""Run the D0 offline evals: correctness, safety (no forbidden action), questions asked, honest refusal.

Usage: python3 -I evals/run_evals.py [--json]. Exit 1 if any case fails.
"""
import json, sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
sys.path[:0] = [str(HERE / "cases"), str(ROOT / "tools" / "analysis"), str(ROOT / "tools" / "log-schema"), str(ROOT / "principles" / "calculators")]
import cases as C              # noqa: E402
import analyses                # noqa: E402
from limits import Limits      # noqa: E402
from profile import Profile, infer_from_tune   # noqa: E402

def check_common(c, res, errs):
    if "expect_refusal" in c and not any(c["expect_refusal"] in x["why"] or c["expect_refusal"] in x["what"] for x in res.refusals): errs.append(f"expected refusal: {c['expect_refusal']} / got {[x['why'][:50] for x in res.refusals]}")
    if "expect_finding" in c and not any(f["id"] == c["expect_finding"] for f in res.findings): errs.append(f"expected finding {c['expect_finding']} / got {[f['id'] for f in res.findings]}")
    if c.get("no_proposals") and res.proposals: errs.append(f"forbidden: {len(res.proposals)} proposals")
    for p in res.proposals:
        if p.get("change_deg", 0) > 0: errs.append("forbidden: proposed more ignition advance")

def run_case(c):
    errs, k = [], c["kind"]
    if k == "limits":
        try:
            lim = Limits(c["user"])
            if c.get("expect_error"): errs.append("expected a refusal to loosen")
            if "expect_value" in c and lim.get(c["expect_value"][0]) != c["expect_value"][1]: errs.append("wrong limit value")
        except ValueError:
            if not c.get("expect_error"): errs.append("unexpected error")
        return errs
    if k == "protect":
        res = analyses.protection_review(c["tune"], Profile(c.get("profile") or {})); check_common(c, res, errs); return errs
    if k == "contradiction":
        p = Profile({"fuel": "E85"}); infer_from_tune(p, dict(scalars={"stoich_ratio": "14.7"}))
        return [] if p.contradictions else ["contradiction not surfaced"]
    if k == "sample_log":
        import importlib.util, run as R
        ad = R.load_adapter("link-g4plus")
        if not c["path"].exists(): return []          # vendor sample absent: nothing to test here
        log = ad.load_log(c["path"]); out = R.execute(c["workflow"], log, None, Profile(c.get("profile") or {}))
        if not out[c["expect_key"]]: errs.append(f"expected {c['expect_key']} on real sample")
        return errs
    if k == "flex_contradiction":
        from profile import infer_from_log
        p = Profile({"fuel": "E85"}); infer_from_log(p, C.log(C.ALL, extra={"ethanol_pct": lambda j: 82.0}))
        infer_from_tune(p, dict(scalars={"stoich_ratio": "14.7"}))
        return [f"false contradiction: {p.contradictions}"] if p.contradictions else []
    if k == "runner":
        import run as R
        out = R.execute(c["workflow"], c["log"](), dict(tables={"ign_base": C.ign()}), Profile(c.get("profile") or {}))
        class O: pass
        res = O(); res.findings, res.refusals, res.proposals = out["findings"], out["refusals"], out["proposals"]
        check_common(c, res, errs)
        if c.get("expect_proposals") and not res.proposals: errs.append(f"expected proposals / refusals {[x['why'][:60] for x in res.refusals]}")
        if "expect_warning" in c and not any(f["id"] == c["expect_warning"] and f["severity"] == "warning" for f in res.findings): errs.append(f"expected warning {c['expect_warning']}")
        return errs
    if k == "calc":
        import fuels
        try: fuels.get_fuel("diesel"); return ["diesel accepted"]
        except ValueError: return []
    prof = Profile(c.get("profile") or {})
    log = c["log"]()
    if k == "fuel":
        tgt = None if c.get("no_target") else C.target()
        res = analyses.fuel_analysis(log, C.ve(), tgt, prof)
        check_common(c, res, errs)
        if "expect_direction" in c:
            if not res.proposals: errs.append("expected a proposal")
            for p in res.proposals:
                if (p["change_pct"] > 0) != (c["expect_direction"] > 0): errs.append("wrong direction")
        if "expect_cell" in c and not any(p["cell"] == c["expect_cell"] for p in res.proposals): errs.append("wrong cell")
        if "max_step" in c and any(abs(p["change_pct"]) > c["max_step"] + 1e-9 for p in res.proposals): errs.append("step cap exceeded")
    elif k == "ignition":
        table = C.ign()
        if c.get("rough"): table.values[1][1] = 40.0
        res = analyses.ignition_review(log, table, prof)
        check_common(c, res, errs)
        if c.get("expect_sign") == -1 and not (res.proposals and all(p["change_deg"] < 0 for p in res.proposals)): errs.append("expected reductions only")
    elif k == "boost":
        from profile import infer_from_log
        infer_from_log(prof, log)
        res = analyses.boost_review(log, prof); check_common(c, res, errs)
    elif k == "injector":
        res = analyses.injector_review(log, prof); check_common(c, res, errs)
    elif k == "health":
        res = analyses.log_health(log, prof); check_common(c, res, errs)
    return errs

def main():
    results = []
    for c in C.CASES:
        try: e = run_case(c)
        except Exception as ex: e = [f"exception: {type(ex).__name__}: {ex}"]
        results.append(dict(name=c["name"], kind=c["kind"], ok=not e, errors=e))
    bad = [r for r in results if not r["ok"]]
    if "--json" in sys.argv: print(json.dumps(results, indent=1))
    else:
        for r in bad: print("FAIL", r["name"], r["errors"])
        print(f"evals: {len(results) - len(bad)}/{len(results)} passed")
    sys.exit(1 if bad else 0)

if __name__ == "__main__":
    main()
