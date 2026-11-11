---
id: methodology/knock-assessment
title: Assessing knock
layer: L2
status: draft
confidence: medium
sources: [practice, engineering-texts]
verified: 2026-11-10
applies_to: {fuels: [gasoline, ethanol, methanol], engines: [all]}
depends_on: [principles/combustion/knock]
supersedes: []
---

# Assessing knock

## Claim
Knock evidence comes from more than one channel and is judged by the worst plausible case. An ECU knock control system does not make a poor tune safe.

## Why (derivation)
Sensor signals carry mechanical noise that grows with rpm, and thresholds are set by someone. Audio monitoring and ECU knock levels can disagree, so a clean signal is weak evidence and a suspicious one is strong.

## Assumptions
The monitoring system has been set up and validated for this engine.

## Breaks when
Very high rpm, noisy valvetrain or loose sensor mounting will hide or fake events.

## Practical use
Treat a threshold crossing, or audible knock, as real until shown otherwise.

## Decision rules
On any knock event during a run: abort, then remove 2 to 3 degrees in that region before trying again. Never answer knock by raising a threshold or disabling detection. Find the cause when knock appears suddenly at a known-good point (fuel, temperature, boost).

The threshold is meant to sit just above the engine's background noise at every rpm and load point, and that noise changes with both. When the background exceeds the threshold, knock control triggers falsely and the engine runs retarded for nothing. Measure the background where the engine is known not to knock (low load across the rpm range), confirm with audio, and set the threshold from that. This calibration is different from raising a threshold because knock was reported: that is never done without the noise-floor evidence. Some systems also mask known noise events such as gear shifts. Validate any detection system against audio before trusting it: practitioners report both false alarms and ECUs that missed knock that could be heard. Keep the threshold just above the no-knock background (one practitioner starts about 10 % above a clean run's reading), and re-check it through the rev range. Mount a sensor on a flat, solid area high on the block where possible. Tune on the fuel the engine will actually run. Never hold the engine in knock to finish a run: back off first, and repeat. Knock always follows the spark; pre-ignition comes before it, and the two are different faults.

## Data gates
Knock channel present and meaningful; a defined window of crank angle; sample rate adequate for the event.

## Worked example
A log shows one cylinder over the threshold during a pull. Abort, remove timing on that part of the map, repeat, and only then consider a per-cylinder approach.

## Disputed / conflicts
Cross-check: the factors that raise knock in the combustion textbook (timing, inlet temperature, coolant temperature, load, mixture near its peak) match the practitioners. The combustion textbook places the knock resonance between 3 and 10 kHz depending on bore and chamber shape, which supports choosing frequency from bore. Audio confirmation of a sensor system is practice, with no textbook test of it.

## Citations
- practice: Practitioner training and tuning practice, distilled and cross-checked.
- engineering-texts: Engine, combustion, charging and control engineering texts.
