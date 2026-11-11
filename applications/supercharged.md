---
id: applications/supercharged
title: Supercharged profile
layer: L4
status: draft
confidence: low
sources: [engineering-texts]
verified: 2026-11-10
applies_to: {fuels: [gasoline, ethanol, methanol], engines: [supercharged]}
depends_on: [principles/boost/compressor-and-surge, applications/turbocharged]
supersedes: []
---

# Supercharged profile

## Claim
A mechanically driven supercharger ties boost to engine speed and has no exhaust energy feedback, so boost comes earlier and is more predictable, at the price of drive power.

## Why (derivation)
The compressor is geared to the crank, so airflow follows rpm directly. There is no turbine pressure lag, but compressor heat and drive losses remain.

## Assumptions
Bypass valve behaviour is known.

## Breaks when
Different types (roots, screw, centrifugal) have very different boost-versus-speed curves.

## Practical use
Use the turbocharged step procedure, but treat a centrifugal unit as near full boost only at high rpm.

## Worked example
A roots-type unit reaches near its full boost well below peak rpm, so load cells are reached early in a pull.

## Disputed / conflicts
None recorded.

## Citations
- engineering-texts: Engine, combustion, charging and control engineering texts.
