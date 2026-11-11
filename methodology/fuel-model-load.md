---
id: methodology/fuel-model-load
title: Fuel model and load axis selection
layer: L2
status: draft
confidence: medium
sources: [practice, engineering-texts]
verified: 2026-11-11
applies_to: {fuels: [gasoline, ethanol, methanol], engines: [all]}
depends_on: [principles/airflow/volumetric-efficiency, principles/thermo/air-density, principles/fueling/injector-flow-and-dead-time, principles/fuels/stoichiometry-and-lambda]
supersedes: []
---

# Fuel model and load axis selection

## Claim
The fuel model decides what the main fuel table means, and the load axis decides which engine states share a cell. Choose both before tuning, because changing either later invalidates the table. In an airflow (VE) model the table should describe only air; the lambda target, injector data, fuel properties and capacity each carry their own effect, so they must be right first or their errors are absorbed into the VE numbers. Use manifold pressure as load unless it stops tracking airflow (individual throttles, very large cams, boosted engines backed off the throttle), and then use throttle position with pressure still in the calculation.

## Why (derivation)
### The speed-density chain
Per cylinder per cycle: m_air = VE x (p_man / (R T_charge)) x V_d / n_cyl. Fuel mass m_fuel = m_air / (AFR_stoich x lambda_target). Effective pulse width = m_fuel / (injector mass flow at the actual pressure difference), then dead time and any short-pulse correction are added. A MAF system replaces the first step with a measured air mass (g/s), and per-cylinder load is g/cyl = (g/s x 120 / rpm) / n_cyl. With pressure, temperature, target and injector terms outside the table, the VE table is flatter and mostly shows how the engine breathes.

### Pulse-width models and their background multipliers
In a time-based model the table holds pulse width directly, or a percentage of a master pulse width. Effective PW = PW_master x cell/100 x (p_man/100 kPa, if load equals MAP) x (1/lambda_target, if a target overlay is on) x compensations. With the MAP multiplier, doubling manifold pressure doubles fuel, so the table only needs to describe VE and target changes. With the overlay, the table is in effect tuned to lambda 1 and the target applies 1/lambda in the background (0.82 gives about 22 % more fuel), and the model then behaves almost like a VE model. Order of multiplication does not change the result, so a MAP-axis enrichment table filled with 1/target - 1 does the same job on an ECU without an overlay. Rescaling: because delivered PW is master x cell, a change of master from PW_old to PW_new is neutral if every cell is multiplied by PW_old / PW_new.

### Why manifold pressure can stop representing load
Load equals MAP assumes trapped air is proportional to manifold pressure at a given rpm. It fails when:
- Individual throttles or very large cams: the volume between throttle and valve is tiny, so pressure reaches near atmospheric by about 30-40 % throttle and every larger opening collapses into one row; a balance-tube average also misrepresents the cylinder on its intake stroke, which sees deeper vacuum behind its own blade. A big-overlap cam on a single throttle can idle at 70-80 kPa, leaving 20-30 kPa of span.
- Turbo engine backed off the throttle: the wastegate closes to hold boost, so the same manifold pressure occurs with less throttle and higher exhaust back pressure; trapped air falls and a MAP-indexed cell runs rich (one example: a cell at 8 psi tuned to 13.0:1 at full throttle read 11.5-12:1 at 30-40 % throttle with a high boost target).
- Variable vane turbines change back pressure with vane position, so VE moves with vane state; a MAF follows this, speed density must be corrected.
- Several continuously variable cams and runners: VE is no longer a function of rpm and load alone; factory systems use table sets per cam state or a learned model.

### Charge cooling
Evaporating fuel cools the charge, which raises its density in proportion to fuel quantity. Some models include a charge-cooling coefficient for this. It mainly decides whether measured lambda follows a change of target, and in a generic model it partly acts as a fitting factor rather than a measured temperature drop.

## Assumptions
Injector flow, dead time and short-pulse data are characterised (`methodology/injector-characterisation`). Capacity, cylinder count, fuel type and stoichiometric ratio, fuel density and its temperature coefficient, fuel pressure reference and base pressure are entered correctly. Lambda targets are realistic before any VE tuning. Mechanical configuration is fixed for the life of the calibration.

## Breaks when
- Setup data is wrong: a stroker entered at stock capacity (for example 2.0 L built to 2.3-2.4 L), wrong injector flow or rated pressure, or a placeholder target table; the VE table absorbs the error, loses meaning and stops tracking target changes. Half a millimetre of overbore barely matters.
- The charge-cooling coefficient is changed after the VE table is tuned: it shifts fuelling everywhere and forces VE rework.
- A MAF is used outside its calibration: any change to the airbox, filter, duct or meter housing alters the velocity profile and the transfer curve; the output saturates once airflow exceeds its range (fuel stays flat and, worse, ignition stays at the lower-load value, a recipe for knock); reversion pulses from big overlap are counted more than once; an atmosphere-vented blow-off valve dumps air that was already metered, giving a rich spike or a stall on lift, and a recirculation return aimed at the meter can push air back through it.
- Generic VE models are not exact: the same engine on three VE-based ECUs gave tables that could not be swapped, and absolute VE values differ with how deeply each ECU models the injector and fuel pressure.
- Using injector tables to hide an airflow error, or VE to hide an injector error: both corrupt the model and the error reappears elsewhere.

