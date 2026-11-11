---
id: methodology/flex-fuel
title: Flex fuel tuning
layer: L2
status: draft
confidence: medium
sources: [practice, reference-data]
verified: 2026-11-10
applies_to: {fuels: [ethanol, gasoline], engines: [all]}
depends_on: [principles/fuels/stoichiometry-and-lambda, principles/fuels/energy-and-charge-cooling]
supersedes: []
---

# Flex fuel tuning

## Claim
Tune at the fuel-content endpoints that actually occur, with the sensor verified, and make the low-ethanol end the conservative one.

## Why (derivation)
Stoichiometry and knock resistance vary with ethanol content. The ECU interpolates between tables, so the endpoints must be valid and an unexpected low content must fall back to safe timing and boost.

## Assumptions
A verified content sensor and known behaviour on failure.

## Breaks when
Sensor failure, seasonal fuel, or stale fuel in a line after a tank change.

## Practical use
Check the sensor and blend settings first.

## Decision rules
Lambda targets are often the same as on pump fuel, but confirm. Make sure lambda targets are valid in the blended table, or VE values become meaningless. Make the low-ethanol ignition and boost tables safe. If the sensor fails, the fallback must be conservative.

Knock resistance rises most between E0 and about E40, so test some intermediate blends. Fuel temperature from the composition sensor must read sensibly, since it is used to correct the reading. Viscosity changes flow for a given pulse, so use data for each fuel where available. Cranking fuel must rise a lot on ethanol at low temperature.

As a start, raise cranking fuel by 25 to 50 % on ethanol and tune from there. Fuel pump estimates need a 35 to 40 % increase on ethanol.

## Data gates
Measured ethanol content stable; known fuel in the line; fuel temperature plausible.

## Worked example
Unexpectedly, a sensor reports 132 C fuel temperature. Do not trust the sensor or the data derived from it until the fault is fixed.

## Disputed / conflicts
Cross-check: NREL reports ethanol's effect on octane as non-linear, with diminishing effect as content rises, which agrees. The practitioner's specific figure of about E40 is not confirmed there.

## Citations
- practice: Practitioner training and tuning practice, distilled and cross-checked.
- reference-data: Published reference data: thermophysical properties, fuel data, sensor and injector data sheets, statistics.
