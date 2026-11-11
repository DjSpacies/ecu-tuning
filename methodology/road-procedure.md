---
id: methodology/road-procedure
title: Road and track procedure
layer: L2
status: draft
confidence: high
sources: [practice]
verified: 2026-11-11
applies_to: {fuels: [gasoline, ethanol, methanol], engines: [all]}
depends_on: [methodology/dyno-procedure, methodology/data-quality, methodology/log-capture-protocol]
supersedes: []
---

# Road and track procedure

## Claim
Without a dyno, the driver is the load control. Use smooth inputs and data logging, and take only as much road risk as the task needs. Road and track work does two jobs: it confirms a dyno tune under real airflow, temperatures and load, and it reaches cells a dyno cannot hold. Fuel can be tuned well on the road; ignition cannot be optimised to MBT there, because there is no torque measurement, so road timing is set conservatively against knock.

## Why (derivation)
### What the road has that the dyno lacks
- Airflow: at 100 to 150 km/h the radiator, intercooler and engine bay see airflow no dyno fan reproduces, so coolant and intake temperatures, and therefore fuelling and knock margin, differ. Intakes that draw air from behind the radiator can run tens of degrees hotter on track than on the dyno.
- Inertia: on the road the car's mass keeps the engine turning when the throttle is nearly closed, so the high-vacuum cruise and coast cells a load-bearing dyno cannot hold (it needs some torque to keep turning) become reachable.
- Sustained load: a road pull in a high gear, back-to-back gears, or a long track straight builds more chamber heat than a short dyno ramp. Exhaust temperature keeps rising under sustained load while a short ramp never reaches equilibrium.

### What the road lacks
- Load control: opening the throttle makes the car accelerate, so rpm climbs out of the column. Gear choice and the brakes provide the load instead. Left-foot braking against the throttle acts like an adjustable hill.
- Torque measurement: seat-of-the-pants feel resolves perhaps 5 to 10 hp at best, while timing optimisation is about gains of 2 to 3 whp. Log-based acceleration estimates depend on identical runs, which road surface, gradient, wind and heat soak prevent.
- Attention: watching a laptop or wideband while driving compromises control, and full-power tests may need speeds beyond legal limits. A closed road or track and a second person are strongly preferred.

## Assumptions
- A safe, legal place to test (closed road or track for anything beyond low-power cars), and an extra person where possible.
- A wideband logged by the ECU or a logger, plus a gauge readable in peripheral vision; audio knock monitoring for full-load work.
- The engine has a safe base: idle and fuel roughly right, timing conservative, protections configured.

## Breaks when
- Road gradient, wind, traffic, corners and bumps interrupt steady data; legal speed limits cap which gears and rpm can be used.
- Heat soak after a stop (roadside edit, reflash, pit lane, idling in traffic) skews the first minutes of data.
- Throttle transients and gear changes trigger acceleration enrichment, deceleration enleanment and overrun cut, which contaminate steady-state lambda.
- Brake heat from left-foot braking rises quickly with engine power, limiting how much of the map can be held this way.
- Automatics kick down or slip; a loose converter means low-rpm high-load cells cannot be reached on the road either.

## Practical use
### Before logging
- Drive at normal speed for a couple of minutes (the sources use one to three minutes, or a lap) after any stop until coolant and intake temperatures are back to normal running values, then start the logger. In one demonstration intake temperature in the pits was about 48 C and fell back towards the 30s before logging resumed. Data taken while heat-soaked produces corrections that look wrong once the engine recovers, so the tuner chases their tail.
- Use a portable wideband matched to the one used on the dyno so road and dyno readings compare.
- Clear any adaptive learn tables before a confirmation drive if learning is being used, and make sure warm-up is not being learned.

