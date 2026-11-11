---
id: methodology/rotary-engines
title: Rotary engine tuning
layer: L2
status: draft
confidence: medium
sources: [practice]
verified: 2026-11-11
applies_to: {fuels: [gasoline, ethanol, methanol], engines: [rotary]}
depends_on: [principles/combustion/mbt-timing, principles/combustion/knock]
supersedes: []
---

# Rotary engine tuning

## Claim
Rotary engines respond to fuel and ignition the way piston engines do: torque rises with advance, plateaus and falls, and power has a plateau against mixture. The same methods therefore apply. The differences are in the margins. Rotaries tolerate almost no knock, reject more heat to the exhaust, are run somewhat richer, idle more retarded, and have twin plugs whose leading-to-trailing split acts as part of total timing. The tuner sets every margin on the conservative side and does not chase MBT or peak-power lambda under load.

## Why (derivation)
- **Knock intolerance**: apex seals are damaged by very little detonation, sometimes one or two events. By the time knock is detected, damage may already be done.
- **Heat**: rotaries are less thermally efficient and reject more heat to the exhaust. Practitioner measurements put cruise EGT on a turbo rotary about 100 to 200 C above a comparable turbo four-cylinder. Fuel beyond the power requirement cools the charge and the exhaust.
- **Gentle retard side**: torque falls away more gently on the retarded side of MBT than on a piston engine, so a conservative timing costs little power.
- **Twin plugs**: the leading plug does most of the burn (about 95 % in one practitioner's estimate). Disabling the trailing plugs barely changes power, while disabling the leading plugs makes the engine run very badly. The trailing plug completes combustion and helps emissions and smoothness. Reducing the split (firing trailing sooner) advances the overall burn and so behaves like adding timing. Zero split is effectively over-advanced, and trailing before leading is dangerous.
- **Ports instead of valves**: port overlap (heavily so on bridge and peripheral ports) means the wideband sees unburnt mixture and does not report the true combustion mixture at idle and light load. Ported engines need higher idle speeds and have poor part-throttle drivability.
- **Lubrication oil in the charge**: oil from the metering pump or premix in the fuel lowers effective octane and adds knock and pre-ignition tendency.
- **Fuel delivery**: one injector per rotor usually cannot meet demand, so primaries and secondaries are staged.

## Assumptions
- Twin-plug rotary with independent trailing control (or a trailing split table).
- A wideband after the turbine (or in the collector), ideally per-rotor EGT as a secondary check.
- Base timing verified with a strobe on both leading and trailing plugs.
- Builder's guidance known for premix ratio, boost and rev limit.

## Breaks when
- **Port type**: stock, bridge and peripheral ports differ greatly in idle speed, idle mixture readings and light-load behaviour.
- **Mixture readings at idle on ported engines**: the displayed lambda is not the burn mixture.
- **Older ECUs without split control**: some fire both plugs together, which is zero split, effectively over-advanced.
- **Sign conventions**: some software enters the split as a negative number for trailing-after-leading, so a positive entry fires trailing first.
- **Aggressive rev limiting**: violent popping, especially from ignition-only cut, can on its own damage stock apex seals. A soft limiter, cutting fuel and spark together on a rotor, is preferred.
- **Race use**: sustained load and heat move targets richer than a street car.

## Practical use
### Base set-up
- **Timing marks vary by generation**: older engines carry separate leading and trailing marks (5 and 20 degrees ATDC on some series), while later engines carry one mark at 20 degrees ATDC. Use a rotary timing-lock mode that fixes leading and trailing at known angles, strobe the trailing plug, then lock normally so the leading plug fires on the same mark and check it. Have a helper hold rpm, because the engine runs badly there. Correct the base angle, then unlock. A base timing error leaves the engine very retarded, hot, and unresponsive to tuning, and is a common source of damage.
- **Trigger mode**: on some platforms the obviously named rotary trigger preset is not the right one for every generation. Check against the strobe.
- **Base ignition for first start (one practitioner's turbo street map)**: about 5 degrees at idle (rotaries idle far more retarded than piston engines), about 15 degrees in vacuum up to 100 kPa, 10 degrees from 100 to 160 kPa, 5 degrees from 160 to 220 kPa. Very conservative until optimised.
- **Split base**: start from factory-style values: about 15 degrees at idle (smooths idle), about 10 in cruise, interpolating down to about 8 to 10 degrees at full boost. If unsure, 10 degrees everywhere. In most software the trailing plug follows the main table plus split, so tuning the main table moves both.
- **Staging**: some ECUs limit primaries by a minimum off-time rather than a duty limit, so the usable primary duty depends on rpm, and then blend in secondaries automatically. Seamless staging depends on accurate injector characterisation. With secondaries mounted outside the trumpets on NA engines, the tuner may deliberately shift fuel toward secondaries at high rpm.

### Fuel targets (practitioner examples, not limits)
- **Idle**: about 0.92 on a stock port (rotaries idle poorly at stoich). On ported engines choose by experiment the leanest displayed value that still idles well, at a higher idle speed (one practitioner cites about 950 to 1000 rpm stock and 1500 to 1800 rpm with a decent bridge port).
- **Cruise**: lambda 1 only in true cruise (roughly 2500 to 3500 rpm, light vacuum) on a street car, with EGT watched. Vacuum areas above about 3500 rpm at about 0.95. Circuit cars run cruise and overrun richer, about 0.90, to pull heat out during part-throttle and braking.
- **Near 100 kPa**: about 0.90, against about 0.95 to 0.98 on a comparable piston engine.
- **Turbo WOT**: about 0.75 to 0.76 at around 200 kPa absolute on pump fuel for street use, 0.73 to 0.74 for sustained circuit load, richening further at higher boost and over the last 500 to 1000 rpm. That is about 0.02 to 0.04 lambda (4 to 5 %) richer than a comparable turbo piston engine.
- **NA WOT**: power was roughly flat from about 0.86 to 0.90 in one demonstration. The practitioner picked the rich edge (about 0.88), tapering to about 0.86 from 6000 to 8000 rpm.
- **Method**: sweep lambda at WOT, and richen until power just starts to drop, then stop. That is the rich edge of the plateau, before the power cliff.
- **Overrun**: race rotaries often skip overrun fuel cut and add fuel instead, to cool the engine. Street cars may still use cut.
- **Premix**: at typical ratios (sources cite roughly 50 to 150 ml of two-stroke oil per 20 L) premix is insignificant for injector sizing and fuelling. Its accuracy matters for lubrication. Sit on the less-oil side of the builder's range where possible, since oil lowers octane.

### Ignition
- Advance only until the torque gain begins to taper, and stop there; do not chase MBT under boost. The flat retarded side costs little.
- The ignition table is flatter with rpm than on a piston engine. Light-load timing plateaus rather than climbing. One demonstration copied the last tuned column out to the limiter without adding rpm advance.
- Isolate variables. Rotary power is very sensitive to mixture, so changing fuel and timing in the same run hides the timing effect. In one demonstration a large timing increase in boost appeared to gain top-end power, but the gain came from a rich spot being corrected at the same time.
- **Split**: power is insensitive to it. A near-standard split table is one of the few places a generic map is acceptable. Do not go below about 8 degrees under load.
- **Knock control**: several practitioners do not use it on rotaries. Calibrating it means making the engine knock, which a rotary may not survive, and detection may come after damage. They rely on conservative timing and audio monitoring instead. Do not read this as permission to remove knock protection where it is already set up; see Disputed.

### Health and diagnostics
- A rotary that starts quickly and easily is usually mechanically healthy; hard starting often points to compression or sealing problems.
- Frequent plug fouling on boosted engines is more often the tune than the plug. Heavily ported engines with lots of overlap foul more easily, worse with the very cold plugs they need.
- EGT lags lambda by a long time, so it is a slow secondary check, not a tuning signal. Per-rotor EGT can trim rotors relative to each other at WOT while one wideband after the turbine sets overall fuelling. Steady-state 3D EGT trims are hit and miss because of probe lag.
- Boost on pump fuel stays conservative. One practitioner's ceiling for a 13B on 98 RON was around 18 to 20 psi (about 125 to 140 kPa gauge) depending on turbo, with mild boost advised for a stock engine. Race fuel or water/methanol injection permits more.

## Decision rules
- Read the software's split sign convention before entering any split value.
- Check base timing on both plugs. It is the most common place for damage.
- Do not chase power with the split; keep at least about 8 degrees under load.
- Under boost, stop advancing where torque gain starts to taper; stop richening where power just starts to fall.
- Change one variable per run.
- Treat EGT as confirmation, not feedback.

## Data gates
As for piston engines, plus:
- Leading and trailing timing channels, with split, logged.
- EGT (per rotor if available), allowed to settle before reading.
- Lambda after the turbine; per-rotor widebands are rarely fitted because of exhaust temperature.
- Primary and secondary duty/pulse width and staging fraction.

## Worked example
### Cruise EGT trade
In one practitioner demonstration a street 13B at 3000 rpm and about 48 kPa absolute (about 18 % pedal) reached nearly 800 C EGT at lambda 1. Richening to about 0.90 brought it into the 770s C after a long settle. On a turbo rotary at 2500 to 3000 rpm light cruise, lambda 1 gave 790 to 830 C, and about 10 % enrichment dropped it 40 to 50 C. The economy cost of 10 % more fuel is weighed against a few tens of degrees: acceptable for a road car in true cruise, but not across all vacuum cells.

### Split sign
Leading at 10 degrees BTDC with a 15 degree split puts trailing at 10 - 15 = -5, that is 5 degrees ATDC. If the software expects the split as a negative number and +15 is entered, trailing fires at 25 degrees BTDC, ahead of leading. That is the dangerous over-advanced case.

## Disputed / conflicts
- **How rich under boost**: the practitioners run about 0.75 to 0.76 lambda at about 200 kPa absolute on a street rotary. Many tuners run 10.0 to 10.5:1 AFR on gasoline (about 0.68 to 0.71 lambda) on any turbo rotary. The practitioners say that richness costs visible power at modest boost and is unnecessary; the common practice adds margin. Test: WOT lambda sweep with EGT, picking the point where power just begins to fall.
- **Knock control on rotaries**: the practitioners do not calibrate or use it, because calibration needs induced knock and damage may precede detection. This conflicts with the general advice to use knock detection as a protection. Both agree conservative timing is the primary defence. One practitioner's view; do not remove an existing knock protection on the strength of it.
- **Trailing ahead of leading at light load**: some schools of thought claim economy gains. One practitioner has seen none and gets smoother idle and cruise with trailing behind leading. Light load is low knock risk, so it can be tested on a dyno.
- **Split effect**: practitioners find the split mainly affects emissions and smoothness, not power (runs within noise at 8 to 15 degrees). That is consistent across three demonstrations but rests on one engine family.

## Citations
- practice: Practitioner training and tuning practice, distilled and cross-checked.
