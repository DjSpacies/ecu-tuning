"""Brand-neutral analyses over the normalised models. Each returns a Result: findings, proposals, refusals, evidence.

Proposals are advice for a person to enter. Nothing here touches a file or an ECU.
"""
import statistics
from dataclasses import dataclass, field

import gates
from limits import Limits

@dataclass
class Result:
    workflow: str
    findings: list = field(default_factory=list)
    proposals: list = field(default_factory=list)
    refusals: list = field(default_factory=list)
    gate_summary: dict = field(default_factory=dict)
    notes: list = field(default_factory=list)

def _find(r, id_, severity, text, **kw): r.findings.append(dict(id=id_, severity=severity, text=text, **kw))
def _refuse(r, what, why): r.refusals.append(dict(what=what, why=why))

def log_health(log, profile=None):
    r = Result("log-health-check"); ch = log.channels
    for need in ("rpm", "lambda", "map_kpa", "ect", "iat", "tps", "ign_adv"):
        if need not in ch: _find(r, f"missing_{need}", "warning", f"The log has no {need} channel.")
    rate = log.sample_rate_hz()
    _find(r, "sample_rate", "info", f"Sample rate is {rate:.1f} Hz over {log.time_s[-1] - log.time_s[0]:.0f} s.", value=rate)
    if rate < 5: _find(r, "low_sample_rate", "warning", "Under 5 Hz is too slow to judge transient behaviour.")
    gaps = sum(1 for a, b in zip(log.time_s, log.time_s[1:]) if b - a > 3.0 / max(rate, 1e-6))
    if gaps: _find(r, "gaps", "warning", f"{gaps} gaps in the time record.", value=gaps)
    for name, lo, hi in (("rpm", 0, 20000), ("map_kpa", 0, 500), ("ect", -40, 150), ("iat", -40, 150), ("battery_v", 0, 20)):
        if name in ch:
            v = ch[name]
            if min(v) < lo or max(v) > hi: _find(r, f"range_{name}", "fault", f"{name} is outside its plausible range ({min(v):.1f} to {max(v):.1f}).")
    if "egt" in ch:
        run = [x for x, rp in zip(ch["egt"], ch["rpm"]) if rp > 500]
        # Plausibility only, not a limit: an exhaust gas reading above this is a sensor fault, not a temperature.
        if run and (min(run) > 1300 or max(run) - min(run) < 2):
            _find(r, "egt_implausible", "fault", f"EGT reads {min(run):.0f} to {max(run):.0f} C and barely moves while the engine runs; this looks like an open or unconnected thermocouple, so EGT cannot be used.")
    for name in ("lambda", "map_kpa", "tps", "ect", "iat"):
        if name in ch:
            run = [x for x, rp in zip(ch[name], ch["rpm"]) if rp > 500]
            if len(run) > 20 and max(run) - min(run) < 0.002 * max(abs(max(run)), 1.0): _find(r, f"flat_{name}", "fault", f"{name} never changes while the engine runs, so the sensor or mapping is suspect.")
    if "battery_v" in ch:
        run = [x for x, rp in zip(ch["battery_v"], ch["rpm"]) if rp > 500]
        if run and statistics.median(run) < Limits().get("battery_running_min_v"):
            _find(r, "low_voltage", "warning", f"Median running battery voltage is {statistics.median(run):.1f} V, below the charging check level.")
    reasons = gates.classify(log) if "rpm" in ch else []
    r.gate_summary = gates.summary(reasons)
    _find(r, "usable", "info", f"{r.gate_summary.get('kept', 0)} of {len(log)} samples pass the data-quality gates.", value=r.gate_summary.get("kept", 0))
    return r

def _align(values, times, rpm, h):
    """Value measured `delay` after each sample: what that sample's fuelling produced."""
    out, j, n = [], 0, len(times)
    for i in range(n):
        target = times[i] + gates.lambda_delay_s(rpm[i], h)
        while j < n - 1 and times[j] < target: j += 1
        out.append(values[j] if times[j] >= target else None)
    return out

