---
id: methodology/launch-antilag-tc-traction-and-shift
title: Traction control, torque delivery and shift cut
layer: L2
status: draft
confidence: medium
sources: [practice]
verified: 2026-11-11
applies_to: {fuels: [gasoline, ethanol, methanol], engines: [all]}
depends_on: [methodology/launch-and-antilag, methodology/engine-protection]
supersedes: []
---

# Traction control, torque delivery and shift cut

## Claim
Usable tyre torque is set by surface, gear and driver, so delivered engine torque should be shaped to it (boost by gear or speed, throttle caps, timing trims), with slip-based traction control as a backstop rather than the primary controller. Shift cuts exist to unload gearbox dogs (or ease a clutched shift on a turbo engine). The cut must last until the gear is engaged and no longer, which closed-loop gear-position feedback achieves and timed cuts only approximate. Torque return after a cut should be ramped to keep the tyres hooked.

## Why (derivation)
- **Slip.** Slip is how far, in percent, the driven wheels run ahead of the undriven (ground) speed. The ECU can convert ground speed through tyre circumference, gear and final drive into the rpm the engine should be at, add the slip target, and cut when actual rpm exceeds that limit. Wrong ratios or circumferences shift the calculated slip directly.
- **Reaction versus prevention.** Traction control acts only after spin starts. Mid-corner at speed, a short burst of wheelspin may be enough to lose the car, and frequent cuts are hard on the crank and driveline. If power far exceeds grip, traction control must intervene so much that it is rough and sounds awful. Matching torque to grip lets it merely trim.
- **Actuator speed.** Cuts take effect on the very next firing event. Retard is also quick and powerful, but it drives EGT up, more so on a turbo engine leaning on it heavily. Boost reduction is too slow for traction control, though good for planned torque shaping. Throttle closing has proven too slow or imprecise for top-level traction control in the sources' testing.
- **Positive feedback with an rpm axis.** A boost duty table indexed on rpm adds duty when wheelspin flares rpm, which adds boost and more spin. Indexing on undriven wheel speed (and gear) avoids this.
- **Dog engagement.** Dog faces are back-cut, so transmitted torque pulls them into engagement and no lever force can pull the gear out under load. Any shift needs a brief torque reversal: a cut for a power-on upshift, a throttle blip for power-off shifts (which on a downshift also matches revs). A cut that ends before the next gear is fully engaged reapplies torque to partly engaged dogs and rounds or breaks them. An over-long cut costs only shift time. Slow, hesitant shifts round dog edges over time and cause jumping out of gear.
- **Turbo flat shift.** A lift shuts the throttle, vents boost via the blow-off valve, and shaft speed falls, after which the intake has to be filled again. Staying at full throttle and cutting ignition sacrifices a little exhaust energy yet keeps shaft speed up, and the larger the turbo is for the engine, the more this is worth. Gains on NA engines with synchro boxes are small and partly psychological.

## Assumptions
- Calibrated wheel speeds: at least one driven and one undriven source for slip control, ideally all four wheels.
- A torque-reduction model in the ECU, so traction, launch and shift functions know what each reduction removes and do not fight.
- For closed-loop shift cut, a gear barrel position sensor logged fast enough to see shift completion (one source: 500 Hz).

## Breaks when
- **All-wheel drive.** No true undriven reference; slip control works less well. Wire all four wheels, or use longitudinal acceleration from an accelerometer as a grip proxy, or rpm rise-rate limits.
- **Open differential.** Only the unloaded inside wheel may spin, which one driven sensor can miss; using the fastest driven wheel makes slip worst-case. The outside undriven wheel turns faster in corners; a second undriven sensor preserves the reference when one wheel locks under brakes. One sensor on the driveshaft or diff input can replace a pair of driven-wheel sensors.
- **Wheel changes.** Staggered or changed tyre sizes and wet tyres change circumference; update them every time.
- **Synchromesh boxes.** Shifting a synchro box clutchless gains nothing, engages poorly and eats the synchro cones. Shifting much above about 9000 rpm is difficult. A strain gauge lever is not usable; keep using the clutch and let the ECU only manage engine speed.
- **Clutch-switch shift cut on a circuit car.** Without a throttle lockout the cut also fires on clutched downshifts and stops the driver blipping to match revs.
- **Over-long maximum cut.** If the gear sensor fails, a maximum of 1000 ms makes a horrendous shift; one source uses about 150 ms where shifts normally complete in 40 to 80 ms.
- **Limits of electronics.** Rpm takes time to fall, so a quick enough shift engages before the engine has slowed to the new gear speed; a lighter flywheel helps, nothing else can.
- **A 100% cut that does not release the dogs** means the cut is probably not happening as configured; verify in logs.
- **Pedalled drag runs.** Once the driver pedals, the data no longer cleanly show what upset the car; do not draw boost-map conclusions from them.
- **Slipper and slider clutches.** Changing delivered power changes clutch lock-up, so ECU power changes confound clutch tuning.

