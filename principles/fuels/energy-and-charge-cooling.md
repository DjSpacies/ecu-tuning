---
id: principles/fuels/energy-and-charge-cooling
title: Fuel energy, latent heat and charge cooling
layer: L0
status: draft
confidence: medium
sources: [engineering-texts, reference-data, practice]
verified: 2026-11-11
applies_to: {fuels: [gasoline, ethanol, methanol], engines: [all]}
depends_on: [principles/fuels/stoichiometry-and-lambda]
supersedes: []
---

# Fuel energy, latent heat and charge cooling

## Claim
Per kilogram of air, gasoline, ethanol and methanol release nearly the same heat at stoichiometric. Alcohols make more power mainly by cooling the charge and resisting knock, which allows more timing, boost or compression, and they need far more fuel flow.

## Why (derivation)
Energy per kg of air at lambda 1 is LHV / AFR_stoich: about 2.9 to 3.1 MJ/kg for all three, despite LHV falling from about 43 to 20 MJ/kg.
Fuel mass per unit of air rises by the ratio of stoichiometric AFRs: about 1.6 times for ethanol and 2.3 times for methanol.
Evaporating fuel takes heat from the charge. The upper bound on the temperature drop is
dT = h_fg / (lambda x AFR_stoich x c_p,air), about 21 K for gasoline and 187 K for methanol at lambda 1.
The real drop is much smaller, because some of the heat comes from walls and not all the fuel evaporates before the valve closes. Water has roughly six times the latent heat of gasoline per kg and releases no energy, which is why water injection cools strongly but adds nothing to combustion.
Cooling raises charge density slightly (practitioners put the real VE gain from ethanol's cooling at only a percent or two) and, more importantly, lowers the end-gas temperature that drives knock. A cooler charge with a knock-resistant fuel is why methanol engines tolerate very high compression and boost, and why some short-duration methanol drag engines run very high boost without an intercooler.

## Assumptions
Property values vary with composition and temperature. The cooling figure is a bound, not a prediction.

## Breaks when
- Port injection on a hot wall takes much of the latent heat from the metal. Very rich alcohol mixtures may not fully evaporate at all, which raises wall wetting and oil dilution.
- Direct injection: the point in the cycle where fuel is injected changes how much of the cooling the charge receives, so injection timing can move the knock-limited advance; it needs testing per engine.
- Alcohols are close to single-component fuels and evaporate around one much higher temperature than gasoline's light ends, so in the cold they barely evaporate at all (see `methodology/cold-start-warmup`).

## Practical use
- Use the fuel ratio to check injector and pump capacity before any change of fuel. Do not expect a power gain from the alcohol's energy; expect it from extra knock margin allowing more timing or boost. On an engine that already reaches MBT on gasoline, the gain from an alcohol is small.
- A model ECU's charge-cooling coefficient depends on latent heat and fuel quantity, so it will likely differ between gasoline and E85; recalibrate it on the new fuel by the same step test, and address it for dual-fuel and flex setups.
- Intake temperature correction for air density is a gas-law effect and does not change with fuel. What may change is the extra high-temperature enrichment and retard used for knock protection, which a better fuel may need less of.
- Exhaust temperatures are notably lower on E85 and much lower on methanol. Practitioners find turbo spool on E85 is not much different despite the lower EGT, attributing it to the larger fuel mass increasing exhaust mass flow. Set safe EGT expectations per fuel: gasoline-like EGT on a methanol engine signals a seriously lean condition.

## Worked example
Moving a gasoline engine to E85 at the same lambda: 14.7 / 9.8 = 1.5 times the fuel mass. By mass that takes an injector at 60 % duty to 90 %. The denser fuel delivers a little more mass per cc, so the real figure is near 86 %, already at a common duty ceiling.
Exhaust temperature by fuel, from the sources' logs: a six-cylinder methanol drag engine settled near 720 to 735 C late in a pass, against about 875 to 915 C for a four-cylinder on leaded race gasoline; a methanol rotary at full boost showed 750 to 770 C before the turbine at about lambda 0.62.

## Disputed / conflicts
- Published latent heats differ (methanol about 1100 to 1215 kJ/kg). The calculators use one table for consistency.
- **Why methanol makes more power.** One practitioner explains it by the much larger fuel mass burned per cycle (2.5 to 3 times gasoline) multiplying a heating value about half of gasoline's. Per kilogram of air, the stoichiometric energy is only about 5 to 6 % higher for methanol, and fuel beyond the available oxygen cannot release its full heating value. The physics points instead to charge cooling, more moles of product per mole of charge, and the knock margin that allows more timing and boost. Discriminating test: compare torque on both fuels at the same lambda and at MBT on an engine with no knock limit on gasoline; a large gain there would support the practitioner's view.
- **Rich mixture and knock on E85.** Practitioners agree extra fuel cools the charge and reduces knock on alcohol as on gasoline, but note alcohol engines at very high boost are more prone to pre-ignition, possibly from oil washed into the charge by very rich mixtures. The mechanism is not settled.

## Citations
- engineering-texts: Engine, combustion, charging and control engineering texts.
- reference-data: Published reference data: thermophysical properties, fuel data, sensor and injector data sheets, statistics.
- practice: Practitioner training and tuning practice, distilled and cross-checked.
