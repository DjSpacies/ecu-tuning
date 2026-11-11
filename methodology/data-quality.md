---
id: methodology/data-quality
title: Data quality for tuning logs
layer: L2
status: draft
confidence: medium
sources: [practice, reference-data]
verified: 2026-11-10
applies_to: {fuels: [gasoline, ethanol, methanol], engines: [all]}
depends_on: [principles/data/statistics-for-tuning, principles/data/sensor-lag-and-delay]
supersedes: []
---

# Data quality for tuning logs

## Claim
Only samples from a valid, steady state support a change. Decide which samples qualify before computing anything, and report what was rejected.

## Why (derivation)
Warm-up, transient enrichment, limiters and lag all produce plausible numbers that describe the wrong condition.

## Assumptions
Log channels exist for the conditions being tested, or the missing ones are reported.

## Breaks when
A low log rate can't resolve transient events.

## Practical use
Apply the gate checks in order and show the rejection counts.

## Decision rules
Reject samples with: cold or unstable temperatures; invalid or heater-not-ready wideband; acceleration enrichment or a limiter active; rapid rpm or throttle change; overrun fuel cut. Align lambda by the estimated delay. Log core channels: rpm, throttle, manifold pressure, lambda, timing and injector duty. Confirm the wideband against a second reference where possible: a steady calibration offset is invisible in a log alone.

Rates between 1 and 25 Hz suit most channels; match the rate to the sensor. Make sure the load axis used for analysis is the one the fuel table uses. Never trust a data channel whose calibration has not been confirmed. Compare a factory wideband with a known good meter before relying on it. Exclude overrun samples, which look lean.

## Data gates
These rules are the gates. Numeric thresholds are project defaults in tools/analysis/gates.py and are marked unsourced.

## Worked example
Of 12000 samples, 8000 are rejected: 5000 cold, 2000 transient and 1000 at a limiter. The remaining 4000 are unevenly spread, so only well-sampled cells are analysed.

## Disputed / conflicts
None recorded.

## Citations
- practice: Practitioner training and tuning practice, distilled and cross-checked.
- reference-data: Published reference data: thermophysical properties, fuel data, sensor and injector data sheets, statistics.
