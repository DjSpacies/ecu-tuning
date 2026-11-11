---
id: methodology/staged-injectors
title: Staged injection
layer: L2
status: draft
confidence: medium
sources: [practice]
verified: 2026-11-11
applies_to: {fuels: [gasoline, ethanol, methanol], engines: [all]}
depends_on: [principles/fueling/injector-flow-and-dead-time, methodology/injector-characterisation, methodology/fuel-system-sizing]
supersedes: []
---

# Staged injection

## Claim
Two (or more) sets of injectors per cylinder are used either for capacity (a small primary set meters idle and cruise accurately, a large secondary set adds peak flow) or, on highly developed naturally aspirated engines, for mixture quality (injectors far upstream at high load). A staging transition is right when lambda does not change as the secondaries come in and both sets keep headroom everywhere the engine runs. That depends on accurate data for every set and on the secondaries never being asked for pulses too short to open them properly.

## Why (derivation)
- One injector large enough for peak power can sit in its non-linear short-pulse region at idle and cruise, making stable mixture hard (`principles/fueling/injector-flow-and-dead-time`). Fuels needing more mass (E85 about 35 to 40 % more volume, methanol about 2 to 2.5 times) amplify the problem, and rotaries have little injection time per rotor, so they nearly always stage.
- Modern large injectors with good short-pulse behaviour (the 1700 to 2000 cc class) push the point where staging is needed higher. Sources place it mainly at small-displacement, very high power engines on alcohol, roughly 900 to 1400 hp and up.
- Mixture-quality staging: injectors outside the trumpets give more time to mix and vaporise, worth a small power gain valued in tight race classes, but they wet the throttle plates at idle and part throttle and need high air speed to keep fuel suspended. So the port injectors run light load and the upstream injectors take over at high rpm and throttle.
- When the ECU splits a fuel mass between sets, a secondary pulse that is commanded but too short to open the valve is fuel the ECU counts but does not deliver: a lean dip at stage-in.
- An equal fuel-mass split (50 %) between injectors of different size saturates the smaller set first. For maximum total flow both sets should reach maximum duty together, which means equal pulse widths: the secondary share should be 100 x R / (1 + R) %, where R = secondary flow / primary flow.
- Secondaries upstream of the throttle see rail minus barometric pressure, not rail minus manifold, so the ECU needs their location to compute differential pressure; upstream secondaries also add transport delay.

## Assumptions
Enough injector drivers for the chosen mode (sequential staging needs one driver per injector; fewer drivers force grouped secondaries); full characterisation data for every set (separate dead-time table for secondaries); a fuel model that represents airflow well.

## Breaks when
- Nominal flow ratings are inaccurate or at different pressures: one rotary combination rated 2.9 to 1 worked at about 3.3 to 1; a nominal 550 cc injector might flow about 480.
- Secondaries are introduced near their minimum pulse, which is likely when they are much larger than the primaries.
- Grouped secondaries on one driver exceed its current rating; most ECUs use saturated drivers, so paralleled injectors must be high resistance and the total current checked.
- A 2D staging table set from full-load ramp runs leaves the primaries maxed at high-rpm part throttle (mid-corner modulation): in one check at about two-thirds of the rev limit, primary duty reached about 72 % before the secondaries took over.
- A fixed minimum primary off time caps primary duty more at high rpm (one ramp: about 83 % at stage-in near 4800 rpm falling to about 76 % at peak rpm with a 2 ms off time).
- Staging a naturally aspirated engine by throttle at low rpm, where reversion pulsing upsets upstream injectors, is unwise; an rpm lockout prevents it.

## Practical use

