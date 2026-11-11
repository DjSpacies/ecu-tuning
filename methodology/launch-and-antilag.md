---
id: methodology/launch-and-antilag
title: Launch control and anti-lag
layer: L2
status: draft
confidence: medium
sources: [practice]
verified: 2026-11-11
applies_to: {fuels: [gasoline, ethanol, methanol], engines: [turbo, na]}
depends_on: [methodology/full-load, methodology/engine-protection]
supersedes: []
---

# Launch control and anti-lag

## Claim
Launch control gives a repeatable start: a held rpm (and on turbo engines a held boost) at the line, then, ideally, a controlled rpm-versus-ground-speed path through first gear. Anti-lag strategies (launch boost building, rolling anti-lag, rally off-throttle anti-lag) make turbine energy by burning fuel and air in the exhaust using an ignition-cut limiter plus heavy retard, and for rally also bypass air. They deliberately trade turbine, manifold, exhaust valve and valvetrain life for response. They must be conditional, time-limited, as mild as the driver accepts, and checked against the valvetrain and turbo they will abuse.

## Why (derivation)
- **Repeatability is the value.** Even skilled drivers cannot repeat the exact rpm and clutch combination every start; the ECU can. A good driver's best manual launches are therefore a data source for the strategy, not a reason to skip it.
- **A fixed rpm cannot match the tyres.** At standstill a locked clutch would demand near-zero engine rpm. Dropping the clutch at, for example, 4500 rpm corresponds in first gear to a wheel speed of about 35 km/h with no slip, far ahead of the car. Either the clutch slips to bridge the gap or the tyres spin. Tyres give peak acceleration at a small positive slip (sources quote 5 to 10%, varying with tyre and temperature), so the target is slight controlled spin.
- **Boost building.** On an ignition-cut limiter, cut cylinders send a full unburnt charge into the manifold. Firing cylinders with timing retarded near or after TDC are still burning as the exhaust valve opens and ignite it upstream of the turbine. A fuel-cut limiter takes away the very fuel the process depends on, so it does little. A large turbo on a small engine that reaches full boost only near 7000 rpm can leave the line on a few psi with a plain limiter and 20 to 30 psi with cut plus retard in the sources' examples.
- **Self-sustaining spool.** As soon as boost begins to rise the turbine sustains itself with less retard, so a fixed retard lets boost keep climbing past target. Retard scheduled against MAP (heavy below target, much less above) becomes a crude boost controller.
- **Rally anti-lag** needs, with the pedal released, extra air getting past the shut throttle, fuel for that air, and timing late enough that burning carries on as the exhaust valve opens. Opening the bypass further offers the turbine more energy, but the engine then needs still later timing to keep its speed and torque in check, and that later timing is what heats the exhaust and turbo, the main way anti-lag does damage.
- **Valvetrain mechanism.** The exhaust pressure pulses lift exhaust valves off their seats. Hydraulic lifters pump up into the gap and hold valves open, killing compression on one to three cylinders until they bleed down (sources: 20 to 30 s). Rocker-type valvetrains can throw rockers, shim-over-bucket heads can spit shims, and some engines bend exhaust valves within a few aggressive launches.

## Assumptions
- Closed course or drag strip use; the user accepts the mechanical cost.
- The ECU supports an ignition-cut limiter and a retard table that can be indexed by MAP, and arming conditions.
- For speed-based launch, a valid ground-speed reference exists (undriven wheel).