## Practical use
### Torque shaping first
- **Boost by gear or speed.** Step boost up through the gears (one drag example rose from roughly 1.5 bar at the line to roughly 3.1 bar in the top gear, in steps of 0.3 to 0.7 bar per gear), review every pass for rpm blips revealing spin, and nudge each gear up until just short of spinning. Vehicle speed may suit automatics better. On high-power FWD, slow the boost ramp so the full figure comes in higher up the rev range.
- **Big turbo, traction-limited low gear.** Keep boost up and remove torque with ignition timing (examples: about 8 to 12 degrees pulled in second), so the turbo is spooled for the next gear and the shift does not drop boost. Only for brief periods; retard dumps heat into the exhaust and is not for a whole circuit lap. Add a time-since-launch retard table for finer control around 60 ft.
- **Throttle caps (drive-by-wire).** Selectable maximum-throttle tables on rpm and pedal: cap opening around the torque peak (for example 60% at 3500 to 4000 rpm) and allow 100% once torque falls off. A gentler pedal progression for wet maps helps. When the wastegate cannot lower boost further (creep), throttle caps are the only way to reduce power. One wet race car combined a five-position switch driving a boost multiplier and a pedal-translation table, and a fallback position chosen for a failed switch signal.
- **Driver switch presets.** Boost, launch rpm and slip targets change together between wet and dry, so tie them to one multi-position switch with an off position. Group only functions that change for the same reason.
- **Driven blow-off valve as a power lever.** Holding an ECU-driven blow-off valve open roughly halved power on one drag car in a test; a strong, fast lever where traction is limited.
- **Torque capping for weak parts.** Reduce boost or throttle around peak-torque rpm to cap cylinder pressure on stock rods, then restore it above. This also shapes a flatter curve.
- **Supercharger predictability.** A centrifugal blower's boost depends only on rpm, which makes torque at any rpm repeatable; a turbo may arrive suddenly on corner exit. One reason traction-limited FWD cars sometimes choose centrifugal superchargers.

### Slip-based traction control
- Target slip around 5 to 8% (one dry-track setting: 6%, with a switchable 0 to 12% range and tighter in the wet). Zero target makes it overactive and ineffective, because driven and undriven speeds always differ slightly.
- Shape the target: more slip allowed in first and second; less in hard high-speed corners (compensate by lateral g against speed); an aggressiveness switch.
- Set a minimum activation speed (one example 20 km/h) so traction control does not fight launch control and drag burnouts remain possible.
- Use a cut range of about 100 rpm; zero range gives an abrupt hard cut, and a large range permits far more real wheelspin than the target suggests.
- Prefer fuel cut as the primary cut where valve control is marginal or lifters are hydraulic, for the reasons in methodology/engine-protection. A high logged fuel-cut percentage skips that share of injection events; it does not lean every cylinder.
- Proportional throttle closing and retard can make intervention smoother and quieter, with cut handling the rest; watch EGT when retard is used.

### Power management alternatives (drag)
- **Speed or driveshaft target against time.** Start a race timer at trans-brake or two-step release, define target driveshaft speed (or rpm) against time over about 15 s, and apply cut and timing removal proportional to overshoot (one example: zero cut at zero error rising to about 90% at about 30 mph overshoot).
- Timer-based schemes do not react: a bad launch leaves the timer running exactly as before, so they demand a lot of testing. One practitioner reports mixed results and prefers open-loop power reduction tables on measured wheel speed and other runtime values.
- **Ground-speed rpm limits per gear.** Fill a gear-by-speed table with rpm logged on the best pass (undriven speed), so the ECU replicates the best acceleration profile.
- **2WD with front-wheel lift or rules banning ground speed:** profile driveshaft rpm against time from a good pass and intervene when it spikes above the profile.