## Practical use
### Choose the model
- Time-based (ms) and percentage-of-master models are direct and transparent, but target, injector size and density are baked into the numbers, so changing injectors or targets means retuning the table. Starting values depend on injector size (going from about 350 to 1000 cc injectors cuts every value by roughly two thirds), so base-map tools or calculated required fuel help before first start.
- VE models compute fuel from air, target and injector data. Gains appear only when everything is calibrated: mixture changes in the target table alone, an injector swap that needs only new data plus a check, and flex fuel, because engine VE barely changes with ethanol content and fuel properties are modelled separately. A flat VE of about 50 % across the table usually starts the engine.
- Know what the numbers literally are. Some ECUs store literal milliseconds, others a percentage of a master value, others VE; some display a VE or duty view of a time-based table that is only an estimate. A table whose load axis is labelled generically ("efficiency", "load") must be traced to the channel that drives it; move the throttle and confirm the cursor moves as expected.
- In a time-based model the target table only drives closed loop (unless an overlay is on). To test whether the engine wants a different mixture, change the main table, or both tables; changing only the target just makes the trims work harder.

### Choose the load axis
- Manifold pressure for most engines (sources put it at about 90 %), including turbo single-throttle engines. Confirm whether the axis is absolute or gauge before editing.
- Throttle position (alpha-N) for individual throttles and for cams too large to give usable idle vacuum. Still fit a MAP sensor (runner tappings joined into a small balance volume) and use it as a background pressure term; without it part-throttle lambda wanders on gentle hills. On NA alpha-N, baro as the equation pressure term is steady and still follows altitude.
- Turbo with individual throttles: VE on throttle position, the ECU multiplying fuel by measured manifold pressure, lambda targets and ignition on manifold pressure, and a separate manifold-pressure fuel trim for the high-boost, high-rpm richness that appears as the turbo leaves its efficient range and back pressure rises (examples: rich drift from about 15-20 psi on stock turbos; trims of -1 to -4 % at 6000-7000 rpm and 220 kPa, deepening with boost). Correct only at the lowest boost in the throttle table, because its full-throttle cells serve every boost level; make high-boost corrections in the pressure trim.
- A combined mode, throttle-based at idle and pressure-based above set thresholds, helps big-cam engines idle. MAF only where rules require it or the factory meter is accurate and unrestrictive.
- Prefer a single primary table with deterministic background terms; with two blended primary tables it is unclear which to correct.
- Exhaust-to-intake pressure ratio as a load term is possible where a math channel and an exhaust pressure sensor exist (see `methodology/altitude-and-baro`).

### Set up a VE model, in order
1. Capacity, cylinder count, firing order, fuel type and stoichiometric ratio (14.7 for pump gasoline), fuel density and temperature coefficient, fuel pressure reference (manifold-referenced, returnless or measured) and the base pressure at which injector flow was rated.
2. Injector flow, dead time and short-pulse data.
3. The lambda target table with the mixtures actually wanted everywhere (sources use about lambda 1.0 for cruise, slightly rich of 1 at idle where it idles better, about 0.95 at light load high rpm, about 0.85-0.90 at NA full load and about 0.78-0.82 on boost with pump fuel). Target breakpoints can be coarser than fuel breakpoints. The most common mistake reported is leaving default targets and forcing the desired mixture through VE.
4. Charge-cooling coefficient, if the model has one, by a target-step test (below), early and before detailed VE work.
5. VE table, tuned until measured lambda equals target (`methodology/steady-state-fuel`, `methodology/airflow-ve-table-shaping`). Afterwards, change mixture in the target table and leave VE alone unless airflow changes mechanically.

### Target-step test for model consistency
With closed loop off and VE trimmed to hit lambda 1.0 at a steady mid-map cell (about 3000 rpm, moderate load, away from idle heat soak and the injector's short-pulse region), change only the target to about 0.90. If measured lambda goes richer than requested, reduce the coefficient; if leaner, raise it (calibrated values in the sources range from about 5 to 63 depending on the model's units and the engine; a direct-injection engine landed far from its default). Re-trim VE to the base target after each change, repeat until requested and measured agree, then restore the original targets. Errors of about 1 % are within margin. The same step test, with no coefficient involved, is a quick check of any VE model: a well-calibrated model followed a WOT target change from about 0.89 to 0.82 within about 0.01.

