---
id: principles/boost/intercooling
title: Intercooling
layer: L1
status: draft
confidence: high
sources: [engineering-texts, practice]
verified: 2026-11-11
applies_to: {fuels: [gasoline, ethanol, methanol], engines: [turbo, supercharged]}
depends_on: [principles/boost/compressor-and-surge]
supersedes: []
---

# Intercooling

## Claim
Cooling the charge after compression raises density and knock margin. An intercooler's work is summarised by its effectiveness and its pressure drop: it can never bring the charge down to ambient, and every unit of pressure it loses must be made up by the compressor at a higher pressure ratio.

## Why (derivation)
Effectiveness is the fraction of the possible temperature drop achieved: (T_hot_in - T_hot_out) / (T_hot_in - T_coolant_in). Lower charge temperature means more mass per unit of boost (roughly 3 % density per 10 C over the usual intake range, see `principles/thermo/air-density`) and lower end-gas temperature for knock.
The engine sees only manifold pressure, but the compressor must make the pressure ahead of the cooler, so a cooler that drops 2 psi moves the compressor up its map by that much. Denser internal finning transfers more heat and costs more pressure; the design is a balance.
A water-to-air system adds a second transfer step: the water must sit above ambient to reject heat and the charge sits above the water, so, all else equal, a good air-to-air core gives a cooler charge on a road or circuit car. A core's metal mass also acts as a heat sink, absorbing a short burst of heat before shedding it.

## Assumptions
Coolant (air or water) temperature is known. Steady operation. Cooling air actually passes through the core rather than around it.

## Breaks when
- Heat soak in a stationary car or on a low-airflow dyno: effectiveness measured there does not hold on the road. Dyno air temperatures commonly exceed logged road values (one example: 45 to 50 C on the dyno against 30 to 35 C on road and track).
- Water-to-air systems saturate on long pulls; an iced reservoir works well only for runs of seconds.
- Gaps around a front or V-mount core let air bypass it; a V-mount without an exit path barely flows.
- A large front core restricts radiator airflow, so a marginal cooling system may overheat.
- Inlet and outlet in line at the bottom of the end tanks concentrate flow in the lower rows (one practitioner's view).
- A ducted factory airbox replaced by an engine-bay filter: on a turbo engine manifold temperature may barely change because the intercooler absorbs the extra load, hiding the loss.

## Practical use
### Logging and expectations
Log charge temperature during pulls. A temperature that climbs over a pull means knock margin is shrinking, so treat the end of a pull as the limiting case. Practitioner expectations for a good intercooled setup vary from about 10 to 20 C above ambient; one aims for about 30 to 35 C absolute, notes top-mount layouts commonly sitting in the mid-40s to 50 C, and treats consistently higher values as a reason to revisit the turbo or cooler. Above about 40 to 50 C on low-octane pump fuel, one practitioner expects knock trouble. Make sure the air-temperature ignition compensation is set so very hot charge cannot lead to detonation.

### Diagnostic test: core or conditions?
Intake temperature climbing run after run while power falls points at the core. In one case a supplier had quietly changed to cores with about half the internal fins: about 75 C after one pull; an older, well-finned core of the same size brought end-of-pull temperature down to roughly 35 C and added more than 10 % power. Inspect internals through the end tanks. Check for pressure drop by measuring before and after the core: an practitioner treats under about 1 psi as negligible and more than 2 to 3 psi as lost performance.
To judge an intake change on a turbo engine, log air temperature ahead of the compressor before and after the change, not only manifold temperature.

### Keeping dyno work representative
Use extra fans, open the bonnet, wet the core between runs or columns, return to light load to recover, and set alarms on coolant and air temperature. Tune at the temperatures the car will really see, and where seasons swing widely, check at both extremes.

### Choosing and fitting
- Frontal area within the bumper opening matters most; at higher power more area helps more than more thickness.
- Pipe size is set in practice by compressor outlet and throttle sizes; avoid needlessly large or long pipes, though charge-pipe volume affected response less than commonly claimed in one practitioner's experience.
- Plenum volume does not cool the charge; heat must be removed upstream.
- Seal ducting so all incoming air passes through the core, and size the whole cooling package together.
- Water-to-air makes sense where ducting air is hard (mid- or rear-engine cars, valley-mounted superchargers). Pump flow has an optimum: too fast leaves less time for heat exchange, so log charge temperature at several pump speeds.
- Water spray on the core helps mainly at high boost or with an undersized core. Refrigerant chilling costs engine power, and gas sprays are effective but short-lived.
- Methanol's large charge cooling lets some drag engines omit the intercooler, sometimes adding fuel sprayed into the charge pipe instead; one practitioner still ran an iced water-to-air core on a methanol car for consistent intake temperature within and between runs.

## Worked example
Charge enters at 400 K, cooling air 300 K, and leaves at 330 K. Effectiveness is 0.7. If the core drops 15 kPa, a 200 kPa manifold target needs about 215 kPa at the compressor outlet; at 100 kPa inlet the compressor runs PR 2.15 rather than 2.0.

## Disputed / conflicts
- Bar-and-plate versus tube-and-fin: more heat-sink mass and toughness against more heat-soak capacity per weight; one practitioner has had good results with both and will not pick a winner.
- Charge-pipe volume and lag: commonly blamed for slow response; one practitioner's experience across many cars (including a change from a short to a much longer front-mount layout) showed no perceptible change. Anecdote; a logged response test would settle it.
- Target intake temperature: figures differ between practitioners (10 to 15 C over ambient, about 20 C over, about 30 to 35 C absolute). All agree lower is better and the trend through a pull matters more than any single number.

## Citations
- engineering-texts: Engine, combustion, charging and control engineering texts.
- practice: Practitioner training and tuning practice, distilled and cross-checked.