### Steady-state (cruise and part throttle)
- Choose 3rd or 4th gear for most steady-state work (2nd, 3rd and some 4th across the map in one session). Low gears multiply torque, so a powerful car spins its wheels and heats the brakes; high gears reach excessive road speed high in the rev range.
- Hold a column with left-foot braking: light, subtle brake pressure while slowly opening the throttle, increasing brake as throttle rises, working down one rpm column through each load cell and staying centred in each cell. It feels unnatural until practised.
- For the lightest load row, where the engine slows even on the road, accelerate slightly above the target rpm, drop to that throttle and take the reading as rpm coasts through the cell centre.
- Brake heat: work one column, then release the brakes and cruise at moderate speed to cool them in moving air. Stop loading the brakes at pedal vibration, sponginess, reduced effect or hot-brake smell. Do not park with very hot brakes; the rotor under the pads heats locally and warps.
- Keep throttle movement slow and smooth, avoid gear changes, and dwell in each cell until the averaged value stops changing; pass through target cells many times. Pause through corners and bumps.
- Log in one gear and start the logger only once in that gear. Use the throttle trace to separate steady sections from transients and ignore lambda during transients.
- Note the rpm and load of any hesitation, surge or roughness, ideally with a passenger recording; those are cells to investigate.
- A cell-averaging trace or quick-tune tool on a long drive gathers broad cruise coverage much faster than picking corrections from a log by hand. Expect more than one pass.
- Alpha-N (throttle-position load) maps are easier to hold on the road, since a throttle position is held directly rather than hunting for a MAP value. The lowest throttle rows still need road work, and where idle is held by an electronic throttle the idle throttle position may not be near zero.