## Breaks when
- **All-wheel drive.** No undriven wheel means no ground speed. in one comparison a 10 Hz GPS, and also a 20 Hz unit, lagged an undriven wheel trace too much; one AWD drag car is reported to use 50 Hz successfully. Fall back on a two-step, a cap on how fast rpm may climb once the clutch is released, or accelerometer-based schemes.
- **Clutch switch misplaced.** A factory switch that changes state at the top of pedal travel holds the car on the launch limit while the clutch is already biting: bog or stall. A switch that releases well before the bite shows as an rpm flare before take-up. Both destroy consistency.
- **Small turbo or NA engine.** Retard is irrelevant on NA engines and often unnecessary (just noisy) on small turbos, which make 5 to 7 psi on a limiter from airflow alone. Some ECUs cannot set launch timing above about TDC, which gave excessive popping on a small-turbo engine; there the retard was disabled.
- **Weak parts.** Stock sintered rods bent under a mild rolling anti-lag test in one anecdote. Hydraulic lifters, rocker valvetrains and stock rotary seals are at risk.
- **Lambda is invalid.** With cuts active, unburnt oxygen reads lean (one demonstration: lambda read about 1.13 with anti-lag running, against 1.0 at plain idle). Do not tune launch or anti-lag fuel from lambda.
- **Blow-off valve.** It must be absent or disabled while rally anti-lag is active. On the line at full throttle a blow-off valve stays shut and does nothing.
- **Vacuum brake booster.** Anti-lag removes overrun manifold vacuum; at marginal vacuum the pedal alternates between assisted and rock hard. Some rally cars blank the booster so the pedal is always heavy but consistent.
- **Misfire diagnostics.** Reflash-tuned OE ECUs may correctly flag the deliberate misfires; disabling the code also hides real misfires.
- **Terminology.** Many ECUs call a stationary launch with retard "anti-lag". Rally anti-lag works off-throttle. Check which a feature is, and which retard convention the table uses (see Practical use).

## Practical use
### Two-step (secondary limit)
- Wire and verify the clutch switch (runtime state changes correctly, active edge right for the wiring), and set it to change state right at the clutch engagement point.
- Arm with conditions: throttle above a threshold (examples 70 to 80%), coolant warm (examples 60 to 65 C), below a vehicle speed (examples 2 to 15 km/h disarm), and a clutch arming time (about 1 s) so normal clutch use on gear changes cannot engage it. Disarm when the throttle is almost shut.
- Finding launch rpm on an unfamiliar car: begin near two-thirds of the rev limit and lower it 500 rpm at a time across logged launches. Too high spins the tyres up onto the limiter; too low bogs or stalls, which shocks clutch, gearbox and driveline harder than spin does. So err high. As grip changes through a race day, launch rpm is the setting most worth revisiting.
- Tune the limiter for a flat rpm line. If rpm oscillates over about 200 rpm, the torque available at clutch drop depends on where in the cycle it lands. A too-narrow range (50 to 100 rpm) gives erratic control; wider ranges are smoother but shift where rpm settles. Slider clutches are sensitive even to 50 to 100 rpm variation.
- Exit decay: on turbo drag launches any gradual reinstatement of power after the clutch released caused a bog in one source; zero decay cured it.
- Without a clutch switch, one method uses launch always active with a low disarm speed (about 2 mph); another reduces a speed-indexed launch table to two sites (launch rpm at 0 km/h, normal limit at 1 km/h).

