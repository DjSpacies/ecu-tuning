---
id: methodology/base-setup
title: Base setup and pre-start checks
layer: L2
status: draft
confidence: medium
sources: [practice]
verified: 2026-11-10
applies_to: {fuels: [gasoline, ethanol, methanol], engines: [all]}
depends_on: [methodology/tuning-order]
supersedes: []
---

# Base setup and pre-start checks

## Claim
Before an engine is started, inputs read correctly, outputs fire on the right cylinders, and timing is confirmed. A wrong setting found here costs minutes; found running, it can cost an engine.

## Why (derivation)
Every calculation the ECU makes starts from sensor values and crank angle. A timing reference wrong by tens of degrees or one full revolution creates a misfire or a fire outside the combustion stroke.

## Assumptions
Standalone-style configuration where these settings are exposed.

## Breaks when
Factory-ECU reflashes often hide or fix these settings, so the checks change to verifying what the calibration claims.

## Practical use
Run the checks in order and record results. Base table sizes are a starting point; zones can be added later.

## Decision rules
Check each sensor against a known reference. Verify base timing with a timing light at a locked value. If the engine will not fire and timing appears correct, a 360-degree error is a likely cause. Load axis choice comes first, since changing it later affects the whole tune. Start with 500 rpm zones and about 20 kPa load zones, finer near idle and cruise, and refine after running.

A wrong reluctor sensor polarity shows as timing drift with rpm, so sweep the rpm with timing locked and confirm it stays steady. Always check the fuel pressure, even on an unadjustable system. Verify base timing with a simple inductive light; on wasted-spark systems a dial-back light reads double. Remember to release the timing lock afterwards.

## Data gates
Battery voltage holds during cranking. Temperature and pressure sensors agree with ambient on a cold engine.

## Worked example
An engine locked at 15 degrees reads 25 on the timing light: the timing reference is wrong by 10 degrees and must be fixed before any table is tuned.

## Disputed / conflicts
None recorded.

## Citations
- practice: Practitioner training and tuning practice, distilled and cross-checked.
