---
id: methodology/compensations
title: Compensation tables
layer: L2
status: draft
confidence: high
sources: [practice, engineering-texts]
verified: 2026-11-11
applies_to: {fuels: [gasoline, ethanol, methanol], engines: [all]}
depends_on: [principles/thermo/air-density, principles/airflow/volumetric-efficiency, principles/combustion/knock]
supersedes: []
---

# Compensation tables

## Claim
Compensations carry known physics, such as air density against temperature, and deliberate changes such as richer targets or retarded timing when hot, so the main tables do not have to. Set them from the physics first, confirm them against logged lambda and knock, make sure none acts unseen where the main tables are being tuned, and never let a manual compensation repeat a correction the fuel model already applies.

## Why (derivation)
### Density and temperature
At constant pressure rho = p / (R T), so d rho / rho = -dT / T. Near 293 K a 10 K rise lowers density by about 3.4 %; the curve is slightly non-linear but a straight line is close over the normal range. If the fuel calculation does not include temperature, fuel must follow it through a table.

### Sensor temperature is not charge temperature
The charge at the valve sits between intake air temperature (IAT) and the temperature of the manifold and ports, which tracks coolant (CLT). At low airflow the charge spends longer in contact with hot metal and picks up more heat; at high airflow it picks up less. A charge-temperature estimate is therefore a blend, T_charge = T_IAT + b (T_CLT - T_IAT), with the coolant bias b larger at idle and light load and smaller at high load and rpm (one course example used about 70 % coolant bias at idle falling to about 50 % at high load). This is also why a sensor reading hotter than the charge after heat soak makes a full density correction remove too much fuel.

### How compensations combine
Fuel compensations are usually percentages of the main-table result and multiply together; ignition compensations are usually degrees and add. Several modest ignition trims active at once therefore sum to a large retard. Everything else (acceleration, warm-up, cranking enrichment) is applied on top of the main table, so an error in the base propagates into every compensation.

## Assumptions
You know which corrections the fuel model already contains (pressure, air temperature, charge-temperature blend, baro). The temperature sensors are placed where they represent what the table assumes. Main-table tuning happens at stable operating temperature.

## Breaks when
- A density compensation is applied on top of a model that already corrects for it: the correction is doubled and lambda drifts with temperature in the opposite sense to the uncorrected case.
- The IAT sensor is heat-soaked (manifold-mounted, under-bonnet restart after 10-15 minutes parked): the theoretical trim over-removes fuel at idle and light cruise and the engine runs lean, hesitant and rough.
- A generic charge-temperature model does not suit the manifold (aluminium and plastic manifolds soak differently), or a factory plenum sensor sits where it does not track charge temperature; a sensor further into the intercooler piping can work better.
- Hidden or leftover trims sit inside the normal operating range (warm-up enrichment still active at 70 C, a coolant correction at 70-80 C that switches in and out as the fan cycles): fuelling seems to change between sessions and the tuner chases it.
- Learned or closed-loop trims cover a missing compensation: they shift between a hot day and a cool night and never settle.
- A trim keyed to a slowly decaying channel (such as a time-averaged load) stays active after the condition ends, for example into part-throttle cruise.
- In ECUs that pick the richest of several active target tables, a lean placeholder used to disable a table makes an interpolated enrichment engage much later than its breakpoints suggest.

## Practical use
Check what the fuel model already covers before filling any compensation table, then work in this order.

### 1. Audit before tuning the main tables
- Confirm every fuel compensation (coolant, IAT, AFR or target offsets, throttle or speed based) is neutral across the range the engine runs in during tuning, typically from about 70 C coolant upward; check the runtime trim or correction channels in the log rather than trusting the table view.
- Zero warm-up enrichment at and above operating temperature, and tune warm-up only after the main table is done.
- Check ignition compensations the same way, including any whose axes default to meaningless ranges; rescale axes so they cover realistic temperatures.
- Keep protective trims that act only outside normal operation (for example a modest enrichment above about 105-120 C coolant, or retard at high coolant and high load).
- Start with the minimum set of compensations and add tables only when a need appears; each enabled table is something else that can be wrong.

### 2. Air temperature fuel correction
- If the model includes air temperature (ideal-gas or charge-temperature model), start the manual IAT table at zero and add only residual trim where logged lambda drifts at very high or very low air temperatures.
- If the system has no automatic correction, have the IAT table in place before tuning the main table. Leaving it at zero while tuning bakes the temperature drift of the session into the base table: one practitioner saw IAT move from 20 to 45 C through a single turbo ramp run, worth about 7 % fuel.
- Manual table: pick a zero point near 15-20 C, add fuel below it and remove fuel above it at a constant slope. The slopes used in the sources range from 2 to 3 % per 10 C (see Disputed). The zero point does not need to match the temperature at which the engine was tuned, because only the slope matters as temperature moves.
- On an NA engine, clamp the hot end (one example stopped at -7.5 % at 50 C) so a failed or heat-soaked sensor cannot strip a large amount of fuel. IAT routinely above about 60 C suggests an intake design problem unless the climate is very hot.
- Where heat soak upsets restarts, soften the lean-out in the low-load, high-vacuum region only (one example: -2.5 % at 50 C instead of -7.5 %) and keep the full trend at cruise and full load.
- To run richer when hot for knock margin: in a model that uses the lambda target, change the target with temperature (for example 0.88 to 0.86 at 60 C); in a pure pulse-width model, make the hot end of the IAT fuel table less negative instead (for example -8 % rather than -10 %).
- Verify with deliberate runs at clearly different air temperatures and adjust; real engines diverge from ideal-gas theory.

