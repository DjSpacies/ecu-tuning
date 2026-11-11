---
id: methodology/histogram-analysis
title: Confirming a tune with histograms
layer: L2
status: draft
confidence: high
sources: [practice, reference-data]
verified: 2026-11-11
applies_to: {fuels: [gasoline, ethanol, methanol], engines: [all]}
depends_on: [methodology/data-quality, principles/data/statistics-for-tuning]
supersedes: []
---

# Confirming a tune with histograms

## Claim
A histogram of logged error binned on the table's own axes shows, cell by cell, what the table needs and how much evidence there is for it. It is the right tool for long road or track logs that revisit each cell many times; a time graph is the right tool for a single ramp run. Histograms refine and confirm a tune; they do not create one from nothing, and their output is trusted only where counts are high, filters were applied and neighbouring cells agree.

## Why (derivation)
A fuel or ignition table is addressed by rpm and load, so the error must be aggregated by the same addressing to show what each cell needs. A long drive passes through the same cell dozens or hundreds of times, scattered through the file; a time graph cannot show the per-cell trend, while a histogram averages every visit. A ramp run passes each rpm once along a narrow path, so a time graph (or a histogram that shows the path) is enough there.

The value binned is a percentage error: measured lambda divided by target lambda, minus one, times 100. Positive means lean (add fuel), negative rich. For factory ECUs running closed loop, the sum of short- and long-term fuel trims is the equivalent error; in open loop, use wideband error against the commanded value. The approach comes from factory-ECU reflash work, where airflow-meter and VE tables are calibrated from histograms because changes cannot be made live.

## Assumptions
Bins match the fuel table's axes and breakpoints exactly. Samples have passed the gates in methodology/data-quality. The target table and any commanded value in the log still mean what the analyst thinks.

## Breaks when
- Mismatched bins interpolate into the wrong cells. Some tools also invert the load axis orientation relative to the ECU, or round axis values to odd breakpoints when precision is set wrongly.
- Overrun cells look lean.
- Cells at a closed-loop to power-enrichment switch log false lean error from lag.
- The commanded table was deliberately skewed to correct an earlier error: the logged commanded value is then no longer the wanted lambda, and the logged error keeps showing the old offset. Judge against the real desired value.
- The ECU switches between several tables (by cam position, cam mode or fuel) and samples from all of them are mixed into one histogram.
- The table axis is a calculated quantity (pressure ratio, airflow per cylinder) that does not follow rpm and MAP in a simple way; one demonstration with a pressure-ratio axis showed a ramp at fixed boost tracing a curved path through the table.

## Practical use
Use only cells with enough hits; exclude overrun and transient samples. Look at the count view beside the average view every time.

### Building the histogram
- Copy the table's breakpoints into the histogram axes rather than retyping them; tools that allow it paste the axis labels directly. Where results cannot be pasted back automatically, still align breakpoints so each value can be read against its cell.
- Use the same load source as the table (MAP for speed density, throttle for alpha-N, airflow-meter frequency or voltage for meter calibration, air mass per cylinder for mass-based tables).
- For multi-table strategies, build one histogram per table and filter each to the condition that selects that table (for example a band of logged cam position around each table's cam value). The sources found a band of about 10 degrees worked in practice even though it is exact only at the band centre.
- Make separate histograms for closed-loop data (trim-based error) and open-loop data (wideband error).

### Reading it
- **Counts.** Low-count cells are a flash in the pan. Treat single-digit counts as unreliable and a few dozen as weak; see principles/data/statistics-for-tuning for the spread of thresholds in the sources.
- **Trends.** A smooth trend across high-count neighbours is believable. An isolated cell that disagrees with consistent neighbours, or neighbours that alternate sign, is suspect unless the same pattern repeats in the adjacent column. Revisit it.
- **Edges and straddles.** A cell crossed briefly or sampled at the boundary with the next breakpoint can carry the neighbour's error. When the ECU was interpolating between two rows (for example the atmospheric row and the one below at full throttle), apply the correction to both.
- **Overrun signature.** High rpm with very low MAP and a big lean error is lift-off overrun, not a fuelling fault.
- **Sizes worth acting on.** Errors around 1 % are within run-to-run variation and not worth chasing.

### Applying it
- Make partial corrections rather than full ones (half is a common choice), and repeat. The sources typically iterate two or three times with manual touch-ups.
- Automatic paste of every cell is safe only when counts are high and the error surface is smooth. Otherwise blend by hand: apply well-supported cells, then extend the trend into unvisited neighbours, which may still be used on the road. One demonstration extrapolated a column running from 3 % to 6 % to about 2.5 % above and 6 % below it, reasoning that an estimate is closer than leaving the old error.
- Before copying values, make sure the view is set to the average, not the count: pasting counts ruins a table.
- After applying, check the table shape in a 3D or colour view for steps, spikes or holes the correction introduced.
- In a target-AFR table (rather than a fuel-quantity table) removing fuel means raising the number, so the correction direction is inverted.

### Diagnostic tests
- **Airflow-meter scaling versus a compensation table.** On factory ECUs, error that is consistent across rpm at a given meter reading belongs in the meter scaling. Error that appears only in one rpm band (one example: 6 to 10 % in a band around 2500 to 3000 rpm, small elsewhere, caused by fuel pressure pulsation) belongs in the rpm-based compensation table; changing the meter scaling would spoil other rpm ranges. Bin error by meter reading and rpm to tell them apart.
- **VE error versus transition artefact.** Error concentrated in the cells where the target steps from closed loop to power enrichment is lag. Calibrate in two passes: steady data below the enrichment threshold, then full-enrichment pulls above it, and disregard the transition cells.
- **Ramp path versus whole table.** A pull touches only a band of the table. Use a histogram of the path (cells hit, with counts) to edit only those cells and their interpolation neighbours, and do not read the rest of the table as confirmed.

## Decision rules
Match histogram bins to table breakpoints. Treat high-rpm low-load cells as probable overrun. Make partial corrections rather than full ones (half is a common choice), and repeat. Do not act on a low-count cell with a large error; collect more data there first. Check counts before auto-applying, and never auto-apply across isolated outliers.

## Data gates
Cell hit count reported, alongside the median error and spread. Rejection counts from methodology/data-quality reported first.

## Worked example
A cell with 1100 hits at 1800 rpm and 70 kPa is reliable. A cell with 12 hits at 6500 rpm and 35 kPa is probably overrun.

A road-log histogram shows a smooth trend from about 4 % lean near closed throttle to 2.5 % rich at 70 kPa in one rpm column, with several hundred hits per cell, except one cell slightly lean between two cells at 3 % rich. Half of the trend is applied to the well-sampled cells, the odd cell is left and revisited on the next drive, and unvisited cells at the top of the column are given the extrapolated trend.

## Disputed / conflicts
- **Automatic application.** Some correction tools are designed to apply every cell; several practitioners prefer to apply only selected cells and hand-blend the rest, and one notes that auto-applying from a ramp run changes only the cells crossed while a proper correction also adjusts interpolation neighbours. The automatic route is more useful with large, varied road logs where manual analysis is impractical.
- **Thresholds for trust** vary widely between sources; see principles/data/statistics-for-tuning.
- **Large error in a power-enrichment table.** One practitioner corrects small full-load errors (within about 2 to 3 %) directly in the commanded table, and fixes larger ones in the airflow scaling instead, so the commanded value stays meaningful.

## Citations
- practice: Practitioner training and tuning practice, distilled and cross-checked.
- reference-data: Published reference data: thermophysical properties, fuel data, sensor and injector data sheets, statistics.
