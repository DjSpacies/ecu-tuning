---
id: methodology/first-start
title: First start
layer: L2
status: draft
confidence: high
sources: [practice]
verified: 2026-11-11
applies_to: {fuels: [gasoline, ethanol, methanol], engines: [all]}
depends_on: [methodology/base-setup, methodology/cold-start-warmup, methodology/idle]
supersedes: []
---

# First start

## Claim
The first start is about getting a safe, stable running engine, not accuracy: fuel is adjusted coarsely with a conservative ignition value, and the engine's vital signs are watched.

Fuel is corrected with block changes over the whole region the engine will pass through, never cell by
cell. The tuner holds the speed with the throttle until idle control is set up. Lambda readings are taken
only once the wideband is live, and are read knowing that post-start and warm-up enrichment are still active.
Leaks, oil pressure, noises and charging voltage matter more at this stage than the mixture.

## Why (derivation)
A blank map rarely starts first time. A locked conservative timing keeps knock out of the picture while mixture is corrected.

- **Damage risk is low at this point; distraction risk is not.** At cranking and idle loads, mixture errors cannot
  hurt the engine in the seconds needed to correct them. Far too lean simply will not fire or idle. Far too rich
  mostly fouls plugs, a nuisance fixed by cleaning them. Several course lessons make this point to counter the
  belief that a near-perfect map is needed first. The real risks are mechanical (no oil pressure, leaks, fire,
  overheating from an air lock) and a tuner too focused on lambda to notice them.
- **Why block changes.** The engine moves from near atmospheric pressure at key-on, down through the low-rpm
  cells, to idle vacuum. The active cell keeps changing, and a base table's shape is often unrealistic anyway
  (for example the same pulse width from 40 kPa down to 0 kPa). Moving the whole block shifts every cell the
  engine might use, including the cranking-area cells.
- **Why only coarse accuracy.** On a cold or partly warm engine (one example: about 42 °C), post-start and
  warm-up enrichment are layered on the base table. The mixture drifts, usually leaner, as they decay. Fine
  tuning now would chase compensations, not the base table (methodology/cold-start-warmup).
- **Why a sane fuel model helps.** With correct injector data and target lambda, a VE table is close to a true
  VE. A flat starting value of around 50% usually starts a stock engine, and in one example it was almost exactly
  right at idle.

## Assumptions
Oil, coolant and fuel systems are filled, and leaks are checked.

- Base ignition timing has been verified with a timing light, and a known-safe flat or conservative timing table
  is loaded.
- Injector data, the target lambda (aim) table, and the crank-to-run rpm threshold are set (methodology/base-setup).
- A wideband is fitted, and its readiness can be seen.

## Breaks when
Very high compression or special fuels may need a different locked timing.

- **Cranking timing too advanced.** High-compression or big-cam engines can kick back against the starter.
  Retard cranking timing.
- **Run threshold below cranking speed.** The ECU leaves crank mode while still cranking, and cranking fuel stops.
  Check cranking rpm first and set the threshold above it (typically 300 to 400 rpm).
- **No trigger signal at cranking.** A weak variable-reluctance sensor may need a lower arming threshold before
  anything else matters.
- **Big-overlap cams.** Idle manifold pressure of 75 to 80 kPa absolute is normal with these cams, but it is a red
  flag on stock cams.
- **Long-stored or unknown engines.** Hydraulic lifters often tap for the first 30 to 60 s while they pump up.
  Tapping that persists, or is excessive, means stop and investigate.

## Practical use
### Before cranking
- Have a helper ready to watch the engine bay. Note coolant and air temperatures.
- With idle control not yet set, plan to hold a little throttle: examples range from 2 to 10% throttle while
  cranking and running.
- Cranking timing: about 10 degrees is the usual safe value, and cells in the main table that the engine reads
  while cranking should hold similar modest values (methodology/cold-start-warmup).

### Getting it to fire
- If it will not fire at all with a sensible base table, add fuel to the whole block and retry. One course
  lesson adds about 20 to a flat VE table and adjusts up or down from there.
- **Fires then stalls, lambda swinging lean** (about 1.1 to 1.2 in two examples): the whole operating block,
  including the cranking area near atmospheric pressure, needs more fuel. Blanket increases of about 10 to 20%
  got those engines running at about 0.93 to 0.96.
- **Starts very rich** (lambda 0.60 to 0.80): remove fuel in coarse steps. If it is extremely rich, type a much
  smaller value directly, then move to finer steps near target.
