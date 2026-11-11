---
id: methodology/data-quality
title: Data quality for tuning logs
layer: L2
status: draft
confidence: high
sources: [practice, reference-data]
verified: 2026-11-11
applies_to: {fuels: [gasoline, ethanol, methanol], engines: [all]}
depends_on: [principles/data/statistics-for-tuning, principles/data/sensor-lag-and-delay]
supersedes: []
---

# Data quality for tuning logs

## Claim
Only samples from a valid, steady state support a change. Decide which samples qualify before computing anything, and report what was rejected. Most large errors in an unfiltered log are not fuelling errors at all: they are overrun, shift cuts, limiters, transients, lag, heat soak, closed-loop trim, mismatched axes or mismatched graph scales.

## Why (derivation)
Warm-up, transient enrichment, limiters and lag all produce plausible numbers that describe the wrong condition. The sources repeat one phrase in many forms: bad data in gives bad corrections out. A correction tool, whether manual or automatic, applies whatever the data says, so a polluted cell goes straight into the table.

The common contaminants and what they look like:
- **Overrun fuel cut.** With injectors shut the sensor sees fresh air and pegs lean. In histograms this shows as huge lean errors (tens of percent, up to about 90 % in the sources) in light-load and high-rpm, very-low-MAP cells.
- **Ignition-cut shifts and limiters.** Unburnt mixture and air pass the sensor, so each cut reads as a lean spike. The sources show these at every upshift on a sequential gearbox and near the rev limit.
- **Transients.** Tip-in triggers acceleration enrichment and leaves small rich or lean excursions even with a good transient model; lift-off leans out. Large rich spikes at closed throttle during a gearshift are not a table error.
- **Target steps.** Where the ECU switches from closed loop to a rich power-enrichment target, measured lambda lags and logs a false lean error (principles/data/sensor-lag-and-delay).
- **Heat soak.** After the engine has sat (bonnet down at the roadside, idling on the dyno, or shut down for a reflash) intake and fuel temperatures are abnormal and trims read unrealistically for the first few minutes of driving. The ECU cannot model soak because it does not know how long the engine sat. One factory-ECU demonstration showed short-term trim at about -6 to -8 % straight after a hot restart against near zero after settling.
- **Closed-loop correction.** If closed loop is active, measured lambda looks right while the trim hides the table error. Either turn it off, or log the trim and remove it (corrected-error methods below).
- **Slow drift.** Lambda drifting over a stint (in one source, on target for two laps and 6 to 8 % richer by lap ten) means something is changing: intake temperature and its compensation, coolant temperature, fuel pressure, heat soak on out-laps, or barometric pressure at altitude.

## Assumptions
Log channels exist for the conditions being tested, or the missing ones are reported. In particular, throttle position must be logged: without it the closed-throttle and transient filters cannot run.

## Breaks when
- A low log rate cannot resolve transient events.
- The analysis load axis is not the fuel table's load axis, or the logged load is not where the ECU really was (see the altitude case in Decision rules).
- The wideband is a factory sensor trusted beyond its accurate range; several factory sensors are accurate near stoichiometric but lose accuracy at rich mixtures.

## Practical use
Apply the gate checks in order and show the rejection counts. Then look at what is left before computing anything: check the graph scales, check the cells the ECU actually used, and check that the vitals were normal.

### Diagnostic tests
- **Overrun versus real lean.** Lean error in cells at very low MAP or high rpm with throttle closed is overrun. Filter closed throttle and see if the error disappears. In one course example the 20 kPa row read -16 to -19 % and the error vanished once closed-throttle samples were removed.
- **Shift or limiter cut versus real lean.** Line the spike up with the gear-change cut, the limiter status, or a fast rpm change. If they coincide, it is a cut.
- **Limiter cut versus hardware misfire.** When an engine breaks up on a pull, check the limiter status channels at that moment. Active limiter: the ECU is cutting on purpose. No limiter active: look for a coil, injector, lead or plug gap fault.
- **Lag versus error at a target step:** see principles/data/sensor-lag-and-delay.
- **Real offset versus graph scaling.** Two traces auto-scaled to their own ranges can look offset when they agree, or overlap when they differ (one source showed 0.93 target and 0.97 measured looking identical). Put measured and target on one fixed scale, or read values at the cursor.
- **Trigger fault versus real data.** A maximum rpm far above anything the engine reached (tens of thousands after a 7000 rpm pull), or sharp spikes in a smooth ramp, often in one rpm band, means spurious trigger pulses. Log rpm, rpm rate of change and the trigger error counter.
- **Airflow-meter ceiling versus fuel-system limit.** On a mass-airflow engine both show as lambda going lean toward the top of a pull. If logged airflow flattens while power is still rising, or the raw sensor output sits at the top of its range, the meter is at its limit. Otherwise check fuel pressure and injector duty. A healthy airflow trace follows the shape of the power curve.
- **Heat soak versus a real error.** Compare intake and coolant temperatures with their normal driving values. Errors that fade as they return to normal were soak.
- **Drift versus table error.** If error changes with time in the session rather than with cell, look at temperatures, fuel pressure and baro before editing the table.
- **Oil pressure surge versus a pump fault.** A brief oil pressure dip tied to sustained lateral, braking or acceleration load that recovers at once is surge; check throttle and load at the moment, since a dip with no load is less serious than the same dip under high load.

