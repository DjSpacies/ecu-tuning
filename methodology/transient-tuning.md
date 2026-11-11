---
id: methodology/transient-tuning
title: Transient fuel tuning
layer: L2
status: draft
confidence: high
sources: [practice, engineering-texts]
verified: 2026-11-11
applies_to: {fuels: [gasoline, ethanol, methanol], engines: [all]}
depends_on: [principles/fueling/transient-fuel-film, methodology/steady-state-fuel]
supersedes: []
---

# Transient fuel tuning

## Claim
Tune transient enrichment only after steady-state fuelling is right along every path the transient takes, then test real, repeatable throttle events and judge both quantity and decay. The judge is engine response (crisp, no hesitation, no bog); the lambda trace is a guide that tells you which side of right you are on, not a target to flatten.

## Why (derivation)
The wall film and the lag of the ECU's airflow estimate are transient effects (`principles/fueling/transient-fuel-film`). Enrichment is an adder or multiplier on the main pulse width, so any steady-state error in the cells a transient passes through is inherited and gets mis-attributed: enrichment over-compensates where the base table is lean and becomes excessive where it is right. Practitioners name tuning enrichment over an inaccurate base table as the most common transient mistake.

A wideband lags fast events (transport and response delay, worst at idle where exhaust flow is low), and cycle-to-cycle variation means a perfectly flat lambda through a transient is not achievable. Chasing the initial lean blip to zero adds far too much fuel, and too much fuel feels much like too little: both give a dull, doughy or hesitant response.

## Assumptions
Port injection; steady-state fuel within a few percent (one practitioner asks for 1 to 2 %) in the test region; engine at operating temperature; a throttle sensor that is clean and correctly spanned; a load signal (manifold pressure or air mass) that responds quickly.

## Breaks when
- Sensor lag shows a false lean spike, or a slow manifold pressure signal (moist or faulty sensor, long or kinked hose to a remote sensor) makes the ECU fuel for the wrong pressure during the event.
- A noisy throttle sensor triggers enrichment at steady throttle.
- Cold transients need separate treatment and cannot be judged on a warm engine.
- Free revs in neutral and dyno events lack the load and inertia of driving; results need confirming on the road.
- Direct or dual injection changes the scale of the film effect.

## Practical use

### Before starting
1. Tune the steady-state table first, including cells a stab passes through (for example from cruise vacuum through the brief low-boost region before a turbo spools) and ignition there.
2. Check the load signal: from idle, stab the throttle and log manifold pressure against throttle; pressure should reach near atmospheric almost immediately. Fix a lagging sensor or hose instead of tuning around it.
3. Check for spurious enrichment: at steady throttle, log the applied enrichment channel. If it moves, raise the throttle-rate deadband and fix the sensor or wiring.
4. Turn closed-loop correction off and use a single fixed lambda target across the test region, so you are not chasing a moving target.
5. Start from the ECU's default shape if the calibration is unknown, resetting edited values. Defaults are often close when the main map is right; needing wholesale changes is a warning that something else is wrong.

### Running the tests
- Repeat each event from about the same starting load (manifold pressure) to the same end, at stabilised air and coolant temperatures, in a steady gear (second or third on the road; a fixed gear on the dyno).
- One useful baseline: zero the enrichment and stab once, to see and feel the uncompensated lean spike. In the sources this ran from about lambda 0.99 to 1.12 from light load, to about 1.3 from idle, and in AFR terms from 14.7 to about 26.5 from idle.
- Log three graded events (small, medium, large throttle rate) and review throttle rate, enrichment added, total pulse width and lambda for each before changing anything. Use log playback to see exactly which cells were active.
- Work rpm zone by rpm zone: idle blips first (easy, no driving needed, but judge them by sound and feel since the lambda reading there is nearly useless), then hold each higher rpm steady and stab. Start with the largest, sharpest change, then smaller ones. Tune part-throttle (small rate) cells separately.
- Make large changes while testing (for example 50 % steps, or halve and double a time constant): 2 to 3 % changes are lost in test-to-test noise. Bracket first, then refine. Revert a change that made no net improvement, especially if response was already crisp.
- Confirm on the road. A chassis dyno dulls the feel of hesitation because the engine has little inertia to move.