def fuel_analysis(log, ve, target_table, profile, limits=None, h=gates.HEURISTIC):
    """Per-cell lambda error against target. A change is proposed only with the fuel known, a valid target and a declared step cap."""
    r = Result("fuel-trim-analysis"); limits = limits or Limits(profile.limits if profile else None)
    ch = log.channels
    if not profile or not profile.known("fuel"):
        _refuse(r, "fuel table changes", "Fuel type is unknown. It governs stoichiometry and every mixture judgement."); return r
    if "lambda" not in ch: _refuse(r, "fuel table changes", "The log has no lambda channel."); return r
    if profile.value("wideband_valid") is False: _refuse(r, "fuel table changes", "The wideband is reported as not valid."); return r
    if not profile.known("wideband_valid"): r.notes.append("Wideband validity is not confirmed; treat these results as a screening only.")
    if target_table is None and "lambda_target" not in ch: _refuse(r, "fuel table changes", "No lambda target is available from the tune or log."); return r
    running = [x for x, rp in zip(ch["lambda"], ch["rpm"]) if rp > h["rpm_min"]]
    if len(running) > 20 and max(running) - min(running) < 0.002:
        _refuse(r, "fuel table changes", "Lambda never changes while the engine runs, so the sensor or its mapping is suspect."); return r
    reasons = gates.classify(log, h, fuel=True); r.gate_summary = gates.summary(reasons)
    if r.gate_summary.get("closed_loop_trimming"):
        r.notes.append(f"{r.gate_summary['closed_loop_trimming']} samples left out because closed-loop lambda was trimming; for a base-table check, log with closed loop off or read the trims separately.")
    aligned = _align(ch["lambda"], log.time_s, ch["rpm"], h)
    y_name = ve.y_channel
    if y_name not in ch: _refuse(r, "fuel table changes", f"The log lacks the table's load channel {y_name}."); return r
    cells = {}
    for i, why in enumerate(reasons):
        if why is not None or aligned[i] is None: continue
        if not h["lambda_min"] <= aligned[i] <= h["lambda_max"]: continue    # the delayed reading must itself be valid
        x, y = ch[ve.x_channel][i], ch[y_name][i]
        cell = ve.cell(x, y)
        if max(w for rr, cc, w in ve.weights(x, y) if (rr, cc) == cell) < 0.5: continue
        tgt = ch["lambda_target"][i] if "lambda_target" in ch else target_table.lookup(x, y)
        cells.setdefault(cell, []).append(aligned[i] / tgt)
    rich_cap, lean_cap = limits.get("fuel_change_rich_max_pct"), limits.get("fuel_change_lean_max_pct")
    thin = 0
    judged = [(statistics.median(e) - 1) * 100 for e in cells.values() if len(e) >= h["min_samples_per_cell"]]
    if len(judged) >= 6 and not (profile and profile.value("global_bias_checked")):
        mean_err = statistics.fmean(judged); bias_sd = statistics.pstdev(judged)
        if abs(mean_err) >= h["bias_min_pct"] and bias_sd < h["bias_uniform_ratio"] * abs(mean_err):
            _find(r, "global_bias", "fault", f"All {len(judged)} measured cells are off in the same direction by about {mean_err:+.1f} %. This points to one shared cause.", mean_error_pct=round(mean_err, 2))
            _refuse(r, "fuel table changes", "A uniform error across the map suggests wideband calibration, fuel pressure, injector data or a global scaling. Check those first, then set global_bias_checked.")
            return r
    for (row, col), errs in sorted(cells.items()):
        if len(errs) < h["min_samples_per_cell"]: thin += 1; continue
        med = statistics.median(errs); sd = statistics.pstdev(errs); pct = (med - 1) * 100
        info = dict(cell=[row, col], rpm=ve.x_axis[col], load=ve.y_axis[row], samples=len(errs), median_error_pct=round(pct, 2), spread_pct=round(sd * 100, 2))
        if abs(pct) < h["deadband_pct"]: continue
        same_side = sum(1 for x in errs if (x - 1) * pct > 0) / len(errs)    # a median can sit on one side of split data
        if same_side < h["direction_consistency"] or sd * 100 > h["noise_ratio"] * abs(pct):
            _find(r, "noisy_cell", "info", f"Cell at {ve.x_axis[col]} rpm, {ve.y_axis[row]} load: error {pct:+.1f} % is within the spread ({sd * 100:.1f} %). More steady data needed.", **info); continue
        adding = pct > 0                      # measured leaner than target: fuel must rise
        cap = rich_cap if adding else lean_cap
        word = "adding" if adding else "removing"
        _find(r, "lambda_error", "warning", f"Cell at {ve.x_axis[col]} rpm, {ve.y_axis[row]} load is {pct:+.1f} % from target over {len(errs)} samples.", **info)
        if cap is None:
            _refuse(r, f"{word} fuel at cell {row},{col}", "No step cap is set for this direction. Sources give no general figure; declare one in the setup profile."); continue
        change = max(-cap, min(cap, pct))
        conf = "low" if profile.fields.get("wideband_valid") is None else "medium"
        if conf == "low" and not adding: change /= 2.0     # risk-adding direction, unconfirmed sensor: smaller step (docs/SAFETY.md rules 3-4)
        r.proposals.append(dict(table=ve.role, native=ve.native_name, cell=[row, col], rpm=ve.x_axis[col], load=ve.y_axis[row], change_pct=round(change, 2), full_error_pct=round(pct, 2), clamped=abs(change) < abs(pct), confidence=conf,
                                current=ve.values[row][col], proposed=round(ve.values[row][col] * (1 + change / 100.0), 2)))
    if thin: r.notes.append(f"{thin} cells have too few samples to judge.")
    if not cells: _find(r, "no_usable_data", "warning", "No samples passed the gates in any cell. Not enough data to change this safely.")
    return r

