---
id: principles/boost/intercooling
title: Intercooling
layer: L1
status: draft
confidence: high
sources: [engineering-texts]
verified: 2026-11-10
applies_to: {fuels: [gasoline, ethanol, methanol], engines: [turbo, supercharged]}
depends_on: [principles/boost/compressor-and-surge]
supersedes: []
---

# Intercooling

## Claim
Cooling the charge after compression raises density and knock margin. An intercooler's work is summarised by its effectiveness, and it costs some pressure.

## Why (derivation)
Effectiveness is the fraction of the possible temperature drop achieved: (T_hot_in - T_hot_out) / (T_hot_in - T_coolant_in). Lower charge temperature means more mass per unit of boost, and less end-gas temperature for knock.

## Assumptions
Coolant (air or water) temperature is known. Steady operation.

## Breaks when
Heat soak in a stationary car or on a low-airflow dyno: effectiveness measured there does not hold on the road. Water-to-air systems saturate on long pulls.

## Practical use
Log charge temperature during pulls. A climbing temperature over a pull means knock margin is shrinking, so treat the last part of a pull as the limiting case.

## Worked example
Charge enters at 400 K, cooling air 300 K, and leaves at 330 K. Effectiveness is 0.7.

## Disputed / conflicts
None recorded.

## Citations
- engineering-texts: Engine, combustion, charging and control engineering texts.
