---
id: methodology/etc-throttle
title: Electronic throttle control
layer: L2
status: draft
confidence: medium
sources: [practice]
verified: 2026-11-11
applies_to: {fuels: [gasoline, ethanol, methanol], engines: [all]}
depends_on: [principles/control/feedback-and-pid, methodology/idle, methodology/sensors-io-calibration]
supersedes: []
---

# Electronic throttle control

## Claim
An electronic (drive-by-wire) throttle is a safety-critical servo, not just a sensor. Commissioning it means wiring and calibrating redundant pedal and throttle sensors, then using the control settings characterised for that exact throttle body. Once it works, the pedal-to-throttle target table is a torque-shaping tool. Throttle airflow is strongly non-linear, so a 1:1 map makes a powerful engine behave almost like an on/off switch. Shaping the map is how the tuner makes torque follow the pedal.

## Why (derivation)
### Redundancy and supervision
The pedal and the throttle body each carry two position tracks (main and sub), often moving in opposite voltage directions. The ECU cross-checks the pair on each device and compares target with measured blade position. A disagreement, or a tracking error that is too large, triggers a failsafe: throttle drive cut, limp mode, or a very low rpm limit by fuel and spark cut. Some ECUs run a separate supervisor processor for this. A jammed cable throttle has no such protection. Two practitioners report cable throttles sticking part-open at high speed on their own drag cars.

### Servo control
A DC motor driven by an H-bridge moves the blade against a return spring. A PID loop with feed-forward (bias) duty sets how hard it chases error. Plate inertia means it can never track perfectly. The opening side needs more duty than the closing side, because the spring helps closing. With power off, many bodies rest slightly open rather than fully closed; one demonstration body rested at about 6.8 %. Wrong gains give oscillation, overshoot or loss of control, a crash risk that other actuators do not carry.

### Airflow non-linearity
Flow area against blade angle is very non-linear. The sources measured or quoted that most of the airflow rise happens in the first 20 to 30 % of opening, roughly 60 to 70 % of peak flow by 30 % opening, and very little change beyond about 70 to 80 %. A larger bore magnifies the early jump. On a dyno at low rpm, torque at 50 % throttle was within a few percent of full throttle in several demonstrations.

### Latency
A well set up system starts moving the blade about 10 to 20 ms after the pedal moves, and reaches full open some 30 to 60 ms after the pedal does. That compares with about 300 ms for a blink. Cable systems also lag, through slack and flex. The sluggish feel of some early factory cars was deliberate damping for smoothness and mount loads, not a hardware limit.

## Assumptions
- Both pedal tracks and both throttle tracks are wired to analog inputs (on some ECUs, specific high-speed inputs tied to the supervisor).
- The ECU maker supplies PID gains, frequency, dead band and duty clamps for the specific throttle body, or an automatic characterisation routine exists.
- The ECU has enough I/O. Each throttle body needs four analog inputs in total (two pedal tracks, two throttle tracks), and every extra throttle adds two tracks plus a full H-bridge output. Multiple throttle bodies on V engines exhaust inputs quickly.

## Breaks when
- **Unknown throttle bodies**: no characterisation data exists. Some makers will characterise one on the bench if it is sent in. A few bodies (one large aftermarket racing body, one older factory unit) were barely controllable on any ECU, while other common factory bodies control very well.
- **Factory ECUs**: these usually hard-code throttle control, so swapping throttle bodies on a reflash is rarely practical.
- **Setup or calibration modes**: these disable safety checks. The car must not be driven in them.
- **Brake-pedal throttle limits**: these block brake-held burnouts and left-foot staging in drag use, so those applications adjust them.
- **Pedal saturation**: some pedals have a sub track that saturates before the main; set the sub maximum where it stops.

## Practical use
### Commissioning
1. Wire both pedal tracks and both throttle tracks, the motor outputs, 5 V reference and sensor ground. Any pedal with main and sub tracks can be used.
2. Enter the calibration or setup mode and calibrate the pedal first. Record closed, then press firmly to the floor with a foot, as in real driving. A gentle hand press records too low a maximum, so the driver later exceeds it, 100 % is never reached, or a calibration error is flagged. Then run the automatic throttle sweep (end stops, and on some ECUs PID derivation).
3. Load the ECU maker's PID gains, frequency, dead band and min/max duty for that throttle body. Do not invent them; tune by hand only where none exist.
4. If tuning the bias table by hand, zero P, I and D, and place breakpoints just either side of the rest position plus 0 and 100 %. Raise opening-side duty in small steps until position roughly follows target, then set closing-side values negative. Accept imperfect tracking: the closer the open loop gets, the less the closed loop has to correct. Tracking-error shutdown may need disabling during this step only, and must be re-enabled afterwards.
5. Return to the normal mode so safety checks are active. Confirm both pedal channels and throttle position sweep 0 to 100 % smoothly, and that tracks agree. Repeat calibration until the ECU reports it good. One demonstration threw a fault right after calibration and needed a second pass.
6. Make sure the calibration is stored permanently. On some ECUs it is lost at power-down unless written and read back in the documented order.
7. Enable the brake-pedal check where a brake input exists. A faint hum with key on and engine off is the servo holding position, not a fault.

