---
id: methodology/cold-start-warmup
title: Cold start and warm-up
layer: L2
status: draft
confidence: high
sources: [practice, engineering-texts]
verified: 2026-11-11
applies_to: {fuels: [gasoline, ethanol, methanol], engines: [all]}
depends_on: [methodology/transient-tuning, principles/fueling/transient-fuel-film, methodology/idle]
supersedes: []
---

# Cold start and warm-up

## Claim
Cold tuning needs a truly cold engine. Start with large changes, because cold-engine feedback windows are short, and treat wideband data early in a cold start with caution.

Starting fuel runs in stages: an optional prime, cranking enrichment, post-start enrichment (run-time based)
and warm-up enrichment (coolant based, ideally also load based). Each stage is a multiplier or adder on the
warm main fuel table, so it can only be tuned after that table is right. Each stage is judged by its own
evidence:
- cranking by how quickly and crisply the engine fires;
- post-start by lambda in the first seconds after firing;
- warm-up by lambda once post-start has decayed.

Cold faults are never fixed in the main table. The same post-start table also covers lean hot restarts after
heat soak.

## Why (derivation)
- **Wall film.** Hot ports and valves flash fuel to vapour. Cold metal lets fuel condense as a film and enter as
  liquid that burns poorly. To keep the same effective mixture, far more must be injected, and more still while
  cranking (principles/fueling/transient-fuel-film). Gasoline's light fractions only begin to vaporise around
  40 °C, which is why the vapour fraction of a cold charge is too lean to burn on hot-engine fuel alone. One
  source illustrates the film as a notable share of each injection (an example of about 20% per cycle).
- **Load dependence.** Film is worst at low air speed (idle, light cruise) and much smaller at high airflow,
  where fuel stays suspended. Enrichment needed at a given coolant temperature therefore falls with load. In
  one demonstration table at 20 °C, closed throttle wanted about 30% while wide open wanted about 2.5%. A
  coolant-only table tuned at idle runs rich when the car is driven hard while cold.
- **Injector placement.** Injectors far from the valve (trumpet-mounted, throttle-body injection) wet more tract
  and need more enrichment and sometimes a prime. Injectors aimed at the valve back need less.
- **Cold torque loss.** Thick oil and tight clearances add friction, and poor fuel preparation lowers combustion
  efficiency. A cold engine needs more idle air, often a higher idle target, and sometimes a slightly richer
  target to idle smoothly (methodology/idle).
- **Hot restart.** After a hot engine sits for five to ten minutes, fuel in the rail is superheated toward vapour
  and the manifold is hot, so less fuel mass arrives. The engine runs lean for roughly 10 to 60 s. Warm-up
  enrichment is zero at that coolant temperature, so post-start enrichment in the hot rows covers it.
- **Why order matters.** The enrichments are percentages on the base calculation. Tuned before the base is
  right, they absorb base errors. Retuning the main table later then shifts them.
- **Volatility of ethanol.** Ethanol is far less volatile and harder to light cold, so cranking fuel must rise
  sharply. Warm-up needs only somewhat more.

## Assumptions
A warm-up lasting long enough to observe, and the engine cold-soaked to the condition being tuned.

- The warm main fuel table, injector data and target lambda are proven at operating temperature, including the
  idle cells and the faster cold-idle cells (for example 1000 to 1300 rpm).
- Hot closed-loop trims at idle are small. One practitioner accepts about −4% at a heat-soaked idle at most; with
  ±15% trims, cold tables only fudge VE error.
- Cranking cells (zero rpm, near atmospheric pressure) and the low-rpm cells the engine passes through on start
  hold a sensible smooth extrapolation of the tuned table.
- Coolant and air temperature sensors are calibrated. After a full soak both should read ambient.

## Breaks when
A wideband needs its own warm-up. Readings straight after starting can be wrong or absent.

- **Not truly cold.** Blocks hold heat for hours. Starting even 5 to 10 °C above ambient is not a cold start.
  Expect only one to three usable cold starts per day.
- **Season.** Summer mornings may only reach 10 to 18 °C, while winter mornings reach −5 to −10 °C. Cells colder
  than the coldest tested temperature are extrapolation only.
- **Closed loop during warm-up.** Measured lambda can look on target because trims are correcting. Watch the
  short-term trim, or tune open loop.
- **Big-overlap cams.** Idle lambda is unreliable, so cold start becomes partly a feel job: start from base
  values, reduce fuel and watch the idle.
- **Millisecond-based start tables** must be rescaled after an injector change. Percentage-based warm-up
  corrections usually need little change.
