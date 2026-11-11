---
id: methodology/base-setup
title: Base setup and pre-start checks
layer: L2
status: draft
confidence: high
sources: [practice]
verified: 2026-11-11
applies_to: {fuels: [gasoline, ethanol, methanol], engines: [all]}
depends_on: [methodology/tuning-order]
supersedes: []
---

# Base setup and pre-start checks

## Claim
Before an engine is started, inputs read correctly, outputs fire on the right cylinders, the configuration describes the real engine, protective limits are set, and timing is confirmed with a light. A wrong setting found here costs minutes; found running, it can cost an engine, or hours spent tuning around a fault that looks like a tuning problem.

## Why (derivation)
Every calculation the ECU makes starts from sensor values, configuration constants and crank angle. A timing reference wrong by tens of degrees or one full revolution creates a misfire or a fire outside the combustion stroke. A timing reference wrong by a few degrees in the advanced direction is worse than it looks: every table value is then more advanced than displayed, and a map that seems conservative can drive the engine into knock.

Configuration constants scale everything downstream. In a VE-based fuel model, displacement sets the air mass assumed at 100 % VE, so an engine with a stroker or overbore entered at its factory capacity carries an error into every cell and into every compensation built on them. A wrong stoichiometric ratio shifts every fuel mass calculation. A wrong coolant reading makes warm-up enrichment act on the wrong temperature, and the engine runs rich or lean in a way that looks like a fuel table problem.

Output errors differ in how visible they are. A swapped coil lead usually gives obviously bad running. A swapped injector in sequential mode often runs almost normally and only shows later as fuelling that will not behave, which makes it the more dangerous mistake.

Tables interpolate between breakpoints, and many ECUs hold the last value beyond the table edge. So resolution is needed only where the engine's requirement changes quickly or where it spends time; extra breakpoints elsewhere only add work. One course demonstration on a V6 compared a normal table with one of only four cells and found nearly identical peak power, but with an uncontrollable rich point where VE departed from a straight line: interpolation does most of the work, and resolution matters where VE is not linear.

## Assumptions
Standalone-style configuration where these settings are exposed.

## Breaks when
- Factory-ECU reflashes often hide or fix these settings, so the checks change to verifying what the calibration claims (methodology/reflash-tuning). On a factory ECU with trigger wheels in their factory positions, base timing is inherently correct and there is usually no lock mode.
- Engines whose VE changes sharply (aggressive cams, cam-lobe switching, variable runners) need extra breakpoints where it happens.
- Older engines can have a harmonic damper whose rubber bond has failed, so the marked outer ring has rotated relative to the crank and the marks lie. Rare, but it explains an engine that will not idle at any sensible advance.

## Practical use
Run the checks in order and record results. Base table sizes are a starting point; zones can be added later.

### Starting file
- Start from the closest base file for the exact board and vehicle when one exists: its inputs and outputs already match the factory wiring, and in a native chassis it may also drive the dash and immobiliser correctly. A file from another box for the same engine can carry the trigger, cam and engine setup across, leaving only pin assignments to redo.
- Save it at once under a new name in a folder for that vehicle; keep the original untouched.
- A supplied base file starts a stock version of the car at best. It knows nothing of changed injectors, fuel system, turbo or sensors. Walk every configuration item, page by page, and be able to set it from a blank file; base files can carry errors and can have features enabled that you do not want (launch control was found active in one demonstration). Disable unused functions explicitly.
- Wizard-generated maps need inspection before use. One generated map for a common V8 had idle pulse width more than double what the engine needed and a flat low-load region. Fuel must fall as manifold pressure falls, so a flat low-load region predicts a very rich start. Rich and retarded is still the right side to start on.
- For a custom or adapter harness, document every pin (factory pin, ECU pin, function, sensor type and calibration) and configure against that document.
- After loading a file onto the ECU, confirm it really is your file by spot-checking settings you changed, and re-audit key values (stoichiometric ratio, injector data, axis scaling). One demonstration found the stoichiometric ratio changed after upload. Store or burn changes to permanent memory; on many ECUs unstored changes are lost when the ignition is cycled, and some settings take effect only after a power cycle or a reprogram.
- After moving a file to a different box model, recheck every input, output and wideband assignment; a box lacking some hardware can drop those assignments silently.
- Firmware should match the software version. Read the release notes first (some updates need configuration changes), update key-on with the engine off and a charger on a doubtful battery, never interrupt power during the update, and do not update on a race day.

### Engine description
Cylinder count, firing order (it maps injectors and coils to cylinders), odd-fire settings only where the engine really is odd-fire, injection mode, trigger setup, true displacement, fuel type and stoichiometric ratio, fuel system type and base pressure, injector data matched to the fitted injectors (dead time against voltage), and bank assignment on engines with a lambda sensor per bank. Establish fuel type, intended use and missing hardware first (for example no idle air valve on a competition car), because they decide strategy.