- **Grossly rich even with closed loop pulling hard.** In one example, closed loop was already removing 20% and
  lambda still sat at about 0.70 to 0.74 against a 0.93 to 0.95 target. Scale the idle region down immediately
  (×0.8 there) rather than waiting for warm-up, to save the plugs.

### Bringing the mixture into the ballpark
- Select the whole region the engine will run in, and move it together. Examples: 0 to 100 kPa and 0 to 2000 to
  3000 rpm; vacuum up to 0 kPa gauge and out to 2000 to 2500 rpm; or the entire table on an injection-time ECU.
- Steps: about 10% while far off, then a few percent, then about 0.5 to 1% near target. Wait a moment after each
  change for lambda to respond.
- Aim window: about lambda 0.85 to 0.95 (some sources accept 0.85 to 1.0). Prefer slightly rich to lean. A few
  percent rich at this stage is not a concern, and a lean swing at idle is harmless and can be corrected calmly.
- Hold about 1000 to 1500 rpm by hand while correcting. Once close, let it try to idle on its own. Some
  calibrations idle unaided at this point.
- Wait for the wideband controller to come online before trusting any reading, and remember both sensors on a
  two-bank engine may read slightly differently.
- Expect the mixture to drift lean as post-start and warm-up enrichment decay. Keep nudging the block, but do not
  chase precision until the engine is at operating temperature.
- Leave ignition alone; it is a second variable that adds nothing at this stage.

### Vital signs while it warms
- **Oil pressure:** confirm immediately, from the gauge or the warning light going out. Note the reading as a
  reference.
- **Leaks:** a helper watches for fuel, coolant and oil leaks. Shut down at once for any.
- **Noises:** listen for abnormal mechanical noise, especially on a fresh or unknown engine.
- **Coolant:** watch for overheating or an air lock.
- **Charging voltage:** about 13.8 to 14.2 V running. A non-charging alternator found early avoids a flat
  battery an hour into dyno work, after it has already skewed injector and pump behaviour.
- **Idle vacuum:** compare with what the cam should allow, as a reference for the health check in
  methodology/idle.
- **Idle speed:** idle sitting above the hot target shortly after start is normal while the cold target is active.

### Hand-over to idle tuning
Once it runs cleanly, warm it to operating temperature, then continue with idle setup (methodology/idle) and
steady-state fuel. The cold-start tables are tuned later, from a true cold soak.

## Decision rules
Hold 1000 to 1500 rpm by hand until idle is tuned. Aim for lambda about 0.85 to 0.95 at this stage, and scale the whole fuel table if the engine will not fire. Stop for no oil pressure, coolant or fuel leaks, or a charging fault.

Block changes only, no single cells. Ignition stays on the conservative locked or flat table. Do not fine-tune VE while warm-up enrichment is active. Wait for the wideband to be ready before acting on lambda. Shut down for persistent mechanical noise.

## Data gates
Oil pressure present and battery voltage around 13.8 to 14.2 V while running; wideband warmed up before its reading is used.

Coolant temperature logged, with the active enrichments (post-start, warm-up) visible, so that lambda drift can be attributed to them rather than to the base table.

## Worked example
The engine fires then dies, and lambda reads 1.2. Fuel is far too lean: add a uniform percentage to the whole table, not a local cell.

A further case: a flat placeholder table fires and stalls at lambda 1.1 to 1.2. A blanket +10% over 0 to
100 kPa and 0 to 3000 rpm gets it running near target at 2200 rpm with throttle held. It reads about 5% rich
nearer idle, then leans slightly as post-start enrichment decays. Running at about 1200 rpm with 14.1 V and
28 kPa absolute at idle, the engine is mechanically sound. Its lambda drifts from rich toward 0.99 as warm-up
enrichment fades, which is the enrichment tapering, not a base table error.

## Disputed / conflicts
- **Global trim versus VE block changes.** One course lesson suggests the overall trim (often limited to about
  ±50%), or a base pulse width, for coarse first-start changes. Another practitioner avoids the global trim,
  because it hides error that belongs in the VE table, and makes block changes directly to VE after setting the
  aim table. Both are coarse; the difference is where the correction ends up.
- **Mixture window.** Most sources aim for about 0.85 to 0.95. Some accept up to 1.0, or aim for about 0.9 to 1.0
  on a turbo engine. Leaning toward 1 is harmless at idle but closer to a lean stall.
- **Oil-pressure start inhibit.** One source offers a start delay to build oil pressure. Another regards it as
  rarely needed on modern engines, which build pressure while cranking and carry low loads at idle.

## Citations
- practice: Practitioner training and tuning practice, distilled and cross-checked.
