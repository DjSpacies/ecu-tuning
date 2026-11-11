---
id: principles/control/feedback-and-pid
title: Feedback control and PID limits
layer: L0
status: draft
confidence: high
sources: [engineering-texts]
verified: 2026-11-10
applies_to: {fuels: [gasoline, ethanol, methanol], engines: [all]}
depends_on: [principles/data/sensor-lag-and-delay]
supersedes: []
---

# Feedback control and PID limits

## Claim
Feedback corrects errors it can measure, within limits set by delay and actuator range. Feed-forward carries the known part of the demand so feedback only handles the remainder.

## Why (derivation)
A PID controller adds proportional, integral and derivative terms of the error. Integral action removes steady error, but when an actuator saturates the integral keeps growing (windup) and causes overshoot. Delay limits how fast a loop can respond; gain that would be fine without delay goes unstable with it. Good feed-forward reduces the error the feedback loop has to fix, which is why a correct base map matters even with closed-loop control.

## Assumptions
Linear behaviour near the operating point; gains are valid around where they were tuned.

## Breaks when
Loop behaviour changes across speed and load, needing gain scheduling. Sensor faults fed into feedback drive the actuator the wrong way.

## Practical use
Tune open-loop base values first, then feedback. Limit feedback authority. Treat persistent, large feedback trims as a sign the base data is wrong.

## Worked example
A boost controller saturates at maximum duty while below target. The integral grows; when boost arrives it overshoots. Clamping the integral or adding a correct duty feed-forward removes the overshoot.

## Disputed / conflicts
None recorded.

## Citations
- engineering-texts: Engine, combustion, charging and control engineering texts.