### Gear shift cut
- **Trigger.** Synchro box: clutch switch (driver clutches each shift with the throttle pinned). Dog or sequential box: lever strain gauge or barrel position sensor allows clutchless shifts. Strain gauge thresholds: the upshift force can be high (the box cannot be pulled out under power), the downshift force lower, so the request goes out before the driver can force the box out of gear unsynchronised and lock the rear wheels. Add a small hysteresis.
- **Closed loop wherever possible.** Hold the cut until the barrel sensor shows the next gear. The entered time is then a maximum (about 150 ms where shifts complete in 40 to 80 ms). One sequential example logged maximum times of 80, 70 and 60 ms for successive upshifts.
- **Timed cut only.** Start long (about 120 ms) and shorten, always erring long; per-gear values for slower across-gate shifts (one drag car: 60 ms on straight shifts, 80 to 100 ms across the gate). Typical synchromesh shifts take 100 to 200 ms.
- **Clutch-switch secondary limit (synchro flat shift).** A generic rpm limit indexed on clutch state and throttle: with the clutch in and throttle above about 80%, hold the engine near the rpm it will meet in the next gear (for example 5000 rpm when shifting from 6500). Because it follows the clutch pedal, it ends when the shift ends, which a timed cut cannot do. Set other cells far above the main limit. The throttle axis stops it capping heel-and-toe blips.
- **Cut depth.** Practitioners differ (see Disputed). A partial cut often suffices, since a preloaded lever needs only a partial lift to unload the dogs; start around 60 to 70% and reduce until shifts fail, or use 90 to 100% where the ECU or box demands it.
- **Torque return.** Ramp torque back (20 to 100 ms in the sources) and add post-shift retard (examples up to about 30 degrees) to stop the returning torque unloading the tyres. Slower reintroduction is kinder to the driveline; very fast return suits drag but shock-loads the transmission. A default slow decay made one car feel doughy in the next gear.
- **Lockouts.** Throttle (above about 30 to 50%), rpm and speed thresholds, a maximum cut time in case a switch sticks, a downshift over-rev lockout, a re-arm delay against double requests, and neutral or reverse protections on paddle systems.
- **Speed matching** targets next-gear rpm (slightly above 100% for power-on, slightly below for power-off). Still tune the open-loop blip properly, because a sensor fault reverts to it.
- **Shift air supply.** Monitor accumulator pressure with a sensor rather than a pressure switch and relay. Low air gives slow shifts that damage dogs; set a fallback timed compressor run if the sensor fails.
- **First from neutral.** Ask for the gear soon after the clutch goes down, before the input shaft stops; once stopped, dogs tend to butt face to face, especially with cold oil.
- **Driver technique matters.** Violent downshifts gave rear compression lock until the drivers moved the lever more deliberately. An inexperienced driver holding the limiter on a lever box was cured by a button-actuated air shifter.

### Pit lane limiter
- Prefer a true speed-based limiter; an rpm-based one depends on gear and tyre diameter (wets versus slicks), so brief the driver on which gear to use.
- Cut-based speed limiting gave the most accurate control in one test; throttle-only control was too slow, and cruise control is far too slow. Throttle limiting is best used to cap opening.
- Tune the cut range for smoothness first, then validate actual pit speed and adjust the set speed (set and achieved speed differed by 2.5 to 3 km/h in one example); re-validate after any change.
- Teach drivers to hold the throttle where the cut just begins rather than flooring it, which forces heavy cutting and popping. Show the limiter state clearly on the dash; a limiter left on has been reported as a misfire, and one left on at a rolling start risks a rear-end collision.

## Decision rules
- Shape torque to grip first; traction control is the backstop.
- Calibrate wheel speeds and ratios before any slip-based function, and after any wheel change.
- Closed-loop shift cut where a gear position sensor exists; otherwise time it long.
- Ramp torque back after every cut on traction-limited cars.
- Gate shift cuts by throttle on circuit cars so heel-and-toe still works.
- Fuel or partial cut on fragile valvetrains; audit the cut type of every function.

## Data gates
Log driven and undriven wheel speeds, calculated slip and slip target, traction speed limit against engine speed, gear and gear position voltage (fast), cut percentages and counters by function, ignition trims, throttle and pedal, boost and boost target, lateral and longitudinal g, and clutch switch or position.

## Worked example
A rear-drive car: wheel circumference 1.95 m, first gear 3.6, final drive 4.1. At an undriven speed of 50 km/h (13.9 m/s) the wheel turns 7.12 rev/s, so the no-slip engine speed is 7.12 × 3.6 × 4.1 × 60 ≈ 6300 rpm. With a 6% slip target the traction limit is about 6680 rpm, and with a 100 rpm cut range full cut is reached near 6780 rpm, about 7.6% real slip. If smaller tyres are later fitted to the undriven axle and the circumference entry is not updated (2% too large), the calculated ground speed reads 2% high, the limit rises 2%, and about 1.06 × 1.02 ≈ 8% real slip passes before the cut begins.

## Disputed / conflicts
- **Shift cut type.** One practitioner (an `practice` gear shift session) uses ignition cut for shifts almost always. Another (097) prefers ignition cut but advises caution on sensitive valvetrains. Others (200, 314, 090) prefer fuel or combined cut unless the valvetrain is proven, and one (186) prefers ignition cut plus heavy retard on turbo drag engines with a valvetrain built for it, because the exhaust combustion helps keep the turbo spinning. Choose by valvetrain and exposure.
- **Shift cut depth.** A course lesson (10-12) uses 90 to 100% cut; sessions 200 and 314 call 100% a common error and run 60 to 70% (80% conservative) on turbo engines; session 186 notes 100% works but is unnecessary.
- **Slip-based traction control versus power management.** The `practice` drag sessions found slip-based control too coarse to adjust and use power management as the default replacement. The `practice` traction control session demonstrates effective slip-based control on a circuit car with shaped targets. They are partly different applications (drag versus circuit).
- **Throttle as the traction actuator.** Sessions 090, 155 and an `practice` throttle session find it slow or hard to tune; custom-firmware tests in 090 added proportional throttle closing alongside cut with unproven benefit. No source shows throttle alone as sufficient.
- **Two-step exit decay versus shift decay.** Zero decay helps drag launches; a small decay extended sequential gearbox life on shift cuts in the same source.

## Citations
- practice: Practitioner training and tuning practice, distilled and cross-checked.
