---
id: principles/combustion/knock
title: Knock and surface ignition
layer: L1
status: draft
confidence: high
sources: [engineering-texts, reference-data]
verified: 2026-11-10
applies_to: {fuels: [gasoline, ethanol, methanol], engines: [all]}
depends_on: [principles/fuels/octane-rating]
supersedes: []
---

# Knock and surface ignition

## Claim
Knock is autoignition of the unburned end gas before the flame reaches it. Its pressure waves damage engines, and anything that raises end-gas temperature, pressure or time at temperature makes it more likely.

## Why (derivation)
The end gas is compressed and heated by the piston and by the advancing flame. If its chemistry reaches ignition before the flame arrives, the remaining charge releases its energy very quickly, sending pressure waves that ring the chamber at its acoustic frequencies. Those waves erode the thermal boundary layer, so heat flux to piston and head jumps.
Surface ignition is different: a hot spot lights the mixture, independent of the spark. Pre-ignition, before the spark, adds compression work against an already burning charge, and can run away as temperatures climb.

## Assumptions
Homogeneous spark-ignition combustion.

## Breaks when
Audible or sensor-detected knock is only a proxy for chamber pressure events. Sensor signals include mechanical noise, so a low reading at high rpm does not prove the absence of knock.

## Practical use
Knock limits (more timing, more load, less margin) are checked against evidence. Factors raising risk: more spark advance, higher charge temperature, higher load, lower octane, leaner mixture towards peak heat, hotter coolant, residual gas, deposits. Treat any suspected pre-ignition as an immediate stop.

## Worked example
An engine shows knock at 0.95 lambda with 22 degrees of timing at peak torque. Hotter intake air than the previous pull is a likely contributor. The safe response is to remove timing or load in that region, not to assume the sensor is wrong.

## Disputed / conflicts
The combustion textbook records two historical explanations, autoignition and detonation theory. Modern practice treats autoignition of end gas as the origin, with possible developing detonation waves in severe events. Mixture has a peak effect: The combustion textbook places the highest octane requirement slightly rich of stoichiometric, falling on both sides. So advice that richer always helps, or that leaner always hurts, holds only for part of the range.

## Citations
- engineering-texts: Engine, combustion, charging and control engineering texts.
- reference-data: Published reference data: thermophysical properties, fuel data, sensor and injector data sheets, statistics.
