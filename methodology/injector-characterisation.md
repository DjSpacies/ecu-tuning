---
id: methodology/injector-characterisation
title: Injector data before fuel tuning
layer: L2
status: draft
confidence: medium
sources: [practice, reference-data]
verified: 2026-11-10
applies_to: {fuels: [gasoline, ethanol, methanol], engines: [all]}
depends_on: [principles/fueling/injector-flow-and-dead-time]
supersedes: []
---

# Injector data before fuel tuning

## Claim
Accurate injector data (flow, dead time against voltage and pressure, short-pulse behaviour) goes in before the fuel table is tuned. Otherwise the fuel table quietly compensates for injector errors.

## Why (derivation)
Dead-time error matters most at the shortest pulses. If it is absorbed by the fuel table, then changing fuel pressure, voltage or load later gives errors with no obvious cause. A correct model also makes the VE table look like a real engine's VE.

## Assumptions
Manufacturer data is available for this injector. Check before buying one.

## Breaks when
Data measured at another pressure. A non-referenced fuel system changes differential pressure with manifold pressure.

## Practical use
Enter complete data first. If VE trends look strange or fuel drifts with voltage, return here before changing the fuel table.

## Decision rules
Use data at the actual differential pressure and voltage. Do not accept a figure with no stated pressure. Where a returnless or unreferenced fuel system is in use, make sure differential pressure is used for flow.

Dead-time error shows most at idle. Injectors can be rated in volume or mass, so check, and check the rated pressure. Raising fuel pressure is useful only for a modest gain, about 10 to 15 % of flow. Bench data apply at the pressure and voltage they were measured at. When the ECU's dead-time table has only a voltage axis, choose the data for the differential pressure the engine sees at idle, since that is where an error shows most. An engine can be tuned with dead time set to zero: the fuel table then absorbs the error at the voltage it was tuned at, but the mixture moves with battery voltage and the fuel table no longer reflects the engine alone. Sweeping charging voltage at idle and adjusting dead time until the mixture holds steady gives a table that keeps idle stable, but its absolute values are not true dead times. On reflash platforms, latency is often trimmed until the summed fuel trims approach zero, with the same limitation. Do not leave ethanol sitting in a stored fuel system: one practitioner drains E85 and runs gasoline if the car will sit more than about a week.

## Data gates
Fuel pressure and battery voltage logged, if at all possible.

## Worked example
At 14 V an injector shows 925 microseconds of dead time. Entering 700 microseconds makes idle lean, and the tuner then adds fuel in the idle cells, which creates an error elsewhere.

## Disputed / conflicts
Cross-check: the square-root pressure rule follows from orifice flow; 10 to 15 % more flow means about 20 to 32 % more differential pressure.

## Citations
- practice: Practitioner training and tuning practice, distilled and cross-checked.
- reference-data: Published reference data: thermophysical properties, fuel data, sensor and injector data sheets, statistics.
