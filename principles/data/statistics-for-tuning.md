---
id: principles/data/statistics-for-tuning
title: Statistics for trustworthy tuning data
layer: L0
status: draft
confidence: medium
sources: [reference-data]
verified: 2026-11-10
applies_to: {fuels: [gasoline, ethanol, methanol], engines: [all]}
depends_on: []
supersedes: []
---

# Statistics for trustworthy tuning data

## Claim
A change should be justified by enough steady samples and a spread small beside the correction. A mean over a few points, or a filter over a transient, is not evidence.

## Why (derivation)
The uncertainty of a mean falls with the square root of the sample count, but only if samples are independent. Consecutive log samples are strongly correlated, so a high log rate does not create many independent measurements. The spread (standard deviation) and an outlier check show whether the data describes one condition or several.

## Assumptions
The process is steady during the samples: the data-quality gates in the methodology decide that.

## Breaks when
Non-stationary conditions, such as warming intake temperature. A median is more robust than a mean where sensor spikes exist.

## Practical use
Report sample counts and spread with each cell. Prefer medians for lambda error. Treat small corrections relative to spread as no change.

## Worked example
A cell has 40 samples, median lambda error 1.0 %, standard deviation 3 %. The correction is smaller than the spread: more steady data is needed before changing it.

## Disputed / conflicts
None recorded.

## Citations
- reference-data: Published reference data: thermophysical properties, fuel data, sensor and injector data sheets, statistics.
