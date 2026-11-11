---
id: applications/direct-injection
title: Direct injection profile
layer: L4
status: draft
confidence: low
sources: [engineering-texts, practice]
verified: 2026-11-10
applies_to: {fuels: [gasoline, ethanol, methanol], engines: [all]}
depends_on: [principles/fueling/injector-flow-and-dead-time]
supersedes: []
---

# Direct injection profile

## Claim
Direct injection puts fuel in the cylinder under high pressure, so injection timing, pump capacity and evaporation time are additional limits.

## Why (derivation)
The fuel evaporates in the cylinder, cooling the charge directly and changing the knock limit. The available time window shrinks with rpm.

## Assumptions
Fuel pressure is measured.

## Breaks when
Port-injection rules on dead time and wall film do not transfer directly.

## Practical use
Instruction coverage is thin in this corpus (one dedicated lesson), so treat DI work as needing extra caution and vendor data.

## Worked example
At high rpm the injection window shrinks, so fuelling can be limited by time before it is limited by flow.

## Disputed / conflicts
None recorded.

## Citations
- engineering-texts: Engine, combustion, charging and control engineering texts.
- practice: Practitioner training and tuning practice, distilled and cross-checked.
