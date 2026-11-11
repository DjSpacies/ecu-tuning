---
id: principles/fueling/injector-flow-and-dead-time
title: Injector flow, dead time and duty
layer: L1
status: draft
confidence: high
sources: [engineering-texts, reference-data, practice]
verified: 2026-11-11
applies_to: {fuels: [gasoline, ethanol, methanol], engines: [all]}
depends_on: [principles/fuels/stoichiometry-and-lambda]
supersedes: []
---

# Injector flow, dead time and duty

## Claim
An injector delivers fuel at a rate set by the pressure difference across its nozzle, and only for the part of the commanded pulse during which the valve is actually open. Delivered mass is right only when three things are right: flow at the real differential pressure, dead time at the real voltage and differential pressure, and the injector's behaviour at short pulses, where flow stops being proportional to pulse width. Errors in any of them are a fixed time or a fixed shape, so they matter most where pulses are shortest (idle and light cruise) and least at long full-load pulses.

## Why (derivation)

### Flow and differential pressure
Flow follows the orifice relation: volume flow Q scales with the square root of differential pressure dP, so Q2 = Q1 x sqrt(dP2 / dP1). dP is rail pressure minus the pressure at the nozzle tip. For an injector downstream of the throttle that is manifold pressure; for one mounted upstream of the throttle (for example outside intake trumpets) it is roughly barometric. Rail pressure on its own is not the driver: if manifold pressure rises and the rail does not, delivery falls, and if they were ever equal no fuel would flow at all.
- A manifold-referenced regulator raises rail pressure one for one with manifold pressure, so dP and flow per millisecond stay constant.
- A fixed-pressure (returnless or unreferenced) rail holds rail pressure constant against atmosphere, so dP is highest in deep vacuum at idle, about the set pressure at naturally aspirated full load, and falls by every kPa of boost.
- A rising-rate regulator (more than one for one) is an old workaround for ECUs that could not add fuel in boost; an ECU that assumes one-for-one will mis-fuel with it.

Injector ratings are meaningless without the pressure they were measured at, and may be given as volume (cc/min) or mass (lb/h). Converting needs the fuel density: about 0.74 to 0.75 g/cc for pump gasoline gives the familiar factor of roughly 10.2 cc/min per lb/h, which does not hold for alcohol fuels or hot fuel. Alcohol's different viscosity can also change volume flow slightly at the same pressure, by an amount that varies between injector designs and is rarely published.

### Dead time
The injector is a solenoid valve with a moving armature and pintle. After the drive signal starts, current must build and the valve must lift against spring and fuel pressure before flow begins; at the end of the pulse it takes a shorter time to close. The net of the opening and closing lags is the dead time (also called offset, latency or battery compensation): the difference between commanded open time and the time fuel effectively flows. Commanded pulse = effective pulse + dead time.
- Dead time rises as battery voltage falls (less energy to lift the valve). Published curves for a 1000 cc class injector run from about 1 ms near 14 to 16 V to 2 to 3 ms near 8 V.
- Dead time rises with differential pressure (the valve opens against it). At very high dP and low voltage some manufacturers list no value at all: the valve may not open, which can stop an engine starting when cranking pulls the battery down.
- Dead time depends on the driver circuit, so data measured on one ECU's drivers can differ from another's for the same injector.
- Peak-and-hold drive (a high opening current, then a lower holding current) was developed for heavy-pintle, low-resistance injectors and shortens their opening. Modern light-armature injectors are high resistance and open quickly on simple saturated drive.

### Why a dead-time error looks the way it does
Because dead time is a fixed slice of every pulse, an error in it is a fixed slice too. With a 0.1 ms error, a 1.5 ms idle effective pulse is wrong by about 7 %, but a 12 ms full-load pulse by under 1 %. A wrong dead-time-to-voltage slope makes mixture move when voltage moves (fans, lights, charging state), again mostly at idle.

Percentage compensations (air temperature, coolant, manifold pressure scaling, cylinder trims) are meant to scale only the effective pulse. If dead time is not modelled and the fuel table holds the whole pulse, every percentage is also applied to the dead time, so a requested change produces a larger real change. An ECU that doubles pulse width expecting double fuel gets more than double when dead time is hidden inside the number.

### Short-pulse non-linearity
Even with dead time correct, flow is proportional to pulse width only above some pulse length, because at short pulses the valve does not reach full lift or bounces. Characterisation data for port injectors typically show a straight line above roughly 1.5 to 2.5 ms (it varies by design), a different, non-linear region below that, and a sharp knee around 0.8 to 1.4 ms below which delivery collapses. Some older large high-flow designs show pintle bounce: a trough in the flow curve in which a shorter pulse can deliver more fuel, so the mixture responds backwards to a fuel change. Some also show a kink at high duty (around 80 %) before they go fully static.

What limits idle control is the smallest fuel quantity the injector can meter repeatably compared with what the engine needs at idle, not the pulse width at the knee by itself. A very large injector with excellent short-pulse behaviour can still overfuel a small engine at its shortest usable pulse; a smaller injector with poor low-end behaviour may never go near its bad region because idle needs several milliseconds. Operating on the knee is fragile: a small negative trim can drop delivery sharply and stall the engine.

Fuller injector models describe this with a short-pulse adder (extra time added below a short-pulse limit), a two-slope flow curve, or a full linearisation table of required pulse against desired quantity, differential pressure and voltage. These come from laboratory flow testing, not from tuning.