### Percentage-of-master models: resolution
Choose the master value so table numbers use the range: sources aim for peak cells around 60-90 % with headroom below any cap, idle cells around 30-40 %, and the onset of boost around 40-50 %. Too large a master leaves small numbers where the smallest edit step is a large fuel change; too small runs out of range before full load. Rescale the whole table by old/new when changing the master; expect a momentary lean or rich step until the table is rescaled, and confirm a reference cell lands within about 0.02 lambda.

### MAF calibration
- The MAF transfer curve (voltage or frequency to g/s) plus injector data is the main fuelling job on a MAF system; ignition load usually comes from it too, so get it right before anything else.
- Prepare: disable closed loop and long-term learning, set open-loop modifier tables to neutral, disable over-temperature enrichment and overrun cut, fix full-load enrichment at one conservative target with an entry threshold that is not crossed by accident, and stop any speed-density subsystem from blending in during transients, so the error you log belongs to the meter.
- Collect steady-state data up to the full-load enrichment crossover and separate full-throttle ramp data, logging only after the enrichment step; a wideband lags a target step and creates false errors near the crossover. Drive smoothly or filter large throttle changes.
- Histogram measured/commanded lambda error against meter frequency or voltage, with bins matching the calibration breakpoints. Rich means the meter is over-reporting air: reduce the curve there by the error; lean means increase it. Apply full error on the first pass and about half on later passes, average out isolated cells whose sign flips, extrapolate the trend into unlogged cells, and keep the curve smooth (a good one is a smooth near-exponential shape; bumps cause driveability problems). Expect two or three iterations. Small residual full-load errors are better left in the commanded mixture table than chased into the curve.
- Acceptance as the sources present it: residual error about 1-2 % (about 1 % at full load ideal); idle trims within 3-5 % on an incoming car suggest a reasonable calibration; trims of 10 % or more mean the curve needs work. Band-aiding with trims tends to produce fault codes days after the car leaves.
- Where a load-compensation table also acts, use rpm as a second histogram axis: scale the meter from rpm bands where the compensation is inactive, and assign remaining error at the same meter output in the active band to the compensation table.

### Attribute the error before correcting
If the air estimate is believable (idle g/s check, VE shape against torque) and lambda still misses, the error is on the fuel side: injector flow or dead time. Idle magnifies dead-time error because dead time is a large fraction of a short pulse; a VE error would show across operating points. Correct the side that is wrong.

## Worked example
Speed density, 5.74 L V8 (350 ci) at 6000 rpm, standard density 1.225 kg/m3, VE 1.0: volume flow = 0.00574 x 6000/120 = 0.287 m3/s; air = 0.352 kg/s (about 46 lb/min); per cylinder 0.044 kg/s. At AFR 12.5 each cylinder needs 3.52 g/s of fuel. An injector of 7.56 g/s (60 lb/h) runs at 3.52/7.56 = 46.6 % duty; at 6000 rpm the cycle is 20 ms, so effective pulse width is 9.3 ms, plus dead time.
Master rescale: master 13 ms to 10 ms, multiply every cell by 13/10 = 1.3; a reference cell at 34.5 % becomes 44.9 % and delivers the same fuel.
MAF load: 300 g/s at 5000 rpm on a V8 is (300 x 120 / 5000) / 8 = 0.9 g/cyl.
Target overlay without the feature: base tuned to lambda 1; for 0.85 enter 1/0.85 - 1 = 17.6 % enrichment in the MAP-axis table.

## Disputed / conflicts
- VE versus time-based models: several practitioners say both tune equally well and the claimed injector-swap benefit is moot because a careful tuner rechecks anyway; others prefer VE for consistency between cars and for flex fuel. The VE model's advantage requires correct injector data and capacity.
- MAF versus speed density: many aftermarket tuners treat the MAF as a restriction and a nuisance (reversion, blow-off valves, bulk). Other training sessions argue a correctly calibrated, unrestrictive factory meter is very accurate, needs fewer compensations and suits emissions, and back-to-back tests on later engines showed no power from deleting it while a small early meter cost about 15-25 whp. Context decides: intake changes, cam overlap, boost and meter range.
- Throttle-based fuel on plenum turbo engines: one practitioner prefers throttle position with a pressure overlay even on single-throttle turbo engines because it models back-pressure-driven VE changes; the common practice is manifold pressure, with satisfactory results.
- Charge-cooling coefficient: some models omit it and still track target changes well; its value is small but it also feeds background corrections, so some practitioners calibrate it anyway.
- Feature-rich models: one practitioner's view is that a simpler model the tuner fully understands often gives a better result than a more complete one set up carelessly.

## Citations
- practice: Practitioner training and tuning practice, distilled and cross-checked.
- engineering-texts: Engine, combustion, charging and control engineering texts.