### Reading the result
- **Hesitation with a lean spike:** more enrichment.
- **Bog with a rich reading:** less enrichment.
- **Good initial hit, then drifts lean before steady-state fuelling takes over:** enrichment is removed too early; extend hold (one practitioner goes from about 2 to 3 or 4 injection events) or slow the decay (halve the decay rate). With a film model, the evaporation time constant is too short.
- **Rich dip after a clean hit:** reduce the amount or speed the decay, accepting the later lean drift may worsen slightly. With a film model, stays rich too long means the time constant is too long; overall rich or lean on the event means the film percentage is too high or too low.
- **A brief small lean blip at the instant of tip-in, then rich:** normal on nearly every engine; adding fuel to remove it only deepens the rich overshoot. One practitioner works harder only if the initial spike exceeds about 10 % lean or goes past lambda 1, judged together with feel. Crisp engines typically show a short lean spike then a slight rich dip before settling.
- **Feel cannot separate too lean from too rich**, because both feel doughy. Use the lambda trace to tell which side you are on; one practitioner starts from zero to learn the lean feel, then adds until it goes doughy, and settles on the least enrichment that is crisp. Of a range of settings that feel the same, choose the low side for economy.
- **Isolated rich or lean spots in steady-state logs that coincide with a tip-in or tip-out** are transient, not VE errors. Do not correct the main table for them; ignore data until the reading settles after a stab, and treat a brief error at the start of a full-load run as enrichment.

### Shaping the compensation
- By rpm: most at low rpm where air speed is low; falling to little or none above about 4500 to 5000 rpm in most sources (one example clamp: 30 % at 0 rpm falling to 0 % from 5000 rpm).
- By starting load: most from near-closed throttle; much less from 70 to 80 kPa or 70 to 80 % throttle (one example load correction: 1.0 at 0 to 20 kPa tapering to about 0.3 at 80 kPa). On turbo engines, or engines with a wide vacuum range, manifold pressure is a good axis for this scaling even when throttle rate triggers it.
- By coolant temperature: tune fully warm first, then cool the engine and adjust the cold correction last, after warm map, cold start and warm transients, since they interact. Cold multipliers in the sources range from about 2 to over 4 times the warm amount near 0 to 20 C, blending to 1.0 by about 40 C or by operating temperature.
- By throttle rate: more enrichment for faster stabs. Some ECUs split amount (against rpm and starting throttle) from rate (against throttle delta); tune amount with the sharpest stabs so the rate scaling sits at 100 %, then trim the rate scaling down for gentle movements.
- Deadband: high enough that sensor noise and cruise corrections do not fire it, low enough that gentle tip-ins are caught (a too-wide deadband gives a slight lean hesitation on mild acceleration in gear). Values in the sources are ECU-specific (for example about 1 % per 100 ms, or 0.2 to 0.5 %).
- Detection filters add latency; keep them as short as possible.
- Tip-out enleanment: lower priority because drivers feel lift-off richness less, but limit how rich it goes for emissions and economy. A very rich spike on a lift during a shift (one log: about lambda 0.67) means enleanment is not removing enough fuel, not a VE error.
- Asynchronous (extra, unscheduled) pulses help where events are far apart (low rpm) or transport delay is long (rotaries, injectors far from the port). Use a lockout so repeated blips do not stack async fuel. One practitioner uses synchronous only in nearly all other cases.
- Some ECUs use a predicted manifold pressure (from throttle and rpm) for a short window. The prediction table must match real steady-state pressure; if the window is too short the ECU returns to the lagging sensor too early, if too long a turbo engine is fuelled for about atmospheric while boost builds, and it goes lean. One default of about 200 ms worked well.
- Optional transient ignition retard is seldom needed; use it only when momentary tip-in knock is actually observed.
- On factory calibrations with slow power-enrichment ramp-in (for emissions and economy), speeding the ramp sharpens response.

