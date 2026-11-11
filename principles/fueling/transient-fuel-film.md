---
id: principles/fueling/transient-fuel-film
title: Transient fuelling and wall film
layer: L1
status: draft
confidence: medium
sources: [engineering-texts, practice]
verified: 2026-11-10
applies_to: {fuels: [gasoline, ethanol, methanol], engines: [all]}
depends_on: [principles/fueling/injector-flow-and-dead-time]
supersedes: []
---

# Transient fuelling and wall film

## Claim
During a throttle change the fuel reaching the cylinder lags the fuel injected, because part of it joins or leaves a film on the port walls. Transient compensation exists to cover that difference, and the MAP/air estimate lag.

## Why (derivation)
A common model splits injected fuel: a fraction X lands on the wall, the rest goes straight in. The film then evaporates with a time constant tau. Rising load (rising pressure, falling evaporation) makes the film grow, so the cylinder runs lean unless more fuel is added. Falling load drives the film off, which runs rich.
X and tau depend on wall temperature, speed, load and fuel. Alcohols and a cold engine make them larger.

## Assumptions
Port injection. Parameters are valid only near where they were measured.

## Breaks when
Direct injection has different wall behaviour. A lean spike after a tip-in may instead come from sensor lag or from an airflow estimate that is behind.

## Practical use
Confirm steady-state fuelling first. Then use transient logs aligned for sensor delay. Fix enrichment shape by amount and decay, and check cold and warm separately.

## Worked example
At 40 C coolant the film is much larger than at 90 C, so the same throttle stab needs more enrichment and a longer decay; a table tuned warm will run lean cold.

## Disputed / conflicts
None recorded.

## Citations
- engineering-texts: Engine, combustion, charging and control engineering texts.
- practice: Practitioner training and tuning practice, distilled and cross-checked.
