---
id: methodology/catalyst-emissions
title: Tuning a car that keeps its catalytic converter
layer: L2
status: draft
confidence: medium
sources: [practice]
verified: 2026-11-11
applies_to: {fuels: [gasoline, ethanol, methanol], engines: [all]}
depends_on: [methodology/closed-loop-fuel, methodology/combustion-afr-targets, principles/fuels/stoichiometry-and-lambda]
supersedes: []
---

# Tuning a car that keeps its catalytic converter

## Claim
A three-way catalyst needs the mixture held at stoichiometric and cycled slightly either side of it, needs to light off quickly from cold, and is destroyed by unburnt fuel burning in the exhaust and by excessive exhaust temperature. Where a catalyst is fitted or emissions compliance matters, those needs constrain idle and cruise targets, cold start, full-load targets, launch and anti-lag strategies.

## Why (derivation)
Factory calibrations target stoichiometric at idle and cruise, and well into moderate load, because the combined tailpipe output of CO, HC and NOx after a three-way catalyst is lowest there. Economy is secondary for the manufacturer: emissions compliance is the gate to production. The catalyst converts best when the mixture alternates slightly rich and lean of stoichiometric rather than sitting exactly on it, so factory closed-loop control deliberately dithers the target around stoichiometric. Without that cycling the catalyst does not convert efficiently, which is why closed loop with rich-lean cycling is described as essential for an emissions test.

Catalysts are damaged by heat and by combustion in the exhaust. Ignition-cut strategies (ignition-cut launch control, anti-lag) send unburnt mixture into the exhaust where it ignites; the sources describe this destroying a catalyst almost immediately. Sustained full load raises exhaust temperature, and factory calibrations model exhaust temperature in software (after characterising it with fast thermocouples during development), mainly for catalyst protection, rather than fitting a sensor.

Light-off is about putting heat into the exhaust: factory cold-start strategies raise idle speed and retard ignition heavily for the first period after start to cut cold-start hydrocarbons.

## Assumptions
A three-way catalyst on a gasoline or alcohol-blend engine with closed-loop lambda control. Diesel aftertreatment is out of scope.

## Breaks when
- No catalyst is fitted and emissions compliance does not apply: dithering brings no benefit, and lean cruise for economy becomes an option.
- The catalyst has been removed or replaced with a high-flow unit on a factory ECU: catalyst-efficiency diagnostics may trip (methodology/reflash-tuning).

## Practical use
- Ask first whether a catalyst is fitted and whether the car must pass an emissions test. That decides the idle and cruise strategy.
- With a catalyst and compliance needs: keep closed loop at stoichiometric at idle and cruise, and use target oscillation (dither) if the ECU offers it. Without a catalyst, leave oscillation off.
- Use fuel-cut, not ignition-cut, launch control on a car with a catalyst, and make sure the engine sits smoothly on the limiter. Do not use anti-lag with a catalyst.
- At full load, one demonstration tapered the lambda target richer with rpm (from about 0.90 to about 0.87 at 8000 rpm) to control exhaust temperature for the catalyst.
- Keep any factory catalyst-protection enrichment unless it has been replaced by an equivalent strategy; when it is changed for logging, restore it afterwards.
- For cold start on a road car with a catalyst, the factory approach of raised idle with retarded timing is the reference behaviour.

### Diagnostic tests
- **Dither working or not.** In a closed-loop idle or cruise log, lambda should cycle slightly about stoichiometric at a regular rate. A flat trace with dither enabled, or a trace sitting persistently to one side, points at the controller or the base table.
- **Exhaust heat at full load.** Where EGT is measured, compare it across pulls as the target is changed; where it is not, a factory ECU's modelled exhaust temperature or its catalyst-protection enrichment activity can show when protection is acting.

## Worked example
A road car with a catalyst cruises at lambda 1.00 in closed loop. The owner asks for a lean cruise target of 1.05 for economy. Because the car keeps its catalyst and must pass emissions testing, the cruise target stays at stoichiometric with dither enabled; the economy request is recorded as applicable only to a car without those constraints.

## Disputed / conflicts
- **Lean cruise for economy.** One source notes that a small economy gain is available slightly lean of stoichiometric and that aftermarket street tunes sometimes target it; the same source cautions that lean cruise raises net emissions and stops the catalyst working properly. Both hold: the choice depends on whether a catalyst and compliance apply.
- **Why stoichiometric.** A common belief is that factory calibrations sit at stoichiometric because it is best for economy. The sources say instead that it is chosen for catalyst conversion and combined emissions, with economy as a reasonable by-product.

## Citations
- practice: Practitioner training and tuning practice, distilled and cross-checked.
