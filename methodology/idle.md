---
id: methodology/idle
title: Idle tuning
layer: L2
status: draft
confidence: medium
sources: [practice]
verified: 2026-11-10
applies_to: {fuels: [gasoline, ethanol, methanol], engines: [all]}
depends_on: [methodology/first-start]
supersedes: []
---

# Idle tuning

## Claim
Set mixture and a stable ignition value first, then idle air control. Idle is sensitive to injector data, so bad dead-time data shows up here first.

## Why (derivation)
At idle, pulses are short, so dead-time error is a large fraction of delivered fuel. Ignition timing away from MBT gives the ignition a torque reserve in both directions, which is what idle ignition control uses.

## Assumptions
Idle target is realistic for the engine.

## Breaks when
Large overlap cams dilute the idle charge and read misleadingly in the exhaust.

## Practical use
Check smoothness and consistency of the idle ignition numbers, then mixture, then the air control base position, then closed-loop gains last.

## Decision rules
Typical idle advance is 15 to 20 degrees; heavily cammed engines often settle at 12 to 15. If ignition idle control is used, start 6 to 8 degrees retarded from the chosen base. Stock engines idle about lambda 0.95 to 1.0. Do not run richer than about 0.90 for long: plug fouling and bore wash. Choose a realistic idle speed; cold idle is commonly 200 to 300 rpm higher.

Prove idle with closed loop and ignition idle control off, because they mask errors in the base idle position. Set a realistic idle speed; forcing an unrealistic one is a very common mistake. Sitting below MBT keeps torque in reserve to control speed in both directions; one practitioner avoids sustaining much below about 5 degrees. Closed-loop gains can be raised until oscillation starts, then backed off. A stepper or a boost-style solenoid behaves differently, so check its frequency range.

## Data gates
Engine warm and stable; no electrical loads switching during measurement.

## Worked example
A cammed engine hunts at 15 degrees. Retarding to 12 degrees and adding idle air stabilises it, at the cost of a little more air.

## Disputed / conflicts
Cross-check: no textbook passage on idle ignition reserve was found in this corpus, so the torque-reserve explanation rests on practitioners and the MBT physics.

## Citations
- practice: Practitioner training and tuning practice, distilled and cross-checked.
