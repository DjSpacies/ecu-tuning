---
id: methodology/cam-control
title: Cam control tuning
layer: L2
status: draft
confidence: medium
sources: [practice, engineering-texts]
verified: 2026-11-11
applies_to: {fuels: [gasoline, ethanol, methanol], engines: [all]}
depends_on: [principles/airflow/volumetric-efficiency, principles/control/feedback-and-pid, methodology/closed-loop-fuel]
supersedes: []
---

# Cam control tuning

## Claim
Variable cam timing (continuously phased or two-position switched) is a further airflow axis. The tuner finds, by measured torque, the cam position or switch point that traps the most air at each speed and load. Fuel is then fitted to that airflow, and ignition last. Any later cam change makes the VE table wrong again, so the order of work and the way cam changes are judged decide the result.

## Why (derivation)
### Valve events and charge inertia
Real valve events do not line up with TDC and BDC. The exhaust opens before BDC to blow down cylinder pressure, and closes after TDC. The intake opens before TDC and closes after BDC, so both valves are open together around overlap TDC. A phaser moves the whole lift curve; it does not change lift or duration.

The intake charge has mass, so it carries momentum that grows with port velocity. At high rpm the moving column keeps filling the cylinder after BDC, so a later intake closing (intake retarded) raises VE. At low rpm the momentum is small, and a late closing lets the rising piston push charge back into the port, so an earlier closing (intake advanced) fills better. The combustion textbook and an automotive handbook give the same result: inlet closing sets the trade between low-speed and high-speed filling. This is why the intake cam usually has the larger torque effect, and why many engines phase only the intake.

### Overlap and exhaust pressure
Advancing the intake, or retarding the exhaust, adds overlap. When exhaust pressure at overlap is lower than intake pressure, overlap scavenges residual gas and raises filling, mostly at low and mid rpm. When exhaust back pressure is high (rising with rpm, or with a small turbine housing) exhaust gas flows back into the cylinder during overlap and displaces fresh charge, so the engine wants less overlap. At light load, overlap acts as internal EGR. That cuts pumping loss and NOx, which is why factory maps often add overlap at cruise for emissions and economy rather than torque.

### What trapped air does to fuel and spark
More trapped air needs more fuel for the same lambda. On a speed-density model the ECU cannot see the extra air, so a cam move that raises VE shows as a lean shift (or as closed-loop trim adding fuel). A cam move that lowers VE shows as a rich shift. On an air-mass-meter model the meter sees the change and lambda stays roughly put. Cam position also changes how fast the charge burns and how close the engine runs to knock, so the best ignition timing moves with the cam.

### The actuator
Most continuously variable systems use a vane phaser driven by engine oil. An ECU solenoid, typically pulsed at a few hundred hertz, sends oil to one side of the vanes. A cam position sensor closes the loop. Authority is typically 30 to 50 crank degrees on factory engines with mild cams. Oil pressure and viscosity set how fast and how well the phaser tracks. At idle, with low oil pressure, and with cold, thick oil, it is slow and erratic. Lobe-switching systems (VTEC-type) and two-position phasers are oil-switched on/off devices with no position feedback.

## Assumptions
- Cam position tracks its target (checked in the log) before any target is judged.
- Torque is measured on a load-bearing dyno. Street tuning of cam timing is close to impossible, because near the optimum a 5 to 10 degree move changes torque but barely moves lambda.
- The fuel model is known: speed-density (lambda or trim shows airflow change) or air-mass metering (it does not).
- The engine builder has confirmed valve clearance across the full phaser range for any modified engine.
- Ignition is in a knock-safe state while cams are explored.

## Breaks when
- **Modified valvetrain**: aftermarket cams, pistons or skimmed heads can let a valve hit a piston, or one valve hit another, at a phaser extreme. Factory engines are designed with no contact across their range; modified ones are not. The phaser can go to either end on a control or mechanical fault, so software limits are not protection. Dynamic effects (chain stretch, rod stretch, piston rock, exhaust valve float) take up clearance that a static hand-turn check shows as present.
- **Aggressive race cams**: these cannot be phased as far as mild factory cams. Narrow-band race engines often lock the cams or use fixed adjustable gears instead, because phasing adds little over a 7000 to 10000 rpm band.
- **Switched systems**: VE changes in a step at the changeover, so interpolation across the switch is wrong (see Practical use).
- **Unreachable targets**: a target beyond mechanical travel holds the cam on its stop with a constant error. The integral term winds up, and the cam then lags for a second or more when the target comes back into range.
- **Cold oil, idle and lockouts**: tracking is poor; a temperature lockout parks the cam while the VE table was tuned with it moved.
- **Hardware changes**: a new turbo, exhaust or intake can move the optimum. There are no universal cam numbers.
- **Air-mass metered engines**: the lean-shift indicator does not apply.
- **Partial control**: an ECU that controls only some of the engine's phasers (for example intakes only, exhausts locked) gives up some of the factory behaviour, such as boost response.

