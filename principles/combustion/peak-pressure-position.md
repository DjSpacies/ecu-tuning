---
id: principles/combustion/peak-pressure-position
title: Peak cylinder pressure timing
layer: L1
status: draft
confidence: high
sources: [engineering-texts, practice]
verified: 2026-11-11
applies_to: {fuels: [gasoline, ethanol, methanol], engines: [all]}
depends_on: [principles/combustion/mbt-timing]
supersedes: []
---

# Peak cylinder pressure timing

## Claim
At or near MBT, peak cylinder pressure occurs roughly 15 to 18 degrees after top dead centre. Peak pressure is what drives torque, and this window is where it has the best leverage on the crank. The figure explains why timing must move with speed, load and fuel. It is a target only when cylinder pressure is actually measured.

## Why (derivation)
- Gas pressure turns the crank only through connecting-rod angularity. At top dead centre the rod is in line with the crank, so pressure there produces almost no rotation and only loads the bearings. A few degrees later the effective lever arm grows, while expansion is already reducing pressure. The best compromise puts the pressure peak a little after top dead centre.
- Combustion takes a finite crank angle. The spark must lead the target window by the burn time converted to degrees. Higher rpm (less time per degree) and slower-burning charges therefore need more lead. Faster-burning, denser charges need less.
- Higher compression also means a higher expansion ratio. The gas expands and cools more before the exhaust opens, so more of the pressure becomes work and less leaves as exhaust heat. This is one practitioner illustration comparing equal peak pressure at two compression ratios.
- Rod-to-stroke ratio and chamber geometry shift the best angle slightly. The sources describe this as a second-order effect beside burn speed.

## Assumptions
Pressure is measured, or the figure is used only to explain timing behaviour.

## Breaks when
- **Knock-limited operation:** the spark is retarded, so the peak lands later than the optimum.
- **Deliberate pressure limiting:** around peak torque, peak pressure is highest. One practitioner treats it as the point where head gasket clamping becomes the weak link at high specific output. He prefers retarding about 5 to 8 degrees through that region over tapering boost, because timing can be restored faster than boost after peak torque.
- **Ring seal and blow-by:** pressure that escapes past the rings does no work. One practitioner's view is that ring seating depends on cylinder pressure getting behind the top ring, so long idling during break-in gives poor seating. He recommends cycling moderate load with closed-throttle periods.
- **Thermal limits:** a lean or hot condition can grow the piston and close running clearance, and a too-tight ring gap can butt. Failures blamed on pressure can be thermal in origin.

## Practical use
- Use the window to explain table shape: advance rises with rpm, falls with load, and dips around peak torque.
- Use it to explain fuel effects: a slower fuel needs earlier spark to reach the same window.
- Without pressure sensing, find the window indirectly as the timing that gives peak torque on a load-holding dyno (principles/combustion/mbt-timing). Peak torque on the dyno coincides with correct peak-pressure location.
- In-cylinder pressure sensors (including pressure-sensing spark plugs) show the trace directly, and detonation appears as obvious oscillation on it. Sources note that cost has fallen. One practitioner's view is that they are not yet cost-effective for most tuners, and a dyno is still needed for everything else.
- Do not state a target angle to a user without pressure data.

## Worked example
At a fixed rpm, advance must rise because the same crank position has to be reached in less time. Retard with load comes from the faster burn of a denser charge. An practitioner illustration: at about 20 degrees before top dead centre the peak lands near 16 to 18 degrees after, at around 80 bar. At about 13 degrees before, the peak arrives late at around 40 bar, roughly half the torque. At about 35 degrees before, pressure builds against the rising piston and knock risk rises.

## Disputed / conflicts
- The combustion textbook gives about 15 degrees after top centre. Most practitioners give 16 to 18, and one training series gives 15 to 20. All describe the same idea, and the spread does not affect practice.
- The practitioners add that the best angle varies slightly with engine geometry. They advise against predicting timing from geometry, and finding MBT from torque instead.

## Citations
- engineering-texts: Engine, combustion, charging and control engineering texts.
- practice: Practitioner training and tuning practice, distilled and cross-checked.
