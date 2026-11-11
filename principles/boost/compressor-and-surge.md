---
id: principles/boost/compressor-and-surge
title: Boost, pressure ratio and compressor limits
layer: L1
status: draft
confidence: high
sources: [engineering-texts]
verified: 2026-11-10
applies_to: {fuels: [gasoline, ethanol, methanol], engines: [turbo, supercharged]}
depends_on: [principles/thermo/air-density]
supersedes: []
---

# Boost, pressure ratio and compressor limits

## Claim
A compressor's operating point is a pressure ratio and a flow. It must stay between surge and choke, and compressing air heats it by an amount set by the ratio and the compressor's efficiency.

## Why (derivation)
Pressure ratio is absolute outlet pressure over absolute inlet pressure, so the same boost gauge reading is a higher ratio at altitude or with a restricted inlet.
Ideal compression raises temperature by T1 x (PR^((gamma-1)/gamma) - 1); real compressors divide that rise by their isentropic efficiency.
Surge is unstable flow at low flow and high ratio. Choke is the flow limit at the compressor's narrowest passage. Compressor maps use flows corrected to a reference inlet state so maps from different conditions agree.

## Assumptions
Steady flow. Map accuracy, especially near surge, where the line is built from test data.

## Breaks when
Transient flow reversal when the throttle snaps shut. Maps are measured on a test bench with steady flow, and real installations pulse.

## Practical use
Use `principles/calculators/boost.py`. Judge a boost target on pressure ratio, flow and outlet temperature, not on the boost number. Tests that may surge or overspeed are stopped, not explored.

## Worked example
Target 200 kPa absolute, baro 100, inlet losses 5, charge side losses 10: PR = 210 / 95 = 2.21. With 300 K inlet and 70 % efficiency, outlet temperature is about 409 K before intercooling.

## Disputed / conflicts
None recorded.

## Citations
- engineering-texts: Engine, combustion, charging and control engineering texts.
