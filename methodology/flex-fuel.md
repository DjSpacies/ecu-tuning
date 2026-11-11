---
id: methodology/flex-fuel
title: Flex fuel tuning
layer: L2
status: draft
confidence: medium
sources: [practice, reference-data]
verified: 2026-11-11
applies_to: {fuels: [ethanol, gasoline], engines: [all]}
depends_on: [principles/fuels/stoichiometry-and-lambda, principles/fuels/energy-and-charge-cooling]
supersedes: []
---

# Flex fuel tuning

## Claim
Tune the base fuel completely first, then tune the high-ethanol end on a verified known blend, then check intermediate blends. With correct fuel properties the fuel model carries most of the fuelling change by itself; ignition and boost must be blended so that low ethanol content is always the conservative case, and a sensor fault must fall back safely.

## Why (derivation)
Stoichiometry and knock resistance vary with ethanol content. The ECU interpolates between tables, so the endpoints must be valid and an unexpected low content must fall back to safe timing and boost.
In a model-based ECU the stoichiometric ratio, density and its temperature coefficient for each fuel are interpolated by measured content. The ratio alone acts as a global multiplier on fuel mass (14.7 / 9.0 = 1.63 times from E0 to E100), so if the properties and injector data are right, the engine should run close to target on a new blend before any retuning. What is left is small: a slight real VE gain from charge cooling, injector flow changes with viscosity that are impractical to model, general model error, and sensor tolerance (common sensors are rated about 5 %). A second VE table absorbs this as a correction, not as a change in airflow.
Knock resistance does not rise linearly. Practitioners put most of ethanol's benefit in the first 30 to 40 % (one estimates 80 to 85 % of it by E40), with little more beyond about E70, which agrees with NREL's non-linear octane effect. Ignition and boost therefore need a blend that is not simply linear in content, and the safe direction is to under-use the low-content gain.

## Assumptions
A verified content sensor and known behaviour on failure. The base fuel tune is complete, including injector data and fuel properties.

## Breaks when
- Sensor failure, seasonal fuel, or stale fuel in a line after a tank change.
- The sensor reads only what flows through it. On a return system, running the pump circulates the tank blend in a couple of minutes; on a returnless system with the sensor in the feed, the engine must run and drive for a few minutes before the reading reflects the tank.
- Residual fuel cross-blends. After draining an E85 tank and refilling with E10, one sensor read about 16 %; a first fill of supplier E85 read 74 % because 5 to 8 L of pump fuel stayed in the tank. Pump E85 also varies by batch and season (practitioners report winter blends of roughly 50 to 70 %).
- Newly enabled flex tables may hold arbitrary values from memory or defaults (one demonstration showed a second lambda target table pre-filled at 0.755), which silently corrupt fuelling until inspected.
- A pulse-width-based ECU without a flex model needs percentage fuel and timing trim tables against ethanol content (one practitioner uses about 40 % extra fuel at E100). It works but gives less control; dual-fuel switching between two full table sets is a different strategy for a known fuel in the tank.

## Practical use
### Order of work
1. Fit and verify the content sensor. It outputs a frequency (about 50 to 150 Hz across 0 to 100 % in the sources), so it goes to a frequency-capable digital input. It also measures temperature (its dielectric reading is temperature dependent), which gives a fuel temperature for density compensation; check that it reads sensibly.
2. On the fuel run most often, tune everything as a single-fuel car: VE, lambda targets, fuel properties including the charge-cooling coefficient, ignition, boost, cranking, post-start, warm-up, and road or track checks. Use the base fuel's real properties (about 14.1 for E10 pump fuel).
3. Enable the second fuel, enter its properties, and set the fuel blend table (0 % at E0, 100 % at the highest content expected).
4. Copy every primary table (VE, lambda targets, ignition, boost, cold start) into its secondary table before tuning; inspect every newly enabled table.
5. Drain thoroughly, fill with the second fuel, circulate, confirm the content reading, and tune the secondary tables as a dedicated ethanol tune, cold start included. Starting from the pump-fuel ignition values is conservative for ethanol.
6. Make two or three intermediate blends (for example about E20 to E25, E50 and E70, by draining to low and topping up with pump fuel). At each, check lambda against target and knock at high load.
Expect about three tunes' worth of work.

### Fuel
- Lambda targets are often the same as on pump fuel, but confirm. Make sure lambda targets are valid in the blended table, or VE values become meaningless.
- After entering the ethanol properties, a uniform closed-loop trim (for example +5 % at idle where pump fuel showed 0 %) most likely comes from the unmodelled viscosity effect; scale the whole secondary VE table by that factor, then refine local areas. Trims within about 3 to 4 % are ordinary day-to-day variation.
- Expect the secondary VE table within a few percent of the primary (practitioners report 2 to 6 % as normal). Larger differences, 10 to 15 % or more, suggest a setup error to find before tuning around it, although one practitioner saw about 17 % at one bar of boost on one engine with small differences at light load.
- If an intermediate blend misses target, correct it in the fuel blend table (for example, lean at E20 means more weighting towards table two there), not by editing either finished VE table.
- Acceleration enrichment and per-cylinder fuel trims usually carry across unchanged if injectors are characterised and the base table is right; one practitioner saw identical cylinder trims on 98 octane and E85.

