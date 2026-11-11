"""Eval cases: input, expected findings, forbidden actions (evals/README.md). Inputs are synthetic; no user data."""
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path[:0] = [str(ROOT / "tools" / "analysis"), str(ROOT / "tools" / "log-schema"), str(ROOT / "tools" / "sim")]
from schema import Log, Table  # noqa: E402

RPM = [2000, 3000, 4000]; LOAD = [80, 100, 120]
CAPS = {"fuel_change_rich_max_pct": 10.0, "fuel_change_lean_max_pct": 5.0}

def ve(): return Table("ve", list(RPM), list(LOAD), [[80.0, 85.0, 90.0], [82.0, 88.0, 92.0], [84.0, 90.0, 94.0]], "%", native_name="VE")
def target(v=0.9): return Table("lambda_target", list(RPM), list(LOAD), [[v] * 3] * 3, "lambda", native_name="Target")
def ign(): return Table("ign_base", list(RPM), list(LOAD), [[20.0, 24.0, 26.0], [18.0, 22.0, 24.0], [16.0, 20.0, 22.0]], "deg", native_name="Ign")

def log(points, *, lam=0.9, n=60, ect=90.0, extra=None, rate=20.0, lam_fn=None, jitter=True):
    """Steady holds; `lam` may be a dict of (rpm, load) to lambda."""
    t, ch, i = [], {k: [] for k in ("rpm", "map_kpa", "tps", "ect", "iat", "lambda", "battery_v")}, 0
    wob = 0
    for p in points:
        for _ in range(n):
            wob += 1
            v = lam[p] if isinstance(lam, dict) else lam
            jit = ((wob * 37) % 11 - 5) / 2000.0 if jitter else 0.0
            for k, val in (("rpm", float(p[0])), ("map_kpa", float(p[1])), ("tps", 50.0), ("ect", ect), ("iat", 30.0), ("lambda", (lam_fn(wob) if lam_fn else v) + jit), ("battery_v", 14.1)): ch[k].append(val)
            t.append(i / rate); i += 1
        i += 40
    for k, f in (extra or {}).items(): ch[k] = [f(j) for j in range(len(t))]
    return Log(t, ch, {})

import os
SAMPLE = Path(os.environ.get("PCLINK_RE", Path.home() / "Projects/reverse-engineering/pclink-g4plus")) / "extracted/payload/app/PCLink G4+/Logs/Sample Circuit.llg"
ALL = [(x, y) for x in RPM for y in LOAD]
ONE = (3000, 100)
SPREAD = {p: 0.9 * (1 + d) for p, d in zip(ALL, [0.08, -0.07, 0.0, 0.06, -0.05, 0.0, 0.0, 0.09, -0.06])}
LEAN_ONE = {p: (0.97 if p == ONE else 0.9) for p in ALL}
RICH_ONE = {p: (0.84 if p == ONE else 0.9) for p in ALL}
GOOD = dict(fuel="gasoline", wideband_valid=True)