## Practical use
### Before mapping targets
1. **Confirm the control mode and I/O**: choose the mode that matches the cam wheel pattern and the actuator layout (single intake, dual, or one per bank on a V engine). Check the ECU has enough inputs and outputs for every controlled cam. VVT engines are in practice tied to the factory trigger pattern, because it also carries the cam angle.
2. **Zero the cam reading**: with the cams at rest (solenoids unplugged, a cam test mode, or an automatic stop-learn routine), set each cam's offset so it reads zero. Do this even on plug-in ECUs, since factory tolerances vary; it is the cam equivalent of setting base timing. In a tooth-angle test, readings that jump around mean the wrong test count. The right count gives stable readings.
3. **Know the number convention**: table values are degrees moved from the rest stop (intake rest is usually fully retarded, exhaust rest fully advanced, which gives minimum overlap). They are not cam-card centreline figures. Sign conventions for exhaust cams differ between ECUs. Do not convert; move the cam and judge by torque.
4. **Prove the controller**: start from the ECU maker's gains for the engine. Step the target (for example 0 to 10 degrees) and blip the throttle while logging target, actual (per bank), and solenoid duty. Tune P, I and D only if it does not track. One practitioner demonstration needed more derivative gain to stop oscillation around target. Feed-forward (hold) duty can be found with warm oil at a fixed mid rpm by sweeping duty until the cam neither advances nor retards. It is often near half duty but not universal, and each bank may differ.
5. **Find the travel limit**: command a target past the expected range and note where actual stops. Clamp every table value inside it.
6. **Match the load axis**: the cam target table must use the same load variable as the VE table (MAP with MAP, throttle with throttle). Otherwise one fuel cell can see different cam angles, worst on a turbo engine where MAP at a given throttle changes as the turbo spools. Breakpoints need not match, and the cam table can be coarser.

### Order of work: two accepted routes
- **Cam first, fuel tracked**: set ignition conservatively, map the cams while closed loop (or manual correction) holds lambda, fold the trims into VE, then optimise ignition.
- **Fixed-cam base first**: tune fuel and spark with the cam at rest (or switched cam held off), then add cam advance in broad steps. The change in fuel demand at each step is itself a measure of airflow gain. Then retune VE and revisit spark. The sources note that more intake advance often makes the engine less knock sensitive, so spark may go up slightly afterwards. One demonstration also showed knock warnings appearing as VE rose, so watch for both.
- Either way, at part throttle, put realistic cam targets in before the final VE calibration so later cam changes do not undo it.

### Steady-state optimisation (cruise and part load)
- Hold rpm and load in the centre of a cell, enter a new cam value, and read torque the moment it changes (dyno torque wanders, so the immediate response is what counts).
- Step about 10 degrees, keep going while torque rises, back off when it falls, then bracket in 5 degree steps. A large torque change means you were far from optimum; a small one means you are on the plateau.
- Restore target lambda before judging. One practitioner example: an intake move first looked like a torque loss, but lambda had gone about 6 to 10 % lean. Once fuel was corrected, torque was well above baseline.
- Effects shrink at very light load, where a 10 degree move changed torque by only a few percent in one demonstration. Use the lambda shift as a second cue there.
- Optimum advance generally falls toward lower load on a given rpm row and changes smoothly. Tune anchor sites and interpolate. Use a lower gear or interpolate for cells the dyno cannot hold.

### WOT optimisation (ramp runs)
- Set the whole WOT region to one cam value, make a named run, and repeat in 10 degree steps (0, 10, 20, 30, 40, within travel). Overlay torque (more sensitive than power) and logged cam position.
- Build a composite row from the angle that wins in each rpm band. Typically there is lots of intake advance low and mid, tapering toward rest at high rpm. Smooth it and confirm with a final run that should equal or beat every fixed-angle run.
- Refine an existing map by shifting the WOT region by plus and minus about 5 degrees. Keep a change only in the band where it helped.
- Large trims at WOT can make lambda look correct while hiding a big VE error. Read the trim, not just lambda.

### Dual cams
Optimise the intake with the exhaust held at rest, then the exhaust (which effectively sets overlap), then bracket the intake again, and try moving both together. Then finalise fuel and ignition. On a single camshaft carrying both lobes, or a cam-in-block engine, only phase moves and overlap is fixed. When a fuel model offers a table per intake/exhaust combination, only the combinations that physically occur need tuning.

