---
id: principles/fueling/transient-fuel-film
title: Transient fuelling and wall film
layer: L1
status: draft
confidence: high
sources: [engineering-texts, practice]
verified: 2026-11-11
applies_to: {fuels: [gasoline, ethanol, methanol], engines: [all]}
depends_on: [principles/fueling/injector-flow-and-dead-time]
supersedes: []
---

# Transient fuelling and wall film

## Claim
During a load change the fuel reaching the cylinder lags the fuel injected, because part of it joins or leaves a liquid film on the port walls and valve. The film's equilibrium mass rises mainly with manifold pressure, so a rising manifold pressure (tip-in) steals fuel and runs the cylinder lean, and a falling one (tip-out) releases fuel and runs it rich. Transient compensation exists to cover that difference and, separately, the lag in the ECU's own estimate of airflow.

## Why (derivation)

### The film model
A common model (often called X-tau) splits each injection: a fraction X lands on the wall, the rest goes straight into the cylinder. The film then evaporates or is stripped into the airflow with a time constant tau. In steady state the film is topped up exactly as fast as it leaves, so it has no net effect on mixture and does not affect steady-state fuel tuning.

The film's equilibrium size depends on:
- manifold (port) pressure: higher pressure, less evaporation, bigger film. This is the variable that changes fastest during a throttle event;
- port air speed (rpm and airflow): higher air speed strips the film, so it is smaller and matters less;
- wall and valve temperature: cold walls hold far more fuel. Alcohol fuels, with higher heat of vaporisation and more fuel per unit air, make the effect larger;
- injector placement, spray pattern and targeting: sprays aimed at the back of the valve wet less wall than sprays aimed at the port walls or divider;
- injected quantity and fuel pressure.

### Why tip-in goes lean and tip-out goes rich
When manifold pressure jumps, the equilibrium film is larger, so for a few tenths of a second part of each injection goes into building it. An illustrative course example: if the film share is 0.5 ms of a 3 ms pulse at 40 kPa and 1.5 ms of a 6 ms pulse at 80 kPa, a snap from 40 to 80 kPa diverts about 1 ms of fuel per event into the film while it grows. When pressure drops, the film shrinks and its surplus enters the cylinder, so the mixture goes rich.

The demand therefore scales with the change in manifold pressure, not with throttle movement as such:
- a stab from closed throttle near idle swings manifold pressure by 65 to 70 kPa and needs the most fuel;
- a move from 70-80 % throttle to full at high rpm changes manifold pressure little and needs little or none;
- at high rpm air speed carries fuel in, so need falls with rpm and often reaches near zero by about 4500 to 5000 rpm in the sources;
- boost only widens the pressure range; turbo and naturally aspirated engines obey the same logic.

### Throttle rate as a proxy
Most ECUs trigger transient fuel from the rate of change of throttle position, scaled by rpm, starting load and coolant temperature. Throttle rate is not the cause, but it leads manifold pressure and is clean and fast to measure, so it works well and is easy to tune. Some ECUs model the film directly from manifold pressure, rpm and temperature, which can represent both enrichment and enleanment better but has more parameters to calibrate.

### The airflow estimate also lags
A transient lean or rich error is not all film. The ECU's load signal can lag the real air:
- a manifold pressure signal is filtered, and a remote sensor on a long or restrictive hose (extra volume) lags further, so during a stab the ECU briefly fuels from the wrong part of the table. It looks fine in steady state;
- an air mass meter upstream of a long intake tract sees flow before or after the cylinders do; some factory strategies switch to a speed-density estimate during rapid throttle changes for this reason;
- predicted-manifold-pressure strategies use throttle and rpm to anticipate pressure for a short window.

### Other transient effects
- During an acceleration ramp the film is growing continuously, so cells tuned in steady state can read lean in a ramp run (about 5 % in one demonstration), and more so at higher ramp rates. Decelerating at full load reads rich for the same reason.
- When fuel returns after a cut (for example a cut-based shift), some fuel rebuilds the film, so the first events can be slightly lean.
- Plenum volume downstream of the throttle (long intercooler pipework after a throttle-before-blower layout) stores air that must be consumed after a lift, which slows response.
- Changing where the injector aims or when it fires (injection timing) changes the film and so the transient requirement.
- Injectors far from the valve (upstream secondaries, single-point injection, rotary ports) add transport delay; extra unscheduled pulses can help there.

## Assumptions
Port or throttle-body injection. Film parameters are valid only near the operating point and temperature where they were found. The steady-state fuel table is close to right; any error in the cells a transient passes through adds to what looks like film error.

## Breaks when
- Direct injection has different, much smaller wall behaviour; dual-injection engines need different scaling (one calibration settled at about half the port-only default).
- A lean spike after a tip-in may come from a lagging load signal, a lean hole in the steady-state table along the transient path, or extrapolated cells (for example low rpm at atmospheric pressure) that cannot be tuned in steady state.
- Carburetted and single-point systems introduce fuel far from the valve and wet more surface, so the effect is probably larger and slower.
- The wideband's own transport and response delay distorts any reading of a fast event; at idle exhaust flow is so low that the reading is nearly useless for transients.

## Practical use
- Confirm steady-state fuelling first, across every cell a throttle event passes through.
- Check the load signal's own speed: stab the throttle from idle and log manifold pressure against throttle; pressure should rise to near atmospheric almost immediately. If it lags, fix the sensor or plumbing instead of adding enrichment.
- Shape compensation by the physics: most at low rpm, from closed throttle and cold; less as rpm and starting load rise; near none at high rpm and high starting load.
- Expect transient needs to change after changing injectors, spray pattern, injection timing, throttle bodies or intake layout.
- Procedure: `methodology/transient-tuning`. Sensor delay: `principles/data/sensor-lag-and-delay`.

## Worked example
A snap from 40 to 80 kPa at 2000 rpm. With the film share rising from 0.5 ms to 1.5 ms per event, about 1 ms of each injection goes into the wall for the few tenths of a second the film takes to grow. On a 6 ms pulse that is about a 17 % shortfall, which is the order of the lean spike seen with enrichment disabled (sources show lambda rising from about 0.99 to 1.12 from light load, and to about 1.3 from idle). At 40 C coolant the film is much larger than at 90 C, so the same stab needs more enrichment and a longer decay; a table tuned warm will run lean cold.

## Disputed / conflicts
- **What to trigger on.** Physics says manifold pressure; several practitioners still prefer throttle rate because manifold pressure is filtered and slow and a fast enough signal can hurt drivability. One practitioner estimates throttle rate is easier in nearly all cases. Film models based on pressure are described as better when set up well but fiddly; one practitioner's view is that most enthusiasts see little gain over conventional tables. Discriminating test: on the same engine, compare tip-in lambda excursion and feel with each method at equal tuning effort.
- **Textbook vs practice on the target.** The film model suggests full compensation could hold lambda flat; practitioners agree a flat trace is unrealistic because of sensor lag and cycle-to-cycle variation, and that response feel is the judge (see `methodology/transient-tuning`).
- **Ramp-run leanness.** One practitioner treats the lean reading of steady-state-tuned cells in a ramp run as real film behaviour and tunes full load in ramp runs; part of the difference may be sensor delay. Compare with lag-corrected logs.

## Citations
- engineering-texts: Engine, combustion, charging and control engineering texts.
- practice: Practitioner training and tuning practice, distilled and cross-checked.
