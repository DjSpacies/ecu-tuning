---
id: principles/myths/torque-drop-reveals-knock
title: Myth: a dyno torque drop, mixture or exhaust temperature will reveal knock
layer: L1
status: draft
confidence: medium
sources: [practice]
verified: 2026-11-11
applies_to: {fuels: [gasoline, ethanol, methanol], engines: [all]}
depends_on: [principles/combustion/knock, methodology/knock-assessment]
supersedes: []
---

# Myth: a dyno torque drop, mixture or exhaust temperature will reveal knock

## Claim
Knock cannot be found reliably from the torque curve, the wideband reading or exhaust gas temperature. Only knock-specific sensing (audio monitoring or a validated ECU knock system) detects its onset.

## Why (derivation)
- **Torque.** Knock usually begins on one or two cylinders. Those lose a little work, but the rest are still moving towards MBT and gain from each step of advance, so the engine total can keep rising. Only severe knock on all cylinders lowers measured torque noticeably, and by then damage is likely on a high-output engine.
- **Mixture.** Air and fuel are trapped when the intake valve closes; knock happens later in the same cycle and cannot change the ratio a wideband measures. A misfire, not knock, reads lean.
- **Exhaust temperature.** Thermocouple probes respond over seconds, far too slowly for sporadic knock events. EGT also rises with retarded timing and with leaner mixtures, so there is no EGT value that marks a knock threshold, which depends on boost, compression and chamber design.

## Assumptions
Multi-cylinder spark-ignition engine; normal dyno ramp or steady-state testing.

## Breaks when
Heavy, widespread knock does flatten or drop torque, and a single-cylinder engine has no other cylinders to mask it. Neither case makes torque a safe detector, because the event has already happened.

## Practical use
When a user says knock monitoring is unnecessary because the dyno will show it, explain the masking effect and require knock-specific evidence for any timing near the limit. Use exhaust temperature for what it does well: cylinder-to-cylinder evenness and a maximum-temperature check for turbo and engine, and for alcohol drag engines a single cylinder's EGT running away from the others as an abort trigger for a fuel fault.

## Worked example
A pump-fuel turbo engine at about 1 to 1.2 bar of boost gains torque with every 2 degrees of advance, while headphones and per-cylinder logs show clear light knock on one cylinder. The torque curve says keep going; the knock evidence says retard to a margin below onset. The knock evidence wins.

## Disputed / conflicts
The torque-drop method is presented by practitioners as a common view, particularly among tuners who work on load-bearing dynos. Multiple practitioners in the sources report having heard knock on pump-fuel turbo engines while torque and power were still climbing. Discriminating test: step timing on a knock-limited engine while logging torque and per-cylinder knock together; onset on one cylinder will appear before any torque loss.
A related suggestion that a falling EGT at stable mixture shows pistons absorbing knock heat is rejected by one practitioner on response-time grounds.

## Citations
- practice: Practitioner training and tuning practice, distilled and cross-checked.
