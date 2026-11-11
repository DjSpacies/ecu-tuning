---
id: principles/thermo/air-density
title: Air density from pressure, temperature and humidity
layer: L0
status: draft
confidence: high
sources: [engineering-texts, sae-j1349]
verified: 2026-11-10
applies_to: {fuels: [gasoline, ethanol, methanol], engines: [all]}
depends_on: []
supersedes: []
---

# Air density from pressure, temperature and humidity

## Claim
The mass of air an engine can trap is proportional to air density, and density is set by absolute pressure, absolute temperature and, slightly, humidity.

## Why (derivation)
Treat air as an ideal gas: density rho = p / (R T), with R = 287.05 J/(kg K) for dry air.
Water vapour is lighter than air (R_v = 461.5 J/(kg K)) and displaces dry air at the same total pressure, so humid air is less dense:
rho = (p - p_v)/(R T) + p_v/(R_v T), where p_v is the partial pressure of water.
Oxygen available for combustion scales with the dry-air term only.

## Assumptions
Ideal-gas behaviour, which holds well at intake conditions. Pressure and temperature are absolute (kPa, K).

## Breaks when
A gauge pressure used in place of absolute. A manifold or inlet sensor reading that does not represent the charge actually trapped (heat pick-up in the port, pressure waves at high rpm).

## Practical use
Use `principles/calculators/air.py` (`air_density`). Always convert boost to absolute first. Compare densities, not boost figures, when judging what a change will do to airflow.

## Worked example
At 101.325 kPa and 25 C, dry air: 101325 / (287.05 x 298.15) = 1.184 kg/m3. At 200 kPa absolute and 40 C: 200000 / (287.05 x 313.15) = 2.225 kg/m3, 1.88 times denser despite double the pressure, because the charge is hotter.

## Disputed / conflicts
None recorded.

## Citations
- sae-j1349: p.8 (reference dry-air pressure and inlet temperature). Page numbers are those of our converted copy.
- engineering-texts: Engine, combustion, charging and control engineering texts.
