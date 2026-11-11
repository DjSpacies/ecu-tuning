---
id: applications/turbocharged
title: Turbocharged profile
layer: L4
status: draft
confidence: medium
sources: [practice, engineering-texts]
verified: 2026-11-10
applies_to: {fuels: [gasoline, ethanol, methanol], engines: [turbo]}
depends_on: [principles/boost/compressor-and-surge, principles/boost/exhaust-back-pressure, methodology/boost-control]
supersedes: []
---

# Turbocharged profile

## Claim
A turbocharged engine runs knock-limited over much of its boosted range, and its fuelling and timing must be proven in small boost steps, with a declared boost ceiling and protection.

## Why (derivation)
Boost multiplies air and cylinder pressure. Back pressure, charge temperature and turbine response tie boost to speed and history. An overboost can take the engine out of its tuned range in moments.

## Assumptions
Boost control is stable and a limit is configured.

## Breaks when
A very high minimum boost changes which cells can be reached in steady state. Heat soak changes the limit during a pull.

## Practical use
Tune in steady state to about 200 kPa where possible, then use ramp runs, and step boost by about 20 kPa. Past the target, make timing fall sharply so a boost failure is less harmful.

## Worked example
At 170 kPa target, cells at 180 to 200 kPa carry several degrees less timing than the 170 row as a backstop.

## Disputed / conflicts
None recorded.

## Citations
- practice: Practitioner training and tuning practice, distilled and cross-checked.
- engineering-texts: Engine, combustion, charging and control engineering texts.