def ignition_review(log, ign, profile, limits=None):
    """Find knock and map roughness. Only risk-reducing changes are proposed; a log alone cannot justify more advance."""
    r = Result("ignition-knock-review"); limits = limits or Limits(profile.limits if profile else None); ch = log.channels
    if ign is not None:
        limit = limits.get("timing_adjacent_cell_review_deg")
        steps = 0
        for row in ign.values:
            steps += sum(1 for a, b in zip(row, row[1:]) if abs(b - a) > limit)
        for a, b in zip(ign.values, ign.values[1:]):
            steps += sum(1 for x, y in zip(a, b) if abs(x - y) > limit)
        if steps: _find(r, "map_roughness", "warning", f"{steps} neighbouring cell pairs differ by more than {limit:g} degrees.", value=steps)
    has_knock = "knock_count" in ch or "knock_level" in ch
    r.notes.append("A log cannot show that more ignition advance is safe, so this review never proposes an increase.")
    if not has_knock or not (any(ch.get("knock_count", [])) or any(ch.get("knock_level", []))):
        msg = "The log has no knock channel." if not has_knock else "The knock channels stay at zero, which may mean no knock or an inactive system."
        _find(r, "knock_unverified", "warning", msg + " Absence of evidence is not evidence of safety.")
        if not profile or not profile.known("knock_detection"): _refuse(r, "ignition changes", "Knock detection method is unknown.")
        return r
    series = ch.get("knock_count") or ch["knock_level"]
    events = [i for i, (a, b) in enumerate(zip(series, series[1:]), 1) if b > a]
    _find(r, "knock_events", "fault" if events else "info", f"{len(events)} knock events in the log.", value=len(events))
    if not events: return r
    if ign is None: _refuse(r, "ignition changes", "No ignition table was supplied."); return r
    y_name = ign.y_channel
    if y_name not in ch: _refuse(r, "ignition changes", f"The log lacks the table's load channel {y_name}."); return r
    step = limits.get("timing_retard_on_knock_deg")
    cells = {}
    for i in events:
        c = ign.cell(ch[ign.x_channel][i], ch[y_name][i]); cells[c] = cells.get(c, 0) + 1
    for (row, col), n in sorted(cells.items()):
        r.proposals.append(dict(table=ign.role, native=ign.native_name, cell=[row, col], rpm=ign.x_axis[col], load=ign.y_axis[row], change_deg=-step, current=ign.values[row][col], proposed=round(ign.values[row][col] - step, 2), events=n, confidence="medium"))
    return r

