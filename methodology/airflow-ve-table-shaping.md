---
id: methodology/airflow-ve-table-shaping
title: Building and shaping the VE table
layer: L2
status: draft
confidence: medium
sources: [practice]
verified: 2026-11-11
applies_to: {fuels: [gasoline, ethanol, methanol], engines: [all]}
depends_on: [principles/airflow/volumetric-efficiency, methodology/fuel-model-load, methodology/steady-state-fuel, methodology/full-load]
supersedes: []
---

# Building and shaping the VE table

## Claim
Place breakpoints where airflow changes fastest and where the engine spends its time, not uniformly. Fill cells that cannot yet be tuned from the expected VE shape, erring rich. When a ramp run finds an error in a region that was only extrapolated, correct the whole column; when an error sits between two breakpoints that are both on target, add a breakpoint rather than bending its neighbours. Approach unverified targets from the rich side.

## Why (derivation)
### Interpolation
The ECU blends linearly between neighbouring cells, so a point between two breakpoints receives a weighted mix of both. A narrow feature in the real VE curve (cam reversion hole, runner switch, a resonance) cannot be represented by two correct neighbours; editing them to fix it spoils the region they are right for. A new breakpoint inserted with interpolated values changes nothing until it is edited. The real VE surface is smooth over most of the map: one training session demonstration replaced a full map with four corner cells and still idled normally and came within about 1 kW at full load, but went lean near the top and could not hold stoichiometric cruise, which is why about 500 rpm spacing is the practical compromise.

### Ratio correction
Delivered fuel is proportional to the table value, so the correction that lands on target in one step is new = old x (lambda_measured / lambda_target). A measured 0.83 against a target 0.88 gives 0.943, about 6 % less fuel.

### Throttle airflow is non-linear
Airflow through a butterfly rises steeply over the first few percent of opening and barely changes from about 70-80 % to fully open. A completed throttle-axis column in one course climbed from about 49 % VE at 5 % throttle to about 84 % within a few breakpoints, then plateaued (96-102 %) above about 40-50 %; in another, fuel changed only about 1.7 % between 40 and 100 % throttle. At higher rpm the same small opening passes less air per cycle, so light-throttle cells usually need VE removed as rpm rises.

### Columns share their error
Columns above the steady-state limit are copies or extrapolations of one guess, so an error measured at full load in such a column is probably present at part load in the same column too.

## Assumptions
The fuel model and injector data are set up first (`methodology/fuel-model-load`). Compensations are neutral in the tuned region (`methodology/compensations`). Lambda readings are aligned in time with the cells that produced them.

## Breaks when
- Cam-switched engines: the usual copy-and-extrapolate approach works poorly because the switch changes VE; sample a few rpm points and key loads per cam state and block-change from there.
- Ramp runs move diagonally through rpm and load, and boost builds through low rpm, so the active cell and its interpolation neighbours both contribute; a correction applied to one cell can create a spike.
- A lambda reading taken just after a heavily corrected area can still carry that area's error; recheck such regions on the next pass.
- Moving a breakpoint value in some software does not re-interpolate the cells, which silently shifts a tuned table; use the function that re-interpolates.

## Practical use
### Lay out breakpoints first
- Rpm: about every 500 rpm from 0 to a little beyond the rev limit, plus sites near idle and off-idle. Very dense factory layouts add work without benefit.
- Manifold pressure: about every 10-20 kPa, with extra rows around idle and cruise; place idle in the middle of one cell (one example added a 35 kPa row because idle sat at 34 kPa between 30 and 40), so it can be controlled without moving two rows. On an NA engine keep a row just below 100 kPa (for example 90 kPa), because full throttle often reads 93-99 kPa at altitude or with a restrictive intake; check which rows the log actually accesses before editing full-load cells.
- Extend the load axis beyond the highest expected boost, for fuel and ignition; load beyond the last breakpoint reuses the top row. Warnings about cells the engine will never reach can be ignored.
- Throttle axis: roughly exponential spacing, for example 0, 2, 4, 6, 8, 10, 15, 20, 30, 40, 50, 60, 80, 100 %, keeping resolution where the car cruises. Even 10-20 % spacing at the bottom makes idle and cruise fuelling impossible to control consistently.
- Add breakpoints either side of a known abrupt VE change (runner switch, cam changeover) and where an engine has a known local idiosyncrasy.

### Start values
- VE model: a flat 40-60 % (most sources use 50 %) starts the engine; a generator using idle MAP, redline and expected torque and power rpm gives a plausible shape when tuning on the road without a dyno.
- Give light-load rows a downward taper before running, since flat values guarantee richness where airflow falls.

