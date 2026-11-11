---
id: methodology/trigger-setup
title: Trigger setup
layer: L2
status: draft
confidence: medium
sources: [practice]
verified: 2026-11-11
applies_to: {fuels: [gasoline, ethanol, methanol], engines: [all]}
depends_on: [methodology/base-setup]
supersedes: []
---

# Trigger setup

## Claim
Every fuel and spark event is placed from the trigger decode, so the trigger is proven before anything else is tuned. The sequence is: pick a decode mode that matches the real wheels and sensors; prove it while cranking with the engine unable to fire (steady, believable rpm, full sync, an error counter that stops rising); calibrate the displayed timing against the crank with a timing light; run a locked-timing rpm sweep to show the reference does not drift; and keep watching the error counter and the rpm trace through the tune. A trigger fault often looks like a fuel, knock, misfire or power problem, so it has to be ruled out before those are chased. Filtering hides a symptom. It does not fix the cause.

## Why (derivation)
### Speed, position and phase
A four-stroke cycle takes 720 crank degrees. A crank wheel alone gives speed and position within one revolution (360 deg). It cannot tell compression TDC from exhaust TDC. That is enough for batch or semi-sequential injection and wasted spark, but full sequential injection and coil-per-cylinder direct fire need a phase (sync, home) signal at half engine speed, from the cam or distributor. A wheel turning at cam speed with a missing tooth (for example 24-1 on a cam) gives both speed and phase from one sensor, because its gap comes round once per cycle. An engine always has a crank or cam-speed reference. Cam sync is optional and is added for sequential operation. A throttle-body batch system fed from the coil negative only needs speed (pulse frequency and cylinder count).

### Why the reference belongs on the crank
Anything driven from the camshaft picks up belt or chain lash and valvetrain torsional resonance. A cam-driven disc can oscillate past its pickup, so teeth are missed or counted twice, and the effect grows with stiffer springs and bigger cams. The sources agree that the speed and position reference is best taken from the crank, with only the phase taken from the cam. Ignition and injection are referenced to crank TDC anyway.

### Interpolation between teeth
Between teeth the ECU assumes the crank turns at constant speed. In reality it slows on each compression stroke and speeds up on each power stroke, and most of all at a lumpy idle, on low cylinder counts and with big cams. With few teeth (4 to 8) spark placement therefore wanders at idle by up to a few degrees. The wander fades above about 1500 to 3000 rpm. More teeth track speed better but carry costs (see Disputed).

### Sync window
With an evenly toothed crank and a single cam sync edge, the ECU checks sync by counting crank teeth between sync events. Tooth spacing is 360/n crank degrees, so a sync edge placed midway has a margin of about ±180/n crank degrees before it crosses a crank edge. Belt stretch, chain movement or cam resonance moves the cam edge by some cam angle x, which is 2x crank degrees. Once the edge crosses, the ECU counts one tooth too many or too few, flags an error and drops sync. With a missing-tooth crank wheel the sync only has to avoid the gap, a window of roughly 350 crank degrees, so placement is far less critical. A cam level signal (high for one revolution, low for the next) avoids edge placement entirely.

### Variable reluctor (VR) signals
A VR output rises as a tooth approaches, crosses zero sharply at tooth centre and then decays. Its amplitude grows with tooth surface speed: a few volts or less at cranking and idle, 20 V or more at high rpm, and over 50 V on a large wheel at high rpm, where input protection may clamp it. Noise grows with rpm too. The ECU arms when the signal passes an arming threshold and triggers on the next zero crossing, so the threshold must rise with rpm. The sources' rule of thumb is about one third of peak amplitude at each rpm. With reversed polarity, or the wrong edge selected, the ECU triggers on the slow, decaying side of the waveform, whose crank position moves with amplitude. Timing then drifts with rpm, often by 15 to 30 degrees, while the engine still starts and idles.

### Hall and optical signals
These give a square wave from an open-collector output that only pulls to ground. Without a pull-up the input floats, showing no edges or random wavering. Some low-cost Hall sensors round off their falling edge more and more as frequency rises, which moves the trigger point and limits them on high tooth counts.

### Fixed delays become angle
A fixed time delay t (sensor processing, coil or igniter response) is an angle error of θ = 6·N·t degrees, with N in rpm and t in seconds. That is why a correctly wired trigger can still show a degree or two of retard at high rpm, and why many ECUs have a delay or latency setting that removes it.

### Filtering versus tooth period
Tooth period is T = 60/(N·n) s for n teeth per crank revolution. A debounce or filter rejects pulses shorter than its width. At high rpm on a high-count wheel, real teeth get close to the filter width and are thrown away, which produces the same errors the filter was meant to cure.

