---
id: methodology/altitude-and-baro
title: Altitude and barometric pressure
layer: L2
status: draft
confidence: medium
sources: [practice, engineering-texts]
verified: 2026-11-11
applies_to: {fuels: [gasoline, ethanol, methanol], engines: [turbo, supercharged, na]}
depends_on: [principles/thermo/air-density, principles/boost/compressor-and-surge, principles/airflow/volumetric-efficiency, methodology/fuel-model-load]
supersedes: []
---

# Altitude and barometric pressure

## Claim
Falling barometric pressure reduces air density and, in a boosted engine, raises the compressor pressure ratio for the same manifold pressure, so a turbo can be pushed beyond its limits at altitude. How much the fuel and ignition tune moves with altitude depends on the fuel model and load axis: a mass airflow meter follows air mass directly, absolute manifold pressure follows intake density but not the exhaust side, gauge pressure and throttle-based loads need baro in the calculation, and a pressure ratio across the engine is the most complete basis. Weather alone moves baro a little; large altitude changes are what matter.

## Why (derivation)
### Air mass and mixture
Air-fuel ratio is a mass ratio. At lower baro the same volume of air holds less mass and less oxygen, so a system that meters fuel by volume or by throttle position without a pressure term delivers the same fuel to less air and goes progressively rich as altitude rises. Standard sea-level baro is 101.3 kPa; one event example starts at roughly 80-85 kPa and finishes near 63-65 kPa (about 4300 m).

### Compressor pressure ratio
For the same absolute manifold pressure, compressor work scales with the ratio to ambient pressure, so the turbo spins faster. At 80 kPa ambient, 200 kPa absolute is a pressure ratio of 2.5 instead of 2.0: the same as raising boost from 200 to 250 kPa at sea level.

### Why manifold pressure alone is incomplete
VE depends on the pressure ratio across the engine, intake to exhaust, because exhaust pressure sets residual gas and pumping. On an NA engine exhaust pressure is roughly baro, so at altitude the same manifold pressure meets a lower exhaust pressure and fills differently. A speed-density model that uses absolute MAP corrects intake density but not this exhaust-side effect. A load of manifold pressure over baro (NA) or manifold over exhaust manifold pressure (turbo) folds it in.

### How each load basis moves with altitude
- Absolute MAP axis: at full throttle an NA engine reaches only local baro minus intake restriction, so it runs further down the load axis (left or lower rows) of both fuel and ignition tables. Whether those cells are right depends on how large the baro change is.
- Gauge pressure axis (MAP minus baro): an NA engine at full throttle stays in the 0 kPa row whatever the baro, and the real MAP still enters the fuel equation, so the operating cell already represents the changed density; one source argues this removes the need for a separate baro fuel multiplier.
- Throttle-based load (alpha-N): without baro in the equation a sea-level map runs badly rich at high altitude; using baro as the pressure term keeps the airflow estimate steady and still follows altitude.
- MAF: measures air mass directly, so fuelling self-corrects; if ignition load is air per cylinder, the engine moves to lower-load cells at altitude and gets more advance automatically (one example: 18 degrees at sea level becoming about 21-24).

## Assumptions
The baro sensor is real and live, not latched at key-on, and is mounted away from any ram-air effect (engine bay or cabin). The fuel model's handling of baro is known.

## Breaks when
- An ECU that reads baro from the MAP sensor at key-on cannot follow a large climb during one drive; it is fine only when baro will not change much while running.
- A gauge-pressure axis models poorly in deep vacuum and on turbo engines, where exhaust pressure is not baro (see Disputed).
- Pressure-ratio loads need an exhaust pressure sensor. One practitioner found the raw turbine-inlet signal so noisy that filtering it enough added too much lag for fuelling; a mechanical damper on the line may be needed. On ITBs, manifold over baro has the same lack of resolution as MAP once the manifold reaches atmosphere (about 30-35 % throttle), so alpha-N is still needed.
- On some ECUs full baro correction is not automatic even when air temperature correction is; the baro table must be enabled and tuned whether load is throttle or MAP.

