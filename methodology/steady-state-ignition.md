---
id: methodology/steady-state-ignition
title: Steady-state ignition and MBT
layer: L2
status: draft
confidence: high
sources: [practice, engineering-texts]
verified: 2026-11-11
applies_to: {fuels: [gasoline, ethanol, methanol], engines: [all]}
depends_on: [methodology/steady-state-fuel, principles/combustion/mbt-timing]
supersedes: []
---

# Steady-state ignition and MBT

## Claim
Where torque can be measured and knock margin exists, advance in small steps from the retarded side until torque stops rising, then settle at the start of the plateau. Where knock arrives first, the map is knock-limited and sits a margin below the knock threshold. Each cell is judged by its own measured response, and the trends between cells are used to check it, predict the next cell, and fill cells that cannot be reached.

## Why (derivation)
See principles/combustion/mbt-timing. Torque is flat near the optimum, and timing beyond it adds knock risk for no gain. Most pump-fuel and boosted engines reach the knock limit before MBT. Fuel is tuned first because spark does not change the trapped mixture, while a conservative spark map removes knock risk while fuel is still unknown. Changing one variable at a time keeps every change attributable.

## Assumptions
Torque is measured repeatably on a load-holding dyno. The engine is knock-monitored, by audio detection or ECU knock control, throughout. Fuel is on target. Base timing has been confirmed with a timing light, because a wrong offset can hide 5 to 15 degrees more real advance than the laptop shows.

## Breaks when
- **No torque feedback:** without it there is no way to find MBT. On the road or an inertia dyno, timing must be justified by knock threshold (if knock-limited) or by conservative known values, or held. Only ramp runs are possible on an inertia dyno.
- **Poor torque resolution:** at about 1000 rpm, or very light load, the engine barely turns the rollers and torque resolution is too poor. Steady-state ignition work starts around 1500 rpm and moderate load, and the lighter cells are filled from trends.
- **Automatic transmissions at low rpm:** converter slip rises with torque, so rpm flares as timing improves and the engine leaves the cell centre. Re-set the dyno point and confirm MAP before each comparison.
- **Unstable conditions:** very light load on some dynos, or rising coolant temperature during long holds.
- **Inherited calibrations:** where the delivered timing is base table plus modifiers, or the load axis is calculated air mass (so a wrong VE also puts the engine in the wrong spark cell), the table value is not what the engine gets. Log delivered advance.

## Practical use
### 1. Base table before fuel tuning
Start retarded and advance. Never start over-advanced. Typical in the sources:
- A flat value of about 15 degrees is knock-safe for most NA engines, with a little less at low-rpm full load on knock prone engines.
- Turbo engines: about 15 degrees to the onset of boost, then retard to about 8 to 10 degrees at 1 bar of boost. Go lower on high compression; one example reached about 2 degrees at 240 kPa absolute on a 10:1 engine on pump fuel.
- Engines with known knock prone peak-torque bands get extra retard there.
- High-compression engines get lower first full-load timing (about 10 degrees in one example) while VE, cam settings and the knock noise baseline are developed. Cam changes invalidate spark tuned earlier.
- A base map with 40 to 45 degrees at part throttle is too aggressive to start fuel tuning on. A blanket value around 15 to 20 degrees is safe without making the engine bog and overheat its exhaust.

### 2. Measuring a cell
- **Isolate the cell.** Set the target cell and its neighbours to the same value, and change them together, so small drift and interpolation do not dilute the change. Hold rpm and load centred, with the throttle foot dead still. Any throttle movement changes airflow and masks the timing effect.
- **Compare before and after.** Type the new value, watch torque just before committing it, then watch for the step just after. Mentally average the oscillating trace; watch the graph, not the jumpy number.
- **Step size.** Use 4 to 5 degrees (even 10 in vacuum on an engine known not to be knock-limited) while far retarded. Use about 2 degrees as gains shrink, and 1 degree only when being fussy, since 1 degree is often lost in the noise. Finer than 1 degree is not needed. In boost be more cautious.
- **Torque sweeps.** Some dynos can sweep advance about 1 degree per second while plotting torque against ECU-reported timing. This shows the curve shape well but is too slow for every cell. Use it on a handful of cells to sanity-check the trends.

