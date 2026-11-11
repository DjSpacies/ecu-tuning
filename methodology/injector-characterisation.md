---
id: methodology/injector-characterisation
title: Injector data before fuel tuning
layer: L2
status: draft
confidence: high
sources: [practice, reference-data]
verified: 2026-11-11
applies_to: {fuels: [gasoline, ethanol, methanol], engines: [all]}
depends_on: [principles/fueling/injector-flow-and-dead-time]
supersedes: []
---

# Injector data before fuel tuning

## Claim
Accurate injector data (flow at a stated differential pressure, dead time against voltage and differential pressure, and short-pulse behaviour where the ECU can use it) goes in before the fuel table is tuned, together with a correct description of the fuel system and the real base pressure. Otherwise the fuel table quietly absorbs injector errors, compensations act on the wrong numbers, and later changes of voltage, pressure or injectors produce errors with no obvious cause.

## Why (derivation)
Dead-time and short-pulse errors are largest at the shortest pulses (see `principles/fueling/injector-flow-and-dead-time`). If the fuel or VE table absorbs them:
- mixture moves with battery voltage and, on a fixed-pressure rail, with manifold pressure;
- percentage compensations (temperature, cylinder trims, closed-loop, flex blending) are applied to fuel the ECU believes it is delivering, so they misbehave;
- the table no longer looks like the engine. A correct model makes the VE table follow the engine's real breathing, and a smooth table shape is itself a check that the tune and engine are behaving;
- injectors cannot be swapped by data alone. With full, accurate data for both sets, an engine on a fully characterised model runs the same mixture and trims after a swap without retuning; with a time-based table it needs extensive rework.

In a model-based (VE) fuel calculation the ECU derives pulse width from air mass, target lambda and injector data, so injector data errors appear as false VE errors everywhere. In older time-based tables flow and pressure do not enter the calculation, which hides the errors but does not remove them.

## Assumptions
Manufacturer or laboratory data exists for this injector, measured on comparable drivers. Check before buying an injector: suppliers that publish dead time against voltage and pressure, flow against pressure, short-pulse correction and minimum reliable pulse or volume are preferred. Many aftermarket injectors share core units; what differs, and what matters to a modern ECU, is the quality of the data.

## Breaks when
- Data measured at another pressure, or a regulator that does not hold the pressure assumed.
- A fixed-pressure (returnless or unreferenced) rail changes differential pressure with manifold pressure, so a dead-time table on voltage alone cannot be right everywhere.
- Data copied or invented by a seller; data for a similar but different injector; modified (tip-removed) injectors.
- Aged or unmatched injectors: one random set matched to about 1 to 1.5 % at full static flow but spread about 14 % at a 2 ms pulse, while a dynamically matched set stayed within about 1 %. Static matching says little about idle and cruise.
- The ECU's units or axes differ from the data's (percent vs milliseconds, voltage breakpoints that skip 14 V).

## Practical use

### What the ECU needs
- Time-based ECUs: a master pulse scaling (often total or per-injector flow) and dead time against voltage. If the ECU has both a single dead-time value and a dead-time table, zero the single value so dead time is not applied twice.
- Model-based ECUs: rated flow at its rated pressure (or flow against differential pressure), dead time against voltage and differential pressure, minimum pulse, and a short-pulse adder where supported. The fuel's stoichiometric ratio must also match the fuel.
- Fully characterised models: minimum reliable volume, reference flow and pressure, and a linearisation table of pulse against desired volume, differential pressure and voltage. Factory ECUs with such models can only hit target if every table is right; on them, only swap to injectors with published data for that ECU.

### Tell the ECU about the fuel system
Select the regulator type correctly: manifold-referenced, fixed pressure against atmosphere, or measured with a fuel pressure sensor. A wrong choice makes the differential-pressure calculation wrong and fuelling skews with load. Set the nozzle reference: manifold pressure for injectors after the throttle, barometric for injectors upstream of it. Even with a sensor, set the regulator type and static pressure correctly, because they are the fallback if the sensor fails. Measure base pressure (see `methodology/fuel-system-sizing`) and enter the real value, because without a sensor every calculation uses it.

