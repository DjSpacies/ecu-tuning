---
id: principles/fueling/injector-flow-and-dead-time
title: Injector flow, dead time and duty
layer: L1
status: draft
confidence: high
sources: [engineering-texts, reference-data]
verified: 2026-11-10
applies_to: {fuels: [gasoline, ethanol, methanol], engines: [all]}
depends_on: [principles/fuels/stoichiometry-and-lambda]
supersedes: []
---

# Injector flow, dead time and duty

## Claim
An injector delivers fuel at a rate set by the pressure across it, only for the part of its pulse when it is open. Getting mass right needs correct flow, differential pressure and dead time.

## Why (derivation)
Flow follows the orifice relation, proportional to the square root of differential pressure. Rail pressure alone is not the driver: if manifold pressure rises and the rail does not, delivery falls.
An injector takes time to open and close, so a commanded pulse does not all deliver fuel. Dead time (offset) is the pulse length at which delivery effectively starts. It rises as battery voltage falls and with differential pressure. Very short pulses become non-linear and need separate characterisation.
Duty is pulse width over cycle time; a four-stroke cycle takes 120000 / rpm milliseconds.

## Assumptions
Liquid, incompressible fuel flow and an injector operating in its linear region. Sequential injection once per cycle in the duty formula.

## Breaks when
Pressure or voltage outside the characterised range, very short pulses, or duty approaching 100 % where the injector cannot close before the next event. High-temperature fuel may vaporise in the rail.

## Practical use
Use `principles/calculators/injector.py`. Prefer manufacturer dead-time data at the actual voltage and pressure. If idle needs a big change and full load does not, suspect dead-time or short-pulse data before touching fuel tables.

## Worked example
1000 cc/min at 300 kPa differential, fed 40 mg per cycle of gasoline: 40 mg / 12.42 g/s = 3.22 ms, plus 0.8 ms dead time = 4.02 ms. At 6000 rpm the cycle is 20 ms, so duty is 20 %.

## Disputed / conflicts
None recorded.

## Citations
- engineering-texts: Engine, combustion, charging and control engineering texts.
- reference-data: Published reference data: thermophysical properties, fuel data, sensor and injector data sheets, statistics.