### Shape the untuned regions before ramp runs
- Copy the last tuned column out to the end, then shape it toward the expected curve: VE peaking near peak-torque rpm and tapering after. Examples in the sources: a stock turbo engine expected to fall from about 6000 rpm, removing a couple of percent per column and more at 7500-8000; an NA engine anticipated to peak around 5500-6500 rpm, adding a few percent there; a high-revving NA engine given about +10 % to a peak near 105 %. Shaping rather than flat copying meant first ramp runs within 1-2 % of target in one course.
- Rising boost (one practitioner's method): copy the last tuned row upward adding about 2-5 % VE per 20 kPa, take out timing at about 2 degrees per 20 kPa, and raise boost one breakpoint (about 20 kPa or 2-3 psi) at a time. Coming into new areas rich and retarded is safer than finding them lean and knocking. Expect VE to flatten with boost (`principles/airflow/volumetric-efficiency`).
- Above the highest boost reachable on the dyno, add a little fuel rather than copying the last value: heat soak can raise boost 1-2 psi on track when the wastegate cannot keep up.
- Unreachable vacuum rows and very low rpm columns: extrapolate each column's trend, but less steeply than linear (one example applied 4 % where the linear trend suggested about 14 % over 20 kPa), staying rich. Cells near idle matter because interpolation reaches into them.

### Apply ramp-run corrections
- Rpm already tuned in steady state: correct only the full-load rows being traversed, including the neighbours the ECU interpolates from, then smooth any spike created.
- Rpm only extrapolated: apply the percentage to the whole column, all loads, and carry it to the columns above, where VE is expected to keep tapering, slightly enlarging it there. Apply it also above the boost reachable today so trends stay consistent when boost rises.
- Large errors in unknown territory: correct by less than the measured error (examples: 8 % for 11 % rich, 6 % for 10 %, 5 % for 7 %) and approach target over successive runs; overshooting lean is the worse outcome. One practitioner deliberately over-corrects small errors from experience of a specific ECU's response, and another deliberately over-corrects lean errors at the top of the rev range so as not to keep chasing the tail.
- Error between two breakpoints that are both on target (examples: 3-5 % midway between 500 rpm columns; 2 % at 3250 or 4750 rpm): insert a breakpoint at the error rpm, correct only the new column (often only its full-load rows), and restore any neighbour already bent in an earlier attempt. Small blips at rpm the engine passes quickly under little stress are not worth chasing.
- Fix fuel before touching ignition while no knock is heard, so each change is isolated.
- With boost switched between a few settings (for example spring pressure and a higher setting), tune accurately at each real level and interpolate smoothly between; intermediate rows are only passed through.
- Throttle-axis VE on a turbo engine: correct at minimum boost only, and place high-boost errors in the separate pressure-axis trim.
- Stop at about 2-3 % residual error at part load; closed loop absorbs the rest once re-enabled.

### Check the shape after each pass
- Smooth trends across columns and rows on the 3D view; a single cell or a local dip out of character with its neighbours is usually a tuning error (for example a cell tuned off-centre) and should be retested.
- Expect smooth tables on mild turbo engines; accept genuine roughness at low rpm on NA engines with aggressive cams, which smooths out higher up.
- A large VE jump between adjacent low-rpm columns is not normal; it can point to a mechanical issue or to injector short-pulse characterisation. Note it and watch whether the trend continues.
- If successive increases stop raising lambda as expected, or two rows tune nearly the same, expect the next to be similar and copy forward.

## Worked example
Ramp run at 6500 rpm in an extrapolated column: target 0.80, measured 0.76 (5 % rich). Ratio = 0.76 / 0.80 = 0.95. Applying the full 5 % to the whole 6500 rpm column and 6 % to the 7000 rpm column follows the taper; a cautious first pass would use 4 % and 5 % and rerun.
Between-breakpoint fix: lambda on target at 2000 and 2500 rpm but 3 % lean at 2250. Insert a 2250 rpm column (values are the average of neighbours, so nothing changes), then raise only its full-load cells by 3 %.

## Disputed / conflicts
- Under- versus over-correction: most training lessons undercorrect large errors to approach from rich; one practitioner deliberately removed 3 % for a 2 % rich reading from experience of one ECU, and another overshot lean corrections at high rpm to stop chasing the tail. Discriminating evidence: the residual on the following run.
- Smoothness as a quality test: see `principles/airflow/volumetric-efficiency`.
- Starting tables: a flat value is the common choice; one practitioner kept a supplied dense base map to demonstrate self-learning, noting learning can cope with a poor base VE.

## Citations
- practice: Practitioner training and tuning practice, distilled and cross-checked.
