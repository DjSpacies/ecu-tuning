---
id: applications/supercharged
title: Supercharged profile
layer: L4
status: draft
confidence: medium
sources: [engineering-texts, practice]
verified: 2026-11-11
applies_to: {fuels: [gasoline, ethanol, methanol], engines: [supercharged]}
depends_on: [principles/boost/compressor-and-surge, principles/boost/intercooling, applications/turbocharged]
supersedes: []
---

# Supercharged profile

## Claim
A mechanically driven supercharger ties compressor speed to engine speed and has no exhaust energy feedback, so boost is predictable from rpm and arrives without turbine lag, at the price of drive power. The boost-versus-rpm shape, charge temperature and drive loss depend strongly on the type: Roots, twin-screw or centrifugal.

## Why (derivation)
The compressor is geared or belted to the crank, so airflow capacity follows rpm directly. There is no turbine back pressure and no boost threshold set by exhaust energy, but compressor heat and drive losses remain.
- Roots (positive displacement, no internal compression): flow tracks crank speed, giving boost almost off idle and a fairly flat curve. Efficiency is reasonable at low speed and boost (around 80 to 90 % in the sources) but falls to roughly 50 to 55 % at high pressure ratio, so high boost means a very hot charge, and drive power is large (tens of horsepower in the sources).
- Twin-screw (positive displacement with internal compression): cooler charge and less drive power per unit of boost than a Roots, so more power at the same boost, though still less efficient than a well-sized turbo compressor (around 75 to 80 %) at high boost.
- Centrifugal: a compressor wheel run at very high speed through a step-up drive. Boost is near zero at low rpm and rises steadily with rpm to the rev limit, so torque is skewed to high rpm; for a given peak boost it gives the most top-end power, the coolest charge and the lowest drive loss.

## Assumptions
Bypass valve behaviour is known. Drive ratio (pulley sizes) is fixed for the calibration.

## Breaks when
- Different types have very different boost-versus-speed curves, so a turbo-style assumption about where load cells are reached does not transfer.
- Worn rotor and case clearances on positive-displacement units leak and drop boost over time.
- Pulley misalignment between crank and blower drive causes reliability problems on centrifugal units; the bracket must be accurate and rigid.
- Valley-mounted positive-displacement units usually rely on a manifold-integrated water-to-air core with limited area, so charge temperature ends up higher than with a large front air-to-air core.

## Practical use
- Use the turbocharged step procedure, but treat a centrifugal unit as near full boost only at high rpm, and expect a positive-displacement unit to reach high load cells early in a pull and in normal driving.
- Boost changes by pulley ratio rather than by a wastegate duty table; where a bypass valve controls boost, verify its behaviour and its effect on part-throttle airflow before tuning.
- A blow-off or bypass valve on a centrifugal unit does not keep the compressor spinning, since its speed is tied to the crank, but it still relieves thrust loading on lift. It vents a lot of air, including at idle and closed-throttle high rpm, so recirculate it to the intake ahead of the compressor to avoid noise.
- Log charge temperature through long pulls, especially on Roots and water-to-air layouts, and set charge-temperature timing protection accordingly.
- Break-in follows the turbo approach: limit throttle so boost stays low early, stepping up as break-in progresses.
- One practitioner's view: a Roots blower is chosen mainly for looks or period builds; twin-screw or centrifugal suit performance better, and an off-the-shelf twin-screw kit is often the pragmatic choice for mild to moderate gains despite higher charge temperature.

## Worked example
A Roots-type unit reaches near its full boost well below peak rpm, so load cells are reached early in a pull. Take a unit delivering pressure ratio 1.8 from 300 K inlet air: at 85 % efficiency the outlet is about 300 + 300 x (1.8^0.2857 - 1) / 0.85 = 365 K; at the 55 % efficiency typical of a Roots at high ratio it is about 400 K. At the same boost, the hotter charge is about 9 % less dense, before intercooling.

## Disputed / conflicts
- Intercooler plumbing volume and response: one practitioner moved a supercharged engine from a short top-mount layout to a much longer front-mount and noticed no change in throttle response from the driver's seat (anecdote).
- Shape of the centrifugal curve: the source describes boost rising roughly linearly with rpm; compressor theory puts pressure rise nearer the square of wheel speed at low ratios. Logged boost against rpm on the actual unit settles it.
- Efficiency figures for the types come from one presentation and vary with the specific unit and operating point.

## Citations
- engineering-texts: Engine, combustion, charging and control engineering texts.
- practice: Practitioner training and tuning practice, distilled and cross-checked.