## Assumptions
- The wheel pattern, tooth count, sensor type (VR versus Hall/optical) and edge convention are known, or can be found from a scope capture.
- The ECU offers a decode mode for the pattern, or a generic mode that can describe it.
- The pulley or damper marks are trustworthy, or true TDC has been found and marked.
- A timing light can pick up cylinder 1's spark, and the ECU can lock ignition to a fixed angle that bypasses tables and compensations.

## Breaks when
- High-count cam-driven discs (for example 360-slot optical units, giving 180 pulses per crank revolution) run on modified valvetrains. Harmonics cause double counts and the decode loses position at certain rpm.
- The sync edge sits close to a crank tooth edge, or drifts into one at high rpm through belt stretch. This shows as errors only near the top of a pull.
- A missing-tooth wheel has a full-depth gap. The large swing after the gap stops the next tooth crossing zero at high rpm, so a tooth is missed. The sources say a gap of about half tooth depth avoids this.
- A VR arming threshold is too high for weak cranking signals (large air gap, slow starters), giving no rpm, or too low at high rpm, letting noise trigger.
- A pickup bracket is not rigid, so it vibrates at some rpm and can touch the wheel.
- A distributor-only trigger has drive slack that makes the reference oscillate in some rpm bands.
- Moving a cam that carries the trigger or sync sensor shifts base timing, and can push a marginal sync edge into a crank edge.
- A preset named after the vehicle is assumed to be right when it is not. One rotary example needed the generic mode; for one early four-cylinder, a decoder with a similar model name was the wrong pattern.
- A simple pattern decoded in the wrong mode can idle and only fail higher in the rev range.
- A home-built pattern on an uncommon engine variant may also disturb variable cam control decoding until the ECU maker helps.

## Practical use
### Assess the trigger hardware first
- On a home EFI conversion, suspect the trigger first. It is built from scratch, unlike an OE-engineered system.
- Read the wire count as a hint only: two wires usually means VR, three or four means Hall (supply, ground, signal, shield). The scope is the proof.
- Count teeth over a 720 deg capture against the cam pulse to identify an unknown wheel (for example 12 crank pulses per cam pulse, or 58 pulses and a two-tooth gap per revolution on 60-2).
- For a custom build, the sources prefer a crank reference with a cam sync placed about midway between two crank teeth. One practitioner's preferred wheel for high-rpm drag engines is 12 teeth (run to about 11,000 rpm). A missing-tooth wheel is the more forgiving choice where sync placement is hard to control.
- Any cam-train modification on an engine with a cam-driven high-resolution sensor is the point at which one practitioner fits a crank trigger. A replacement 24-tooth plus single-sync disc in the factory sensor is a middle step that fixes most stock or lightly modified engines.
- A VR sensor is well suited to the crank speed signal: robust, self-powered, still working when cranking voltage sags. A Hall sensor is often the better fit for a slow, irregular cam signal. A VR on a very large wheel at high rpm can over-voltage the input, and a Hall swap cures it.
- Engines keeping factory variable cam control are tied to the factory cam patterns, because the ECU must measure cam position from them.

### Configure the decoder
- Use the engine-specific mode where it exists. It may also underpin variable cam control decoding, so the exact mode matters beyond just running. Use generic modes for custom wheels. When unsure, ask the ECU maker. Unsupported patterns can often be added if the maker is sent a scope capture.
- Missing-tooth geometry is usually entered as the tooth count as if none were missing (24 for 24-1), plus the number missing. Gap-width style decoders instead take physical teeth and gap angles summing to 360 deg, with plausibility windows on each gap.
- Assign the higher tooth-count signal to the primary trigger input.
- Hall or optical: pull-up on. VR: pull-up off, rpm-dependent arming table, edge chosen from the waveform.
- Start with minimum filtering and minimum rpm averaging. Add filtering only after a wiring and shielding check, and only if errors remain. One engine speed averaging start point is 720 deg divided by cylinder count.
- Keep sync set to always use the home signal. If the ECU ignores sync after the first lock and then loses a tooth, it cannot recover, and timing can be anywhere.
- Some ECUs can skip the first few pulses or require a number of teeth before syncing, to cope with irregular early cranking. A quick-start option may fire batch or wasted spark until sync. Set the cranking-to-run rpm threshold slightly above real cranking speed.
- Where the ECU uses a reference tooth plus a trigger angle, the trigger angle can cap the maximum advance available. The sources suggest a reference about 45 to 60 deg before TDC, above the most advance the map will ever ask for.
- Odd-fire engines need per-cylinder TDC angles. Even-fire engines use the evenly spaced default.

