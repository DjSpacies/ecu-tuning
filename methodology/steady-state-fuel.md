---
id: methodology/steady-state-fuel
title: Steady-state fuel tuning
layer: L2
status: draft
confidence: high
sources: [practice, engineering-texts]
verified: 2026-11-11
applies_to: {fuels: [gasoline, ethanol, methanol], engines: [all]}
depends_on: [methodology/idle, principles/airflow/volumetric-efficiency, methodology/closed-loop-fuel, methodology/wideband-sensors]
supersedes: []
---

# Steady-state fuel tuning

## Claim
Tune fuel cell by cell under stable, warm conditions with the operating point centred in each cell. Start at low rpm and load and work upward, correcting towards a lambda target table that has already been set. Do this before ignition. Correct by the ratio of measured to target lambda. Pre-load each untuned cell from the trend of the cells already done, erring rich, so the engine never discovers a lean cell under load.

## Why (derivation)
- **Mixture first.** Mixture is the base for torque and knock behaviour, and combustion is more sensitive to mixture error than to a small ignition error. The mixture is also fixed once the intake valve closes, well before the spark. Timing does not change the delivered air-fuel ratio, so fuel and ignition can be tuned as separate passes.
- **Ratio correction.** In a VE or pulse-width model, delivered fuel scales linearly with the cell value, as long as injector flow and dead time are characterised correctly. Measured lambda is proportional to air divided by fuel. So new value = old value x (measured lambda / target lambda), and a correctly characterised system lands in one step. In lambda units, a small difference reads directly as a percentage: 0.95 measured against 1.00 wanted is about 5 %. That is one reason to tune in lambda rather than AFR. The ratio also holds across fuels without converting stoichiometric values.
- **Interpolation.** Off the cell centre, the ECU blends the surrounding cells. The measured error then belongs partly to neighbours, and an edit to one cell only partly moves the mixture. The effect is largest early on, when tuned cells sit next to a flat untuned base (for example 65 % beside 50 %, or 105 % beside 50 %). Even 50 rpm off-centre on closely spaced breakpoints shows up in the reading.
- **VE trends make guessing ahead work** (principles/airflow/volumetric-efficiency):
  - VE rises with load;
  - at low and mid rpm, VE rises with rpm toward peak torque, then falls;
  - neighbouring columns share a similar shape, so an error at one point in a new column is usually present through the whole column.
- **Risk is asymmetric.** At very light load and low rpm a lean mixture cannot do damage, because cylinder pressure and heat are low. That is why mapping starts there. At high load and boost a lean cell must be left immediately. Starting rich and leaning out is the safe direction.

## Assumptions
- Correct injector data, fuel pressure and fuel model, so corrections represent airflow error alone (methodology/fuel-model-load).
- A valid, warm wideband with a known offset (methodology/wideband-sensors), and a lambda target table that is already filled in, because every correction is a ratio to it.
- A load-bearing dyno that can hold rpm, or road conditions that let the engine dwell in a cell. An inertia dyno cannot do steady state.
- Coolant at operating temperature, intake air not heat soaked, and no warm-up or post-start enrichment active. Any compensation still applied gets baked into the base table as error.

## Breaks when
- **Off cell centre:** the change smears into neighbours, or an untuned neighbour drags the reading. The tuner may then mis-tune the current cell to compensate.
- **Unreachable cells.** A dyno cannot hold the lightest loads, because the engine must make torque to turn the rollers, and on overrun the engine simply slows. Some boosted rows may also be out of reach. Their values are estimates. The road, with vehicle inertia, can reach lower loads.
- **NA WOT that does not reach the 100 kPa row,** because baro is below 100 kPa and the intake loses pressure. At WOT the engine then interpolates between the top two load rows, and the trace slides diagonally across the table as rpm rises. One source saw only about 90 kPa at 6000 rpm at altitude on a cold day.
- **Temperatures climbing at high load,** which makes the tune unrepresentative.
- **Transients during data collection:** throttle stabs, gear changes, or a sample count too small to trust.
- **Steady-state results differ from sweeps.** In most ECUs a ramp run reads slightly leaner than the steady-state result for the same cell, because the port fuel film behaves differently while rpm sweeps.
- **Very aggressive NA cams** produce a genuinely peaky low-rpm VE table that follows the torque curve. Smoothing it would remove real features.
- **Closed loop or learning active and ignored,** so lambda sits on target over a wrong table (methodology/closed-loop-fuel).

## Practical use

