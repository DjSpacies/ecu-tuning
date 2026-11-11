---
id: methodology/idle-ignition-control
title: Idle ignition control
layer: L2
status: draft
confidence: high
sources: [practice]
verified: 2026-11-11
applies_to: {fuels: [gasoline, ethanol, methanol], engines: [all]}
depends_on: [methodology/idle, principles/combustion/mbt-timing, principles/control/feedback-and-pid]
supersedes: []
---

# Idle ignition control

## Claim
Spark timing is the fast, fine idle speed actuator, and airflow is the slow, coarse one. Idle ignition control
works only if the on-target idle timing sits well retarded from idle MBT, so there is torque to add as well as
remove. Correction should be indexed by rpm error from the active target, not by absolute rpm. Where the
timing settles is the best single indicator of whether base idle air is right: timing hovering near its target
means the air is right. Timing pinned at a clamp, or held far retarded, means the air is wrong. Fix the air;
do not lean on spark to hide it.

## Why (derivation)
- Torque versus spark advance peaks at MBT and falls either side (principles/combustion/mbt-timing). At MBT,
  advancing gains nothing, so the controller can only pull rpm down. Below MBT, advancing raises torque and
  rpm and retarding lowers them, both within a combustion cycle. Air bypass changes have latency: the actuator
  moves, then the manifold fills.
- With fixed throttle on one demonstration engine, 10, 18 and 24 degrees gave roughly 850 to 880, 980 and 1080 to
  1090 rpm. That is about a 200 rpm window from 14 degrees of spark span with no air change. Idle rpm acts as the
  torque meter that a dyno would otherwise provide.
- In that demonstration, a headlight and fan load at fixed 15 degrees dropped idle by about 90 rpm. With
  error-based correction active, the same load cost only about 20 rpm as timing rose from about 12 to 15 to 18
  degrees, with air still in open loop.
- An error axis follows the target as it moves with coolant temperature. A table on absolute rpm only works at one
  speed: a raised cold target lands in the retard zone, so the cold idle gets pulled down.
- Spark does not change the trapped air-fuel ratio, so a hunting spark idle does not itself foul plugs.

## Assumptions
- Base idle air is set so target speed is reached with timing near its on-target value.
- The idle timing target is below idle MBT. The sources put idle MBT on gasoline engines at roughly 20 to 30
  degrees; demonstration engines measured about 24 to 28 at 800 to 900 rpm.
- Lockouts confine the function to genuine idle.

## Breaks when
- **Base air far off.** The function saturates. Timing pinned at maximum with rpm still low means too little air.
  Timing pinned at minimum, or sitting very retarded, with rpm high means too much air.
- **Lockouts too loose.** If the throttle lockout sits above the real closed-throttle reading plus noise (for
  example 1.5 to 2% where the rest value wanders 0.2 to 0.3%), the function stays active on gentle pull-away
  and retards against the driver.
- **Two actuators fighting.** An electronic throttle and spark both correcting fast can make idle unstable. One
  demonstration cut the throttle's idle gain to almost nothing and let spark do most of the work.
- **Lopey cams.** Correction tables tuned for a smooth stock cam can be too aggressive with a lopey cam and
  make idle worse. One source scales such tables by about half as a first test.
- **Rotary engines.** They idle smoothly near 0 to 5 degrees BTDC, or even after TDC, and normally run far more
  retard than piston engines. The piston-engine numbers here do not apply, though the principle does.
- **Fuel changes MBT.** An engine that only holds target with extreme retard (one example: about 30 degrees after
  TDC) has too much air, or wants different timing for its fuel. The exhaust gets very hot and the manifold can
  glow.

## Practical use
### Order
Leave idle ignition control off while setting base timing, idle fuel and the base air table. It is fast
enough to mask base air errors. Enable it last (methodology/idle).

### Choosing the on-target timing
- Find idle MBT approximately. Advance a couple of degrees at a time at a fixed air setting until idle speed
  stops rising. One course lesson sets on-target timing about 6 to 8 degrees retarded from that point.
- Values in the sources: about 10 to 16 degrees BTDC on-target for most piston engines, with some using 16 to 18
  where MBT is in the high 20s. One practitioner calls 10 to 15 degrees typical and safe for most engines.
- Keep the idle cells of the base table flat, so interpolation does not move timing on its own.
- Open the idle air slightly more than an engine running near MBT would need, so target is reached at the
  retarded on-target value.

### Shaping the correction
- Add timing below target and remove it, more aggressively, above target. Do not add beyond MBT: it stops
  adding torque.
