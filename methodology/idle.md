---
id: methodology/idle
title: Idle tuning
layer: L2
status: draft
confidence: high
sources: [practice]
verified: 2026-11-11
applies_to: {fuels: [gasoline, ethanol, methanol], engines: [all]}
depends_on: [methodology/first-start, principles/control/feedback-and-pid, principles/combustion/mbt-timing, principles/fueling/injector-flow-and-dead-time]
supersedes: []
---

# Idle tuning

## Claim
Idle is a torque balance held at the lowest speed the engine combination can sustain. Work in this order:
check the engine is mechanically healthy, pick a realistic target, get idle fuel and a smooth idle ignition
value right, then set the open-loop base air position across coolant temperature with every feedback loop off,
then add load steps, then closed-loop air, then idle ignition control (methodology/idle-ignition-control).
Idle control cannot fix a bad base calibration, a target the engine cannot reach, or a mechanical fault. It
can only hide them. Idle is also where bad injector data shows up first.

## Why (derivation)
- **Torque balance.** At steady idle the engine makes just enough indicated torque to cover friction, pumping
  and accessory load. An practitioner example puts this at only about 6 to 10 lb-ft, roughly 8 to 14 N·m, for a
  typical road engine. Speed rises when torque exceeds that and falls when it does not. Anything that changes
  torque changes idle speed: airflow (fuel follows it), spark advance, mixture, friction, and accessory load.
- **Two actuators with different speeds.** Air is the coarse, slow lever. A stepper, a bypass solenoid or a
  throttle blade has to move, then the manifold has to fill before torque changes. Spark acts within one
  combustion cycle, so it is the fast, fine lever. This only works while timing sits below MBT
  (principles/combustion/mbt-timing).
- **Mixture moves torque too.** In one demonstration, richening a warm idle from lambda about 1.1 to 1.0 raised
  speed by about 40 rpm with nothing else changed. A lean idle, especially leaner than stoichiometric, hunts and
  idles roughly. A moderately rich one usually still idles. Fuel is not a usable speed-control lever, but a
  wrong idle mixture changes how much air the controller seems to need.
- **Feed-forward plus feedback.** Idle air control is a base (feed-forward) position plus a PID correction
  (principles/control/feedback-and-pid). If the base already gives target speed, the feedback has almost
  nothing to do and control is stable across conditions. A large, persistent feedback contribution means the
  base is wrong, even when actual speed sits exactly on target.
- **Why some engines need a higher idle.** Long duration and high overlap cut low-speed VE and add exhaust
  dilution and reversion, so combustion becomes unstable at low speed. Fewer cylinders (fewer power strokes per
  revolution) and light flywheels or rotating parts also reduce stability. Very large injectors run in their
  non-linear short-pulse region at low idle speed, which makes fuelling erratic.
- **Why a cold engine needs more air.** Thick oil and tight clearances add friction, and wall wetting lowers
  combustion efficiency, so the same speed needs more airflow when cold. A higher cold target also helps
  combustion while fuel preparation is poor (methodology/cold-start-warmup).
- **Dead time.** Idle pulse widths are short, so a dead-time error is a large fraction of the fuel delivered
  (principles/fueling/injector-flow-and-dead-time). A supply voltage away from normal shifts dead time and moves
  idle fuelling.

## Assumptions
- The idle target is realistic for the cam, capacity, cylinder count and flywheel.
- Main fuel and ignition at the idle site are tuned, and coolant and air temperature corrections keep lambda on
  target across temperatures.
- The actuator works, moves the right way, and has enough but not excessive authority.
- Charging voltage is normal, and no hidden warm-up, post-start or acceleration enrichment is active when warm
  fuelling is judged.

## Breaks when
- **Big overlap cams.** The wideband reading at idle may not represent combustion, because unburnt charge
  reaches the exhaust. Tuning becomes partly by ear. Closed-loop idle can chase the engine's natural lope and
  destabilise itself. See Disputed / conflicts for the two ways practitioners handle this.
- **Huge injectors.** Lambda can bounce at a low idle because the injectors are working at very short pulses.
  In one example, raising idle speed fixed it where fuel table changes would not have.
- **Oversized MAF.** If the sensor or housing is sized well beyond the power target, idle sits at the bottom of
  its calibration. Idle fuelling then becomes inconsistent and trims wander. With a turbo, air reverting past
  the MAF when the driver lifts off (or a blow-off valve venting to atmosphere) gives a brief over-read and a
  rich stumble or stall when coming to a stop. The sources treat this as nearly impossible to tune out. The
  fixes are hardware: more tube length between the MAF and the turbo, and a recirculating valve.