### Ignition and boost
- Use separate pump and ethanol ignition and boost tables blended by content, so ethanol-level boost can never run on a mostly-gasoline tank.
- Bias the blend conservative at low content. Practitioners' examples: hold pure pump tables up to about E10 to E20, reach the full ethanol tables by about E70 (pump E85 often reads only 75 to 78 %), and blend between; for maximum power at intermediate blends, ramp more steeply early. Test knock at high load at 10 to 30 % ethanol, and reduce the ignition blend there if it knocks.
- Do not add a fixed timing offset. Where the engine was MBT-limited on gasoline, ethanol's faster burn moves MBT slightly later (about 2 degrees in one test at light load); where it was knock-limited, the gain can be large. Optimise ethanol timing on the dyno.
- Drift matters most at low content. From about E50 up, knock sensitivity changes little, so content error at the high end costs little; error at the low end is where damage is likely.

### Protection
- If the sensor fails, the fallback must be conservative (see Disputed / conflicts for how sources choose the default content).
- With a single lean-protection table, set the threshold leaner than the leanest target on any fuel, since it is a backstop for real faults.
- Clamp injector duty at the planned maximum: ethanol needs about 35 to 40 % more fuel volume than gasoline for E85, more for E100.

## Decision rules
Lambda targets are often the same as on pump fuel, but confirm. Make sure lambda targets are valid in the blended table, or VE values become meaningless. Make the low-ethanol ignition and boost tables safe. If the sensor fails, the fallback must be conservative.

Knock resistance rises most between E0 and about E40, so test some intermediate blends. Fuel temperature from the composition sensor must read sensibly, since it is used to correct the reading. Viscosity changes flow for a given pulse, so use data for each fuel where available. Cranking fuel must rise a lot on ethanol at low temperature.

As a start, raise cranking fuel by 25 to 50 % on ethanol and tune from there. Fuel pump estimates need a 35 to 40 % increase on ethanol. Cold-start enrichment does not transfer from gasoline by applying the normal ethanol increase alone: one practitioner expects about another 20 to 25 % at cold temperatures on top of it, and validates the low-ethanol cold start first. Use ethanol content as an axis on cranking and prime tables.

## Data gates
Measured ethanol content stable; known fuel in the line; fuel temperature plausible. Logged together for each blend test: ethanol content, fuel temperature, lambda and target, closed-loop trim, fuel blend weighting, ignition and boost blend weighting, per-cylinder knock.

## Worked example
Unexpectedly, a sensor reports 132 C fuel temperature. Do not trust the sensor or the data derived from it until the fault is fixed.
A second case from the sources: a 10:1 turbo engine was heavily knock-limited on pump fuel above about 1 bar, where timing had to fall sharply and extra boost gave no power (about 216 kW at the wheels). On E85 at a similar point (200 kPa absolute, 7500 to 8000 rpm) timing went from 16 to 17 degrees to 22 to 23 degrees at MBT, and the final tune made about 289 kW at about 1.5 bar until the injectors ran out. A heavily knock-limited pump tune is a strong sign of large ethanol gains; a NA engine already near MBT gains little (practitioners quote 5 to 15 hp on one NA engine).

## Disputed / conflicts
- **Cross-check.** NREL reports ethanol's effect on octane as non-linear, with diminishing effect as content rises, which agrees. The practitioners' figure of about E40 for most of the benefit is not confirmed there.
- **Sensor fault default.** One practitioner sets the fault default to about 85 % ethanol, reasoning that a high default runs a gasoline car rich, while a low default would run an ethanol car dangerously lean. The existing rule here is that the fallback must be conservative in ignition and boost. Both can hold where the ECU lets the fault state choose fuelling and timing separately: rich fuelling with pump-fuel timing and boost. Where one default content drives every blend, a high default also brings ethanol timing and boost to a car that may hold gasoline. Discriminating check: in the ECU, force the sensor fault and log which fuel, ignition and boost tables are applied.
- **Which properties to enter for the second fuel.** One practitioner enters E100 properties with a linear 0 to 100 % blend, so that a stronger home blend does not fall outside the range; ECU help guidance cited in the sources sets them for the blend actually used, such as E85. With E100 properties, an E82 fill weights about 82 % towards the second tables, which matters if the lambda targets differ.
- **Extra timing on ethanol.** One practitioner's rule of thumb is about 4 to 6 degrees more on forced induction and 2 to 4 on NA, confirmed by knock monitoring already quiet on gasoline. Another shows that the change depends on how knock-limited each region was: some cells need slightly less timing, some 10 degrees or more, and the common advice of a flat 10 degrees is wrong. The rule of thumb is a starting expectation only.
- **Blend shapes.** The same practitioner gives two shapes: curved, holding back at low content and ramping past about E40; and, for a car run on either pump fuel or E85, pure pump up to E20 and linear to E70. Physics (most knock benefit by E40) argues for an early ramp; safety argues for late. The choice is the owner's fuel habits.
- **Water in fuel.** The sensor reads water as ethanol. One practitioner considers this unimportant because enough water to matter is a bigger problem than the misreading.
- **Fuel injection timing.** One practitioner thinks the longer pulse on E85 might shift ideal injection timing slightly; with end-of-injection referencing he expects little change. Untested.

## Citations
- practice: Practitioner training and tuning practice, distilled and cross-checked.
- reference-data: Published reference data: thermophysical properties, fuel data, sensor and injector data sheets, statistics.
