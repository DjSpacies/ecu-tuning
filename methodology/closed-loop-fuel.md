---
id: methodology/closed-loop-fuel
title: Closed-loop fuel control
layer: L2
status: draft
confidence: high
sources: [practice, engineering-texts]
verified: 2026-11-11
applies_to: {fuels: [gasoline, ethanol, methanol], engines: [all]}
depends_on: [principles/control/feedback-and-pid, principles/data/sensor-lag-and-delay, methodology/wideband-sensors]
supersedes: []
---

# Closed-loop fuel control

## Claim
Closed loop trims the small residual errors left after the open-loop map is right: weather, intake temperature, heat soak, fuel blend and ageing parts. It is not a substitute for tuning the base table. While it is active, measured lambda on target proves nothing about the base table. The trim, combined with any remaining lambda error, is the measure of the base-table error. Lockouts, update timing, gain and authority limits decide whether the loop is stable, and how far a bad sensor can move the fuel.

## Why (derivation)
- **Reactive, with dead time.** The controller sees a fuel change only after the transport and sensor delay (principles/data/sensor-lag-and-delay). That delay is long at low exhaust mass flow and short at high flow. If the ECU updates faster than the delay, it adds fuel again before the last correction has arrived, then overshoots and reverses. This is the classic dead-time oscillation of a PI loop (principles/control/feedback-and-pid).
- **Trims carry across cells.** Trim built in one cell stays applied as the engine moves into the next cell. If a rich cell sits next to a lean one, the negative trim from the rich cell makes the lean cell leaner than it would be with no closed loop at all. A uniform error of a few percent suits closed loop. Cell-to-cell scatter does not, and it shows up as hesitation or lean stumble.
- **Measured lambda is already corrected.** With the loop active, the logged lambda includes the trim. The base-table error is therefore the lambda error combined with the trim. For multiplicative corrections: base error factor ≈ (measured/target) x (1 + trim). If a long-term or learned trim is also active, include that too.
- **Why it is worth running on a tuned car.** A speed-density table only estimates airflow, and temperature and baro compensation are imperfect. Sources describe:
  - cruise wandering from 14.7 to 14.2 AFR on different days with the same pulse width;
  - an 8 to 10 % fuel difference between ethanol-free fuel and E10;
  - a stock late-model car briefly adding about 15 % on a hot restart. If an OEM model cannot cover heat soak, a generic aftermarket model will not either.
- **Why authority must be bounded.** If the sensor misreads, trim moves fuel the wrong way. The worst case is a sensor reading falsely rich at high load, which leans the engine. Large constant trims also leave little margin, and they hide map errors from the tuner.

## Assumptions
- A healthy, warm wideband whose signal path is known to be valid (methodology/wideband-sensors), with each sensor assigned to the bank it is physically in.
- A base map already close to target, so trims are small.
- Enrichments that are meant to persist are delivered through the lambda target, not through fuel adders the loop will remove.

## Breaks when
- **Overrun fuel cut.** The sensor reads full lean, the loop winds up to its limit (10 to 20 % in one example) and dumps that fuel at tip-in. The result is a rich hit, then a lean swing and hunting. On recovery the wall film is still rebuilding, so a real brief lean appears, and a loop that chases it overshoots rich afterwards. OEM ECUs block this; many standalones need it configured.
- **Transients.** During tip-in the airflow burst and acceleration enrichment change faster than the sensor reports. A loop left active treats the deliberate enrichment as rich error and the two controllers fight.
- **Cuts and shifts.** Ignition and fuel cuts from limiters, launch and shifts give false lean readings.
- **Warm-up, post-start, hot restart.** Trims learned here do the compensation tables' job and contaminate any learned table. Enrichment still active while trims are read makes the trims look like a base error that reverses once the enrichment decays.
- **Saturated trim.** A trim pinned at its limit understates the error. Sources show trim at +20 % with lambda still about 1.2 against 1.0, and at -15 % with 0.80 against a 0.90 target after a cam change.
- **Wrong bank assignment.** On a dual-bank V engine, each bank is corrected by the other bank's sensor. One trim heads to its rich limit, the other to its lean limit, both banks' lambda wander and the engine runs badly.
- **Fuel adders the loop does not know about.** Coolant overheat enrichment, a cold-engine fuel adder, a nitrous fuel overlay, or methanol in a water-methanol mix, all with an unchanged lambda target. The loop strips the added fuel out.
- **A long-term trim learned at cruise and still applied at WOT.** Some OEM strategies keep it. A learned -5 % can make full load run lean. Poorly scaled modified cars commonly show 10 to 15 % long-term trims that learn slowly, so a dyno-perfect WOT can drift by 10 % or more weeks later.
- **Faults on paths with no diagnostics.** An analog wideband in warm-up or failure gives a fixed or railed value that the ECU cannot recognise as invalid.

