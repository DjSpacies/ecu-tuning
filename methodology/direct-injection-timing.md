---
id: methodology/direct-injection-timing
title: Direct injection timing
layer: L2
status: draft
confidence: low
sources: [practice]
verified: 2026-11-10
applies_to: {fuels: [gasoline, ethanol, methanol], engines: [all]}
depends_on: [applications/direct-injection]
supersedes: []
---

# Direct injection timing

## Claim
In direct injection the injection event must finish before the spark, so timing is a window in crank degrees that shrinks in time as rpm rises.

## Why (derivation)
There are 720 crank degrees in a cycle, but fuel must be delivered within about 300 to 320 of them, before ignition. Injecting too early while the exhaust valve is open loses fuel to the exhaust.

## Assumptions
Knowledge of the injection timing reference used by the software (start or end, and from which top centre).

## Breaks when
Different software references timing differently, and the value's zero point varies.

## Practical use
Compute how many crank degrees an injection occupies, and check it fits.

## Decision rules
Degrees occupied = pulse in ms x rpm x 6 / 1000. Keep the end of injection clear of the most advanced spark by a margin. Instruction coverage is thin: treat as draft and check against the platform's own documentation.

## Data gates
Fuel rail pressure, pulse width and injection timing logged.

## Worked example
At 6000 rpm the crank turns 36 degrees per millisecond, so an 8.5 ms injection takes 306 degrees, close to the available window.

## Disputed / conflicts
None recorded.

## Citations
- practice: Practitioner training and tuning practice, distilled and cross-checked.
