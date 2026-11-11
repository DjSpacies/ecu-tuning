---
id: methodology/overrun-fuel-cut
title: Overrun and fuel cut
layer: L2
status: draft
confidence: medium
sources: [practice]
verified: 2026-11-11
applies_to: {fuels: [gasoline, ethanol, methanol], engines: [all]}
depends_on: [methodology/closed-loop-fuel, methodology/idle, methodology/transient-tuning]
supersedes: []
---

# Overrun and fuel cut

## Claim
Overrun (closed throttle above idle) is a choice between cutting fuel and fuelling it deliberately. On road cars, overrun fuel cut sidesteps a region that is hard to tune, saves fuel and prevents exhaust popping, provided entry, exit and recovery thresholds are set so the engine neither hesitates on light throttle nor stumbles back into idle. On hard-driven track cars and rotaries, some tuners leave overrun fuelled slightly rich so the chamber and housings cool before the next full-load phase. Either way, lambda read during fuel cut is air, not mixture, and must be excluded from analysis and from closed-loop correction.

## Why (derivation)
- With no injection, the wideband sees air and reads its lean limit. A closed-loop system that responds adds a large rich correction just as the throttle reopens, which disturbs drivability.
- Overrun cells cannot be held on a dyno: rpm drops to idle as soon as the throttle shuts, so these cells seldom get proper attention. Too rich costs fuel; too lean produces erratic overrun, rough tip-in transitions and exhaust popping.
- Popping on deceleration needs unburnt fuel and air reaching the exhaust. Fuel cut prevents it; disabling cut, or mistuned overrun fuelling, allows it. Cam overlap is not the main cause.
- After injection stops, the engine briefly burns the residual port wall film. On resumption the film must rebuild before combustion is fully re-established, so there is a short lean dip, the same mechanism as tip-in enleanment (principles/fueling/transient-fuel-film).
- On track, high-rpm vacuum cells are visited only on lifts, gear changes and braking downshifts, not in cruise. Fuelling them slightly rich carries heat away, so the engine is cooler when full load resumes. Genuine cruise rarely exceeds about 3500 rpm, so the economy cost is small.

## Assumptions
- The ECU has an overrun fuel cut with rpm, throttle (or pedal) and delay conditions, and a closed-loop lockout during cut.
- Port or direct injection with a usable minimum pulse width in the overrun region if overrun is to be fuelled.

## Breaks when
- **Cut disabled.** Then the overrun region must be tuned like cruise, or deliberately rich for track use.
- **Recovery too close to idle.** With the clutch in, rpm falls fast. The time taken to resume injection and re-wet the port leaves a lean dip that drags rpm below idle: stumble or stall when coming to a stop.
- **Throttle threshold too high.** Cut then switches on with the driver's foot still resting lightly on the pedal, producing a puzzling hesitation during gentle deceleration with a trace of throttle. A cable throttle's closed reading can wander by 0.1 to 0.2%. With drive-by-wire, the butterfly also moves for idle control, so the pedal is the right signal.
- **Function interactions.** On some firmware, an active overrun cut has overridden cruise control or anti-lag because the pedal was at zero. Check whether cut is engaging when those functions misbehave.
- **Injector at minimum pulse width.** Overrun cells that stay about 20% rich even after removing 20% fuel suggest the injector has reached the bottom of its controllable range, where smaller table values no longer reduce the fuel delivered. That is an injector sizing issue, not a table issue. Many near-stock combinations do hold target to closed throttle.
- **Emissions.** Deliberate overrun fuelling is inappropriate where emissions matter; that is why OE calibrations use deceleration fuel cut.

