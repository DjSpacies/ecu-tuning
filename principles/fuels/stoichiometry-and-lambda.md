---
id: principles/fuels/stoichiometry-and-lambda
title: Stoichiometry and lambda across fuels
layer: L0
status: draft
confidence: high
sources: [engineering-texts, reference-data]
verified: 2026-11-10
applies_to: {fuels: [gasoline, ethanol, methanol], engines: [all]}
depends_on: []
supersedes: []
---

# Stoichiometry and lambda across fuels

## Claim
Lambda is the fuel-independent measure of mixture. The stoichiometric air-fuel ratio differs by fuel, roughly 14.7 for gasoline, 9.0 for ethanol and 6.5 for methanol, so an AFR number means nothing without the fuel.

## Why (derivation)
For a fuel CcHhOo, complete combustion needs c + h/4 - o/2 moles of O2. Air carries 4.773 moles per mole of O2 at a molar mass of 28.96 g/mol, so
AFR_stoich = (c + h/4 - o/2) x 4.773 x 28.96 / (12.011 c + 1.008 h + 15.999 o).
Oxygen already in an alcohol reduces the air needed, which is why alcohols have low stoichiometric ratios.
Lambda = AFR_actual / AFR_stoich. A blend needs air in proportion to each component's mass, so AFR_stoich(blend) is the mass-weighted mean.

## Assumptions
Gasoline is a varying mixture: 14.7 is a convention, and the true value depends on composition and oxygenate content. Blend calculations need the actual ethanol content, which is often below the label.

## Breaks when
Pump gasoline with ethanol has a lower true stoichiometric ratio than 14.7. Seasonal E85 can hold well under 85 % ethanol. A wideband reports lambda whatever AFR scale it displays, so a gasoline-scaled display on alcohol is only useful after dividing by 14.7.

## Practical use
Reason and tune in lambda. Use `principles/calculators/fuels.py`. Convert any AFR reading to lambda using the scale the instrument is set to, not the fuel in the tank.

## Worked example
Ethanol C2H6O: (2 + 1.5 - 0.5) x 4.773 x 28.96 / 46.07 = 9.0. E85 by volume with densities 789 and 745 kg/m3 is 85.7 % ethanol by mass, so AFR_stoich = 0.857 x 8.97 + 0.143 x 14.7 = 9.8. A target of lambda 0.80 is AFR 7.85.

## Disputed / conflicts
Sources give slightly different values for the same fuel (methanol 6.43 to 6.47, ethanol 8.94 to 9.0, gasoline 14.6 to 15.0) because they assume different air and fuel compositions. The differences are small beside real fuel variation.

## Citations
- engineering-texts: Engine, combustion, charging and control engineering texts.
- reference-data: Published reference data: thermophysical properties, fuel data, sensor and injector data sheets, statistics.