## Practical use

### Reading trim as base-table error
- Always read trim and measured lambda together. These are among the most common findings in the sources:
  - lambda on target with a trim of -20 % at first start;
  - a closed-loop multiplier of 0.8 with lambda looking right;
  - +7 % added at WOT while dyno lambda tracked 0.82 exactly;
  - trims around +6 % almost everywhere on a car that looked tuned.
- **Sign.** Negative trim means the loop is removing fuel, so the VE cell is too high: the ECU thinks more air is entering than really is. Positive trim means the cell is too low. Move the cell in the direction of the trim.
- **Combine.** Total error = lambda error + trim (in percent, for small values). Examples from the sources:
  - +2 % trim with lambda 3 % lean needs about +5 %;
  - +3 % trim with lambda 2 % rich needs only about +1 %;
  - lambda 0.98 on a 0.92 target while the trim pulls 4.4 % is really about 0.94.
  Where lambda is on target, apply the trim as it stands. Where lambda is still off even with trim applied, go beyond the trim in the direction lambda shows: for example 8 % where 6 % was shown, or 1.4x where the trim was pinned at +20 % and lambda was still well lean. Where actual is already richer than target, apply less than the trim.
- **Sum all layers.** Short-term + long-term or learn trims together give the total. Reading the short-term trim alone while learning is active gives a false picture: zero short-term trim only means the learned table has absorbed the error. Build a math channel for the combined error. Some log histogram tools compare only measured with target lambda and ignore the trim that was applied, so they understate the error.
- **Lag attribution.** Trim lags its cause. During a 500 rpm/s ramp, one example took about 200 rpm to settle. If lambda was lean at 4100 rpm and the trim peaked at 4250 rpm while lambda had already swung rich, the error belongs to the 4000 rpm column. In a WOT log, a lean reading at 3600 rpm with 4 % still being removed came from trim carried over from an earlier rich region: about 3 % lean with 4 % removed means that cell is about right. Fix the earlier cells, not the one that looks lean.
- **Ignore transitional samples.** Ignore trim where it is still settling at the start of a pull, at closed throttle (normally overrun cut), and straight after a hot restart or idling without the fan. One example started a run with +11 % of heat-soak trim. Positive trim at the start of a pull points to tip-in or acceleration enrichment, not VE.
- **Read trim after a change.** After an edit the old trim double-counts until it unwinds, so expect a brief swing the other way. When a large trim (around 20 %) is being removed, take fuel out in steps of 3 to 10 % and let the trim settle between them. Removing it all at once can stall or lean the engine.
- **Trim drops to zero.** If trim falls to zero partway through a pull, the loop has disabled. From that point estimate error from measured against target lambda, and find out why it dropped out: coolant, rpm, MAP or TPS windows, rate-of-change lockouts, or a failing input. One car had a failing TPS.

### Lockouts and enable conditions
- **Start delay.** Long enough for the fitted controller's heater: about 30 s for one external controller, and sooner for some ECU-internal controllers. A digital link with a ready flag makes this automatic.
- **Coolant lockout.** Set it so the loop does not fight warm-up enrichment, unless warm-up targets are set in the lambda target table (see Disputed).
- **Rate-of-change lockouts** on throttle and MAP, plus a freeze while acceleration enrichment is active. One example used 10 % or 10 kPa per 100 ms.
- **Post-event hold.** A hold after overrun fuel cut and after any ignition or fuel cut. Examples: about 1.5 s after overrun recovery; about 100 ms after a sequential shift cut, as a starting value checked in logs. One practitioner temporarily lengthened the post-transient freeze from 0.15 to 0.4 s while gathering road data, then restored it. Some ECUs label this hold as a delay versus rpm; it is not a transport-delay setting.
- **Rpm, MAP and TPS windows.** If closed loop is limited to idle and cruise, one example used rpm from just below idle to 3500 to 4000 rpm and MAP up to about 70 kPa. One practitioner disabled the loop above 60 to 70 % TPS.
- **Learned trims.** Freeze them during post-start, warm-up and coolant correction, and below normal operating temperature (60 C in one example).

### Update rate or period, and gain
- Make the update interval follow exhaust mass flow or rpm: slow at idle, fast at high load. Figures in the sources:
  - idle: 2 to 3 updates per second is typical, and one ECU was stable with a 2.5 s period at about 2 g/s exhaust flow;
  - high load: 150 to 200 ms at about 260 g/s;
  - one rpm-based delay table ran from about 1000 ms at idle to 50 ms by 5000 rpm;
  - with fast modern elements, one practitioner found rates above about 10 Hz made control worse.
  Check the ECU's units and table direction; one calibration shown had the table inverted.
