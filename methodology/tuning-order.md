---
id: methodology/tuning-order
title: Overall tuning order
layer: L2
status: draft
confidence: high
sources: [practice]
verified: 2026-11-11
applies_to: {fuels: [gasoline, ethanol, methanol], engines: [all]}
depends_on: [methodology/pre-tune-checklist, methodology/steady-state-fuel, methodology/steady-state-ignition, methodology/full-load]
supersedes: []
---

# Overall tuning order

## Claim
Tune in an order that makes each stage safe for the next and does not get undone by a later stage: configure and verify first, then start and idle, then fuel before ignition in steady state, then full load, then confirm in real conditions, and leave the corrections that sit on top of the base tables (transient enrichment, cold start, idle ignition control, fine injection timing) until the base is right. Anything that changes airflow everywhere (cam timing, staging ratio, temperature-compensation strategy) is settled before the fuel table it would invalidate. Effort is spent where the engine actually operates.

## Why (derivation)
### Dependencies
- Every later step relies on the ECU's view of sensors, crank and cam position being right, so inputs, outputs and trigger come first. A mechanical or sensor fault found late wastes all the work above it; poor idle vacuum or unstable idle is often the first symptom of one (for example wrong cam timing), which is why idle is sorted early.
- Fuel and spark are effectively independent controls: fuel tracks airflow, spark sets cylinder pressure. With timing held deliberately low, fuel corrections reflect airflow only, there is almost no knock or pre-ignition risk while the fuel is still unknown, and those same knock-free runs give a clean background-noise baseline for knock calibration. Once fuel is on target, further fuel edits add no power; power then comes from spark and cam.
- Multipliers on top of a base table inherit its errors. Cold-start and warm-up corrections, acceleration enrichment and its temperature correction all act on the VE or fuel table; tuned against a wrong base they absorb its error, and any later base change throws them out. Using transient enrichment to hide steady-state table errors wastes time and gives poor results.
- Some choices change the base everywhere. A cam change alters VE across the map; a wrong secondary-to-primary staging ratio gets tuned into the fuel table; switching the temperature-compensation mode, or later changing the charge-temperature bias, shifts fuel delivery everywhere. Decide these first.
- In a VE-based fuel model, defining injector data, fuel type and the lambda target table before tuning VE means later mixture changes are made in the target table alone, without retuning VE.

### Where effort pays
A road car spends most of its time at idle and light-throttle cruise (the sources give anywhere from 70 to 95 % at part throttle and roughly 5 % at WOT). Drivers notice a cruise cell 10 % lean as hesitation long before they notice a few kW at 6000 rpm WOT. High-rpm part-throttle and high-vacuum cells are only passed through on shifts and lift-offs, so they need safe, sensible values rather than precision. Fuel must be safe in every cell; ignition can be merely safe and smooth in rarely used areas.

## Assumptions
- An engine that runs mechanically, with correct sensors and known fuel; the pre-tune checklist has been passed.
- A load-bearing dyno for the steady-state stages, or the road techniques in methodology/road-procedure.

## Breaks when
- A new fuel, cam, boost hardware or other mechanical change resets the stages it affects.
- Knock-limited engines may need ignition and lambda targets revisited after full-load findings (richer targets can buy timing).
- Variable cam engines: fuel changes so much with cam angle that perfecting fuel before the cam targets are settled wastes work.
- Engines whose part throttle is little used (dedicated drag or race cars) or whose rpm range is limited (a cruiser that never sees high rpm) justify a different split of effort.

## Practical use
### The ten steps
1. Configure the ECU and test inputs and outputs. 2. Trigger setup. 3. Base table configuration. 4. Base ignition timing and fuel pressure. 5. Initial start. 6. Idle. 7. Steady-state fuel. 8. Steady-state ignition. 9. Full-power tuning. 10. Confirm in real conditions. Do not skip forward over an unresolved fault. The basic setup steps are the ones experienced tuners most often skip, and they are a common root of problems.