- **Individual throttles on an alpha-N load model.** Air from a bypass valve does not show up in throttle angle,
  so idle mixture wanders as the valve moves. The sources prefer an electronic throttle on the individual
  throttles, or else a fuel correction indexed by idle valve duty.
- **Very large electronic throttle bodies** (an practitioner cites 90 to 100 mm and up). A tiny change in opening
  gives a large change in airflow, so idle resolution and stability suffer.
- **Heat soak.** Hunting with very hot intake air is most often a lean mixture, not an idle control fault. Check
  lambda first.
- **Rotary engines** idle richer and with far less timing than piston engines. They also need more speed when
  ported (one example: about 1000 rpm stock port, up to about 1500 rpm heavily ported).
- **Automatic transmissions.** A converter matched to a low-idling engine couples hard at a higher idle. Selecting
  drive drags rpm down, and the car pushes against the brake. In the sources the fix is a higher-stall converter,
  or a transmission-controller strategy that partly slips a clutch at a standstill, not idle calibration. The
  sources call strong creep at a standstill a safety issue, not just a comfort one.
- **No idle air device.** A race engine with only a throttle stop can be held by ignition alone, but it needs
  nursing when cold and idles low or high at the temperature extremes.

## Practical use
### 1. Use idle as a mechanical health check first
Before any load tuning, the engine should idle without help at a sensible speed and vacuum. In the sources,
an engine that will not do this is more often mechanical than a calibration problem: wrong cam timing (a tooth
out), intake leaks, a bent or leaking valve, or trigger errors. Fixing it later means redoing the tune.
- Form an expectation for the combination before judging. Practitioner examples of warm idle manifold pressure on
  stock cams are about 30 to 40 kPa absolute (equivalently about −60 to −70 kPa gauge). Mild aftermarket cams
  pull a little less, and aggressive high-overlap cams may sit at 70 to 80 kPa absolute, which is normal for them.
- The same weak vacuum on a stock-cam engine is a red flag. Sources describe a cam-timing fault giving only
  about 0 to −20 kPa gauge.
- An engine that stalls when brought down to a speed it should manage, together with poor vacuum, points to cam
  timing. Erratic rpm, logged trigger errors and unstable lambda point to electrical or trigger faults.
- Check charging voltage: about 13.8 to 14.2 V running. A freshly charged battery reads 12 to 12.5 V and hides a
  dead alternator at first. A non-charging system shows about 11 to 12.5 V and falls. Some alternators charge
  poorly at low idle speed. Voltage above battery level that rises with rpm means it is charging.
- If the idle output is fully closed but the engine idles well above target when hot, air is getting in around
  the throttle: a vacuum leak, a bypass, or another idle air circuit (for example, a factory wax-pellet
  fast-idle) still active.

### 2. Choose a realistic target
Asking for an idle the engine cannot hold is the mistake the sources mention most often. The controller then
fights a battle it cannot win.
- For a stock engine, start from the factory idle speed. For modified engines, add speed in proportion to how
  aggressive the cam is. One practitioner suggests about 50 to 100 rpm more for a mild cam and 200 to 300 rpm or
  more for an aggressive one. Check the engine or cam builder's documentation if there is any.
- Another method: lower the target until idle turns rough or erratic, then add 50 to 100 rpm.
- Typical warm targets in the sources: large stock V8 about 500 to 700 rpm; the same with a big cam about 800 to
  950; stock small four-cylinder about 750 to 950; cammed four-cylinder about 1000 to 1300; extreme drag cams
  1500 to 1800 or more. Several anecdotes describe hours lost pulling a race engine down to a low idle when its
  documentation specified about 1800 rpm.
- Raise the target when cold. A common shape is 200 to 300 rpm higher at about 10 to 20 °C, interpolated down to
  the hot target by roughly 60 to 80 °C. One practitioner regards factory calibrations idling above 1500 rpm when
  very cold as more than needed.
- Some calibrations use a short higher target just after start, decaying with run time, and a small increase
  while the vehicle is rolling (see section 6).
- Hold to a realistic stability goal. One practitioner treats about ±25 rpm around target as acceptable and says
  chasing a few rpm wastes time. Another accepts ±50 rpm.

### 3. Prerequisites: fuel and ignition at the idle site
- Tune idle VE or fuel across every idle rpm and coolant point the engine uses, and keep idle-area ignition
  smooth, before touching idle control. Big steps in the ignition table around idle, or a lean idle, are common
  hidden causes of a bad idle.
