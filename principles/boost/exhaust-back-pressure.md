---
id: principles/boost/exhaust-back-pressure
title: Exhaust back pressure
layer: L1
status: draft
confidence: medium
sources: [engineering-texts]
verified: 2026-11-10
applies_to: {fuels: [gasoline, ethanol, methanol], engines: [turbo, supercharged, na]}
depends_on: [principles/airflow/volumetric-efficiency]
supersedes: []
---

# Exhaust back pressure

## Claim
Exhaust pressure opposes the outgoing gas and holds residuals in the cylinder. A turbo running pressure ratio across its turbine raises it and reduces knock margin and VE.

## Why (derivation)
Higher exhaust pressure leaves more hot residual gas after the exhaust stroke. That displaces fresh charge, raises the temperature of what is trapped, and costs pumping work. Turbine sizing sets how much back pressure a given boost costs. The ratio of exhaust to manifold pressure is therefore a key condition for both VE and knock.

## Assumptions
Exhaust pressure is measured in the manifold; few installations log it.

## Breaks when
At high overlap, exhaust pulses can help or hurt scavenging, so mean pressure alone does not predict VE.

## Practical use
If exhaust pressure is logged, compare it to manifold pressure across the rev range. If timing must be reduced at the top of the rev range without an obvious fuel or temperature reason, ask about turbine sizing and back pressure.

## Worked example
At 200 kPa manifold and 300 kPa exhaust, the pressure across the engine opposes filling, and a tune that was knock-free at lower speed may need less timing at high rpm.

## Disputed / conflicts
None recorded.

## Citations
- engineering-texts: Engine, combustion, charging and control engineering texts.
