---
id: methodology/dyno-procedure
title: Dyno procedure
layer: L2
status: draft
confidence: high
sources: [practice]
verified: 2026-11-11
applies_to: {fuels: [gasoline, ethanol, methanol], engines: [all]}
depends_on: [methodology/full-load, methodology/data-quality, methodology/steady-state-fuel, methodology/steady-state-ignition]
supersedes: []
---

# Dyno procedure

## Claim
A dyno is a comparison instrument, not a power meter. Its value to a tuner is controllable load (holding a cell for steady-state work), live torque (for MBT and other torque-versus-parameter decisions) and repeatable ramp runs (for judging a change run to run). Every one of those depends on the operator keeping the test state constant: temperatures, tyres, strapping, gear, ramp rate and rpm reference. A difference between two runs means nothing until those are shown to match and the difference is larger than the dyno's own run-to-run spread.

## Why (derivation)
### What the dyno measures
A chassis dyno measures torque at the roller or hub and speed of the roller or hub; power is their product. Wheel torque is engine torque times the overall ratio (gear times final drive) minus driveline losses, while roller speed falls by the same ratio, so the gear cancels out of power to first order. What is left over (driveline friction, tyre deformation, slip) differs between gears, tyres, strapping and dyno designs, which is why absolute numbers differ and only like-for-like comparisons are meaningful. Displayed axle torque is a magnified view of engine torque (multiplied by the overall ratio), which makes it a sensitive indicator of small engine-side changes.

### Load-bearing versus inertia
An inertia dyno has only roller mass: power is inferred from how fast the drum accelerates. It cannot hold an rpm, so steady-state cell tuning and torque-based MBT work are impossible on it; its ramp rate is set by engine power and gear, not by the operator. A load-bearing dyno (eddy-current, hydraulic or electric absorber with a load cell) can hold rpm while throttle varies and can impose a chosen ramp rate. A brake with no load cell gives load but no torque feedback, so it still cannot find MBT.

### Ramp rate changes the reading
During a ramp, part of the engine's torque accelerates the engine, driveline and rollers, so faster ramps read lower and steady state reads highest. A slow, heavily loaded ramp also builds more chamber and charge heat, which is where knock and lean mixtures show up. The sources therefore pick a ramp rate that matches real acceleration in a high gear and keep it fixed.

### Why temperature drifts on a dyno
A dyno cell cannot reproduce the radiator and intercooler airflow of a car at road speed, so coolant, intake and oil temperature climb during sustained load and back-to-back runs. Temperature-dependent ECU trims then start altering the very thing being tuned, and the data no longer represents the road.

## Assumptions
- The vehicle is restrained correctly for its power and drive layout, and the dyno is in good order.
- The tuner has engine data (rpm, MAP, lambda) from the ECU and treats it as the reference for table work.
- The car has passed the pre-tune checks (methodology/pre-tune-checklist).

## Breaks when
- Heat soak on low-airflow cells makes runs not comparable; the first run after a hot restart is unrepresentative.
- A cold car and dyno gain power run after run while tyres, gearbox, differential and the dyno itself warm up; that gain is easily mistaken for a tuning gain.
- Tyre compound, pressure or size change, or strapping changes, alter the loss at the tyre-roller contact by amounts comparable to real tuning gains.
- Wheelspin or clutch slip invalidates a run; converter slip on automatics inflates low-rpm torque and shifts derived rpm.
- The load cell is at the bottom of its range (light load, low power car on a big dyno): torque resolution collapses.
- A poor or faulty dyno drifts when hot, producing phantom losses.
- Some modern cars detect front and rear wheel speeds disagreeing on an unlinked two-wheel-drive dyno and go into a limp mode.
- Very high power cars on rollers become hard to hold without wheelspin; hub dynos are limited by hub torque and hub speed instead.