### Shape and drivability
- The phaser is hydraulic and cannot follow big steps over a narrow rpm span, especially in fast low-gear acceleration. Avoid adjacent cells far apart (5 next to 35 degrees) and zig-zags. Add breakpoints where the optimum genuinely changes fast, and accept a few Nm less for a trackable, smooth map.
- Keep targets at or near rest below about 1000 to 1500 rpm and at idle. Rest gives minimum overlap, good vacuum and smooth idle, and oil pressure there is too low for accurate tracking. One demonstration stalled the engine with 40 degrees intake advance at idle.
- With aftermarket cams that have steep ramps, avoid swinging the cam between rest and full advance on every throttle lift. One practitioner holds a constant part-throttle target to spare the chain and tensioner.

### Turbo engines
The method is the same. Overlap wants to be reasonable mid-range and reduced where exhaust back pressure is high. Optimising for torque raises airflow and so helps spool without a separate spool strategy. Develop targets at moderate boost, then check at higher boost with a 2 to 5 degree sweep each way.

### Switched (two-position) systems
- **Classify first**: a two-position oil-switched phaser with no position feedback is tuned like a lobe-switch system, not like continuous control.
- **Locate the changeover early**: before detailed WOT tuning, make one ramp with the switch out of reach (low cam only) and one with it set low (around 3000 rpm), each with fuel roughly corrected. The power curves cross near the best WOT changeover. Do not set the switch absurdly low to keep it always on, since lobe switches are oil-actuated.
- **Tune each mode beyond the boundary**: push the switch out of reach to tune low-cam cells; set it low to tune high-cam cells. To steady-state a column on the boundary, move the switch away so small rpm wander does not toggle the cam. Hold slightly above the switch rpm when tuning the column just after it.
- **Fine-tune last**: once fuel and spark are right, bracket the switch point (for example 250 rpm steps, then about 100 rpm). The combined curve should follow the higher of the two. Allow for actuation latency (one demonstration switched about 100 rpm later than commanded). Keep the original if differences are within run-to-run noise.
- **Load windowing**: the best switch rpm is lowest at WOT and higher at light load. Factory systems window the switch on rpm and load for that reason. A race car that never cruises in the window can live with rpm-only switching.
- **Table strategy**: either one table with breakpoints tight either side of the switch (tens of rpm apart), which works only for an rpm-only switch, or separate low-cam and high-cam fuel (and optionally spark) tables selected by the actual cam state. Dual tables keep fuelling right when the switch moves, when hysteresis or delays apply, or when lockouts hold low cam (a single table under a lockout typically runs very rich at high rpm). Keep both tables on identical axes so they can be copied and compared. Concentrate breakpoints where each cam runs, and extend the last rpm breakpoint to or past redline.
- **Seeding the high-cam table**: copy the tuned low-cam table and add fuel (practitioner examples ranged from about 15 to 20 % above the boundary load), because the high lobe flows more air. Rich at first engagement is the safe side.
- **Hysteresis**: use a lower off-threshold than on-threshold (tens of rpm is enough, about 50 to 100 rpm in the sources). The torque step at switchover itself moves rpm, so without hysteresis the cam chatters. That sounds bad, feels erratic, and was seen as a blip in a torque curve. Very wide hysteresis means a VE band that differs depending on cam state, which one table cannot match.
- **Lockouts**: rpm minimum (sources keep it around 3000 to 4000 rpm), coolant, throttle and oil pressure are typical. Respect the engine maker's oil-pressure needs.
- **Valvetrain limits**: on some lobe-switch engines the low lobe should not be run far into high rpm; follow the engine maker's guidance.

## Decision rules
- Judge every cam change by torque with lambda back on target, never by lambda alone.
- Speed-density, fixed VE: a lean shift or a trim moving toward adding fuel means more air (a gain); a rich shift means less air. This does not hold on air-mass-meter fuelling, and fades near the optimum.
- A large, sudden trim swing after a cam move means airflow changed sharply, so you are far from optimum. If trim hits its authority limit and closed loop drops out, lambda will drift for the rest of the sweep. Pre-add fuel where a cam change is expected to raise airflow.
- Coarse steps first (about 10 degrees), then 5. Adjustable fixed gears use about 2 degree steps in one practitioner's method, since smaller steps are hard to see run to run.
- Intake before exhaust. If unsure of safe cam limits on a modified engine, the engine builder decides, not the dyno.
- Switched systems: choose the changeover where the torque curves cross, never by default at a low rpm.
- Keep all targets inside measured mechanical travel.
- Do not edit safety limits to make cam work possible; a protection that trips is evidence, not an obstacle.

