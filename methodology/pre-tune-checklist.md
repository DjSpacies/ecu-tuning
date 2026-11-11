---
id: methodology/pre-tune-checklist
title: Pre-tune checklist
layer: L2
status: draft
confidence: medium
sources: [practice]
verified: 2026-11-11
applies_to: {fuels: [gasoline, ethanol, methanol], engines: [all]}
depends_on: [methodology/base-setup]
supersedes: []
---

# Pre-tune checklist

## Claim
A car should be mechanically and electrically sound before tuning starts. Many problems on the dyno were present before it arrived, and tuning cannot fix them. The checklist is run every time, its results are recorded, and a failed item stops the session rather than being tuned around. Most cars bring at least one problem with them, and most of those are hardware, not calibration.

## Why (derivation)
- Fuel starvation, leaks, weak charging, slipping clutches and bad compression all masquerade as tuning problems, and leaks at load are dangerous: oil on a hot exhaust is a fire risk, worst where it soaks into fabric exhaust wrap that can smoulder or ignite under sustained load.
- In one practitioner's long experience, only about one car in five went through a dyno session with no fault needing diagnosis, and roughly nine in ten on-dyno problems were wiring or sensor faults rather than calibration. A fault found after the car is strapped down costs paid dyno time just to unload it again.
- Supplied base maps exist to get a car running to the dyno; they can carry odd values (for example an individual-cylinder trim) in cells not yet visited, which surface only when the engine first reaches them.
- A tyre failure on rollers damages both car and dyno.

## Assumptions
Access to do these checks, and the engine in the condition it will be tuned in (warm where the test needs it).

## Breaks when
- A check made with the engine in a different condition will mislead (compression or leak-down from different temperatures, levels checked on a slope or hot versus cold).
- A fresh engine is still bedding in; some checks (oil pressure, leaks, coolant air) must be repeated during the first running.
- A customer's claim ("timing is set", "no leaks") is taken instead of a check.

## Practical use
### Mechanical
- Fluids: oil and coolant at level; bleed air from the coolant. Start with a full tank of the fuel to be tuned on.
- Leaks: look for oil, fuel and coolant leaks, and treat any significant leak or mechanical doubt as a stop. Refusing to run a car is better than a destroyed engine.
- Clutch: one that slips on the road will slip on the dyno.
- Compression and leak-down tests from identical conditions on every cylinder.
- Check base timing yourself, whoever says it is right.
- On first start of an unfamiliar engine, watch for fuel and oil leaks, odd mechanical noise and oil pressure (at least the warning light going out); note manifold pressure and battery voltage once running. Poor idle vacuum on a piston engine can point to incorrect cam timing.
- Confirm a stable idle at a realistic speed before loading the car on the dyno.

### Wheels, tyres and drivetrain (chassis dyno)
- Roller dyno: no tyres with cords or canvas showing; inspect the inside edge on cars with a lot of negative camber, where wear hides. Prefer hard road tyres; avoid slicks on rollers. Gross misalignment (one rebuilt race car arrived with about 15 mm toe-out on one rear wheel) makes the car pull and scrub.
- Hub dyno: bring the locking wheel nut key.
- Modern cars that compare front and rear wheel speeds may enter limp mode on an unlinked two-wheel-drive dyno; plan for a dyno mode, wheel-speed spoofing or a linked dyno.
- Automatics: know how the gear will be fixed for runs (manual mode or scan-tool command).

### Electrical and ECU
- Battery and charging healthy.
- Before changing anything, read out and save the calibration in the ECU as an untouched original.
- Audit every compensation and trim table in a supplied base map (zero or sensible) before tuning.
- Configure the rev limiter and an overboost cut before the first run; a sticking throttle cable can otherwise reach the limiter or overboost on run one.
- When something is not right, start with the simple explanations and the hardware: wiring, connectors, sensors. Put the laptop down and fault-find; scope outputs (for example injector drive) to separate a fuel cut from an ignition fault.

