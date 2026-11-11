---
id: platforms/megasquirt/semantics
title: Megasquirt fuel tables
layer: L3
status: draft
confidence: low
sources: [vendor-documentation]
verified: 2026-11-10
applies_to: {fuels: [gasoline, ethanol, methanol], engines: [all]}
depends_on: []
supersedes: []
---

# Megasquirt fuel tables

From the MS2 Setting Up and TunerStudio references (`vendor-doc`), at contents level.

- Fuel VE tables 1 to 3 exist; speed-density and ITB variants of the VE table are documented.
- With a MAP-based fuel algorithm, the vertical axis of fuel table lookups is in kPa.

Further facts from the MS2 Setting Up guide (`vendor-doc`):
- Primary fuel settings are ReqFuel and the VE table; AFR table only applies with Incorporate AFR (p.45).
- An ITB mode combines alpha-n at high load with speed density at low load, for engines with poor low-rpm vacuum (p.31).
