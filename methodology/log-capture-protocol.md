---
id: methodology/log-capture-protocol
title: Capturing a log that can be tuned from
layer: L2
status: draft
confidence: medium
sources: [practice, vendor-documentation]
verified: 2026-11-11
applies_to: {fuels: [gasoline, ethanol, methanol], engines: [all]}
depends_on: [methodology/data-quality, methodology/cold-start-warmup, methodology/closed-loop-fuel, methodology/full-load, methodology/knock-assessment, methodology/road-procedure]
supersedes: []
---

# Capturing a log that can be tuned from

## Claim
An offline analysis is only as good as the log it is given. Plan the log before it is recorded: one known calibration, the right channels at the right rates, and each operating phase recorded deliberately and in order of risk. Live data cannot be revisited; every tuning drive, pull and race pass should be logged.

## Why (derivation)
The analyses reject samples that are cold, transient, at a limiter, under closed-loop trim or from an unwarmed wideband (methodology/data-quality). A log driven without a plan is mostly rejected samples. A log also does not record edits made to the ECU while it runs, so a tune file and a log describe the same calibration only if nothing changed in between. Phases recorded in a fixed order let each analysis find its own data: warm-up data for warm-up tables, steady data for the base tables, full-load data for the top rows.

Events in a pull or a corner happen too fast to watch live. The sources review the log calmly after the run, step through it, and use the ECU's cell marker to see which cells were in use at each instant. Where the ECU cannot be edited live (most factory ECUs), logging is the whole method.

Rate and channel count trade against each other. A logger has finite bandwidth and memory; on diagnostic-port logging of factory ECUs, each extra parameter lowers the rate for all of them (one demonstration fell to about three samples per second with a large list). Logging faster than a sensor can change adds nothing; logging slower than the event hides it.

## Assumptions
The ECU can log the channels below at a suitable rate. Full-load phases happen only on a dyno, a track or a closed road, with the rev limit, boost ceiling, fuel and knock detection declared.

## Breaks when
The engine has a fault that the health check would find (fix that first); the log rate cannot resolve the events of interest; the road or conditions do not allow steady driving; the logging link is intermittent (a faulty cable caused repeated disconnects in one session; confirm the ECU is online after each store and that the log is complete).

## Practical use
Give the user a capture plan for the analysis they want, then check the log against it with the capture review before analysing anything.