### Fresh or rebuilt engines
- Prime oil pressure by cranking with plugs out and fuel and spark disabled before first start (it can take 30 to 45 s in one demonstration).
- One practitioner's break-in procedure on the dyno: start, immediately apply light load in a high gear at about 2000 to 2500 rpm while checking leaks and bleeding coolant; then short load bursts at 2000 to 3000 rpm and light-to-moderate throttle followed by backing off into vacuum, building over about an hour towards two-thirds of the limit and moderate throttle; then change oil and filter and cut the filter open to look for copper. Falling oil pressure means stop and investigate; expect slightly higher temperatures from ring friction. Backing off into vacuum draws oil up the bores, cools the rings and flushes hone debris.
- Assembly and clearance errors usually show up almost immediately, often before run-in ends; a failure thousands of km later points elsewhere.

### After a failure: find the cause before re-tuning
- Work out what broke first (secondary damage from a high-rpm failure obscures the origin), then why, then change something so it cannot recur. Categories overlap: assembly error, clearance, lubrication, mechanical strength, tuning.
- Rod bolt: a bolt stretched and necked down to a break, with fretting between rod and cap, was correctly tight and failed in tension; without necking and fretting, suspect assembly.
- Bearings: copper showing means metal contact; wear biased to one side of the main shells suggests crank flex at high rpm and load; scoring in the rotation direction suggests debris; blue or black discolouration means severe contact. Damage worst at the last rod and main on the gallery points to oil supply or control, typically starvation in hard cornering on a wet sump.
- Fretted main cap and block faces mean the caps are moving under load and the engine is at its clamping limit.
- Polish on the piston crown edge with a matching witness mark on the head means contact; aluminium rods grow when hot and need extra clearance.
- After a bearing failure, replace the oil cooler (debris trapped in the matrix comes back out when oil warms) and clean all galleries.

## Decision rules
- Start with a full tank of the fuel to be tuned on.
- Look for oil, fuel and coolant leaks, and treat those as stops.
- Check base timing yourself, whoever says it is right.
- Do compression and leak-down tests from identical conditions.
- Start with the simple explanations when diagnosing.
- Protections (rev limit, overboost cut) configured before the first run.
- Original calibration saved before the first edit.
- After an engine failure, no re-tune until the first failure and its cause are identified.

## Data gates
- Coolant, oil and fuel levels verified; battery and charging healthy.
- Oil pressure present at idle and rising with rpm; no leak found under light load.
- Stable idle at a realistic speed before load work.
- Tyres and restraint fit for the dyno type.

## Worked example
A misfire under boost turns out to be a coolant leak onto a coil. Finding it first saves the session.

A second, modelled on a training session: a fresh engine completes the structured dyno break-in with steady oil pressure and no leaks. At the oil change the filter is cut open and shows a small amount of copper-coloured material. That points to bearing contact; the session stops for inspection rather than proceeding to full-power tuning, because once metal contact starts it accelerates quickly to seizure.

## Disputed / conflicts
- Break-in: one presenter argues that with modern honing and ring materials, rings are effectively bedded within roughly 80 to 100 km or about an hour of structured dyno running, so full-power tuning can follow in the same session after the oil change, and that bearings and pistons have nothing to bed (they run on an oil film; metal contact is a build fault). Common advice is thousands of km of gentle driving or a separate run-in tune. One practitioner's view, labelled as such.
- Break-in oil: the same presenter prefers a good mineral oil (synthetic may hinder ring seating) and a second change after about 200 km, but concedes modern rings may seat on synthetic anyway; run-in oils low in detergent must not stay in.
- Road versus dyno break-in: on the road the drivetrain can motor the engine with a closed throttle for deeper vacuum; on a roller dyno load cannot be removed as completely, but leaks are much easier to watch. One practitioner's comparison.

## Citations
- practice: Practitioner training and tuning practice, distilled and cross-checked.
