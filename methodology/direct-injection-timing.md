---
id: methodology/direct-injection-timing
title: Direct injection timing
layer: L2
status: draft
confidence: medium
sources: [practice]
verified: 2026-11-11
applies_to: {fuels: [gasoline, ethanol, methanol], engines: [all]}
depends_on: [applications/direct-injection, methodology/closed-loop-fuel]
supersedes: []
---

# Direct injection timing

## Claim
In direct injection the whole event must fit between intake opening and a safe margin before the spark. That window is fixed in crank degrees and shrinks in time as rpm rises. Within it, injection angle has a large, measurable torque effect (several percent, up to about 10 % in demonstrations), unlike port injection. It is tuned like an ignition sweep, against torque.

## Why (derivation)
### The window
A four-stroke cycle takes 720 crank degrees, and cycle time is t_cycle = 120 / N seconds (N in rpm). The crank turns 6 x N / 1000 degrees per millisecond. DI fuel can only go in during the intake stroke and part of compression, and must finish well before ignition. That leaves roughly 300 to 320 of the 720 degrees, under half the cycle. Duty on DI is therefore relative to that window, not the full cycle, and ECUs define DI duty differently.

Degrees occupied: theta_inj = PW (ms) x 6 x N / 1000.
End angle (both measured before compression TDC): EOI = SOI - theta_inj.

### What can go wrong at each end
- **Too early**: if injection starts while the exhaust valve is still open (around overlap), fuel goes straight out the exhaust. A port injector spraying a closed valve only stores fuel for the next cycle; DI has no such buffer. Spraying early at a piston near TDC can also put liquid fuel on the crown, and on some engines damage it.
- **Too late**: fuel injected close to the spark has no time to mix, giving poor combustion and rough running. Rising cylinder pressure also opposes late injection, which is one reason DI rail pressure is so high.

### Why angle changes torque
Where in the cycle the fuel lands sets how well it mixes with the air (spray targeting into a piston bowl matters on some designs). It also sets how much of the evaporation heat comes from the trapped charge rather than from metal. Charge cooling raises density and the knock limit, which is the basis of DI's compression and timing advantage. So the angle changes both burn quality and knock margin. Often it does this without changing the delivered fuel mass, which is why the wideband may not move.

### Pressure and pulse width
More airflow lengthens the pulse. Raising rail pressure shortens it and helps fit it in the window, within pump and injector limits. Injector opening latency shifts the real start of delivery later than the commanded angle. At high rpm that delay is a large number of crank degrees.

## Assumptions
- The software's timing reference is known: start, end or centre of injection, and from which TDC (some ECUs count from compression TDC, some from a different zero). Know what the value zero means.
- Rail pressure is measured and under control.
- The number of pulses per cycle (one to three, depending on strategy) is known, since each needs its own window.
- A load-bearing dyno is available for torque sweeps. Without one, closed-loop trim is a weaker proxy.

## Breaks when
- **Reference mismatch**: carrying the port-injection habit of an end-of-injection reference onto DI can hide a fatal error. As pulse width grows, a fixed end pushes the start earlier, eventually into the exhaust stroke.
- **Latency at high rpm**: the commanded start excludes opening delay. A factory map that seems to start inside the exhaust stroke at high rpm may in fact deliver after TDC. Copying such angles to a different injector or pressure is not safe.
- **Multi-pulse strategies**: the single-window arithmetic applies per pulse.
- **Combined DI and port engines**: the port share must be zeroed while sweeping DI angle, or the result mixes two effects.
- **Ignition advance at light load**: light-load spark can be 35 to 40 degrees or more BTDC, far more than at WOT. An end limit set as a fraction of the stroke rather than an angle from spark can then be too close.

## Practical use
### Set-up
1. Find the timing reference and convert to the one that answers the question. The start angle shows exhaust-stroke risk; the end angle shows spark margin. Compute the other from pulse width and rpm whenever the ECU does not display it.
2. Set an end-of-injection limit with a margin before the most advanced spark likely to be used. Sources use around 30 to 40 degrees before that spark; one engine used 60 degrees BTDC. The margin varies by engine.
3. Base table: on a reflash, start from the factory calibration, which is usually close. On a standalone, one practitioner base is a 2D table against rpm with start about 320 degrees before compression TDC, ramping later toward about 375 at very high rpm, with an optional throttle or load axis. DI justifies more table resolution than port injection does.
4. Watch pulse width. Combined DI and port engines use the port injectors to keep DI pulse width in the window (a rule of thumb of about 6 to 7 ms maximum at high rpm). DI must never be fully staged out, because fuel flow through the injector cools its tip.