### Before starting
- Fill the lambda target table with the intended mixtures first.
- Warm the engine fully. One source warms to about 140 to 160 F coolant before using lambda or trim to edit the main table, and another tuned at about 80 C coolant with about 16 C intake air. Clear heat soak by running with airflow for a few minutes.
- Fix injector dead time at idle first. Small idle trims after that suggest the injector data can be trusted further up.
- Hold one gear on the dyno. Use a lower gear (2nd or 1st) to reach lighter loads, and a taller gear for high load to avoid wheelspin. With an automatic, lock the gear and watch converter slip.
- Keep audio knock monitoring on throughout.
- Make the ECU's load axis and breakpoints match the data being used. Add a breakpoint where idle or WOT MAP falls between sites, for example a column at 900 rpm idle or at -70 kPa idle load. Inserting a breakpoint that the ECU fills by interpolation changes nothing by itself.

### Correcting a cell
- Centre the operating point using the dyno speed set point and the throttle. Wait for lambda to settle, and average the fluctuating reading by eye or statistically.
- Multiply the cell by measured/target. Examples from the sources:
  - 0.79/0.82 = 0.96;
  - 1.12/1.00 took VE from 60.5 to 67.8 and landed on target;
  - 0.74/0.95 is about 0.8.
- When far off, a large block or row change gets lambda onto the scale first. One source added 6 and then set the whole area to 55 %; another set a whole first column to one broad guess. Then refine cell by cell. When close, use 1 % steps or finer.
- If the table is in AFR-target units rather than fuel units, the direction is inverted: 112 % on the target removes 12 % fuel.
- **One-key auto-correct.** These functions compute the same ratio. They often need a second press, can overshoot (one example went from -6 % to +1 to +2 %), and give poor results if the engine sits between cells or temperatures are abnormal. Correction per press may be capped (30 % on one ECU).
- **With closed loop active.** The trim is the error. Multiply the cell by the closed-loop factor (for example 1.16 for a trim of +16 %) until trim reads near zero, and remember to combine trim with any remaining lambda error (methodology/closed-loop-fuel).
- **After a large change,** torque and rpm move and the engine may drift into a different cell. Re-centre and re-check.
- **Done** when lambda sits within about ±0.01 lambda, or about 1 % of target, at idle and cruise. Lambda never sits still, so a band is the target, not a point.

### Tuning ahead and column-wide corrections
- **Up a column.** Before entering the next load cell, copy the tuned value into it, plus the trend seen so far. Trends in the sources:
  - +2 % per site;
  - about 3 % VE per 10 kPa at 1500 rpm on one turbo engine;
  - 5 % per 10 kPa on one NA engine;
  - in time units, 2.56 then 2.79 ms suggesting about 3.0 ms next.
  An untuned cell holding a lower value than the cell below it guarantees a lean step. One source read 1.13 lambda moving from a tuned 77 % into an untuned 70 %.
- **When error grows with load** (for example from -3 % to -25 %), pre-apply the latest correction to the untuned cells ahead. This matters most when the trend is lean.
- **Next rpm column.** Copy the finished column across and add a guessed rise:
  - 3 to 5 % per 500 rpm below peak torque is typical in the sources;
  - about 4 % per 250 rpm at low rpm in one case;
  - about 10 % in one low-rpm turbo case.
  Then check one representative cell, mid-load or 0 kPa. If it is off, apply that error to the whole column first, then refine individual cells. Learn from each overshoot or undershoot: several sources started at +5 % and cut to +3 or +4 % after it proved too much. When the trend flattens, copy with no addition. Copy the working column one column further ahead too, so that interpolation into it stays small.
- **Lowest reachable cell.** When it is off, correct it together with all lighter-load cells below it.
- **New boosted row.** When a newly reached boosted row is lean (about 6 % in one example), apply the correction to that row and above, then interpolate vertically back to the known-good row.
- **Trends are not exact.** Pre-adding 10 % before one throttle row made it 5 % rich in one source. Always verify after guessing.

### Cells the dyno cannot reach
- **Light load.** Extrapolate downward at a gentler slope than the steepest one observed, erring rich. Examples: 6 % per 10 kPa where 10 % was seen; 4 % per row where about 6 % was suggested. Scale for uneven breakpoint spacing.
- **Anchor on idle.** Interpolate between the lowest tuned row and the known idle values.
- **Road check.** These cells are used when barely on the throttle approaching a stop or rolling down a gentle slope. Lean errors there feel like hesitation. Confirm them on the road with left-foot braking or logs.
- **Unreachable boost.** Extend the observed slope above the highest reached load. If the engine is interpolating into an unreachable boosted row from a correctly tuned row below, any error belongs to the guessed upper row.