### Entering supplier data
- Take the dead-time row for the actual differential pressure, convert microseconds to milliseconds, and interpolate onto the ECU's breakpoints rather than copying cell for cell; extrapolate smoothly beyond the data. The range that matters most is about 12.5 to 14.5 V, since charging voltage is normally about 13.8 to 14.2 V.
- For a 3D table, use the differential fuel pressure channel as the axis, not raw rail pressure, and match breakpoints to the supplier's.
- On a fixed-pressure rail, use flow against differential pressure (or against manifold pressure) rather than a single flow number.
- If the ECU's short-pulse table uses different units or axis spacing from the supplier file, rebuild the axis to suit rather than pasting mismatched numbers. An practitioner did this when one drop-in file came in percent and the ECU wanted milliseconds.
- Load short-pulse data before any fuel tuning, as a base setting like fuel pressure. Adding it afterwards changes delivered fuel at idle and light cruise and invalidates that part of the tune.
- Peak-and-hold parameters (peak time, hold duty) matter only for low-resistance injectors; for an unlisted one an practitioner borrows them from a similar listed injector and edits only flow and dead time.

### When data is missing
In order of preference: supplier or ECU-maker characterisation; a test house; data from a well-defined factory calibration (some factory systems characterise thoroughly, others less so); an ECU injector-test mode firing a fixed count of pulses into a graduated cylinder while voltage and pressure are varied. Short-pulse data cannot realistically be produced on a dyno; leave the adder at zero rather than enter guesses, since wrong linearisation data does more harm than none.

