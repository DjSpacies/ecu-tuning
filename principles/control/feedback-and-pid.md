---
id: principles/control/feedback-and-pid
title: Feedback control and PID limits
layer: L0
status: draft
confidence: high
sources: [engineering-texts, practice]
verified: 2026-11-11
applies_to: {fuels: [gasoline, ethanol, methanol], engines: [all]}
depends_on: [principles/data/sensor-lag-and-delay]
supersedes: []
---

# Feedback control and PID limits

## Claim
Feedback corrects errors it can measure, within limits set by delay and actuator range. Feed-forward carries the known part of the demand so feedback only handles the remainder. Gains belong to one plant: each controlled system has its own speed, latency and precision need, and gains that suit one never transfer to another.

## Why (derivation)
A PID controller adds proportional, integral and derivative terms of the error to a feed-forward value. In one engineering-unit form the output is feed-forward plus a gain times error, plus the accumulated error times a gain, plus a gain times the rate of change of error; the units of each gain (for example percent duty per kPa, or per kPa per second) say what it acts on.

- **Proportional alone leaves an error.** Its push shrinks as the error shrinks, so it never quite reaches target. More gain gets closer but overshoots and then oscillates. With P alone the drive only reverses after the error has changed sign, that is after passing the target, so it cannot prevent overshoot.
- **Derivative brakes.** It responds to the error closing quickly and reduces drive before the target is reached, which allows more P without overshoot. Too much makes the approach slow and rounded.
- **Integral removes the residual.** It accumulates error over time and holds the output against a steady offset. It acts on past error, so too much behaves like excess P: overshoot and oscillation.

The sources use one analogy consistently: P is the accelerator, D the brake, and I the effort needed to hold position on a slope.

Integral action has a failure mode. When an actuator saturates or sits on a mechanical stop, the integral keeps growing (windup) and the next reachable target is answered slowly while it unwinds, or with overshoot. Delay limits how fast a loop can respond; gain that would be fine without delay goes unstable with it. A controller that updates faster than the plant can show the result of its last change keeps adding correction it cannot yet see. Good feed-forward reduces the error the feedback loop has to fix, which is why a correct base map matters even with closed-loop control.

When two integrating loops act on the same error (a fast closed-loop trim and a slow self-learning table, for example), their time constants must be well separated, or the slow one chases the fast one and the pair oscillates. This is why self-learning transfers large errors only slowly.

Switching functions need hysteresis: a function switched on and off at the same threshold toggles rapidly while the engine sits at that point. Dead bands play a related role for continuous loops, treating a small error as no error.

## Assumptions
Linear behaviour near the operating point; gains are valid around where they were tuned.

## Breaks when
- Loop behaviour changes across speed and load, needing gain scheduling. Closed-loop lambda is the clearest case: transport is slow at idle and cruise and fast at high flow, so a gain that is stable at full load can hunt at idle, and one sized for idle is sluggish at full load.
- Sensor faults fed into feedback drive the actuator the wrong way.
- The target is physically unreachable (beyond actuator travel, or a boost level the hardware cannot make): windup follows.
- Some ECUs filter the measured input invisibly; the loop then sees a slower plant than the display suggests.
- Gains are entered as raw, unitless numbers whose scale varies hugely between ECUs; the absolute values tell nothing about strength.

## Practical use
Tune open-loop base values first, then feedback. Limit feedback authority. Treat persistent, large feedback trims as a sign the base data is wrong.