- One practitioner's yardstick: idle closed-loop trims around 5% that settle to 2 to 3% (for example as the fan
  cycles) mean fuelling is right. Another wants trims within about ±2 to 3% before idle work, with the engine
  fully warm.
- When the closed-loop fuel correction is used as a guide, multiply the base cells by the indicated correction
  and repeat until it sits near zero, then blend neighbours. A correction that flips sign means the change
  overshot.
- Trim all cells the operating point interpolates between (both rpm and both load breakpoints), not only the
  highlighted one.
- Lambda transport delay is longest at idle flow. Make changes slowly and wait for the reading to settle,
  otherwise successive changes overshoot.
- Idle fuelling commonly needs another trim once the car moves from the dyno to the road or track. One example
  ran clearly rich, with closed loop pulling about 14%. That is normal, not a fault.
- Cells below the lowest speed that can be held on the dyno are filled by copying the shape of the lowest tuned
  column and scaling it down to the known idle values. VE falls as speed drops, so straight copies run rich.

### 4. Check and size the actuator
- Confirm the actuator moves rpm at all. With idle control off, command the position by hand. If rpm does not
  follow, look for wiring, a stuck stepper, or a PWM frequency the solenoid cannot follow. Typical solenoid
  ranges cited are about 30 to 100 Hz; confirm on the part. Where the idle output shares a frequency with a
  boost solenoid, the boost solenoid is usually the more sensitive device.
- Verify direction. One practitioner reports that over half the cars he received had a stepper or three-wire
  valve wired or configured backwards, so asking for more air closed it. A table trend that looks reversed, or
  closed loop driving the wrong way, points to inverted polarity.
- Steppers have no position feedback. They reference by driving to an end stop at key-on, and a target beyond
  their travel just stalls the motor without harm. Base percentages map onto the motor's step range, a duty cycle
  for a solenoid, or a fraction of a configured maximum opening for an electronic throttle. A solenoid- or
  stepper-scale number entered on an electronic throttle can send the engine to the rev limiter.
- **Authority sizing on electronic throttles.** Many systems scale the base table to a maximum idle opening. Too
  small, and the base table pegs near 100% on a cold start with no room left: cold idle stays low whatever is
  entered. Too large, and each percent moves idle a lot, resolution suffers and it can hunt. Sources start
  around 6 to 10% of throttle and raise it a couple of percent only if cold idle saturates. One practitioner sizes
  it so the coldest start still leaves about 25% headroom. Some factory calibrations cap idle airflow with a
  separate limit. Raise that limit gradually instead of drilling the throttle plate.
- **Mechanical throttle stop with an idle valve.** Set the stop so the valve sits mid-range at hot idle, with
  room both ways. Examples: a hot-idle valve position around 5 to 15% with about 10% preferred; or, with idle
  devices disabled, a stop giving roughly 100 to 200 rpm below the desired hot idle. Re-zero the throttle sensor
  afterwards, because a closed-throttle reading above the idle-mode threshold stops idle control working.
- A bypass valve on a boosted engine should draw from the pressurised pipe before the throttle and feed the
  plenum. That loop is not a boost leak and does not need a check valve. A valve drawing from atmosphere does.
  On a MAF engine, the bypass air must also be metered. Some valves never fully close and leak a minimum flow,
  so the engine cannot reach a low hot idle.

### 5. Base (feed-forward) table: open loop first
- Turn closed-loop air and idle ignition control off, or set the PID gains to zero where open-loop mode hides
  the target table. Both mask errors in the base table.
- Check that no lockout is silently active. Examples from the sources: a closed-throttle reading above the
  throttle threshold, or a MAP lockout set at zero, made a working system look broken.
- Starting from a true cold soak, adjust the base value in the coolant cells currently being interpolated (both
  of them) until rpm meets target. Continue as the engine warms, alternating with idle VE corrections. Expect
  three or four cold starts to finish it.
- Read the base table's correctness from the response: rpm hanging above target means too much feed-forward air;
  settling low, or dipping and stalling after a blip, means too little.
- Faster ways to fill it:
  - let closed loop settle with a very low integral gain and copy the actual position into the base table at
    each temperature;
  - log a coolant-by-airflow (or position) histogram through a warm-up and paste it in.
  Where the actual opening is the base plus a separate closed-loop target, copying the total double-counts.
- **When closed loop is on**, correct the base by the size of the integral and proportional outputs until they
  sit near zero. In one example, idle sat exactly on target with a base of 48% while the integral read −6%. Base
  42% was right, and idle dipped until the integral unwound. A persistent closed-loop addition (one example:
  +20% on a 30% base) means the base is wrong. Error should swing either side of zero. Make small changes; a
  correction that flips from large negative to large positive means the steps are too big.
