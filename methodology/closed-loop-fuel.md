---
id: methodology/closed-loop-fuel
title: Closed-loop fuel control
layer: L2
status: draft
confidence: medium
sources: [practice, engineering-texts]
verified: 2026-11-10
applies_to: {fuels: [gasoline, ethanol, methanol], engines: [all]}
depends_on: [principles/control/feedback-and-pid, principles/data/sensor-lag-and-delay]
supersedes: []
---

# Closed-loop fuel control

## Claim
Closed loop trims small errors after the open-loop map is correct. Its limits, lockouts and gains decide how far a sensor fault can move the fuel.

## Why (derivation)
Delay in the path from injector to sensor limits how fast the loop can run. An out-of-range sensor can drive trim the wrong way, so authority must be bounded.

## Assumptions
A healthy, warm sensor.

## Breaks when
High-load or very rich operation near its accuracy limit, sensor fouling or exhaust leaks.

## Practical use
Tune it open-loop first, then enable, with restricted authority.

## Decision rules
Use lockouts for cold engine, rpm and load. Restrict the trim limit. Treat large persistent trims as a base-map error to fix, not something for closed loop to carry. A load lockout keeps it out of the high-load region where mixture is set by the map.

Tune the base table with closed loop out of the picture, or the measured mixture looks perfect while the trims hide the error. Trims near 1 to 2 % are normal; larger ones show a base-map problem. Narrow band sensors should run only at idle and cruise. One practitioner allows about 5 % authority at high load and disables learning when finished. Trims lag the engine, because they react to what already happened.

## Data gates
Lambda valid; lockouts known; speed-load state away from transients.

## Worked example
A persistent +7 % trim at cruise means the base map is lean there. Fix the base map and let the trim go back near zero.

## Disputed / conflicts
Cross-check: An engine-management textbook states closed-loop lambda stays off until the sensor reaches operating temperature, agreeing with a cold lockout. The 5 % high-load authority figure is one practitioner's and has no textbook value.

## Citations
- practice: Practitioner training and tuning practice, distilled and cross-checked.
- engineering-texts: Engine, combustion, charging and control engineering texts.
