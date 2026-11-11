---
id: methodology/knock-assessment
title: Assessing knock
layer: L2
status: draft
confidence: high
sources: [practice, engineering-texts]
verified: 2026-11-11
applies_to: {fuels: [gasoline, ethanol, methanol], engines: [all]}
depends_on: [principles/combustion/knock]
supersedes: []
---

# Assessing knock

## Claim
Knock evidence comes from more than one channel and is judged by the worst plausible case. Each region of the map is either limited by knock or limited by MBT, and the two are tuned differently. An ECU knock control system is a backstop for conditions the tune did not see; it does not make a poor tune safe, and it only reacts after knock has happened.

## Why (derivation)
Sensor signals carry mechanical noise that grows with rpm and load, and thresholds are set by someone. Audio monitoring and ECU knock levels can disagree. Practitioners report, over long careers, factory and aftermarket systems that flagged knock that was not there (costs power, but safe) and, about as often, systems that stayed silent through knock clearly heard on headphones (dangerous, because the tuner keeps adding timing). So a clean signal is weak evidence and a suspicious one is strong.
Torque is not a knock detector either. Knock usually starts on one or two cylinders; the others still gain from extra advance, so the engine's total may still climb while a cylinder or two knocks. Mixture and exhaust temperature do not show it: the charge is fixed once the intake valve closes, and temperature probes are far too slow. Bare ears are late: on a quiet car, audio equipment picked up light knock about 2 to 3 degrees before it could be heard from the cabin, and on a loud modified engine it may never be heard unaided.

## Assumptions
The monitoring system has been set up and validated for this engine (`methodology/knock-sensing-setup`).

## Breaks when
- Very high rpm, noisy valvetrain, loose piston clearances or loose sensor mounting will hide or fake events.
- Very high specific output engines and rotaries with stock apex seals: a few knocking cycles can cause damage before any reactive system responds, so knock control cannot be the protection.
- Learned retard carried over from a previous session, or an adaptive octane factor still recovering after a reset, makes timing comparisons meaningless.

## Practical use
### Classify each region
- Advance towards MBT with knock monitoring running. If torque plateaus without knock, the region is MBT-limited: tune it to MBT.
- If knock arrives first, it is knock-limited: stop at the onset and leave a margin. Practitioners report that most turbo engines on pump fuel (figures of 85 to 95 % of the engines they tune) and many high-compression NA engines are knock-limited somewhere, typically at low rpm high load and around peak torque. These regions are where better fuel, cooler charge or a richer mixture pay off.
- Near a plateau at high load, one practitioner leaves a couple of degrees short when a gain of 1 to 2 Nm is all that remains on an engine near its knock limit: no driver feels it, and the margin matters.

### Read the signal
- **Real knock** shows as a large sudden jump above the threshold, usually on one or two cylinders, repeatable at the same rpm and load when the run is repeated, and it moves with timing.
- **Background** rises smoothly with rpm on all cylinders. A cylinder that sits slightly louder without sharp spikes is not a concern; one that is consistently louder in a band warrants a per-cylinder trim.
- **Mechanical noise** is the suspect when counts appear with no change of timing, always in the same high-rpm band, or persist on the same cylinder and rpm after timing or fuel there is changed. Test: pull 5 to 10 degrees in that area and repeat; if the signal stays, it is not combustion knock.
- **Artefacts**: throttle lift-off and overrun (driveline shock), the rev limiter's cut shaking the block, anti-lag exhaust combustion (sounds like heavy knock on headphones), and gear shifts.
- **Marginal single counts**: a reading just over the line with low timing, or on a high-octane fuel at modest advance, points to a threshold set too low; practitioners raise the threshold in that band (by 15 to 25 % in their examples) and keep watching. On pump fuel at high load the same reading deserves more suspicion.
- **Random violent knock** between two identical runs, with no change to the map, points to lost or miscounted engine position (trigger errors) delivering over-advanced spark. Check trigger error counters and the rpm trace before chasing timing.
- **Reactive lag**: knock began slightly before where retard first appears in the log, so remove timing starting a little earlier in rpm.
- **Factory learning**: some factory ECUs blend between high- and low-octane ignition tables with a learned factor that rises with sustained knock and decays slowly; others store learned retard per cell, applied pre-emptively next time. Log the factor and the learned values, reset or zero them before comparing changes, and let an adaptive factor recover to fully advanced before a comparison pull. A one-off correction that handles only sudden transients stays at zero on a steady ramp and is the wrong channel for judging a ramp.

