---
id: applications/direct-injection
title: Direct injection profile
layer: L4
status: draft
confidence: low
sources: [engineering-texts, practice]
verified: 2026-11-11
applies_to: {fuels: [gasoline, ethanol, methanol], engines: [all]}
depends_on: [principles/fueling/injector-flow-and-dead-time]
supersedes: []
---

# Direct injection profile

## Claim
Direct injection puts fuel into the cylinder at high pressure. That adds limits a port engine does not have: a crank-angle window, high-pressure pump capacity, a minimum deliverable quantity, and injector tip cooling. Injection timing also matters far more than on port injection. The core fuel and ignition process is otherwise unchanged, and DI engines still need transient and cold-start fuelling.

## Why (derivation)
- **Charge cooling**: the fuel evaporates in the cylinder and takes most of its heat from the trapped charge rather than from port walls and valves. That raises charge density and the knock limit, so DI engines carry higher compression and more advance. The benefit depends on when in the cycle the pulse happens.
- **Window**: fuel can only enter during intake and part of compression, ending well before the spark. That is roughly 300 to 320 of 720 crank degrees, shrinking in time as rpm rises (methodology/direct-injection-timing). Pulse widths in a DI base table therefore look very small compared with a port engine; that is normal.
- **Pressure**: high rail pressure is needed to fit the fuel into the window and to inject against rising cylinder pressure. Raising the pressure target at high load shortens pulse width, within pump limits. Rated DI flow is meaningless without the pressure it was measured at. One course example quotes a DI injector at about 12.5 ml/s at 10 MPa against a port injector at about 3.3 ml/s at 400 kPa.
- **Minimum quantity**: DI injectors have a hard minimum deliverable quantity (about 3 microlitres in one example; effectively zero for a port injector). The ECU must respect it at idle and on overrun.
- **Tip cooling**: the injector sits in the combustion chamber and is cooled by fuel flowing through it. On engines that also have port injectors, DI must never be staged fully out.
- **Film effects remain**: no port wetting, but fuel can still wet the cylinder wall or collect in the crevice between piston and head. Cold walls behave much like cold ports, so transient and cold-start enrichment are still needed, generally smaller than on port injection.
- **Why some engines add port injection**: one practitioner's reading of the maker's technical papers is that DI alone mixes poorly at low air speed because events are short. That needs turbulence-generating ports that cost high-rpm flow; adding port injection lets the design keep a high-flow port and still mix well at low speed. It is not mainly about capacity on that engine.

## Assumptions
- Rail pressure is measured and logged against its target.
- Injector characterisation (flow at stated pressure, latency, minimum quantity) is available, or the factory calibration is retained.
- The platform's handling of DI duty, timing reference and pulse count is documented.

## Breaks when
- **Port rules on dead time and wall film do not transfer directly**: the magnitudes differ, and latency is a large crank angle at high rpm.
- **Big power on factory DI**: stock DI injectors and high-pressure pumps run out well before high boost. Aftermarket DI parts are scarce, and DI flow and latency data are nearly impossible to obtain, so calculator sizing is moot.
- **Combined DI and port engines**: duty-cycle matching between the two sets is the wrong goal. The useful DI limit is pulse width (window), not duty.
- **Injection timing**: injecting too early can spray the piston crown or lose fuel to the exhaust; too late gives poor combustion.

## Practical use
- Treat DI injection timing and high-pressure fuel control as separate, DI-specific tasks. The main VE, lambda and ignition process can be taught and done as for a port engine. One course does exactly that on a turbo DI engine running an ethanol blend.
- **Pulse width**: on DI plus port engines, use the staging (secondary share) table to keep DI pulse width inside the window at high rpm. Sources use about 6 to 7 ms maximum as a rule of thumb; one demonstration ran about 3.5 ms at high rpm with staging. Never set port share to 100 %.
- **Fuel system headroom**: log rail pressure actual against target at WOT. A falling actual with rising pulse width means the pump is at capacity. For power beyond factory DI capacity, the sources fit supplementary port injection (for example injectors in a spacer under the intake manifold) run by an ECU that controls both, as some factory engines already do.
- **Timing**: start from the factory map, sweep against torque, and calculate both ends of the event (methodology/direct-injection-timing).
- **Transients and cold start**: still tune them, with smaller expected magnitudes than port injection.
- Combining overlap-based idle strategies (cam overlap at idle, for example) with DI carries no special risk beyond the usual rule that injection stays clear of the spark.
- Instruction coverage is thin and centred on one engine family. Treat DI work as needing extra caution and the platform's own documentation.

## Worked example
At 7000 rpm the crank turns 6 x 7000 / 1000 = 42 degrees per millisecond. A 7 ms pulse occupies 294 degrees, close to the whole 300 to 320 degree window. That is why sources treat about 7 ms as a rough ceiling at that speed. If airflow rises 20 % at constant pressure, the pulse needs about 8.4 ms (353 degrees) and no longer fits. Raising rail pressure helps: flow scales roughly with the square root of the pressure difference, so a 44 % rise gives about 20 % more flow and brings the pulse back near 7 ms, if the pump can supply it.

## Disputed / conflicts
- **Why combined DI and port**: one practitioner attributes the port injectors on one engine to low-speed mixing and port design, not capacity. For aftermarket high-power builds, added port injection is used mainly for capacity. Both uses exist.
- **DI and transient fuel**: a common belief is that DI needs no transient or cold-start compensation. The sources disagree with that, citing wall and crevice film. Magnitudes are smaller but not zero.

## Citations
- engineering-texts: Engine, combustion, charging and control engineering texts.
- practice: Practitioner training and tuning practice, distilled and cross-checked.