### Sensor checks, key on, engine off
- Every analog input reads a plausible value with no fault status.
- On a cold engine, coolant and intake temperature agree with ambient: this validates their calibration.
- Manifold pressure reads about atmospheric and agrees with the barometric sensor; a mismatch points to a bad sensor or wiring.
- Throttle position scaled 0 to 100 %, with the closed point most important (idle control and overrun fuel cut depend on it).
- The wideband powers up and reads full lean in free air. Check what powers it: on one car it was fed from the ignition key separately from the ECU.
- Digital inputs and key-on outputs (fans, pump prime) work. Defer what needs a running engine (cam solenoids, cam switching, oil pressure).

### Output tests
- With the fuel pump disabled and no pressure in the rail, pulse each injector with short pulses at a low rate (2 ms at about 10 Hz in several sources) and confirm the injector clicking is the one on the matching cylinder; unplugging each in turn and hearing the click stop is a sure check. With pressure present the test fills the ports and cylinders with fuel.
- Fire each coil briefly with low dwell and confirm it is the right cylinder (a spare plug on a grounded lead, or a timing light). Never latch a coil output on; it damages the coil.
- Test pump, fans and idle valve last, confirming by sound or a pressure rise. Turn test mode off afterwards.
- Without an output test mode, use continuity checks for injector and coil order, a power-down and key-on for the pump prime, and temporary thresholds for fans.

### Protective limits before first start
Set the rpm limit and, on forced induction, a boost limit before any running. Several practitioners set a low temporary limit (about 2500 to 3500 rpm, or 4000 to 5000 on an engine meant for 7500 to 8000) so a sticking throttle or a large air leak cannot flare the engine while oil pressure is still building. Remove it once the checks pass: one practitioner lost time on the dyno chasing an apparent misfire that was this temporary limit.

### Table layout
Typical starting layouts in the sources, refined after running:
- rpm breakpoints about every 500 rpm, with a site at target idle and one just off idle (around 1250 rpm, sometimes also 1750) for the idle-to-driving transition; the top site a little beyond the planned rev limit (about 500 rpm in several examples).
- Load breakpoints about every 20 to 25 kPa, tightened toward 10 kPa around the idle and cruise manifold pressures, with the top a little beyond the planned maximum boost so a later limit change stays inside the table. On a naturally aspirated engine remove boost rows (applications/naturally-aspirated). On an engine run at a fixed boost, one practitioner puts a row exactly at that boost.
- Ignition tables can be coarser than fuel: the engine is less sensitive to small timing changes than to fuel, and one demonstration found 10 kPa ignition spacing finer than needed because the optimum moved only a few degrees between 50 and 70 kPa. Many sources still keep fuel and ignition breakpoints matched.
- Choose the load source and axis type first. Know whether MAP is absolute or gauge. Confirm that each table really uses the intended axis: one demonstration found a lambda target table set to throttle position on a boosted engine, where it cannot tell boost levels apart; on generic-labelled tables, check what the load source actually is.
- Changing breakpoints after tuning changes the tune unless the software re-interpolates the cell values; use that option where it exists.
- Some ECUs have a fixed number of breakpoints or a limited number of 3D tables; plan around the allocation.

### Starting values
- VE-model tables: a flat value around 50 % (50 to 60 % in some sources) is usually close enough to start almost any engine if injector data and displacement are right. Typical engines idle around 40 to 60 % VE and reach about 90 to 100 % near peak torque. A rough shape by region (idle, cruise, full load) is an alternative to flat.
- Pulse-width or percentage tables have no portable starting value, because their numbers depend on displacement and injector size; start near the existing idle values (around 30 to 40 % in the examples).
- Where a master pulse width scales the table, choose it so the largest values land well inside the table's range (around 70 to 80 in one tutorial); too small and the table runs out, too large and resolution is poor. When nothing is known, one source starts at about 12 to 14 ms and rescales after the shape is found, since rescaling is lossless. Make global changes by scaling the table rather than relying on a master trim.
- Ignition: a flat value around 15 degrees with verified base timing is safe enough for start and idle on most engines; some practitioners reduce it further at high boost. A tuner who knows the engine well may shape it, but on an unknown engine start flat and work up.

### Base timing
1. Disable fuelling or injection so the engine cannot fire, lock timing at a value that matches a visible pulley mark and at which the engine idles happily (roughly 5 to 20 degrees; 10, 15 or 16 are common), and crank with a helper. Adjust the trigger offset until the light matches. Within about 3 to 5 degrees is enough to start: cranking speed fluctuates and the mark wanders, more so with few trigger teeth.
2. Once running with a sensible mixture, hold about 1500 to 2000 rpm, where the trigger signal is steadier, lock timing and set the offset precisely.
3. Rev to about 3000 to 4000 rpm with timing still locked and confirm the reading stays fixed.
4. Unlock timing afterwards. Forgetting this leaves later ignition changes with no effect; an indicator for locked timing helps.

