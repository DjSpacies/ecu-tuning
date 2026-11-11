"""Data-quality gates (methodology/data-quality). A sample is usable only if it describes a valid, steady state.

The rules come from the methodology. The numeric thresholds below are project defaults with no published source, so
they are marked here and reported as such. They do not set how far a tune may be changed; safety/limits.yaml does.
"""
HEURISTIC = dict(
    ect_min_c=70.0, rpm_min=500.0, rpm_rate_max=300.0, map_rate_max=20.0, tps_rate_max=15.0, lambda_min=0.55, lambda_max=1.6,
    min_samples_per_cell=20, deadband_pct=1.5, noise_ratio=2.0, delay_cycles=4.0, delay_const_s=0.05, delay_max_s=1.0, bias_min_pct=3.0, bias_uniform_ratio=0.3, direction_consistency=0.75,
    cl_trim_active_pct=0.5,
)

def lambda_delay_s(rpm, h=HEURISTIC):
    """Estimated delay from fuelling to wideband reading: a few engine cycles plus a fixed sensor term."""
    if rpm <= 0: return h["delay_max_s"]
    return min(h["delay_const_s"] + h["delay_cycles"] * 120.0 / rpm, h["delay_max_s"])

def _rate(values, times, i):
    a, b = max(i - 1, 0), min(i + 1, len(values) - 1)
    dt = times[b] - times[a]
    return abs(values[b] - values[a]) / dt if dt > 0 else 0.0

def classify(log, h=HEURISTIC, fuel=False):
    """List the reason each sample is rejected, or None if it passes. With fuel=True, samples where closed-loop lambda
    is trimming are also rejected: the measured lambda then reflects the trim, not the base table, and the sign
    convention of the trim channel is not documented, so it is excluded rather than corrected."""
    ch, t = log.channels, log.time_s
    out = [None] * len(t)
    for i in range(len(t)):
        r = None
        if ch["rpm"][i] < h["rpm_min"]: r = "engine_not_running"
        elif "ect" in ch and ch["ect"][i] < h["ect_min_c"]: r = "engine_cold"
        elif "wideband_ok" in ch and not ch["wideband_ok"][i]: r = "wideband_invalid"
        elif "lambda" in ch and not h["lambda_min"] <= ch["lambda"][i] <= h["lambda_max"]: r = "lambda_out_of_range"
        elif ch.get("fuel_cut") and ch["fuel_cut"][i]: r = "fuel_cut"
        elif ch.get("limiter_active") and ch["limiter_active"][i]: r = "limiter_active"
        elif ch.get("accel_enrich") and ch["accel_enrich"][i]: r = "accel_enrich"
        elif fuel and "fuel_trim" in ch and abs(ch["fuel_trim"][i]) > h["cl_trim_active_pct"]: r = "closed_loop_trimming"
        elif _rate(ch["rpm"], t, i) > h["rpm_rate_max"]: r = "rpm_transient"
        elif "map_kpa" in ch and _rate(ch["map_kpa"], t, i) > h["map_rate_max"]: r = "load_transient"
        elif "tps" in ch and _rate(ch["tps"], t, i) > h["tps_rate_max"]: r = "throttle_transient"
        out[i] = r
    return out

def summary(reasons):
    counts = {}
    for r in reasons: counts[r or "kept"] = counts.get(r or "kept", 0) + 1
    return counts
