---
id: methodology/histogram-analysis
title: Confirming a tune with histograms
layer: L2
status: draft
confidence: medium
sources: [practice, reference-data]
verified: 2026-11-10
applies_to: {fuels: [gasoline, ethanol, methanol], engines: [all]}
depends_on: [methodology/data-quality]
supersedes: []
---

# Confirming a tune with histograms

## Claim
Histograms of logged lambda by cell show where a tune holds up in real driving and where samples are too few to judge. They are for confirmation and small corrections, not initial tuning.

## Why (derivation)
Aggregating many passes through a cell averages out transient noise and gives a picture of where the tune is used.

## Assumptions
Bins match the fuel table's axes.

## Breaks when
Mismatched bins interpolate into the wrong cells. Overrun cells look lean.

## Practical use
Use only cells with enough hits; exclude overrun and transient samples.

## Decision rules
Match histogram bins to table breakpoints. Treat high-rpm low-load cells as probable overrun. Make partial corrections rather than full ones (half is a common choice), and repeat.

## Data gates
Cell hit count reported.

## Worked example
A cell with 1100 hits at 1800 rpm and 70 kPa is reliable. A cell with 12 hits at 6500 rpm and 35 kPa is probably overrun.

## Disputed / conflicts
None recorded.

## Citations
- practice: Practitioner training and tuning practice, distilled and cross-checked.
- reference-data: Published reference data: thermophysical properties, fuel data, sensor and injector data sheets, statistics.
