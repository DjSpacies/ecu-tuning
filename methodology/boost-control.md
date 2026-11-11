---
id: methodology/boost-control
title: Boost control tuning
layer: L2
status: draft
confidence: high
sources: [practice, engineering-texts]
verified: 2026-11-11
applies_to: {fuels: [gasoline, ethanol, methanol], engines: [turbo, supercharged]}
depends_on: [methodology/full-load, principles/boost/compressor-and-surge, principles/boost/exhaust-back-pressure, principles/control/feedback-and-pid, methodology/engine-protection]
supersedes: []
---

# Boost control tuning

## Claim
Boost control is first a feed-forward job and only then a feedback job. Prove the mechanical wastegate system gives a smooth, repeatable curve at spring pressure, build a base duty table that puts boost close to target with no feedback at all, and only then add closed-loop correction. Raise boost in small steps with fuel and timing extrapolated conservatively ahead of the step, with an overboost protection set before the first boosted run, and treat a flat dyno trace as necessary but not sufficient: the controller is proven only on the road or track, through shifts and throttle re-application.

## Why (derivation)
### What sets boost
Compressor and turbine share a shaft, so boost follows shaft speed, and the wastegate caps shaft speed by bypassing exhaust around the turbine. The valve is held shut by its spring plus any pressure fed to the dome (top port) and pushed open by boost on the diaphragm (bottom or side port) and by exhaust pressure acting on the valve face. A three-port solenoid controls how much of the boost signal reaches the opening side, so it can only add boost above the level the spring alone holds. Three consequences run through every record:
- The spring sets the floor. Electronic control cannot take boost below it, and cannot open a gate that physically lacks flow.
- The ceiling is set by exhaust pressure on the valve and by solenoid authority. The sources report one three-port solenoid on a soft spring reaching roughly two to four times spring pressure, less with a small, high-back-pressure turbine, and limited by the solenoid itself on a large, free-flowing one.
- Real spring-only boost is not the spring rating. A large, low-back-pressure turbo gives less opening force, so a spring can hold more than its rating (an practitioner example: a 7 psi spring holding about 10 psi); a restrictive turbo opens the gate nearer the rating, and high-rpm back pressure on a small turbine pushes the gate open so boost tapers.

