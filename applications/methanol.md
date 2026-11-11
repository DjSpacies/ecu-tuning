---
id: applications/methanol
title: Methanol profile
layer: L4
status: draft
confidence: medium
sources: [engineering-texts, reference-data, practice]
verified: 2026-11-11
applies_to: {fuels: [methanol], engines: [all]}
depends_on: [principles/fuels/energy-and-charge-cooling, principles/fuels/octane-rating]
supersedes: []
---

# Methanol profile

## Claim
Methanol needs about 2.3 times the fuel mass of gasoline at the same lambda (sources quote 2 to 2.5 times the volume for the same power), cools the charge strongly, resists knock enough to support very high compression and boost, and is hard to start cold. The fuel system is the limiting concern, along with corrosion, oil dilution and pre-ignition.

## Why (derivation)
Its low stoichiometric ratio and high latent heat follow from the composition. It attacks some materials and is toxic. Its octane rating (about 107 to 108 in one source) plus latent heat several times that of gasoline keep the end gas cool, which is why methanol engines run high compression and boost above 100 psi with little knock concern. Like ethanol it is more prone to pre-ignition than to knock at those outputs, and the very rich mixtures wash fuel past the rings into the oil.

## Assumptions
The fuel system is rated for methanol.

## Breaks when
- Cold starting and oil dilution are serious problems, and water absorption changes properties.
- Methanol corrodes aluminium and some injector designs and has no lubricity.
- It burns with an almost invisible flame, so a fire may not be seen by driver or marshals.

## Practical use
- Size injectors and pump first. Handle with care, and check every wetted material.
- Lambda: drag engines at high boost run very rich, strongly dependent on engine and boost; practitioners' examples sit around 0.55 to 0.65. Never carry gasoline lambda or exhaust temperature targets across: methanol engines run far cooler (examples in the sources settle near 720 to 770 C), and chasing gasoline-like exhaust temperatures would mean dangerously lean mixtures.
- Monitor each cylinder's exhaust temperature where possible: one cylinder's EGT running away from the others is a sign of a fuel fault (a failed injector in one example) and a reason to abort.
- Rotaries: one practitioner finds little extra timing worth adding even on methanol; its value is supporting much more boost.
- Living with it: after an event, drain, refill with gasoline and run the engine on it before storage (pickling); add a methanol-compatible lubricity additive; change oil very frequently (drag racers often after every meeting). Mark the car so marshals know the fuel.
- Intercooling: short-duration drag engines on methanol often run without an intercooler at very high boost because evaporating fuel cools the charge; one practitioner still prefers an ice-slurry intercooler for consistent intake temperature through the run. Some very short-duration engines run without a radiator or water jackets, which only suits brief running.
- One practitioner never blends methanol with E85 or gasoline: E85 alone supports well beyond 40 psi in his experience, and a full switch to methanol avoids unknowns.

## Worked example
An engine using 400 cc/min of gasoline at a point needs roughly 400 x 2.27 x 745/792 = 855 cc/min of methanol.
A methanol turbo rotary drag engine at about 3.2 bar boost read about 0.62 lambda at full throttle (the sensor's rich limit, so at times richer still) with 750 to 770 C before the turbine.

## Disputed / conflicts
- **Why it makes power.** One practitioner attributes the gain to burning 2.5 to 3 times the fuel mass per cycle despite half the heating value; per kilogram of air the stoichiometric energy is only about 5 to 6 % above gasoline, so charge cooling and knock margin are the stronger explanations (see `principles/fuels/energy-and-charge-cooling`).
- **Fuel volume multiple.** Sources give 2.25 times and 2 to 2.5 times gasoline; the stoichiometric calculation gives about 2.3 times by mass at equal lambda, more by volume at the richer lambdas methanol is run at.

## Citations
- engineering-texts: Engine, combustion, charging and control engineering texts.
- reference-data: Published reference data: thermophysical properties, fuel data, sensor and injector data sheets, statistics.
- practice: Practitioner training and tuning practice, distilled and cross-checked.
