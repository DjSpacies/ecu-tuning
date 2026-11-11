---
id: principles/fuels/octane-rating
title: What octane numbers measure
layer: L0
status: draft
confidence: high
sources: [engineering-texts, astm-fuel-standards, reference-data]
verified: 2026-11-10
applies_to: {fuels: [gasoline, ethanol, methanol], engines: [all]}
depends_on: []
supersedes: []
---

# What octane numbers measure

## Claim
Octane number ranks resistance to autoignition under two fixed test conditions. It is not a measure of energy or of how much power a fuel makes.

## Why (derivation)
RON and MON are measured in a single-cylinder test engine by raising compression until a standard knock intensity is reached, then bracketing the fuel with reference blends of isooctane and n-heptane. MON runs hotter and faster than RON, so most fuels score lower on it. Pump labels may use RON or (R+M)/2 (the antiknock index). Sensitivity, RON minus MON, describes how differently a fuel behaves at low and high charge temperature; alcohols have high sensitivity, so their real-world resistance in a boosted engine can exceed what either number alone implies.

## Assumptions
Standard test conditions; the engine in question does not match them.

## Breaks when
Comparing labels across regions (RON against AKI). Using one number for a fuel in an engine with very different temperature and pressure history from the test.

## Practical use
Confirm which rating a fuel's label uses. Treat octane as an input to how much margin to expect, and never as a licence to advance timing without knock evidence from this engine.

## Worked example
A fuel sold as 98 RON and another as 93 AKI may be close to each other: AKI is the average of RON and MON, so a 98 RON fuel with 88 MON has an AKI of 93.

## Disputed / conflicts
None recorded.

## Citations
- astm-fuel-standards: D2699 and D2700 (superseded editions, for method only).
- engineering-texts: Engine, combustion, charging and control engineering texts.
- reference-data: Published reference data: thermophysical properties, fuel data, sensor and injector data sheets, statistics.