### Why the plant keeps moving
The duty needed for a given boost is not a property of the engine alone. The sources show it shifting with:
- Exhaust heat. A run from a cold, idled exhaust spools lazily; an immediate repeat, or one after a short hold at moderate boost, comes on noticeably earlier (one demonstration: 500 to 800 rpm earlier, with higher peak boost).
- Load and ramp rate. Low gears sweep rpm quickly at light load and undershoot; tall gears and uphill running approach steady state, put more energy into the exhaust and overboost.
- Air density. Cold, dense air makes more boost for the same duty (one practitioner's experience: about 1 to 2 psi), and baro changes move the turbo operating point.
- Ignition timing. Heavily retarded timing sends combustion energy into the exhaust and inflates boost; several demonstrations show high-rpm creep shrinking, and boost sagging slightly while torque rises, as timing moves toward MBT.

Open-loop duty therefore fixes duty, not boost: it behaves like an electronic bleed valve whose result drifts with all of the above.

### Feed-forward plus feedback
The sources repeatedly compare the base duty table with the main VE table and the closed-loop terms with lambda trim. If the base duty already gives target, feedback only trims a small residual, recovers quickly after a throttle lift because it restarts from the right duty, and overshoots less. Each term has a characteristic failure:
- Proportional: faster response; too much and duty swings between its limits while boost cycles around target.
- Integral: removes residual error but acts on history, so it lags feed-forward errors and winds up when a target is physically unreachable, then overshoots when the turbo finally responds.
- Derivative: damps a fast rise; too much slows the approach.
The wastegate, its hoses and the turbo add latency, so large corrections close to target make the system chase itself into oscillation whether the corrections come from gains or from a hand-built table.

### Solenoid behaviour
Common boost solenoids have dead bands: little or no effect below roughly 10 to 15 % duty and essentially fully open above roughly 85 to 90 %, so the useful range is the middle. Drive frequency must suit the valve: the sources run common three-port units between about 15 and 35 Hz, with 20 to 30 Hz the most quoted. Too high and the valve stops following; too low and an atmosphere-vented gate audibly pulses and boost oscillates even when the logged average looks flat.

## Assumptions
- The wastegate is sized and placed for the turbo, the solenoid is plumbed to its instructions, and what 0 % duty does is known and tested.
- Fuel and ignition are tuned at the current boost level before boost is raised.
- A boost limit or cut is configured, set conservatively, and its existence is remembered.
- The MAP sensor and the fuel and ignition load axes extend above the boost target, so a spike lands in tuned cells rather than clamping at the last row.

## Breaks when
### Mechanical faults no calibration can fix
- Creep: on spring alone, boost keeps climbing with rpm (in bad cases quoted in the sources, from mid-teens psi at gate opening to the mid- to high-20s by 7000 rpm). Causes include an undersized gate or a poor take-off: exhaust resists turning, so an practitioner rule of thumb treats a take-off angle beyond about 45 degrees as poor and near 90 degrees as almost certain to creep.
- If boost already exceeds target at zero duty, no table change will fix it; the hardware must change.
- Wrong solenoid plumbing or inverted output: the first run meant to be at minimum boost can deliver the system's maximum. Without a working gate a turbo can make enough boost to damage an engine and overwhelm traction.
- Long reference hoses (around 2 m in one practitioner's view) add lag; within reason length matters little.
- Maximum duty still short of target: the spring preload or solenoid authority is the limit, not the table.
- A small factory turbo tapering at high rpm, or a mechanical mid-range dip, at a duty already near the upper dead band: accept it or change hardware.

### Conditions that mislead the tuner
- An unreachable low-rpm target winds up the integral and causes overshoot when the turbo lights.
- A conservative, heavily retarded base ignition map inflates boost; creep seen early may vanish once timing is set.
- Unrealistic dyno ramp rates make more or less boost than the same gear on the road.
- A cold versus heat-soaked exhaust changes spool between otherwise identical runs.
- A rally-class inlet restrictor dominates the achievable boost curve; know whether one is fitted.

### Controller and software behaviour
- During a shift cut, torque drops and a closed-loop controller drives duty up, giving a spike when power returns.
- At part throttle the controller shuts the gate harder to hold target, so full boost can persist down to roughly half throttle and pedal-to-torque becomes very non-linear.
- Some ECUs target gauge pressure and others absolute; entering absolute habits into a gauge-target strategy asks for about 1 bar too much, and error is computed against measured baro, not an assumed 100 kPa.
- Some ECUs scale boost limit tables as a percentage of the span between the activation pressure and the main target, not as an absolute pressure or a cut.
- Staged strategies (a fixed spool duty, then a near-target stage, then fine control) can latch the last duty or stay in an early stage if the next stage is not enabled or the target is never approached; read the duty trace against the stage thresholds before blaming hardware. In one ECU's firmware of the time, the derivative term snapped to zero the instant boost reached target, abruptly restoring duty and causing overshoot.
- Some ECUs apply a boost-error duty correction even in open-loop mode, which must be zeroed when building the base table.

## Practical use
### Before the first boosted run
- Check the plumbing against the solenoid's instructions so that de-energised gives spring pressure. Several practitioners estimate that most customer or owner-built cars arrive with boost control plumbed wrongly (anecdote, but consistent across sources), and it is far easier to fix before the exhaust is hot.
- Check output polarity: what 0 % duty does physically. One practitioner's drag car ran far above its intended boost after a software update changed that sense, and lifted the head.
- Test the output with a PWM test and listen for the valve; temporarily lowering the frequency makes the click easier to hear.
- Zero every duty table and every boost trim (coolant, air temperature, gear, error correction). Base files sometimes hold 85 to 100 % duty, which would request maximum boost. Inspect trims for stray values and remember they interpolate: a full cut at 110 C already removes about half the duty at 105 C.
- Set the boost cut around or just above spring pressure until control is proven, then raise it. If the engine seems to misfire suddenly while boost is being raised, suspect that conservative cut.
- Set activation thresholds so the solenoid is not pulsed in vacuum or cruise (examples in the sources: around 2000 rpm and 100 to 105 kPa absolute), but well below any requested boost. A MAP threshold above what spring pressure reaches means control never activates; an activation too close to target leaves no time to manage the approach and causes overshoot. On a laggy turbo there is no reason to drive the solenoid below the rpm where boost can build.

### Step 1: spring-pressure baseline
Run with zero duty, in a fairly high gear, at a realistic ramp rate. Read the curve:
- Flat, or gently tapering at high rpm on a small turbo: the hardware is controllable.
- Climbing with rpm (a mountain shape): creep, a mechanical problem. Stop and require hardware changes.
- Erratic or unrepeatable: hardware or plumbing.
Tune fuel and ignition fully at this lowest-stress boost level first; it also tells you how much duty the target will need (little if spring is near target, much more if the spring is half the target).

### Step 2: build the base duty table
- Make a first flat, moderate duty change (examples in the sources range from 10 % steps up from zero to a flat 15 to 25 %), measure the boost change, and scale the next step from that sensitivity. There is no general duty-to-boost conversion; it depends on spring, turbo, gate count and position.
- Expect nothing until past the lower dead band, and do not waste time adjusting values inside either dead band.
- Use the log cursor to find which rpm and duty cell was active at each error before editing. Add duty where boost lags, leave on-target cells alone, trim a percent or two where it overshoots, and ramp duty up with rpm where boost tapers. Where boost deviates between breakpoints, insert a breakpoint (interpolate it first so nothing changes) and adjust it.
- Where the ECU allows, index base duty by boost target and rpm so it follows target changes; for a higher target, estimate a higher duty from the trend and interpolate.
- Raising duty below the boost threshold to hold the gate shut speeds spool only modestly (one practitioner measured 100 to 200 rpm, not the 500 to 1000 often claimed). The danger is a high-load gear or a long hill reaching target while duty is still high, giving a large overboost. End the high-duty region before the rpm where target is reachable in the worst-case gear, or make it MAP-dependent.
- Set duty to zero in idle and off-boost cells so an open-loop solenoid does not tick needlessly.
- Aim for open-loop boost within a few kPa of target, ideally 1 to 2 kPa, before adding feedback.

### Passive closed loop (measured MAP on the duty table axis)
Put measured MAP on the second duty axis with breakpoints clustered around target, copy the tuned row across, then reduce duty progressively above target and add a little below. An overshoot moves the operating cell to lower duty and pulls boost back without any gains. Keep near-target steps small (about 0.5 to 1.5 % within 5 kPa in the sources), larger further away, slightly more aggressive on the overboost side, and zero duty at a clearly unsafe pressure as a backstop to the cut. If boost bounces, shrink the near-target steps first. If corrections larger than about 3 to 4 % seem necessary, the base table is wrong. This works only as well as the base curve under it, and on ECUs whose closed-loop mode uses the target as the duty axis it is an open-loop technique.

### Closed loop
- Start with all gains at zero, tune the base table, then add gains, with an integral clamp and a maximum duty only slightly above what maximum boost needs.
- With no idea of base values, integral-only control slowly walks duty onto target; the settled duty at each point becomes the feed-forward value.
- Log rpm, throttle, MAP against target, final duty and each P, I and D contribution. The gap between feed-forward and final duty shows how wrong the base table is: raise or lower the base toward the final duty (plus a little if boost was still short) and iterate until they agree within about 1 %. Minimal P and I effort while on target means the base is right.
- In staged strategies, switching from the spool stage too late lets the turbo carry momentum past target (one demonstration: a 210 kPa target overshooting to 236 until the switch was moved earlier and base duty lowered). Use hysteresis between stages, and start with a wide margin; a tight margin drops in and out of control erratically.
- Use the least input filtering that settles noise; too much slows response.
- Gains belong to one engine and turbo combination and do not transfer. Judge them with deliberate target steps (for example plus and minus 10 kPa at fixed rpm) as well as ramps.
- Per-gear gains add complexity few can manage; differences between gears are better handled with gear-dependent base duty.

### Trims and boost strategies
- Gear: leave dyno-like middle gears at zero, add duty in low gears and pull in the top gears, built from road logs, not first-gear dyno runs. A larger turbo may never reach target in first gear whatever the duty.
- Air temperature: zero across the range the car was tuned in, pulling duty progressively in the cold to stop winter overboost.
- Coolant (and high air temperature) trims as protection: drop toward spring pressure when the engine is very cold or overheating, alongside other protections.
- Baro: add a baro axis or compensation where altitude changes are large (see `methodology/altitude-and-baro`).
- Throttle position: because full boost persists at part throttle, a turbo engine can still make most of its torque at half throttle. Reducing the target or duty as throttle closes makes torque follow the pedal, which matters most in light, powerful, traction-limited cars.
- Boost by gear, by road speed, or rising within a gear, to match torque to traction; boost by ethanol content on flex fuel; driver-selected boost via a switch or multi-position input.
- Shape the target to the need: lower around peak torque for weak internals, tapered at high rpm when the fuel system cannot support peak boost there, rising with rpm for corner exits on a traction-limited car.
- Controlling on pre-throttle pressure rather than manifold pressure can steady part-throttle control; fuel and ignition still use MAP.

### Hardware range choices
- A common recommendation is a spring a few psi below running boost so the controller can move boost both ways; a spring equal to target leaves no room downward.
- Traction-limited cars need a low floor as much as a high ceiling: a stiffer spring raises both. Keeping a soft spring and adding authority (a second three-port solenoid on the other port, or regulated gas pressure on the dome for very wide ranges) preserves low-gear control.
- Four-port solenoids widen range but are coarse (the sources report a 1 to 2 % duty change moving boost several psi), which makes fine low-boost control and closed-loop stability hard.
- One solenoid serves twin small internal gates; large external gates may need more flow than one valve passes.
- A wastegate position sensor is mainly a fault-finding tool: it shows the gate creeping open before target, which boost pressure alone does not reveal.
- On very high-boost drag cars a controlled blow-off valve can bleed boost in low gears faster than the wastegate can act.

### Validate in real driving
Log road or track runs: in-and-out throttle above the boost threshold, a quick shift at full boost, a mid-corner lift and re-application. Several practitioners report road boost differing from a flat dyno curve in most cars (often lower, sometimes a few psi higher) and overshoot appearing only in these transients. Set the overboost cut with enough margin to avoid nuisance cuts from shift spikes (an practitioner example: 10 to 20 kPa above target, with a short delay and some hysteresis), preferably by fixing the control rather than widening the cut, and road test before handover.

## Decision rules
- Start at minimum (wastegate spring) boost, with a boost cut configured first and all duty and trim tables zeroed and inspected.
- Increase boost by about 20 kPa at a time; 40 kPa steps only with experience and interpolation over the skipped row. Before each step, extrapolate fuel on the rich side and timing conservatively into the rows above, so a misjudged duty change lands in safe cells.
- Make duty changes small, approaching the target from below; the duty-to-boost response is not predictable and an overshoot costs more than an extra run.
- Place a safety backstop in the duty table above the target, and heavy timing reduction in ignition rows past the target, in case boost control fails.
- A target must be realistic for the hardware at each rpm.
- If open-loop boost is not repeatable, stop and fix the hardware before tuning any gain.
- Choose a wastegate spring a few psi (about 5 psi in one source) below the intended running boost unless a low floor is needed for traction.

## Data gates
- Boost repeatable run to run, with the exhaust preconditioned the same way, before tuning at that level; spool-region differences between runs are treated as variation unless repeated.
- No solenoid saturation (duty pinned at either dead band) unaccounted for.
- Open-loop base within a few kPa of target before closed-loop gains are judged.
- At least one road or track log with throttle transients and shifts before boost control is called finished.

## Worked example
A spring-pressure tune is complete and the target is 220 kPa absolute. The first open-loop run peaks at 234 kPa and sits 10 to 12 kPa high above 5000 rpm. Removing 2 % duty above 5000 rpm puts it on target, leaving a dip between the 5200 and 5700 rpm breakpoints; a breakpoint added between them and nudged by about 1 % removes it. A passive MAP axis is then added around a 150 kPa target at 3500 rpm with duty of 51 % at 145 kPa, 50 % at 150, 47 % at 155, 44 % at 160 and 0 at 170, backed by the boost cut.
Before the next 20 kPa step, the fuel rows above are filled from the VE trend of about 3 % per 20 kPa seen in the proven rows, set a little above trend, and timing is reduced ahead of trend.

## Disputed / conflicts
- Open loop, passive closed loop or PID. Several practitioners hold that well-tuned PID is potentially the best and keeps boost consistent across weather, but that most tuners set it up badly and get worse results than a good open-loop table. One practitioner found one ECU's closed-loop strategy overshot 10 to 20 kPa on road and track despite long tuning while looking perfect on the dyno, and switched to the passive MAP-axis table; another prefers plain open-loop duty by gear and rpm on 60 to 100 psi drag cars, accepting weather drift, because a psi or two of overshoot matters there. Discriminating test: road or track tip-in, shift and re-application logs compared against target, not dyno ramps.
- Solenoid frequency. Sources quote 15 to 20 Hz, about 20 Hz, 20 to 30 Hz, 20 to 35 Hz and a 30 Hz start; one practitioner treats frequency as a trade of resolution (higher) against range (lower). The common ground is to stay near the valve maker's figure and listen for pulsing.
- Dead band onset. Most sources put it at 10 to 15 % for common three-port valves; one practitioner says many do little until 20 to 30 %. Measure it on the installation.
- Holding the gate shut below threshold. Some demonstrations show a small mid-range gain from 90 to 100 % duty during spool; one practitioner considers the spool benefit marginal and the overboost risk the main effect.
- Four-port versus twin three-port solenoids: one view uses the four-port for wide drag ranges; another avoids it for its coarseness and uses two three-port valves.
- Spring choice: about 5 psi below target is the usual advice; one practitioner fitted a very soft spring on a high-compression flex-fuel street engine to keep the widest adjustment range, noting a stiffer spring suits lower compression.
- Internal versus external gates at very high power: reports of trouble with modern, properly sized internal gates are second- or third-hand and unconfirmed.
- Textbook cross-check: the combustion textbook shows knock limits depending on charge pressure, temperature and mixture, and the control text covers feedback generally. Step sizes, duty percentages and frequencies here are practice figures from practitioners, not limits.

## Citations
- practice: Practitioner training and tuning practice, distilled and cross-checked.
- engineering-texts: Engine, combustion, charging and control engineering texts.
