---
id: applications/naturally-aspirated
title: Naturally aspirated profile
layer: L4
status: draft
confidence: medium
sources: [practice]
verified: 2026-11-10
applies_to: {fuels: [gasoline, ethanol, methanol], engines: [na]}
depends_on: [principles/airflow/volumetric-efficiency, methodology/full-load]
supersedes: []
---

# Naturally aspirated profile

## Claim
A naturally aspirated engine has no boost to control, so its limits are thermal and knock limits at about atmospheric pressure, and its airflow comes from VE alone.

## Why (derivation)
Load tops out near atmospheric, so a smaller range of cylinder pressure is in play. Best power usually falls in a broad lambda band, and many engines reach MBT before knock.

## Assumptions
Pump or better fuel, and a typical compression ratio.

## Breaks when
High-compression builds can become knock-limited even at atmospheric pressure.

## Practical use
Expect a 100 kPa row at full load that can dip with intake restriction, so do not copy it blindly to higher speeds. Use the MBT procedure if torque is measured.

## Worked example
At full load a target of 0.88 is inside the 0.85 to 0.92 band usually giving best power. Confirm on a dyno; the plateau is wide.

## Disputed / conflicts
None recorded.

## Citations
- practice: Practitioner training and tuning practice, distilled and cross-checked.
