---
id: methodology/injection-timing
title: Port injection timing
layer: L2
status: draft
confidence: medium
sources: [practice]
verified: 2026-11-11
applies_to: {fuels: [gasoline, ethanol, methanol], engines: [all]}
depends_on: [principles/fueling/injector-flow-and-dead-time, methodology/transient-tuning, methodology/direct-injection-timing]
supersedes: []
---

# Port injection timing

## Claim
On sequential port injection, the injection angle sets how the fuel arrives at the valve: as vapour off a hot closed valve, or as spray through an open one. It changes economy, transient response and sometimes torque. Gains are usually small (a few percent) and appear only where injector duty is low, at idle, cruise and low rpm. The angle is found by experiment. At fixed pulse width, the angle that reads richest (or makes most torque) is delivering fuel in the most burnable form.

## Why (derivation)
### When timing can matter at all
Phasing is controllable only with sequential (or semi-sequential) injection. That needs a cam phase reference, one driver per injector (or pair), and wiring to match. Crank-only or factory batch-wired engines run batch fire, where some cylinders get fuel against an open valve and others against a closed one. That gives uneven mixture preparation, most visible at idle with large injectors.

Duty sets the room to move. The intake valve is open for only about 30 to 35 % of the 720 degree cycle. Above that duty, some fuel must land on a closed valve whatever the angle. At peak power port injectors commonly run 70 to 95 % duty and are open nearly the whole cycle, so timing barely matters there. Short pulses at idle and cruise leave the most freedom. Port injectors can and do spray against the closed valve during compression, power and exhaust strokes; the fuel waits in the port for the next intake event. Restricting injection to valve-open time would cap duty around 30 %.

### Closed-valve and open-valve injection
- **Closed valve** (end of injection roughly 360 to 450 degrees before firing TDC in typical factory maps): fuel lands on the hot valve back and port wall and flashes to vapour before the valve opens. Vapour burns better than even fine droplets, which is why most factory calibrations use it. It assumes a warm engine.
- **Open valve** (end around 180 degrees before firing TDC as typical): fuel is carried in as mist with less wall wetting. At light load and low rpm the pressure across the injector tip pulses erratically once the valve opens, which can disturb delivery.
- Which wins depends on the injector (atomisation, spray targeting at the valve back or the port wall), distance from the valve, fuel pressure, engine temperature and air speed. Transport time depends on air velocity, so high rpm and load may want a different angle than idle.

### Transients
If a cycle's fuel was already placed on a closed valve before the throttle opened, the next intake event draws more air with fuel sized for the old condition, so a lean tip-in is guaranteed. Open-valve timing at low rpm lets the ECU lengthen a pulse that goes straight in with the extra air. Acceleration enrichment that seems to need excessive values may be compensating for poor timing.

### Reading the result
At constant pulse width the delivered fuel mass is fixed. A richer lambda reading therefore means more of that fuel is burning (arriving in combustible form); leaner means fuel is going unburnt. Once the better angle is found, fuel can be removed from the VE table to restore target, saving fuel for the same mixture.

## Assumptions
- Sequential injection with correct firing order and cam phase reference.
- The ECU's timing reference is known: start, end or centre of injection, and what zero means. On most ECUs, angles are crank degrees before compression TDC with end-of-injection reference; some ECUs place zero elsewhere (for example zero meaning 360 degrees before firing TDC).
- Engine at operating temperature for the main sweep.
- Pulse width held fixed (closed loop off, or the trim read) during a sweep.

## Breaks when
- High duty (above about 35 %, and certainly at 70 to 90 %): little or no authority.
- Batch, group or throttle-body injection: timing is largely irrelevant. Single-point injection before or just after the throttle is a dated, inefficient layout.
- Cold engine: the hot-valve vaporisation argument fails. Open-valve injection during cold start may help (one practitioner, from published factory and SAE material rather than his own testing).
- Staged injectors at very different distances from the valve would ideally need separate timing. Many ECUs offer only one table, and the gain from refining it is small.
- Start-of-injection reference: the start moves with rpm and pulse width, so an SOI table must vary heavily with both and the end point drifts relative to the valve. End-of-injection stays where it is placed.
- Siamese-port engines: an injection split feature exists to stop one cylinder robbing another's fuel; one practitioner never needed it.
- Firmware limits on how late the end can be (one ECU stopped port end of injection at about 120 degrees BTDC).

## Practical use
### Set-up
- Use sequential whenever cam sync, drivers and cylinder count allow. Large injectors (around 1700 to 2200 cc/min in one source) never run as smoothly without it. Changing injection mode often requires storing settings and a power cycle.
- Reference to end of injection for port engines and know which reference is selected; the meaning of the numbers depends on it.
- Neutral starting values in the sources range from about 330 to 400 degrees before firing TDC (end). A single value is a fine start; convert to a table vs rpm when refining. A 2D rpm table is usually adequate. 3D load tables rarely repay the effort on port injection, though they can be more precise.
- Cam card valve events locate the window. Intake opening is typically around 390 to 420 degrees before firing TDC, and closing can be 50 to 60 degrees after BDC with performance cams. Calculating from injector-to-valve distance is not needed; start anywhere and test.

