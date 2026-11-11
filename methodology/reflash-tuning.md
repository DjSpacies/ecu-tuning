---
id: methodology/reflash-tuning
title: Tuning through a factory ECU reflash
layer: L2
status: draft
confidence: low
sources: [practice, vendor-documentation]
verified: 2026-11-10
applies_to: {fuels: [gasoline, ethanol, methanol], engines: [all]}
depends_on: [methodology/data-quality, methodology/closed-loop-fuel]
supersedes: []
---

# Tuning through a factory ECU reflash

## Claim
A reflash works within the manufacturer's strategy: the closed-loop and power-enrichment modes, and the tables that feed them, decide what a change actually does. Learn that strategy before changing anything.

## Why (derivation)
Factory calibrations run most of the time in closed loop at stoichiometric, with a separate power-enrichment mode, and a narrow band sensor cannot show mixture in power enrichment. Trims react after the fact, and correct airflow scaling is the base.

## Assumptions
A reflash tool with logging; a wideband added for anything beyond light work.

## Breaks when
Patches that change the strategy (such as speed density) leave new tables empty. Heavily modified engines and alcohol fuels are better done on a dyno.

## Practical use
Identify which mode the engine is in for each sample. Use a wideband, and keep it separate from factory trims.

## Decision rules
Do not trust trims alone: narrow band sensors cannot see power enrichment, and trims lag. After applying a speed density patch, fill the new tables before running. Start with retarded timing. Keep a realistic idle speed after fitting cams: keeping stock idle with an aggressive cam is a common trap. Use the tool's full-write function when a patch needs it, not a calibration-only write.

Factory ECUs often work to torque or load targets, and pass through limits on the way: raise only what is needed and leave the protections meaningful. Keep any boost cut below the sensor's range, so the sensor can see the fault. Do not depend on a knock sensor that has been desensitised. Do not set per-cylinder fuel trim from spark plug appearance.

## Data gates
Mode status and trims logged; a wideband for any high-load work.

## Worked example
A log shows trims at +6 % at cruise and no reading at wide-open throttle. The cruise data is usable; for full load the wideband is the only evidence.

## Disputed / conflicts
None recorded.

## Citations
- practice: Practitioner training and tuning practice, distilled and cross-checked.
- vendor-documentation: ECU and tuning-tool vendor documentation.
