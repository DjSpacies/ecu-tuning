---
id: methodology/engine-protection
title: Setting up engine protection
layer: L2
status: draft
confidence: medium
sources: [practice]
verified: 2026-11-11
applies_to: {fuels: [gasoline, ethanol, methanol], engines: [all]}
depends_on: [methodology/boost-control, methodology/first-start]
supersedes: []
---

# Setting up engine protection

## Claim
Protection belongs in the ECU, configured before the engine is relied on: a rev limit, an overboost cut, temperature-dependent limits and sensible sensor-fault defaults first, then monitored-fault strategies (oil pressure, fuel pressure, lean, EGT; see methodology/engine-protection-monitored-faults). Each response is matched in severity and speed to how quickly the fault destroys the engine, is gated so it does not false-trip, and is logged so a cut can be traced to its cause. A protection is a backstop that reveals a problem; the fix is the root cause, never a looser or disabled limit.

## Why (derivation)
- A driver at the limit watches shift lights, the track and perhaps lap time, not engine vitals. Several failures in the sources (an oil gallery holed at speed, a head lifted after a high-EGT warning) happened with a warning showing, because drivers stay flat when they are winning. Automatic action is therefore the only protection that reliably acts in time. The ECU sees every input continuously.
- The ECU applies the lowest of all active rpm limits. So any protection can be built from generic limiter tables (rpm limit indexed by any channel), and a protection table's "safe" value must sit well above the main limit or it silently caps rpm later.
- Tables interpolate between breakpoints. A temperature-indexed limit falls progressively between two cells unless the breakpoints are placed close together to form a step.
- Load reduction options differ in harshness: retard and enrichment are gentle and invisible; dropping boost back toward spring pressure removes load cleanly; a throttle cap is moderate; a lowered rev limit is the most aggressive and the most obvious to the driver, which is useful when the driver must notice.
- Fuel cut versus ignition cut. With ignition cut, the unfired cylinder pushes its whole fresh charge out into a hot exhaust. If it lights there (more likely on turbo manifolds) the pressure pulse can lift a closed exhaust valve off its seat: hydraulic lifters extend into the gap and then keep the valves from closing, heavy pedestal-mounted rockers can be thrown, shim-type buckets can spit shims, catalysts and stock rotary apex seals suffer. Fuel cut removes the whole injection event from selected cylinders, so there is no lean burn. The residual port wall film is far too lean to fire, and the only side effect is a brief lean moment as the film rebuilds on reinstatement, much like a tip-in transient.

## Assumptions
- The ECU offers rev, MAP and generic limiter tables, and the relevant sensors exist and are logged.
- Port injection with sequential or per-cylinder control for fuel-cut limiting. Group-fire or shared auxiliary injection cannot cut fuel cleanly for one cylinder; some ECU makers advise ignition cut in that case.
- Gasoline, ethanol or methanol spark-ignition engines.

## Breaks when
- **Mechanical over-rev.** A limiter only removes power. A missed downshift drives the engine past any limit through the wheels, and no cut prevents it. Some ECUs refuse a requested downshift that would over-rev.
- **Control-range semantics differ.** On some ECUs the entered limit is the end of the soft-cut ramp, so cutting starts one control range (often 200 rpm, or 10 to 20 kPa for MAP) below it. On others the entered value is where cutting starts, and the engine revs into the band above. Combined modes may add a second cut type 100 rpm above the end value. Misreading this either makes the engine "hit the limiter early" or lets it overshoot a mechanical limit.
- **Logged rpm lags the limiter.** A soft cut may act on per-tooth instantaneous rpm while the logged channel is filtered, so cut events can appear below the set limit.
- **Very low inertia.** A very light flywheel can overshoot a reactive limiter; a predictive (rate-based) limit helps.
- **Pre-throttle boost sensor.** Using it as the overboost source picks up the pressure spike on throttle closure, even with a blow-off valve, and can false-trip.
- **Wet nitrous.** A fuel-cut limiter does not stop an engine whose nitrous kit keeps supplying fuel and oxygen; use ignition cut or disarm nitrous below the limit (methodology/nitrous).
- **Software-only travel limits.** Limiting cam phaser travel in software where valves would hit the piston is unsafe, because a solenoid or control fault drives the cam to its stop. Clearance must be checked and the travel limited mechanically.
- **The protection itself is a hazard.** A sudden total power loss mid-corner or on corner exit has caused a following car to make contact in the sources. On track, cut-until-recovered and graded responses can be safer than a full shutdown.
- **Exposure differs by discipline.** A drag car touches cuts a handful of times per run; a circuit car may log more shifts in a single lap than a drag car sees all season, so identical cut settings punish a circuit engine much more.

