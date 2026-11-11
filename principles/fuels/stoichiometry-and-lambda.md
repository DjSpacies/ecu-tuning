---
id: principles/fuels/stoichiometry-and-lambda
title: Stoichiometry and lambda across fuels
layer: L0
status: draft
confidence: high
sources: [engineering-texts, reference-data, practice]
verified: 2026-11-11
applies_to: {fuels: [gasoline, ethanol, methanol], engines: [all]}
depends_on: []
supersedes: []
---

# Stoichiometry and lambda across fuels

## Claim
Lambda is the fuel-independent measure of mixture. The stoichiometric air-fuel ratio differs by fuel, roughly 14.7 for gasoline, 9.0 for ethanol and 6.5 for methanol, so an AFR number means nothing without the fuel. A fuel model that works in mass needs the correct stoichiometric ratio, and an error in it shifts every cell.

## Why (derivation)
For a fuel CcHhOo, complete combustion needs c + h/4 - o/2 moles of O2. Air carries 4.773 moles per mole of O2 at a molar mass of 28.96 g/mol, so
AFR_stoich = (c + h/4 - o/2) x 4.773 x 28.96 / (12.011 c + 1.008 h + 15.999 o).
Oxygen already in an alcohol reduces the air needed, which is why alcohols have low stoichiometric ratios.
Lambda = AFR_actual / AFR_stoich. A blend needs air in proportion to each component's mass, so AFR_stoich(blend) is the mass-weighted mean. Because ethanol and gasoline densities are close, it is also nearly linear in volume content, which is why tuners interpolate between about 14.7 at E0 and 9.0 at E100.
A model ECU computes fuel mass as air mass / (lambda_target x AFR_stoich), then converts mass to pulse width through density and injector flow. So the stoichiometric ratio acts as a multiplier on every cell: entering 14.7 for a fuel whose true value is 14.1 makes it about 4 % lean everywhere, and the VE table absorbs the error.

## Assumptions
Gasoline is a varying mixture: 14.7 is a convention, and the true value depends on composition and oxygenate content. Blend calculations need the actual ethanol content, which is often below the label.

## Breaks when
- Pump gasoline with ethanol has a lower true stoichiometric ratio than 14.7 (about 14.1 for E10, used by practitioners for US pump fuel). Seasonal E85 can hold well under 85 % ethanol.
- A wideband reports lambda whatever AFR scale it displays, so a gasoline-scaled display on alcohol is only useful after dividing by 14.7. An ECU showing AFR with the wrong stoichiometric setting shows misleading targets on any non-gasoline fuel.
- Oxygenated race fuels need more fuel for the same lambda; one practitioner found about 5 % more fuel and about 5 % more power when switching to one. The target lambda itself does not change.

## Practical use
- Reason and tune in lambda. Use `principles/calculators/fuels.py`. Convert any AFR reading to lambda using the scale the instrument is set to, not the fuel in the tank.
- Lambda also makes have-want arithmetic simple: 0.85 is 15 % richer than stoichiometric for any fuel.
- Set the fuel's real stoichiometric ratio, density and density temperature coefficient before tuning a model-based fuel table; where an ECU's list lacks a blend, a constant entry for that blend is a workaround.
- Water injection does not change the lambda target: water does not burn and does not shift the reading. A methanol mix adds fuel, and lambda 1 still means stoichiometric for the total.
- Never carry lambda or exhaust temperature targets across fuels without thinking: methanol drag engines run far richer (practitioners' examples 0.55 to 0.65) and much cooler than gasoline engines.

## Worked example
Ethanol C2H6O: (2 + 1.5 - 0.5) x 4.773 x 28.96 / 46.07 = 9.0. E85 by volume with densities 789 and 745 kg/m3 is 85.7 % ethanol by mass, so AFR_stoich = 0.857 x 8.97 + 0.143 x 14.7 = 9.8. A target of lambda 0.80 is AFR 7.85 on E85, and 0.80 x 14.7 = 11.76 on gasoline.
Percentages are easy to misread. Going from gasoline (14.7) to ethanol (9.0), the stoichiometric ratio falls by 39 %. The fuel mass needed for the same air rises by 14.7 / 9.0 = 1.63, that is 63 % more. Practitioners who quote "about 40 %" for this are describing the ratio change, or a volume figure for E85 rather than E100.

## Disputed / conflicts
Sources give slightly different values for the same fuel (methanol 6.4 to 6.47, ethanol 8.94 to 9.0, gasoline 14.6 to 15.0) because they assume different air and fuel compositions. The differences are small beside real fuel variation.

## Citations
- engineering-texts: Engine, combustion, charging and control engineering texts.
- reference-data: Published reference data: thermophysical properties, fuel data, sensor and injector data sheets, statistics.
- practice: Practitioner training and tuning practice, distilled and cross-checked.