### Idle on the blade
- Modern DBW can idle on the blade alone; early systems kept a separate idle valve because tiny blade moves gave big idle changes.
- Many ECUs scale idle control output to an idle throttle range (for example 0 to 100 % idle output mapped to 0 to 10 % throttle). Too small, and the engine runs out of authority cold and idles low or will not start. Too large, and resolution coarsens and closed loop gets too much authority. Set it during a cold start (the worst case for air demand) so the coldest start does not peg 100 %. Keep running idle output roughly between 10 and 90 %, and finalise it before tuning the base idle table, since changing it rescales that table.
- Typical ranges in the sources are about 6 to 10 % throttle, with some engines needing 12 to 15 %.
- Hot idle can also be trimmed with the zero-pedal row of the target table.

### Shaping pedal to torque
- Measure first. Hold a fixed rpm in a mid gear away from any intake-system changeover (runner switching makes readings fluctuate), step the pedal from minimum to WOT, and record torque at each step.
- Build a progressive, roughly exponential map that opens the blade slowly over early pedal travel. Source examples: 10 % pedal to about 2 to 5 % throttle, 30 % pedal to about 11 to 19 %, 50 % pedal to about 25 to 30 %, steepening toward 100 %. Another example spreads the first 0 to 20 % of plate opening over the first two-thirds of pedal.
- Adjust per rpm column, car and driver. Pull the curve further down as power rises, and finish by driving the car, not only on the dyno.
- Full linearisation can make a low-powered car feel dead. A 1:1 map is acceptable only where full power is usable all the time. Many tuners choose a compromise.
- An oversized throttle body loses low-opening resolution. Choose the smallest body that does not restrict, and use the map to slow early opening.

### Torque management with the target table
- **Peaks and parity**: a 3D pedal by rpm table can cap torque wherever needed. Cutting target to flatten a peak needs iteration over a few ramp runs, with gradual changes across rpm. One demonstration cut to 60 % and left a hole, while 75 % gave a smooth progression. A large step over a few hundred rpm feels erratic. Race series have used this to match very different engines to within about 1 to 3 %.
- **Launch**: the driver goes to full pedal, and the ECU limits opening to the repeatable value needed, because drivers cannot repeat a part-pedal position.
- **Limiter**: rolling the throttle back near the rev limit means the cut has less torque to remove, so limiting is gentler. Many factory strategies do this. After raising a rev limit on a factory ECU, check whether the throttle map still closes near the old limit.
- **Torque reduction**: throttle is an efficient way to reduce torque. The same reduction by ignition retard needs a lot of retard and makes heat. Because of the non-linearity, throttle must come back a long way before torque falls much. Closing the throttle also reduces boost on a turbo engine.
- **Switchable maps**: these serve breakout rules or endurance fuel use. Less airflow also means less fuel.
- **Detuned variants**: factory lower-spec variants are sometimes limited only by throttle mapping on identical hardware.

### Downshift blip
- The throttle is fast enough; engine rotating inertia (flywheel, clutch, damper) limits how fast revs can rise in the short neutral window. Check by snapping the throttle at about 3000 rpm in neutral.
- Use an rpm-based blip table and tune it per engine. Too little blip risks compression locking the driven wheels; too much hits the overspeed cut, the lesser evil but harsh and loud. Tune to just match revs.
- A minimum throttle against rpm on overrun (a few percent) keeps the plenum out of deep vacuum so the blip responds sooner. Balance it against reduced engine braking.
- Start on a roller dyno, then refine on track with wheel speed and rpm logs, since dyno inertia differs from the track.

## Decision rules
- Never invent throttle PID, frequency or clamps when characterised values exist.
- Never drive in setup or calibration mode, and re-enable any check disabled for set-up.
- Do not connect unusual inputs to throttle cutting. ECUs restrict what can interact with DBW for safety, and at most a digital input selecting between target tables is reasonable.
- Calibrate pedal maximum with a firm foot.
- Shape the map to torque, then confirm by driving.

## Data gates
- Pedal main and sub, throttle main and sub, throttle target and actual, motor duty, and fault or limp status logged.
- Idle output (duty within its range) during a cold start and hot idle.
- Torque against throttle at fixed rpm for map shaping.

## Worked example
A naturally aspirated V6 at 2200 rpm in fourth gear on a 1:1 map made about 420 to 425 Nm at WOT and over 400 Nm at 50 % pedal. The top half of the pedal travel therefore controlled about 5 % of the torque. Re-mapping 50 % pedal to about 25 % throttle dropped torque at that pedal to about 300 Nm (about 71 % of WOT), and 30 % pedal to about 11.5 % throttle extended the controllable range. The goal is torque fraction close to pedal fraction: at 50 % pedal, 50 % of 425 Nm would be about 212 Nm, so a strict linearisation would close the blade further still. The practitioner chose a compromise for feel.

## Disputed / conflicts
- **DBW lag and safety**: a common belief holds that drive-by-wire is inherently slow, spongy or unsafe. Practitioners in several sessions dispute it with latency measurements and the redundancy argument. They attribute the reputation to deliberately soft early factory calibrations. Consistent across sources; the belief persists among users.
- **How far to linearise**: one source fully linearises torque against pedal. Others warn that this makes low-power cars feel sluggish and choose a curve between 1:1 and fully linear. Driver preference decides.
- **Hand-tuning gains**: several sources say never self-tune throttle gains, while some ECUs derive gains automatically and one demonstration hand-tuned the bias table. Common ground: use characterised or automatically derived values first, and keep supervision active.

## Citations
- practice: Practitioner training and tuning practice, distilled and cross-checked.
