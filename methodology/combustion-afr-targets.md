---
id: methodology/combustion-afr-targets
title: Planning lambda targets
layer: L2
status: draft
confidence: medium
sources: [practice, engineering-texts]
verified: 2026-11-11
applies_to: {fuels: [gasoline, ethanol, methanol], engines: [all]}
depends_on: [principles/combustion/mixture-and-power, principles/fuels/stoichiometry-and-lambda, methodology/steady-state-fuel]
supersedes: []
---

# Planning lambda targets

## Claim
A lambda target table is set by heat load and usage, not by a universal number. Light-load areas aim for economy and emissions near lambda 1. Full-load areas run rich of best power by a margin that grows with cylinder heat: boost, sustained duty, compression, chamber design, fuel. Where the table blends from one to the other should follow real engine load (torque produced), not manifold pressure alone.

## Why (derivation)
- Combustion heat follows the mass of charge burned per cycle. At light throttle little is burned, so stoichiometric or slightly lean is thermally safe. At full load much more is burned, and the extra fuel serves as a coolant as well as making sure all oxygen is used (principles/combustion/mixture-and-power).
- Torque is flat across a broad rich band, so choosing a richer point inside it costs almost nothing. Choosing a point lean of the band costs torque and margin.
- Manifold pressure is not load. On an NA engine, near-atmospheric pressure is full throttle. A small turbo can reach about 100 kPa absolute at cruise with a quarter to a third of throttle. Some engines with individual throttles cruise near 90 to 95 kPa. At higher rpm a given pressure also represents a larger share of maximum torque.
- In a VE-based fuel model the target table is what the fuel equation delivers. Measured lambda is tuned to meet it, so targets must be realistic and set before VE tuning. Unrealistic targets corrupt the whole calibration. Once VE is right, mixture experiments are made by editing targets alone.

## Assumptions
Gasoline numbers unless stated, in lambda. Targets are starting points that the dyno then confirms; every source says the particular engine decides.

## Breaks when
- **Ethanol and methanol:** charge cooling from the fuel changes how much enrichment is needed with boost (see Practical use).
- **Unusual designs:** high-compression NA designs converted to boost need targets a purpose-built turbo engine would only use at much higher boost. Rotaries respond differently to lean.
- **No target table:** where the ECU has no target table in the fuel calculation, targets live in the tuner's head and are applied cell by cell.

## Practical use
### Light load
- Idle and cruise: lambda 1.0 for economy and emissions.
- Idle: some engines, particularly with long-duration cams, idle more smoothly slightly rich (about 0.95 to 0.98 in the sources). Modern engines are usually happy at 1.0.
- Lean cruise: best economy is near lambda 1.05. One practitioner finds about 1.03 to 1.05 works best on large-capacity, mild multi-cylinder engines. Cammy four-cylinders often hesitate when leaner than stoichiometric. Around 1.1 is generally too lean: torque falls, the driver opens the throttle, and the saving disappears.

### High rpm and overrun
High-rpm, light-load cells are passed through on lifts, gear changes and overrun. They are not steady cruise, so a slightly rich value (about 0.95 to 0.97) adds cooling at no economy cost. It also helps anti-lag reliability on competition cars.

### The blend from cruise to full load
- NA: blend from lambda 1 to the full-load target as load approaches full throttle. One practitioner's rule of thumb is to begin the move at about 90 to 95 % of that rpm's maximum torque near 2000 rpm, falling to about half of maximum torque by two-thirds of the rev limit. That moves the boundary to lower manifold pressure as rpm rises. A part-throttle cell used in daily driving gained only about 4 N·m going from 1.0 to 0.90 in one demonstration, which is not worth the fuel.
- Turbo: treat the 100 kPa row as a light-load transition zone, about 0.95 (slightly richer at high rpm). Do not use the NA full-throttle figure there. Add a breakpoint just below atmospheric (for example 95 kPa) so interpolation toward the boost targets does not richen the engine while it is still in vacuum. The transition is crossed briefly, so the accuracy of the full-boost targets matters more.

