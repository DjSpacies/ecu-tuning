---
id: methodology/full-load
title: Full-load tuning
layer: L2
status: draft
confidence: high
sources: [practice, engineering-texts]
verified: 2026-11-11
applies_to: {fuels: [gasoline, ethanol, methanol], engines: [all]}
depends_on: [methodology/steady-state-ignition, methodology/knock-assessment]
supersedes: []
---

# Full-load tuning

## Claim
Approach full load gradually using ramp runs, starting inside proven territory and adding rpm in small increments, fuelling safe first and ignition after. Enter untuned territory slightly rich and slightly retarded, at the lowest boost available, with protections armed, and work towards the optimum from the safe side. Judge every change on runs made under the same conditions, at a ramp rate that loads the engine the way it is used.

## Why (derivation)
### Risk is highest here
A full-load error happens at the highest cylinder pressure and thermal load; at high specific output, damage from a lean or over-advanced condition happens within moments, while low-power NA engines tolerate small errors better. Short runs that extend proven range keep each new step close to known behaviour, and VE rarely changes dramatically within 500 rpm of a tuned area. Fuel is fixed first because it sets the mixture knock and timing are judged against.

### Steady state is not the same as a ramp
Steady-state WOT values are close to what a ramp needs (within about 5 % in one source) but the accelerating engine behaves differently: fuel-film effects can make it leaner, charge and chamber temperatures differ, and a turbo engine's MAP changes along the run as it spools. Hence the pre-run safety margin and correction from ramp-run logs rather than copying steady-state numbers.

### Ramp rate sets load and heat
Too fast a ramp under-loads the engine, hiding knock and fuelling problems and reading low power; a relatively slow, heavily loaded ramp is where knock is most likely. The sources pick a rate that matches acceleration in a high gear on the road (about 400 to 500 rpm/s, or about one second per 500 rpm) and keep it constant. A much longer ramp near the end builds the heat of sustained use and acts as a validation.

### Sustained use is hotter than a dyno pull
Exhaust gas temperature does not reach equilibrium in a short ramp; on track, or gear after gear on the road, it keeps rising, and chamber heat builds. An engine knock-free on the dyno can knock under sustained road load or at a gear change. Use, not the dyno pull, sets how much margin is needed.

## Assumptions
- Fuel system capacity is known adequate (injector duty and pump flow checked on the first runs).
- Steady-state tuning complete to about two-thirds of the rev limit, or to the limit of what can be held (for example wastegate spring pressure on a turbo engine).
- Rev limiter, overboost cut and lean protection are configured, and the conservative limits set for first start have been raised to just above intended targets.
- Knock monitoring (audio knock equipment or a calibrated knock system) is active.

## Breaks when
- Long pulls on road or track heat the charge more than a short dyno run.
- Boost varies run to run; variable boost control can mimic or hide a gain.
- Very stiff wastegate springs: at moderate rpm a small throttle increase lets boost jump to a high value, so higher boost cannot be held in steady state and the region between the steady-state area and the WOT line is only reached transiently.
- Automatic transmissions kicking down, and torque converters slipping, at low rpm WOT.
- Inertia dynos: ramp rate is set by power and gear, not chosen.

## Practical use
### Prepare the map
- Add a little fuel and remove a little timing across the full-load area before the first runs. In the sources this is typically 2 to 5 % fuel and about 2 degrees of timing over the top load rows (or the boost region, or the 80 to 100 % throttle rows on a throttle-position axis), then restored once runs are verified. On a VE table that interpolates between rows, cover both rows WOT falls between. Some demonstrations go further on the first boosted pulls: timing set very low across the boost region (from about 0 to 10 degrees) so fuel can be found hands-off and the knock-noise baseline recorded.
- On a turbo engine, start on wastegate spring pressure with boost control off or duty at zero, check the MAP axis and the overboost cut sit above what will be reached, and raise both before targeting more boost.
- Extrapolate fuel and timing into untuned rpm with safety in mind: copy the last tuned timing column flat to the limit (higher rpm normally wants at least as much), and shape fuel to rise towards peak torque and ease off towards the limiter. Expect peak values in a VE table around the rpm of peak torque, and investigate any table that does not show this.
- On boost, extend the load axis a little beyond the maximum expected.
- Make sure post-start enrichment has ended and temperatures are normal before evaluation runs.

### Run the ramp
- Ramp rate about 1 second per 500 rpm (400 to 500 rpm/s in the sources). Start where the car realistically accelerates (about 1500 to 2000 rpm), not at 1000 to 1250 rpm where engines dislike load and cars rarely accelerate.
- First run only through the range already tuned in steady state, or about 500 rpm past it, expecting slightly rich. Extend the end rpm by about 500 rpm per run while learning (about 1000 rpm once confident, or on a familiar engine), fixing fuel in the active rows and extrapolating into the next rpm zone before each extension. Reach the limit over roughly five or six runs; do not go to the limiter on the first run.
- Experienced tuners may set a high end rpm and simply lift when lambda starts to wander; this is safer when closed loop is active to catch fuelling errors.
- Rev until power is clearly past peak and starting to fall, to map the useful range, but stay below the limiter; there is little value far beyond peak power.
- Watch lambda (and boost while it builds) against limit lines; listen for knock. Abort at once on lean drift, knock, boost overshoot or mechanical noise. One demonstration aborted when lambda drifted from about 0.82 to 0.90 by 5500 rpm.
- If a cell is lean or knocking under load, do not stay there correcting it: back out to idle, change fuel and timing with the engine unloaded, then return and check. Turbo engines in particular tolerate sustained lean operation poorly.
- Log every run in the ECU and save the dyno runs for overlay. The log cursor ties lambda error to the exact cells used; on a turbo engine the MAP row changes along the run.
- For log-based or histogram correction, start logging at full throttle just before the ramp and stop before lifting, so tip-in and overrun samples do not land in the table.

