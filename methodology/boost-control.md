---
id: methodology/boost-control
title: Boost control tuning
layer: L2
status: draft
confidence: medium
sources: [practice, engineering-texts]
verified: 2026-11-10
applies_to: {fuels: [gasoline, ethanol, methanol], engines: [turbo, supercharged]}
depends_on: [methodology/full-load, principles/boost/compressor-and-surge, principles/control/feedback-and-pid]
supersedes: []
---

# Boost control tuning

## Claim
Prove boost control is stable with feed-forward first, bring boost up in small increments, and set an overboost protection before relying on the system.

## Why (derivation)
Extra boost raises cylinder pressure and load quickly and can pass the tuned range before a person can react. Feedback can only do well if base duty is close, and integral action needs a limit.

## Assumptions
The engine is tuned at the current boost level before raising it.

## Breaks when
A wastegate spring may set a minimum boost that is already above the tuned range.

## Practical use
Set the boost-limit protection before starting. Use open-loop duty until stable, then close the loop with small gains.

## Decision rules
Increase boost by about 20 kPa at a time; 40 kPa steps only with experience and interpolation over the skipped row. For each step, extrapolate fuel and ignition conservatively first (fuel on the rich side). Make wastegate duty changes small, starting below the target. A safety backstop past the target removes timing strongly if boost control fails.

Start at minimum (wastegate spring) boost, with a boost cut configured first. Check every boost trim table for stray values before tuning open loop, and remember those tables interpolate. Use a solenoid frequency suited to the valve. Add a backstop in the duty table above the target. Change duty in small steps. A target must be realistic for the hardware.

Choose a wastegate spring about 5 psi below the intended running boost, and expect solenoid frequency to stay within about 5 Hz of 20 Hz for most electronic boost controllers.

## Data gates
Boost repeatable run to run before tuning at that level; no solenoid saturation unaccounted for.

## Worked example
A step from 140 to 160 kPa uses a VE trend of about 3 % per 20 kPa from the proven rows. Fuel is set a little above trend before the run.

## Disputed / conflicts
Cross-check: The combustion textbook shows the dependence of knock limits on charge pressure, temperature and mixture, and a charging textbook covers control generally. Step sizes are practice figures.

## Citations
- practice: Practitioner training and tuning practice, distilled and cross-checked.
- engineering-texts: Engine, combustion, charging and control engineering texts.