- **Running too cold.** An engine that never reaches its normal range (for example, no thermostat with an oversize
  radiator, running around 50 °C) stays in warm-up enrichment, runs rich and wears forged-piston skirts and rings.
  Restore the normal range with a thermostat, restrictor, pump control or partial blanking, rather than
  retuning around it.
- **Mechanical fuel pumps** may not build pressure at cranking speed (200 to 300 rpm). One source fits a small
  electric primer pump, run only between about 50 and 500 rpm, instead of starting fluid.
- **Weak trigger at cranking.** Some variable-reluctance sensors produce very little voltage at cranking speed.
  The zero-rpm arming threshold may need lowering before the engine will start at all.

## Practical use
### Schedule
- Finish the hot calibration (dyno, then road), cool the engine, preferably overnight, and tune cold start the
  next morning. Several practitioners run customer cars over two days for this reason.
- Before cranking, confirm that coolant and intake air temperatures agree with each other and with the room.
  Power the wideband early, so the first seconds are logged.
- Start from the ECU's base cold-start values, which the sources describe as usually close.

### Identify the active stage
- Watch the runtime trim channels (prime, crank, post-start, warm-up) alongside lambda, and change only the
  stage active when the fault occurs. Changing the wrong stage moves fuel in a phase that was fine.
- When all stages are right, the added fuel steps down smoothly. A later stage adding more than an earlier one
  (warm-up above cranking, say) suggests a mistake.
- Warm-up from 10 to 15 °C may take only three to five minutes, so post-start, warm-up and cold idle air are
  often tuned in the same session, switching between them.

### Crank-to-run threshold and prime
- Set the run threshold a little above observed cranking speed and below idle (typical values: 300 to 500 rpm,
  with cranking itself at 150 to 250 rpm). If the threshold sits below cranking speed, the ECU leaves crank mode
  while still cranking and the cranking fuel stops applying.
- Set the crank-entry threshold below the slowest continuous cranking, including on a slightly low battery.
- A prime pulse (key-on, first rotation, or throttle-pumped) is rarely needed with injectors close to the valve.
  Consider it for remote injectors and throttle-body injection. Several practitioners leave it off and enable it
  only if starting is poor.

### Cranking enrichment
- No wideband reading is usable while cranking, so judge the start itself:
  - many revolutions before firing means too little fuel;
  - a quick, crisp start means about right;
  - a hesitant start that needs throttle, followed by lambda diving very rich just after firing, means too much.
- A rich dip that clears within a second or so after a crisp start points at cranking fuel slightly high rather
  than at post-start.
- Make bold, whole-table changes so the effect is obvious. Sources use 20 to 50% steps, or doubling and halving
  when the engine only coughs. 5 to 10% steps give no clear direction. Scale the whole table to keep its default
  shape.
- Settle on the smallest amount that starts crisply. Flooding is harder to recover from than a slightly lean
  crank, and excess cranking fuel over five or six cold starts in a row can foul plugs until they are cleaned.
- Tune three or four temperature points (about 0 to 20 °C, 40 to 50 °C, and hot 70 to 90 °C) and interpolate.
  The engine spends only seconds cranking.
- One method isolates cranking by temporarily disabling post-start and coolant corrections. The engine should then
  fire crisply and die, because nothing bridges it to warm running.
- Hold cranking fuel only briefly once the engine fires. In one example, cranking fuel held for about 0.5 to
  0.6 s after the crank ended, plus a large multiplier, caused rough, over-rich running right after fire-up.
  Cutting the hold to about 0.2 s fixed it.
- Many start tables taper cranking fuel toward full throttle as a flood-clear function.
- Cranking timing: about 10 degrees is the usual safe start, with a range of about 5 to 20 by engine. High
  compression or big cams may kick back against the starter, so retard. Cranking near 0 to 5 degrees BTDC can help
  a cold engine fire, especially on alcohol, because the charge is hotter at ignition. Keep the main table's
  cranking-region cells (very low rpm, near atmospheric pressure) at a modest value, because some engines read
  timing from them while cranking.

### Post-start enrichment
- Covers roughly the first 5 to 30 s after firing (hold about a second, then decay), just to stabilise
  combustion. On one cold demonstration it was near zero by about 10 s.
- Diagnosis:
  - fires, runs a second or two, then stalls: post-start too lean;
  - good just after start, then quickly lean: decay too early, so increase the hold;
  - sustained rich for the first 5 to 20 s: post-start excessive.
- Its shape usually stays consistent, so scale the whole table if it is uniformly off. One demonstration's x0.75
  scaling brought lambda straight onto target.