## Decision rules
Reject samples with: cold or unstable temperatures, or heat soak (wait for intake and coolant to return to normal driving values, which the sources reach after two or three minutes at speed); invalid or heater-not-ready wideband; acceleration enrichment or a limiter active; rapid rpm or throttle change; overrun fuel cut and closed throttle; gear changes and the first moments after a shift; samples in the window after a commanded lambda target step. Align lambda by the estimated delay. Log core channels: rpm, throttle, manifold pressure, lambda and lambda target, timing and injector duty, plus closed-loop trim and status, the acceleration enrichment channel, limiter and protection status. Confirm the wideband against a second reference where possible: a steady calibration offset is invisible in a log alone.

Thresholds seen in the sources, as examples rather than limits: closed throttle filtered below about 5 to 10 % throttle position or just above the true closed position; throttle rate of change beyond about 10 % treated as transient; rpm rate filters of about 15 to 20 % per second on road data, and about 2500 rpm per second used to reject shift data on a race car; lambda values implausibly rich (below about 0.5) dropped as sensor faults.

Rates between 1 and 25 Hz suit most channels; match the rate to the sensor. Make sure the load axis used for analysis is the one the fuel table uses, and the target load matches the target table's axis: a correction mapped by the wrong load source lands in the wrong cells. Never trust a data channel whose calibration has not been confirmed. Compare a factory wideband with a known good meter before relying on it. Exclude overrun samples, which look lean.

With closed loop active, analyse uncorrected error: measured lambda with the closed-loop correction removed, compared with target. One practitioner now drives in closed loop on an untuned base map for safety and calibrates from this corrected channel. For factory ECUs in closed loop, the summed short- and long-term trims serve the same role; in open loop, use wideband error against commanded.

Check where the ECU was, not where it was assumed to be. At altitude or with a restrictive intake, full throttle on a naturally aspirated engine can sit well below the atmospheric row (one demonstration at altitude fell from about 96 to 92 kPa absolute through a pull; restrictive intakes can lose 10 to 15 kPa at high rpm), so the ECU interpolates with the row below. Use the ECU's table cursor or logged load to find the cells.

Review vitals first. Before using a log for tuning, confirm oil pressure, coolant and oil temperature, fuel pressure and battery voltage were normal and stable. A lean condition in the most dangerous zone (sustained high load, moderate to high rpm) is checked before anything else; if it is lean there, nothing else matters.

## Data gates
These rules are the gates. Numeric thresholds are project defaults in tools/analysis/gates.py and are marked unsourced; the source values above are context for them.

## Worked example
Of 12000 samples, 8000 are rejected: 5000 cold, 2000 transient and 1000 at a limiter. The remaining 4000 are unevenly spread, so only well-sampled cells are analysed.

A road log shows lambda 1.9 at 3500 rpm in places during cruise, and measured lambda looks richer than target everywhere. The lean readings coincide with closed throttle: overrun, rejected. The everywhere-rich offset disappears when both traces are put on the same fixed 0.8 to 1.1 scale: it was a graph scaling difference, not a fuelling error.

## Disputed / conflicts
- **Closed loop on or off while collecting.** Several sources turn closed loop off so errors stay visible, and note that some automatic correction tools compare measured with target only and ignore the trim. One practitioner instead keeps closed loop on and removes the correction mathematically, arguing that open loop on an untuned map can be unsafe to drive. Both give valid data if the trim is logged and removed correctly; the open-loop route is simpler to check.
- **Filter thresholds** vary between sources and loggers (5 % versus 10 % closed throttle; rpm-rate versus throttle-rate filters). They are tuned to the channel names and rates available; none is a universal number.

## Citations
- practice: Practitioner training and tuning practice, distilled and cross-checked.
- reference-data: Published reference data: thermophysical properties, fuel data, sensor and injector data sheets, statistics.