## Practical use
### Order of setup
1. Before first start: set a sensible rev limit, often temporarily low (practitioner examples range 3500 to 5000 rpm), so a jammed throttle, big vacuum leak or drive-by-wire fault cannot run the engine to redline while oil pressure is still being established. A base map with an absurd limit (10000 rpm on a 6500 rpm engine) is a common trap. Check any limiter turn-on delay is zero.
2. On turbo engines set a conservative overboost cut before the first boosted run. Wastegate plumbing errors are common at first start-up. Raise the limits as tuning proves boost control; forgetting to raise them wastes time on artificial limits.
3. Configure temperature-indexed limits, sensor-fault defaults and global clamps (maximum advance, closed-loop trim authority).
4. Add monitored-fault protections once the logged normal values are known (see the monitored-faults entry).
5. For a fresh build released for break-in, one practitioner sets a temporary rev limit (about 4000 to 4500 rpm) and boost cut for the first few hundred km and tells the driver.

### Rev limiter
- **Cut type.** Default to fuel cut, especially on fragile valvetrains (rocker-type heads known to throw rockers under ignition-cut limiting, shim-over-bucket heads, hydraulic lifters, stock-seal rotaries). Use ignition cut where fuel cannot be cut cleanly (group fire, auxiliary injectors, wet nitrous) or where exhaust combustion is the goal (launch boost building; see methodology/launch-and-antilag). Audit every cut function (main limiter, overboost, launch, gear cut, traction): a rarely hit limiter left on ignition cut has spat a shim in one practitioner's anecdote.
- **Control range.** A soft range of about 100 to 200 rpm, with a randomised (adaptive) cut pattern, gives smooth, accurate limiting and avoids repeatedly cutting (and fouling) one cylinder. A near-zero range acts like on/off control: harsh, overshooting, hard on driveline and belt-driven accessories or superchargers. A very wide range (500 rpm or more) is smoothest but rpm settles below the limit. Four-cylinder engines control more coarsely than V8s because each cut removes a larger torque share. Hard cuts right at a limit suit only classes with a mandated limit where drivers want every rpm.
- **Advanced cut tuning.** Where start and end cut percentages are set: entering the range at full throttle needs more initial cut than at part throttle. Even part throttle may need 70 to 80% cut to hold rpm in one demonstration. With the maximum cut capped under 100% and no hard cut behind it, rpm can simply climb through the limit. So either let the end cut reach 100%, or add a hard cut slightly over the limit, and confirm at WOT.
- **Wide hysteresis.** A factory limiter that cuts at the limit but does not restore until 300 to 400 rpm lower feels like the key was switched off. Shrinking hysteresis gives a smooth hold.
- Test limiter smoothness first at a lower rpm (4000 to 5000), then confirm at the real limit, because behaviour changes.

### Overboost cut
- Set the cut a modest margin above the highest target. Sources use about 10 to 20 kPa; one course example uses 220 kPa delayed and 240 kPa instant for a 200 kPa target. A cut far above target protects nothing.
- Keep activation delay at or near zero (0.1 s at most). With fast-rising turbo boost even 0.1 to 0.4 s lets pressure climb far past safe. A two-level scheme tolerates the normal small overshoot when first reaching target: a delayed threshold for small overshoot, an instant one for gross overshoot.
- Use hysteresis (about 10 to 30 kPa) or a throttle-lift reset so the cut does not cycle at the threshold.
- Where the boost target tapers with rpm or changes with fuel (flex fuel: gasoline versus E85), an absolute cut set for the highest case gives no protection elsewhere. Add a cut relative to the active target. A relative cut needs boost control configured and active, even when running on spring pressure. One practitioner sets a dummy target near spring pressure with zero duty so the relative cut has a valid reference.
- Second layer: put a deliberate steep timing drop in load rows above the highest intended boost (examples: 200 kPa row when running 160 to 170 kPa; about 3 degrees pulled in rows above an achieved 220 kPa peak), so a boost-control failure that stays under the cut still lands in retarded cells.
- Boost from a positive-displacement blower is fixed by its drive ratio and cannot jump to twice the target; a turbo with a detached wastegate line can. Size urgency accordingly.
- An overboost cut that also disables boost control (some ECUs do this) guards against a failed solenoid.

