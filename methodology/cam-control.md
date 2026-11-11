---
id: methodology/cam-control
title: Cam control tuning
layer: L2
status: draft
confidence: low
sources: [practice, engineering-texts]
verified: 2026-11-10
applies_to: {fuels: [gasoline, ethanol, methanol], engines: [all]}
depends_on: [principles/airflow/volumetric-efficiency]
supersedes: []
---

# Cam control tuning

## Claim
Variable cam timing is another axis to optimise: find the cam angle that gives the best torque first, and fuel and ignition for that shape afterwards.

## Why (derivation)
Valve events change airflow across speed and load, so moving the cams changes VE everywhere. A fuel table tuned at one cam setting is wrong at another.

## Assumptions
Cam control is stable, and measured torque is available.

## Breaks when
Switched cam systems have a sharp airflow change at the changeover, where inconsistency is expected.

## Practical use
Tune cam targets early, with fuel and ignition in a safe state. Retune fuel after changing cam targets.

## Decision rules
Choose target angle by torque at each site. For a switched system, set up the two tables first and choose the changeover where the torque curves cross, not at a low rpm.

Change cam angles by about 2 degrees at a time. Advancing the intake cam on a knock-limited engine can be dangerous. The intake cam usually matters more than the exhaust. If in doubt about safe cam limits, ask the engine builder.

## Data gates
Cam position tracks its target before the torque reading is used.

## Worked example
Moving a cam target by 5 degrees changes lambda at that site. Correct fuel only after the angle is chosen.

## Disputed / conflicts
Cross-check: The combustion textbook and an automotive handbook show inlet valve closing setting how filling trades low speed against high speed, which supports the intake cam having the larger effect. The 2-degree step is practice.

## Citations
- practice: Practitioner training and tuning practice, distilled and cross-checked.
- engineering-texts: Engine, combustion, charging and control engineering texts.