## Practical use
### Choosing and setting up the dyno
- Use a load-bearing dyno for anything beyond WOT-only work. An inertia dyno suits drag cars and simple WOT power checks; it cannot do part-throttle mapping or MBT. Before hiring a dyno, agree whether you may drive it and whether you must supply the wideband; for table work use the ECU's own wideband channel, not the dyno's.
- Hub dynos remove the tyre contact patch and give the best run-to-run and session-to-session consistency; roller dynos rig faster, and their inertia lets gear-shift cut and downshift functions be tested, which a low-inertia hydraulic absorber cannot reproduce well (eddy-current units sit between).
- Rollers: set every car to one fixed tyre pressure (an practitioner uses about 40 psi; road pressures let sidewalls deform and absorb power). Prefer hard road tyres; slicks and soft compounds read lower, overheat and can fail. Do not run tyres with cords showing; inspect the inside edge on cars with a lot of negative camber. Gross misalignment makes the car pull and scrub on the rollers.
- Strapping on rollers: strap downward close to the axle line so straps tighten as the wheel climbs onto the drive roller; rearward straps fight that climb, cut traction and promote wheelspin. Over-tight straps read low and inconsistent. In the sources, cars below roughly 200 to 250 kW at the wheels are held by chocks with light straps as backup, and strap tension is made repeatable by a fixed routine (pull tight, release, then snug plus one click). Leave a gap between chocks and tyres so the car can move forward.
- Hub dynos: on a spool only, select a common-axle mode; open and limited-slip differentials need independent hub control, and poor left-right speed control can hurt a clutch-type differential over a session (one practitioner's experience). Bring the locking wheel nut key.
- Gear: use a gear near 1:1 (typically 4th, or 4th or 5th in a six-speed). Lower gears multiply torque at the tyre and promote wheelspin; taller gears may exceed the dyno speed limit. Use the same gear for every comparison. If the dyno needs the overall ratio entered to hold rpm, update it whenever the gear changes.
- Rpm reference: give the dyno a real rpm signal (from the ECU over CAN or an ignition pickup with the right pulses per revolution). Derived rpm from roller speed cannot reveal wheelspin or converter slip, and if calibrated at light load it reads off under WOT because the tyre grows and deforms; if derived rpm is unavoidable, calibrate it at moderate rpm under heavy load. Treat ECU rpm and MAP as truth when relating events to table breakpoints; dyno end-rpm overshoot and small rpm offsets are common.
- Automatics: fix the gear before any run (manual mode, or command a gear with a scan tool). Kickdown ruins the run and on a powerful car causes wheelspin. On boxes that kick down regardless, start the ramp at a throttle just below the kickdown point and roll smoothly to full throttle once past the rpm where kickdown stops, identically every run. With a loose or high-stall converter, start near lock-up to limit slip heat; even a commanded lock-up still slips somewhat.
- Two-wheel-drive modern cars that go into limp mode on an unlinked dyno need a factory dyno mode, front wheel speed spoofing, or a linked dyno.
- MAF engines: check whether the cell fan disturbs the MAF before tuning idle and cruise (see diagnostics below); shield the intake from the fan blast if it does.
- Configure the rev limiter and an overboost cut before the first run; a sticking throttle or boost fault can otherwise send the engine to the limiter or overboost on run one. On an inertia dyno the rollers keep accelerating while the throttle is open, so an ECU rev limit at the intended end rpm is the run's stop.
- Keep records per vehicle: operator, gear, tyre make and size, pressures, strapping and file location. Without them a returning car can appear to have lost power for setup reasons.

### Warm-up and repeatability
- Bring the whole vehicle to temperature, not just the coolant: gearbox, differential and tyres. Several unchanged back-to-back runs (four or five in one source) until results overlay are the baseline; cold sessions commonly gain several kW over the first two or three runs.
- Oil temperature can matter more than coolant for repeatable power on some engines; in one practitioner's tests power barely moved over a 20 to 30 C coolant window but some engines were down until oil reached about 100 C.
- Turbo cars: precondition the exhaust and turbo with a short period of light load or a few seconds at full throttle before each ramp. A cold manifold and turbine spool later, which inflates or hides low-rpm differences between runs.
- Discard the first run after a hot restart and the runs during start-up enrichment; evaluate only once post-start enrichment has ended and closed loop is active.
- Start every comparison run at the same coolant, intake and (where it matters) oil temperature, with the same tyre pressures and boost.
- Know the dyno's spread: if unchanged runs vary by a few hp, smaller gains cannot be confirmed. A sensitive dyno will show the alternator load of the headlights switching at steady state (one practitioner's test); a dyno built for very high power loses resolution on low-power cars.