### 3. Deciding the value (diagnostic tests)
- **Large gain per step:** far retarded; keep going. **Shrinking gains:** near MBT. **No gain:** on the plateau; remove that step.
- **Bracket test:** when advance shows no gain, retard about 2 degrees below the start. A torque drop means the start was right. No drop means the cell was over-advanced, so keep retarding until torque falls, then return to the last value before it fell. When two cells in a row prove over-advanced, start the next by pulling timing first.
- **Repeat doubtful results.** A torque jump that coincides with a small throttle movement or drift off-centre is not a timing effect. At light load, torque is extremely sensitive to throttle. Re-centre and toggle back and forth until the result is consistent.
- **Splitting hairs:** when two values differ by a few N·m or under about 1 %, keep the more retarded one or split the difference, especially as load rises and on turbo engines.

### 4. Moving through the table
- **Up in load:** optimum advance falls with load, so a straight copy upward lands on the advanced, unsafe side. Pre-set the next cell below the trend prediction (typically 2 to 4 degrees under the previous optimum, or the trend value minus about 2 degrees), then advance. Some practitioners restart from a safe low value instead.
- **Across in rpm:** copy the finished column into the next one without adding advance, even though the engine will usually take more (often 2 to 4 degrees). Tune upward from there. Beyond the steady-state limit (about two-thirds of the rev limit), copy the last tuned column flat across and leave it for ramp runs.
- **Use the trend.** At fixed rpm the sources typically see about 2 degrees less per 10 kPa in vacuum, flattening to about 1 degree per 10 kPa or 2 to 3 degrees per 20 kPa higher up. Across rpm, about 2 degrees more per 500 rpm early on, plateauing in the mid range. Trends are specific to the engine and do not continue indefinitely. The measured cell wins.
- **Skip sites.** Optimum varies smoothly, so tune every second load site and interpolate the rest. Breakpoints added only for fuel needs can be filled by interpolation.

### 5. Unreachable cells
- **Lighter load than the dyno can hold:** at least the lowest tuned value, since demand stays the same or rises as load falls. Extend the slope a cell or two, then cap it. Apply the same delta found in the lowest reachable cell when a new column needed more.
- **Boost beyond what is reachable:** extrapolate the observed reduction but more conservatively. One practitioner pulls 5 to 6 degrees per 20 kPa where the tuned area showed about 3. Others remove an extra 2 degrees, or 3 to 4 per 20 kPa. Verify on ramp runs. On pump fuel the per-step retard tends to grow at higher boost as charge temperature climbs, so add margin as boost rises.
- **Why it matters:** the ECU interpolates toward unreached cells when operating near them, and boost overshoot can land there. Negative values in never-visited cells are harmless if they only keep the table shape. Large steps next to visited cells are not.

### 6. Review the finished surface
- Check the 3D view. Expect advance rising with rpm, falling with load, a dip around peak torque on knock-limited engines, and a plateau in the mid table.
- Holes, spikes and up-then-down trends usually mean a mistuned cell, often from drifting off-centre. Retest them rather than trusting either neighbour.
- Do not smooth away real requirements, but do smooth steps in areas where torque resolution was poor.
- Shape a gradual transition off idle (idle about 16 to 18 degrees in several sources, with idle ignition control doing the fine work). A 15-degree idle next to a 27-degree 1500 rpm cell causes erratic drivability.

### 7. Full-load timing on ramp runs
- Before the first ramp run, add a few percent fuel and pull about 2 degrees in the area to be run. Ramp conditions want slightly different fuel and spark from steady state.
- Lay a baseline run, add about 2 degrees over the rows actually used, and overlay only the previous run. Keep the timing where torque rose and remove it where curves overlay. Add more only where gains were large, and back out the last step anywhere knock appears.
- Check from the log which load rows the run visited before judging a change. A change in rows the run never reached will show nothing.
- Read the torque curve rather than power, and treat sub-kW differences as noise. Let intake air temperature settle between runs (within about a degree at run start).
- Carry full-load gains down into lower-load cells of the same rpm, blending so adjacent steps stay small. Do not advance part-load cells to a knock threshold, because they are often not knock-limited and would end past MBT.
- A jagged torque curve and lazy feel, with gains everywhere from a step, mean the timing is grossly retarded.
- Very low timing in boost can drive the turbine harder. Adding timing may then reduce boost toward wastegate pressure, so expect the boost change.
- Tune at minimum (spring) boost first, then raise boost in stages, pre-retarding the next rows.