### Duty and cycle time
Duty is commanded pulse over cycle time. A four-stroke cycle is two revolutions, so cycle time in ms = 120000 / rpm (120 ms at 1000 rpm, 20 ms at 6000 rpm, about 13.3 ms at 9000 rpm). For the same fuel per cycle duty therefore rises with rpm, and a fixed minimum off time between pulses cuts the usable maximum duty more at high rpm: with 2 ms off time the ceiling is 90 % at 6000 rpm and lower above it.

## Assumptions
Liquid, incompressible fuel flow; injector characterised on comparable drivers and at the pressures and voltages it will see; the duty formula assumes one injection per cycle per injector (sequential). Fuel temperature near the characterisation temperature.

## Breaks when
- Pressure or voltage outside the characterised range, or a regulator that does not hold its nominal value (pump overrunning a small regulator at idle, pump falling over at high load).
- Very short pulses near or below the knee, or operation in a bounce trough or high-duty kink of older designs.
- Duty approaching 100 %: the valve cannot close between events, flow is non-linear near the top, and there is no room left for compensations. Sources report delivery becoming inconsistent above roughly 95 %.
- Hot fuel can vaporise in the rail; fuel density shifts with temperature.
- Modifying injectors (removing the tip diffuser to raise flow) changes flow, dead time, spray and linearity, so every published figure becomes invalid.
- Spray pattern and targeting are outside this model: a wide or mistargeted spray wets port walls (see `principles/fueling/transient-fuel-film`) and can leave unburnt liquid fuel that a wideband does not see.

## Practical use
- Use `principles/calculators/injector.py`: `flow_at_pressure`, `differential_pressure_kpa`, `pulse_width_ms`, `cycle_time_ms`, `duty_pct`.
- Always work in differential pressure. Log rail pressure and manifold pressure and compute dP, rather than trusting gauge rail pressure.
- When idle needs a large change and full load does not, suspect dead time or short-pulse data before fuel tables. When mixture moves with battery voltage, suspect the dead-time slope.
- When removing fuel at idle makes the mixture richer, or a small change swings it a long way, suspect operation in a non-linear part of the injector's flow curve rather than the fuel table.
- Before blaming the fuel table for a high-rpm lean trend, compute duty: rpm raises duty at constant power.
- Identify drive type before connecting anything: low-resistance injectors (roughly 0.5 to 5 ohms in the sources) need peak-and-hold drive or a series ballast resistor; high-resistance injectors (roughly 8 to 15 ohms) suit saturated drive. A low-resistance injector on a saturated driver without ballast can damage the driver. A ballast pack left in circuit with high-resistance injectors makes delivery unstable. Measure resistance, since one model may be sold in both types.
- Procedure for entering data lives in `methodology/injector-characterisation`; sizing in `methodology/fuel-system-sizing`.

## Worked example

### Pulse width and duty
1000 cc/min at 300 kPa differential, fed 40 mg per cycle of gasoline: 1000 cc/min x 0.745 g/cc = 12.42 g/s, so 40 mg / 12.42 g/s = 3.22 ms effective, plus 0.8 ms dead time = 4.02 ms. At 6000 rpm the cycle is 20 ms, so duty is 20 %.

### Returnless rail under boost
Rail fixed at 400 kPa gauge, barometer 100 kPa. At idle with 30 kPa absolute manifold pressure, dP = 400 + (100 - 30) = 470 kPa. At 200 kPa absolute boost, dP = 400 - 100 = 300 kPa. Flow falls to sqrt(300 / 470) = 0.80 of its idle-condition value, and dead time also shifts, so a model that assumes one pressure is wrong in both places.

### Compensation error from hidden dead time
Effective pulse 2 ms, dead time 1 ms. A 10 % air-temperature correction should add 0.2 ms. If dead time is not modelled and the table holds 3 ms, the same 10 % adds 0.3 ms: 50 % more correction than intended.

## Disputed / conflicts
- **Maximum duty.** The sources give a spread of personal ceilings: about 85 % (often called conservative, and traced to older designs that went non-linear near the top), 85 to 90 %, 87.5 %, and up to about 90 % for modern compact injectors. Several practitioners call the idea that injectors overheat or fail at high duty a myth, citing manufacturer endurance testing with the valve held open; their stated reasons for a ceiling are top-end non-linearity and the need for headroom (cold dense air, boost overshoot, compensations). Treat any figure as a practice margin, not a physical limit. Discriminating test: log duty against lambda on a ramp run and look for lambda departing from target as duty rises past the 90s.
- **Gain from raising pressure.** The square-root law gives about 41 % more flow for doubled differential pressure; one practitioner quotes 25 to 30 %. The lower figure may fold in pump flow loss at higher pressure, which is real but is a system effect, not an injector one. Measure flow at both pressures to settle it for a given system.
- **Where linear flow starts.** Sources quote 1.5 ms, about 2 ms and 2 to 2.5 ms for different injectors; it is an injector property and must be read from that injector's data.
- **Resistance bands.** Quoted thresholds between low and high resistance vary (about 4, 5, 6 or 7 to 8 ohms). The sources agree there is effectively nothing in between, so a reading of 9 ohms or more is high resistance.
- **Two data sets for one injector.** An injector maker's and an ECU maker's dead time at the same voltage and pressure were seen to differ by about 15 %, attributed to driver circuits. Pick one consistent set and confirm with the voltage test in `methodology/injector-characterisation`.

## Citations
- engineering-texts: Engine, combustion, charging and control engineering texts.
- reference-data: Published reference data: thermophysical properties, fuel data, sensor and injector data sheets, statistics.
- practice: Practitioner training and tuning practice, distilled and cross-checked.
