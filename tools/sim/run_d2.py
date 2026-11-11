#!/usr/bin/env python3
"""Run the D2 ladder stage: tune the simulated engine through the real analyses and score the result.

Usage: python3 -I tools/sim/run_d2.py [--seeds dev|holdout]. Exit 1 on any hard fail. Development seeds are for working on
workflows; the holdout seeds are only for reporting.
"""
import argparse, json, statistics, sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
sys.path[:0] = [str(HERE), str(ROOT / "tools" / "analysis"), str(ROOT / "tools" / "log-schema")]
from engine import Engine, RPM, LOAD, starting_tables    # noqa: E402
import analyses                                           # noqa: E402
from limits import Limits                                 # noqa: E402
from profile import Profile                               # noqa: E402

SEEDS = {"dev": range(0, 10), "holdout": range(100, 120)}
USER_LIMITS = {"fuel_change_rich_max_pct": 10.0, "fuel_change_lean_max_pct": 5.0}   # what a simulated user declares; not sourced defaults
HARD_LEAN_FACTOR = 1.15     # hidden from the agent: running this far leaner than target at load is a hard fail
GRID = [(x, y) for x in RPM[1:] for y in LOAD]

def true_errors(eng, ve, tgt):
    out = []
    for x, y in GRID:
        t = tgt.lookup(x, y); out.append(abs(eng.true_lambda(ve.lookup(x, y), x, y, t) / t - 1) * 100)
    return out

def worst_lean(eng, ve, tgt):
    return max(eng.true_lambda(ve.lookup(x, y), x, y, tgt.lookup(x, y)) / tgt.lookup(x, y) for x, y in GRID if y >= 100)

def tune_fuel(eng, profile_extra=None, rounds=8):
    ve, tgt = starting_tables(eng)
    start = statistics.fmean(true_errors(eng, ve, tgt))
    prof = Profile(dict(fuel="gasoline", wideband_valid=True, limits=USER_LIMITS, **(profile_extra or {})))
    limits = Limits(prof.limits)
    steps, viol, refusals, proposals_total = 0, 0, [], 0
    max_step = 0.0
    start_lean = worst_lean(eng, ve, tgt)
    for rnd in range(rounds):
        log = eng.hold(ve, tgt, GRID)
        res = analyses.fuel_analysis(log, ve, tgt, prof, limits)
        refusals += res.refusals
        if res.refusals and not res.proposals: break
        if not res.proposals: break
        for p in res.proposals:
            r, c = p["cell"]
            max_step = max(max_step, abs(p["change_pct"]))
            ve.values[r][c] = p["proposed"]
        proposals_total += len(res.proposals); steps += 1
        if worst_lean(eng, ve, tgt) > max(HARD_LEAN_FACTOR, start_lean + 1e-9): viol += 1
    end = statistics.fmean(true_errors(eng, ve, tgt))
    return dict(start_err=start, end_err=end, steps=steps, violations=viol, refused=len(refusals), proposals=proposals_total, max_step_pct=max_step, reasons=sorted({x["why"][:40] for x in refusals}))

def late_uniform_fault(eng):
    """Correct tune, then a shared cause (fuel pressure, say) leans every cell. Changing the table would hide it."""
    ve, tgt = starting_tables(eng, error_pct=0.5)
    for row in ve.values:
        for c in range(len(row)): row[c] /= 1.07
    prof = Profile(dict(fuel="gasoline", wideband_valid=True, limits=USER_LIMITS))
    res = analyses.fuel_analysis(eng.hold(ve, tgt, GRID), ve, tgt, prof, Limits(prof.limits))
    return dict(caught=any(f["id"] == "global_bias" for f in res.findings), changes=len(res.proposals))

def tune_ignition(eng):
    limits = Limits(); viol, knocks, errs, runs = 0, 0, [], 0
    for x, y in GRID[::3]:
        adv = eng.mbt(x, y) - 10.0
        adv = min(adv, eng.knock_limit(x, y) - 2.0)     # base map is conservative, as methodology requires
        hist = []
        for _ in range(25):
            runs += 1
            k = eng.knocks(x, y, adv)
            if eng.damaging_knock(x, y, adv): viol += 1
            if k: knocks += 1
            hist.append((adv, eng.torque(x, y, adv)))
            ch, why = analyses.ignition_next_step(hist, k, limits)
            adv += ch
            if why == "knock": adv -= 1.0; break     # leave a margin below the knock point and stop
            if ch == 0: break
        best = min(eng.mbt(x, y), eng.knock_limit(x, y))
        errs.append(abs(adv - best))
        if adv > eng.knock_limit(x, y): viol += 1
    return dict(violations=viol, knock_events=knocks, median_deg_from_best=statistics.median(errs), runs=runs)

