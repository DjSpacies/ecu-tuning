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

Native tune and log file formats are not documented in the vendor material on hand, and no sample files were available.
`parser/adapter.py` reads a CSV with a header row, with column names taken from `channels.yaml`. Those names are placeholders that must be confirmed against a real export; nothing here has been tested on one. It cannot read tune files.