- Keep the last time column at zero, so it cannot persist.
- Hot rows: keep some enrichment at 60 to 100 °C coolant for hot restarts. Examples: about 4 to 6% held for 20 to
  25 s, or about 5% with a 2 s hold. It is a compromise, because an immediate restart without heat soak needs
  less. Some sources also add a few percent at closed throttle and high intake air temperature (above about
  50 °C), and reduce intake-air density correction at low load and high IAT. A hot IAT sensor at low flow does not
  represent the charge, and full correction over-leans.
- Be realistic. One source notes even stock late-model engines show momentary trims of about +12 to 15% after a
  hot restart and rely on closed loop.

### Warm-up (coolant) enrichment
- Tune it first among the cold tables, using only the period after post-start shows zero. Make each change when
  coolant sits in the middle of a breakpoint. Attribute the remaining error at the same coolant cell to warm-up
  alone, then shape post-start for the first seconds, and iterate between the two.
- One method tunes the coolant correction before post-start entirely: ignore the first 10 to 15 s lean period,
  correct the active cell against the wideband at idle, then move up the column as temperature rises.
- **Test for a base error.** If the closed-loop correction at idle is the same cold as warm, the error is in the
  VE table, not in warm-up enrichment.
- Enrichment should fall as the engine warms. A colder cell holding less than a warmer one is suspect, usually
  because the engine passed through it too quickly to tune. Follow the trend, and verify on the next cold start.
- Extrapolate the trend into untestable cold cells rather than copying the last tested value. A flat copy runs
  lean. One example: 33% at 30 °C, 40% at 20 °C and 50% at 10 °C suggest about 65% at 0 °C and 80 to 100% at
  −20 °C.
- Use a load axis (throttle or MAP) where available: largest at closed throttle, tapering as load rises. On a
  throttle axis, breakpoints above about 60% add little. On a dyno, one practitioner sets idle vacuum and a moderate
  boost point at about 20 °C and 50 to 60 °C, and interpolates. Examples: about 13.5% vs 6% at 20 °C between deep
  vacuum and +150 kPa; about 44.5% near idle vs 13.6% at 100 kPa at −10 °C.
- Zero at operating temperature. Confirm warm-up enrichment is zero across the normal running band (about
  60 to 70 °C and up) before any main-table tuning. Several practitioners lost dyno time to a base map shipping
  enrichment out to 80 to 85 °C, or to non-zero cells near operating temperature on a load axis. Residual
  enrichment silently biases the main table. Only a small amount (about 1%) is acceptable at 60 °C on engines
  that run without thermostats.
- By about 60 °C, most engines prepare fuel much as when fully warm. Roughness at normal targets between about
  35 and 60 °C says the engine still wants a richer mixture.

### Cold lambda target
- A cold engine often idles poorly at lambda 1. On ECUs whose target feeds the fuel equation, richen through a
  coolant-indexed target correction, and use the fuel coolant correction only to make the engine achieve that
  target. Fudging extra fuel into the fuel correction works only until closed loop pulls the mixture back to the
  base target.
- On ECUs with no target modifier, set the target for operating temperature, and use warm-up enrichment to run
  deliberately richer than target when cold. Expect measured lambda a little rich of target during warm-up.
- Cold engines also need more acceleration enrichment. A good warm table can feel as if the injectors switched
  off when flooring a stone-cold engine. Tune the coolant-indexed AE addition after the warm table, mostly in the
  0 to 40 °C band (methodology/transient-tuning).

### Cold idle air
Fill the idle base position table across coolant temperature during the same warm-ups. This is covered in
methodology/idle.

### Cold ignition
Opinions differ (see Disputed / conflicts). Where no idle air device exists, cold advance at light load is the
only torque lever left. Restrict it to light load with a coolant-by-load table, so the advance is not applied
in boost.

### Customer expectations
Tell customers up front that the first cold-weather starts may need a short return visit. Several practitioners
offer this free. It protects the tuner's reputation when untested cold cells need correction.

## Decision rules
Target slightly richer than warm idle while cold (about 0.95 is a typical example, until roughly 30 to 40 C). Make reasonably large changes per test. Ensure the wideband is powered early. Tune cold-idle air separately. Enrichment usually reduces with rising load.

Aim for a crisp start with the smallest enrichment that achieves it, since over-fuelling on start fouls plugs. Tune the main VE table first: cold enrichment is meant as a percentage on top of it. Keep some ignition reserve when cold. Ethanol blends need much more cranking fuel at low temperature.

