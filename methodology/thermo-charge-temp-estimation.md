---
id: methodology/thermo-charge-temp-estimation
title: Charge temperature estimation and heat-soak testing
layer: L2
status: draft
confidence: medium
sources: [practice]
verified: 2026-11-11
applies_to: {fuels: [gasoline, ethanol, methanol], engines: [all]}
depends_on: [principles/thermo/air-density, methodology/compensations, methodology/fuel-model-load]
supersedes: []
---

# Charge temperature estimation and heat-soak testing

## Claim
The fuel calculation needs the temperature of the charge at the intake valve, which no sensor measures. A blend of air temperature and coolant temperature, weighted by air speed, estimates it well enough to hold lambda within a percent or two across heat soak. The blend is calibrated by deliberately sweeping intake temperature at a few fixed operating points and reading which way lambda drifts, and the fuel charge-cooling term is calibrated separately by checking that lambda follows a change of target.

## Why (derivation)
### Heat picked up after the sensor
Between the air temperature sensor and the valve, the air passes pipes, throttle body, manifold, runners, ports and the valve itself, all heated by the engine and roughly at coolant temperature. Heat transferred to the charge grows with the time it spends in contact with those walls. At idle, light cruise and high vacuum the air moves slowly and approaches coolant temperature; at high rpm and load it moves fast and stays close to the sensor reading. So
T_charge = T_IAT + b (T_ECT - T_IAT),
where the coolant bias b is large at low air speed and small at high air speed. Many ECUs expose b as a table against rpm and load, where 100 % means use coolant temperature and 0 % means use air temperature; setting the whole table to zero reproduces air-temperature-only behaviour.

### Fuel evaporation
Injected fuel then evaporates and absorbs its latent heat just before the valve, cooling and densifying the charge. Some VE-based models carry a charge-cooling coefficient for this. If it is wrong, the model cannot follow a change in lambda target accurately, and because it scales fuelling everywhere, changing it after the VE table is tuned shifts the whole table.

### Why one table does not fit all
The right bias depends on where the air sensor sits (in a MAF body far upstream, in the pre-throttle pipe, or in a manifold that heat-soaks), on manifold material (aluminium versus plastic) and even on the manifold gasket. A sensor in a cast manifold conducts heat from the casting and reads high at low airflow and after a hot stop.

## Assumptions
- VE table and injector data are already close, so a lambda drift during a temperature sweep reflects the temperature model rather than base fuelling.
- Closed-loop lambda correction is off during the tests so it does not mask the effect.
- Injectors are out of their short-pulse region at the test points.

## Breaks when
- The air sensor is badly placed: heat soak in a manifold-mounted sensor, or engine-bay heat at a sensor above the exhaust; no blend fully corrects a sensor that does not see the charge path.
- Fuel temperature rises during heat soak and changes fuel density, which an air-and-coolant model cannot capture unless fuel temperature is measured. One logged example stayed within about 25 to 40 C in normal use, so most makers judge it not worth modelling.
- Hot restarts: fuel-rail heat soak makes the engine run lean for some 20 to 30 s, and readings in that window are not representative. Even factory systems show double-digit positive trims after hot restarts.
- A coolant sensor that reads wrong shifts the estimate at low airflow; in one example an 11 C error mattered only a few percent because the engine was out of warm-up enrichment.
- On methanol, the fuel's large evaporative cooling is unmeasured; true charge temperature is lower than any sensor reports.

## Practical use
### Starting values
Start from the ECU maker's defaults or reference values: heavily coolant-biased at idle and low rpm (examples in the sources range from about 15 % to 90 %, with 60 to 75 % common in high vacuum) falling to near zero, or about 15 %, at high rpm and boost. Practitioners commonly leave a well-made default alone; tune VE first, then adjust the blend only where air-temperature changes are not being corrected.

### Heat-soak test for the blend (diagnostic)
1. Choose a few anchor sites, for example idle, the lowest steady full-throttle rpm, light load at mid-high rpm, and full load at mid-high rpm.
2. At each, hold steady and log target lambda, measured lambda, air temperature and coolant temperature while deliberately raising intake temperature: close the bonnet, partly block the intercooler, move the filter to hot air, or switch off a water-to-air pump. Watch coolant closely when blocking airflow.
3. Run the test once with the cell at 100 % (coolant) and once at 0 % (air temperature). Note the lambda drift at each extreme. If coolant-only drifts rich by 4 % and air-only drifts lean by 6 % over the same rise, the zero-drift setting lies 4/10 of the way from the coolant end, about 60 %.
4. Refine: lean drift as air temperature climbs means the model reacts too strongly to air temperature, so increase coolant bias; rich drift means decrease it. Near the answer, steps of 2 to 4 % per test are typical.
5. Fill the rest of the table by interpolating and extrapolating a smooth shape from the anchors.
Ignore the momentary lambda dip at the instant the bonnet closes; judge the trend over the whole test. Lambda holding within about 1 to 2 % across a heat-soak test is an excellent result.

### Charge-cooling coefficient (diagnostic)
Before tuning the full VE table, hold a light-load steady point outside the short-pulse region (one demonstration: about 2500 to 3000 rpm, about 60 kPa), tune to lambda 1.0, then step the target richer (to 0.90, including surrounding cells). Overshooting rich means reduce the coefficient; landing lean of target means increase it. Use large steps first (halving or doubling), retune lambda 1.0 and repeat. In one demonstration a request for 0.90 gave 0.88 until the coefficient was halved. The calibration is only meaningful with accurate injector data.

### Residual trims
Leave any charge-temperature fuel trim table at zero and add values only where the model is seen to over- or under-compensate at particular temperatures and loads. A common residual is a few percent of fuel added back at hot, heat-soaked idle, where automatic density correction tends to over-reduce fuel.

### Ignition and dyno conditions
Charge-temperature ignition retard is useful protection, but if charge temperature creeps up during dyno work (one default table began pulling timing around 60 to 70 C at high load), it causes needless retard and run-to-run power variation. Know where you operate in it. Dyno air temperatures often exceed road values; tune timing with intake trims at zero at realistic temperatures, and add retard purely as margin above them. Between tests, return to idle or cruise to let temperatures recover, and do not judge the tune straight after a heat soak.

## Worked example
At 2000 rpm full throttle, intake temperature is swept from 30 to 60 C. With the bias cell at 100 % lambda drifts 4 % rich; at 0 % it drifts 6 % lean. The interpolated bias is 60 %; a confirming test shows a slight rich trend, and the cell settles at 55 %, after which lambda stays nearly flat through the sweep. At 5000 to 6000 rpm and high load the same procedure gives about 8 to 10 %, close to pure air temperature, as expected for fast-moving air.

## Disputed / conflicts
- Model or manual table: several practitioners use the blended estimate and report accurate lambda control; one prefers a 3D air-temperature fuel trim against load and rpm and leaves the estimate off for simplicity; another finds automatic density correction too aggressive at hot idle and prefers a manual table. Whichever is used, the other must stay at zero to avoid a double correction.
- Calibrating the blend is described as effective but hard; several sources recommend leaving defaults unless lambda drift with temperature is observed. Discriminating test: the heat-soak sweep above at the operating points that matter for the car.

## Citations
- practice: Practitioner training and tuning practice, distilled and cross-checked.
