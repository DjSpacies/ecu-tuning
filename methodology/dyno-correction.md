---
id: methodology/dyno-correction
title: Dyno correction and comparing dyno numbers
layer: L2
status: draft
confidence: medium
sources: [practice, sae-j1349]
verified: 2026-11-11
applies_to: {fuels: [gasoline, ethanol, methanol], engines: [all]}
depends_on: [methodology/dyno-procedure, principles/thermo/air-density]
supersedes: []
---

# Dyno correction and comparing dyno numbers

## Claim
Atmospheric correction rescales measured power to a reference air state so that runs on different days or at different sites can be compared; it does not make different dynos, setups or drivetrains comparable. The trustworthy quantity is the change from a baseline on the same dyno, set up the same way, with correction applied the same way. Flat wheel-to-flywheel percentages and brand-to-brand conversion factors are rough at best.

## Why (derivation)
### Air state
At wide-open throttle the mass of air an engine draws is roughly proportional to inlet air density, ρ = p_dry / (R T), with p_dry the dry-air partial pressure (kPa), R = 0.287 kJ/(kg K) and T the inlet temperature (K). Hot or thin air carries less oxygen per cylinder fill, so indicated power falls. A correction factor of the form CF = (p_ref / p_dry) x (T / T_ref)^0.5 scales measured power to reference conditions; the square-root temperature term comes from compressible flow past the throttle rather than pure density. The calculator principles/calculators/correction.py implements this textbook form with a reference of 99 kPa dry air and 25 C. Training material introduces standard conditions as about 101.3 kPa and 15 C; different standards use different references, so corrected numbers are only comparable when the same standard is used.

### What correction cannot fix
The correction models only the air entering the engine. It does not model:
- driveline and tyre losses, which differ by gear, tyre compound and pressure, strapping, dyno type (hub versus roller) and temperature of the driveline;
- ramp rate, which changes the share of torque spent accelerating the rotating parts;
- the dyno's own calibration, control and resolution;
- engine responses that are not proportional to air density, such as a turbo system holding a boost target, knock-limited timing pulled at high intake temperature, or ECU trims reacting to temperature.

So the same car read about 183 kW at the wheels on a hub dyno and about 143 kW on a roller dyno in one demonstration, with the same fuel, tyres and tune; most of the gap is the tyre contact patch. No air correction would remove that.

## Assumptions
- The dyno records barometric pressure, inlet air temperature and, ideally, humidity at the engine inlet, not somewhere unrepresentative.
- The correction standard in use is known and is the same across the runs being compared.

## Breaks when
- Boosted engines with closed-loop boost control: the turbo compensates partly for thin air, so a density correction can overstate the change.
- Knock-limited engines on hot days: the ECU pulls timing, which is a real loss that correction treats as an air-density effect only partially.
- Inlet temperature measured at the dyno cell rather than at the engine intake, especially with intakes drawing hot under-bonnet air.
- Comparing across dyno brands, operators or sessions with different tyres or strapping.

## Practical use
- Use one repeatable dyno and compare session to session on that dyno. Record the correction standard, tyres, pressures, strapping, gear and ramp rate so a returning car is tested the same way.
- Understand how your dyno applies correction rather than trusting it blindly. One practitioner reports that over many years a winter-tuned car retested in summer never matched perfectly after correction.
- Treat wheel-to-flywheel conversion with a flat percentage as an approximation for jobs that need only a rough flywheel figure, for example scaling a torque model in a transmission controller, where the sources accept a nominal loss of about 10 % because exactness is not needed. Do not use it to rate an engine.
- Turbocharger power ratings are flywheel figures; relating them to wheel power on a particular dyno is unreliable.
- When real-world output matters (drag cars), trap speed is a hard-to-fake check on power, provided the runs are consistent (see methodology/road-procedure for its limits).
- Log-based "virtual dyno" estimates are a separate tool with their own errors; see methodology/road-procedure.

## Worked example
A naturally aspirated engine reads 150 kW at the wheels on a day with 95 kPa barometric pressure, 1.5 kPa vapour pressure and 35 C (308 K) inlet air. Dry pressure is 93.5 kPa. CF = (99 / 93.5) x (308 / 298)^0.5 = 1.059 x 1.017 = 1.077, so the corrected figure is about 161.5 kW. A month later the same car on the same dyno reads 158 kW at 99.5 kPa, 1.0 kPa vapour, 20 C (293 K): CF = (99 / 98.5) x (293 / 298)^0.5 = 1.005 x 0.991 = 0.996, corrected about 157.5 kW. The corrected figures suggest a loss of about 4 kW, but before acting, check tyres, pressures, strapping, gear, ramp rate and driveline temperature against the records; any of those can move a roller-dyno reading by that much.

## Disputed / conflicts
- Correction accuracy: the textbook correction is presented in training material as the way to compare days and sites; one practitioner's experience is that it never reconciles seasons perfectly. Both can hold: the correction is right for the air, and the residual is everything else. Discriminating test: the same car, same setup, measured at two clearly different air states with all other records matched.
- Brand offsets: one practitioner estimates his dyno reads about 10 % below another brand; other practitioners call any fixed inter-dyno or drivetrain-loss percentage meaningless across cars and power levels. Keep both; neither is a constant.
- Reference conditions: the training figure (about 101.3 kPa, 15 C) and the calculator's reference (99 kPa dry, 25 C) differ; quote which one is used with any corrected number.

## Citations
- sae-j1349: reference conditions, pages 1-9 (formula section not in the copy on hand).
- practice: Practitioner training and tuning practice, distilled and cross-checked.