### Prove the decode while cranking
1. Make the engine unable to fire. Most sources disable the injectors or the fuel pump. Some also disable coils (see Disputed).
2. Crank and watch: both trigger inputs valid, the sync state reaching full cycle sync (on some ECUs it steps from stopped to 360 then 720), and rpm believable and steady.
3. Cranking speed in the sources is typically 150 to 300 rpm, depending on compression, starter and battery. Steadiness matters more than the value. Readings of 700 to 1500 rpm while cranking, or jumps between about 50 and 1000 rpm, are red flags. So are large swings in rpm rate of change.
4. The error counter may tick once or twice at the start or end of cranking. A counter still rising during steady cranking is a fault to fix before going on.
5. Capture the scope during the crank: both signals present, VR polarity correct for the chosen edge, the sync edge clear of crank edges and of the gap, and a decoded engine angle that ramps smoothly to 720 and resets. Compare the raw trace with the ECU's interpreted tooth state, which separates a bad signal from a bad configuration.
6. Re-enable fuel (and coils) straight away. Forgetting this is a common, time-wasting cause of a no-start.

### Set the base offset
- Never assume a base file's offset is right. An unverified offset can mean a table that looks safe is actually giving 10 to 15 degrees more advance than displayed. Verify on every inherited car too.
- Check the marks. Pulley mark spacing is not standard. Aftermarket dampers may carry different marks, and old elastomer dampers can slip. Even new factory marks can be a degree or two out. Where in doubt, find true TDC with a positive stop and make marks.
- Lock timing to a value you can see on a mark and that the engine will idle at. About 10 deg is common; 0 deg idles poorly unless the engine is held at 2000 to 3000 rpm. Light cylinder 1. On coil-on-plug engines a short HT lead may be needed for a reliable pickup.
- Coarse pass while cranking, fuel disabled. Getting within about 2 to 5 degrees is enough to start. If the marks are not visible, change the offset in steps of 50 to 60 deg until they appear. On some ECUs the cranking advance overrides the fixed value, so set both to the same number.
- Fine pass once running. Hold about 1500 to 2000 rpm, or 1200 to 1500 with low tooth counts or big cams, where the mark is steady. Step the offset and watch which way the mark moves.
- A plug-in base map for a known engine is usually within a couple of degrees and up to about 5. The sources accept starting on it and then checking. On a universal install the offset is unknown, so it is set while cranking before the first fire attempt.
- Turn timing lock off afterwards and save. A forgotten lock makes ignition table edits appear to do nothing and the engine feel flat.

### Drift test
With timing still locked, raise rpm from idle to 3000 to 5000 (or toward 6000) and watch the light.
- About 1 degree of movement is normal in most sources, and 1 to 2 degrees is repeatable and acceptable. Trim it with the ignition or pickup delay setting at 5000 to 6000 rpm until the two speeds agree. Without that setting it ends up in the timing table, which is acceptable.
- More than about 3 to 4 degrees is a problem. 15 to 30 degrees is the signature of reversed VR polarity or the wrong edge.
- If drift appears, confirm the lock is actually active before blaming the trigger.

### During tuning
- Note the error counter before each pull and confirm it is unchanged afterwards. Clear the ECU's max-value statistics before a test. An implausible max rpm there betrays trigger errors.
- Log rpm and rpm rate of change. On a ramp run, rpm should be a straight line with rate of change matching the ramp rate.
- Where the ECU offers a relative sync position channel (50% means midway between crank teeth), log it across rpm. On a belt-driven cam it drifts with speed. Offset the sync from centre at idle to allow for the drift.