### High-load cells
- Do not sit in a lean cell under load while editing. Enter briefly, note lambda (pause the time graph if needed), back off into vacuum or a tuned area, apply the change off-load, then return to verify. Pre-load suspected high-load cells rich (one example used VE 110 %). From about 3500 rpm on turbo engines, alternate boosted sites with light-load cooling.
- Proportion matters. One practitioner judges that a brief slight lean at about 2000 rpm and 40 kPa of boost does no harm, and that at very light throttle about 1.1 lambda is tolerable. The same lean reading in high boost at high rpm is not tolerable.
- On multi-bank engines, tune to the leaner bank. If one bank's sensor is erratic, use the stable bank alone.

### How far to steady-state, and filling the rest
- Steady-state tune to about two-thirds of the rev limit (4500 to 5000 rpm in the examples). Nobody cruises above that, cells there are only transited, and holding high rpm at part load stresses the engine and makes temperatures hard to control. Above that range, visit each column briefly and make whole-column corrections, leaving it slightly rich. Accept a wider lambda tolerance in transited high-rpm part-throttle cells.
- **On a turbo road car** put the effort into low-rpm cruise and the transition into light boost. Those cells see real use: one demo engine reached 100 to 120 kPa at 3000 to 3500 rpm with only 37 to 45 % throttle.
- **Before ramp runs,** copy the last tuned column outward and add a plausible VE shape: a few percent rising toward the expected peak, then about 2 to 5 % per step falling above it, including one row past the limiter. A flat copy that runs rich where VE really falls is a safe error.
- **WOT rows on NA engines:** extend the shape across the top two load rows, add 2 to 3 % fuel and remove 2 degrees from both before the first pulls.
- **Ramp-run corrections.** Read the log at the rpm breakpoints and apply measured/target to every load row the trace interpolated between. Above the steady-state limit, apply the correction to the whole column, and carry it pre-emptively to higher columns, because the whole column was a guess.
- **Fill below the first tuned column** down to idle with the known idle values and interpolate. Linear interpolation of an intermediate column reproduces what the ECU would compute without it, so it is a sound default.

### Logs, histograms and auto-tune
- Build a histogram on exactly the fuel table's breakpoints, with the error expressed as measured/target in percent (positive means lean), and apply it as a multiplier. Plotting raw AFR is less useful once targets vary.
- **Sample filters.** Use a minimum sample count, cell-centre proximity, and transient filters (TPS rate, acceleration-enrichment flag, coolant, minimum load to exclude overrun). One cell showed 1.26 against 0.99 from only 19 samples, crossed during a gear change. Applying 26 % there would have been wrong.
- **Partial corrections.** Apply full corrections when far off and about half when close; that converges in two or three iterations. Several sources deliberately under-correct: for example 10 % where the trim showed 12 to 15 %, or 15 % for a 20 % lean column. Leave errors of about 1 to 3 % alone.
- **Visited cells only.** Paste-style and overlay tools only change visited cells, and paste garbage as faithfully as good data. Extend consistent trends into unvisited neighbours by hand, erring rich.
- **Auto-tune** computes the same ratio, so the inputs decide the result. It needs dwell time in the cell centre, a precision band (about 0.01 lambda), a centre tolerance (about 10 %), coolant and load lockouts, minimal lambda filtering, and an attempt cap. It is most useful on a dyno, or on the road where the driver must concentrate on driving. In fully automatic mode it can lock a cell before the reading settles, so keep watching.
- **Driving for data.** Use smooth, gradual throttle across many throttle angles, rpm and gears. Avoid logging after sitting heat-soaked with the bonnet shut.

### Reviewing the finished table
- A good VE table is smooth and broadly shares the torque curve's shape.
- An isolated cell that does not follow the trend is a cue to recheck it (even a 1 % step is worth noting). Examples: a cell dropping while load rises around it; fuel rising as load falls after only one of two idle cells was corrected.
- Where lambda is good at two adjacent breakpoints but dips between them, or AFR is hard to control over a narrow band, add a breakpoint.
- Smooth only the selected region, one or two passes. Over-smoothing erases real features.
- Check the table shape after each log-based edit, and extend any peak or dip it creates.