## Practical use
### Fuel cut on (road cars)
- **Entry rpm** about 500 to 800 rpm above target idle, with hysteresis (one example 100 rpm). Examples: re-enable around 1600 rpm for a 1000 rpm idle target. OE-style deceleration cut typically restores fuel about 500 to 600 rpm above idle.
- **Entry delay** about 200 to 500 ms so that fast gear changes under hard driving do not each trigger a cut.
- **Throttle threshold** within roughly 0.1 to 0.2% of the logged fully closed reading (log it on road, track or dyno). With drive-by-wire use 0% pedal.
- **Torque smoothing.** Where available, ramp ignition toward a retarded target (one example: about 10 degrees ATDC at 30 deg/s) before cutting fuel, and ramp it back on exit. This softens the step in engine braking on entry and the torque return on exit. Many ECUs simply step the timing.
- **Before enabling cut**, tune overrun lambda with cut disabled anyway, then enable it. Any error then shows only briefly entering or leaving cut.
- **Lift-off jerk.** Bucking only on throttle lift is not normal. It usually comes from other faults in the map rather than deceleration enleanment, though a very rich lift-off mixture can cause erratic combustion.
- **Pops and bangs on deceleration.** Usually mistuned overrun fuelling: enable cut, or tune the lowest reachable load cells accurately and extrapolate into the unreachable ones, using road logs approaching overrun.

### Fuel cut off (track cars, rotaries)
- Target about lambda 0.95 (an AFR near 14.0 on gasoline) in high-rpm vacuum cells, from roughly 4000 to 5000 rpm upward (one turbo example 6000 to 8000 rpm), with cut disabled so the injectors actually fire there.
- Rotaries: fuelling (or enriching) the overrun lets EGT drop more quickly while braking, so the following full-throttle burst begins from a lower temperature. Keep cut for street economy.
- On a gentle road car leave these cells near lambda 1, or use cut. Overrun cut usually has an activation delay, so on track it sees little use anyway.

### Filling unreachable cells
Extrapolate the general shape of the fuel table into the unreachable dead zones. An outlier at fully closed throttle and lowest MAP is not worth chasing if cut will be active there.

## Decision rules
- With overrun fuel cut in use, mixture inside the cut region does not matter; exclude those samples.
- Without cut, keep cruise-like lambda (road) or about 0.95 (hard track use, rotaries).
- A drivability surge on tip-in after lift points to closed-loop trims reacting to cut samples and to the fuel-cut recovery settings.
- A stumble or stall coming to a stop points to the recovery rpm being too close to idle.
- A hesitation on very light throttle while slowing points to the throttle threshold being too high.

## Data gates
An overrun or fuel-cut status channel is needed. Otherwise infer cut from a closed throttle (or 0% pedal), rpm above the entry threshold and lambda pinned at the sensor's lean limit, and say that it was inferred. Logging overrun state, ignition angle and pedal together verifies the entry and exit sequence.

## Worked example
A road log shows lambda at the sensor maximum for 2 s on a closed throttle at 3000 rpm. Those samples are overrun cut, not lean running, and are excluded. On the next stop, rpm drops from 1500 to 800 rpm (idle target 900) about 0.3 s after the clutch goes in, and the overrun status shows cut ended at 1100 rpm. Recovery is only 200 rpm above idle; raising it to about 1500 to 1600 rpm (600 to 700 above idle) with 100 rpm hysteresis gives the film time to rebuild before rpm reaches idle.

## Disputed / conflicts
- **Cut versus fuelled overrun.** Road and OE-quality drivability advice (056, the course AFR lessons) favours cut. Track and rotary advice (062, 065, 066, 258, one course lesson) favours fuelled overrun near 0.95 for cooling, with cut disabled. One `practice` session gives the same split: cut on street cars, optional on race cars. The cooling benefit is stated, not measured; a discriminating test would compare EGT or coolant and oil temperature at the start of the next full-load phase with and without cut over repeated laps.
- **Recovery margin.** Sources quote 500 to 800 rpm (056) and 500 to 600 rpm (348) above idle; these overlap. One idle session sets resume at 1600 rpm for a 1000 rpm idle (600 above).

## Citations
- practice: Practitioner training and tuning practice, distilled and cross-checked.