### Full load
- **NA gasoline:** about 0.88 to 0.92, often tapered richer toward redline (about 0.87). A commonly used safe first-run value is 0.90.
- **Boosted gasoline:** richer with rising boost but with a floor. Typical in the sources: about 0.85 at low boost, about 0.78 to 0.82 near 1 bar of boost, about 0.78 at 1.5 bar and above. Going past roughly 0.75 to 0.76 rarely helps.
- **Design factors:** a high-compression NA engine converted to boost needs richer targets than the boost alone suggests. An practitioner example: about 0.80 to 0.82 at 7 to 9 psi, where a factory turbo engine would use about 0.83 to 0.85. Compression, design origin and knock sensitivity matter as much as torque output: a low-output converted engine can want similar lambda to a much more powerful purpose-built one.
- **Duty:** street full-load bursts last seconds, so chamber temperature never peaks. Circuit sessions sustain load for 15 to 30 minutes, and practitioners run about 0.02 richer for similar power. Land-speed engines at full load for minutes run richer still, accepting a power cost. A drag engine's rising EGT over a few seconds is acceptable where it would not be for sustained use.
- **Boost-control fallback:** tune spring (minimum) boost first with safe targets, so the engine stays safe if boost control fails.
- **Injector-limited engines:** sources richen where cylinder pressure peaks (high boost at mid rpm) and taper leaner at high rpm where boost falls, keeping injector duty in range.

### Ethanol and methanol
- **E85 (one practitioner):** same lambda targets as gasoline, about 0.78 to 0.80 at full load. Progressive enrichment with boost is not needed, and very rich ethanol (0.70 to 0.72) loses power and can misfire. The exception: a knock-limited engine that ran rich on gasoline for cooling does not need that richness on ethanol.
- **Methanol:** rich is safe and lean gives almost nothing. Typical in the sources: about 0.70 at moderate boost, about 0.65 at higher boost, and much richer on very large-displacement engines. Treat 0.70 as where a tune tends to end, not where it starts. Log EGT: one practitioner richens when EGT reaches his chosen ceiling (about 750 C in one marine example). He expects no power loss from richening at that point.
- **Blends:** between the two fuels, biased toward the methanol targets.

### Acceptance
- At full load, being within about 1 % (±0.01) of target is accepted. Smooth small oscillations by eye, and do not chase them.
- On boost, the target should be the leanest mixture you are prepared to see. Confirm a lean spike repeats before correcting it.
- Rich within reason can be corrected later. A far-too-rich excursion into untuned cells (for example around 0.78 on an NA engine) is aborted and corrected, because it fouls plugs.

### Protective enrichment
When a protection overlay is active, the sources richen further. One practitioner example is turbo gasoline going to roughly lambda 0.74 to 0.77. Because it engages only when something is wrong, the power cost is accepted.

## Worked example
A turbo pump-fuel road car, from an practitioner's table:
| Region | Lambda |
|---|---|
| Vacuum / cruise from 1500 rpm | 1.0 |
| Idle | 0.95 |
| 100 kPa | 0.95 |
| 125 kPa | 0.90 |
| 150 kPa | 0.85 |
| 175 kPa | 0.82 |
| 200 kPa and above | 0.80 |

A 95 kPa breakpoint holds 1.0 until near atmospheric. High-rpm vacuum cells go to about 0.95. The values worked for that engine and are not universal.

## Disputed / conflicts
- **Where to start the boost enrichment:** one base map started enriching at 90 kPa, which an practitioner moved to near atmospheric. Another practitioner notes that a particular engine type that cruises near 100 kPa is run leaner there than typical turbo engines. Both follow the same rule: enrich by load, not by pressure.
- **Ethanol targets:** see principles/combustion/mixture-and-power. The sources differ by a few hundredths of lambda in how much margin they carry.
- **Rotary targets:** one practitioner runs rotaries a little richer than piston engines both at cruise and at full load on pump fuel. This is one practitioner's view.
- **Evidence strength:** the boosted gasoline and alcohol figures are tier B practice. The combustion textbook supports the NA best-power figure only.

## Citations
- practice: Practitioner training and tuning practice, distilled and cross-checked.
- engineering-texts: Engine, combustion, charging and control engineering texts.