## Practical use
- Check how the ECU gets baro (separate live sensor, MAP sampled at key-on, none), whether the load axis is absolute or gauge, and whether baro enters the fuel equation.
- Compare pressure ratio, not boost. Decide on a boost target that reduces with altitude if needed, and limit boost by pressure ratio or turbo speed where available. Expect a naturally aspirated engine simply to lose power.
- A car that lives at one altitude needs no special treatment; ordinary weather swings are one small error among others (temperature compensation errors are often larger), and most tuners run plain MAP load for road cars. Treat baro work as necessary for mountain events, large regular altitude changes, or a tune built at one altitude and used at another.
- For large altitude ranges, either add ambient pressure as an extra axis of the VE table (one event car used breakpoints at about 110, 90 and 60 kPa, copied the base table to each, then filled each from closed-loop trim logs gathered at the bottom, middle and top of the course), or build baro compensation tables for fuel, ignition and boost target. Fill them from logged data at different baro rather than theory; the logged correction carries the exhaust back-pressure effect a pure density correction misses.
- Tuning at an elevated dyno site: full throttle on an NA engine may sit between rows (one example: about 94 kPa between the 80 and 100 kPa rows, another site about 97 kPa). Edit the rows actually being accessed, move the neighbouring row in proportion so interpolation lands correctly, and keep a breakpoint just below 100 kPa so full-load fuel can be refined without disturbing part throttle.
- Nothing about altitude is fuel-specific: if the model handles baro correctly, ethanol blends and gasoline are affected alike. Both mixture and the timing for best torque change with density.

## Decision rules
Check how the ECU gets baro, and whether its load axis is absolute or gauge. Limit boost by pressure ratio or turbo speed where available. Expect a naturally aspirated engine to simply lose power. Do not add a manual baro fuel correction where the model or load axis already accounts for baro, or the correction is doubled.

## Data gates
Baro channel logged; turbo speed if available. For baro compensation, data at several clearly different baro values with closed loop active or measured lambda logged, and the same load and rpm cells compared.

## Worked example
From sea level to 61.9 kPa ambient, holding 200 kPa absolute means a pressure ratio of 3.2 against 2.0.
Gauge axis: at 97 kPa baro a manifold pressure of 65 kPa reads -32 kPa gauge; at sea level 0 kPa gauge is about 100 kPa absolute, +100 about 200 kPa (about 15 psi boost) and +200 about 300 kPa. A fuel axis that stops at +120 kPa saturates at about 17-18 psi; if 20 psi is planned, extend it.
Pressure-ratio axis (one turbo demonstration at fixed boost about 165 kPa absolute): intake over exhaust pressure was about 1.15 at 2000 rpm, peaked near 1.32 at 3000 rpm, then fell to about 0.91 at 7500 rpm as exhaust pressure reached about 180 kPa. A full-load run therefore crosses the table diagonally rather than along one row.

## Disputed / conflicts
- Cross-check: the pressure ratio argument follows directly from the definition. A charging textbook notes high compression and expansion ratios in chargers at low ambient pressure.
- Gauge-pressure axis: one source (an practitioner teaching on a gauge-axis ECU) presents it as altitude compensation without a separate table. A training analysis says it holds an NA engine at full throttle and works in boost, but creates more error than absolute MAP in vacuum, and that the correct basis is pressure ratio across the engine. Discriminating test: log lambda error in vacuum cells at two clearly different baro values on each axis.
- "MAP is MAP regardless of altitude": stated as common belief; contradicted by the pressure-ratio argument above (training sources). The size of the error at moderate altitude changes is unmeasured in the sources.
- Pressure-ratio load: presented as self-compensating for altitude and back pressure, but the demonstrating practitioner had not yet proven it over a large baro change, and another found local altitude ranges (about 300-1500 m) too small to show a benefit.
- Need for baro compensation at all: one practitioner says a car at constant altitude does not need it and many tunes omit it; event tuners treat it as essential. Both are right in their context.

## Citations
- practice: Practitioner training and tuning practice, distilled and cross-checked.
- engineering-texts: Engine, combustion, charging and control engineering texts.