- **Measure the delay.** With closed loop off, step fuel by about 10 % at idle and time the lambda response in a log. In one example the response took about a second and reached only 0.94 to 0.95 rather than the expected 0.90 within that time.
- **Gain bracketing.** Start low, double the gain each test until lambda starts to oscillate, then halve it. Several practitioners use this method, and it is the same one used for boost PID. Give more gain at larger errors, and little or none near zero error. Do not trust default gains; on two engines the defaults controlled poorly. The best values depend on how far the sensor is from the ports.
- **Gain as fraction corrected per update.** Correcting 100 % of the error each update tends to oscillate. Values of 50 to 80 % worked in two examples.
- **PID.** One engine worked best with low P, relatively high I and very little D. Clamp the integral (5 to 10 % was enough with a good table) to avoid windup.

### Authority by region
- Size limits by how much legitimate model error each region sees. Idle gets the most because of heat soak and hot restarts, cruise gets moderate authority, and high load or boost gets the least, because a misreading sensor there is the most dangerous.
- Typical finished-map figures across many sources:
  - idle: 10 to 25 %;
  - cruise: 10 to 15 %;
  - WOT or boost: about 5 %. Some sources use 2 to 3 %, and one uses 3 to 5 % on methanol at very high load.
  Setting both limits to zero disables the loop in a region.
- Where the ECU has one global limit there is a conflict: hot restart may need up to about 15 % for a minute or two, while high load wants about 5 %. Compromise, or restrict the active region instead.
- If the ECU declares a fault when trim sits at its limit for a set time (60 s in one example), tight limits can drop closed loop during a hot restart, just when it is needed.
- Wide authority (up to the 100 % or more that some self-learning systems ship with) is a roughing-in tool. Narrow it before the car leaves the dyno.

### Long-term trims and learning
- Long-term or learn tables absorb the persistent part of short-term trim, cell by cell or in broad zones. Per-cell learning works better than the few broad OEM zones, because one zone value can be rich at one end and lean at the other.
- Use learned values as a report card for transferring into the base table, not as a permanent fix. Before transferring:
  - inspect the table, and reject outliers and sign flips. Neighbouring cells at -10 and -35 is a red flag;
  - distrust values extrapolated into cells the engine never visited. One table showed populated cells above the ambient MAP of an NA engine;
  - hand-fill unvisited areas from the trend;
  - scale the transfer: about 0.75 when trims are small, about half when they are around 20 %;
  - expect two to three iterations.
- Some ECUs, after a dual-bank transfer, write the bank average into the base table and leave each bank holding half the difference.
- A rich bias on learning (0 to 10 % available on one ECU, with 2 to 5 % suggested) makes the learned table run richer than target, so short-term trim sits removing fuel. It is a deliberate safety margin against wideband faults.
- Reset learned trims after calibration changes, so old learning does not mask the result.

### Delivering enrichment under closed loop
- Put cold-engine richness, overheat protection richness and power-adder enrichment into the lambda target as well as the fuel adder. Examples: target about 0.95 at idle and cruise until around 50 C; a target overlay of 0.90 to 0.80 keyed on the nitrous input.
- In a model-based fuel strategy (fuel mass = air mass / target AFR), changing the target also changes the open-loop pulse width directly. This works only if the main table is accurate.
- With an unmodelled enrichment such as methanol in a water-methanol mix, the size of the trim (one example went from about -2 % to -12 to -14 % at high rpm) is a useful check that the methanol is flowing. A switched fuel trim is still the proper fix.

### Narrowband and stoichiometric modes
- With a narrowband, closed loop can only hold lambda 1 by dithering rich and lean. That is what the catalyst needs, and it suits idle and cruise only. Stoichiometric modes ignore the target table.
- A wideband mode that chases the target table directly, with error-based gain and rpm-based rate, is the one to use across the range.
- Factory narrowband trims cannot calibrate power enrichment, and they drop to zero once the ECU enters open-loop enrichment (about 95 kPa in one example). Note where that transition happens and keep trim-based calibration below it.

### Using closed loop as a tuning aid
- Wide temporary authority holds the engine near target as untuned cells are entered. Fold the trim into the cell (by hand, or with a one-key transfer some ECUs provide), let it settle and revisit. Set the target table first, because closed loop, learning and the tune itself all aim at it.
- With the fuel model (injector data, pressure) validated, the trim at WOT exposes airflow-model error alone.
- During ignition and injection-timing sweeps, closed loop holds lambda constant so torque changes come from timing. In injection-timing tests, a trim moving more negative indicates fuel that the engine is using more effectively.
- Alternatively, disable closed loop, or clamp its limits to zero so the configuration stays intact, while gathering calibration logs, and use measured/target lambda directly. Above all, know which mode you are in.

