---
id: methodology/water-methanol-injection
title: Water/methanol injection
layer: L2
status: draft
confidence: low
sources: [practice, engineering-texts]
verified: 2026-11-10
applies_to: {fuels: [gasoline, ethanol, methanol], engines: [all]}
depends_on: [principles/fuels/energy-and-charge-cooling, methodology/knock-assessment]
supersedes: []
---

# Water/methanol injection

## Claim
Water/methanol injection buys knock margin, and a tune that uses that margin depends on it. The system must be monitored, and a failure must revert to a safe tune.

## Why (derivation)
Evaporation cools the charge and adds resistance to knock. Timing or boost added on the strength of that is unsafe the moment delivery stops.

## Assumptions
A delivery monitor exists, such as a flow or level switch.

## Breaks when
Tank empty, pump or nozzle failure, or a controller fault.

## Practical use
Tune the base map safely without injection first. Then add margin using it, and switch fuel and timing tables on a verified delivery signal.

## Decision rules
Only add timing or boost if delivery can be detected and the tune falls back when it stops. Without that monitor, do not tune on the assumption it is working.

A common guide is water/methanol flow of about 25 % of the total fuel flow.

## Data gates
Delivery status logged.

## Worked example
A test gained power by adding 4 degrees and 10 kPa. Without a working failsafe, that added margin has to be removed.

## Disputed / conflicts
Cross-check: An engine textbook states water injection is used to mitigate pre-ignition and provide cooling, in general terms. The 25 % flow guide has no textbook value.

## Citations
- practice: Practitioner training and tuning practice, distilled and cross-checked.
- engineering-texts: Engine, combustion, charging and control engineering texts.