### Diagnostic tests (telling one cause from another)
- **No rpm while cranking.** Hall/optical: suspect a missing pull-up or wrong sensor type. VR: confirm a signal on the scope, then lower the arming threshold in the cranking cells (one source went to about 0.1 to 0.2 V at the 500 rpm cell).
- **Rpm present, but the engine bangs, misfires and will not idle.** A common cause is a plain multi-tooth mode selected for a missing-tooth wheel. The ECU sees teeth but expects even spacing.
- **Light shows the right timing but the engine will not fire, or only pops in the exhaust.** Sequential direct fire is 360 deg out. Add or subtract 360 deg from the offset; the light reads the same. On ECUs with limited offset range and a single-pulse cam, swapping the cam edge moves sync to the other revolution. Wasted spark and distributor systems cannot be 360 out this way.
- **Banging or kickback at start blamed on injector data.** Injector dead time would not cause it. Check cranking trigger and timing.
- **Large drift with rpm at locked timing.** Polarity or edge is wrong. Small, repeatable drift is a delay setting.
- **High-rpm-only misfire: trigger or ignition?** Hold rpm and vary load. Ignition breakdown gets worse with load and boost. A trigger misfire follows engine speed only and does not change with load. Then check the error counter and the arming table at that rpm.
- **Errors only near the top of a pull with cam sync.** The relative sync position falls from about 50% toward 15 to 20% as rpm rises, so the sync is approaching a crank edge. Scope the inputs during a ramp at the failing rpm and move the sync edge, or choose the edge pair that gives the widest window.
- **Errors at high rpm on a high-count wheel after adding filtering.** The filter is now rejecting real teeth. Back it off.
- **Erratic tune: lambda scatter, knock that moves run to run, the engine will not take normal timing, a jagged or collapsing curve above some rpm, poor run-to-run repeatability.** Look at rpm noise and rpm rate spikes (one log showed about ±5000 to 6000 rpm/s, which is physically impossible) and at actual versus commanded timing. A single hump where a big turbo comes on boost is usually the dyno's load control, not the trigger.
- **The engine takes far less timing than experience says it should.** Before accepting it as a knock limit, rule out triggering. In one practitioner's case a modified engine held only 5 to 6 degrees under boost against an expected 15 to 16.
- **Loss of sync feels like an ignition misfire.** Most ECUs cut fuel and spark until they resync. A misfire alone does not prove a trigger fault, and ignition noise can itself cause trigger errors.
- **Inherited car that idles fine.** Configuration errors may only show under load, so recheck mode, edge and polarity whenever trigger symptoms appear.
- **Checking VR polarity without a scope.** With a DC voltmeter across the sensor, let a steel screwdriver shaft stick to the tip and flick it away. With meter positive on sensor positive, the reading should swing negative. Otherwise use the locked-timing drift test once running.

## Decision rules
- Match the decode mode and tooth counts to the actual wheel, and ask the ECU maker when in doubt. Do not assume a similar-sounding preset is right.
- VR inputs: set the arming threshold above background noise and about a third of peak amplitude across rpm, using scope captures at several speeds. Hall/optical inputs: pull-up on.
- Use as little filtering as possible. Needing heavy filtering is a sign of a trigger or wiring problem to fix, not a cure. Look at wiring, shielding and grounds first.
- Avoid options that ignore the sync input above some rpm. They are a band-aid and can leave the ECU unable to recover position.
- Disable fuel and ignition during verification cranking, then re-enable them.
- Verify base timing with a light on every new or inherited install, at cranking and again running, and finish with a locked-timing drift test.
- Recheck base timing and sync margin after any change to a cam that carries a trigger or sync sensor.
- Polarity errors on a reluctor sensor produce timing drift. An engine that runs is not proof of correct polarity.

## Data gates
- No trigger errors counted after the initial sync; the counter is unchanged across each pull.
- Steady rpm while cranking (typically 150 to 300 rpm in the sources), with no spikes or jumps, and full sync.
- Rpm rate of change on a ramp run matches the commanded ramp rate, with no spikes.
- Locked-timing drift from idle to 3000 to 6000 rpm within about 1 to 2 degrees.
- Where logged, relative sync position stays well clear of 0% and 100% across the rpm range.

## Worked example
**Delay drift.** A fixed 50 µs of unaccounted delay at 6000 rpm gives θ = 6 × 6000 × 50×10⁻⁶ = 1.8 deg of retard. At 1500 rpm it is 0.45 deg. This matches the 1 to 2 degree high-rpm retard the sources treat as normal and remove with the delay setting. A 20 deg movement on the same test is far too large to be delay, which points at VR polarity or edge.

**Filter versus real teeth.** On a 60-tooth-spaced wheel at 8000 rpm, T = 60/(8000 × 60) = 125 µs per tooth, so a 50 µs debounce still passes real teeth. A cam-driven 360-slot disc gives 180 pulses per crank revolution, so at 8000 rpm T = 60/(8000 × 180) ≈ 42 µs, which is shorter than the same 50 µs debounce. Real slots would be rejected. Data rate and filtering both work against such discs at high rpm, before valvetrain harmonics are even considered.

