---
id: principles/combustion/knock
title: Knock and surface ignition
layer: L1
status: draft
confidence: high
sources: [engineering-texts, reference-data, practice]
verified: 2026-11-11
applies_to: {fuels: [gasoline, ethanol, methanol], engines: [all]}
depends_on: [principles/fuels/octane-rating]
supersedes: []
---

# Knock and surface ignition

## Claim
Knock (detonation; the two words mean the same thing) is autoignition of the unburned end gas after the spark has started a normal flame. Its pressure waves damage engines by stripping the protective thermal boundary layer and by shock-loading the bottom end. Anything that raises end-gas temperature, pressure or time at temperature makes it more likely. Pre-ignition is a different fault: a hot spot lights the charge before the spark, and it destroys parts faster.

## Why (derivation)
### Knock
The end gas is compressed and heated by the piston and by the advancing flame. If its chemistry reaches ignition before the flame arrives, the remaining charge releases its energy almost at once. The practitioners contrast a normal flame front of the order of 5 to 100 m/s with a detonation pressure front of several hundred to about 2000 m/s; the figures differ between sources but the gap of one to two orders of magnitude is the point. The result is a sharp pressure spike that rings the chamber at its acoustic frequencies. One practitioner showed in-cylinder traces from a single engine: at the MBT advance (20 degrees in that example) peak pressure sat about 16 to 18 degrees after TDC near 80 bar, while 35 degrees of advance gave a steep rise before TDC with oscillation and a peak over 120 bar. Sources describe knock peaks from about double to three times normal.

### Two damage mechanisms
- **Heat.** A thin layer of relatively stagnant gas normally insulates piston and head from flame temperatures far above the melting range of aluminium alloys (about 700 to 750 C in the sources). The pressure waves scour that layer away, so heat flux jumps. Light, sustained knock gives a sandblasted or finely pitted crown, starting at the outer edge (often the intake side) and at sharp features such as valve-relief edges; similar pitting appears on the head and top of the bore. Severe knock at high output can melt out the side of a piston within seconds.
- **Mechanical shock.** The spike hammers the crown, ring lands, rods and big-end bearings. Cast pistons, being brittle, crack ring lands (which may only show as lost compression, blow-by and oil use); rods bend on engines with weak rods; head gaskets lift; ring grooves can be closed up so rings pinch.

### Severity scales with specific output
Damage depends on power per cylinder and rpm, not total power. Practitioners contrast a tired low-output engine that pings while labouring uphill for years without harm with a high-boost engine at high rpm, where almost any knock breaks parts. A two-litre four making a given power is hurt far sooner than a large V8 making the same power.

### Pre-ignition
Pre-ignition starts from a hot spot (glowing deposit, overheated plug electrode) before the spark, possibly early in compression where pressure is lowest. The piston then compresses a burning charge for the whole stroke, so heat input is far longer and greater than with knock. Practitioners report failure in a handful of cycles, against about a second for heavy knock. The typical sign is a hole or depression melted through the centre of the crown, torched rings and a swollen piston scuffing the bore. Because it is not set by spark timing, the tuner's ignition map is usually not its direct cause. Low-speed pre-ignition in downsized direct-injection turbo engines is a related mechanism.

### Knock frequency follows the bore
The first circumferential acoustic mode of a cylinder of bore B has frequency f = 1.841 c / (pi B), with c the speed of sound in the hot gas. With f in kHz, B in mm and c near 980 m/s, this is close to the tuners' rule f = 1800 / (pi x B). Higher modes and harmonics sit above it; many factory sensors and filters work at about twice the fundamental, where mechanical noise is weaker.

## Assumptions
Homogeneous spark-ignition combustion. Damage temperatures and pressure ratios are the sources' approximate figures, not design values.

## Breaks when
- Audible or sensor-detected knock is only a proxy for chamber pressure events. Sensor signals include mechanical noise, so a low reading at high rpm does not prove the absence of knock (see `methodology/knock-sensing-setup`).
- The frequency rule gives a starting point only: chamber shape, temperature and the sensor's own response move the best detection frequency.
- Post-mortem signs overlap: both knock and pre-ignition can break ring lands, and a melted piston after a fuel fault may show features of both.

