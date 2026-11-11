---
id: methodology/engine-protection-monitored-faults
title: Protection from monitored faults (oil, fuel, lambda, EGT, coolant)
layer: L2
status: draft
confidence: medium
sources: [practice]
verified: 2026-11-11
applies_to: {fuels: [gasoline, ethanol, methanol], engines: [all]}
depends_on: [methodology/engine-protection, methodology/wideband-sensors]
supersedes: []
---

# Protection from monitored faults (oil, fuel, lambda, EGT, coolant)

## Claim
Cheap sensors (oil pressure, fuel pressure, wideband lambda, and on stressed engines EGT and coolant pressure) let the ECU detect the faults that kill engines fastest and act automatically. Each threshold must follow the variable's normal behaviour (oil pressure with rpm and temperature, fuel pressure with boost, lambda with target and load). Each delay must be shorter than the time the fault takes to cause damage but longer than the normal transients and the false readings created by cuts. Thresholds come from logged normal values under the hottest realistic conditions, not from a gauge rule or cool dyno data.

## Why (derivation)
- **Oil pressure** rises with rpm (pump flow) and falls as oil heats (viscosity). A single switch threshold must sit below hot-idle pressure (one example: a hot engine idling at about 15 psi at 850 rpm, so the switch is near 10 psi). By the time pressure at 6000 to 7000 rpm falls below 10 psi, the bearings are probably already damaged. An rpm-indexed minimum is the only threshold meaningful at both ends. Oil loss gives almost no time: one practitioner considers a second at 6000 rpm and boost enough to ruin bearings, and knows of a failure linked to a default delay of about a second. Fuel or timing changes cannot help oil starvation; only removing load does.
- **Lean mixture** damages at high load and rpm, mainly where rich power targets are commanded. Lean cruise or idle causes misfire or stalling, not damage. So lean protection needs to be armed only under real load, and a rich excursion is not a short-term threat.
- **Any cut corrupts exhaust lambda.** Ignition-cut shifts, launch limiters, rev limiters, overrun fuel cut and transients all pass oxygen (and fuel) past the sensor, which reads lean. A lambda protection without a delay or event gating will trip on every flat shift.
- **Fuel pressure** on a manifold-referenced system follows boost, so the threshold must too. Normal transients (pressure spike on lift at high load, dip on tip-in as boost rises) are typically 20 to 30 kPa for 0.2 to 0.3 s in one practitioner's experience.
- **EGT** climbs very quickly once something goes wrong, as seen in logs from engines lost at the drag strip.
- **Coolant pressure** sits near the radiator cap rating in normal running. Combustion gas entering the water jacket (head lift, gasket failure) makes it climb sharply, often late in a high-boost pull. Absolute value says little; the change is the signal.

## Assumptions
- Sensors are fitted, calibrated, plausibility-checked and logged at a useful rate.
- The ECU can index a limit or protection on arbitrary channels (generic rpm-limit tables, math channels for lambda error, or a dedicated protection function).
- Thresholds are populated from logs of the actual engine.

## Breaks when
- **Dyno oil temperature is lower than track.** A dyno with a big fan on the radiator and oil cooler often sees 70 to 100 C oil; several hard laps on a hot day reach 120 to 130 C. Drawing the minimum line only 5 to 10 psi below a dyno trace invites false cuts after a few hot laps. Conversely, a cold-oil check overstates normal pressure.
- **Cut events read lean.** Launch control and ignition-cut shifts cause false lean readings; protection must be bypassed or delayed through them.
- **Sensor failure.** EGT probes are fragile. A failed probe usually reads nonsense (often negative), but one that fails high triggers protection and fruitless fault-finding. A wideband failure should usually warn rather than stop the engine.
- **Crankcase pressure as a trigger.** On a drag engine a sharp rise usually arrives after a piston has failed, which is too late to save anything. Crankcase pressure is better as a long-term trend of ring wear. Coolant-pressure head-gasket monitoring gave mixed results for one practitioner on milder engines, since a leaking gasket tends to reveal itself in other ways first.
- **Pre-ignition.** At very high specific output on methanol it cannot practically be detected and destroys the engine almost at once. It must be designed out (oil control and type, avoiding charge dilution), and conservative tuning leaves a margin.
- **Single warning lights** tell the driver something is active, not what. Passive warnings fail when racers ignore them.