### Ground-speed launch (2WD)
1. Calibrate wheel speeds (tyre circumference, ratios).
2. Log a no-slip run: roll in first gear, clutch fully engaged, accelerate gently to the limiter with zero wheelspin, logging rpm against undriven wheel speed.
3. Multiply each no-slip rpm by (1 + target slip) to get the limit at that speed.
4. Shape the low-speed bridge: the no-slip line is near idle at 5 km/h, so applying it literally pulls the engine down. Hold slightly below launch rpm for the first 0 to 15 km/h, then interpolate up to the slip line from about 20 to 25 km/h. This transition is the main thing to tune with back-to-back logged launches (100 to 200 rpm changes).
5. Above the speed where wheelspin no longer threatens (60 to 70 km/h in first in one example), set values above the main limit so the lowest limit governs. Beyond first gear, traction control takes over (methodology/launch-antilag-tc-traction-and-shift).
- Optimal slip changes with tyre temperature: a setting that worked leaving the pits on cold tyres bogged on hot slicks after formation laps. Keep separate settings per condition.
- With drive-by-wire, a modest throttle cap through first gear matches torque to grip so the limiter works less. A throttle-versus-speed table is open loop and cannot sense bog or grip; copying a driver's erratic throttle trace replays it blindly. Keep any cap broad and flat, at 100% while stationary, and blend back to full opening before first gear runs out.
- Repeatable clutch slip (a hydraulic bleed restrictor, release to full engagement in about 1.5 to 2 s in one practitioner's drag cars) transformed AWD drag consistency in the sources, at the cost of heavy clutch wear (about 10 passes per clutch pack). An rpm rise-rate limit (examples 3000 to 5000 rpm/s) after leaving the two-step stops rpm racing to the main limiter before the plates grab.

### Building and holding launch boost (turbo)
- Use an ignition-cut launch limiter, and only after confirming the valvetrain tolerates it.
- Start with zero or near-normal retard and add 2 to 3 degrees (some use 5 to 6) per test until boost jumps, with audible popping. Use the minimum that reaches target.
- Schedule retard by MAP: little or none below atmospheric pressure (so the car stays drivable while staging and will not stall each time the clutch goes down), heavy as boost builds, reduced approaching target, near normal above it. Combine with wastegate duty (a gear-zero or launch duty row). Timing-based control still wanders by 2 to 4 psi; top drag cars add a charge-pipe wastegate set at launch boost.
- If the launch timing map is heavily retarded the engine is lethargic and struggles to reach the limiter; switch to it only above a throttle threshold and retard only the full-throttle cells above launch rpm.
- Launch boost depends on launch rpm and retard together: raising launch rpm by 1000 rpm added roughly 5 to 8 psi at the same timing in one example, so retune timing when rpm changes. Targets depend on tyre and track (one example: near spring pressure for a modest car, 300 to 350 kPa absolute for a big-tyre prepared drag car).
- Confirm the effect by logging exhaust manifold pressure: spiky pressure (one demonstration: about 108 kPa without retard, spikes near 135 kPa with about 20 degrees retard) is the signature of combustion in the manifold.
- Launch fuel: several practitioners never add any, because the heat of a launch lands mainly in the turbo and manifold rather than the chamber, and cut cylinders pass a cooling charge. Add fuel only if EGT monitoring suggests it.
- Exposure: do not sit on retard-based launch for long. One practitioner allows about a minute of cooling between development tests and warns against holding it 30 to 45 s. Watch EGT approaching 950 to 1000 C.

### Rolling anti-lag (roll racing)
- Same principle as launch boost building, held at a rolling speed on a momentary button. Releasing the button restores timing and the car leaves already at 20 to 30 psi.
- Arm only with gating (throttle under roughly 40%, coolant over roughly 60 C, optionally a minimum speed), lock the current rpm or speed as the limit, use a separate boost target and a MAP-indexed retard table, show armed state clearly on the dash, and allow instant disarm. An rpm bump per button press lets the driver match the other lane after arming.
- One practitioner considers it easier to control than brake boosting and likely kinder to the engine, since brake boosting adds heat.

### Rally (off-throttle) anti-lag
- Air: a bypass solenoid, throttle kicker, drive-by-wire opening or secondary air. The factory idle valve has never flowed enough in one practitioner's experience.
- Sequence for initial tuning (one practitioner): open the bypass roughly 10% past the normal idle position; retard until the engine settles near 1800 to 2100 rpm with anti-lag on (absolute timing around 15 to 20 degrees ATDC to start; 30 to 50 degrees ATDC is very aggressive); then add random ignition cut of 20 to 50% of events; then optional fuel of 5 to 10% (10 to 15% the most ever needed). Always start mild.
- Arming: require a high throttle reading held briefly (example 80% or more for 100 ms), which keeps it inactive on road sections; enable and mode switches; shutdown on EGT and coolant limits; a timeout (about 5 s without re-arming) so it does not idle building heat after a stage. Keep anti-lag table values only below about 30% throttle so normal operation is untouched. Optional brief cyclic idle cool-down after deactivation (5 to 10 s).
- If EGT runs away: first give back timing, then trim bypass to suit, and only then add fuel. Extra fuel by itself will not hold EGT down in an aggressive setup, so a fuel-only EGT control loop is unlikely to work. Validate with a pre-turbine probe on a real stage; a dyno cannot reproduce stage-like anti-lag loading for long enough. Post-turbine EGT cannot be translated because the temperature drop over the turbine differs from one turbo size to another. Use encased probes; exposed ones lasted only a few meetings and the two types read 80 to 100 C apart.
- Driver calibration: strong anti-lag keeps driving the engine with the pedal up, so engine braking disappears and the car runs wide on entry. Ask the driver whether response improved and whether entry push is excessive. Novices want milder settings; drive-by-wire allows switchable maps.
- Cyclic (rotational) idle is only a way to control idle when the bypass is fixed. With drive-by-wire or a bypass solenoid it is not needed, and customers who wanted it for the sound usually asked for it removed because the low-throttle transition is jerky in traffic.
- Proving function: turbo shaft speed that recovers or holds off throttle (one dyno test held at least about 40,000 rpm after an 81,000 rpm peak) and positive pre-throttle pressure. Manifold pressure shows reduced vacuum, not boost, so expecting 5 to 10 psi plenum boost off throttle is a myth.
- A good anti-lag improves boost threshold slightly and lag substantially (one practitioner: 500 to 600 rpm extra usable band).
- On a circuit car with a turbo already suited to the engine, one practitioner judges the reliability cost (turbos consumed, cracked manifolds, stretched valves, blown pre-turbo gaskets) outweighs a small benefit; it pays in rally, where a driver can end up a gear too high.

### Retard table conventions
ECUs express retard as degrees subtracted from base, as absolute final timing, or as a percentage of base timing removed (values above 100% go after TDC: from a 30 degree base, -200% gives 30 degrees ATDC). Some launch timing tables are absolute replacement maps, others are trims. Confirm the convention and check the resulting final ignition angle in a log before running; misreading it gives dramatically wrong exhaust temperature and boost. Absolute mode is easiest to read.

## Decision rules
- Require arming conditions: throttle threshold, warm coolant, speed limit, clutch arming time.
- Use ignition cut for turbo boost building only when the valvetrain is proven (solid lifters, adequate springs); otherwise use fuel cut and accept less boost. For hydraulic-lifter engines that need retard launch, the sources convert to solid lifters; heavier springs by themselves may not prevent pump-up.
- Schedule retard by MAP, not as a fixed value.
- Keep launch and anti-lag events short; monitor pre-turbine EGT.
- Ignore lambda during launch and anti-lag; base enrichment on EGT.
- Log ignition angle against table timing, cuts and launch state every time.

## Data gates
Log rpm alongside the active rpm limit, MAP against boost target, exhaust manifold pressure if fitted, wastegate duty, gear, driven and undriven wheel speed, launch armed and active states separately, ignition and fuel cut %, launch ignition and fuel trims, final ignition angle against table ignition, clutch switch (and clutch position if fitted), throttle, coolant, IAT, EGT and lambda (flagged invalid during cuts).

## Worked example
**Slip table.** The no-slip log shows 5000 rpm at 40 km/h in first. For 10% slip the limit at 40 km/h is 5000 × 1.10 = 5500 rpm. At 50 km/h with a no-slip 6200 rpm, the 10% limit is about 6800 rpm (one source chose 6600 to 6700 after testing). Launch rpm is 4500; hold 4300 rpm from 0 to 15 km/h, then interpolate to the slip line by about 25 km/h.

**Launch boost table.** Target 250 kPa absolute. MAP-indexed launch trim: 0 degrees below 90 kPa, -10 degrees at 95 kPa, -20 at 105 kPa, about -32 through the spool region, easing to -28 above 260 kPa so timing returns and boost settles near target. Earlier, with a fixed 30 degree retard, boost climbed past target every launch.

## Disputed / conflicts
- **Launch fuel.** One live training session (`practice`) logged lambda near 0.83 on the launch limiter where 0.79 was targeted and added about 15% launch fuel (also to cool the exhaust), alongside more retard. Most course and session practitioners (`practice` 060, 104 and the launch-control sessions) say lambda cannot be trusted with cuts active and that launch fuel is seldom needed; they would base it on EGT. Discriminating test: pre-turbine EGT and boost with and without the added fuel.
- **Launch limiter cut type.** Several sources default to fuel cut for launch on fragile valvetrains and NA engines; others prefer ignition cut generally for launch, and turbo boost building requires it. Agreement: ignition cut only where the valvetrain is proven.
- **Rolling anti-lag versus brake boosting.** One practitioner's view that rolling anti-lag is easier on the engine; no measurement offered.
- **Speed-based launch versus two-step.** The `practice` launch sessions prefer ground-speed launch for 2WD. An `practice` session notes a 3D launch table on throttle and driven wheel speed can act as a speed-dependent limit without traction control sensors where rules ban traction control. Both agree a true slip-based limit needs an undriven reference.
- **Exit decay.** Zero decay cured launch bog in one source; the same source found some decay extended sequential gearbox life on shift cuts. The two are different functions, not a contradiction.

## Citations
- practice: Practitioner training and tuning practice, distilled and cross-checked.
