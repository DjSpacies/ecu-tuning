---
id: platforms/motec/quirks
title: MoTeC quirks
layer: L3
status: draft
confidence: low
sources: [vendor-documentation]
verified: 2026-11-10
applies_to: {fuels: [gasoline, ethanol, methanol], engines: [all]}
depends_on: []
supersedes: []
---

# MoTeC quirks

- `vendor-doc`: M1 behaviour is package-specific. A table or channel in one package may not exist in another, so check the package and version first.
- No file parser exists, and this adapter has not met a real package or log.
