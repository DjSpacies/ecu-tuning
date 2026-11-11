---
id: methodology/log-capture-protocol
title: Capturing a log that can be tuned from
layer: L2
status: draft
confidence: medium
sources: [practice, vendor-documentation]
verified: 2026-11-10
applies_to: {fuels: [gasoline, ethanol, methanol], engines: [all]}
depends_on: [methodology/data-quality, methodology/cold-start-warmup, methodology/closed-loop-fuel, methodology/full-load, methodology/knock-assessment, methodology/road-procedure]
supersedes: []
---

# Capturing a log that can be tuned from

## Claim
An offline analysis is only as good as the log it is given. Plan the log before it is recorded: one known calibration, the right channels, and each operating phase recorded deliberately and in order of risk.

## Why (derivation)
The analyses reject samples that are cold, transient, at a limiter, under closed-loop trim or from an unwarmed wideband (methodology/data-quality). A log driven without a plan is mostly rejected samples. A log also does not record edits made to the ECU while it runs, so a tune file and a log describe the same calibration only if nothing changed in between. Phases recorded in a fixed order let each analysis find its own data: warm-up data for warm-up tables, steady data for the base tables, full-load data for the top rows.

## Assumptions
The ECU can log the channels below at a suitable rate. Full-load phases happen only on a dyno, a track or a closed road, with the rev limit, boost ceiling, fuel and knock detection declared.

## Breaks when
The engine has a fault that the health check would find (fix that first); the log rate cannot resolve the events of interest; the road or conditions do not allow steady driving.

## Practical use
Give the user a capture plan for the analysis they want, then check the log against it with the capture review before analysing anything.

## Decision rules
Before recording:
- Save the tune file that is in the ECU, and make no changes until logging stops. If a change is unavoidable, note the time and treat the two halves as separate logs.
- Power the wideband early so it is warm before data is needed. Confirm its calibration matches the ECU input.
- Log at least rpm, throttle, manifold pressure, lambda and lambda target, timing, injector duty and pulse width, coolant and intake temperature, battery voltage, closed-loop trim and status, knock level and count, and limiter and cut status. Add fuel and oil pressure, ethanol content, EGT, gear and speed where fitted. Where the ECU can log the value it reads from each fuel and ignition table, log those too: they are the only proof of which calibration ran.
- Rates of 1 to 25 Hz suit most channels; match the rate to the sensor and use the faster end for transients and knock.
- For base fuel table work, turn closed-loop lambda off, or the measured mixture will look right while the trims hide the error. If it must stay on, log the trims.

Recording, in this order:
1. Start logging with the key on before cranking, so priming, cranking and the first seconds after start are captured.
2. Let the engine idle from cold to operating temperature without touching the throttle. This is the warm-up and cold-idle data.
3. Idle warm for a few minutes, with any loads (fans, air conditioning) noted.
4. Drive steadily: hold rpm and load at as many steady points as the road allows, with smooth throttle, using gear choice to set load. Repeat points rather than chase new ones.
5. If knock detection is to be checked, add part-throttle, low-load running up through the rpm range where knock is reported, so the noise floor at that rpm can be separated from load. A level that rises with rpm at low load is mechanical noise; one that appears only with load and advance may be knock. Confirm with audio either way.
6. If transient fuelling is to be reviewed, add separate, deliberate throttle tip-ins at different rates, kept apart from the steady driving.
7. Only with the limits above declared, and on a dyno, track or closed road: full-throttle pulls in a gear that gives several seconds of acceleration (the project owner uses third gear from about 3000 rpm), ending below the declared rev limit. Do one pull, stop and review it before any more. Lift at once on any knock or abort condition. Let temperatures recover between pulls.
8. Stop logging, save the log, and record anything that changed during it.

A log is not tuning data when: the tune changed during it; it mixes fuels; closed-loop trim was active for base-table work and was not logged; the wideband was not warm; or the health check fails.

## Data gates
Uses methodology/data-quality. The capture review counts each phase, reports what is missing, and says what to record next time.

## Worked example
A 15-minute road log starts with the engine already warm, has closed loop on throughout and contains no full-throttle data. The capture review reports no cold start, no warm-up, base fuel not judgeable, and no full-load data, and asks for a new log that starts before cranking with closed loop off.

## Disputed / conflicts
None recorded. The recording order is the project owner's stated practice, assembled with the sourced rules in the entries this depends on.

## Citations
- practice: Practitioner training and tuning practice, distilled and cross-checked.
- vendor-documentation: ECU and tuning-tool vendor documentation.