## Practical use
### What raises knock risk
More spark advance; more boost or compression; higher intake air temperature or poor intercooling; hotter coolant (one practitioner gained timing on a high-compression engine by fitting a cooler thermostat, and saw track coolant run well above dyno coolant); sustained full load, which soaks heat into the chamber so a limit found on a fresh engine overstates what it tolerates; lower octane; a mixture leaner than a rich full-load target; residual gas and restrictive exhaust; deposits; oil entering the charge through worn rings or the crankcase ventilation, which dilutes the fuel's knock resistance; and chamber design. Fuel temperature should matter in the same direction (one practitioner's untested view). Cam timing changes the burn rate and filling and can move an engine towards or away from its limit.

### Where it happens
Low rpm at high load, and the peak torque region, are where cylinder filling and pressure are highest; practitioners repeatedly find the knock limit there. Peak torque knock magnifies mechanical stress; high-rpm knock is no safer, because peak power and heat are made there.

### Fuel and mixture levers
Richer mixtures cool the charge and, on an engine already limited by knock, can let it accept more timing for a net gain. On alcohol fuels and high-octane race fuel the mixture window is wide; on low-octane pump fuel small lambda changes shift knock tendency a lot.

### Diagnostics from parts and plugs
- Sandblasted crown edge, sharp ring-land erosion, pitted head: knock.
- Hole through the centre of the crown, piston swollen: pre-ignition.
- Spark plug insulator under magnification: black specks are an early sign; tiny balls of aluminium mean significant detonation that should already have been heard.
- Knock does not change the measured mixture (the charge is fixed at intake valve closing), and exhaust temperature probes are too slow to see sporadic knock; neither is a knock detector.

Treat any suspected pre-ignition as an immediate stop.

## Worked example
An engine shows knock at 0.95 lambda with 22 degrees of timing at peak torque. Hotter intake air than the previous pull is a likely contributor. The safe response is to remove timing or load in that region, not to assume the sensor is wrong.
Detection frequency for an 86 mm bore: 1800 / (pi x 86) = 6.7 kHz, second harmonic about 13.3 kHz; practitioners used about 6.7 and 13.7 kHz on such engines. For a 95.5 mm bore the estimate is 6.0 kHz, and in one demonstration 12 kHz showed knock more clearly than 6 kHz.

## Disputed / conflicts
- **Theory.** The combustion textbook records two historical explanations, autoignition and detonation theory. Modern practice treats autoignition of end gas as the origin, with possible developing detonation waves in severe events.
- **Mixture.** The combustion textbook places the highest octane requirement slightly rich of stoichiometric, falling on both sides. Practitioners say a leaner mixture raises knock tendency; both hold over part of the range only (see `principles/myths/lean-mixtures-melt-pistons`).
- **Knock from heat versus from advance.** One practitioner finds that knock caused by heat and knock caused by over-advance sound, log and damage parts the same way, heat simply bringing an engine nearer its limit. That is practice, consistent with end-gas theory, not a separate test.
- **Peak pressure under knock.** Stated as about double normal in one source and two to three times in another; the pressure-trace example sits at about 1.5 times. Magnitude depends on severity.
- **Alcohol fuels.** Practitioners agree methanol and ethanol strongly resist knock but are relatively prone to pre-ignition at very high boost, linking it to oil washed into the charge by very rich mixtures and to hot spots. The mechanism is not settled in the sources; one practitioner said he could not recall it fully.
- **Melting temperature.** Practitioners quote 700 to 750 C for piston alloys; the exact solidus depends on the alloy.

## Citations
- engineering-texts: Engine, combustion, charging and control engineering texts.
- reference-data: Published reference data: thermophysical properties, fuel data, sensor and injector data sheets, statistics.
- practice: Practitioner training and tuning practice, distilled and cross-checked.