### Correct fuel
- Keep lambda on target first. Read measured lambda and closed-loop trim together.
- Mentally smooth sample-to-sample noise. Treat errors within about 1 to 2 % as acceptable and correct only errors of about 2 % or more; chasing smaller errors means chasing run-to-run variation.
- Correct slightly less than the indicated error (for example 2 % for a 3 % spike) and creep up over runs; single-log corrections tend to overshoot.
- Within steady-state tuned columns change only the WOT rows; beyond the steady-state limit, if a column is rich at WOT, the guessed VE is probably high through the whole column and further out, so apply the change to the whole column and extrapolate it to the right.
- On a turbo engine, follow the falling boost when choosing which load cells to change, and accept small residual errors in transition cells that are only passed through.
- A small negative trim (engine slightly rich) is preferable to a positive one; one run is not grounds for change.

### Then ignition
- Add timing in steps of about 2 degrees across rows, reducing to 1 degree steps near the optimum, and stop when torque no longer rises. Remove added timing that does not repeat as a gain.
- On a knock-limited engine, try a slightly richer target (about 0.02 lambda in one source), retune fuel and see if more timing is accepted.
- Finish WOT changes before blending them into lower-load cells.
- Change one variable at a time and compare on overlaid runs from the same starting temperatures.

### Raising boost
- After any boost increase, recheck fuelling immediately before adding timing.
- Extend the observed row-to-row trends (one demonstration saw fuel rising about 2 % and timing falling 2 to 3 degrees per 20 kPa row), raise boost about one row at a time, refine, and re-extrapolate. Revisit fuel and spark at each higher boost step, keeping the rev limit conservative on a stock engine.
- Small boost increases that stay within cells already crossed add little; step into genuinely untuned rows before fine correcting.

### Validate
- Finish with one or two much longer runs (about 1.5 s per 500 rpm, or about 200 rpm/s on a knock-sensitive engine) and listen for knock. If none appears and lambda holds, timing margin and temperature trims are judged enough for road or track use. Watch the cooling system: long runs overheat a car on a dyno with poor fan airflow.
- For sustained use (high gears on fast roads, track), the sources add a few percent fuel by gear or road speed because dyno EGT understates sustained-load EGT.
- Confirm on road or track (methodology/road-procedure).

## Decision rules
- A ramp of about 1 second per 500 rpm is a useful default; finish with a longer run.
- Remove about 2 degrees on the top rows before the first run; add rpm 500 at a time.
- Abort on knock, lean drift or boost overshoot; never stay in a bad run hoping it recovers.
- Keep lambda on target first; then add 2 degrees over rows, reducing to 1 degree steps near the optimum, and stop if torque does not rise.
- Fuel is safer rich: start rich and remove.
- Correct only repeatable errors larger than the run-to-run spread, and slightly under-correct.
- Lowest boost first; recheck fuel after every boost increase.

## Data gates
- Injector duty below ceiling; no limiter or cut active during the run.
- Run-to-run temperature comparable (coolant, intake air) and peak boost comparable.
- No wheelspin, kickdown or slip during the run (engine rpm to roller speed ratio smooth).
- Knock channel clean at the timing being kept.

## Worked example
A first run ends at 5000 rpm, lambda 0.91 against a 0.88 target. Fuel is added to the rows that were active. The next run extends to 5500.

The error is 0.91 / 0.88 = 1.034, about 3.4 % lean. Following the under-correction habit, about 3 % is added to the active WOT rows rather than the full 3.4 %, and because 5000 rpm sat beyond the steady-state limit, the same factor is carried across that whole column and into the extrapolated columns to its right. The next run to 5500 rpm reads 0.885, inside the 1 to 2 % band, so that zone is left alone and the run is extended again.

## Disputed / conflicts
- Cross-check: The combustion textbook describes mixture being enriched towards maximum power near wide-open throttle (p.834), which agrees. Run-length and step rules are practice.
- Size of the pre-run margin: the sources range from about 2 % to 5 % fuel with about 2 degrees of retard, and some use very low flat timing in boost for the first pulls. All agree on direction (rich and retarded first); the size depends on confidence in the steady-state data.
- Extension step: 500 rpm for learners in most sources; 1000 rpm used by an practitioner to save time; straight to the limit for experienced tuners with closed loop active. The step is a risk choice, not a property of the engine.
- Closed loop during ramp runs: one demonstration disables it and corrects from measured against target lambda; others leave it on as a safety net and fold trim into the correction. Both work if the correction accounts for what closed loop was doing.
- Knock mid-run: abort is the rule. One practitioner's view is that a couple of momentary light events on a low-power robust engine may not require aborting. The KB keeps abort (methodology/knock-assessment).
- Final timing on a drag car: one practitioner recommends getting timing close on the dyno and adding about a degree per pass at the track, keeping it only if trap speed rises, because chasing the last horsepower on the dyno is unnecessary risk. Other competition examples in the sources stop at target power with conservative timing. Both prioritise reliability; they differ on where the last step is taken.

## Citations
- practice: Practitioner training and tuning practice, distilled and cross-checked.
- engineering-texts: Engine, combustion, charging and control engineering texts.
