---
id: methodology/knock-sensing-setup
title: Setting up and validating knock sensing
layer: L2
status: draft
confidence: medium
sources: [practice, engineering-texts]
verified: 2026-11-11
applies_to: {fuels: [gasoline, ethanol, methanol], engines: [all]}
depends_on: [principles/combustion/knock, methodology/knock-assessment]
supersedes: []
---

# Setting up and validating knock sensing

## Claim
A knock sensing system, whether a tuner's audio monitor or the ECU's closed-loop control, is only evidence once it has been set up for this engine and shown to separate real knock from background noise. The background rises with rpm, load and timing, so the threshold must follow a no-knock noise profile measured at realistic timing, and the whole chain must be checked against a known knock event.

## Why (derivation)
A block-mounted piezo sensor hears every vibration: piston slap, valvetrain, chain and guides, gear and clutch rattle, the rev limiter, anti-lag combustion. Knock adds energy at the chamber's resonant frequency during a short crank-angle window after the spark. Detection therefore improves signal-to-noise three ways: a band-pass filter near the knock frequency, a window that listens only when the firing cylinder can knock, and a threshold that tracks the no-knock energy at each operating point. Because the background grows with mechanical speed, cylinder pressure and power, a threshold measured with very retarded timing sits below the noise of a properly timed engine and flags false knock. A threshold far above the noise gives no protection.

## Assumptions
The sensor is sound, correctly wired and solidly mounted; the ECU or monitor knows which cylinder is firing (an ignition reference plus firing order) if per-cylinder attribution is wanted.

## Breaks when
- Race engines with loose piston clearances, solid lifters, open exhaust or open wastegates can stay hard to read whatever is done.
- The engine is changed (swap, forged pistons with more clearance, big cams): a factory narrow-band sensor and its calibration may no longer fit. Practitioners report that factory systems usually cope better than feared, but not always.
- One sensor on a long or V engine: cylinders nearer the sensor read louder.
- Logging hardware that clips (gain too high) or compresses values (gain too low).

## Practical use
### Sensor and mounting
- Two-wire flat-response (broadband) sensors suit most engines; single-wire resonant factory sensors are tuned to one engine, and those grounded through their body can be very noisy (one practitioner replaced such sensors because only the second harmonic was usable). The two wires go to the ECU's dedicated knock input and a sensor (signal) ground; a chassis ground spoils the reading. Run shielded twin-core cable, its shield terminated at one end, at the ECU.
- The best spot is up near the deck face of the block, where the resonance begins, and on the side away from exhaust heat. Ranking in the sources: a free boss up high on the block; any other block location, the sump rail area often being fine; a borrowed engine-mount bolt where the face clears; a cast alloy timing cover or sump; the cylinder head (poor with solid lifters at high rpm); the intake manifold only when nothing else is possible. Keep away from where block meets gearbox: clutch and bearing noise travels in there.
- The sensor's whole flat face must seat on a flat, rigid, faced surface at the specified torque; an angled or partly supported sensor or a rough casting transmits poorly. One practitioner drills a common 8 mm-bore sensor to 10 mm to fit M10 bosses and reports no loss over many years; a stepped stud is the alternative but tends to seize in dirty threads.
- V and flat engines: one sensor per bank for per-cylinder control (one is usually enough for audio listening); long inline engines: front and rear.
- If an ECU uses factory sensors, leave them in the best places and put the audio monitor's own sensor in the next-best place; do not tee the audio unit into the ECU's sensor, which changes amplitude and can set faults.
- If knock is not crisp and distinct from background in a location, stop and move the sensor.

### Frequency
- Start from f (kHz) = 1800 / (pi x bore in mm), then test it and about double it. Many factory sensors and strategies use the second (sometimes third) harmonic; typical fundamentals in the sources are 6 to 8 kHz.
- Find the best value by provoking a brief, mild event at low speed and moderate load and seeing which filter shows the clearest step: with a multi-frequency monitor, spread channels widely, pick the winner, then re-centre in smaller steps. A spectrogram or recorded audio with a frequency analysis does the same job. In one demonstration a cylinder-block fundamental near 6.7 kHz gave background readings near full scale at only 10 degrees of timing; the second harmonic dropped the background to about a tenth.
- Narrow-band filters usually beat wide 4-10 or 10-16 kHz bands for background rejection; a wide band can work with a quiet flat-response sensor.
- For headset listening, filter choice is engine specific: try band-pass near the fundamental and 5 and 10 kHz high-pass, and keep whichever makes knock a crisp click over a low hum.