## Practical use
### Oil pressure
- Build a minimum-pressure table against rpm (and against oil or coolant temperature where available). Fill it from a logged run at hot operating temperature, then set the line modestly below; confirm against hot track logs before finalising.
- Practitioner examples: a minimum of 100 kPa at 1000 rpm climbing to 300 kPa by 8000 rpm; roughly 100 kPa near idle and 300 kPa from 5000 rpm up; and a 25 to 30 psi trip point at 4000 rpm on an engine that normally shows about 40 psi there. One logged engine showed about 220 kPa at 1600 rpm, 475 kPa at 4000 and 600 kPa at 6300.
- Set the response to the severest level: a limit near idle (practitioner examples 0 to 3000 rpm, with 2000 rpm common), effectively removing load from the bearings. A limit only bites if it sits below the rpm the engine is already at, so where pressure falls at low rpm the limit has to be lower still. Leave a margin between the dash warning line and the cut line.
- Delay: zero or very short (0.1 to 0.2 s). Use a start-up lockout or a minimum run time (about 2 to 5 s) so cranking and pressure build-up at start do not trip it; or enable only above about 1500 rpm so a low hot-idle pressure is allowed.
- No throttle or MAP precondition: zero pressure is dangerous at any load (a dry-sump belt failure, a broken pump gear, a lost drain plug).
- A maximum pressure limit (one example 9 bar) can catch cold-oil overpressure from hard revving on a winter start.
- On track, prefer cut-until-pressure-recovers over a shutdown that needs a restart. Brief the customer that hesitation in hard corners means oil surge. Factory wet sumps cannot cope with sustained 1.5 to 2 g on slicks, and cars with marginal oil systems have hit the cut two or three times a lap, worse late in a session. The fix is the oil system (baffling, accumulator, dry sump), not a looser line. Surge from road-car sumps on track is the bearing-failure cause one practitioner meets most often. At minimum, fit and log oil pressure even if no cut is used.
- Because oil warms roughly in step with coolant, a separate cold-oil limit adds little over the coolant table. Use oil temperature for over-temperature protection with a gentler response and a longer delay (one example: warn near 120 C with a 5000 rpm limit and 5 s delay; another keeps the full limit up to 130 C, then 5000 rpm there and 3000 rpm by 140 C). Good synthetic oil tolerates a few degrees over; rotary engines are far less tolerant and need a lower alarm. One practitioner prefers 110 to 115 C race oil temperature and avoids exceeding 130 C. A regularly hit limit means an oil cooler is needed.

### Fuel pressure
- Returnless systems: limit when pressure falls well below normal (one example: a 3.5 bar returnless system that normally drops near 3.3 bar when revved hard, protected below 2.5 bar).
- Manifold-referenced systems: protect on differential pressure, or index the threshold by MAP. One practitioner permits a 50 kPa shortfall against a 350 kPa nominal, held for 0.5 s, before acting.
- Use hysteresis so it does not chatter, a short delay to ride through the 0.2 to 0.3 s transients, and a limp limit around 3000 rpm. Low pressure at light cruise mostly leans the engine harmlessly; the danger is surge at high rpm and load in a corner, which the limit caps.
- An ECU that compensates pulse width for measured fuel pressure tolerates a larger drop if injector headroom exists. None of this substitutes for an adequate fuel system.

### Lean protection
- Arm only under real load. Examples from the sources: above about 3000 to 4000 rpm with 80% throttle; above 160 to 180 kPa MAP in boost; above 100 kPa and 50% throttle.
- Compare measured lambda with target rather than a fixed value where possible. Make the allowed error a table: roughly 5% lean of target where the target is 0.78 to 0.80, very loose (effectively off) near lambda 1, large in vacuum, tight in high boost. Without a target comparison, index on measured lambda and throttle or MAP (one example: no limit at 0.90, interpolating to a 3000 rpm limit at lambda 1.0 above 80% throttle).
- Delay: long enough to ride through logged shift-cut and transient spikes, short enough for the engine's damage time. Measure the spike length from logs before arming. On a very high specific output engine, shorten it; one second lean at 3 bar can be catastrophic.
- Bypass or gate it during launch control and gear cuts. One method indexes the lean protection table by launch status, so the limit becomes unreachable while launch is active.
- Response: warn, or a moderate limit (examples 3000 to 5000 rpm). One practitioner uses a short delay, escalating from a soft cut to a full cut if the lean reading continues. Normal driving below the limit rpm then never nuisance-trips.
- With closed-loop control at full load, short-term trim held past about ±5% for some time is an alternative trigger that naturally ignores brief shift cuts.
- Direct lambda monitoring catches a lean condition from any cause (pump, filter, injector, running out of fuel), which indirect fuel pressure monitoring does not.

### EGT
- Fit a pre-turbine probe on turbo engines; on engines at their limit, per-cylinder EGT matters because normal cylinder-to-cylinder distribution may leave a single cylinder lean enough to be lost.
- Practitioner ceilings for pump fuel cluster around 900 to 1000 C, with a short delay. A default of 1500 C was called far too optimistic. Per-cylinder shutdown around 1000 C appears in one source. Turbo rotaries routinely run around 900 C. Methanol runs much cooler.
- No single safe number exists: probe location (flange versus collector, centre versus wall) shifts readings by 50 to 100 C. Sheathed probes survive far longer than exposed-junction types but read somewhat lower and react more slowly.