- Some practitioners leave the base slightly above the opening closed loop settles on (one example: about 0.2 to
  0.3% of throttle; with a MAF histogram, about 1 to 2 g/s extra). Idle then settles down onto target rather than
  undershooting.
- Response can be non-linear. In one example, the first ~10% of added base had little effect before speed rose
  to target. Cold cells that look inconsistent are revisited from a true cold start after the main maps are done.
- Long-term learned idle trims, where available, are kept off while hand-tuning. One practitioner then enables
  them for about a week of driving and folds the learned average back into the base.

### 6. Transitions: after start, coming to a stop, return to idle
- **After start.** A startup or post-crank air addition (park position, startup offset or post-crank duty) is
  held briefly and then decays. Sources aim for a crisp start with a small flare, about 100 to 200 rpm, that
  settles smoothly. A big flare, or a long hang at 1200 to 2000 rpm, means the offset is too large or held too
  long. A low rough stumble means too little. Tune it after the base table, because it adds on top of it. Keep
  post-crank additions to the first few seconds; additions still present 40 to 60 s after start overlap the
  warm-up base and confuse tuning.
- **Coasting to a stop.** When the wheels drive the engine above target with the throttle shut, closed loop
  closes the valve (and the integral winds down). When the clutch goes in there is no air left, and the engine
  dips or stalls. The fixes, in the sources:
  - a throttle lockout so idle control engages only with the throttle truly closed;
  - an rpm lockout band (about 400 to 600 rpm above target);
  - a vehicle-speed lockout;
  - a neutral or clutch timeout of a few seconds before closed loop engages;
  - a decel hold position or offset that decays onto target;
  - integral limits (one example: ±5%, with total feedback around ±10% if open loop is right);
  - a slightly raised target or base while rolling. Keep this small, or the car creeps or the rpm flares.
- **Return to idle after a blip.** Preferred behaviour is rpm coming down onto target from slightly above. An
  undershoot that recovers quickly (one example: 80 to 100 rpm) is acceptable on a slow system. A large
  undershoot sets the controller oscillating for several seconds. A decel offset that is too large hangs rpm;
  too small dips it. Some systems instead add a temporary rpm offset to the target on entry and ramp it away.
- **Stalls on return to idle are often fuel.** Manifold pressure drops first and rpm trails down through overrun
  and low-rpm transition cells. Errors there (too lean or very rich) cause stalls blamed on idle control. Map
  those areas and keep ignition transitions smooth before changing idle parameters.

### 7. Load steps
- Wire the A/C request, power steering pressure switch, fan output and neutral/drive inputs, and give each a
  feed-forward step, so closed loop does not have to react. Toggle each load in open loop and size the step until
  idle stays flat: a dip on engagement means too small, a flare means too large.
- One practitioner prefers a duty or airflow addition for A/C (the compressor needs more air for the same speed)
  over only raising the target. Others add both a small target increase (about 50 to 100 rpm) and an air step.
- Electrical loads change idle fuelling as well as speed. A trim swing of around 12% when a fan switched was
  treated as a sign it needs a load-based fuel adder, not closed loop doing the work.
- Brake booster draw dips idle slightly. It is normally ignored, but grows with small plenums.

### 8. Closed-loop gains and lockouts
- Default gains are usually fine. Change only the term the symptom points to:
  - oscillation suggests too much proportional (or too little derivative);
  - slow recovery suggests the opposite;
  - sharp rpm jumps on a dip suggest too much anti-stall gain, and frequent stalls too little.
- A valve moving erratically while idle hunts means the gains are too aggressive. Use idle ignition control for
  the fast part and slow the air loop.
- A deadband that is too tight makes the slow air loop fight natural fluctuation (about 25 rpm was called tight).
- Limit the duty range. Set the maximum so the coldest case can still exceed target, and the minimum a few
  percent below the lowest hot value. Excess authority does harm.
- Set throttle lockouts just above the logged closed-throttle reading. Sources cite about 0.5 to 1% throttle;
  one practitioner uses about 0.2% above the observed rest value. A lockout set too high leaves idle control
  fighting the driver at small openings and causes odd driveability.

## Decision rules
Typical idle advance is 15 to 20 degrees; heavily cammed engines often settle at 12 to 15. If ignition idle control is used, start 6 to 8 degrees retarded from the chosen base. Stock engines idle about lambda 0.95 to 1.0. Do not run richer than about 0.90 for long: plug fouling and bore wash. Choose a realistic idle speed; cold idle is commonly 200 to 300 rpm higher.

