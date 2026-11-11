---
id: principles/boost/compressor-and-surge
title: Boost, pressure ratio and compressor limits
layer: L1
status: draft
confidence: high
sources: [engineering-texts, practice]
verified: 2026-11-11
applies_to: {fuels: [gasoline, ethanol, methanol], engines: [turbo, supercharged]}
depends_on: [principles/thermo/air-density]
supersedes: []
---

# Boost, pressure ratio and compressor limits

## Claim
A compressor's operating point is a pressure ratio and a corrected mass flow. It must stay between surge and choke, and compressing air heats it by an amount set by the ratio and the compressor's efficiency at that point. Boost pressure alone describes neither: it is largely a measure of how hard the engine resists the flow being pushed into it.

## Why (derivation)
### Pressure ratio
Pressure ratio is absolute compressor outlet pressure over absolute compressor inlet pressure. Inlet pressure is roughly baro, but filter, airbox and metering losses pull it lower at high flow, and a ram feed can raise it. Intercooler, pipework and throttle losses put the manifold below the compressor outlet. So manifold pressure divided by baro understates the true ratio, and the same manifold pressure is a higher ratio at altitude: 200 kPa manifold is a ratio of 2.0 at 100 kPa baro, 2.5 at 80 kPa and about 3.2 at 63 kPa.

### Temperature rise
Ideal compression raises temperature by T1 x (PR^((gamma-1)/gamma) - 1); a real compressor divides that rise by its isentropic efficiency. Lower efficiency islands mean a hotter, less dense charge, more turbine work for the same boost, and more load on the intercooler. Outlet temperatures of 150 to 200 C from a 25 C inlet are typical in the sources, depending on ratio and efficiency, which is why there is no fixed temperature rise per psi.

### Surge and choke
Surge is aerodynamic stall at low flow and high ratio: the engine cannot accept the flow, pressurised air escapes back through the wheel, pressure drops, the wheel recovers and the cycle repeats rapidly, producing the familiar flutter or chirp. The wheel does not stop or reverse; its inertia at tens of thousands of rpm makes that impossible, and logged shaft speed confirms it. Choke is the flow limit at the narrowest passage; past it efficiency collapses and the compressor mostly adds heat. Choke itself is not directly destructive, but it usually coincides with overspeed, which is.
Compressor maps use flows corrected to a reference inlet state so maps from different conditions agree.

### Two surge modes
- Throttle lift: pre-throttle pressure stays high while flow collapses, crossing the surge line for about a second. The reversed flow raises axial thrust, which wears plain thrust bearings quickly; ball-bearing cartridges carry thrust far better. This is the main reason for a blow-off or bypass valve.
- Under load at full throttle: a sizing or operating-point problem, damaging to the whole turbo and unsettling to the engine.

### Airflow and power
Power follows oxygen mass, so mass flow, not volume flow, is what matters. A rule of thumb used in the sources is roughly 9.5 to 10.5 lb/min of air (about 0.07 to 0.08 kg/s) per 100 flywheel hp. That is an upper bound: the flow must be available at a usable pressure ratio, and a knock-limited fuel or a restrictive engine caps power well below it. A large engine moves a given mass flow at a much lower ratio than a small one on the same compressor.

## Assumptions
Steady flow. Map accuracy, especially near surge, where the line is built from test data. Inlet and outlet pressures known or reasonably estimated.

## Breaks when
- Transient flow reversal when the throttle snaps shut.
- Maps are measured on a steady-flow test bench; real installations pulse.
- Efficiency calculated on the car from inlet and outlet temperatures is meaningless during a ramp run (one demonstration read 100 % and more) and only approaches a believable value after a long steady hold, once sensors and pipework reach thermal equilibrium.
- Airflow from a MAF calibration that is off after intake changes misplaces the point on the map.
- Twin-turbo or twin-scroll systems where one side works harder than the other.

