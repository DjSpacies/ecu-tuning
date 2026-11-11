---
id: methodology/full-load
title: Full-load tuning
layer: L2
status: draft
confidence: medium
sources: [practice, engineering-texts]
verified: 2026-11-10
applies_to: {fuels: [gasoline, ethanol, methanol], engines: [all]}
depends_on: [methodology/steady-state-ignition, methodology/knock-assessment]
supersedes: []
---

# Full-load tuning

## Claim
Approach full load gradually using ramp runs, starting inside proven territory and adding rpm in small increments, fuelling safe first and ignition after.

## Why (derivation)
A full-load error happens at the highest cylinder pressure and thermal load. Short runs that extend proven range keep each new step close to known behaviour. Fuel is fixed first because it sets the mixture knock and timing are judged against.

## Assumptions
Fuel system capacity is known adequate. Steady-state tuning complete up to about two-thirds of redline.

## Breaks when
Long pulls on road or track heat the charge more than a short dyno run.

## Practical use
Extrapolate fuel and timing into untuned cells with safety in mind before each new step.

## Decision rules
A ramp of about 1 second per 500 rpm is a useful default; finish with a longer run. Remove about 2 degrees on the top rows before the first run; add rpm 500 at a time. Abort on knock. Keep lambda on target first; then add 2 degrees over rows, reducing to 1 degree steps near the optimum, and stop if torque does not rise. Fuel is safer rich: start rich and remove.

Remove a couple of degrees from the top load rows before the first ramp runs. Expect peak numbers in a VE table around the rpm of peak torque, and investigate any table that does not. On boost, extend the load axis a little beyond the maximum expected.

## Data gates
Injector duty below ceiling; no limiter or cut active during the run; run-to-run temperature comparable.

## Worked example
A first run ends at 5000 rpm, lambda 0.91 against a 0.88 target. Fuel is added to the rows that were active. The next run extends to 5500.

## Disputed / conflicts
Cross-check: The combustion textbook describes mixture being enriched towards maximum power near wide-open throttle (p.834), which agrees. Run-length and step rules are practice.

## Citations
- practice: Practitioner training and tuning practice, distilled and cross-checked.
- engineering-texts: Engine, combustion, charging and control engineering texts.
