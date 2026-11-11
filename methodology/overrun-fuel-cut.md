---
id: methodology/overrun-fuel-cut
title: Overrun and fuel cut
layer: L2
status: draft
confidence: low
sources: [practice]
verified: 2026-11-10
applies_to: {fuels: [gasoline, ethanol, methanol], engines: [all]}
depends_on: [methodology/closed-loop-fuel]
supersedes: []
---

# Overrun and fuel cut

## Claim
During overrun the injectors are often shut off, making lambda readings meaningless. Excluding those samples, and keeping closed-loop trims from reacting, keeps other tuning data honest.

## Why (derivation)
With no fuel, the sensor reads air. A closed-loop system that responds to it adds a large rich correction just as the throttle reopens, which disturbs drivability.

## Assumptions
The ECU has a fuel-cut or a closed-loop lockout.

## Breaks when
Without fuel cut, the area can be tuned similarly to cruise.

## Practical use
Mark fuel-cut samples in logs and exclude them, and make sure closed loop is disabled in overrun.

## Decision rules
With overrun fuel cut in use, mixture in that region does not matter. Without it, keep similar lambda to cruise. A drivability surge on tip-in after lift points to closed-loop trims and fuel-cut recovery.

A common rule of thumb sets the fuel-cut recovery threshold 500 to 800 rpm above target idle.

## Data gates
A fuel-cut or overrun status channel is needed; otherwise infer from throttle closed and high rpm, and say so.

## Worked example
A log shows lambda at maximum for 2 seconds on a closed throttle. Those samples are overrun, and are not lean running.

## Disputed / conflicts
None recorded.

## Citations
- practice: Practitioner training and tuning practice, distilled and cross-checked.
