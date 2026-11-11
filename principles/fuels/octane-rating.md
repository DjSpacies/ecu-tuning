---
id: principles/fuels/octane-rating
title: What octane numbers measure
layer: L0
status: draft
confidence: high
sources: [engineering-texts, astm-fuel-standards, reference-data, practice]
verified: 2026-11-11
applies_to: {fuels: [gasoline, ethanol, methanol], engines: [all]}
depends_on: []
supersedes: []
---

# What octane numbers measure

## Claim
Octane number ranks resistance to autoignition under two fixed test conditions. It is not a measure of energy or of how much power a fuel makes, and in a real boosted engine a fuel's knock resistance can differ a lot from its label.

## Why (derivation)
RON and MON are measured in a single-cylinder test engine by raising compression until a standard knock intensity is reached, then bracketing the fuel with reference blends of isooctane and n-heptane. MON runs hotter and faster than RON, so most fuels score lower on it. Pump labels may use RON or (R+M)/2 (the antiknock index). Sensitivity, RON minus MON, describes how differently a fuel behaves at low and high charge temperature; alcohols have high sensitivity, so their real-world resistance in a boosted engine can exceed what either number alone implies.
Alcohols add a second effect the rating does not capture: their latent heat cools the charge (`principles/fuels/energy-and-charge-cooling`), lowering the end-gas temperature that drives knock. Practitioners note that pure ethanol, rated around the low 100s, behaves in boosted engines like race fuels rated well above 110, and that one back-to-back test at very high boost found E85 and a high-octane race gasoline almost identical in power, both reaching MBT.

## Assumptions
Standard test conditions; the engine in question does not match them.

## Breaks when
- Comparing labels across regions (RON against AKI). Using one number for a fuel in an engine with very different temperature and pressure history from the test.
- The fuel in the tank is not the fuel on the label: stale fuel, a customer's own mix of race and pump fuel, additive dosing, or oil ingestion in a worn engine all change effective resistance.

## Practical use
- Confirm which rating a fuel's label uses; a number is meaningless without its method.
- Treat octane as an input to how much margin to expect, and never as a licence to advance timing without knock evidence from this engine.
- Tune on the exact fuel the engine will run. Practitioners refuse to tune on a better fuel than the owner will use: a tune made on a higher grade leaves timing and boost unsafe on the lower one. One recalls a familiar combination that knocked, took no timing and was well down on power until it was found to be on a lower grade than intended.
- Prefer a single defined fuel (a pump grade, an ethanol blend, or a proper race fuel) over mixtures and additives. A tune made on a mix is only safe while the exact ratio is repeated every fill; one practitioner tells of an engine tuned on a race and pump fuel mix that melted its pistons within weeks.
- Bottled octane boosters gave little or nothing in one practitioner's informal dyno tests, and they make octane vary from tank to tank.

## Worked example
A fuel sold as 98 RON and another as 93 AKI may be close to each other: AKI is the average of RON and MON, so a 98 RON fuel with 88 MON has an AKI of 93. Practitioners treat a 98-rated fuel in Europe or New Zealand as roughly equal to a 93 AKI fuel in the US.

## Disputed / conflicts
- One practitioner suggests pump E10 often uses a lower-octane base gasoline, so blending ethanol into the best available premium may give a small gain. This is opinion; base-stock practice varies by market.
- Practitioners' estimate that pure ethanol behaves like a fuel rated 116 to 120 or more is practical judgement, not a measured rating; octane sensitivity and charge cooling are the textbook explanations for the gap.

## Citations
- astm-fuel-standards: D2699 and D2700 (superseded editions, for method only).
- engineering-texts: Engine, combustion, charging and control engineering texts.
- reference-data: Published reference data: thermophysical properties, fuel data, sensor and injector data sheets, statistics.
- practice: Practitioner training and tuning practice, distilled and cross-checked.