### Steady-state sweep
1. Hold rpm and load fixed, lambda on target, closed loop off (or watched). Lock pulse width.
2. Step the angle in large increments (about 50 degrees) across the range, or 10 degrees near a candidate. Change surrounding cells together to avoid interpolation effects.
3. Wait for equilibrium at each step and ignore the brief spike after a change.
4. Pick the angle where lambda settles richest, or preferably torque is highest. If torque rises without a lambda change, chase torque.
5. Re-correct VE to target at the chosen angle, then refine with finer steps watching torque. It is iterative, like cam timing.
6. At idle, where the dyno shows no torque, rising idle rpm is the torque indicator (as with idle ignition).
7. With closed loop active, the angle needing the least correction (running richest for the same pulse) is the better one.

### Ramp runs and the full table
Shift the whole table in 20 to 100 degree steps on ramp runs (for example 350, 400, 450) to find direction. Continue until nothing changes, then refine. As a minimum check, shift the whole table up and down 50 to 100 degrees on ramp runs; if nothing moves, leave the defaults.

### Where to spend effort
Idle, cruise and low rpm (below about 4000 rpm in two sources). Engines with large injectors on small engines, and ITB engines with injectors in the trumpets (long transport), respond most. Rotary engines follow the same principle with port timing instead of valves: make coarse moves of about 50 degrees and let torque or the AFR shift guide. One practitioner's rotary result ended close to factory timing. Ethanol blends rarely need a different angle, a last-few-percent refinement. Race classes with injector restrictions sometimes size injectors for about 60 to 65 % peak duty to keep timing authority at high load.

### Always road test
One practitioner found that a dyno-optimised angle hurt transient enrichment behaviour on the road. Wrong timing carries no mechanical risk, but drivability can outweigh a 1 to 2 % torque gain.

## Decision rules
- Do not expect power from port timing; expect small economy and response gains at low duty.
- A richer reading at fixed pulse width means a better angle. Confirm with torque where it is measurable, and look for consistent trends over more than one step, not single spikes.
- If acceleration enrichment seems excessive at low rpm, test open-valve timing before adding more enrichment.
- Leave timing at defaults if a whole-table shift of 50 to 100 degrees shows no change.

## Data gates
- Injector duty (or pulse width with rpm) per site. Sites above about 35 % duty cannot be all open-valve, and sites above about 80 % will show little effect.
- Lambda settled at each step, with pulse width constant (closed loop off, or the trim logged).
- Injection angle and its reference logged.

## Worked example
### Open-valve feasibility
At 3000 rpm the cycle takes 120 / 3000 = 40 ms, so a 35 % open-valve window is about 14 ms (about 250 crank degrees). A cruise pulse of 4 ms (10 % duty) fits easily, so its placement can be chosen freely. At 7000 rpm the cycle is about 17 ms; a WOT pulse of 15 ms (about 88 % duty) leaves almost nothing to move.

### Sweep result
In one demonstration on a port-only 2.0 L flat-four at 3000 rpm and 60 kPa, moving end of injection from 450 degrees BTDC (closed valve) to 300 and then 200 degrees added about 10 to 20 Nm. Lambda moved 1 to 2 % richer at unchanged pulse width. Fuel was then removed from VE to restore target. On a V6 at 2000 rpm light load, moving from 450 to about 300 degrees raised torque from about 100 to about 108 Nm (about 8 to 10 %) with tiny lambda change, then fell back toward open-valve. On a four-cylinder at idle, about 250 degrees (open valve) looked best.

## Disputed / conflicts
- **Size of the benefit**: several sources call port timing a small refinement (a few percent economy, slightly crisper response, often ignored by good tuners). Demonstrations at light load showed 8 to 10 % torque on one V6 and 10 to 20 Nm on a flat-four. Both hold: the gain depends on the engine and on duty, so test it.
- **Closed or open valve**: closed-valve vaporisation off a hot valve is the factory default and is argued as better once warm. Open valve carries mist with less wetting and helps tip-in. At light load the erratic tip pressure can favour closed valve again. Factory choices are driven by emissions and are not automatically best for torque. Dyno results on different engines found the best at open-valve angles (about 200 to 300 degrees). The test is a sweep on the engine in question.
- **Lambda against torque**: the richest-lambda rule is widely taught, but one WOT sweep found the richest-lambda angle near the lowest torque. The variation was only about 4 Nm against noise. Use lambda to find a region, then torque to decide.
- **Starting value**: the sources variously suggest about 330, 340, 360 and 400 degrees (end, before firing TDC) as neutral starts. All agree the start barely matters because the sweep decides.
- **Table dimension**: some sources prefer a 2D rpm table as adequate; others note a 3D table against load can be more precise since transport time varies with air velocity. The difference is small on port injection.

## Citations
- practice: Practitioner training and tuning practice, distilled and cross-checked.
