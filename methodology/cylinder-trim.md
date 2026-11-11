---
id: methodology/cylinder-trim
title: Individual cylinder trims
layer: L2
status: draft
confidence: medium
sources: [practice]
verified: 2026-11-11
applies_to: {fuels: [gasoline, ethanol, methanol], engines: [all]}
depends_on: [methodology/steady-state-fuel, methodology/wideband-sensors, principles/fueling/injector-flow-and-dead-time]
supersedes: []
---

# Individual cylinder trims

## Claim
A single collector or bank wideband reports an average, so rich and lean cylinders can cancel and the average can sit on target while one cylinder is dangerously lean. Per-cylinder (or per-bank) fuel and spark trims correct real distribution differences, but only when those differences are measured, repeatable and understood. Without per-cylinder measurement, trims are guesses and are best left at zero.

## Why (derivation)
Cylinders differ because:
- intake manifold design favours some runners and port flow varies across the head; a cylinder that gets more air runs leaner on equal fuel;
- fuel delivery differs: injector flow spread (used, cleaned factory injectors 5 to 10 or more years old can differ by 5 % or more; new modern injectors are rarely a concern), and a rail near its flow limit can feed the first injector more than the last as pressure falls along it;
- unequal runners or trumpet lengths, unbalanced individual throttle blades (a blade cracked open more feeds that cylinder more air), production tolerances, wear;
- some cylinders are more knock prone by design or cooling.

Fuel trims scale the common calculated fuel for one cylinder (the effective pulse, before dead time is added); spark trims shift that cylinder's timing in degrees. The goal is equal combustion and cylinder pressure, or each cylinder taken to its own limit.

Imbalance usually changes with rpm, load, airflow and pulse width. One production engine showed about a 9 to 10 % lambda spread at idle, about 1 % at 2500 rpm steady, and 5 to 10 % at other points. A trim taken from idle (about -13.5 % on one cylinder) made that cylinder 11 to 12 % lean at 2500 rpm, where the idle imbalance had gone.

## Assumptions
Sequential or semi-sequential fuel (cam sync and one injector driver per cylinder) for fuel trims; direct-fire coils for fully independent spark trims (wasted spark trims only the pair sharing a coil; a distributor allows none). Batch-fire and single-point throttle-body injection cannot target one cylinder. Main fuel table tuned to target on the trusted collector sensor first.

## Breaks when
- Absolute readings from different sensors or positions disagree: runner sensors averaged about 0.98 while the collector read 1.08 in one test. Only relative differences between runners are trustworthy.
- Exhaust temperature (EGT) is not purely a function of mixture: probe lag, probe position, run-to-run variation, combustion efficiency, coolant flow around the head and especially ignition timing all move it. Cylinders 1 % apart in lambda showed equal EGT; three cylinders matched in lambda showed one about 15 C hotter.
- EGT probes are mounted at different depths or distances from the flange, which alone produces large differences.
- Early-run drag data: pre-stage, launch and first-gear spreads (35 to 50 C, or 350 to 452 C at part throttle in vacuum) reflect lag and non-equilibrium, and converge from the top of second gear.
- A deviation that is not repeatable run to run, or appears in only one rpm band on one cylinder, is a fault (mechanical, ignition, injector), not a calibration.

## Practical use

### When it is worth it
- Most road and mild race engines tune well on a single collector sensor, especially with the slightly rich full-load margin many tuners keep for this reason. Without per-cylinder data, run somewhat richer at high load to protect any lean cylinder.
- Per-cylinder data becomes valuable as specific output rises and margins shrink, and it is close to essential on methanol and high-boost drag engines, where one lean cylinder can hole a piston and the lean side is the destructive side. One practitioner will not tune such engines without per-cylinder EGT.
- Balancing rarely adds power directly, since power is flat over a wide mixture window. Its main value is safety; the power gain comes on knock-limited engines, where richening a hot, knock prone cylinder lets it take more timing.

### Instruments
- Per-cylinder lambda is more accurate and faster than EGT; use it for 3D trim tables. Do overall fuel tuning on the collector sensor and use runner sensors only to balance cylinders relative to each other.
- EGT is slow and imprecise; use it to set one fixed trim per cylinder, which suits engines that live at full load over a narrow rpm band (drag cars often only 1000 to 2500 rpm wide). Mount every probe identically (same distance from the flange, about 50 mm in one demonstration, and same depth, ideally near runner centre).
- A sensor per bank allows bank trims on V engines: allocate all cylinders of a bank to one trim.
- Plug colour across cylinders (on gasoline, lighter means leaner, darker richer) hints at distribution but has no rpm or load context and barely works on methanol.