Do not richen beyond about lambda 0.80 to 0.85 cold, because of plug fouling.

Never alter the main fuel table to fix cold running. Diagnose by stage, from where in the log the fault occurs. Warm-up enrichment must be zero at operating temperature. For ethanol, a common starting point is 25 to 50% more cranking fuel than the petrol values at high blend (one example multiplies the high-blend end by about 1.4); warm-up and post-start can use a second, blended table (methodology/flex-fuel). Recurrent plug fouling on cold starts, with plugs fine when warm, means cold enrichment is too rich: first confirm warm idle is right, then lean cranking, post-start and warm-up.

## Data gates
Coolant temperature at the condition being tuned; wideband ready; ambient and fuel temperature noted.

At key-on: coolant within a few degrees of ambient and of intake air temperature. Runtime trim channels for prime, crank, post-start and warm-up logged with lambda, short-term trim, rpm, coolant, IAT and MAP or throttle. Warm main-table trims at hot idle small, before any cold table is changed.

## Worked example
An engine at 33 C is too warm to tune for a 15 C start. Tune when actually cold-soaked.

Separating stages at 20 °C: post-start adds +39%, decaying to zero by about 30 s, and the coolant correction adds
+12.5% at idle vacuum. Coolant temperature barely moves in those 30 s. After post-start reaches zero, lambda sits
about 0.04 lean of a 0.95 cold target. That error belongs to the coolant cell, so that cell goes from 12.5% to
about 17% (a 4% richer mixture needs roughly a 1.04 multiplier on total fuel: 1.125 × 1.04 ≈ 1.17). On the next
cold start the remaining error just after firing is attributed to post-start, and its table is scaled.

Cranking: a demonstration start at about 23 °C was crisp, but lambda dropped to about 0.72 to 0.75 immediately,
then recovered within a second or so to about 0.88 against a 0.92 target. The quick-clearing dip pointed at
cranking fuel slightly high (160% in that cell), so cranking was reduced a little. The steady slightly-rich
warm-up offset was intended and left alone.

## Disputed / conflicts
- **How rich cold.** This entry's rule floors cold mixture at about lambda 0.80 to 0.85. Sources range from about
  0.95 at 20 °C (one practitioner), to about 0.88 to 0.90 at the coldest expected temperature (another, who warns
  that richer than that fouls plugs over repeated short runs), to 0.80 to 0.85 at about 10 °C (a third, who
  says never richer than 0.80 even below zero, and that below zero more cranking fuel matters more than a
  richer running mixture). Another source suggests about 12.5 to 13:1 AFR on petrol while cold, roughly 0.85 to
  0.88. All agree that slightly rich is better than lean when cold, and that gross richness fouls plugs. Test:
  idle stability and plug condition over repeated short cold runs at each target.
- **Where warm-up enrichment lives.** One ECU maker suggests doing all warm-up in the post-start (run-time)
  table. One practitioner disagrees because that table has no load axis, and keeps post-start only for the first
  seconds. Some ECUs make the post-crank table minutes long, so it is effectively a warm-up table.
- **Order of tuning.** One practitioner tunes warm-up first, then post-start, then cranking last. Others tune
  prime and cranking first (with the later corrections disabled), then coolant correction, then post-start. Both
  isolate one stage at a time. Test: whichever order converges in fewer cold starts.
- **Cold ignition advance.** Some sources add advance when cold to recover torque, especially with no idle air
  device. One practitioner normally leaves cold timing alone and has not seen a benefit, noting that factory
  calibrations often advance significantly after catalyst-heating retard ends. Another sees cold advance as
  useful only when hot idle timing is deliberately retarded for idle control.
- **Pre-crank prime.** One practitioner leaves a key-on prime enabled. Most leave it off, and one has used it only
  once or twice in a career. One prefers a throttle-triggered prime, so the operator controls exactly what goes
  in.
- **Lambda 1 when cold.** Factory ECUs often run lambda 1 soon after a cold start, for emissions and catalyst
  light-off, relying on fast closed loop. Practitioners argue that without equivalent closed loop, or with big cams,
  running richer cold is better.
- **Oil-pressure start delay.** One source offers a start delay to build oil pressure. Another regards inhibiting
  firing until oil pressure builds as rarely needed on modern engines.
- Cross-check: engine textbooks both describe cold-start and warm-up enrichment as a function of engine
  temperature. Neither gives a procedure, so the specific steps here are practice.

## Citations
- practice: Practitioner training and tuning practice, distilled and cross-checked.
- engineering-texts: Engine, combustion, charging and control engineering texts.
