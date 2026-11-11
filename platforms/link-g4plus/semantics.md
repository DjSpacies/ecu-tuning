---
id: platforms/link-g4plus/semantics
title: How Link G4+ tables behave
layer: L3
status: draft
confidence: medium
sources: [vendor-documentation, file-format-analysis, practice]
verified: 2026-11-10
applies_to: {fuels: [gasoline, ethanol, methanol], engines: [all]}
depends_on: []
supersedes: []
---

# How Link G4+ tables behave

Facts are from the PCLink G4+ 5.6.8 help (`vendor-doc`) unless tagged. They apply to that version.

## Fuel
- Three Fuel Equation Modes from firmware 5.2.0: Traditional, Modelled, and Modelled - Multi Fuel.
- In Modelled modes the Fuel Table is the engine's volumetric efficiency. In Traditional mode its numbers mix VE with other constants, and Master Fuel sets the overall level. In every mode a higher number means more fuel.
- A Modelled mode needs real physical data: engine capacity, injector flow with the differential pressure it was rated at, and fuel properties. Traditional does not use Injector Flow at Rated Pressure.
- The AFR/Lambda Target Table is always used in Modelled modes and optional, though recommended, in Traditional. Tune to match that table so a target can change later without retuning the fuel table.
- Modelled - Multi Fuel has two target tables, blended by the Multi Fuel Blend parameter.
- Dead time depends on battery voltage, differential fuel pressure and the drive type. A typical figure at 3 bar and 14 V is just under 1 ms. A short pulse width adder corrects non-linear flow, generally below about 4 ms.
- The fuel table's axes are configurable, up to 22 speed columns and 20 load rows.

- Equation Load Source is how the fuel equation estimates air charge. Load=MAP is the preferred mode; Load=BAP is only for naturally aspirated engines with no usable MAP signal; a crossover mode exists for a weak MAP signal in vacuum.
- Modelled modes take extra inputs: Fuel System Type, Base Fuel Pressure, Fuel Density and its temperature coefficient, Stoichiometric Ratio and a Fuel Charge Cooling Coefficient.
- Multi Fuel setup tunes the first fuel completely, in Modelled mode, on unblended fuel, before setting up the second.

- A correct order applies to fuel tuning: in Traditional mode, configure Charge Temperature Correction before tuning, and get a good range of fuel table numbers first. Master Fuel is only used in Traditional mode.
- Fuel System Type selects how differential pressure is obtained; injector flow, rated pressure and base fuel pressure must agree. In Modelled modes dead time needs MAP and fuel pressure sensors to correct fully.
- Fuel Density guidelines at 20 C: gasoline 0.745, ethanol 99 % 0.789, ethanol 95 % 0.8077, methanol 0.791 g/cc. The temperature coefficient must be set whether or not a fuel temperature sensor exists.
- The Fuel Charge Cooling Coefficient is set before final tuning and not changed afterwards.
- MAP is not a recommended Fuel Table load axis in the help's example setups; MGP or TP are used. The Equation Load Source is separate.
- IAT fuel correction is recommended for all applications.
- Multi Fuel: use one rated pressure for both fuels' injector flow figures, and the blend table must output 0 % on the first fuel and 100 % on the second. Do not assume E85 is 85 % ethanol.
- Enrichment sequence: pre-crank prime, crank enrichment, post-start enrichment with decay, then warm-up enrichment alone. Warm-up is best with one axis on throttle position and the other on coolant temperature.
- Accel Load Axis is recommended to be TPS. Accel Hold is counted in injection events, so its meaning depends on injection mode. Wakeup Enrichment applies to group fire only.
- Overrun fuel cut needs a throttle position sensor, and its de-activation rpm must sit above idle speed. On electronic throttle, keep a very low angle at fuel return to avoid a surge.

## Fuel tuning order (help, Fuel Tuning Procedure)
Before tuning in any mode: confirm the fuel and engine settings, because some force a full retune if changed later; zero or set known values in the correction tables and bring them in afterwards; and fill in the target table.
- Traditional: set up charge temperature correction first if used, set Master Fuel Trim to 0, choose Master Fuel for a usable span (about 50 at mid rpm and load, 20 to 30 at idle, 75 to 85 at full power).
- Modelled: every fuel and injector figure must be right, not guessed. Configure the charge temperature table first; check that fuel pressure holds at the Base Fuel Pressure setting; set the Fuel Charge Cooling Coefficient before final tuning. Changing either of those later means retuning the VE table.

Fuel System Type: None (no pressure correction, a last resort), MAP Referenced, Returnless (needs MAP), or FP Sensor (needs fuel pressure and MAP sensors, and is the only one that supports a rising rate regulator).

Charge temperature is blended between IAT and ECT by a table (0 % means IAT, 100 % means ECT). It is always used in Modelled modes. Sensor position matters: a sensor before the throttle body may not represent the charge, and a heat-soaked manifold raises charge temperature.