def boost_review(log, profile, limits=None, h=gates.HEURISTIC):
    r = Result("boost-control-review"); limits = limits or Limits(profile.limits if profile else None); ch = log.channels
    if not profile or not profile.known("aspiration") or profile.value("aspiration") == "na_or_unboosted":
        _refuse(r, "boost review", "This log does not show a boosted engine, or aspiration is unknown."); return r
    if "map_kpa" not in ch: _refuse(r, "boost review", "No manifold pressure channel."); return r
    peak = max(ch["map_kpa"]); _find(r, "peak_boost", "info", f"Peak manifold pressure is {peak:.0f} kPa absolute.", value=peak)
    ceiling = limits.get("max_boost_kpa")
    if ceiling is None: _refuse(r, "raising boost", "No boost ceiling is declared. It is safety-critical and engine-specific.")
    elif peak > ceiling: _find(r, "over_ceiling", "fault", f"Peak manifold pressure {peak:.0f} kPa is above the declared ceiling of {ceiling:.0f} kPa.")
    if "boost_target_kpa" not in ch: _find(r, "no_target", "warning", "The log has no boost target, so overshoot cannot be measured."); return r
    errs = [(m - t) for m, t, rp in zip(ch["map_kpa"], ch["boost_target_kpa"], ch["rpm"]) if t > 0 and rp > 1500]
    if not errs: return r
    over = max(errs); _find(r, "overshoot", "warning" if over > 0 else "info", f"Largest overshoot above target is {over:.0f} kPa.", value=over)
    margin = limits.get("boost_overshoot_abort_kpa")
    if margin is not None and over > margin: _find(r, "overshoot_abort", "fault", f"Overshoot exceeds the abort margin of {margin:g} kPa.")
    if "wastegate_duty" in ch and max(ch["wastegate_duty"]) >= 100: _find(r, "duty_saturated", "warning", "Wastegate duty reached its maximum, so feedback had no authority left.")
    sign = sum(1 for a, b in zip(errs, errs[1:]) if a * b < 0 and abs(a) > 3 and abs(b) > 3)
    if sign > 8: _find(r, "oscillation", "warning", f"Boost error changes sign {sign} times, which suggests oscillation.", value=sign)
    return r

def injector_review(log, profile, limits=None):
    r = Result("injector-duty-review"); limits = limits or Limits(profile.limits if profile else None); ch = log.channels
    if "inj_duty" not in ch: _refuse(r, "injector duty judgement", "No injector duty channel."); return r
    peak = max(ch["inj_duty"]); cap = limits.get("injector_duty_max_pct")
    _find(r, "peak_duty", "fault" if peak > cap else "info", f"Peak injector duty is {peak:.1f} %, against a ceiling of {cap:g} %.", value=peak)
    return r

def ignition_next_step(history, knock_now, limits, near_optimum_gain_pct=0.5):
    """Decide the next advance change during measured-torque tuning (methodology/steady-state-ignition).

    history is [(advance, torque)] with the latest last. Returns (change_deg, reason). Requires torque: without it the
    procedure must not run at all.
    """
    if knock_now: return -limits.get("timing_retard_on_knock_deg"), "knock"
    if len(history) < 2: return limits.get("timing_step_advance_deg"), "explore"
    (_, t0), (_, t1) = history[-2], history[-1]
    gain = (t1 - t0) / t0 * 100.0
    if gain <= 0.0: return 0.0, "torque_flat_or_falling"
    if gain < near_optimum_gain_pct:
        return 0.0, "near_optimum"
    return (limits.get("timing_step_advance_fine_deg") if gain < 2 * near_optimum_gain_pct else limits.get("timing_step_advance_deg")), "torque_rising"

