---
id: platforms/ecumaster/semantics
title: ECUMaster fuel tables
layer: L3
status: draft
confidence: low
sources: [vendor-documentation]
verified: 2026-11-10
applies_to: {fuels: [gasoline, ethanol, methanol], engines: [all]}
depends_on: []
supersedes: []
---

# ECUMaster fuel tables

From the EMU manual's contents and specification table (`vendor-doc`), read at that level only.

- Fuel table: 16 by 16, in 0.1 % VE steps. Two VE tables exist ("VE table 1 and 2").

Further facts from the EMU manual (`vendor-doc`):
- The VE table is the volumetric effectiveness in the fuel calculation, combined with MAP and an air density percentage relative to 21 C (p.55).
- Software categories cover fuel, ignition, knock sensor, idle, boost, nitrous and logging (p.18).