### Cruise targets
- Cruise is normally tuned at lambda 1.0; big-overlap cams may want about 0.95. Best economy sits near 1.05 on any fuel, and one source used 1.04 from 2000 to 4000 rpm and 30 to 60 kPa.
- Leaner still costs torque, so the driver opens the throttle and the saving disappears. Judge economy at constant torque, not constant throttle; a falling pulse width at fixed throttle is misleading. As a shortcut, one practitioner leans a cruise cell until torque has fallen about 6 to 7 % and stops there.

## Decision rules
- Correct by the ratio of measured to target lambda. For a small difference, a matching small percentage change is enough.
- Steady state up to about two-thirds of redline, then check higher-rpm columns briefly. Keep knock monitoring on throughout.
- Add zones only where the engine's airflow changes faster than interpolation covers.
- Lambda is never perfectly steady, so average by eye or by statistics and accept about 1 to 2 % from target (about ±0.01 lambda at idle and cruise). Road-log residuals of 1 to 3 % are generally accepted.
- At WOT, sit on target or up to 2 to 3 % rich. High specific-output engines should never be left lean of target.
- Start each new load rich and lean out towards target, since discovering lean under load is the dangerous direction. Copy forward before entering any untuned cell.
- If one cell of a new column is off, correct the whole column first.
- Never edit off-centre.
- Never sit lean at high load while editing.
- Erratic VE shapes signal a problem in that part of the table or a measurement fault. Recheck before smoothing.
- Fix fuel before ignition on every ramp-run iteration.

## Data gates
- Warm coolant and stable intake temperature, with no warm-up or post-start enrichment.
- Operating point centred in the cell, and lambda settled.
- No transient, acceleration enrichment, cut or overrun.
- Wideband valid, with its offset known.
- Closed-loop and learned trims logged and combined, or held at zero.
- Enough samples per cell for log-based corrections.

## Worked example
At 2000 rpm, a VE cell at 81.5 reads lambda 1.10 against a 1.00 target. The new value is 81.5 x 1.10 = 89.7, and lambda goes on target.

The next site up, 60 kPa, still holds an untuned 84. The trend predicts more VE, so the tuner pre-loads it before entering. It then reads 1.06 and becomes 84 x 1.06 = 89.

Copying this column to 2500 rpm with +5 % gives a first cell 3 % rich: 0.97 measured against a 1.00 target. The whole column is multiplied by 0.97, and the next column's guess is cut to +2 %.

A cell elsewhere at lambda 0.92 has a target of 0.85. The correction is fuel x 0.92 / 0.85, a rise of about 8.2 %.

## Disputed / conflicts
- **Textbook cross-check.** Textbooks support the physics of lambda and VE but give no steady-state tuning procedure. The order, the two-thirds-of-redline rule and the guess-ahead percentages are practice.
- **Steady state versus ramp runs.** One practitioner finds that ramp runs read slightly leaner than steady state for the same WOT cells, and attributes it to wall-film behaviour. That would argue for tuning each region the way it is used: steady state for cruise, ramp runs at a realistic acceleration rate for WOT. Other course examples tune WOT steady state to about two-thirds of redline and then correct on ramp runs. The discriminating test is the same cells tuned both ways on one engine, with the lambda difference logged.
- **Full versus partial corrections.** Several sources stress that one full ratio step lands within a couple of percent with a good fuel model. Others deliberately under-correct, or apply half corrections, to avoid overshoot from noise and transients. Both are valid. The choice depends on data quality and on how far off the cell is.
- **Auto-tune versus manual.** Several practitioners prefer manual edits, from logs or a log-based mixture map, for control and speed. They say auto-tune is fine in principle but is corrupted by transients, off-centre operation and heat soak. One practitioner found a particular one-key implementation worked well with a digital wideband. One practitioner considers open-loop auto-tune impractical on the road unless the engine can hover in a cell.
- **Fuel and ignition together.** A common belief holds that ignition changes alter AFR, so fuel and timing must be tuned together. The sources counter that the mixture is set before the spark. Experienced tuners may still alternate passes.
- **Smoothness.** Most sources treat a lumpy table as an error. The exception, noted by two sources, is aggressive cams with a genuine sharp VE step. Smooth only after checking.
- **Cruise lambda.** A target of 1.0 is standard where emissions apply. Leaner cruise (1.04 to 1.05) is one source's practice on cars without emissions constraints. One practitioner's 6 to 7 % torque-drop shortcut is opinion.

## Citations
- practice: Practitioner training and tuning practice, distilled and cross-checked.
- engineering-texts: Engine, combustion, charging and control engineering texts.