## Boost setup (help, Closed Loop Boost Setup Guide)
The help's worked setup for 220 kPa zeroes all gains and trims, tunes each boost-target row of a 3D wastegate duty table separately (rising from 180 kPa), and enables feedback last with very soft gains. Its example values are P 0.2, I 0.1, D 0.1, a 90 % maximum duty clamp and a 15 % integral clamp, with 90 % stage 1 duty.

## Knock settings
Clear I-Trim Tables decides if learned knock retard resets at key-on. Set to power-on (the common choice), the engine starts in its most advanced state and timing is removed after knock is detected. Set to off, the stored retard stays, so the stored values must be right. Window Start is measured after the ignition event, and the sum of window start, length, retard limit and processing delay must fit between the two closest firing events.

## Ignition
- Ignition Delay compensates for signal path delay, which grows in crank degrees with rpm and otherwise gives a slight retard of a few degrees.
- Dwell must rise when voltage falls. Not all igniters limit current, so excessive dwell can be harmful.
- Above 8 cylinders, knock control and individual cylinder trims do not work correctly.
- Trailing split tables appear only with Engine Type set to Rotary.

## Limits
RPM, MAP, speed and launch limits can be ignition, fuel or combined cuts. With group injection the help recommends ignition cutting for smooth limiting; with auxiliary injection only ignition cut. A correct boost setup should never reach the MAP Limit, and the limit does not directly control pressure. Rpm can still be exceeded on down-shifts.

## Idle and VVT
Closed-loop idle needs a wheel speed source, throttle position, and a finished fuel and ignition tune. An ISC solenoid is recommended at 200 Hz, and must move engine speed 300 rpm above and below target at all temperatures. Use a preset VVT mode where one exists. For inlet cams the most retarded position is the least aggressive; for exhaust cams the most advanced is.

## Triggers
A valid tooth count divides evenly into 360, and on a missing-tooth wheel it counts the teeth as if none were missing. Arming threshold and filtering are advanced features. Timing must be calibrated with a timing light after setup.

## Direct injection
GDI capable units exist (such as the Force GDI). Do not guess pump control settings; injector duty cycle is limited to 50 % by hardware on those drives, and setting a saturated drive where Direct Injection mode is needed can damage the injector.

## Multi Fuel, in detail
Fuels can differ in stoichiometric ratio, density, viscosity, injector flow, target lambda, VE and cold start. Multi Fuel also suits two similar fuels or two tunes on one fuel, switched by a dial. Setup: tune the first fuel on unblended fuel in Modelled mode, use 3D prime, crank and post-start tables against ECT and blend, and set Warm Up Enrichment to Multi-Fuel. Then on unblended second fuel, change to Multi Fuel, set the second fuel's flow, density, coefficient, stoichiometric ratio and charge cooling coefficient, start the blend table linearly, and copy the target table to Table 2 and adjust it. A second VE table (Interpolate Between) is only needed for a large fuel change.

## Knock control details
Retard Gain is degrees removed per percent of knock level above threshold, typically 0.5. Advance Delay and Advance Rate set how timing returns. Processing delay in degrees is 0.004 x rpm on firmware 5.6.5 and later and 0.012 x rpm on earlier versions; window start, length, retard limit and delay must fit between the two closest firing events, and the help gives maximum rpm per cylinder count. Above those limits individual cylinder detection can be wrong. Set the RPM High Lockout below them.

## Tools
Quick Tune adjusts the main fuel table only, never ignition, and the help says it assists rather than replaces a professional tuner. Tune ignition and boost control before using it. Quick Trim and closed-loop lambda are separate functions. Mixture Map and Quick Trim need the fuel and target tables to have matching load sources set, or a load value entered. Mixture Map gives each cell its average actual, target, sample count and error, and can apply a correction. Closed-loop lambda must be off for Quick Tune, which has lockouts for coolant, load and rpm.

## Transient
Acceleration enrichment has Accel Mode, Load Axis, Clamp Table, Sensitivity, Hold, Decay, Deadband, Cold Correction and Load Correction, and Wakeup Enrichment.

## Closed-loop lambda
A minor trim for use while driving. The help states it is not a tuning aid. Modes differ for narrow and wide band sensors, and stoichiometric modes dither around target.

## Ignition and knock
Knock control operates only above 500 rpm. It reduces advance when knock is detected, through internal detection or an external unit on a digital input. It is not a substitute for a correct map (`practice`).

## Boost
Closed-loop boost runs in three stages: a fixed duty to spool, then PD on a base duty table approaching the target, then full control. Open-loop duty must already give stable boost (`practice`). The help recommends 20 Hz for the boost solenoid in one topic and 15 to 20 Hz in another; higher frequencies can make it unpredictable.
