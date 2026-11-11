#!/usr/bin/env python3
"""Run a workflow's analysis on a log and tune through a platform adapter. Prints JSON; touches nothing else.

  python3 -I tools/analysis/run.py log-health-check --platform <ecu> --log L
  python3 -I tools/analysis/run.py fuel-trim-analysis --platform <ecu> --log L --tune T --profile P.json
"""
import argparse, importlib.util, json, os, sys
from dataclasses import asdict
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
sys.path[:0] = [str(HERE), str(ROOT / "tools" / "log-schema")]
import analyses                                # noqa: E402
from limits import Limits                      # noqa: E402
from profile import Profile, infer_from_log, infer_from_tune    # noqa: E402

REQUIRED = {"log-health-check": [], "log-capture-review": [], "fuel-trim-analysis": ["fuel", "wideband_valid", "tune_matches_log", "live_edits_during_log"], "ignition-knock-review": ["knock_detection", "tune_matches_log", "live_edits_during_log"],
            "boost-control-review": ["aspiration", "max_boost_kpa"], "injector-duty-review": [], "protection-review": ["max_rpm", "max_boost_kpa"]}

def load_adapter(platform):
    path = ROOT / "platforms" / platform / "parser" / "adapter.py"
    if not path.exists(): raise SystemExit(f"no adapter for platform '{platform}'")
    spec = importlib.util.spec_from_file_location(f"adapter_{platform.replace('-', '_')}", path)
    mod = importlib.util.module_from_spec(spec); spec.loader.exec_module(mod)
    return mod

def execute(workflow, log, tune, profile):
    tabs = (tune or {}).get("tables", {})
    infer_from_log(profile, log)
    if tune: infer_from_tune(profile, tune)
    limits = Limits(profile.limits)
    if workflow == "log-health-check": res = analyses.log_health(log, profile)
    elif workflow == "log-capture-review": res = analyses.capture_review(log, profile)
    elif workflow == "fuel-trim-analysis":
        if "ve" not in tabs:
            res = analyses.Result(workflow); res.refusals.append(dict(what="fuel table changes", why="No fuel table was supplied."))
        else: res = analyses.fuel_analysis(log, tabs["ve"], tabs.get("lambda_target"), profile, limits)
    elif workflow == "ignition-knock-review": res = analyses.ignition_review(log, tabs.get("ign_base"), profile, limits)
    elif workflow == "boost-control-review": res = analyses.boost_review(log, profile, limits)
    elif workflow == "injector-duty-review": res = analyses.injector_review(log, profile, limits)
    elif workflow == "protection-review": res = analyses.protection_review(tune, profile, limits)
    else: raise SystemExit(f"unknown workflow {workflow}")
    if tune:
        found, verdict = analyses.tune_log_match(log, tabs)
        res.findings[:0] = found
        if verdict != "not_checkable":
            profile.set("tune_matches_log", verdict == "match", "measured", "high", "logged table outputs compared with the tune file")
        multi = any(f["id"].startswith("multi_table") for f in found)
        uses_tables = workflow in ("fuel-trim-analysis", "ignition-knock-review")
        if uses_tables and res.proposals:
            why = None
            if verdict == "mismatch": why = "The tune file does not match what the ECU ran during this log, so changes worked out from it would be wrong."
            elif profile.value("live_edits_during_log") not in (False, "no", "No"):
                if not profile.known("live_edits_during_log"): why = "A log does not record live edits. Confirm nothing was changed in the ECU while it recorded."
                elif profile.value("live_edits_during_log"): why = "The ECU was changed while the log recorded, so samples before and after the edit describe different calibrations."
            if why is None and verdict == "not_checkable" and profile.value("tune_matches_log") is not True:
                why = "This log has no table-output channels to prove the tune file is what ran. Confirm it, or log the table outputs."
            if why is None and multi:
                why = "Two blended tables are active; a change to one table alone would not land where the error was measured."
            if why:
                res.refusals.append(dict(what=f"{len(res.proposals)} proposed table changes", why=why)); res.proposals = []
    out = asdict(res)
    out["questions"] = profile.question_block(REQUIRED[workflow])
    out["contradictions"] = profile.contradictions
    out["ledger"] = profile.ledger()
    out["unknown_limits"] = limits.unknown()
    return out

def analyses_only_tune(workflow, tune, profile):
    from profile import infer_from_tune
    infer_from_tune(profile, tune)
    limits = Limits(profile.limits)
    out = asdict(analyses.protection_review(tune, profile, limits))
    out.update(questions=profile.question_block(REQUIRED[workflow]), contradictions=profile.contradictions, ledger=profile.ledger(), unknown_limits=limits.unknown())
    return out

def main():
    ap = argparse.ArgumentParser(); ap.add_argument("workflow"); ap.add_argument("--platform", required=True)
    ap.add_argument("--log", default=""); ap.add_argument("--tune", default=""); ap.add_argument("--profile", default=""); ap.add_argument("--exe", default=os.environ.get("PCLINK_EXE", ""), help="local PCLink.exe for .pclr files (or set PCLINK_EXE)")
    a = ap.parse_args()
    ad = load_adapter(a.platform)
    if not a.log and a.workflow != "protection-review": ap.error("--log is required for this workflow")
    tune = ad.load_tune(a.tune, exe=a.exe or None) if a.tune else None
    if not a.log:
        if tune is None: ap.error("protection-review needs --tune")
        print(json.dumps(analyses_only_tune(a.workflow, tune, prof := Profile(json.loads(Path(a.profile).read_text()) if a.profile else None)), indent=1, default=str)); return
    log = ad.load_log(a.log)
    prof = Profile(json.loads(Path(a.profile).read_text()) if a.profile else None)
    print(json.dumps(execute(a.workflow, log, tune, prof), indent=1, default=str))

if __name__ == "__main__":
    main()
