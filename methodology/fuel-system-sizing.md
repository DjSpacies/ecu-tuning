---
id: methodology/fuel-system-sizing
title: Fuel system sizing
layer: L2
status: draft
confidence: medium
sources: [practice]
verified: 2026-11-10
applies_to: {fuels: [gasoline, ethanol, methanol], engines: [all]}
depends_on: [principles/fueling/injector-flow-and-dead-time, principles/fuels/energy-and-charge-cooling]
supersedes: []
---

# Fuel system sizing

## Claim
The pump, lines and injectors must be sized together with margin. An alcohol fuel changes the whole calculation.

## Why (derivation)
Injector duty sets the injector limit and pump flow against pressure sets the supply limit. With a boost-referenced regulator, pump pressure rises with boost, reducing flow.

## Assumptions
Fuel flow demand estimated from a target power and fuel type.

## Breaks when
Voltage drop to the pump reduces flow, and pump data at a different pressure misleads.

## Practical use
Check capacity before raising power or changing fuels.

## Decision rules
Rules of thumb from one practitioner: about 1 litre per minute per 200 hp on gasoline, and a pump with about 25 % more flow than the injectors need. Do not exceed the injector's rated pressure. Size injectors sensibly: very large injectors give poor control at idle unless they are linear at short pulses; consider staged injection. Measure fuel pressure, even with a fixed system.

## Data gates
Fuel pressure logged under load.

## Worked example
A 400 hp gasoline target implies about 2 L/min by the rule of thumb. E85 needs roughly half as much more again.

## Disputed / conflicts
Cross-check: no textbook value for the 25 % margin or 1 litre per minute per 200 hp. They are practice guides.

## Citations
- practice: Practitioner training and tuning practice, distilled and cross-checked.