### Street and road logs
Isolated, sporadic retard events on a street car on pump fuel (often the first hard pull after a long cruise) are common even on stock calibrations. Act on knock that repeats at the same rpm and load each time; chasing every one-off event leaves the whole map needlessly retarded. A retard histogram on the ignition table axes shows which cells to address. This latitude does not apply to high-boost race engines on alcohol or race fuel, where almost any knock is unacceptable.

### Is it timing or mixture?
Before pulling timing where knock retard appears, check the local mixture against what that engine should have there. If it is lean, fix fuel first; if it is on target, remove timing. Lean cylinders run hotter and knock first, so balancing cylinders before final ignition work can allow more advance.

### Margins and verification
- Leave about 2 to 3 degrees below light knock onset (the sources' common figure), more for engines that see sustained high load (circuit, land speed) or a heavy-footed owner, and slightly more where there is no effective closed-loop knock control.
- Heat soak moves the limit: holding full load for tens of seconds or several ramps can bring light knock at timing that was clean at first (one example suggests 2 to 4 degrees less after a long hold). After the main tune, run one or two much slower ramps (one example 200 to 250 rpm/s instead of 500, another 18 to 20 s from 2000 to 7000 rpm instead of 10 s). If they stay clean, the tune should hold on road or track.
- Test sensitivity to coolant: one practitioner partly blanks the radiator to raise coolant about 10 C and adds high-load retard against coolant temperature if knock appears. Tune for the temperatures seen in use, not only on the dyno.
- Intake temperature: one practitioner starts with no ignition correction up to about 40 C and pulls timing above it, then tests; the right amount depends on fuel quality and how close the engine is to its limit.

### When the fuel is the limit
If each boost increase forces timing out so that torque no longer rises, the engine has reached its limit for that fuel and combination; more boost only adds heat and stress. Practitioners place that plateau near 1.5 to 1.7 bar of boost on typical pump fuel, with exceptions both ways (larger turbos with lower back pressure and lower compression go further). On a knock-limited engine, richening by about 0.02 lambda is worth keeping if it buys 2 to 3 degrees of knock-free timing; about one degree or less means the cooler mixture is doing little. Beyond that, better fuel or lower boost are the fixes, not ever more retard (which raises exhaust temperature).

### Per-cylinder trims
Usually only one or two cylinders limit the engine: whichever runs hottest, gets most air, has poorer coolant flow or a lean injector, or sits nearest a turbo's radiant heat. Where the ECU allows, trim timing on that cylinder instead of the main table so the others run nearer MBT; global retard gives power away. Inspect per-cylinder knock trims after sessions (lengthening the re-advance delay temporarily keeps them visible).

### Transients
Tip-in and shift knock are rare in the sources (a handful of engines in many years). Confirm it is real with audio first. When it is, it is an ignition problem: use transient ignition retard with a decay, not changes to acceleration fuel. One or two occasional tip-in events are not the reliability concern that sustained high-rpm full-load knock is.

### Driver warning
Base any driver warning on the retard actually applied (one practitioner uses 2 degrees on any one cylinder), not on raw sensor level; the retard already reflects how the threshold rises with rpm. A warning at full throttle should mean: lift, and try again later.

## Decision rules
On any knock event during a run: abort, then remove 2 to 3 degrees in that region before trying again. Never answer knock by raising a threshold or disabling detection. Find the cause when knock appears suddenly at a known-good point (fuel, temperature, boost, trigger errors).

The threshold is meant to sit just above the engine's background noise at every rpm and load point, and that noise changes with both. When the background exceeds the threshold, knock control triggers falsely and the engine runs retarded for nothing. Measure the background where the engine is known not to knock, confirm with audio, and set the threshold from that (`methodology/knock-sensing-setup`). This calibration is different from raising a threshold because knock was reported: that is never done without the noise-floor evidence. Some systems also mask known noise events such as gear shifts. Validate any detection system against audio before trusting it: practitioners report both false alarms and ECUs that missed knock that could be heard. Keep the threshold just above the no-knock background (one practitioner starts about 10 % above a clean run's reading, others 20 to 30 %), and re-check it through the rev range. Mount a sensor on a flat, solid area high on the block where possible. Tune on the fuel the engine will actually run. Never hold the engine in knock to finish a run: back off first, and repeat. Knock always follows the spark; pre-ignition comes before it, and the two are different faults.

