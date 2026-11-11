---
id: principles/data/sensor-lag-and-delay
title: Sensor lag and transport delay
layer: L1
status: draft
confidence: medium
sources: [engineering-texts, practice]
verified: 2026-11-10
applies_to: {fuels: [gasoline, ethanol, methanol], engines: [all]}
depends_on: []
supersedes: []
---

# Sensor lag and transport delay

## Claim
A measurement of lambda arrives later than the events that caused it: first a transport delay through the engine and exhaust, then the sensor's own lag. Logged channels must be aligned in time before they are compared.

## Why (derivation)
An engine-control textbook models the fuel-to-sensor path as a first-order lag with a time delay, both depending on operating point. The delay is partly a cycle effect and partly gas travel time, so it is longest at low speed and low flow, shrinking at high exhaust flow. Filters in the sensor controller or ECU add further lag.

## Assumptions
A roughly constant delay near a given operating point.

## Breaks when
Rapid speed or load changes, sensor location changes, and sensors running outside their heater-ready state.

## Practical use
Estimate delay from the log, using a step in fuel or throttle. Discard samples around transients unless delay has been handled. Do not attribute a lambda excursion to the table cell that was active at the time of the reading.

## Worked example
At 1000 rpm one four-stroke cycle takes 120 ms, and the delay spans at least several events plus gas travel and sensor response. A lean spike logged at time t was caused by fuelling earlier than t by that delay.

## Disputed / conflicts
None recorded.

## Citations
- engineering-texts: Engine, combustion, charging and control engineering texts.
- practice: Practitioner training and tuning practice, distilled and cross-checked.