### Gain, window and lock-outs
- Choose overall gain so that, without knock, the peak reading at full throttle close to the rev limit lands near the middle of the scale. Too low and a 10 % margin has no resolution; too high and the channel saturates with no knock. A doubled gain once produced readings near full scale that were pure artefact.
- Use the manufacturer's default crank-angle window unless there is evidence against it; practitioners have rarely needed to move it.
- Equalise per-cylinder gains so every cylinder's no-knock level matches. If one cylinder reads 20 to 30 % higher, a single threshold set above it leaves the quieter cylinders deaf.
- Low-rpm, light-throttle lock-outs are common; with a well-made threshold they are not essential, and light-load knock is both harder to provoke and less damaging. Prioritise protection at high rpm and high load.

### Building the threshold
1. Set the threshold to its maximum so control is armed but inactive.
2. Log ramp runs at near-normal timing from a known-safe map (one practitioner removes only about 2 degrees), confirmed knock-free by ear.
3. Draw the threshold a little above the knock-free profile at each rpm, and on load too where the ECU allows: a table by rpm only left light-load areas mismatched in one demonstration. Practitioners' margins over the clean-run peaks run from roughly a tenth to nearly a third; smooth the line so it follows the noise curve without humps.
4. Ignore samples from throttle lift-off and overrun, the rev limiter and anti-lag when placing it.
5. Repeat a knock-free run and confirm the line is never crossed.

### Validating
Provoke a short, mild knock event in a mid gear at low speed and part load (examples in the sources add 10 to 15 degrees to a few full-load cells near 2000 to 3000 rpm), get in and out quickly, and confirm that the audio monitor, the logged per-cylinder level against threshold, the knock count and the retard all respond together. Adding a large trim to a single cylinder checks per-cylinder attribution. A correctly set system shows a clear gap between noise and knock; a scatter where the two overlap means the setup is wrong. Re-check after big changes: moving to a better fuel with more timing and boost raised background noise enough to cross the old threshold in one case.

### Response settings
Practitioners set modest retard authority (about 4 to 6 degrees in their examples), an aggressive enough first retard to stop knock at once, a short delay and a gradual re-advance. Needing more than about 5 degrees of knock retard suggests the main ignition table is wrong. Several respond with spark retard only, finding added fuel does little; others add fuel or reduce boost as well.

## Worked example
An engine with an 87.5 mm bore: 1800 / (pi x 87.5) = 6.5 kHz, so test near 6.5 and 13 kHz. With gain set so the full-load background near the limiter peaks near half scale, a no-knock ramp at the known-safe timing minus 2 degrees reads, say, 120 at 7000 rpm. A threshold about 20 % above gives 145 there, interpolated down through the rev range to follow the curve. Adding 10 degrees briefly to one cylinder at 3000 rpm, part load, should push only that cylinder well above its line and draw retard on it alone.

## Disputed / conflicts
- **Baseline timing.** Several practitioners build the threshold from runs at low or even zero timing. Others show that background noise grows with timing and power, so a heavily retarded baseline sits far below a properly timed engine's noise and produces false knock later. Discriminating test: log the same rpm range at very retarded and at near-normal timing, both confirmed knock-free by ear, and compare the background levels.
- **Inducing knock.** Most sources deliberately induce brief light knock at low rpm and load to learn its sound and to validate the ECU. One practitioner will not take that risk and relies on a by-ear no-knock baseline. On stock-seal rotaries and very high specific output engines, sources agree inducing knock is too dangerous.
- **Fundamental or harmonic.** The theory favours the second harmonic for signal-to-noise; one practitioner has seen good results with both and could not pick a winner. Test both.
- **Threshold margin.** Starting margins vary between practitioners from 10 % to 30 % above no-knock noise. No source gives a physical basis; the right margin is the smallest that is never crossed on knock-free runs.
- **Engine-specific notes.** The combustion textbook places knock resonance at 3 to 10 kHz by bore and chamber; the practitioners' fundamentals sit in that range, their harmonics above it.

## Citations
- practice: Practitioner training and tuning practice, distilled and cross-checked.
- engineering-texts: Engine, combustion, charging and control engineering texts.