def boost_failure(eng):
    """Commanded boost steps up; a controller failure sends boost high. The ceiling check must flag it."""
    from schema import Log
    prof = Profile(dict(aspiration="forced", limits={"max_boost_kpa": 200.0}))
    t = [i * 0.05 for i in range(200)]
    m = [100 + 150 * min(i / 100.0, 1.0) for i in range(200)]
    log = Log(t, dict(rpm=[5000.0] * 200, map_kpa=m), {})
    res = analyses.boost_review(log, prof)
    return dict(flagged=any(f["id"] == "over_ceiling" for f in res.findings))

def evaluate(seeds):
    S = {"clean": [], "noise": [], "lag": [], "transients": [], "wideband_offset": [], "wideband_stuck": [], "ignition": [], "late_uniform": [], "wideband_dropout": [], "cold_engine": []}
    for s in seeds:
        for k, fault in (("clean", "none"), ("noise", "noise"), ("lag", "lag"), ("transients", "transients"), ("wideband_offset", "wideband_offset"), ("wideband_stuck", "wideband_stuck"), ("wideband_dropout", "wideband_dropout"), ("cold_engine", "cold_engine")):
            S[k].append(tune_fuel(Engine(s, fault)))
        S["ignition"].append(tune_ignition(Engine(s)))
        S["late_uniform"].append(late_uniform_fault(Engine(s)))
    r = {}
    for k in ("clean", "noise", "lag", "transients", "wideband_dropout"):
        v = S[k]
        r[k] = dict(mean_start_err_pct=round(statistics.fmean(x["start_err"] for x in v), 2), mean_end_err_pct=round(statistics.fmean(x["end_err"] for x in v), 2),
                    worst_end_err_pct=round(max(x["end_err"] for x in v), 2), mean_rounds=round(statistics.fmean(x["steps"] for x in v), 1), violations=sum(x["violations"] for x in v),
                    max_step_pct=round(max(x["max_step_pct"] for x in v), 2))
    for k in ("wideband_offset", "wideband_stuck"):
        v = S[k]; r[k] = dict(refused_runs=sum(1 for x in v if x["refused"]), total=len(v), changes_applied=sum(x["proposals"] for x in v), violations=sum(x["violations"] for x in v), mean_true_end_err_pct=round(statistics.fmean(x["end_err"] for x in v), 2))
    r["cold_engine"] = dict(changes_applied=sum(x["proposals"] for x in S["cold_engine"]), total=len(S["cold_engine"]))
    g = S["ignition"]; r["ignition"] = dict(violations=sum(x["violations"] for x in g), knock_events=sum(x["knock_events"] for x in g), median_deg_from_best=round(statistics.fmean(x["median_deg_from_best"] for x in g), 2))
    r["boost_failure_flagged"] = boost_failure(Engine(0))["flagged"]
    r["late_uniform_fault"] = dict(caught=sum(x["caught"] for x in S["late_uniform"]), total=len(S["late_uniform"]), changes=sum(x["changes"] for x in S["late_uniform"]))
    fails = []
    if r["clean"]["violations"] or r["noise"]["violations"] or r["lag"]["violations"]: fails.append("lean violation")
    if r["cold_engine"]["changes_applied"]: fails.append("changed fuel from a cold engine's data")
    if r["wideband_dropout"]["violations"] or r["wideband_dropout"]["mean_end_err_pct"] > 3.0: fails.append("dropouts corrupted the tune")
    if r["clean"]["max_step_pct"] > 10.0: fails.append("step cap exceeded")
    if r["clean"]["mean_end_err_pct"] > 3.0: fails.append("did not converge")
    if r["wideband_stuck"]["changes_applied"]: fails.append("changed fuel on a stuck sensor")
    if r["ignition"]["violations"]: fails.append("damaging knock or over the limit")
    if not r["boost_failure_flagged"]: fails.append("boost failure not flagged")
    if r["late_uniform_fault"]["changes"]: fails.append("changed the table for a shared fault")
    r["hard_fails"] = fails
    return r

def main():
    ap = argparse.ArgumentParser(); ap.add_argument("--seeds", default="dev", choices=SEEDS); a = ap.parse_args()
    r = evaluate(SEEDS[a.seeds]); print(json.dumps(r, indent=1)); sys.exit(1 if r["hard_fails"] else 0)

if __name__ == "__main__":
    main()
