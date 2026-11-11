---
id: principles/ignition/spark-and-dwell
title: Spark energy and dwell
layer: L1
status: draft
confidence: high
sources: [engineering-texts, practice]
verified: 2026-11-11
applies_to: {fuels: [gasoline, ethanol, methanol], engines: [all]}
depends_on: []
supersedes: []
---

# Spark energy and dwell

## Claim
An inductive coil stores energy during dwell, the coil charge time. Too little dwell leaves the coil short of saturation and the spark weak, which shows as misfire under high cylinder pressure. Too much dwell adds no spark energy, only heat, and can destroy coils, usually all at once. Once the charge reliably lights, more spark energy gives no more power.

## Why (derivation)
- **Charging:** primary current rises toward battery voltage over resistance with a time constant L/R, and stored energy is ½·L·I². Low battery voltage charges the coil more slowly, so it needs more dwell to reach the same current.
- **Saturation:** once the current plateaus at saturation (typically 5 to 8 A primary in one training session's figures), further dwell only heats the winding and driver. A scope demonstration in the sources shows the effect of inductance: a straight wire reaches several amps almost at once, a coiled wire takes a few milliseconds, and an iron core takes longer still. Each coil therefore has its own correct dwell, and values cannot be copied between coil types.
- **Breakdown voltage:** higher cylinder pressure at the spark needs a higher voltage to jump a given gap. Boost, high compression and added timing at load all raise it, which is why boost exposes weak ignition first.
- **Spark timing matters too:** compression alone raises pressure toward top dead centre. A spark at about 13 degrees before top dead centre must jump at much higher pressure than one at 35 degrees. A heavily retarded "safe" base map can itself cause breakdown misfire on a marginal system.
- **Fuel and mixture:** less volatile fuels such as E85, and very rich alcohol mixtures, are harder to ignite. On methanol the rich limit is set by what the ignition can light.
- **Time available:** at high rpm the time between sparks limits dwell. A distributor coil fires every event and a wasted-spark coil once per revolution, while coil-per-cylinder fires once per cycle and has the most charge time. Some coils also carry a duty-cycle limit: duty = dwell ÷ cycle time, where a four-stroke cycle at 3000 rpm is 40 ms.

## Assumptions
Inductive coil-on-plug, wasted-spark or distributor system. Coil data available, or measurable.

## Breaks when
- **Capacitive discharge systems** store energy differently. They use fixed-duty or system-specific settings, and many need the opposite output polarity. One practitioner's view is that CDI units can be damaged when a misfire leaves the energy nowhere to go, so he prefers good inductive coils for road cars.
- **Short dwell at high rpm:** at very high rpm on distributor or wasted-spark layouts, a minimum discharge (spark duration) time may be needed, and dwell may have to fall to stay inside the coil's duty limit.
- **Ignition-induced faults:** if the coil cannot discharge across the gap, energy may arc inside the coil and damage it. Electrical interference can also cause spark events far from the commanded time. One anecdote describes several rods failing at once on a high-boost methanol engine from random early sparks.

## Practical use
### Setting up the outputs (before connecting coils)
- **Output polarity / spark edge is the first check.** Almost all systems fire on a falling edge. Some OE distributor systems from at least two Japanese and American makers, and some aftermarket CDI units, need rising. The wrong edge holds the coil in dwell whenever it should be idle, so at key-on with no cranking the coil charges continuously and burns out quickly. Configure with coils (and expensive sensors) unplugged. Confirm with the ECU or coil maker when unsure.
- **Know the coil type:** two-pin coils usually need an external igniter. Three- or four-pin coils usually have one built in. Some later coils lack one because the OE ECU contained it, and they will not work driven straight from a logic-level output.
- **Output test mode:** use short pulses (about 3 ms) and listen for each coil's faint tick in the bay. Unplug the coil that should be firing to confirm the cylinder. Never set an ignition drive to constant-on in test mode.
- **Advance and retard clamps:** set them as a backstop against typos or stacked trims. Remember a forgotten low clamp makes timing changes appear to do nothing.
- **Spark latency / ignition delay:** a fixed electrical delay costs more crank degrees as rpm rises. The sources describe 1 to 2 degrees of drift by 4000 to 5000 rpm if it is uncompensated. Set the delay (defaults of tens of microseconds) so locked timing reads the same on a timing light at idle and at high rpm. If left at zero, the error is simply absorbed into the main ignition table.
- **Distributors under ECU control:** phase the rotor so it stays aligned with the cap post across the whole advance range, or the spark can run off the rotor tip at full advance.

### Choosing dwell
- Use the coil or ECU maker's figures as a table against battery voltage. Voltage is the main driver; rpm-based dwell is rarely critical.
- Typical in the sources: about 2.5 to 3.5 ms at 14 V, with a wider 2 to 4.5 ms seen across coils. Base maps have been found with too-short values such as 1.5 to 2 ms.
- A rule of thumb from one training session: at half running voltage expect roughly double the dwell (for example 2.5 ms at 14 V suggests about 5 ms at 7 V). Confirm by clean starting.
- **Unknown coils:** start low (about 1.0 to 1.5 ms), load the engine hard near peak boost and peak torque, and step dwell up 0.1 to 0.2 ms until misfire clears. Then add a margin, because spark energy falls as the coil heats. This approaches from the harmless side: too little dwell misfires, while too much destroys coils. A scope and current clamp on a bench can map dwell to saturation per voltage.
- Repeated coil failures on an aftermarket ECU often point to excess dwell.
- Extra dwell beyond saturation does not compensate for worn coils or fouling. If the coil is at its limit, fit a stronger coil.

### Suspect ignition when
Misfire appears as boost or load rises at a mixture the engine otherwise supports, worst near peak torque. Methodology/ignition-hardware-misfire gives the diagnostic sequence and plug selection.

## Worked example
A misfire appears only above about 180 kPa near peak torque. Dwell is 2.5 ms at 14 V on coils that came with a base map. Raising dwell to 3.0 ms changes nothing, so dwell is not the cause. Closing the plug gap from about 1.1 mm to about 0.8 mm cures it, which points at breakdown voltage. In a second case, at 0.5 ms the engine misfired at about 1.5 bar of boost, was clean from about 1.5 ms, and was set at 2.5 ms for margin. Power was identical at 1.5 and 2.5 ms.

## Disputed / conflicts
- **More spark energy for power:** a common belief is that higher-energy ignition or longer dwell adds power. Back-to-back tests in the sources (dwell 1.5 against 2.5 ms; inductive coils against an aftermarket CDI on a high-boost four-cylinder of several hundred kW) showed no difference beyond run-to-run variation. The practitioner's reading is that a reliably lit flame is self-sustaining. Extra energy matters only where misfire exists. He notes emissions effects were not examined.
- **Dwell figures differ** between practitioners (about 2.5 to 3.5 ms, 3 to 4 ms, 3.5 to 4.5 ms at 14 V) because coils differ. The figures do not conflict: they describe different coils.
- **Wasted spark against direct fire:** one practitioner's view is that wasted spark with good coils works well even at high power. Direct fire helps at very high rpm and boost because each coil has more charge time.

## Citations
- engineering-texts: Engine, combustion, charging and control engineering texts.
- practice: Practitioner training and tuning practice, distilled and cross-checked.
