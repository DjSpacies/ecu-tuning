---
id: principles/boost/exhaust-back-pressure
title: Exhaust back pressure
layer: L1
status: draft
confidence: medium
sources: [engineering-texts, practice]
verified: 2026-11-11
applies_to: {fuels: [gasoline, ethanol, methanol], engines: [turbo, supercharged, na]}
depends_on: [principles/airflow/volumetric-efficiency]
supersedes: []
---

# Exhaust back pressure

## Claim
Exhaust pressure opposes the outgoing gas and holds residuals in the cylinder. On a turbo engine the turbine makes pre-turbine pressure rise steeply with rpm and boost, which reduces VE and knock margin and pushes the wastegate open. The ratio of exhaust manifold to intake manifold pressure is the key measure of how well the hot side is matched: higher means quicker response, lower means more top-end power.

## Why (derivation)
### Residuals and pumping
Higher exhaust pressure leaves more hot residual gas after the exhaust stroke. That displaces fresh charge, raises the temperature of what is trapped and costs pumping work. When exhaust pressure exceeds intake pressure during overlap, the cylinder cannot be scavenged; when intake pressure exceeds it, the engine breathes more like a naturally aspirated one and gains per unit of boost climb steeply.

### Why the turbine sets it
The turbine needs a given amount of energy for a given boost. A small wheel or tight housing (small A/R) extracts it at a high pressure drop: fast spool and a low threshold, but high back pressure and lost top end. A larger wheel lowers pressure (the coarse adjustment); housing A/R fine-tunes it. A big wastegate vents flow but cannot make a tight housing free-flowing, because the turbine still needs its energy for the target boost. Twin-scroll housings use pulse energy better, giving faster response for a given size or allowing a larger A/R for the same response.

### Exhaust pressure and the wastegate
Exhaust pressure acts on the wastegate valve face and helps open it. That is why small turbos taper boost at high rpm with constant duty, why the same spring holds more boost on a free-flowing turbo, and why exhaust pressure spikes (for example during anti-lag) can lift a soft-sprung gate off its seat.

### Things that raise it
- More boost from the same turbine, or holding manifold pressure at altitude, which forces the wastegate further shut.
- Retarded ignition, which moves combustion energy into the exhaust (also raising turbine energy and boost).
- Re-plumbing an atmosphere-vented wastegate into the exhaust, which passes extra flow through the downstream system.
- Extra combustion such as continuous nitrous use through a small turbine.
- Closing variable turbine vanes: in one demonstration, closing the nozzle further at idle raised exhaust pressure from about 11 to about 100 kPa and audibly strangled the engine.

## Assumptions
Exhaust pressure is measured in the manifold, ahead of the turbine. Few installations log it, and the raw signal needs heat protection and a pulsation damper (a mechanical canister in the line) to be usable.

## Breaks when
- At high overlap, exhaust pulses can help or hurt scavenging, so mean pressure alone does not predict VE.
- Pressures in two scrolls or two turbo manifolds are expected to match but often do not; on twin-turbo engines differing wastegate springs can make one turbo work harder, visible per bank in exhaust pressure or shaft speed.
- A matching calculator that predicts high back pressure usually does not feed that back into VE; the user must lower the high-rpm VE assumption.

## Practical use
### Reading the ratio
Log exhaust and intake manifold pressure through a ramp run. Before the run both equal baro. Typical shapes in the sources:
- Exhaust below intake for most of the run, crossing only near the top: a free-breathing match that favours top end; check that full boost still arrives early enough.
- Exhaust about twice boost or more: common on factory turbo engines tuned for low-rpm response, and the reason factory boost peaks near peak torque and tapers.
Ranges quoted by practitioners (opinion, and moving as turbine technology improves): below 1 for high-end drag engines that launch on a two-step, about 1 to 1.5 for circuit cars, about 1.5 to 2 or more for responsive street cars. There is no single correct number; choose by use.

### Diagnostic uses
- Raise boost while logging exhaust pressure: where exhaust pressure escalates and approaches or passes boost, extra boost gives diminishing returns. One drag demonstration stopped raising boost when exhaust pressure exceeded intake pressure while injector duty was near its practical limit.
- Boost taper at high rpm with flat duty on a small turbo: usually the turbine side, with pre-turbine pressure near double boost, not the compressor running out of flow. The tell for the compressor is a charge that superheats while added boost brings little or no power.
- Boost creep at high rpm with very low timing: suspect the timing first. Each timing increase reduced the creep in one demonstration until the curve was flat on target.
- Mixture drifting rich only at high rpm and high boost on a small turbo (when the fuel model assumes VE unchanged): back pressure is reducing VE; correct only that region.
- If timing must be reduced at the top of the rev range without an obvious fuel or temperature reason, ask about turbine sizing and back pressure.
- Lambda reading suspiciously rich pre-turbo: positive exhaust pressure makes a wideband read richer than actual, and leaning to suit it makes the engine leaner than shown. On a naturally aspirated car this is uncommon; compare a collector-mounted reading with a tailpipe probe.
- After fitting a larger turbo, lower turbine inlet pressure reduces residuals and the engine often accepts more advance; still start retarded from the old map and advance toward MBT.
- After re-plumbing a wastegate into the exhaust, recheck boost control and fuelling.

### Exhaust temperature
Pre-turbine temperature matters for the turbine, housing and wastegate. Practitioners give rough ceilings around 950 to 1050 C sustained on gasoline turbo engines, cooler on E85 and much cooler on methanol (roughly mid-700s C), so a safe gasoline value would mean damage on methanol. Readings depend on probe type (exposed tips read faster and higher but die quickly), location and depth; post-turbine sensors read some 200 to 300 C lower and are not comparable. Retarded timing raises readings. Use EGT mainly for spread between cylinders (one practitioner treats 15 to 20 C as matched) and hardware protection, with lambda as the fuel tuning driver.

## Worked example
At 200 kPa manifold and 300 kPa exhaust, the pressure across the engine opposes filling, and a tune that was knock-free at lower speed may need less timing at high rpm. In a matching-calculator example, a small turbo at 7000 rpm and 18 psi boost predicted about 28 psi pre-turbine, 10 psi above boost; the practitioner lowered the high-rpm VE assumption from about 100 to about 90 % to account for it. Moving to a larger housing cut the predicted exhaust pressure by about 1.5 psi and reduced wastegate flow.

## Disputed / conflicts
- Target ratio: one practitioner quotes about 1.1 as a good peak on a responsive street package and modern factory cars at 2 to 2.5; another quotes 1.5 to 2 for street. Both agree the right value depends on use and that a response gain can make a car faster overall despite some lost peak power.
- Lower baro at the tailpipe is sometimes thought to help a boosted engine at altitude; the sources say the extra turbine work and pre-turbine pressure needed to hold manifold pressure outweigh it.
- Textbooks treat residual fraction and pumping from first principles; the practitioner ratios above are practice ranges, not derived limits.

## Citations
- engineering-texts: Engine, combustion, charging and control engineering texts.
- practice: Practitioner training and tuning practice, distilled and cross-checked.