The lock overrides the main table and all compensations on nearly all ECUs, so trims need not be disabled.

Reading the marks: research what each mark means (factory manual over internet sources); know the rotation direction, because it decides which way advance moves the mark and some engines rotate opposite to most; sight straight along the pointer to avoid parallax. Factory marks are typically within about a degree of true TDC; aftermarket pulley marks must be verified. Without marks, find TDC with a positive stop (a plug body with a protruding rod, about 25 mm in one source): with the plugs out, rotate by hand to contact each way and mark; TDC is midway. Never crank with the stop fitted.

Lights: a simple inductive light without dial-back is the beginner's choice. Dial-back lights mislead when misused and can be confused by wasted spark, where the light may also see the waste spark. On an engine with only a TDC mark that will not idle at zero advance, dial-back lets timing be locked at 15 to 20 degrees; confirm afterwards by holding 1500 to 2000 rpm with timing locked at zero, where the engine tolerates it. On coil-on-plug engines, clamp the coil wiring if it triggers the light, or fit a short lead between coil and plug.

Always verify timing with a light, even on plug-in ECUs, inherited tunes and cars "already set up": the number on the screen is easy to believe.

### Health checks once idling
Battery voltage about 13.8 to 14.2 V once running (a non-charging alternator is common on freshly wired cars; some race alternators with underdrive pulleys only start charging above idle, so raise rpm briefly before diagnosing), oil pressure sensible hot and cold, fuel pressure at its target running and key-on, no leaks or noises, idle manifold pressure plausible.

## Decision rules
Check each sensor against a known reference. Verify base timing with a timing light at a locked value. If the engine will not fire and timing appears correct, a 360-degree error is a likely cause. Load axis choice comes first, since changing it later affects the whole tune. Start with 500 rpm zones and about 20 kPa load zones, finer near idle and cruise, and refine after running.

A wrong reluctor sensor polarity shows as timing drift with rpm, so sweep the rpm with timing locked and confirm it stays steady. Always check the fuel pressure, even on an unadjustable system. Verify base timing with a simple inductive light; on wasted-spark systems a dial-back light reads double. Remember to release the timing lock afterwards.

Do not tune on a weak battery or a non-charging alternator. Low voltage changes injector opening time and pump flow, so fuelling tuned at low voltage is wrong once charging is fixed; one practitioner charged a battery reading about 11 V key-on before tuning.

Enter true displacement and confirm fuel and stoichiometric settings before any VE tuning.

Set protective limits before first start, and remove any temporary limit afterwards.

### Diagnostic tests
- **Timing drift with rpm** at locked timing: reversed reluctor polarity (or a trigger fault).
- **Mark jumps a few degrees at low idle** but steadies at 1500 to 2000 rpm: normal trigger behaviour at low speed, not a fault.
- **Engine will not idle at any sensible advance** on an old engine: suspect a slipped damper ring; check against true TDC.
- **Engine runs but one region of fuelling will not behave:** recheck injector-to-cylinder assignment.
- **No power-up on a plug-in board:** board jumpers or variant pinout wrong for the model.
- **Running voltage stays at 11 to 12 V and falls over time:** alternator not charging.
- **Coolant or intake reading differs from ambient on a cold engine:** sensor calibration or wiring fault; fix before tuning.

## Data gates
Battery voltage holds during cranking and reaches charging voltage once running. Temperature and pressure sensors agree with ambient on a cold engine.

## Worked example
An engine locked at 15 degrees reads 25 on the timing light: the timing reference is wrong by 10 degrees and must be fixed before any table is tuned.

A first start on a new base map lands at lambda 0.93 against a 0.90 target with about 3 % closed-loop correction. One practitioner reads that as the result of reasonable injector data, VE values and sensor calibration, and judges idle fuelling only once idle speed has settled at target.

## Disputed / conflicts
- **Base map or blank file.** One practitioner argues that building from scratch avoids inheriting errors; the same source accepts that vendor base files for common engines are good and are the usual real-world start. Both positions agree that every setting must be verified whatever the starting file.
- **Where to build the base map.** One practitioner builds it connected at the car, so each item is verified as it is programmed; others build offline and verify afterwards. Either works if the verification is done.
- **Ignition resolution.** Some sources keep ignition breakpoints matched to fuel; others use coarser ignition spacing. The demonstration above supports coarser spacing on smooth ignition surfaces.
- **Top of the load axis on a naturally aspirated engine:** see applications/naturally-aspirated.
- **Plain water for the first heat cycles** where a multi-layer steel gasket is fitted is one practitioner's view (glycol can seep past a gasket that has not settled); it is not a widely stated rule.

## Citations
- practice: Practitioner training and tuning practice, distilled and cross-checked.