### Steady-state sweep (load-bearing dyno)
- Hold rpm and MAP very steady in the cell centre with fixed ignition and lambda on target (closed loop is acceptable). Load drift corrupts the torque trace.
- Step the angle about 10 degrees in one direction. Reverse when torque drops, settle on the peak, then move to the next load row. Change surrounding cells together so interpolation does not blur the result.
- Read the result to about 5 degrees. The trace is noisy, and a clear plateau is more useful than a single best value.
- Once torque falls steadily in one direction, stop going that way.
- Make small moves on unfamiliar engines. Torque fell sharply after only 10 to 15 degrees the wrong way in one demonstration.

### Ramp runs (high rpm and load)
Treat it like cam or ignition optimisation. Run a baseline, shift the whole region by a large step (about 20 degrees), follow any direction that gains, then refine with 10 and then 5 degree steps. Steps of 2 to 5 degrees will not show in ramp data. Areas already optimised in steady state will likely go backwards, which is expected.

### Without a dyno
At lambda 1 in closed loop, the angle that needs the most fuel to hold target matched the torque optimum closely in one demonstration. Trim can therefore point the direction, less clearly than torque. Each angle change moves the fuelling, so fold trims back into the fuel table afterwards; trims are only a temporary fix.

## Decision rules
- Always compute both ends of the injection event. Start must not fall before intake opening (overlap) unless a factory map with known latency says otherwise. End must keep the spark margin.
- Torque is the authority. Lambda may stay constant while torque changes by 10 % or more.
- Factory DI maps are a safe base, but they were chosen for emissions. Optimise for torque only where emissions compliance is not required.
- Coverage in the sources is mostly one engine family. Check angles against the platform's own documentation and treat the numbers as examples.

## Data gates
- Logged rpm, MAP, pulse width, rail pressure (target and actual), injection angle (and its reference), ignition advance and lambda.
- Derived: start and end angle per pulse, and the spark-to-end margin, in every row used.
- Rail pressure at target during sweeps, since pressure changes pulse width and spray.
- Port share zero (combined engines) while DI angle is swept.

## Worked example
### Window arithmetic
At 6000 rpm, t_cycle = 120 / 6000 = 20 ms, and the crank turns 720 / 20 = 36 degrees per millisecond. An 8.5 ms pulse occupies 8.5 x 36 = 306 degrees. Starting at 360 degrees before compression TDC (start of intake), it ends at 360 - 306 = 54 degrees BTDC. With spark near 25 to 30 degrees BTDC under load, that is a marginal 25 to 30 degree gap, inside the 30 to 40 degree margin the sources use. More pressure or an earlier start would be needed.

### Torque sweep
In one demonstration on a 2.0 L DI engine (DI only, port disabled), at 3000 rpm and 60 kPa with fixed 34 degree ignition and lambda 1, peak torque was about 126 Nm with start at about 312 degrees BTDC. There was a plateau from about 305 to 325 degrees, a sharp fall toward 200, and a clear loss at 360. That matched the factory map. In the 80 kPa row, a 40 degree change took axle torque from about 530 to about 585 Nm, roughly 10 %.

## Disputed / conflicts
- **Reference choice**: one demonstration swept DI using an end-of-injection reference successfully, while another lesson warns that end referencing on DI pushed injection into the exhaust stroke unnoticed, and recommends start-of-injection. A further source states start referencing is the norm for DI and end for port. Resolution in this entry: either reference works only if the other end is calculated and checked.
- **Lambda as a guide**: one demonstration found DI angle changed torque with no lambda change, so torque was the only feedback. Another found closed-loop trim moved by about 2 % and tracked the torque optimum. Both may hold: trim shows burn-efficiency changes at lambda 1 that an open-loop wideband reading may not resolve. Test: sweep the same cell open and closed loop and compare.
- **Injecting near TDC**: factory practice on at least one engine injects near intake TDC at high rpm with a gain (explained by latency and a piston bowl). Another warning says spraying at a piston near TDC can damage pistons on some DI engines. Do not generalise either.
- **Thin coverage**: the instruction base is a handful of lessons largely on one engine family. Treat with caution.

## Citations
- practice: Practitioner training and tuning practice, distilled and cross-checked.
