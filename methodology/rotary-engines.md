---
id: methodology/rotary-engines
title: Rotary engine tuning
layer: L2
status: draft
confidence: low
sources: [practice]
verified: 2026-11-10
applies_to: {fuels: [gasoline, ethanol, methanol], engines: [rotary]}
depends_on: [principles/combustion/mbt-timing, principles/combustion/knock]
supersedes: []
---

# Rotary engine tuning

## Claim
Rotary engines run richer than a piston engine at the same load and need correct leading/trailing plug timing. The split between plugs affects timing as a whole.

## Why (derivation)
Exhaust temperatures and sealing make richer operation normal. Reducing the leading-to-trailing split has the same effect as advancing timing, and firing the trailing plug first is dangerous.

## Assumptions
Twin-plug rotary with independent trailing control.

## Breaks when
Late trailing strategies and port types vary.

## Practical use
Understand the sign convention in the software before entering any split. Check base timing marks carefully, the most common place for damage.

## Decision rules
Idle is often richer than lambda 1, particularly with a ported engine. Practitioners report lambda near 0.90 at 100 kPa and a few points richer than a piston engine at boost. Splits often around 15 degrees at idle and cruise, reducing to 8 to 10 at high boost in one practitioner's experience. Reducing the split is the same as advancing timing.

## Data gates
As for piston engines, with EGT if available.

## Worked example
A positive split value on one software package may mean the trailing plug fires first. Check the sign before entering a value.

## Disputed / conflicts
None recorded.

## Citations
- practice: Practitioner training and tuning practice, distilled and cross-checked.