### Temperature-indexed limits (no extra sensors)
- **Rev limit against coolant.** Lower when cold (examples 4000 to 5000 rpm below about 20 C, full limit from about 40 to 60 C), full limit through the normal band, then pulled down above about 105 to 110 C (examples 3000 to 3500 rpm by 110 to 120 C). The sudden low limit feels like a misfire and forces the driver to look at the dash. A street car can still limp home under it.
- **Boost limit against coolant.** Lower when cold (one example 120 kPa at 20 C, 200 kPa once warm), and lower again when overheating. A boost multiplier that falls from 100% at 105 C to about 50% by 115 C reduces heat input subtly, paired with a sharp rev-limit step as the unmistakable backstop.
- **Fuel and timing against temperature.** At high load only, add fuel above the normal coolant range (examples +5% at 110 C, +15% at 120 C above 60% throttle; around 10% is the useful amount, 1 to 3% does little) and retard with high IAT (one example -1 degree at 40 C to -5 degrees at 70 C). A drift-car practitioner pre-populates high-temperature retard on both coolant and IAT before the first outing, because overheating found in logs after a 10 to 20 minute session may be too late.
- **Breakpoint placement.** A thermostatless engine running 65 to 70 C on the dyno sat between a cold cell and the full-limit cell and hit an interpolated limit in a pull. Check where the engine actually runs against the table breakpoints.
- Tell the customer about cold and hot limits, or expect a report of a cold misfire. Respect a customer who declines them, and record it.

### Sustained-load protection
A dyno session or road pull lasts 5 to 10 s of WOT; sustained top-speed runs or long full-load sections heat-soak the chamber and can tip a marginal engine into knock never seen on the dyno. Options from the sources: enrichment and retard indexed on a full-throttle timer (unchanged for roughly the first 6 to 10 s, after which fuel is added and timing removed), on driven-wheel speed (one example +2% to +10% fuel and -2 to -5 degrees from 200 to 240 km/h), on top gear, or on a rolling average of load with a chosen time constant (seconds for sensitive engines, tens of seconds for endurance). Running richer everywhere instead wastes fuel and power.

### Graded responses
Assign each fault a severity matching its danger. Mild: slight enrichment, boost reduction, a few degrees of retard. Moderate: a fuel-cut rev limit around 5000 to 5500 rpm or a throttle cap. Severe: a limit near idle or an engine stop. A limp limit around 3000 rpm lets the driver reach the pits, and is preferred by one practitioner for everything except total oil pressure loss. A modest fuel pressure or lambda error can be met with extra fuel; oil starvation cannot be helped by fuel or timing and needs the load removed. Trigger on current-drive-cycle faults rather than stored history.

### Sensor-fault defaults and global clamps
- MAP fault default near atmospheric (about 100 kPa) so the car can limp. A low default (30 to 40 kPa) runs too lean under load. Flag the sensor outside its plausible voltage band (about 0.1 to 4.9 V). One source substitutes 60 to 70 kPa; the fallback will never be right, only drivable.
- Coolant fault default high enough (about 100 C) that the fans run.
- IAT plausibility bounds with a fixed substitute (one example 25 C).
- Clamp global ignition limits to a sane band (one course clamps to about -10 to +40/45 degrees on a pump-gas engine) so stacked compensations cannot command absurd timing.
- Limit closed-loop authority (one course: ±5% at high load, ±10% elsewhere, ±15% at idle) so a wideband that fails without raising a fault cannot trim the engine into damage.
- Drive-by-wire fault limp limit low but drivable (one source suggests 1600 to 1800 rpm).
- Gear-sensor failure: an ECU with wheel speeds, rpm and gear ratios can estimate the gear as a fallback.

### Dyno-side protection
Use dyno alarms (coolant above about 100 C, rpm-qualified oil pressure) so temperatures are not missed while concentrating. On highly stressed engines one practitioner sets a dyno-side rpm limit and aborts a ramp run once power is clearly below the reference run. There is no need to load the engine to the limiter to learn a change was worse.

