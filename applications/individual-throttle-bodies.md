---
id: applications/individual-throttle-bodies
title: Individual throttle body profile
layer: L4
status: draft
confidence: low
sources: [practice]
verified: 2026-11-11
applies_to: {fuels: [gasoline, ethanol, methanol], engines: [itb]}
depends_on: [principles/airflow/volumetric-efficiency]
supersedes: []
---

# Individual throttle body profile

## Claim
With individual throttle bodies there is little manifold vacuum signal, so a pressure-based load is unstable and throttle position is the usual load. Every table whose output changes airflow (fuel, cam targets, cam switch) should then share that throttle axis. Throttle airflow is very non-linear, so throttle breakpoints are spaced unevenly. Injector position, and on some high-revving engines throttle opening itself, become tuning variables.

## Why (derivation)
- Without a shared plenum, pressure at low load carries strong per-cylinder pulses and changes little with load, so it is a poor load signal.
- Airflow against butterfly angle rises far faster in the first part of travel; beyond roughly 70 to 80 % opening little more is gained. With several butterflies in parallel the effective area is large, so the early jump is magnified further.
- Cam position changes VE. If cam targets or a cam-switch window used a different load variable from the fuel table, one fuel cell would see different cam states and could not be tuned consistently.
- Injectors are often far from the valve (in the trumpets, above the butterflies). That means longer transport, more port wall wetting at low air speed, and better mixing and charge cooling at high rpm.

## Assumptions
No shared plenum, or a balance tube too small to give a usable pressure signal.

## Breaks when
- Combining individual throttles with forced induction needs a more complex fuel model (throttle for fuel at low load, pressure for boost), and is for experienced tuners.
- A small balance plenum with a stable pressure signal may allow a blended or pressure-based load at higher loads.
- Drive-by-wire on multiple throttle bodies multiplies sensor and driver I/O: each throttle needs two position tracks and an H-bridge output.

## Practical use
- **Load axis**: choose throttle position for fuel. Where both throttle and pressure are meaningful (boost), keep manifold pressure for ignition (one training session).
- **Throttle sites**: put more sites in the first part of travel than above half throttle (an practitioner example uses 0, 10, 40, 60, 80, 100 % after re-axising imported tables; finer sites near closed throttle are common).
- **Imported maps**: tables built for a pressure axis must be re-axised to throttle before use. Paired tables (low and high cam, or cam target and fuel) should share identical axes.
- **Cam tables**: cam target and cam-switch tables use the same throttle axis as fuel on an ITB engine.
- **Injector placement**: near-valve injectors suit low speed. Upstream or above-trumpet injectors help high-rpm WOT mixing but hurt idle, cold start and low-speed control; one methanol example ran well at WOT and badly at idle and cold start. Developed NA race engines stage the upstream set in only at high rpm, which gave a small but worthwhile gain in one example. ITB engines with trumpet-mounted injectors also respond more to injection timing than typical port engines (methodology/injection-timing).
- **Throttle limiting at low rpm**: on some very high-revving ITB engines (bike-derived, around 12000 to 14000 rpm), peak torque at low rpm came at well under full throttle. One example peaked at about 35 % throttle at 2000 rpm, and full opening was not useful until about 4500 to 5000 rpm. On drive-by-wire, test reduced maximum opening at low rpm on the dyno and cap it with a maximum-throttle table. The practitioner attributes it to air velocity effects but does not claim a mechanism.
- **Filtration**: always filter the intake, even though a restrictive ITB filter can cost power (one owner was tempted by about 20 whp). Debris ingested by an unfiltered ITB engine can hold a valve open and wreck the engine.
- **Drive-by-wire**: modern electronic throttles on ITB engines are accurate and repeatable; the poor reputation dates from early factory systems (methodology/etc-throttle).

## Worked example
For a 4-cylinder ITB engine, fuel throttle sites at 0, 2, 4, 6, 8, 10, 15, 20, 30, 40, 60, 80 and 100 %. Seven of the thirteen sites sit below 15 %, where airflow changes fastest. If a cam target table imported on a pressure axis is left on that axis, a cell at 30 % throttle and 2500 rpm can see the cam move with small, noisy changes in measured pressure. Re-axising it to the same throttle sites removes that inconsistency.

## Disputed / conflicts
- **Low-rpm throttle limiting**: one practitioner reports a torque gain from less than full throttle at low rpm on high-revving ITB engines, but offers no confirmed mechanism. Treat it as a test to run, not a rule.
- **Filter loss against protection**: removing a filter can gain power, but the sources rank engine protection above it. Keep the filter.

## Citations
- practice: Practitioner training and tuning practice, distilled and cross-checked.