## Decision rules
- Tune the base table with closed loop out of the picture, or with its trim folded into every correction. Never judge the table on lambda alone while trims are active.
- Finished map:
  - short-term trims sit within about 1 to 3 %;
  - consistent trims beyond about 5 % (beyond about 10 % in one source) mean the base map needs work;
  - zero everywhere is unrealistic, so stop chasing 1 % differences on the dyno.
- Persistent trims are base-map errors. Fix the table and let the trim return near zero.
- Lockouts: cold start until the sensor is ready; transients and acceleration enrichment; overrun cut and its recovery; any cut. Learning is also locked out until fully warm.
- Authority: most at idle, least at high load. Narrow it once the base map is right. With an analog wideband, or any path without fault reporting, keep high-load authority small or disable closed loop there.
- Oscillation: before changing anything, decide whether it comes from gain, from period, or from alternating rich and lean VE cells (see Practical use).
- Verify sensor-to-bank assignment before enabling dual-bank control.
- Disable or tightly bound long-term learning once the tune is done, as a preference. Never leave learning free to drift WOT fuelling.

## Data gates
- Lambda valid: heater ready, no fault flag, no cut or misfire.
- Lockout and closed-loop status channels logged.
- Speed-load state away from transients, with no acceleration enrichment, overrun or post-start active.
- Coolant at operating temperature for any sample used to change the base table.
- Trim not saturated, or the saturation flagged.

## Worked example
A WOT log with closed loop active shows the following.
- At 4000 rpm: lambda 0.80 against a 0.82 target, so 2.4 % rich. Trim is +1 %, still lagging from the previous cell. Base factor = (0.80/0.82) x 1.01 = 0.985, so remove about 1.5 % from the 4000 rpm cells.
- At 4500 rpm: lambda 0.82 on target with trim at -5 %. Base factor = 1.00 x 0.95, so remove about 5 %.
- At 5000 rpm: lambda 0.86 against 0.82 (4.9 % lean) with trim -4 % still unwinding from 4500. Base factor = (0.86/0.82) x 0.96 = 1.007, so leave the cell alone and rerun after fixing 4500.
- Separately, a cruise cell shows a persistent +7 % trim with lambda on target. The base map is lean there by about 7 %. Fix the cell and the trim returns near zero.

## Disputed / conflicts
- **Closed loop at WOT and in boost.** Older practice, including two practitioners' own earlier habit, limited closed loop to idle and cruise, because analog widebands could fail silently. The same practitioners now run it across the whole map, including boost on track cars, because digital controllers report warm-up and faults and the ECU can disable correction. They still keep high-load authority small. A third practitioner still prefers to rely on a correct map and verify by logging. All agree it should be conditional on fault reporting.
- **Coolant lockout.** An engine-management textbook states closed-loop lambda stays off until the sensor reaches operating temperature, and this supports a cold lockout. Several practitioners argue that modern fast-heating controllers that report readiness make a warm-up lockout largely unnecessary for short-term trims, provided warm-up lambda targets are set. Learning should still wait for full temperature. One practitioner lowers the coolant enable for a first start (from about 160 F to 100 F) so trims can rescue a poor base map, then restores it.
- **Long-term learning.** Some practitioners leave it on, and one notes that others do too. Several disable it once the tune is complete, or bound it to about 5 to 10 %, so WOT fuelling is exactly as programmed. This is preference. The common ground is that learning must never act during warm-up or transients.
- **Tuning with closed loop on or off.** One camp disables it so the wideband shows the true error, and treats the narrowband trims of factory systems as hunting, reactive and useless in power enrichment. The other camp tunes with it on as a safety net and folds the trim into every edit. An objection common online is that aged factory sensors make trims meaningless. One practitioner considers that largely irrelevant, because the same sensors define the target once closed loop is re-enabled. Both camps agree that ignoring the trim is the error.
- **Authority figures.** Finished-map WOT limits range from about 2 to 3 % up to 5 %, and idle limits from about 10 % to 25 %. These are practitioners' choices, not limits from any textbook. Factory systems often allow about 25 % short-term and long-term each. Practitioners read a need for that much on an aftermarket map as a fault.
- **Final residual bias.** One practitioner prefers to finish with the trim slightly removing fuel, so the base is a touch rich and the safer error remains if closed loop is off. This is one practitioner's view.
- **Self-learning from a flat table.** A manufacturer reported a car becoming essentially tuned from a flat table after a long drive. The practitioner reporting it stresses that this does not replace tuning. One course example found two self-learn ramp runs did roughly what six or seven manual runs had done. Both are anecdotes.
- **Control theory.** A feedback-control textbook supports the dead-time and gain reasoning. The specific rate, period and gain numbers are platform and installation dependent.

## Citations
- practice: Practitioner training and tuning practice, distilled and cross-checked.
- engineering-texts: Engine, combustion, charging and control engineering texts.