## Practical use
### Placing the operating point
Use `principles/calculators/boost.py`. Log any two of pressure ratio, mass flow in map units and shaft speed, and the third confirms the point. Ideally measure pressure immediately before and after the compressor; at minimum use a pre-throttle charge-pipe sensor. Plot several rpm points through a ramp run against the surge line, efficiency islands and choke. A line sitting in mild islands with large headroom is fine if more boost is planned; as a final package a smaller turbo might respond better.

### Judging a boost target
Judge it on pressure ratio, flow and outlet temperature, not the boost number. Holding manifold pressure at altitude raises ratio, shaft speed and outlet temperature; a turbo comfortable at sea level can approach its speed limit high up, which is why purpose-built high-altitude cars fit shaft speed sensors and compressors that look oversized. Intake restrictions and intercooler pressure drop raise the ratio the compressor must make for the same manifold pressure. Tests that may surge or overspeed are stopped, not explored.

### Diagnosing surge
- Chirp or flutter on lift with a valve fitted: the valve is too small to vent the flow, or its spring too stiff for manifold vacuum to open it. A blow-off valve cannot really be too large, only mismatched.
- Flutter appearing around peak torque at full throttle as boost is raised, then disappearing as rpm rises: the point has just crossed the surge line where the engine's airflow demand is lowest for that ratio. A classic cause is a hybrid with a larger compressor on a small factory turbine that drives it hard at low rpm. Other causes in the sources: a big shot of nitrous on a large turbo, a twin-scroll arrangement feeding all flow to one scroll, and a small engine short-shifted into an rpm range that cannot swallow the flow at very high boost.
- Fixes, in order of preference: size the compressor correctly; as a band-aid lower the target around peak torque and ramp it up with rpm; opening the wastegate or vanes moves the point away from surge. Bleeding boost off through a valve wastes air and adds heat and belongs to extreme drag use.

### Blow-off valves
On plain-bearing turbos fit one. On ball-bearing turbos one practitioner treats it as largely optional for protection, and a back-to-back test at about 1 bar showed no measurable difference in boost recovery after a lift, with shaft speed dropping to about the same value with or without it. Mounting position (compressor cover or near the throttle) and angle appeared to make little difference. On engines metered by a MAF, an atmosphere-vented valve dumps air already metered (momentary rich), and an undersized or missing valve lets air reverse back through the meter (re-metered); a recirculating, adequately sized valve avoids both. Check factory valves for leakage after raising boost; worn piston-type valves can leak, and diaphragm types avoid that.

## Worked example
Target 200 kPa absolute, baro 100, inlet losses 5, charge-side losses 10: PR = 210 / 95 = 2.21. With 300 K inlet and 70 % efficiency, outlet temperature is about 409 K before intercooling. Taken to 80 kPa baro with the same manifold target and losses, PR = 210 / 75 = 2.8, and the outlet temperature at the same efficiency rises to about 447 K; on the map the point moves up toward the speed lines and, at low rpm, toward surge.

## Disputed / conflicts
- Blow-off valve and response. The common claim is that a valve keeps the turbo spinning for quicker re-boost. One practitioner doubts it and a single back-to-back test at about 1 bar found no difference; the same practitioner warns that at around 3 bar the rotor carries more energy and much more air must be vented, so the result should not be generalised, and valves should not be removed on its strength. Discriminating test: the same lift and re-apply sequence logged at high rate with and without the valve, at the boost level in question, controlling for exhaust temperature growth during the test.
- Deleting the valve: tolerated better by ball-bearing turbos and sometimes omitted with anti-lag so boost is not vented, but one practitioner warns lift-off pressure on high-power drag cars can push the throttle plate open.
- Bearing thrust strength figures quoted for ball-bearing cartridges are recalled manufacturer claims; treat with caution.

## Citations
- engineering-texts: Engine, combustion, charging and control engineering texts.
- practice: Practitioner training and tuning practice, distilled and cross-checked.