def protection_review(tune, profile, limits=None):
    """Are the configured limits there, and consistent with what the user says the engine can take?"""
    r = Result("protection-review"); limits = limits or Limits(profile.limits if profile else None)
    prot = (tune or {}).get("protections")
    if prot is None: _refuse(r, "protection review", "This platform's tune data does not expose protection settings."); return r
    for key, ceiling_key, unit in (("rpm_limit", "max_rpm", "rpm"), ("map_limit_kpa", "max_boost_kpa", "kPa")):
        v = prot.get(key); ceiling = limits.get(ceiling_key)
        if v is None: _find(r, f"no_{key}", "fault", f"No {key} is configured."); continue
        _find(r, key, "info", f"Highest configured {key} is {v:g} {unit}.", value=v)
        if ceiling is None: r.notes.append(f"{ceiling_key} is not declared, so {key} cannot be judged.")
        elif v > ceiling: _find(r, f"{key}_above_ceiling", "fault", f"Configured {key} of {v:g} {unit} is above the declared ceiling of {ceiling:g} {unit}.")
    return r


OUT_FOR = {"ve": "ve_out", "ve_2": "ve_2_out", "ign_base": "ign_out", "ign_base_2": "ign_2_out"}

def tune_log_match(log, tables, h=gates.HEURISTIC):
    """Compare the table value the ECU logged with the same table in the supplied tune, at steady samples.

    A log holds no record of live edits, so this is the only evidence that the tune file is the calibration that ran.
    Returns (findings, verdict): verdict is 'match', 'mismatch' or 'not_checkable'. The tolerance covers display
    rounding and interpolation only; it is a project default, not a sourced figure.
    """
    ch, out, checked = log.channels, [], 0
    reasons = gates.classify(log, h)
    worst = None
    for role, name in OUT_FOR.items():
        tb = tables.get(role)
        if tb is None or name not in ch or tb.x_channel not in ch or tb.y_channel not in ch: continue
        tol = 0.6 if role.startswith("ign") else 0.6 * max(abs(v) for row in tb.values for v in row) / 100
        diffs = [abs(ch[name][i] - tb.lookup(ch[tb.x_channel][i], ch[tb.y_channel][i])) for i, why in enumerate(reasons) if why is None]
        if len(diffs) < 50: continue
        checked += 1
        bad = sum(d > tol for d in diffs) / len(diffs)
        med = sorted(diffs)[len(diffs) // 2]
        if bad > 0.2:
            out.append(dict(id=f"tune_mismatch_{role}", severity="fault", text=f"{tb.native_name or role}: the ECU's logged value differs from the supplied tune in {bad:.0%} of steady samples (median difference {med:.2f}). The tune file is probably not what ran during this log, for example edited live or saved later.", value=bad))
            worst = "mismatch"
        else:
            out.append(dict(id=f"tune_match_{role}", severity="info", text=f"{tb.native_name or role}: logged values agree with the supplied tune in {1 - bad:.0%} of steady samples.", value=1 - bad))
    for a_, b_ in (("ve_out", "ve_2_out"), ("ign_out", "ign_2_out")):
        if a_ in ch and b_ in ch:
            sep = [abs(x - y) for x, y, why in zip(ch[a_], ch[b_], reasons) if why is None]
            if sep and sorted(sep)[len(sep) // 2] > 0.5:
                out.append(dict(id=f"multi_table_{a_[:-4]}", severity="warning", text=f"Two {'fuel' if a_.startswith('ve') else 'ignition'} tables are active and differ; the ECU blends or switches between them, so an analysis against one table alone is incomplete.", value=None))
    verdict = worst or ("match" if checked else "not_checkable")
    return out, verdict

# Thresholds for recognising capture phases. Project defaults with no published source; they only classify a log's
# contents and never set how far a tune may change.
CAPTURE = dict(warm_c=70.0, cold_start_margin_c=20.0, warm_idle_s=60.0, idle_rpm_max=1300.0, steady_min_s=60.0,
               pull_tps=90.0, pull_span_rpm=2000.0, cl_active_frac=0.2)

def capture_review(log, profile=None, c=CAPTURE, h=gates.HEURISTIC):
    """Check a log against methodology/log-capture-protocol: which phases it holds, and what to record next time."""
    r = Result("log-capture-review"); ch, t = log.channels, log.time_s
    rpm = ch["rpm"]; ect = ch.get("ect"); tps = ch.get("tps")
    dt = 1.0 / max(log.sample_rate_hz(), 1e-6)
    have, missing = [], []
    def phase(ok, name, text_ok, text_missing):
        (have if ok else missing).append(name)
        _find(r, f"phase_{name}", "info" if ok else "warning", text_ok if ok else text_missing)
    start = next((i for i, x in enumerate(rpm) if x > h["rpm_min"]), None)
    phase(start is not None and start > 0 and t[start] - t[0] > 0.5, "before_crank",
          "Logging started before the engine ran.", "Logging started with the engine already running; start logging with the key on before cranking.")
    if ect is not None and start is not None:
        e0 = ect[start]
        phase(e0 < c["warm_c"] - c["cold_start_margin_c"], "cold_start", f"Engine started cold ({e0:.0f} C).",
              f"Engine was already at {e0:.0f} C when it started, so there is no cold start or warm-up data.")
        warm_at = next((i for i in range(start, len(ect)) if ect[i] >= c["warm_c"]), None)
        phase(warm_at is not None, "reached_temperature", "Coolant reached operating temperature.", "Coolant never reached operating temperature.")
        idle = sum(dt for i in range(len(rpm)) if ect[i] >= c["warm_c"] and h["rpm_min"] < rpm[i] < c["idle_rpm_max"] and (tps is None or tps[i] < 2))
        phase(idle >= c["warm_idle_s"], "warm_idle", f"{idle:.0f} s of warm idle.", f"Only {idle:.0f} s of warm idle; idle warm for a few minutes.")
    else:
        missing.append("temperatures"); _find(r, "phase_temperatures", "warning", "No coolant temperature, so warm-up phases cannot be judged.")
    reasons = gates.classify(log, h)
    steady = [i for i, why in enumerate(reasons) if why is None and rpm[i] >= c["idle_rpm_max"] and (tps is None or tps[i] < c["pull_tps"])]
    phase(len(steady) * dt >= c["steady_min_s"], "steady_driving", f"{len(steady) * dt:.0f} s of usable steady driving.",
          f"Only {len(steady) * dt:.0f} s of usable steady driving; hold steady rpm and load points with smooth throttle.")
    pulls, i = [], 0
    if tps is not None:
        while i < len(rpm):
            if tps[i] >= c["pull_tps"]:
                j = i
                while j + 1 < len(rpm) and tps[j + 1] >= c["pull_tps"]: j += 1
                if rpm[j] - rpm[i] >= c["pull_span_rpm"]: pulls.append((rpm[i], max(rpm[i:j + 1])))
                i = j + 1
            else: i += 1
    phase(bool(pulls), "full_load_pull", f"{len(pulls)} full-throttle pull(s): " + ", ".join(f"{a:.0f} to {b:.0f} rpm" for a, b in pulls[:6]) + ".",
          "No full-throttle pull spanning a useful rpm range.")
    if "fuel_trim" in ch:
        trimming = sum(1 for i, why in enumerate(reasons) if why is None and abs(ch["fuel_trim"][i]) > h["cl_trim_active_pct"])
        kept = max(1, sum(1 for why in reasons if why is None))
        frac = trimming / kept
        sev = "warning" if frac > c["cl_active_frac"] else "info"
        if sev == "warning": missing.append("closed_loop_off_for_base_fuel")
        _find(r, "closed_loop", sev, f"Closed-loop lambda was trimming in {frac:.0%} of usable samples." + (" Base fuel tables cannot be judged from this; log with closed loop off." if sev == "warning" else ""), value=frac)
    else:
        _find(r, "closed_loop", "warning", "No closed-loop trim channel; whether closed loop was active is unknown.")
    outs = [n for n in ("ve_out", "ign_out") if n in ch]
    _find(r, "table_outputs", "info" if outs else "warning", "Table output channels are logged, so the tune file can be checked against what ran." if outs else
          "No table output channels; the tune file cannot be checked against the log. Log them if the ECU allows, and confirm nothing changed during the log.")
    for n in ("lambda", "map_kpa", "tps", "ign_adv", "ect", "iat", "knock_level"):
        if n not in ch: _find(r, f"channel_{n}", "warning", f"Channel {n} is not logged.")
    r.notes.append("Next log: " + ("all phases present." if not missing else "record " + ", ".join(missing).replace("_", " ") + "."))
    r.notes.append("Phase recognition thresholds are project defaults, not sourced figures; they only describe the log.")
    return r