### 3. Charge-temperature models
- With a coolant-biased charge estimate, the charge temperature swings much more than IAT during warm-up (one example: about 70 C from a 20 C cold start), so the model does much of the warm-up work itself. Start the IAT trim at zero and the warm-up table at zero, then add only the residual warm-up enrichment needed.
- Set the blend so lambda tracks across temperatures first; then use a charge-temperature correction table, starting at zero, for regions that still over- or under-correct.

### 4. Target corrections versus fuel corrections
In a model where the lambda target is part of the fuel calculation, fuel compensations exist to hold the current target as conditions change, and target compensations exist to change the target. To add enrichment when hot, add it to the target; closed loop then works with the change instead of pulling it back. Do not disable closed loop to make an enrichment stick.

### 5. Ignition compensations
- Hot coolant and hot intake air move the engine toward knock; removing timing when they exceed the normal range is protection. Extra timing with cold coolant is optional and a matter of preference; if used, keep it to vacuum only and blend it out before boost.
- Calibrate IAT retard by testing, not guessing: tune at realistic temperatures, then deliberately heat-soak or block the intercooler for one or two back-to-back pulls and watch for knock. Use a 3D table against manifold pressure where available so retard applies only under load.
- Add up every trim that can be active together. Examples in the sources: 3 degrees for IAT plus 3 for coolant gives 6 when both are hot; a coolant, IAT and speed trim together leave full-load timing far below the main map, costing power, raising exhaust temperature and, on a turbo engine, upsetting boost control.
- A stock calibration may begin pulling timing at quite ordinary IAT (one example from about 30 C, about 3 degrees by 45 C at full load). Match coolant and IAT at the start of each comparison run; one practitioner moves the start of such a trim 5-10 C higher so it is inactive in normal dyno conditions but still protects above them.
- For knock that appears only when hot, a temperature-keyed retard avoids giving away power all the time; richening is the alternative.

### 6. Other compensation tables
Extra tables on other axes are useful when kept narrow: a speed-and-throttle table that adds fuel and removes timing only during sustained high-speed running (an example used 10 % fuel and 4 degrees above 200 km/h and 70 % throttle), per-gear fuel and ignition tables sharing identical axes, a switched table for special maps so normal driving is unaffected, timers that make a correction depend on time since an event, and a manifold-pressure fuel trim that removes fuel only where a throttle-based load table drifts rich at high boost (see `methodology/fuel-model-load`).

## Decision rules
- Fuel-table-based system without model temperature correction: start near 2.5-3 % fuel per 10 C of air temperature, zero near 20 C, and verify in the log.
- Model already corrects temperature: manual IAT table starts at zero; any added value is a residual trim.
- No compensation may act inside the conditions where the main table is being tuned unless it is the density correction meant to be there.
- Sum all ignition trims at the hottest realistic condition before accepting them.

## Data gates
Stable engine; a real temperature change is the thing being measured, with load and rpm held. For IAT work, compare runs whose only difference is air temperature; for ignition trims, compare back-to-back runs with knock monitored. Exclude warm-up and heat-soak restarts unless they are the subject.

## Worked example
Tuned at 20 C with no model compensation, an engine running 40 C air needs about 6 % less fuel for the same lambda (ideal gas: 293/313 = 0.936, so 6.4 %).
A manual table at 2.5 % per 10 C with zero at 20 C reads +10 % at -20 C, -5 % at 40 C and -10 % at 60 C, flat beyond. The ideal multiplier at 60 C is 293/333 = 0.880 (-12 %), so the 2.5 % slope leaves the engine about 2 % richer than the pure density calculation at 60 C, which is the margin some practitioners deliberately leave for sensor heat pick-up.
Stacked retard: main table 20 degrees at full load; coolant at 110 C adds -4, IAT above 50 C adds -2, a speed trim adds -1; delivered timing is 13 degrees, a 35 % reduction that shows up as lost power, not as a safety problem on its own.

## Disputed / conflicts
- Slope of the IAT correction: the ideal gas law gives 3.4 % per 10 K at 20 C (one training session's best-fit line gives 3-3.5 %). Practising practitioners mostly start at 2.5 %, some at 2-2.5 %, because the sensor reads air at its location rather than the charge at the valve and the pure calculation tends to over-correct. Discriminating test: log lambda error against IAT with load and rpm held and fit the slope.
- Automatic versus manual correction: most sources say leave the manual table at zero when the model corrects for temperature; one practitioner sometimes disables the automatic correction and hand-tunes a table because the model mis-corrects during heat soak. Both agree the outcome is judged by lambda tracking across temperature.
- Compensations active while tuning: the sources agree the IAT fuel correction must be active while tuning the main table. For ignition IAT trims one practitioner tunes with them at zero first and adds them afterwards.
- Cold-engine timing advance: one practitioner zeroes it as personal preference; another builds up to +10 degrees in vacuum only on a drift car. Neither is a safety issue if confined to vacuum.
- Baro correction is covered in `methodology/altitude-and-baro`.

## Citations
- practice: Practitioner training and tuning practice, distilled and cross-checked.
- engineering-texts: Engine, combustion, charging and control engineering texts.
