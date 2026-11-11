---
id: principles/data/statistics-for-tuning
title: Statistics for trustworthy tuning data
layer: L0
status: draft
confidence: medium
sources: [reference-data, practice]
verified: 2026-11-11
applies_to: {fuels: [gasoline, ethanol, methanol], engines: [all]}
depends_on: []
supersedes: []
---

# Statistics for trustworthy tuning data

## Claim
A change should be justified by enough steady samples, a spread small beside the correction, and agreement with neighbouring cells or a repeat run. A mean over a few points, a single momentary excursion, or a filter over a transient is not evidence. Run-to-run variation sets a floor below which a correction is noise.

## Why (derivation)
The uncertainty of a mean falls with the square root of the sample count, but only if samples are independent. Consecutive log samples are strongly correlated, so a high log rate does not create many independent measurements: a few seconds spent in a cell at 50 Hz is still one visit. The spread (standard deviation) and an outlier check show whether the data describes one condition or several.

Lambda at a fixed rpm and load is not one fixed number. Practitioners in the sources consistently report that repeated pulls through the same gear and rev range differ by about 0.01 to 0.02 lambda, or about 1 to 2 %, from run to run, and that small fluctuations of around 1 % at high rpm are noise. A correction of that size cannot be separated from the variation with one run.

The engine's fuel requirement changes smoothly across rpm and load on most engines (VE changes gradually), so a real error also tends to vary smoothly between neighbouring cells. A value that breaks the trend of its neighbours is more likely to be a data problem than a real feature: too few samples, a transient pass, or a sample taken at the edge of a cell where the ECU was interpolating with the next one.

## Assumptions
The process is steady during the samples: the data-quality gates in the methodology decide that. Sharp real features exist only where the hardware explains them (cam switching, variable runners, resonance), and are checked against that explanation.

## Breaks when
- Non-stationary conditions, such as warming intake temperature, heat soak, or fuel temperature rising over a stint. A slow drift adds spread that more samples will not remove.
- Sensor spikes: a median is more robust than a mean.
- Filtering and smoothing: these lower apparent spread but also remove real detail and shift peaks in time. Heavy smoothing gives a trace that looks clean and is wrong; one source used an extreme filter on a very noisy pressure channel and stressed that the filter must be flagged so it is not forgotten.
- Sample counts from a high-rate log overstate independence (see above).

## Practical use
- Report sample counts and spread with each cell. Prefer medians for lambda error. Treat corrections smaller than the run-to-run variation (about 1 to 2 % in the sources) as no change.
- **Repeat before changing.** A small error seen once is a hypothesis. Repeat the run; change only what repeats. When a correction is made, a partial step (for example two thirds of the error) followed by a repeat shows whether the result is repeatable.
- **Average repeated runs before comparing.** To judge a small gain or loss, the sources make two or three runs with no change and average them, then compare against the averaged runs after the change.
- **Check unchanged regions first.** On a second run, look first at regions that were not edited. If they moved, the run differs and the edited regions cannot be judged from it.
- **Neighbour test.** A cell is suspect when it disagrees with neighbours that agree with each other, when neighbours alternate in sign, or when one cell sits several percent from a smooth surrounding trend. Treat it as missing data and re-collect, unless the same pattern repeats in the next column or row.
- **Noise near the point of interest matters most.** On a sweep, a blip far from the optimum can be ignored; noise around the optimum invalidates the result and calls for a rerun.

### Diagnostic tests
- **Real error versus scatter:** compare the median error in a cell with its spread and with the run-to-run variation from repeated runs. Act only when the median clearly exceeds both.
- **Real feature versus outlier:** compare a cell with its neighbours on both axes. A deviation that is isolated, has a low count, or flips sign between neighbours is an outlier; a deviation that is smooth and repeated across a row or column is real.
- **Drift versus scatter:** split a long log by time. If the error moves steadily from the first part to the last, something is changing (temperature, fuel pressure, baro), and averaging the whole log hides it.

## Worked example
A cell has 40 samples, median lambda error 1.0 %, standard deviation 3 %. The correction is smaller than the spread and within run-to-run variation: more steady data is needed before changing it.

A road log histogram shows a column of cells at +3, +4, +2.8 and +4 %, each with several hundred samples. The 2.8 % cell has a lower count because the operating point drifted into the next rpm column while passing through. The trend says about +3.5 % for the whole group; the low cell is treated as under-sampled, not as a real dip.

## Disputed / conflicts
- **How many samples a cell needs.** The sources give very different minimums: about 20 to 30 hits in one practitioner's dyno work; about 200 in two others; a few hundred described as reasonably accurate; 500 to 1000 described as solid for an automatic correction tool; and roughly 5000 suggested for cruise cells in a factory-ECU airflow calibration. All agree that single-digit counts are not trustworthy and that a few dozen is weak. The differences follow from rate, steadiness and correlation: a held dyno cell at a high rate collects many correlated samples quickly, while a road log passes through a cell many separate times. Discriminating test: split the samples in a cell into halves by time and see whether the two halves agree.
- **What run-to-run variation is acceptable.** Most sources accept about 1 to 2 %; one practitioner accepted up to about 3 % outliers on a throttle-body-injected system and argued such systems are inherently less repeatable.

## Citations
- reference-data: Published reference data: thermophysical properties, fuel data, sensor and injector data sheets, statistics.
- practice: Practitioner training and tuning practice, distilled and cross-checked.
