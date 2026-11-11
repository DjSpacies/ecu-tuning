---
id: principles/thermo/air-density
title: Air density from pressure, temperature and humidity
layer: L0
status: draft
confidence: high
sources: [engineering-texts, sae-j1349, practice]
verified: 2026-11-11
applies_to: {fuels: [gasoline, ethanol, methanol], engines: [all]}
depends_on: []
supersedes: []
---

# Air density from pressure, temperature and humidity

## Claim
The mass of air an engine can trap is proportional to air density, and density is set by absolute pressure, absolute temperature and, slightly, humidity. The temperature that matters is that of the charge entering the cylinder, which is often not what the air temperature sensor reads.

## Why (derivation)
Treat air as an ideal gas: density rho = p / (R T), with R = 287.05 J/(kg K) for dry air.
Water vapour is lighter than air (R_v = 461.5 J/(kg K)) and displaces dry air at the same total pressure, so humid air is less dense:
rho = (p - p_v)/(R T) + p_v/(R_v T), where p_v is the partial pressure of water.
Oxygen available for combustion scales with the dry-air term only.
Because density goes as 1/T, a 10 C rise near 300 K cuts density by about 10/300, roughly 3 %. The curve is gently non-linear overall but close to linear over the automotive intake range (about -20 to 70 C), which is why the sources quote a manual intake-temperature fuel correction of about 2 to 3 % per 10 C, removing fuel as air gets hotter and adding it as air gets colder.

## Assumptions
Ideal-gas behaviour, which holds well at intake conditions. Pressure and temperature are absolute (kPa, K).

## Breaks when
- A gauge pressure is used in place of absolute. Some ECUs and many gauges work in gauge pressure; real baro is about 101.3 kPa at sea level and varies with altitude and weather, not a fixed 100.
- The sensor reading does not represent the charge actually trapped. At low air speed the charge picks up heat from manifold, ports and valves after the sensor; a sensor in a cast manifold can heat-soak and read high; a sensor in a MAF housing on a boosted engine sits ahead of the compressor and intercooler. Fuel evaporation then cools the charge where nothing measures it. See `methodology/thermo-charge-temp-estimation`.
- Pressure waves at high rpm make manifold pressure an imperfect measure of trapped charge.
- Fuel temperature, which changes fuel density, is not captured by an air-temperature correction.

## Practical use
Use `principles/calculators/air.py` (`air_density`). Always convert boost to absolute first. Compare densities, not boost figures, when judging what a change will do to airflow. A colder charge carries more oxygen and has more knock margin per unit of mass, but the denser charge can itself want slightly less timing, so a cold-day check is still worth doing on a knock-limited engine. Hotter coolant raises charge temperature and knock tendency, which matters more on a boosted performance engine than the small efficiency gain that leads factory systems to run hot.
When a physics-based compensation in the ECU's fuel model already handles density, a separate manual intake-temperature fuel table should stay at zero to avoid correcting twice.

## Worked example
At 101.325 kPa and 25 C, dry air: 101325 / (287.05 x 298.15) = 1.184 kg/m3. At 200 kPa absolute and 40 C: 200000 / (287.05 x 313.15) = 2.225 kg/m3, 1.88 times denser despite double the pressure, because the charge is hotter. If the same 200 kPa charge reaches 50 C instead, density is 200000 / (287.05 x 323.15) = 2.156 kg/m3, 3.1 % less, close to the 3 % per 10 C rule.

## Disputed / conflicts
- Manual correction slope: sources quote about 2 to 2.5, 2.5 to 3, and about 3 % per 10 C. The ideal-gas value near 300 K is about 3.2 to 3.4 % per 10 C at the sensor; smaller practical slopes are consistent with the charge not following the sensor fully (see Breaks when). Discriminating test: lambda drift during a controlled heat-soak sweep.

## Citations
- sae-j1349: p.8 (reference dry-air pressure and inlet temperature). Page numbers are those of our converted copy.
- engineering-texts: Engine, combustion, charging and control engineering texts.
- practice: Practitioner training and tuning practice, distilled and cross-checked.
