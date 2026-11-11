---
id: methodology/launch-and-antilag
title: Launch control and anti-lag
layer: L2
status: draft
confidence: low
sources: [practice]
verified: 2026-11-10
applies_to: {fuels: [gasoline, ethanol, methanol], engines: [turbo, na]}
depends_on: [methodology/full-load]
supersedes: []
---

# Launch control and anti-lag

## Claim
These strategies deliberately run ignition far retarded and with cuts at high load. They trade component life for response, so they are bounded and conditional.

## Why (derivation)
Retarded timing and cuts put fuel and heat into the exhaust, spooling the turbine, at the cost of very high exhaust temperatures and stress.

## Assumptions
The user accepts the mechanical cost, and the use is on a closed course.

## Breaks when
Prolonged use damages exhaust and turbo components.

## Practical use
Enable conditionally, by throttle, coolant and speed, and keep usage short.

## Decision rules
Require conditions: throttle above a threshold and coolant warm enough. Log ignition and any cuts. Begin with conservative retard and verify exhaust temperature if measured.

Anti-lag depends on unburned fuel and air reaching the exhaust, so its heat is intrinsic. A shift cut that is too short re-applies torque in mid-shift.

## Data gates
Launch-active status logged.

## Worked example
Launch engages only over 60 C coolant and below a speed limit, so it cannot run on a cold engine or at speed.

## Disputed / conflicts
None recorded.

## Citations
- practice: Practitioner training and tuning practice, distilled and cross-checked.
