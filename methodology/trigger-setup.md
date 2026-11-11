---
id: methodology/trigger-setup
title: Trigger setup
layer: L2
status: draft
confidence: low
sources: [practice]
verified: 2026-11-10
applies_to: {fuels: [gasoline, ethanol, methanol], engines: [all]}
depends_on: [methodology/base-setup]
supersedes: []
---

# Trigger setup

## Claim
A correct trigger setup is the base of all timing. Choose the mode that matches the wheel, verify a clean signal, and do not filter around a real fault.

## Why (derivation)
Every fuel and ignition event is placed from this reference. Noise or a wrong decode causes errors that masquerade as fuel or knock problems.

## Assumptions
The wheel pattern is known.

## Breaks when
Noisy reluctor signals, or sensors with wrong arming thresholds.

## Practical use
Verify with a trigger scope and engine speed reading before anything else.

## Decision rules
Match the decode mode and tooth counts to the actual wheel, and ask the ECU maker when in doubt. Set the arming threshold above background noise. Treat filtering as a sign of a problem to fix, not a cure. Disable fuel and ignition during verification cranking.

A correct arming threshold sits above the noise. Use as little filtering as possible. Polarity errors on a reluctor sensor produce timing drift. Check the pattern against the actual wheel, and do not assume a similar-sounding option is right.

## Data gates
No trigger errors counted; stable rpm while cranking.

## Worked example
An erratic rpm reading at high rpm with no fuel issue points at the trigger signal.

## Disputed / conflicts
None recorded.

## Citations
- practice: Practitioner training and tuning practice, distilled and cross-checked.