## Decision rules
- Start with a rev limit and a boost cut; never start tuning with either absent or absurd.
- Fuel cut is the default limiter mode unless there is a specific reason (fuel cannot be cut cleanly, wet nitrous, deliberate exhaust combustion with a tolerant valvetrain).
- Fill protection-table safe regions with a value well above the main limit (for example 10000 rpm), never equal to it.
- Lower the rev limit progressively with rising coolant temperature; place breakpoints knowing the table interpolates.
- Overboost: small margin, near-zero delay, hysteresis, and a target-relative cut where targets vary.
- Never disable a protection to complete a tune or to stop nuisance trips; find why it trips.
- An oil pressure protection rule of thumb of about 10 psi per 1000 rpm exists for engines with no better data, but logged hot-oil values are better (see the monitored-faults entry).
- Exhaust gas temperature much over about 900 C on gasoline concerns one practitioner; turbine materials are said to suffer above about 950 to 1050 C sustained (see Disputed).

## Data gates
- Protection, limiter and cut-status channels must be logged (active limit, limiter state, ignition and fuel cut %, which protection is active). With several strategies active, the first question after a cut is which one fired.
- Log rpm against the active limit at a fast rate when judging limiter quality.
- Coolant, IAT, MAP and boost target are needed to audit temperature- and target-relative limits.

## Worked example
**Rev limit with a control range.** An engine should not exceed 6700 rpm. On an ECU whose table value is the end of a 200 rpm ramp, enter 6700: cutting begins at 6500 and reaches full cut at 6700. On an ECU whose value is the start of the ramp, enter 6500 with a 200 rpm band. Entering 6700 there would let the engine reach 6900.

**Overboost on a tapered target.** Target 250 kPa to 6000 rpm, tapering to 200 kPa at 7500 rpm. A fixed cut at 260 kPa gives a 10 kPa margin at 6000 rpm but 60 kPa at 7500 rpm, so a wastegate fault at high rpm could reach 255 kPa without a cut. A relative cut of target + 20 kPa trips at 270 kPa and 220 kPa respectively. With fast turbo boost rise of, say, 100 kPa/s, a 0.4 s delay would add about 40 kPa beyond the threshold before acting, while 0.1 s adds about 10 kPa.

**Coolant limit interpolation.** Limit 7500 rpm at 100 C and 3000 rpm at 110 C: at 105 C the limit is 5250 rpm. To hold 7500 rpm to 109 C and then step, add a 109 C breakpoint at 7500 rpm.

## Disputed / conflicts
- **Fuel cut versus ignition cut.** Most sessions and courses (084, 171, 253, 264, 350, 372, 374 and several course lessons) default to fuel cut. An practitioner in 036 and 039 generally prefers ignition cut as immediate and certain, using fuel cut only on fragile valvetrains. Both sides agree on the valvetrain mechanism and on ignition cut where boost building is wanted. The ECU maker's advice for group fire favours ignition cut. Choose per engine; the discriminating question is valvetrain type and exposure.
- **Is fuel cut a lean risk?** A common worry is that the residual port film burns as a lean charge during fuel cut. The sources consistently say the residual film is too lean to burn and that one practitioner has not seen a problem from it in over 20 years. One source adds that the first cycle after a cut may carry a very lean charge. No textbook test is cited; a cylinder-pressure or per-cylinder EGT test during limiter events would discriminate.
- **Hard cut versus safe-in-traffic response.** Sources agree oil starvation must be acted on instantly. They also report a sudden cut on corner exit causing contact from a following car. The positions are reconciled by graded responses, cut-until-recovered rather than shutdown, and fixing the cause (surge), but a fixed answer does not exist.
- **Numeric cross-check.** No textbook in this KB supports the oil pressure rule of thumb or the turbine temperature figures; treat both as practice guides and prefer engine or turbo manufacturer data. Practitioners' EGT ceilings differ: 900 C on pump fuel (60), 950 C (372), 950 to 1000 C (104, 174), 1000 to 1050 C sustained (350). Probe type and location alone shift readings by 50 to 100 C, which explains part of the spread.

## Citations
- practice: Practitioner training and tuning practice, distilled and cross-checked.