Use audio knock detection during fuel tuning too, not only ignition work: a conservative base map can still be over-advanced somewhere, and steady-state fuel work holds load for long periods. If knock is heard, lift, reduce load, pull timing in the cells in use, and only then continue. Start conservative and add timing; never start aggressive and pull timing after hearing knock. Do not rely on a torque drop or on exhaust temperature to find knock. Remote or road tuning without validated knock data is unsafe even when the mixture is on target. Automatic table smoothing can raise advance in cells beyond what was proven; on engines near their knock limit smooth by hand and re-check. When copying a tuned row into untuned higher-rpm rows, sweep it with knock detection before trusting it.

## Data gates
Knock channel present and meaningful; a defined window of crank angle; sample rate adequate for the event. Per-cylinder knock level and threshold, knock retard per cylinder, ignition timing, rpm, load, throttle and coolant and intake temperature logged together; learned knock values and any adaptive octane factor logged on factory ECUs; trigger error counters available.

## Worked example
A log shows one cylinder over the threshold during a pull. Abort, remove timing on that part of the map, repeat, and only then consider a per-cylinder approach.
A second case: after adding 4 degrees at full load on a V6, power does not change, and cylinder 2 spikes twice above its line near 5400 rpm while the rest stay below. With no torque gain the timing comes back out anyway. Had the extra timing given power, the better answer would be a cylinder 2 trim of a degree or two, leaving the others advanced.
A third case: on a ramp at 220 kPa, power rises but all cylinders get louder and knock control pulls a little timing. A general rise across cylinders means the engine is near its limit on that fuel; remove about a degree where activity appeared and seek more power from better fuel rather than more timing.

## Disputed / conflicts
- **Cross-check.** The factors that raise knock in the combustion textbook (timing, inlet temperature, coolant temperature, load, mixture near its peak) match the practitioners. The combustion textbook places the knock resonance between 3 and 10 kHz depending on bore and chamber shape, which supports choosing frequency from bore. Audio confirmation of a sensor system is practice, with no textbook test of it.
- **Torque-drop method.** A common view, said to be widespread where load-bearing dynos are standard, is that advancing to peak torque is self-protecting because torque falls when knock starts. Practitioners across several sources call this false: they have heard clear knock on pump-fuel turbo engines while torque was still rising. Discriminating test: log per-cylinder knock and torque together while advancing in steps on a knock-limited engine.
- **Is detection needed on high-octane fuel?** One practitioner argues that on E85, race fuel or methanol drag engines knock is rare and, at those outputs, so quickly fatal that audio adds little; the same practitioner insists on it for knock-limited pump-fuel work. Others note engines still knock on E85 (a 12.5:1 engine at moderate boost stayed knock-limited) and keep listening. Only testing on the engine shows it cannot be made to knock.
- **Trusting factory detection.** Practitioners find some factory systems reliable on stock or mildly modified engines (one estimates excellent agreement with audio on about 95 % of one model he tunes), while others missed audible knock on several cars. Validate per car.
- **High- and low-octane tables.** A common practice copies the high-octane ignition table into the low-octane one. One practitioner advises against it where the ECU blends adaptively towards the low-octane table, because that blend gives preventive margin against a bad tank; he does copy them where the adaptive strategy is no longer active.
- **Reducing factory knock authority.** One practitioner reduces factory maximum retard by a couple of degrees and speeds its recovery on a well-calibrated NA engine, finding factory strategies pull more than needed. This trades protection for power; it is not a reason to weaken protection on a modified or boosted engine.
- **Learned trims as a tuning tool.** One source shows long-term learned knock trim being transferred into the base table; the same series stresses that learning is reactive and needs knock to happen first. Treat learned trim as a pointer to cells to re-test with audio, not as the tune.
- **Rotaries and knock control.** Practitioners do not rely on closed-loop knock control on rotaries, since calibrating it means inducing knock and stock seals break with almost any knock; they acknowledge other tuners disagree.

## Citations
- practice: Practitioner training and tuning practice, distilled and cross-checked.
- engineering-texts: Engine, combustion, charging and control engineering texts.