### Thermal management
- Watch coolant, intake air and, if fitted, oil temperature and pressure continuously; set an on-screen warning for coolant (the sources use about 100 C). It is easy to become absorbed in a cell and miss them.
- Return to idle with the fans running to recover between columns or runs. Work faster at high rpm and load, and avoid long steady-state holds at high rpm and boost on powerful engines; ramp runs cover that region.
- Turbo cars: the intercooler heat-soaks on sustained load. Spraying water on the intercooler between runs with the fan on is the sources' method for keeping intake temperature consistent.
- For an NA car, tune with the bonnet open (fans cannot match road airflow) and then use closed-bonnet back-to-back runs, or a temporarily blocked intercooler on a turbo car, deliberately to raise intake temperature and test the intake temperature compensation (watching coolant, since radiator flow is cut as well).
- Larger cell cooling and extraction fans keep conditions consistent and reduce cool-down stops; extract exhaust for the operator's health as much as for power readings.

### Steady-state technique
- Use throttle to move through load and the dyno set point to hold rpm. On rollers, rpm creeps up as load rises (tyre deformation, the car moving forward, slight slip), so trim the speed target down each time throttle opens, or use an engine-rpm control mode, to stay on the cell centre; off-centre corrections land on interpolated cells.
- WOT cells are easiest to hold (the throttle cannot wobble); part-throttle cells suffer from foot movement and MAP oscillation.
- Start a fresh map at low rpm and low load, where events are slow and errors cause little harm, work up each column, then copy the finished column forward as the start for the next.
- The dyno has a load floor: below a certain throttle the engine cannot drive the roller and rpm sags instead of load falling. The floor drops as rpm rises. To go lower, use a shorter gear (more wheel torque for the same engine torque) at a lower roller speed, or briefly raise rpm and drop the throttle back into the cell to read lambda before the dyno drags rpm down. Extrapolate what still cannot be reached and confirm it on the road (methodology/road-procedure).
- On automatics at low rpm the converter flares, so the operating point moves diagonally up and right rather than up a column; tune along that path, come back for skipped cells, and extrapolate the unreachable low-rpm high-load cells (the car cannot operate there on the road either).
- Read torque from a scrolling trace, not a numeric gauge. Type the new value, then commit it in one step while watching the trace, so the step change is attributable; repeated small taps smear the change over time. If unsure, toggle back and forth.
- At the bottom of the load cell's range the trace wanders and spikes. Use bigger timing steps (one demonstration used 5 degrees instead of 2) so the response rises above noise, read the averaged trend, and when nothing clear shows, prefer slightly conservative timing. Supporting cues are smoother running and sound as timing improves. Fill the lowest cells from trends in cleaner cells.
- Torque-versus-parameter sweeps (ignition, cam angle, injection timing, lambda): settle in the cell first, set surrounding cells to the same start value so interpolation does not blur the result, hold the throttle absolutely still, and sweep slowly (about 1 unit per second in the sources). Read the trend, not individual blips; peaks and troughs often come from MAP wobble. Sweeps take most of a minute, so use them for four to six anchor cells and as a sanity check, and tune the rest from the live trace.
- Light-load cruise MBT and economy work are the hardest tests to do accurately on a chassis dyno because torque is so sensitive to tiny throttle movement; average noisy data.

### Ramp runs: what to watch and when to abort
- Nobody can scan a dozen channels during a run. Graph lambda and power, plus MAP on boosted engines, with limit lines (lambda band, boost ceiling) so one glance answers "abort or continue". While boost builds, watch boost only; return to lambda once it stabilises. Slow-updating displays (around two updates per second) are useless during a ramp.
- Overlay the live run on the previous run. A power curve that noses over with no explanation is a reason to abort even if lambda and MAP look fine: in one practitioner's account a failing bearing showed only as lost power.
- Hover over the clutch for every full-power run. Abort by lifting and dipping the clutch at the first unacceptable reading, audible knock or mechanical noise; never brake abruptly during a run. There is no obligation to finish a run.
- Use a lead-in below the logged start (the sources use about 250 rpm on a hub dyno) and ignore the torque spikes at the start and end of the ramp, which come from the dyno holding or clamping the engine.
- Plot against engine rpm, not road speed. Name and save each run with notes so runs can be overlaid; clear older runs and overlay only the comparison run.
- Start runs where the engine and car realistically accelerate (the sources use about 1500 to 2000 rpm), not at very low rpm where engines dislike load.
- Ramp details, extension steps and correction rules: methodology/full-load.

