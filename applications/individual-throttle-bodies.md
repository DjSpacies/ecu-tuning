---
id: applications/individual-throttle-bodies
title: Individual throttle body profile
layer: L4
status: draft
confidence: low
sources: [practice]
verified: 2026-11-10
applies_to: {fuels: [gasoline, ethanol, methanol], engines: [itb]}
depends_on: [principles/airflow/volumetric-efficiency]
supersedes: []
---

# Individual throttle body profile

## Claim
With individual throttle bodies there is little manifold vacuum signal, so a pressure-based load is unstable and throttle position is the usual load.

## Why (derivation)
Without a shared plenum, pressure at low load carries strong per-cylinder pulses, and pressure changes little with load.

## Assumptions
No shared plenum.

## Breaks when
Combining individual throttles with forced induction needs a more complex fuel model, and is for experienced tuners.

## Practical use
Choose throttle position as the load axis for fuel, keeping manifold pressure for ignition under boost where both are present (training session 089); choose throttle position, and note that airflow rises far faster in the first half of throttle travel, so use unevenly spaced throttle sites.

## Worked example
Use more throttle sites below 50 % than above it.

## Disputed / conflicts
None recorded.

## Citations
- practice: Practitioner training and tuning practice, distilled and cross-checked.
