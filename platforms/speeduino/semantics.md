---
id: platforms/speeduino/semantics
title: How Speeduino fuel tables behave
layer: L3
status: draft
confidence: low
sources: [vendor-documentation]
verified: 2026-11-10
applies_to: {fuels: [gasoline, ethanol, methanol], engines: [all]}
depends_on: []
supersedes: []
---

# How Speeduino fuel tables behave

From the project wiki (`vendor-doc`).

- The VE table's load axis follows the fuelling algorithm: Speed Density (MAP in kPa) or Alpha-N (throttle position).
- Values are a percentage of the Required Fuel amount at each speed and load point, so they are not always pure VE.
- An option multiplies the VE value by a MAP ratio, which flattens the table. Check it before reading a value as VE.
- A separate AFR table holds air-fuel targets. Speeduino works in AFR, so convert to lambda using the actual fuel.

Further facts from the wiki (`vendor-doc`):
- Knock input needs an external amplifier. Open plus closed loop is recommended for new idle installations. Oil pressure protection sets a curve under which the rpm limit applies.