### Coolant, crankcase and other channels
- Coolant pressure: a reading more than about 5 psi over the cap rating, or a near-vertical climb late in a pull, indicates head lift. Log it first, because normal variation is larger than people expect. A coolant pressure that has not risen at all a couple of minutes after a cold start points to a major leak or a dry system. On high-boost builds where gasket sealing is the limit, an ECU shutdown strategy (perhaps referenced to boost) is warranted.
- Crankcase pressure and oil analysis: log and trend to schedule ring and bearing refreshes. Compression tests compare cylinders, not absolute values.
- Turbine speed: if fitted, cut at the turbo maker's maximum speed.
- Charging failure: if voltage remains under roughly 12.5 V while running (normal 13.8 to 14.2 V), shed non-critical loads to reach the pits.
- Water-methanol or nitrous dependence: if the tune relies on the spray (less fuel, more timing, more boost), loss of spray leaves it lean, over-advanced and over-boosted. Wire the kit's failsafe, level, pump-fault and ideally flow outputs into the ECU, and on a fault remove the offsets, drop to wastegate boost and warn (methodology/water-methanol-injection).

### Driver warnings
- Keep ECU protection and dash warnings independent; the dash warns, the ECU acts.
- Show the live value in the warning message, not the trigger value. Zero oil pressure means switch off now; a momentary surge may allow limping to the pits.
- Prioritise: oil pressure highest, then coolant temperature (faster moving), oil temperature, lambda and fuel pressure, then drivetrain. Never let a minor warning take over the shift light.
- Escalating temperature warnings (raise the trigger a step after each reset, a limited number of times, fall back after a quiet period) stop a marginal cooling system distracting the driver without silencing it.
- Log every warning and protection state so the cause can be found after the session.
- On a catastrophic failure, the driver should kill the ignition and press the clutch at once; otherwise the drivetrain keeps turning the engine and spreads debris.

## Decision rules
- Oil pressure, fuel pressure and lambda sensing are cheap compared with an engine; one practitioner treats them as non-negotiable.
- Oil pressure protection: rpm-indexed minimum from hot logs, near-zero delay, start-up lockout, severest response, no load precondition.
- Lean protection: armed only at high load, target-relative, delayed past logged cut spikes, bypassed during launch, warn or moderate limit.
- Gentler, slower responses for slow-acting faults (oil temperature), fast and severe for fast ones (oil pressure, fuel pressure loss under load).
- Use the old guide of roughly 10 psi for each 1000 rpm only when no logs exist.

## Data gates
- Oil pressure, oil temperature and rpm logged together; at least one hot-oil track or road log before the line is finalised.
- Lambda, lambda target, MAP, throttle and every cut channel (shift, launch, limiter, overrun) logged together for sizing the lean delay.
- Fuel pressure (differential if referenced), MAP and injector duty logged together.
- Protection status channels for every strategy.

## Worked example
A track engine logs hot oil pressure of 150 kPa at 1000 rpm, 330 kPa at 4000 rpm and 450 kPa at 7000 rpm with oil at 125 C. Set the minimum line at roughly 70% of these: about 100, 230 and 310 kPa. Cells below the line get a 2000 rpm limit; cells above get 10000 rpm. Set a 3 s run-time lockout and zero delay. A brief surge to 200 kPa at 6000 rpm in a long corner now cuts power until pressure returns. By contrast, the dyno trace at 95 C oil read about 520 kPa at 7000 rpm; a line set 35 kPa under it (485 kPa) would trip in normal hot running at 450 kPa, which is the nuisance-trip trap the sources describe.

Lean delay: logged flat-shift lean spikes last 120 to 250 ms; set the delay to about 400 to 500 ms, and on a very high output engine accept a shorter delay with shift-event gating instead.

## Disputed / conflicts
- **Oil pressure delay.** Most sources want zero to 0.2 s with a separate start-up lockout. One live training session used about a 2 s activation delay with a 20 s start-up lockout on an NA engine while first building the table from data, and another source allows about 100 ms if minor fluctuation must be tolerated. Discriminating evidence: logged surge duration against bearing damage; most practitioners cite failures from delays of about a second.
- **Lean protection delay.** Values range from 100 to 200 ms (253), about 0.5 s (042, 264), 0.5 to 1 s (039), 700 ms (372), about 1 s (a drag-car live training session) to 2 s for a throttle-indexed version (036). All agree it must exceed logged spike length and shrink for engines that fail quickly.
- **10 psi per 1000 rpm.** Widely quoted as a rough guide; one practitioner (039) considers it outdated for modern engines on thin oils. Logged data supersede it either way.
- **EGT ceilings** differ between practitioners, partly explained by probe type and position; see methodology/engine-protection.
- **Coolant pressure value.** One session (042) found head-gasket monitoring by coolant pressure of mixed value; others (140, 193, 372) rate it as an early warning on high-boost drag engines. The difference tracks how marginal gasket sealing is on the build.

## Citations
- practice: Practitioner training and tuning practice, distilled and cross-checked.