### 8. Special cases
- **Single-value or mechanical distributor timing:** only the whole curve can be shifted. Advance it a couple of degrees per ramp run and keep the best net compromise, since low rpm wants less than high rpm. This also adds cruise advance, so watch for part-throttle knock on high compression or poor fuel. A single cruise value is always a compromise across rpm.
- **Switching cams:** cells tuned on one cam will want different timing when the changeover moves. The high cam typically accepts a few degrees more. A large step across a short rpm span still needs verifying.
- **Ethanol:** non-knock-limited areas typically need only 2 to 4 degrees more. The large gains are in areas that were knock-limited on gasoline.
- **Drivability:** retarding light-load, just-off-idle timing away from MBT can soften cam lope and jerky pull-away. Some ECUs' OE-style knock-learning strategies make the torque curve lumpy. One practitioner prefers reducing the learned authority and raising the base table, on a car tuned for its fuel.

## Decision rules
- Always start from retarded, safe timing and advance. Once near MBT, advance in steps of about 2 degrees. Take the point where torque first peaks, not where it starts to fall.
- Timing generally rises with rpm and falls with load. A higher-load cell needing more advance than the cell below it is a red flag: retest the lower cell.
- When torque differences are at the size of the measurement noise, keep the more retarded value. Timing that adds no torque only reduces knock margin and adds heat.
- On a knock-limited engine, find the threshold slowly and retreat by a margin. Sources commonly keep 2 to 3 degrees on road cars backed by knock detection, and more for circuit use, since lap after lap at full load builds chamber heat. Pulling more than about 4 to 5 degrees costs notable power on a knock-limited engine. The margin is a reliability-against-power decision agreed with the owner; one practitioner puts the typical cost at a few kW.
- If knock appears entering a new cell, lift, return to idle, and pull a large amount (about 5 degrees) from that area before retrying. Never sit in knock. After audible knock on a ramp run, abort and remove 2 to 3 degrees.
- High-octane fuels may never knock, so over-advancing shows up only as lost torque.
- Adjacent cells differing by more than about 4 degrees deserve a second look. Practitioners put typical neighbours 1 to 3 degrees apart and treat 5 to 6 or more as likely errors. These are review thresholds, not limits. Steps cause torque steps, surging and hunting.
- Ignition load breakpoints can be coarser than fuel breakpoints. The engine runs cleanly over a wide spread of timing, but not over a similarly wide mixture spread. Keep the ignition load axis on manifold pressure even where fuel uses throttle position, since knock and timing demand follow cylinder filling.
- As a base-map starting point, one practitioner retards about 2 to 4 degrees per 20 kPa of boost, and calls it a starting point only.
- After a head skim with no return dyno visit, one practitioner's precaution is pulling 1 to 2 degrees, depending on knock sensitivity.

## Data gates
Same as fuel, with torque repeatable to well within the size of the change being judged. Knock monitoring active. Engine centred in the cell, throttle steady, coolant and intake temperatures stable. For ramp comparisons, similar starting intake temperature and the same rows visited.

## Worked example
At 1500 rpm in a stock NA engine, the first 2-degree steps gain about 6, 5 and 3 N·m, then about 1, then nothing. The last useful step is kept. Over the column the optima fall 21, 19, 16, 14, 12 and 10 degrees from 40 to 100 kPa. At full load, 12 degrees gives nothing, but 8 degrees loses torque, so 10 degrees is confirmed at the knee. The next rpm column starts as a copy. At its lightest reachable cell it needs 2 degrees more, so the unreachable lighter cells get the same +2.

## Disputed / conflicts
- **Textbook cross-check:** timing rising with rpm and falling with load matches an engine textbook and the map form in an engine-control textbook. The knock buffer and the extrapolation slopes are practice figures with no textbook value.
- **Neighbour step threshold:** one practitioner's training session accepts about 4 degrees between adjacent zones; course material treats 5 to 6 as the review point. Both are review thresholds, not limits.
- **How close to the plateau:** some practitioners stay one step short of the measured best in boosted cells for a car that will be used hard, accepting about 1 % torque. Others run MBT whenever the engine is not knock-limited. For rotary engines one practitioner stops as soon as gains per degree taper, because the extra heat of track use pushes an over-tuned engine into detonation.
- **Pre-setting the next load cell:** most practitioners pre-set from the trend minus a margin. One restarts each higher-load cell from a safe low value. Both approach from the retarded side.
- **Road tuning:** one practitioner's view is that road-tuned, knock-limited cars come within a few percent of dyno results. That rests on his own experience, and holds only for engines that knock before MBT.
- **Ramp against steady-state values:** sources report steady-state MBT not transferring exactly to ramp runs, in both directions. Restoring the pre-ramp safety retard sometimes gained power and sometimes did nothing. Treat ramp results as the authority for full load.

## Citations
- practice: Practitioner training and tuning practice, distilled and cross-checked.
- engineering-texts: Engine, combustion, charging and control engineering texts.