### Channel sets by task
Keep each list small and task-specific; clutter distracts and, on bandwidth-limited links, lowers the rate.
- **Fuel, steady and road:** rpm, throttle, manifold pressure (or the table's own load channel), lambda and target, closed-loop trim and status, acceleration enrichment, injector pulse width and duty, coolant and intake temperature, fuel pressure (differential where measured).
- **Full-throttle pull:** add timing, knock level and count, boost and boost target, injector duty for headroom, and the limiter status channels.
- **Factory ECUs with airflow meters:** airflow in g/s and the raw meter voltage or frequency (the axis of the meter calibration), calculated load, short- and long-term trims, open/closed-loop status, commanded and measured lambda, knock correction and any learned advance multiplier.
- **Engines with variable cams:** cam target and measured position, so data can be split by cam position.
- **Transients:** rpm, throttle rate, acceleration enrichment, effective and actual pulse width, lambda and target, at the ECU's internal rate.
- **Health and protection:** oil and fuel pressure, coolant, oil and intake temperatures, battery voltage, protection and limiter status, and the warning-acknowledge channel where the ECU has one (it shows whether a driver dismissed warnings before a failure).
- **Trigger health:** rpm, rpm rate of change and the trigger error counter on every ramp run.

### Rates
Typical in the sources: lambda, manifold and boost pressure, rpm and other fast engine channels at about 20 to 25 Hz; oil and fuel pressure at no less than about 20 Hz where surge matters, because 5 to 10 Hz defaults can miss it; coolant and air temperatures at 1 to 2 Hz (one source found 1 Hz slightly slow for coolant; intake temperature a bit faster on turbo engines); pressure transients such as lift-off spikes much faster; shift-system and gear-position checks at around 200 Hz. Onboard logging capacity varies widely between ECUs, from about 100 Hz to about 1000 Hz maximum in one comparison.

### Laptop versus onboard logging
Laptop logging suits the dyno and ride-along road tuning. Onboard logging is needed for drag, circuit, rally and other use where a laptop cannot ride along, and on cars where each pass costs parts wear: set it up and verify it before the first run, with automatic start and stop (examples in the sources: start above about 2000 or 3000 rpm and stop about 10 s after rpm falls or reaches zero) and a check that memory lasts the session. Some laptop logs include a short history from before the record button was pressed; that section predates the run.

### Viewing layouts
Build task-specific pages rather than relying on defaults: the table being tuned beside the live channels and log playback. Overlay only channels of similar scale and behaviour; give rpm, oil pressure and injector duty their own groups; fix lambda axes manually (for example 0.7 to 1.1) because auto-scaling stretches to the lean peg at lift-off and flattens everything; give each overlaid sensor its own colour. Save the layout explicitly, since some software loses unsaved layouts on update.

## Decision rules
Before recording:
- Save the tune file that is in the ECU, and make no changes until logging stops. If a change is unavoidable, note the time and treat the two halves as separate logs.
- Power the wideband early so it is warm before data is needed. Confirm its calibration matches the ECU input.
- Log at least rpm, throttle, manifold pressure, lambda and lambda target, timing, injector duty and pulse width, coolant and intake temperature, battery voltage, closed-loop trim and status, knock level and count, and limiter and cut status. Add fuel and oil pressure, ethanol content, EGT, gear and speed where fitted. Where the ECU can log the value it reads from each fuel and ignition table, log those too: they are the only proof of which calibration ran.
- Rates of 1 to 25 Hz suit most channels; match the rate to the sensor and use the faster end for transients and knock.
- For base fuel table work, turn closed-loop lambda off, or the measured mixture will look right while the trims hide the error. If it must stay on, log the trims.
- Make sure every channel a filter needs is in the list (throttle position above all).

Recording, in this order:
1. Start logging with the key on before cranking, so priming, cranking and the first seconds after start are captured. A log of a failed start is the only way to review it afterwards.
2. Let the engine idle from cold to operating temperature without touching the throttle. This is the warm-up and cold-idle data.
3. Idle warm for a few minutes, with any loads (fans, air conditioning) noted.
4. If the engine has sat hot (after a reflash, a roadside stop or dyno idling), drive at speed for a few minutes until intake and coolant temperatures are back at normal driving values before the steady phase.
5. Drive steadily: hold rpm and load at as many steady points as the road allows, with smooth throttle, using gear choice to set load and staying in one gear where possible. Repeat points rather than chase new ones. The sources gather at least 5 to 10 minutes of varied driving, and around 20 minutes once the engine runs well. On a dyno, hold each cell for a few seconds until it settles before moving on.
6. If knock detection is to be checked, add part-throttle, low-load running up through the rpm range where knock is reported, so the noise floor at that rpm can be separated from load. A level that rises with rpm at low load is mechanical noise; one that appears only with load and advance may be knock. Confirm with audio either way. Without a knock channel, a log-marker button pressed when knock is heard marks the spot.
7. If transient fuelling is to be reviewed, add separate, deliberate throttle tip-ins at different rates, kept apart from the steady driving.
8. Only with the limits above declared, and on a dyno, track or closed road: full-throttle pulls in a gear that gives several seconds of acceleration (the project owner uses third gear from about 3000 rpm), ending below the declared rev limit. Let lambda settle at full throttle before the data of interest and finish the data before lifting. Do one pull, stop and review it before any more. Lift at once on any knock or abort condition. Let temperatures recover between pulls.
9. To check a closed-loop controller (boost, cam, idle), command a step in its target during the run and log target, measured value, output duty and the individual control terms where available; a plain ramp does not exercise the controller once it is on target.
10. Stop logging, save the log with a name that identifies the test, and record anything that changed during it.

Review order, before any tuning analysis: vitals over the whole session (minimum, maximum and average of coolant, oil temperature, oil and fuel pressure, battery voltage; whether temperatures stabilised or were still rising), then protection or limiter events, then lambda in the most dangerous zone, then the tuning analyses.

A log is not tuning data when: the tune changed during it; it mixes fuels; closed-loop trim was active for base-table work and was not logged; the wideband was not warm; the engine was heat soaked; or the health check fails.

Keep logs. Logging every channel on every run builds a baseline: slow deterioration (fuel or oil pressure, pump current, crankcase pressure trend) is found by comparing old runs with new.

## Data gates
Uses methodology/data-quality. The capture review counts each phase, reports what is missing, and says what to record next time.

## Worked example
A 15-minute road log starts with the engine already warm, has closed loop on throughout and contains no full-throttle data. The capture review reports no cold start, no warm-up, base fuel not judgeable, and no full-load data, and asks for a new log that starts before cranking with closed loop off.

A second log has 40 diagnostic-port parameters and runs at about 3 samples per second. The review reports that lambda and load cannot be aligned at that rate and asks for a fuelling-only list of eight parameters.

## Disputed / conflicts
- The recording order is the project owner's stated practice, assembled with the sourced rules in the entries this depends on.
- **How many channels.** Several sources favour a minimal core set to avoid confusion and preserve rate; one notes that logging every channel on every run builds a valuable baseline. The two agree once the logger's rate is not affected by channel count: minimal lists where bandwidth is shared, broad logging where it is not.
- **Closed loop during capture:** see methodology/data-quality.

## Citations
- practice: Practitioner training and tuning practice, distilled and cross-checked.
- vendor-documentation: ECU and tuning-tool vendor documentation.
