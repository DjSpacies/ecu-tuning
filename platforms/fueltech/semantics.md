---
id: platforms/fueltech/semantics
title: FuelTech fuel tables
layer: L3
status: draft
confidence: low
sources: [vendor-documentation]
verified: 2026-11-10
applies_to: {fuels: [gasoline, ethanol, methanol], engines: [all]}
depends_on: []
supersedes: []
---

# FuelTech fuel tables

From the manuals' contents pages (`vendor-doc`), read at that level only.

- FT700: a main MAP VE (Volumetric Efficiency) table and an AFR Target map.
- FT450, FT550, FT600: a main fuel table and overall fuel trim. They are not necessarily VE; check before reading a value as VE.

Further facts from the FT700 manual (`vendor-doc`):
- The AFR Target Map holds a lambda value per RPM and MAP or TPS, at 200 rpm spacing up to 3000 rpm and 500 rpm above (p.123).
- The main MAP VE table is described as true volumetric efficiency (p.119).
