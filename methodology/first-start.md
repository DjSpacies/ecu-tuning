---
id: methodology/first-start
title: First start
layer: L2
status: draft
confidence: medium
sources: [practice]
verified: 2026-11-10
applies_to: {fuels: [gasoline, ethanol, methanol], engines: [all]}
depends_on: [methodology/base-setup]
supersedes: []
---

# First start

## Claim
The first start is about getting a safe, stable running engine, not accuracy: fuel is adjusted coarsely with a conservative ignition value, and the engine's vital signs are watched.

## Why (derivation)
A blank map rarely starts first time. A locked conservative timing keeps knock out of the picture while mixture is corrected.

## Assumptions
Oil, coolant and fuel systems are filled, and leaks are checked.

## Breaks when
Very high compression or special fuels may need a different locked timing.

## Practical use
Stay near idle-to-light-throttle until mixture is close. Any abnormal vital sign ends the session.

## Decision rules
Hold 1000 to 1500 rpm by hand until idle is tuned. Aim for lambda about 0.85 to 0.95 at this stage, and scale the whole fuel table if the engine will not fire. Stop for no oil pressure, coolant or fuel leaks, or a charging fault.

## Data gates
Oil pressure present and battery voltage around 13.8 to 14.2 V while running; wideband warmed up before its reading is used.

## Worked example
The engine fires then dies, and lambda reads 1.2. Fuel is far too lean: add a uniform percentage to the whole table, not a local cell.

## Disputed / conflicts
None recorded.

## Citations
- practice: Practitioner training and tuning practice, distilled and cross-checked.