For dead time without data, the sources converge on one approach:
1. Start from a typically shaped curve (the ECU default, or a known injector's) shifted so the 14 V value is plausible: the sources suggest about 0.75 to 1.0 ms for factory-type injectors and about 0.85 ms as a generic start.
2. Tune idle mixture at charging voltage.
3. Drop voltage by disconnecting the alternator (about 12.5 to 13 V), then add electrical load (lights, fans, heater) to go toward 10 to 11 V. At each step adjust that voltage's dead time until idle mixture returns to the 14 V value; extrapolate beyond what you can reach.
4. Watch fuel pressure throughout: the pump also slows at low voltage, and a pressure drop would lean the mixture too. Correcting that through dead time bakes a pressure error into the table.

This gets the slope between voltages right, so idle stays stable as voltage changes, but not the absolute values; the fuel table absorbs the remaining offset at 14 V. Many tuners wrongly believe it produces a true table. Some dynos offer a regression that leans and richens the mixture repeatedly to estimate dead-time error at the running voltage; it gives an estimate, not bench accuracy. On reflash platforms latency is often trimmed until summed fuel trims approach zero, with the same limitation.

### Diagnostic tests
- **Voltage sweep at idle.** With correct dead time, idle lambda holds steady from 14 V down toward 10 V. Mixture that moves with electrical load (fans, headlights) points to the dead-time slope, provided fuel pressure held.
- **Airflow or injector? (model-based ECUs).** At warm idle convert estimated air per cylinder to total airflow: g/s = rpm / 120 x cylinders x g per cylinder. Compare with what the engine should need (one practitioner uses about 3.5 to 4.5 g/s for a four-cylinder; another about 4 to 5 g/s for a warm 2.4 L four-cylinder). If estimated airflow is outside the expected window, the idle VE is wrong; if it is inside the window and the mixture is still off, the target and air are right and the fuel-mass-to-pulse conversion (dead time, then flow) is the likely fault. Compare total g/s, not a per-cylinder rule, which confuses engines of different cylinder count. An air mass meter, if fitted, can confirm the estimate. Account for warm-up enrichment before blaming either: let coolant reach operating temperature first.
- **Table shape.** A hump or upward kick in the lightest-load cells, above the smooth trend, means dead time is set too low or short-pulse non-linearity is being absorbed; a sunken idle region means dead time is too high. A flow-rate error alone scales the whole table and does not cause a local distortion.
- **Corrections that do not land.** On a well-characterised model, a ratio correction (measured lambda / target lambda) should land on target in one or two steps. A pattern of residual error after corrections, or an auto-tune that does not converge, points to injector data (especially dead time) or wrong fuel properties. A small residual is normal.
- **Backwards response.** Removing fuel at idle makes it richer, or both more and less fuel make it richer: the injector is in a bounce trough or knee. Change the operating point (different injector, a richer idle target to lengthen the pulse, staging) rather than chasing it in the table.
- **Read the pulse, not the table.** Check commanded pulse width (including dead time) to know whether idle sits in the non-linear region. A time-based table number excludes dead time and can look tiny on oversized injectors.

### Changing injectors
- Model-based: enter the new flow at the pressure you will run, its dead time and short-pulse data; mixture should start very close to target, provided the old VE table and old injector data were genuinely right.
- Time-based: multiply the master fuel value by old flow / new flow, scaling the whole table if the field cannot hold the exact figure; update dead time and short-pulse data; then warm up, hold about 2000 to 3000 rpm at light-moderate load (the linear region) and apply a whole-table correction there; only then trim idle and light cruise individually. Correcting at idle first would spread short-pulse error across the whole table.
- Either way, idle and cruise need rechecking unless the ECU models the short-pulse region and has data for both injectors.

### Injector and output tests
Test each injector output before first start with the fuel pump disabled: listen for clicking, unplug each injector to confirm the right one stops. Residual rail pressure can still be emptied into one cylinder by a continuously pulsing test, enough to flood or hydrolock it; test with the injector out of the rail, or use a test with a defined pulse count. To clear a flooded engine or check spark by cranking, disable injection rather than pulling plugs.

## Decision rules
- Use data at the actual differential pressure and voltage. Do not accept a figure with no stated pressure, and check whether a rating is volume or mass.
- With a manifold-referenced regulator a 2D dead-time table against voltage is enough. With a fixed-pressure rail use 3D (voltage and differential pressure). If only 2D is available on a fixed-pressure rail, choose the data for the differential pressure seen at idle (rail plus manifold vacuum), since that is where an error shows most; most tuners instead enter the rated pressure, which is right only near atmospheric manifold pressure.
- An engine can be tuned with dead time set to zero: the fuel table then absorbs the error at the voltage it was tuned at, but mixture moves with voltage, compensations are mis-scaled and the table no longer reflects the engine alone. One practitioner would not tune without dead time today.
- A zeroed short-pulse adder is acceptable: it costs some accuracy at idle and very light cruise, the main table absorbs it (as an odd bump of rising numbers where load falls), and a good tune is still achievable. On factory ECUs, where idle and cruise run in closed loop, missing short-pulse data makes fuel trims work hard and causes odd drivability, so buy injectors with complete data.
- A dead-time error of 0.05 to 0.1 ms does not prevent a tune; it shows mainly as an odd idle shape and slightly wrong compensations.
- Raising fuel pressure is useful only for a modest gain (about 10 to 15 % of flow in the sources); recalculate the injector data for the new pressure and stay within the pressures the injector was characterised at.
- Bench data apply at the pressure and voltage they were measured at.
- Do not leave ethanol sitting in a stored fuel system: one practitioner drains E85 and runs gasoline if the car will sit more than about a week.
- For flex-fuel, if no second-fuel flow data exist, enter the same flow for both fuels and let the second fuel table absorb the difference.

## Data gates
Fuel pressure (or differential fuel pressure) and battery voltage logged, if at all possible. Coolant at operating temperature before idle VE or dead-time work. Idle and voltage tests with closed-loop correction off or noted.

## Worked example
- At 14 V an injector shows 925 microseconds of dead time. Entering 700 microseconds makes idle lean, and the tuner then adds fuel in the idle cells, which creates an error elsewhere and makes idle mixture drift as voltage changes.
- Idle check on a four-cylinder at 920 rpm with an estimated 0.12 g per cylinder: 920 / 120 x 4 x 0.12 = 3.7 g/s, below the 4 to 5 g/s that practitioner expects for that engine, so the idle VE (not dead time) was raised by about 5 %, bringing estimated air to about 0.13 to 0.14 g per cylinder and closed-loop correction to about zero. A residual of 2 to 3 % was accepted.
- Time-based swap from 290 cc to 1180 cc injectors: 15 ms x 290 / 1180 = 3.7 ms. If the field takes whole milliseconds, enter 4 ms and scale the table by 3.7 / 4 = 0.92.

## Disputed / conflicts
- Cross-check: the square-root pressure rule follows from orifice flow; 10 to 15 % more flow means about 20 to 32 % more differential pressure.
- **Can a tuner produce dead-time data?** One course lesson says tuners cannot generate it accurately; other sessions give the voltage-sweep and graduated-cylinder methods. They agree in substance: the sweep gives the slope, not absolute values, and laboratory testing is needed for absolute and short-pulse data.
- **Which data set.** Injector-maker and ECU-maker data for the same injector were seen to differ (about 1.08 vs 1.24 ms at 14 V and about 410 kPa). Pick one consistent set; the voltage sweep can show which holds idle steadier.
- **Simple vs rich injector models.** One practitioner's view is that simple models (flow, pressure, dead time) are a deliberate balance between accuracy and data the tuner can obtain, and that the unmodelled short-pulse error is a few percent the table can absorb; others stress that richer models are what let injector swaps and staging work without retuning. Both hold: the value of a rich model depends on having the data.
- **Correcting a fuel change in flow or VE.** On a model with a non-linear small-pulse region, scaling only reference flow does not change delivery correctly across the range; one practitioner prefers a global VE change and accepts either as valid.

## Citations
- practice: Practitioner training and tuning practice, distilled and cross-checked.
- reference-data: Published reference data: thermophysical properties, fuel data, sensor and injector data sheets, statistics.