### Procedure
1. Get collector or bank lambda on target with the main table.
2. Check repeatability: run the same test several times. Healthy cylinders repeat within about 1 %. Trim only cylinders that read consistently.
3. Choose the trim form: a single value per cylinder only for a cylinder that is consistently off by a similar amount everywhere, or for EGT-based balancing; otherwise per-cylinder rpm by load tables with coarse breakpoints (about every 1000 rpm and 50 kPa in one session) and the same load axis as the main table.
4. Concentrate on high load and full load, where a lean cylinder can destroy an engine; drift at idle and cruise mainly costs economy.
5. At each operating point, remove fuel from the rich cylinder and add to the lean one, then recheck. When several cylinders cluster with one or two outliers, match the outliers to the cluster. Sources prefer adding fuel to the lean cylinder or bank over leaning the rich one, while leaning one that is clearly rich and cold.
6. On a V engine with one sensor per bank, one approach trims only the leaner bank (always adding fuel) and leaves the other at zero, correcting the main table to the reference bank.
7. With staged injection, trim primaries and secondaries separately so cylinders stay matched through the transition.
8. Spark trims: retard only the knock prone cylinder, or advance the cylinders that tolerate more; factory calibrations on some engines do exactly this.

### Diagnostic tests
- **Fault or calibration?** A cylinder whose lambda trace differs every run (one case: about 10 % rich above 3500 rpm, non-repeatable while others repeated within about 1 %), or that shows up as noise on the collector at high rpm, points to a mechanical or ignition fault on that cylinder.
- **Misfiring cylinder.** Even a couple of misfire events show as a drop in that cylinder's EGT, because unburnt charge cools the probe.
- **Choppy bank trace.** One bank's lambda much choppier than the other's: check for an exhaust leak (one case: a pinhole crack in a header) upstream of that sensor.
- **Individual throttles.** Audible misses or pops at idle and light throttle while average lambda looks fine: balance the throttle blades with a flow gauge in each trumpet before tuning.
- **Rail feed bias.** On inline engines with an end-fed rail and return at the other end, cylinders near the feed may run richer and far ones leaner.
- **Single injector fault.** One of several injectors on a methanol cylinder operating erratically melted that piston; an injector misbehaving shows first in that cylinder's EGT or lambda.

## Decision rules
- Leave trims at zero (disabled) when there is no way to measure per-cylinder fuelling, except small pre-emptive enrichment of a cylinder known by experience to fail first on that engine family.
- Spreads in the sources: most engines within about 5 % richest to leanest; up to about 10 % not unusual even with healthy engines (also typical trim spread on high-power drag engines); beyond about 10 to 15 %, look for a mechanical or injector fault rather than tune around it.
- Tolerances the sources aim for: cylinders within about 1 to 2 % in lambda; banks within about 2 to 3 %; EGTs within about 10 to 20 C under load, without chasing a one or two degree match. EGT balancing at idle is not meaningful.
- Base trims on settled data (later gears, stabilised ramps), not on transients.

## Worked example
A V6 with one wideband per bank differed by a few percent, mostly near closed throttle. One practitioner applied the same trim to one bank's three cylinders: -4 % at 1000 rpm, -2 % at 2000 rpm, zero above, and +1 % at full load, which brought both banks nearly equal. On another V6 the leaner bank needed up to about 16 % at 3250 rpm full load. Single-value trims from EGT: adding 5 % to a hot cylinder and removing 5 % from a cold one brought the spread to 10 C (676 vs 666 C), but because the cold cylinder was rich only above about 3500 rpm, the fixed trim made it 10 to 15 C hot lower down: a single trim is a compromise when the imbalance depends on rpm.

## Disputed / conflicts
- **Single trims vs tables.** One course recommends a fixed trim per cylinder for most cases and tables only when imbalance changes across the map; other sessions show imbalance changing with operating point on most engines and recommend tables whenever per-cylinder lambda is available. Both agree single values suit EGT feedback and narrow-band engines.
- **Add or remove fuel.** Several sources prefer adding fuel to lean cylinders; others remove from rich and add to lean together. Adding is the safer default when unsure which sensor is right.
- **Collector adequacy.** One practitioner's decades of V6 and V8 tunes on a collector sensor show it is usually enough; per-cylinder tests show 5 to 10 % spreads are common. Both hold: the spread exists, but matters mainly near the limit.

## Citations
- practice: Practitioner training and tuning practice, distilled and cross-checked.