### Order of work for any loop (idle, boost, cam, throttle, lambda)
1. Set all gains to zero so the system runs on feed-forward alone, and tune the feed-forward table until the output lands as close to target as practical across conditions. This also proves the hardware controls repeatably on its own. An oscillating closed loop makes the logged output useless for refining the base table, which is another reason to start here.
2. Measure the real actuator range (cam travel, wastegate duty that holds a boost level) and keep every target inside it, with a margin. For a cam with a rest stop, calibrate the rest reading slightly beyond zero so a zero target is always reachable; otherwise a reading that drifts slightly past zero leaves the integral pushing into the stop.
3. Raise P from a small value, doubling each time and judging the response to step changes in target, until it oscillates; then halve. Small steps (24 to 23, say) often show no visible change, so direction cannot be judged.
4. Add D in the same way until overshoot is gone without the approach becoming lethargic; trade P against D.
5. Add a little I last, doubling until steady error is removed, and back off when overshoot returns.
6. Validate with commanded steps, not ramps. Pick both step values away from mechanical stops (for example 10 to 30 degrees on an intake cam stopped at 0), so overshoot shows on both sides, and expect the two directions to differ when one is mechanically easier.
7. Once the base is right, tighten the authority of the loop (one practitioner narrowed closed-loop fuel trim to about plus or minus 12 % once trims sat within 1 to 2 %).

### Matching expectations to the plant
Examples from the sources, not limits: hydraulic cam phasing can move 10 to 20 degrees in under a tenth of a second and is expected to hold within about half a degree; electronic throttle needs about a tenth of a percent; idle speed has inherent latency and tolerates tens of rpm; turbo boost rises smoothly rather than as a square wave. Chasing a response the hardware cannot give wastes time. Slow plants suit a slow update interval (100 to 200 ms for idle air in one example), and idle loops are often integral-only, with a small P added when the actuator is fast.

### Diagnostic tests
- **Gain too high versus too low.** Slow approach with a large lingering error: P low. Oscillation about target: P or I high. Oscillation that D removes: D low. Rounded, late arrival: D high or P low. Steady offset: I low.
- **Stability edge.** Constant noise in the output duty while the measured value still looks stable warns that the loop is close to oscillation.
- **Windup versus a slow actuator.** Request a reachable step from rest and time it; then hold an unreachable target for a while and request the same step. If the second response is much slower (about 10 s in one cam demonstration against a fraction of a second normally), the integral wound up.
- **Closed-loop lambda gain versus transport.** Trims swinging from rich limit to lean limit and back, or short-term trim constantly crossing zero, at idle or cruise means the controller is correcting faster than the sensor can show; reduce gain there, possibly scheduling it higher at high rpm. Oscillation at full load is the dangerous case to watch for.
- **Base error versus controller.** Large steady trims or a large steady integral contribution mean the feed-forward is wrong; fix it there rather than in the gains.

## Worked example
A boost controller saturates at maximum duty while below target. The integral grows; when boost arrives it overshoots. Clamping the integral or adding a correct duty feed-forward removes the overshoot.

On a throttle loop, P of 10 gives full oscillation, 6 gives audible flutter on closing, 4 slight overshoot on return to zero, and 2 almost none. P is set at 2, I at about half of P to remove the residual, and a very small D added as a brake. The numbers are in one ECU's units and say nothing about another ECU.

## Disputed / conflicts
- **Analytical tuning versus stepping.** Control texts give systematic tuning rules (relay and step-response methods). One practitioner's experience is that nearly all engine tuners use trial and error by doubling and halving instead. Both aim at the same result; the empirical route needs no plant model and tolerates the raw gain scales of engine ECUs.
- **Derivative in lambda control.** One ECU maker's guidance shown in the sources prefers no D term for closed-loop fuel, while other sources use D generally as a brake. Lambda feedback is dominated by transport delay, where derivative action on a noisy signal adds little.
- **Integral clamps.** Clamping the integral reduces windup; one practitioner holds that keeping targets within reach is the better fix, with clamps as a backstop. Both are compatible.
- **Dead bands.** Sources use a dead band for idle speed (tens of rpm) and near-zero dead band for throttle and cam control, and note that lambda moves too constantly for a dead band to help; filtering is used instead.

## Citations
- engineering-texts: Engine, combustion, charging and control engineering texts.
- practice: Practitioner training and tuning practice, distilled and cross-checked.
