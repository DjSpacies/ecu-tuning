---
id: methodology/steady-state-fuel
title: Steady-state fuel tuning
layer: L2
status: draft
confidence: medium
sources: [practice, engineering-texts]
verified: 2026-11-10
applies_to: {fuels: [gasoline, ethanol, methanol], engines: [all]}
depends_on: [methodology/idle, principles/airflow/volumetric-efficiency]
supersedes: []
---

# Steady-state fuel tuning

## Claim
Tune fuel cell by cell in stable conditions, from low rpm and load upward, correcting towards a chosen lambda target, and do it before ignition.

## Why (derivation)
Mixture is the base for torque and knock behaviour, and combustion is more sensitive to error in mixture than to a small ignition error. Working outward from low load keeps each new cell close to values already proven.

## Assumptions
A correct fuel model and injector data, so corrections represent the engine's actual airflow.

## Breaks when
Interpolation means a cell's value also affects its neighbours. A change of throttle or an active enrichment contaminates the reading.

## Practical use
Hold the engine in the centre of the cell, let it settle, and correct. Copy a finished cell or column forward as a starting value for the next one.

## Decision rules
Correct by the ratio of measured to target lambda. For a small difference, a matching small percentage change is enough. Steady-state up to about two-thirds of redline, then check higher-rpm columns briefly. Keep knock monitoring on throughout. Add zones only where the engine's airflow changes faster than interpolation covers.

Lambda is never perfectly steady, so average by eye or by statistics and accept about 1 to 2 % from target. Start each new load rich and lean out towards target, since discovering lean under load is the dangerous direction. Keep audio knock monitoring on during fuel work. Erratic VE shapes signal a problem in that part of the table or a measurement fault.

## Data gates
Warm coolant and stable intake temperature; operating point centred in the cell; no transient or enrichment active; wideband valid.

## Worked example
A cell at lambda 0.92 has a target of 0.85. The correction is fuel times 0.92 / 0.85, a rise of about 8.2 %.

## Disputed / conflicts
Cross-check: textbooks support the physics of lambda and VE, and give no steady-state tuning procedure. The order and the 2/3-of-redline rule are practice.

## Citations
- practice: Practitioner training and tuning practice, distilled and cross-checked.
- engineering-texts: Engine, combustion, charging and control engineering texts.