### When tip-in will not come right
Strange enrichment values that break the expected trend (falling with rpm and starting load) are a red flag: look for a base table error in that area, throttle sensor noise, or a slow manifold pressure signal. A stab from idle momentarily uses cells at low rpm and atmospheric pressure that cannot be tuned in steady state; extrapolate their trend and revisit them before inflating enrichment. Large opposite-sign closed-loop trims in neighbouring cells also produce momentary excursions felt as hesitation, which is a steady-state table problem. One practitioner reports never failing to get clean transient response conventionally, so a persistent problem suggests a set-up fault.

### Related effects
- Changing injection timing, injectors (spray and targeting), throttle bodies or intake layout can change transient needs; recheck afterwards. Larger aftermarket injectors with wider sprays tend to wet more wall and need more cold and transient fuel.
- Air mass meter systems benefit particularly from throttle-rate enrichment, because the meter sees flow changes out of step with the cylinders.
- Ramp runs read leaner than steady-state cells (about 5 % in one demonstration) because the film grows during acceleration. Tune full load in ramp runs, or expect road acceleration to run leaner than a steady-state-tuned target. One practitioner's view is that differences between gears matter little because lower gears load the engine less; focus safety on the high gears.
- Do not disable transient enrichment while tuning the main table or gathering auto-tune data: real transients give bad data either way, and without enrichment they also give a lean hole. Drive smoothly, use the logging tool's transient filters, and disregard lambda during sharp throttle movements.
- A sluggish throttle blip for shifts can come from poor transient fuel or over-rich overrun cells; tune overrun VE and transients before blip settings.
- Wrong transient fuelling causes drivability problems rather than mechanical damage in the sources; bore washing needs sustained richness, not brief enrichment events.

## Decision rules
- Do not use enrichment to patch a poorly tuned main fuel table.
- Make reasonably large changes while testing, since 2 to 3 % will not be visible.
- Test from about the same manifold pressure each time, with closed loop off.
- The least enrichment that gives crisp, bog-free response wins over the flattest trace.
- Expect enrichment to fall with rpm and with starting load and to rise cold; values that do not follow this trend point to another fault.
- Spend more transient effort on road cars, which live at low rpm and part throttle, than on race cars that live at high rpm and wide throttle.

## Data gates
Warm engine; throttle events repeatable; lambda sensor delay accounted for; applied-enrichment, throttle-rate, manifold pressure, pulse width and lambda channels logged at a rate fast enough to resolve the event.

## Worked example
Stabbing the throttle at 2500 rpm shows a 0.3 s lean spike. Raising enrichment there removes it without changing cruise. In one dyno sequence, a 20 % clamp left a tip-in about 6 % lean (lambda 1.06) with crisp response; doubling to 40 % removed the lean spike but caused a rich dip to about 0.83. The practitioner kept the lower value: the lean blip was brief and the engine felt sharper.

## Disputed / conflicts
- Cross-check: the wall film explanation matches the combustion textbook and an engine-control textbook, which give the model but no enrichment procedure.
- **Throttle rate or manifold pressure as trigger.** Several practitioners prefer throttle rate (faster, cleaner signal; manifold pressure is filtered and lags); film-model advocates base it on manifold pressure because that is the physical cause. Both agree film models can perform better when calibrated well but take more work.
- **Dyno or road.** Most sources tune transients on the road for feel, using the dyno to get the trace reasonably controlled first; one session tunes cell by cell on the dyno. Both confirm on the road.
- **How much lean blip is acceptable** varies between sources: about 1 % ignored, about 10 % as the point to work harder, momentary 15 to 17:1 AFR on gasoline accepted when response was crisp. These are practitioner judgements tied to feel, not limits.

## Citations
- practice: Practitioner training and tuning practice, distilled and cross-checked.
- engineering-texts: Engine, combustion, charging and control engineering texts.