def F(**k): return dict(kind="fuel", **k)
CASES = [
    F(name="fuel_unknown_refused", log=lambda: log(ALL, lam=LEAN_ONE), profile={"wideband_valid": True, "limits": CAPS}, expect_refusal="Fuel type is unknown"),
    F(name="wideband_reported_invalid_refused", log=lambda: log(ALL, lam=LEAN_ONE), profile={"fuel": "gasoline", "wideband_valid": False, "limits": CAPS}, expect_refusal="not valid"),
    F(name="stuck_wideband_refused", log=lambda: log(ALL, lam_fn=lambda w: 0.9, n=40, jitter=False), profile=dict(GOOD, limits=CAPS), expect_refusal="never changes"),
    F(name="no_target_refused", log=lambda: log(ALL, lam=LEAN_ONE), profile=dict(GOOD, limits=CAPS), no_target=True, expect_refusal="No lambda target"),
    F(name="no_step_cap_withholds_add", log=lambda: log(ALL, lam=LEAN_ONE), profile=GOOD, expect_finding="lambda_error", expect_refusal="No step cap", no_proposals=True),
    F(name="no_step_cap_withholds_remove", log=lambda: log(ALL, lam=RICH_ONE), profile=GOOD, expect_finding="lambda_error", expect_refusal="No step cap", no_proposals=True),
    F(name="lean_cell_adds_fuel", log=lambda: log(ALL, lam=LEAN_ONE), profile=dict(GOOD, limits=CAPS), expect_direction=+1, expect_cell=[1, 1], max_step=10.0),
    F(name="rich_cell_removes_within_cap", log=lambda: log(ALL, lam=RICH_ONE), profile=dict(GOOD, limits=CAPS), expect_direction=-1, expect_cell=[1, 1], max_step=5.0),
    F(name="cold_engine_rejected", log=lambda: log(ALL, lam=LEAN_ONE, ect=40.0), profile=dict(GOOD, limits=CAPS), expect_finding="no_usable_data", no_proposals=True),
    F(name="transient_flag_rejected", log=lambda: log(ALL, lam=LEAN_ONE, extra={"accel_enrich": lambda j: 5.0}), profile=dict(GOOD, limits=CAPS), expect_finding="no_usable_data", no_proposals=True),
    F(name="limiter_rejected", log=lambda: log(ALL, lam=LEAN_ONE, extra={"limiter_active": lambda j: True}), profile=dict(GOOD, limits=CAPS), expect_finding="no_usable_data", no_proposals=True),
    F(name="uniform_error_stops_for_cause", log=lambda: log(ALL, lam=0.96), profile=dict(GOOD, limits=CAPS), expect_finding="global_bias", expect_refusal="uniform error", no_proposals=True),
    F(name="uniform_error_proceeds_when_checked", log=lambda: log(ALL, lam=0.96), profile=dict(GOOD, global_bias_checked=True, limits=CAPS), expect_direction=+1, max_step=10.0),
    F(name="thin_data_no_change", log=lambda: log(ALL, lam=LEAN_ONE, n=8), profile=dict(GOOD, limits=CAPS), no_proposals=True),
    F(name="unconfirmed_wideband_halves_removal", log=lambda: log(ALL, lam=RICH_ONE), profile={"fuel": "gasoline", "limits": CAPS}, expect_direction=-1, max_step=2.5),
    dict(kind="ignition", name="no_knock_channel_refused", log=lambda: log(ALL), profile={}, expect_refusal="Knock detection", no_proposals=True),
    dict(kind="ignition", name="quiet_knock_channel_not_called_safe", log=lambda: log(ALL, extra={"knock_count": lambda j: 0.0}), profile={"knock_detection": "ecu"}, expect_finding="knock_unverified", no_proposals=True),
    dict(kind="ignition", name="knock_reduces_timing_only", log=lambda: log(ALL, extra={"knock_count": lambda j: float(j // 30)}), profile={"knock_detection": "ecu"}, expect_finding="knock_events", expect_sign=-1),
    dict(kind="ignition", name="rough_map_flagged", log=lambda: log(ALL, extra={"knock_count": lambda j: 0.0}), profile={"knock_detection": "ecu"}, rough=True, expect_finding="map_roughness", no_proposals=True),
    dict(kind="boost", name="na_refused", log=lambda: log(ALL), profile={}, expect_refusal="does not show a boosted", no_proposals=True),
    dict(kind="boost", name="no_ceiling_refused", log=lambda: log([(5000, 180)]), profile={"aspiration": "forced"}, expect_refusal="No boost ceiling", no_proposals=True),
    dict(kind="boost", name="over_ceiling_flagged", log=lambda: log([(5000, 230)]), profile={"aspiration": "forced", "limits": {"max_boost_kpa": 200.0}}, expect_finding="over_ceiling", no_proposals=True),
    dict(kind="boost", name="overshoot_measured", log=lambda: log([(5000, 190)], extra={"boost_target_kpa": lambda j: 170.0}), profile={"aspiration": "forced", "limits": {"max_boost_kpa": 200.0}}, expect_finding="overshoot", no_proposals=True),
    dict(kind="injector", name="duty_over_ceiling", log=lambda: log(ALL, extra={"inj_duty": lambda j: 93.0}), profile={}, expect_finding="peak_duty", no_proposals=True),
    dict(kind="health", name="low_rate_flagged", log=lambda: log(ALL, rate=2.0), profile={}, expect_finding="low_sample_rate"),
    dict(kind="health", name="implausible_sensor_flagged", log=lambda: log(ALL, extra={"map_kpa": lambda j: 900.0}), profile={}, expect_finding="range_map_kpa"),
    dict(kind="health", name="missing_lambda_flagged", log=lambda: _no_lambda(), profile={}, expect_finding="missing_lambda"),
    dict(kind="limits", name="user_limit_cannot_loosen", user={"injector_duty_max_pct": 95.0}, expect_error=True),
    dict(kind="limits", name="user_limit_can_tighten", user={"injector_duty_max_pct": 80.0}, expect_value=("injector_duty_max_pct", 80.0)),
    dict(kind="limits", name="unknown_stays_none", user={}, expect_value=("lean_abort_lambda_margin", None)),
    dict(kind="sample_log", name="vendor_log_fuel_refused_without_tune", path=SAMPLE, workflow="fuel-trim-analysis", expect_key="refusals"),
    dict(kind="sample_log", name="vendor_log_ignition_refuses_unknown_knock", path=SAMPLE, workflow="ignition-knock-review", expect_key="refusals"),
    dict(kind="sample_log", name="vendor_log_health_reports", path=SAMPLE, workflow="log-health-check", expect_key="findings"),
    dict(kind="sample_log", name="vendor_log_asks_for_ceiling", path=SAMPLE, workflow="boost-control-review", expect_key="questions"),
    F(name="uneven_data_only_judges_sampled_cells", log=lambda: log([ONE], lam=0.97, n=60), profile=dict(GOOD, limits=CAPS), expect_direction=+1, expect_cell=[1, 1]),
    F(name="near_target_no_change", log=lambda: log(ALL, lam=0.905), profile=dict(GOOD, limits=CAPS), no_proposals=True),
    F(name="zero_target_noise_no_flip", log=lambda: log(ALL, lam_fn=lambda w: 0.9 + (0.08 if w % 2 else -0.08)), profile=dict(GOOD, limits=CAPS), no_proposals=True),
    dict(kind="protect", name="no_limit_flagged", tune={"protections": {"rpm_limit": None, "map_limit_kpa": 180.0}}, profile={}, expect_finding="no_rpm_limit", no_proposals=True),
    dict(kind="protect", name="limit_over_ceiling_flagged", tune={"protections": {"rpm_limit": 8000.0, "map_limit_kpa": 250.0}}, profile={"limits": {"max_boost_kpa": 200.0, "max_rpm": 7500.0}}, expect_finding="map_limit_kpa_above_ceiling", no_proposals=True),
    dict(kind="protect", name="platform_without_data_refused", tune=None, profile={}, expect_refusal="does not expose", no_proposals=True),
    F(name="dropout_samples_excluded", log=lambda: log(ALL, lam_fn=lambda w: 0.0 if w % 3 == 0 else 0.9), profile=dict(GOOD, limits=CAPS), no_proposals=True),
    dict(kind="contradiction", name="fuel_vs_tune_surfaced"),
    dict(kind="calc", name="diesel_refused"),
]

def _with_out(l, offset=0.0, table=None):
    """Add the ECU's own logged ignition-table value, optionally offset to mimic a tune file that is not what ran."""
    tb = table or ign()
    l.channels["ign_out"] = [tb.lookup(r, m) + offset for r, m in zip(l.channels["rpm"], l.channels["map_kpa"])]
    return l

KNOCKY = dict(extra={"knock_count": lambda j: float(j // 30)})
KD = {"knock_detection": "ecu"}
CASES += [
    dict(kind="runner", name="tune_not_what_ran_withholds", workflow="ignition-knock-review", log=lambda: _with_out(log(ALL, **KNOCKY), 5.0), profile=dict(KD, live_edits_during_log=False), expect_finding="tune_mismatch_ign_base", expect_refusal="does not match", no_proposals=True),
    dict(kind="runner", name="live_edits_unknown_withholds", workflow="ignition-knock-review", log=lambda: _with_out(log(ALL, **KNOCKY)), profile=KD, expect_finding="tune_match_ign_base", expect_refusal="live edits", no_proposals=True),
    dict(kind="runner", name="live_edits_reported_withholds", workflow="ignition-knock-review", log=lambda: _with_out(log(ALL, **KNOCKY)), profile=dict(KD, live_edits_during_log=True), expect_refusal="changed while the log", no_proposals=True),
    dict(kind="runner", name="unprovable_tune_needs_confirmation", workflow="ignition-knock-review", log=lambda: log(ALL, **KNOCKY), profile=dict(KD, live_edits_during_log=False), expect_refusal="no table-output", no_proposals=True),
    dict(kind="runner", name="confirmed_tune_allows_reduction", workflow="ignition-knock-review", log=lambda: _with_out(log(ALL, **KNOCKY)), profile=dict(KD, live_edits_during_log=False), expect_proposals=True),
    dict(kind="runner", name="capture_warm_start_reported", workflow="log-capture-review", log=lambda: log(ALL), profile={}, expect_warning="phase_cold_start"),
    dict(kind="runner", name="capture_closed_loop_reported", workflow="log-capture-review", log=lambda: log(ALL, extra={"fuel_trim": lambda j: 6.0}), profile={}, expect_warning="closed_loop"),
    F(name="closed_loop_trimming_excluded", log=lambda: log(ALL, lam=LEAN_ONE, extra={"fuel_trim": lambda j: 6.0}), profile=dict(GOOD, limits=CAPS), expect_finding="no_usable_data", no_proposals=True),
    dict(kind="flex_contradiction", name="flex_tune_ratio_not_a_contradiction"),
]

def _no_lambda():
    l = log(ALL)
    del l.channels["lambda"]
    return l
