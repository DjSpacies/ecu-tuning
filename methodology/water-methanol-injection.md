---
id: methodology/water-methanol-injection
title: Water/methanol injection
layer: L2
status: draft
confidence: medium
sources: [practice, engineering-texts]
verified: 2026-11-11
applies_to: {fuels: [gasoline, ethanol, methanol], engines: [all]}
depends_on: [principles/fuels/energy-and-charge-cooling, methodology/knock-assessment]
supersedes: []
---

# Water/methanol injection

## Claim
Water/methanol injection buys knock margin, and a tune that uses that margin depends on it. It makes no power by itself: the gain comes only from the timing or boost it permits, and only on an engine that is limited by knock. The system must be monitored, and a failure must revert to a safe tune.

## Why (derivation)
Evaporation cools the charge and adds resistance to knock. Water has roughly six times the latent heat of gasoline and cools strongly but releases no energy; methanol also cools strongly, burns, and has a high octane rating, which raises the effective knock resistance of a low-grade pump fuel. A mix of the two combines both. Timing or boost added on the strength of that is unsafe the moment delivery stops.
Because the extra margin is only useful where the engine was knock-limited, an engine that already reaches MBT without knock gains little or nothing (at most a slight density gain). Injecting fluid without retuning, or injecting too much, costs power: in one test plain water with no tune change lost about 5 kW from about 180 kW, a much larger nozzle cost more, and very excessive flow can quench the flame and misfire.

## Assumptions
A delivery monitor exists, such as a flow or level switch.

## Breaks when
- Tank empty, pump or nozzle failure, or a controller fault.
- Used as a replacement for an intercooler: it works and beats no intercooler, but if the tank runs dry the engine meets very hot charge air that is hard to protect against in the tune. One practitioner would not do it today.
- Methanol content much above half makes the stored fluid flammable.
- Tap water deposits minerals that block nozzles over time; use distilled water.

## Practical use
### Is it worth it?
Check first whether the engine is knock-limited: knock appearing while torque still rises with advance. It is mostly a tool for turbo engines on pump fuel, though a very high-compression NA engine can benefit. On E85, the fuel's own cooling largely duplicates the effect; in one comparison an engine on pump fuel with 50/50 injection still knocked while torque was rising, but reached MBT on E85 at the same boost. On an engine that already makes peak torque before knock (one rotary example), its value is enabling more boost, not more timing at the same boost.

### Sizing and control
- A common guide is flow of about 25 % of total fuel flow; one practitioner starts lower, about 15 %, and builds up on the dyno. Work from actual fuel flow (total injector flow times peak duty), not injector ratings.
- A progressive controller that drives the pump between a start boost and a full-flow boost keeps fluid roughly proportional to airflow instead of dumping full flow at low boost.
- Start injection before the point where the engine becomes knock-limited; an engine that knocks almost as soon as it makes boost may need it from very low boost (about 2 psi in one example). Do not spray in vacuum: it gives no benefit and hurts drivability.
- An ECU output driving a high-current pump needs a solid-state relay or a half-bridge; a constant pump with a fast low-current solenoid valve near the engine is an alternative.
- Consumption tracks power; budget fluid for testing.

### Nozzle location
After the turbo and after the intercooler. Injection before the compressor is reported to help compressor efficiency, but poorly atomised fluid erodes the wheel; before the intercooler, water can drop out and pool inside it.

### Tune structure
1. Tune fuel and spark fully without injection: this is the fallback.
2. Wire a delivery or active signal to the ECU, combined with arming, positive boost and high throttle, to switch in dedicated fuel and ignition offset tables and any higher boost limit.
3. Keep the same lambda target. Water does not burn and does not shift the lambda reading; the methanol is fuel, so remove port fuel while spraying to hold target rather than letting it run rich.
4. Add timing only where knock margin allows, typically a few degrees (one practitioner expects at least 4 to 6 degrees over a 91 to 93 octane value), verified with knock monitoring.

### Hydraulic lock
Practitioners consider a large nozzle practically unable to hydrolock a running engine, since even 1000 cc/min is small at boost airflow. The real risk is a system that pulses fluid while the engine is stopped.

## Decision rules
Only add timing or boost if delivery can be detected and the tune falls back when it stops. Without that monitor, do not tune on the assumption it is working.

A common guide is water/methanol flow of about 25 % of the total fuel flow; one practitioner starts at about 15 % and increases on the dyno.

## Data gates
Delivery status logged. Also boost, ignition timing, lambda against target, per-cylinder knock, and the active state of the injection offset tables.

## Worked example
A test gained power by adding 4 degrees and 10 kPa. Without a working failsafe, that added margin has to be removed.
In that test (a low-boost turbo DI engine at 12.5:1 on pump fuel), wheel power rose from about 183 to 199 kW with knock still below threshold, while exhaust temperature fell only from about 715 to 700 C. The small EGT change is not a measure of the cooling, since timing and boost rose at the same time; more gain is expected on higher-boost engines where there is more compression heat to remove.
Sizing for 4 injectors of 550 cc/min at 85 % peak duty: fuel flow is about 1870 cc/min; 15 % is about 280 cc/min of fluid as a starting nozzle, 25 % about 470 cc/min.

## Disputed / conflicts
- **Cross-check.** An engine textbook states water injection is used to mitigate pre-ignition and provide cooling, in general terms. The 25 % flow guide has no textbook value.
- **Pre-compressor injection.** Reported to improve compressor efficiency by some; practitioners warn of wheel erosion and, for pre-intercooler injection, pooling. Neither side is tested in the sources.
- **Adding it to E85.** Practitioners expect little gain because of duplication; this is untested opinion in the sources.
- **Effective octane.** One source says methanol injection can make 91 to 93 pump fuel behave like roughly 100 to 110; this is a rule of thumb, not a measured rating.

## Citations
- practice: Practitioner training and tuning practice, distilled and cross-checked.
- engineering-texts: Engine, combustion, charging and control engineering texts.