### Stages 1 to 6: before load
- First connection: read out and save the calibration already in the ECU as an untouched original in a per-project folder, separate from vendor base maps; edit only a working copy. Save a new named file at each stage (base, idle and start-up, part-throttle cruise, WOT, and any special feature) so there is always a known-good point to step back to.
- Some ECUs lose live edits at power-down unless they are explicitly stored, and an undo may only reach back to the last store; store often.
- Check sensors (MAP against baro, throttle position), crank and warm up, review fuel and spark at idle, confirm idle control works, verify base timing with a timing light, run any variable-cam test. Switch any timing lock off after setting base timing: if ignition table changes produce no torque change at all, a timing lock left on is the first suspect.
- Leave master fuel and ignition trims at zero. Use them only for quick across-the-board tests, then move any kept change into the main table; a forgotten ignition trim can mean more timing in the engine than the table shows.
- Audit every compensation and individual-cylinder trim table in a supplied base map before tuning; base maps exist to get the car to the dyno and can hold odd values in cells not yet visited.
- On a generated base map, an idle error of a consistent size usually means the whole map is off by about that much; apply the coarse correction globally rather than to the idle block alone.
- On ECUs whose tables do not re-interpolate when an axis breakpoint changes, finalise breakpoints before tuning. Elsewhere, start with coarse resolution and add breakpoints where lambda swings or torque steps locally; adding them mid-tune does not harm existing work.
- Choose the temperature-compensation strategy now and keep it.
- Begin with only the essential corrections enabled (coolant and air temperature); add others when a specific need appears. Keep torque-management and similar strategies as simple as achieves the goal.
- Get a stable idle at a realistic speed and confirm the engine is mechanically sound before loading the car on the dyno.

### Stages 7 and 8: steady state
- Set timing deliberately low and flat across the area being fuelled (the sources use about 10 to 20 degrees at part throttle, and very low values in boost) and tune fuel first. Listen for knock even during fuel-only work: the "safe" map could still be over-advanced somewhere. Experienced tuners alternate fuel and ignition cell by cell.
- Work from low rpm and low load upward, copy each finished column or row forward as the start for the next (scaled up a few percent for fuel at low rpm, where VE rises with rpm), and extrapolate slightly conservatively into the next cells so each new cell starts close.
- Steady-state tune to about two-thirds of the rev limit (some sources say three-quarters; one says 4000 to 5000 rpm on a 7000 rpm engine is fine), then switch to ramp runs. Stop lower on an engine that never operates higher, such as a high-mileage cruiser.
- Turbo engines: steady-state up to wastegate spring pressure, treating it like an NA engine with richer targets. The cruise and transition zone of a turbo road car reaches into mild positive boost at small throttle openings; map it accurately with targets leaner than NA WOT values.
- Cam control: either settle cam targets first at WOT with fuel and timing roughly right and then map part throttle, or do cam and fuel together cell by cell, keeping fuel merely safe until the cams are settled; optimise ignition last because better filling speeds combustion and changes MBT.
- Staged injection: tune the base table on primaries until primary duty approaches its upper working range, then bring staging in and judge the ratio from the lambda change before continuing.
- Charge-temperature tables: tune early with fuel roughly right, by varying intake temperature at a fixed operating point; afterwards do the main VE table.

### Stage 9: full load
Finish WOT changes before blending them into lower-load areas, so a change that proves useless is easy to remove. Fuel first, then timing; then step boost up row by row. Details in methodology/full-load.

### Stage 10 and after
- Confirm on road or track (methodology/road-procedure).
- Then transient enrichment, tuned warm first and then cold for its temperature correction.
- Cold start, cranking and warm-up from a truly cold engine: the block holds heat for hours (one demonstration still read 33 C after two hours), so this is next-morning work, often a two-day booking. You get one genuine cold start per soak.
- Idle ignition control last, after main fuel and ignition are right.
- Injection timing is a final refinement after fuel and ignition; staged injectors at different distances from the valve may each want their own timing.

