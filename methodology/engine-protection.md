---
id: methodology/engine-protection
title: Setting up engine protection
layer: L2
status: draft
confidence: low
sources: [practice]
verified: 2026-11-10
applies_to: {fuels: [gasoline, ethanol, methanol], engines: [all]}
depends_on: [methodology/boost-control]
supersedes: []
---

# Setting up engine protection

## Claim
Configure ECU protection before relying on the engine: a rev limit, a boost limit, and reductions as temperatures climb, with sensor faults treated as a reason to limit, not ignore.

## Why (derivation)
A driver cannot watch every value. A protection strategy reacts when conditions go wrong, and an interpolated limit gives a gradual response.

## Assumptions
The ECU offers the function and the sensors exist.

## Breaks when
A faulty sensor can trigger a false limit, or disable one, so range checks are also needed.

## Practical use
Set conservative values at first and raise them only with evidence. Never disable a protection to complete a tune.

## Decision rules
Start with a rev limit and a boost cut. Lower the rev limit progressively with rising coolant temperature; note a table interpolates between its points. A fuel cut is generally preferred for a rev limit, and check whether a control range makes the cut begin before the set value. Protect against faulted sensors.

Set oil pressure protection by engine speed; a common rule of thumb is about 10 psi per 1000 rpm, for an engine with no better data. A rev limit by fuel cut is generally preferred over ignition cut, which can damage valvetrain in some applications; check the ECU's advice for group-fire injection. Check whether a control range starts cutting before the limit. Turbine materials suffer above about 1000 to 1050 C sustained exhaust temperature.

An practitioner once preferred ignition cut and later training sessions prefer fuel cut: see Disputed. Exhaust gas temperature much over about 900 C on gasoline is a concern for one practitioner.

## Data gates
Protections show as active in a log channel.

## Worked example
A boost cut set well above the target does nothing useful. Set it just above the highest target, with a small re-enable margin.

## Disputed / conflicts
Cross-check: no textbook here supports the oil pressure rule of thumb or the 1000 to 1050 C turbine figure. Treat both as practice guides, and use engine or turbo manufacturer data where available. Practitioners disagree between training sessions on fuel against ignition cut for rev limiting: 084, 253, 350 and 374 prefer fuel, and 036 prefers ignition. The valvetrain concern and the ECU maker advice for group fire both matter; choose per engine.

## Citations
- practice: Practitioner training and tuning practice, distilled and cross-checked.