### Diagnostics on the dyno
- Wheelspin versus clutch slip versus normal drift: plot engine rpm (real, not derived) against roller speed. A gentle, steady drift of the ratio over a run is normal tyre growth and the car climbing the roller; a sharp kink, usually near peak torque or spool, is slip. Clutch slip looks the same in the data; wheelspin leaves rubber in the bay. Automatics show converter slip until lock-up.
- Small gain with no relevant change: a power rise after an edit that should not affect power (for example a fuel-only change with lambda already on target) points to driveline warm-up, a fixed boost leak or another incidental cause, not the edit.
- Power loss after a pause: check whether a temperature-based lambda target or trim changed the mixture before blaming the change under test.
- Boost drifted between runs: different peak boost puts the engine into different cells, so lambda changes may not be from the edit.
- Fan-sensitive MAF: warm up with the fan off, note trims, switch the fan on; a sharp lean or trim jump means the fan blast is disturbing the meter.
- Graph sanity: in hp and lb-ft the power and torque curves must cross at 5252 rpm; if not, the setup or display is wrong. A channel that shows nothing may have units that do not match the graph scale. A jagged torque curve may only be a zoomed axis.
- A nitrous activation spike-and-dip on some hub dynos is load-control overreaction, not engine behaviour.
- If the dyno itself is unreliable (readings drift hot, phantom losses), stop the session rather than tune against it.

### Where steady state ends
Steady-state work replicates how the engine is actually used: cruise and light load really are steady, but WOT at low and mid rpm always accelerates, so WOT is finished with ramp runs. Most precision goes into idle, off-idle transitions and the cruise band; high-rpm part-throttle cells are only passed through and need ballpark values. Steady-state to about two-thirds of the rev limit is typical in the sources (see methodology/tuning-order).

## Decision rules
- Never touch the brake pedal hard during a dyno run; abort with throttle and clutch.
- Check temperatures between runs, and start every comparison run from the same temperatures, tyre pressures and boost.
- Longer ramps put more load and heat into the engine and test thermal margin.
- Tyre deformation on a rolling road makes high-torque data less consistent, so compare like with like.
- Stay at the cell centre during steady-state work.
- Judge a change only if it repeats and exceeds the unchanged run-to-run spread; trust repeatability over a single comparison.
- Change one variable at a time between comparison runs.

## Data gates
- Run-to-run temperature comparable (coolant, intake air; oil where the engine is sensitive to it).
- Torque repeatability better than the size of the change being judged.
- Engine-rpm to roller-speed ratio free of kinks for the run to count.
- Torque well above the load-cell floor before a torque-based MBT decision is made.

## Worked example
Two pulls differ by 8 kW, but the second started 15 C hotter. The difference cannot be attributed to a tuning change.

A second case modelled on a training demonstration: a timing increase shows a small peak-power gain on the summary. The live overlay of the two runs lies on top of the baseline through the whole rpm range, and three unchanged runs earlier spread by about the same amount. The gain is run-to-run variation, so the added timing is removed. In a different demonstration, a 2 degree reduction looked like it changed nothing, but restoring it brought back a small gain that repeated twice with no knock; there the timing was kept. The rule in both cases is the same: decide on repeatability, not on one pair of runs.

## Disputed / conflicts
- Absolute numbers between dynos: one practitioner quotes his dyno as reading about 10 % below another common brand. Other practitioners treat any such conversion as meaningless because brand, operator, strapping, ramp rate and gear all change the result; compare only on one dyno. See methodology/dyno-correction.
- Tyre change size: two sessions report different losses for a road-to-semi-slick tyre swap on similar cars (about 8 kW in one, 10 to 15 kW in the other). Both agree on direction; the size depends on car, power and tyre.
- Knock during a run: the default is to abort and correct. One practitioner's view is that on a low-power, robust engine he knows well, a couple of momentary light events may not require aborting; on high-power engines or with sustained knock, abort at once. The KB keeps abort as the rule (methodology/knock-assessment).
- Which temperature controls repeatability: most sources key on coolant and intake air; one practitioner's dyno tests found oil temperature mattered more than coolant on two engines. Discriminating test: unchanged runs at fixed coolant with oil temperature varied, and the reverse.
- How much restraint a roller car needs: chocks alone below about 200 to 250 kW at the wheels is one practitioner's practice on one dyno type; it is not a general safety limit.

## Citations
- practice: Practitioner training and tuning practice, distilled and cross-checked.