### Set-up
- Choose the mode the hardware allows: sequential staged where cam sync and drivers permit; otherwise grouped secondaries, paired by bank (firing order does not matter for grouped secondaries) with driver current checked.
- Enter primary data correctly first, then a separate dead-time and flow set for the secondaries. Enter injector location (before or after the throttle).
- Set the secondary flow ratio from data measured at the same pressure (ideally both sets on the same bench); treat nominal ratings as a starting point.
- Set a secondary pulse lockout so staging waits until the calculated secondary pulse is long enough to be linear: about 1.5 to 2 ms in one session, even with modern injectors. Fully characterised models handle the minimum pulse themselves, visible as a sharp initial step in secondary pulse rather than a ramp from zero.
- On capacity staging, one approach starts staging around 35 to 45 % primary duty and ramps to the matched-pulse share at full load (interpolating from a low start, for example 10 % at about 105 kPa). Another ECU style leaves the staging table at zero, drives the primaries as hard as allowed and adds only the extra fuel needed; in the sources that blended with no visible lambda disturbance.
- For mixture-quality staging, put the staging table on throttle and ramp progressively from all-primary to all-secondary at high rpm and throttle rather than jumping straight to 100 %.
- Use a 3D (rpm by load) staging table so part-throttle high-rpm operation also keeps both sets in headroom.
- Any staging make-up (accel) fuel is a transition pulse for transport delay, not acceleration enrichment. Zero it to isolate it; add it only if a lean dip appears at stage-in, mainly with secondaries far upstream.

### Verification tests
- **Primary-only baseline.** With staging disabled, do a run ready to abort, logging primary and secondary duty overlaid with lambda. In one session the calculated primary duty reached about 140 % and lambda went sharply lean after a rich dip, and the run was aborted as planned. This shows where staging must start.
- **Lambda across stage-in.** If lambda goes rich when secondaries stage in, the secondary/primary ratio is set too low; if lean, too high. Adjust in steps of about 0.1 to 0.2 and rerun against the primary-only baseline. The goal is no change across the transition.
- **Lean dip right at stage-in:** the secondary pulse is below its minimum useful width; raise the lockout or the staging start point. On a fully characterised model, a lambda shift when the split changes points to injector data.
- **Rich dip right at stage-in:** zero the staging make-up fuel; if the dip goes, it was the cause.
- **Matched duty.** At full load both sets should show equal duty (one log: 67.1 % each; another: both sets meeting at about 66 % near 140 kPa, where the earlier rich spike at stage-in had gone).
- **Part-throttle sweep.** After the ramp-run pass, hold about 4500 to 5000 rpm (around two-thirds of the limit) in steady state and sweep throttle from light load upward, checking both banks keep headroom.
- **Off-time limit.** If primary duty falls toward peak rpm because of a fixed off time and the fuel system is at its limit, reduce the off time.

## Decision rules
- Stage only when one set cannot both supply peak flow and meter idle and cruise; otherwise a single modern injector with good short-pulse data is simpler.
- A drag engine that idles only in the lanes can accept a slightly rich idle from huge single injectors; a street or emissions car cannot.
- Recompute the full-load staging share whenever the flow ratio changes.
- Keep headroom in both sets at all times.
- With staged injection and per-cylinder balancing, primaries and secondaries can be trimmed separately to keep cylinders matched through the transition (see `methodology/cylinder-trim`).

## Worked example
Secondaries of 1600 cc over primaries of 550 cc: nominal R = 2.9, so the matched-pulse share is 100 x 2.9 / 3.9 = 74 %. On the engine the working ratio was about 3.3, giving 100 x 3.3 / 4.3 = 76.7 %. With a 50 % share the primaries, one third the size, would saturate while the secondaries idled, leaving a step in delivery once the primaries hit their limit.

## Disputed / conflicts
- **Is staging tuning effort?** Sessions on ECUs with automatic staging and full characterisation report no visible lambda disturbance and no tuning needed; sessions on simpler systems spend most of their time on ratio, lockout and make-up fuel. The difference is the quality of the fuel model and injector data; without good data, mixture steps at stage-in and tuning is an uphill battle.
- **Where to start staging.** One practitioner starts at 35 to 45 % primary duty to keep headroom in both sets; another ECU style deliberately drives primaries to their limit first. Both report smooth results on their systems; the test is the lambda trace across stage-in and the part-throttle sweep.

## Citations
- practice: Practitioner training and tuning practice, distilled and cross-checked.
