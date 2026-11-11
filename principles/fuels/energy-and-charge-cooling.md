---
id: principles/fuels/energy-and-charge-cooling
title: Fuel energy, latent heat and charge cooling
layer: L0
status: draft
confidence: medium
sources: [engineering-texts, reference-data]
verified: 2026-11-10
applies_to: {fuels: [gasoline, ethanol, methanol], engines: [all]}
depends_on: [principles/fuels/stoichiometry-and-lambda]
supersedes: []
---

# Fuel energy, latent heat and charge cooling

## Claim
Per kilogram of air, gasoline, ethanol and methanol release nearly the same heat at stoichiometric. Alcohols make more power mainly by cooling the charge and resisting knock, and they need far more fuel flow.

## Why (derivation)
Energy per kg of air at lambda 1 is LHV / AFR_stoich: about 2.9 to 3.1 MJ/kg for all three, despite LHV falling from about 43 to 20 MJ/kg.
Fuel mass per unit of air rises by the ratio of stoichiometric AFRs: about 1.6 times for ethanol and 2.3 times for methanol.
Evaporating fuel takes heat from the charge. The upper bound on the temperature drop is
dT = h_fg / (lambda x AFR_stoich x c_p,air), about 21 K for gasoline and 187 K for methanol at lambda 1.
The real drop is much smaller, because some of the heat comes from walls and not all the fuel evaporates before the valve closes.

## Assumptions
Property values vary with composition and temperature. The cooling figure is a bound, not a prediction.

## Breaks when
Port injection on a hot wall takes much of the latent heat from the metal. Very rich alcohol mixtures may not fully evaporate at all, which raises wall wetting and oil dilution.

## Practical use
Use the fuel ratio to check injector and pump capacity before any change of fuel. Do not expect a power gain from the alcohol's energy; expect it from extra knock margin allowing more timing or boost.

## Worked example
Moving a gasoline engine to E85 at the same lambda: 14.7 / 9.8 = 1.5 times the fuel mass. By mass that takes an injector at 60 % duty to 90 %. The denser fuel delivers a little more mass per cc, so the real figure is near 86 %, already at a common duty ceiling.

## Disputed / conflicts
Published latent heats differ (methanol about 1100 to 1215 kJ/kg). The calculators use one table for consistency.

## Citations
- engineering-texts: Engine, combustion, charging and control engineering texts.
- reference-data: Published reference data: thermophysical properties, fuel data, sensor and injector data sheets, statistics.