- One example table: +8 degrees at 50 rpm under, +15 at 300 under; −5 at 50 over, −14 at 200 over and beyond.
- One example absolute table: about 25 degrees at 500 rpm under, about 10 at target, 0 to 5 when 100 to 500 rpm
  over.
- For cold running, the cold rows can lean toward adding timing, because undershoot is expected there.

### Clamps and floor
- Examples in the sources: minimum 0 degrees, maximum about 22 to 30 degrees, or a band of about ±15 degrees
  centred on the target. The centre must allow movement both ways.
- Avoid holding idle at very low timing. Practitioners set the sustained floor between about TDC and 5 degrees
  BTDC (see Disputed / conflicts). Long idling at 0 to −10 degrees heats the exhaust manifold, turbo and engine
  bay, and makes pull-away lethargic. After-TDC values are acceptable only as brief corrections to a momentary
  flare.
- If timing regularly needs to retard more than about 5 to 10 degrees to hold target, reduce base air.

### Lockouts
Lock out above normal idle MAP, above an rpm a few hundred over target, above a small vehicle speed, and above
a throttle opening just over the logged closed reading. One practitioner sets that about 0.2% above the observed
rest value; others cite 0.5 to 1%. A silently active lockout (one example: a MAP limit left at zero) disables
the function completely.

### Reading the logs
- Compare base-map timing with actual timing at idle. The difference is what the controller is doing.
- Small, constantly moving corrections are normal.
- Large sustained offsets point to wrong idle air.
- Timing that barely leaves its target means the base air is close.

### Without a dedicated function
- Put closely spaced rpm breakpoints around target in the main ignition map, with timing rising below target
  and falling above it (examples: 24/18/14 degrees, or 24/10/5 at 750/800/850 rpm). Confine this to
  idle-vacuum load cells, because the car drives through those cells when pulling away. Heavy retard there
  makes take-off hesitant.
- Alternatively, use an additive overlay indexed by rpm error and throttle position, so it does nothing once
  the throttle is open. Enter offsets, not absolute timing.

### Engines with no idle air device
- Set the throttle stop so hot idle near on-target timing is above the desired speed. Sources use about 100 to
  400 rpm above (for example 1200 to 1250 rpm for a 1000 target). Retard then pulls it down when hot, and
  advance holds it when cold.
- Expect a compromise. One example only reached about 1000 rpm hot and idled about 800 to 900 cold. Throttle
  may still be needed for the first few minutes from cold, and one source found the method weak in sub-zero
  weather.
- Still set coolant-indexed targets, because the error axis depends on them.

### Big cams and surge
Retarding at idle and very light throttle dulls torque response and damps surge and lope, at some cost to
economy and response. If timing comes out, open the idle air to restore speed.

## Worked example
A turbo engine idles at 1300 to 1400 rpm against an 1100 rpm target, and idle timing is parked at its −5 degree
minimum. Spark has run out of authority because the base throttle admits too much air. Lowering the base
electronic-throttle opening in small steps (about 4% to 3%) brings speed near target, and idle timing rises to
about 8 to 10 degrees, inside its range.

The opposite case: an engine sits about 300 rpm below target with idle timing at its 30 degree cap. Raising the
base valve position (45% to 50% in the example) brings speed up and lets timing fall back to its 10 degree
baseline, with room to move between 0 and 30.

## Disputed / conflicts
- **Sustained retard floor.** Several practitioners avoid sustaining much below about 5 degrees BTDC. Others clamp
  at 0 degrees and accept TDC as the rough lower limit, while allowing brief after-TDC excursions. Both sides
  agree that sustained deep retard means too much air and costs exhaust heat. Test: EGT and manifold
  temperature after ten minutes of idle at each floor.
- **Locked timing after start.** One practitioner prefers active idle ignition control over a period of locked
  timing after start. Locking removes a variable, but gives up a strong idle tool.
- **Cold advance.** Some sources add advance when cold to recover cold torque, especially with no idle air device.
  One practitioner normally leaves cold timing alone and relies on fuel and idle air, and says he has seen no
  benefit (methodology/cold-start-warmup).
- **Cosmetic lope.** One demonstration made the park/neutral correction deliberately over-aggressive to mimic a
  big-cam lope. It is presented as purely cosmetic, active only in park or neutral with the throttle closed, and
  it is not a performance change. A spark-driven hunt does not change the trapped mixture, so it does not foul
  plugs in itself.

## Citations
- practice: Practitioner training and tuning practice, distilled and cross-checked.