### Ignition on the road
- Without torque feedback, only confirm that the base ignition table is knock-free in steady state; deal with knock as on a dyno. Refine lower-load timing later.
- On a knock-limited engine, advance carefully with knock detection to the threshold and then back off (2 to 3 degrees in one session). Where knock never arrives first, it is easy to go past MBT and lose torque with no warning; road tune conservatively and buy dyno time for ignition.
- Proxies for torque on the road (each with limits):
  - Throttle roll-back at constant speed: on a flat road at fixed speed, each timing increase that adds torque forces the throttle to be closed slightly to hold speed. When adding timing no longer needs any throttle reduction, torque has stopped rising (one practitioner's method).
  - Mixture shift with cam changes: with fuel fixed and a correct baseline fuel table, a cam change that traps more air leans the mixture and one that loses air richens it; use that as a sign of a torque gain, then retune fuel (one practitioner's method).
  - Log-based virtual dyno: usable for large changes when inputs and test stretch are identical; measure the spread of 4 to 5 unchanged runs first and treat any change smaller than that spread as undetectable. One practitioner's test found a virtual dyno overstated a 4 degree timing gain by roughly double, and an ECU-integrated estimate read well below the real dyno and misplaced peak torque; another practitioner found one virtual-dyno tool within about 5 hp at about 300 hp. Implausible results (a large jump on an NA engine from a small timing step) mean a setup or data error.
  - Trap speed: a good real-world check for drag cars, but strongly affected by launch; a poor 60 ft time can raise trap speed. Useless if unchanged runs vary by 1 to 2 mph.
- Rotary engines tend to announce detonation by damaging themselves, so road timing on them stays conservative, especially on low-octane fuel.

### Full-load runs on road or track
- Build the map with steady-state work first so the early pulls are already close; then extend runs gradually as on a dyno (methodology/full-load).
- Use 3rd or 4th gear on a long straight, from about 1500 to 2000 rpm to near the limit. 2nd gear accelerates too fast to load the engine and promotes wheelspin, and a turbo engine in a very low gear makes less boost than in normal use; higher gears end at unsafe speed. On track, pick the highest gear whose terminal speed still suits the braking zone.
- Do not edit maps while driving. Concentrate on driving, glance at a windscreen-mounted wideband (and boost on a turbo car), listen with audio knock equipment, and lift immediately if the mixture strays or knock is heard. Mark events with a log marker or hotkey. Make changes parked, from the log, comparing measured with target lambda at the cells the cursor shows. A passenger can operate the laptop.
- Check three things on each pull: lambda tracking target, no knock, boost not exceeding target. Compare peak MAP with the dyno before comparing lambda; if boost matches, the fuel data is comparable.
- Leave closed loop on as a safety net if it is normally active, and read measured lambda and trim together.
- Errors from single road logs often overshoot when corrected in full: apply a little less than the indicated error and expect two or three iterations.
- Public-road WOT pulls are only for low-power cars within limits; powerful cars belong on a closed road or track.

### Confirming a dyno tune
- First log cruise and transition areas (typically about 1500 to 4000 rpm, from closed throttle to the start of boost), dwelling as long as possible in each cell; then sample high-rpm part throttle loosely, erring rich; then do WOT pulls replicating the dyno ramp.
- Expect small differences: in the sources, WOT lambda moved by about 2 to 3 % between dyno and road in either direction, the spool-up zone needed most of the refinement, and on-boost cells usually matched within about 1 %. Light-throttle cells the dyno could not reach were found 10 to 17 % rich in one demonstration.
- Check drivability, boost compared with the dyno, and any knock that did not appear on the dyno. A dead-flat dyno boost curve can be higher, lower or less stable on the road.
- Real-world airflow can push long-term adaptive trims a few percent; driving with long-term learning enabled for a period and folding the learned values back into the base table reduces the work closed loop has to do. Halve or scale learned corrections in sparse, extrapolated cells before applying them.
- A dedicated race car may skip road confirmation and be verified at the circuit with logging instead.

## Decision rules
- Drive a few minutes before adjusting, and again after every stop.
- Use smooth throttle changes to keep enrichment out of the data.
- Stop if brakes fade or smell hot, and let them cool by moving, not by stopping.
- Treat MBT as unknown without torque data: limit timing by the knock-margin approach and stay conservative.
- Road safety outranks data. Never watch a laptop during a pull; never edit while driving.
- Do the ten-step process on a road car too, adapted to conditions.
- Accept 1 to 2 % from target; chasing a perfect lambda wastes time.
- Confirm any dyno tune in real driving.

## Data gates
- Same as methodology/data-quality, plus road conditions noted.
- Coolant and intake temperature back at normal running values before the log segment used.
- Throttle steady and no gear change in samples used for steady-state correction.
- For WOT corrections: peak MAP comparable with the reference run, no wheelspin, knock channel clean.

## Worked example
A log shows a clean pull except where a bend forced a lift. Only the clean part is used.

A track pull modelled on a training demonstration: a third-gear run from 2000 rpm to the limiter shows peak boost 197 kPa, matching the dyno. A lean spike appears as the throttle opens, then from 4000 rpm lambda reads about 0.74 against a 0.77 target, closing to within 1 % by 6800 rpm. The tip-in spike is a transient-fuel issue, not the base table. The on-boost richness (about 3 %) is safe but differs from the dyno, which is the reason for the road check. With boost confirmed first, the tuner removes about 3 % at 4000 to 5000 rpm and about 2 % at 5500 to 6500 rpm over the active boost rows, then re-logs.

## Disputed / conflicts
- Is a dyno needed for ignition? Most of the training material says MBT cannot be found on the road and recommends hiring dyno time for ignition. One session argues that for stock-like engines on pump gasoline, knock rather than MBT sets maximum advance, so road tuning with a margin below knock can equal dyno work; it agrees a dyno is needed for heavily modified engines or high-octane fuels such as ethanol blends or race fuel, where MBT may be reachable before knock. The discriminating test is whether the engine reaches knock before torque stops rising.
- Virtual dyno accuracy: one practitioner found a log-based tool within about 5 hp of a hub dyno; another's test found tools overstated gains and misplaced the curve. Both agree that only consistency between identical runs is usable; neither supports small-step timing decisions.
- Gear for turbo road pulls: most sources use 3rd or 4th; one session prefers 4th or 5th to get longer sustained high-load runs as a worst case. Speed limits and venue decide.
- Ram air: possible with a sealed forward-facing intake at high speed, but one practitioner's view is that it rarely affects the tune in practice.

## Citations
- practice: Practitioner training and tuning practice, distilled and cross-checked.
