---
id: methodology/transient-tuning
title: Transient fuel tuning
layer: L2
status: draft
confidence: medium
sources: [practice, engineering-texts]
verified: 2026-11-10
applies_to: {fuels: [gasoline, ethanol, methanol], engines: [all]}
depends_on: [principles/fueling/transient-fuel-film, methodology/steady-state-fuel]
supersedes: []
---

# Transient fuel tuning

## Claim
Tune transient enrichment only after steady-state is right, testing real throttle events and judging both quantity and decay.

## Why (derivation)
The wall film and air-estimation lag are transient effects. Steady-state errors would be misread as transient ones.

## Assumptions
Port injection and a steady-state fuel map within tolerance.

## Breaks when
Sensor lag can show a false lean spike. Cold transient needs separate treatment.

## Practical use
Check rpm zones one by one. Enrichment is usually greatest at low rpm and low air speed.

## Decision rules
Hesitation with a lean spike: more enrichment. Bog with a rich reading: less. If lambda is good initially then wanders, adjust decay time. Often little or no enrichment is needed above 5000 rpm.

Do not use enrichment to patch a poorly tuned main fuel table: practitioners name this as the most common mistake. Make reasonably large changes while testing, since 2 to 3 % will not be visible. Test from about the same manifold pressure each time, with closed loop off.

## Data gates
Warm engine; throttle events repeatable; lambda sensor delay accounted for.

## Worked example
Stabbing the throttle at 2500 rpm shows a 0.3 s lean spike. Raising enrichment there removes it without changing cruise.

## Disputed / conflicts
Cross-check: the wall film explanation matches the combustion textbook and an engine-control textbook, which give the model but no enrichment procedure.

## Citations
- practice: Practitioner training and tuning practice, distilled and cross-checked.
- engineering-texts: Engine, combustion, charging and control engineering texts.
