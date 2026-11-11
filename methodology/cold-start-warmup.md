---
id: methodology/cold-start-warmup
title: Cold start and warm-up
layer: L2
status: draft
confidence: medium
sources: [practice, engineering-texts]
verified: 2026-11-10
applies_to: {fuels: [gasoline, ethanol, methanol], engines: [all]}
depends_on: [methodology/transient-tuning]
supersedes: []
---

# Cold start and warm-up

## Claim
Cold tuning needs a truly cold engine. Start with large changes, because cold-engine feedback windows are short, and treat wideband data early in a cold start with caution.

## Why (derivation)
Cold walls hold more fuel as film, so far more must be injected for the same in-cylinder mixture. Only minutes are available before the engine has warmed past the range being tuned.

## Assumptions
A warm-up lasting long enough to observe, and the engine cold-soaked to the condition being tuned.

## Breaks when
A wideband needs its own warm-up. Readings straight after starting can be wrong or absent.

## Practical use
Use several cold starts across days, focusing where the engine will actually be started.

## Decision rules
Target slightly richer than warm idle while cold (about 0.95 is a typical example, until roughly 30 to 40 C). Make reasonably large changes per test. Ensure the wideband is powered early. Tune cold-idle air separately. Enrichment usually reduces with rising load.

Aim for a crisp start with the smallest enrichment that achieves it, since over-fuelling on start fouls plugs. Tune the main VE table first: cold enrichment is meant as a percentage on top of it. Keep some ignition reserve when cold. Ethanol blends need much more cranking fuel at low temperature.

Do not richen beyond about lambda 0.80 to 0.85 cold, because of plug fouling.

## Data gates
Coolant temperature at the condition being tuned; wideband ready; ambient and fuel temperature noted.

## Worked example
An engine at 33 C is too warm to tune for a 15 C start. Tune when actually cold-soaked.

## Disputed / conflicts
Cross-check: Engine textbooks both describe cold-start and warm-up enrichment as a function of engine temperature. Neither gives a procedure, so the specific steps here are practice.

## Citations
- practice: Practitioner training and tuning practice, distilled and cross-checked.
- engineering-texts: Engine, combustion, charging and control engineering texts.
