---
id: platforms/haltech/formats
title: Haltech file formats
layer: L3
status: draft
confidence: low
sources: [vendor-documentation]
verified: 2026-11-10
applies_to: {fuels: [gasoline, ethanol, methanol], engines: [all]}
depends_on: []
supersedes: []
---

# Haltech file formats

`parser/adapter.py` reads a CSV with a header row, with column names taken from `channels.yaml`. Confirm those names against your export. Tune files are not read.