**Sync window.** A 12-tooth crank wheel has 30 deg between teeth. A sync edge placed midway has about ±15 crank degrees (±7.5 cam degrees) of margin. On a 24-tooth wheel the margin halves to ±7.5 crank degrees. One practitioner's drag engine log showed relative sync position drifting steadily with rpm until it crossed over at about 10,000 to 11,000 rpm and cut out, so the idle setting was offset from 50% to allow for belt stretch.

**Erratic rpm at high speed.** An rpm signal reading erratically at high rpm with no fuel issue points at the trigger signal. In one practitioner's example, a big-turbo six on a factory high-resolution cam sensor gained about 81 kW at the wheels above 5000 rpm from a crank trigger alone. In another, an engine returned to a workshop at about 195 kW with a jagged curve and an error counter of 222 after a few runs. The Hall sync edge had drifted next to a crank tooth. Changing the sync edge in software restored a wide window and about 320 kW, and an offset change alone would not have fixed it.

## Disputed / conflicts
- **Cause of factory 360-slot cam sensor problems.** One practitioner attributes the double counting to valvetrain harmonics bouncing the fine-slotted disc. He notes another view that blames the aftermarket ECUs' signal processing. Both sides agree the problem is real and worse after cam and spring changes. Discriminating test: scope the disc output against a crank reference at the failing rpm. Extra pulses that appear only with the modified valvetrain point at harmonics.
- **Is timing jitter worth a crank-trigger upgrade?** On a knock-limited, high-boost pump-fuel engine, one practitioner treats any jitter as a problem, because an advance excursion can cross the knock limit and forces a retarded base map. On race fuel or ethanol blends that are not knock limited it matters much less, and some very high-power engines keep the factory sensor. This is a cost-versus-margin judgement, not a rule.
- **Tooth count.** More teeth give steadier idle timing and better tracking of fast speed changes. Fewer teeth give a wider sync window and lighter decode load at high rpm; one practitioner reports 60-2 at 8,000 to 10,000 rpm flooding some ECUs. He prefers 12 teeth plus single sync (worst case 36-2) for high-rpm builds and accepts a couple of degrees of idle jitter. Another lesson favours missing-tooth wheels because they make sync placement uncritical. Both positions hold within their contexts.
- **Which edge convention to use for VR inputs.** One practitioner always configures the falling zero crossing and corrects polarity in the wiring, so the convention is checked physically. Other sources simply select the other edge in software where the ECU allows it. One cranking capture showed a cam signal that needed the rising edge, against convention. Where the ECU offers no edge choice for VR inputs, the wiring must be right.
- **Arming threshold starting values.** Defaults quoted differ: about 0.3 to 0.5 V at 0 rpm rising to about 4 V at 7000; about 0.5 rising to 3 V; about 1.5 V at 1600 rpm rising to 5 V above 4000. A single-value threshold starts near 0.3 V and is raised as far as reliable triggering allows. All agree on the principle: above the noise, below the signal, and near a third of peak when measured.
- **The trigger must occur a set angle before TDC.** One practitioner calls the old belief that the trigger must occur at least about 15 deg before TDC a hangover from older ECU documentation, not a constraint for modern decoders. Separately, ECUs that use a reference tooth plus trigger angle can cap available advance at that angle. This is a real but setting-specific limit, not a processing-time limit. Check the ECU's documentation.
- **What to disable while cranking.** One lesson disables fuel rather than coils, because injectors spraying with no spark wet the plugs. Other lessons disable both injectors and coils. Both prevent starting. The fuel-only approach needs care if timing may be badly off, since the engine can kick back.
- **Factory ECUs.** One source says locking timing to set a crank offset is unnecessary on a late-model OE ECU, because OE wheels fit one way and tolerance is under a degree. Standalone sources insist on verifying every install, including OE-pattern presets, because of manufacturing tolerance. The two apply to different situations.
- **Inline resistor on a VR signal.** One practitioner reports a high-rpm VR misfire on an older ECU cured with a series resistor that knocked the signal level down. On ECUs with an rpm-based arming table he has never needed one.
- **Hall sensor limits.** A common low-cost Hall type is reported fine on a 12-tooth wheel even at 10,000 rpm, but troublesome on 36-tooth or 36-2 wheels from about 7000 to 8000 rpm. Another view holds that either sensor type works well if correctly selected and installed. The sources recommend a VR with square teeth for 36-2.
- **Drift tolerances.** Sources variously call about 1 deg, 1 to 2 deg, and up to 3 to 4 deg acceptable. Only the larger figure is cited as the limit beyond which there is definitely a problem. Treat about 1 to 2 deg as normal and anything larger as a reason to investigate.

## Citations
- practice: Practitioner training and tuning practice, distilled and cross-checked.
