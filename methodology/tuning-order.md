---
id: methodology/tuning-order
title: Overall tuning order
layer: L2
status: draft
confidence: medium
sources: [practice]
verified: 2026-11-10
applies_to: {fuels: [gasoline, ethanol, methanol], engines: [all]}
depends_on: []
supersedes: []
---

# Overall tuning order

## Claim
Tune in an order that makes each stage safe for the next: configure and verify first, then start and idle, then fuel before ignition in steady state, then full load, then confirm in real conditions.

## Why (derivation)
Later stages depend on earlier ones. Fuel affects combustion speed and knock, so ignition is optimised on a stable fuel base. Full-load work is the highest-risk and is only attempted once the region around it is proven safe. Mechanical or sensor faults found late waste all the work above them.

## Assumptions
An engine that runs mechanically, with correct sensors and known fuel.

## Breaks when
A new fuel or mechanical change resets the stages it affects. Knock-limited engines may need ignition revisited after full-load findings.

## Practical use
Workflows and session plans follow these stages and mark which are complete.

## Decision rules
1. Configure and test inputs and outputs. 2. Trigger setup. 3. Base table configuration. 4. Base ignition timing and fuel pressure. 5. Initial start. 6. Idle. 7. Steady-state fuel. 8. Steady-state ignition. 9. Full-power tuning. 10. Confirm in real conditions. Do not skip forward over an unresolved fault.

## Data gates
Each stage has its own gates in its own entry.

## Worked example
An engine starts but its trigger scope shows missing sync events under load. Stop: stage 2 is not complete, regardless of how far fuel tuning has got.

## Disputed / conflicts
None recorded.

## Citations
- practice: Practitioner training and tuning practice, distilled and cross-checked.
