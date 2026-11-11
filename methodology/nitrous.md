---
id: methodology/nitrous
title: Nitrous oxide tuning
layer: L2
status: draft
confidence: low
sources: [practice]
verified: 2026-11-10
applies_to: {fuels: [gasoline, ethanol, methanol], engines: [all]}
depends_on: [principles/combustion/knock, methodology/full-load]
supersedes: []
---

# Nitrous oxide tuning

## Claim
Treat nitrous as added load: more oxygen and fuel, faster combustion. Start with timing retarded from the base map and verify mixture on the first run.

## Why (derivation)
The extra oxygen allows a larger charge. Combustion becomes faster and hotter, so less spark advance is needed for MBT and knock risk rises. Delivery has its own transient on activation.

## Assumptions
A correctly installed system with fuel delivery confirmed.

## Breaks when
Empty bottles and low bottle pressure change delivery, so a tune made at one bottle pressure can be wrong at another.

## Practical use
Use dedicated fuel and timing tables for the nitrous condition, starting conservative, working up.

## Decision rules
Use lambda targets similar to a boosted engine. Remove timing first and add it back gradually; the first test run is conservative. Expect an irregularity in mixture at activation.

## Data gates
Nitrous-active status logged, and bottle pressure if available.

## Worked example
On a first run an extra 4 degrees is removed from the main table during nitrous. After reviewing mixture and knock, timing is added back in steps.

## Disputed / conflicts
None recorded.

## Citations
- practice: Practitioner training and tuning practice, distilled and cross-checked.
