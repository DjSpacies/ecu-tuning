---
id: principles/combustion/mixture-and-power
title: Mixture, power and combustion temperature
layer: L1
status: draft
confidence: high
sources: [engineering-texts, practice]
verified: 2026-11-11
applies_to: {fuels: [gasoline, ethanol, methanol], engines: [all]}
depends_on: [principles/fuels/stoichiometry-and-lambda, principles/fuels/energy-and-charge-cooling]
supersedes: []
---

# Mixture, power and combustion temperature

## Claim
Best torque comes a little rich of stoichiometric, across a broad band, because all the air gets burned. Lean of that band, torque falls quickly. Rich of it, torque falls slowly. The richer side can be used deliberately to manage combustion heat and knock, so the target within the band is chosen for safety and economy, not power. Unlike spark timing, mixture has no single optimum.

## Why (derivation)
### Air sets the power
Air mass sets the energy that can be released. Fuel only has to be matched to it, so adding fuel does not add power. A slight fuel excess makes sure the oxygen is consumed despite imperfect mixing in a turbulent full-load charge. The combustion textbook puts maximum power near an equivalence ratio of 1.1 (about lambda 0.91), and combustion is fastest slightly rich of stoichiometric.

### Why torque falls on each side
- **Lean:** the mixture is no longer rich enough everywhere to use all the oxygen. Then the gas near the plug becomes too lean to light reliably, and lean misfire follows.
- **Rich:** extra fuel absorbs heat by evaporation and dissociation but does not burn completely, so torque falls slowly. At extreme richness the charge becomes hard to ignite, and rich misfire appears. Where that happens depends on the ignition system.

### Measured shape in the sources
Sources sweep lambda at fixed rpm on a dyno:
- NA engines at full load: torque within about 1 % from roughly lambda 0.85 to 0.95, a peak near 0.89 to 0.93, a sharp fall lean of about 0.95 to 0.98, and a gradual fall rich of about 0.80 to 0.83.
- Part-throttle cruise: torque still peaks near lambda 0.91 (about 9 % rich). It falls steeply lean, losing roughly 40 % by lambda 1.1 in one cell.

### Temperature and the rich margin
Leaning from very rich first raises combustion and exhaust temperature as the cooling excess disappears. EGT peaks near the best-power mixture. Leaner still, EGT falls because less energy is released, and then lean misfire arrives. A falling EGT when very lean is therefore not a sign of safety. Extra fuel lowers combustion temperature and knock tendency. This is why targets richen with heat load: more boost, more sustained full load, a knock prone design.

## Assumptions
Homogeneous charge, port or homogeneous direct injection. Torque measured at fixed rpm, spark and load. Wideband lambda never reads perfectly steady, so the plateau is read by averaging, not from one point.

## Breaks when
- **Knock-limited engines** may run richer than best power for protection. The extra fuel cooling can let the engine accept more timing, for a net torque gain. Practitioners report this on older, less efficient chambers, which needed about lambda 0.86 to 0.87 where a modern four-valve NA engine was happy at 0.88 to 0.90.
- **Very lean operation** needs an engine built for it: thermal clearances, coated crowns, heat-tolerant valves and seats, and adjusted timing. One practitioner's example is a purpose-built endurance engine running lambda 0.95 to 0.98 at full load.
- **Rotary engines:** one demonstration showed a turbo rotary gaining power when leaned from about 0.76 toward 0.78. Richer than about 0.74, power fell sharply. The practitioner still ran slightly richer than peak power for reliability.
- **Ethanol and methanol:** charge cooling from the fuel itself reduces the need for progressive enrichment with boost. On methanol, leaning gains almost nothing, and past a point there is a sharp cliff to engine damage. Rich is the safe direction, limited only by what the ignition can reliably light, and power falls only at extreme richness.
- **Excess rich over long periods:** on an NA engine, a mixture far richer than needed washes oil from the bores and dilutes the sump. Bore and ring wear rise, and economy suffers. On very rich methanol the same dilution can lower the autoignition point, which can lead to pre-ignition.
- **Catalyst:** a car keeping its converter and used on track gets more exhaust heat from leaner full-load mixtures, so sources keep it richer at the top end.

## Practical use
- Treat lambda, not AFR, as the working unit. A wideband measures lambda and shows AFR only by multiplying by its stoichiometric setting. AFR numbers on ethanol shown on a gasoline scale are really lambda in disguise. Correction factor = measured lambda / target lambda.
- Find the band on a dyno where torque is measured. Before any lean excursion at load, retard timing first to widen the knock margin. Do not do lean full-load sweeps on high-output engines.
- Choose where to sit by heat load and knock margin: richer for boost, sustained load, high compression, knock prone chambers, or a retained catalyst. Methodology/combustion-afr-targets holds the target-planning practice.
- **Diagnostic:** if a timing change seems to change measured lambda, look elsewhere. Overlaid lambda traces across timing sweeps show no shift, and closed-loop trims stay within about 1 %.
- **Diagnostic:** reports that a lean mixture "melted" the engine usually mean lean raised knock tendency and knock did the damage. Look at timing, boost and knock evidence together.

## Worked example
At 2500 rpm and full load on an NA V6, with a little timing pulled first, a sweep from lambda 0.80 to 1.00 showed torque climbing to a flat top from about 0.88 to 0.94, then falling past about 0.95. A target of 0.90 gives up nothing measurable and sits on the cooler side. In a cruise cell at the same rpm, lambda 1.0 gave a little less torque than the 0.91 peak. That is a deliberate trade for economy, and the driver opens the throttle very slightly to compensate.

## Disputed / conflicts
- **NA best-power bands agree:** instruction gives lambda 0.85 to 0.92 for best NA power and the combustion textbook about 0.91.
- **Boosted bands:** practitioners give 0.82 to 0.85 as boosted best power, and about 0.78 to 0.82 near 1 bar of boost on pump fuel. Those figures include a safety margin. The combustion textbook gives no boosted figure, so they have tier B support only. Enriching well past best power does lower knock tendency and exhaust temperature (engine textbooks), which agrees with practice.
- **Rich limit on gasoline:** one practitioner finds little gain once the target passes roughly 0.75 to 0.76, with rich misfire and lost power beyond. Another sets 0.78 as the richest he uses outside sustained-load events. These are close, and both depend on ignition energy.
- **Ethanol lambda:** one practitioner runs the same lambda targets on E85 as on gasoline, or slightly leaner at high boost. He criticises very rich ethanol targets (0.70 to 0.72) as costing power and causing misfire. A methanol practitioner gives E85 figures around 0.76 to 0.78 and methanol 0.65 to 0.70, with large-displacement methanol drag engines far richer. The sources agree the choice depends on fuel cooling and duty, and differ on how much margin to carry.
- **Lean and burn speed:** see the Disputed section of principles/combustion/mbt-timing.

## Citations
- engineering-texts: Engine, combustion, charging and control engineering texts.
- practice: Practitioner training and tuning practice, distilled and cross-checked.