### Priorities and scope
- Road car: idle (hot, cold and heat-soaked restart), then cruise, then WOT safety, then the rest. A tune done only with WOT ramp runs leaves the most-used areas untuned.
- Dedicated drag or race car: start, warm up and drive through the pits without stalling, surging or bucking; part throttle must not be grossly rich or lean but gets limited time. Make the first pass of a day a dialled-back checkout.
- Match lambda and timing margin to use: road use rarely holds WOT beyond 6 to 7 seconds; circuit and top-speed use hold load far longer and need more margin, or ECU features that reduce power with average load or time at WOT.
- Competition reliability margin outweighs the last horsepower; stop when target power is reached with conservative timing and boost.

### Working habits
- One change category at a time, also on reflash platforms where flashing is slow and batching is tempting; small timing steps (about 2 degrees).
- Correct mixture by the computed percentage error, as a multiplier over a block, not by repeated small nudges.
- View tables as a 3D surface or with a colour gradient as well as numbers; a typo such as 7 for 70 hides in a grid but shows as a spike. Rotate the view to a realistic scale.
- Smooth at most once, and only where irregularities remain after interpolation; repeated smoothing alters correct cells.
- Treat auto-tune output as information and apply it selectively; it absorbs transient and other background errors into the table.
- Chasing torque differences under about 1 % wastes time.
- When something is wrong on the dyno, suspect wiring and sensors first (one practitioner's estimate is nine problems in ten); put the laptop down and fault-find the hardware.
- Plugs show only the instant the engine was cut; use them to check heat range, damage, early detonation and cylinder distribution, not mixture through a run.
- Keep firmware current, but not the day before an event.

## Decision rules
- Follow the ten steps in order; do not skip forward over an unresolved fault.
- Fuel before ignition, with timing held safely low while fuel is unknown.
- Base tables before the corrections that multiply them (transient, cold start, idle ignition).
- Settle airflow-changing choices (cam targets, staging ratio, temperature-compensation strategy) before finalising fuel.
- Master trims return to zero once the main tables carry the change.
- Save the original calibration before any edit, and a named file at each stage.

## Data gates
Each stage has its own gates in its own entry. Moving on requires: inputs and trigger verified; stable idle and no leaks or mechanical warning signs; steady-state fuel tracking target across the reachable map before ignition optimisation; fuel safe at full load before timing is advanced; cold-start work only from an engine at ambient temperature.

## Worked example
An engine starts but its trigger scope shows missing sync events under load. Stop: stage 2 is not complete, regardless of how far fuel tuning has got.

A second case from an practitioner's anecdote: a car runs well at moderate boost, but at high boost on race fuel it behaves as if it hits a limiter at 7000 rpm. Time is lost chasing ignition. Scoping the injector drive shows one injector switching off at that rpm and load; the supplied base map carried an individual-cylinder trim of about -100 % in cells that had never been visited. Auditing every trim and compensation table at stage 3 would have found it, and scoping injector drive separates a fuel cut from an ignition fault.

## Disputed / conflicts
- WOT first or part throttle first: the structured courses teach part throttle first, which builds most of the map before WOT and suits learners. One presenter's view is that an experienced tuner can do WOT first, building the map quickly and safely, and that an early ramp to the limit exposes an inadequate pump or injectors before hours of part-throttle work. Cam work is a special case where WOT cam optimisation first is recommended because a cam change alters VE everywhere.
- Fuel and ignition separately or together: separate is the taught method for learners; experienced tuners alternate. Both agree timing must be safe while fuel is unknown.
- How far to steady-state tune: about two-thirds of the rev limit in most sources, about three-quarters in one session, lower on engines that never rev. Turbo boost cells: one session steady-states only a little way into boost because ramp operation differs from steady state anyway, while others steady-state up to spring pressure.
- Fresh engines: one presenter argues modern rings bed within roughly 80 to 100 km or an hour of structured dyno running, so full tuning can follow in the same session after an oil change; common advice is a long gentle run-in first. One practitioner's view; it concedes the oil-type point is uncertain (see methodology/pre-tune-checklist).
- Whether fuel pressure sensing and full injector characterisation are essential: one presenter's view is that they are nice to have, having tuned for years without dead-time compensation; other KB entries treat injector data as the foundation of a VE model (methodology/injector-characterisation).

## Citations
- practice: Practitioner training and tuning practice, distilled and cross-checked.