Prove idle with closed loop and ignition idle control off, because they mask errors in the base idle position. Set a realistic idle speed; forcing an unrealistic one is a very common mistake. Sitting below MBT keeps torque in reserve to control speed in both directions; one practitioner avoids sustaining much below about 5 degrees. Closed-loop gains can be raised until oscillation starts, then backed off. A stepper or a boost-style solenoid behaves differently, so check its frequency range.

Fix the cause before tuning idle control: a mechanical fault (vacuum, cam timing), a lean idle, a non-charging alternator, a hidden enrichment or an unrealistic target. Order: health check, target, idle fuel and ignition, actuator check, open-loop base across warm-up, load steps, closed-loop air, idle ignition last. Modified engines with big cams may idle best at lambda 0.90 to 0.95; small or mild engines may also idle more smoothly at about 0.95 when emissions do not require lambda 1.

## Data gates
Engine warm and stable; no electrical loads switching during measurement. Wideband ready, and its idle reading treated with caution on big-overlap cams. Warm-up and post-start enrichment confirmed zero, and no acceleration enrichment active, when warm idle fuel is judged. Charging voltage about 13.8 to 14.2 V. Idle lockouts confirmed inactive (closed-throttle reading below the threshold, idle MAP below any MAP lockout). Base table work done with closed-loop air and idle ignition control off, or with their outputs logged.

## Worked example
A cammed engine hunts at 15 degrees. Retarding to 12 degrees and adding idle air stabilises it, at the cost of a little more air.

Base table hidden by closed loop: a warm engine idles exactly on its 800 rpm target with closed loop on, and the
base table reads 48%. The logged integral output is −6%, so the controller is removing six points of opening.
Setting the base to 42% first drops idle (the integral is still pulling) and then speed returns to target as the
integral unwinds to about zero. Now a blip lands rpm near target without a long hunt, because the controller
starts from the right place.

Unrealistic target: a small four-cylinder with high-overlap cams set to 750 rpm hot oscillates and stalls despite
good fuel and timing. Raising the target to 1100 rpm hot and about 1350 rpm at 20 °C gives a stable idle, and
the base table can then be filled without the controller saturating.

## Disputed / conflicts
- **Richest acceptable idle.** This entry's rule caps sustained idle at about lambda 0.90. One course lesson
  allows down to about 0.85 before calling it a plug-fouling risk, and one practitioner puts the richest typically
  needed at about 12.8 to 13.2:1 AFR on petrol (roughly lambda 0.87 to 0.90). They agree that a sustained
  rich idle fouls plugs. Discriminating test: plug condition and idle stability over repeated short runs at
  0.90 versus 0.85.
- **Big-cam idle mixture.** Most sources richen a big-cam idle to about 0.90 to 0.95. One practitioner instead
  leans the mixture until rpm picks up, arguing that overlap makes the wideband read richer than combustion.
  Test: sweep mixture at fixed air and timing and use rpm (torque) as the judge, not the wideband reading.
- **Closed loop on lopey engines.** One course lesson falls back to open-loop air where closed loop hunts on a
  wild cam. Other sources keep closed loop with reduced gains and lean on idle ignition control. Test: rpm
  variance with each strategy at the same base table.
- **What holds warm idle.** One practitioner uses the idle air motor only for cold start and warm-up on most race
  cars, holding warm idle with a fixed opening and spark. Others make air the main controller at all
  temperatures, with spark only as a trim. Another practitioner ran race cars with no idle device for years, but
  now prefers working idle control even on race-only cars.
- **Electronic throttle plus a factory idle valve.** One practitioner's anecdote: the separate valve can be
  disabled and the electronic throttle used alone, with no issues seen. This is a single-source view.
- **Stepper versus solenoid.** One practitioner generally prefers a simple PWM solenoid. Another sees no
  performance difference, only that steppers can lose count and lean on closed loop to recover.
- **Base table margin.** Most sources aim the base at exactly the opening needed. Some deliberately leave it a
  little high so idle settles from above. These are compatible if the margin is small.
- **Torque converters.** Raising idle for a big cam can push an automatic toward converter stall. One
  practitioner advises keeping idle as low as the engine tolerates and retarding near idle. Others say the engine
  needs the speed, so the converter must change. Test: idle quality at the lowest stable speed versus converter
  creep force.
- Cross-check: no textbook passage on idle ignition reserve was found in this corpus, so the torque-reserve
  explanation rests on practitioners and the MBT physics.

## Citations
- practice: Practitioner training and tuning practice, distilled and cross-checked.