## Data gates
- Cam actual tracks target (per bank) within a few degrees in steady state, and settles within a fraction of a second after a step, before any torque reading is used.
- No persistent target-minus-actual offset at high targets; if present, the target exceeds travel.
- Lambda back on target (or the trim recorded) before comparing torque between cam settings.
- Each WOT comparison run shows logged cam position equal to the intended fixed value.
- Oil at normal operating temperature for controller and hold-duty work.
- Switched systems: the cam-state channel is logged with rpm so latency and chatter are visible.

## Worked example
### Continuously variable intake, steady state
One practitioner example at 2500 rpm and 40 kPa absolute: moving the intake from 0 to 10 degrees advance first dropped torque from about 40 to 30 Nm, while lambda went from 1.00 to about 1.06. Adding about 8 % VE restored lambda 1.00, and torque became about 47 to 48 Nm. At 20 degrees, after the same correction, it reached about 60 Nm. The lean shift was the clue that air mass rose; the apparent loss was the mixture, not the cam.

The size of the lean shift follows from fixed fuel mass: lambda_new = lambda_old x (m_air,new / m_air,old). So 1.06 / 1.00 means about 6 % more trapped air, consistent with the roughly 8 % VE added (the difference is measurement noise and the mixture effect on torque).

### WOT composite
On a V6 demonstration the intake was set to fixed values across the whole WOT region. 30 degrees was best up to about 4750 rpm, 20 to about 5600, 10 briefly near 5750, and rest above about 5850. The composite row followed that envelope. It was then smoothed, because a 30-to-0 degree swing over 1000 rpm is near what a hydraulic phaser can follow during a fast pull.

### Switched cam, reading the VE table
On a turbo lobe-switch engine with one VE table and a 4600 rpm switch, VE either side of the switch at about 200 kPa was near identical (about 126 %), so the WOT switch point was right. At 60 kPa it fell from about 89 % to 47 % across the same rpm, so the light-load switch wanted to be much higher (near 6000 rpm). The engine would gain from a load window.

## Disputed / conflicts
- **Order of work**: some lessons tune fuel and spark with the cam at rest first and then add cam, using the fuel demand change as the gain measure. Others set ignition conservatively, map cams with closed loop holding lambda, and finalise fuel and ignition last. Both agree that VE must be redone after any cam change. The second route saves repeating ignition work; the first gives a clean baseline without a dyno. Test: count rework hours on a fixed engine either way.
- **Cold lockout**: several practitioners prefer no coolant lockout (or a very low one, around 30 C), accepting sluggish tracking over a parked cam that makes the VE table wrong. Other material sets a minimum coolant lockout because cold oil gives poor control, and some ECUs instead offer an oil-temperature compensation. Test: log lambda error and cam error during a cold drive with each setting.
- **Low-rpm lobe switching and oil**: one lesson says switching very low may not engage reliably and robs bearing oil; another calls the bearing-starvation claim an unconfirmed legend. Both still set a minimum of around 3000 to 4000 rpm, and the comparison run will show if lower is wanted.
- **Switch off-delay**: one course adds about a 1 s off delay to the switch output to stop cycling, citing factory practice. Other material says rpm hysteresis of tens of rpm is enough, that 0.5 s is more than needed, and that hold timers beyond a few tenths cause drivability side effects. Test: log cam-state toggles and torque with each.
- **Dual ignition tables**: some sources run separate spark tables for each cam lobe because the high lobe tolerates more advance (one example showed several degrees more at WOT on high cam). Another practitioner calls dual fuel essential but dual spark optional, since being 2 to 3 degrees off is still near MBT while fuel errors across a switch can be 5 to 20 %.
- **Part-throttle goal**: the power approach maximises filling. A counterpoint is that more overlap and less filling can reduce pumping loss for economy (and emissions), as factory maps do. The torque-optimal map therefore differs from stock.
- **Boost sensitivity**: most sources find optimal cam targets change little between moderate and high boost while the turbo is efficient. One notes that a very large boost range (drag) makes low-boost cam results largely irrelevant, because exhaust back pressure changes the optimum.
- **Value of the work**: one practitioner reports an engine where more than 20 hours of cam work gave only a few kW, while other engines gain a lot (one demonstration gained about 30 kW at the wheels at 3500 rpm over the rest position). Anecdotal; test the specific engine.
- **Electronic fail-safe**: one practitioner does not rely on the ECU's target-error fail-safe for valve-contact protection, because the build should make contact impossible. That is a view on what protects the engine, not advice to turn the fail-safe off.
- **Textbook cross-check**: the combustion textbook and automotive handbook support the intake cam having the larger effect through inlet closing. The 2 and 10 degree step sizes are practice, not derivation.

## Citations
- practice: Practitioner training and tuning practice, distilled and cross-checked.
- engineering-texts: Engine, combustion, charging and control engineering texts.
