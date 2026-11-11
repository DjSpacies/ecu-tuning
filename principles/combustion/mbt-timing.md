---
id: principles/combustion/mbt-timing
title: MBT spark timing
layer: L1
status: draft
confidence: high
sources: [engineering-texts, practice]
verified: 2026-11-11
applies_to: {fuels: [gasoline, ethanol, methanol], engines: [all]}
depends_on: [principles/combustion/knock]
supersedes: []
---

# MBT spark timing

## Claim
For any operating point there is a spark timing that gives maximum brake torque (MBT). Torque against advance rises steeply, flattens into a broad plateau, then falls. MBT is best defined as the least advance that reaches the plateau. Beyond it, more advance gains nothing and costs knock margin. Many operating points meet the knock limit before MBT; there the usable timing is set by knock, not by torque.

## Why (derivation)
### Where the optimum comes from
Combustion is a flame that spreads through the charge over a finite crank angle. It is not an instant explosion. Spark too early and pressure builds while the piston is still rising, so the gas does negative work on the compression stroke and knock risk rises. Spark too late and the burn chases a falling piston: peak pressure is lower and arrives later. Several practitioner illustrations show peak pressure roughly halving when spark moves from about 20 to about 13 degrees before top dead centre. MBT is the balance point, and it sits where peak pressure lands in a fairly repeatable window after top dead centre (see principles/combustion/peak-pressure-position).

### Why MBT moves across the map
The burn takes roughly a fixed time for a given charge. The required lead therefore depends on two things: how much time each crank degree takes, and how fast this charge burns.
- **Engine speed:** at higher rpm each degree takes less time, so more advance is needed. The effect is partly offset because turbulence rises with speed.
- **Charge density (load, VE, boost):** a denser charge burns faster and needs less advance. A sparse, light-load charge burns slowly and needs more. Boost acts as an extension of the load axis. It does not change the rule.
- **Together:** along a full-load run, advance usually rises with rpm, dips a few degrees around peak torque (peak VE, the densest charge), then rises again as VE falls. The sources expect this trough. Many also expect it because knock tendency peaks there.
- **Geometry and chamber:** larger bores and offset plugs mean longer flame travel and more advance. A central plug, compact fast-burn chamber and higher compression need less. Practitioners contrast older two-valve, large-bore pushrod designs, which want more, with modern four-valve chambers. Rotary engines generally want less advance than piston engines across the map, and their advance climbs less steeply with rpm.
- **Fuel and mixture:** a slower-burning fuel needs earlier spark to put peak pressure in the same place. Ethanol blends, in areas that are not knock-limited, typically want only about 2 to 4 degrees more than gasoline. Mixture also changes burn speed (see Disputed).
- **Density from altitude:** lower air density acts like lower load and wants a little more advance. Timing left unchanged ends up slightly retarded of MBT, which is safe.
- **Cam phase / profile:** a longer, higher-overlap profile lowers dynamic compression and cylinder pressure. Sources report the high-lift cam on switching-cam engines tolerating a few degrees more than the low cam.

### Why the top is flat
Near MBT the work lost on compression and the work gained on expansion change at almost the same rate, so torque is flat over several degrees. In the sources, being 2 to 4 degrees from MBT typically costs about 1 % torque or less. Practitioners commonly describe a plateau of 4 to 6 degrees on engines that are not knock-limited. Being about 5 degrees short of the plateau can cost around 10 % (one cruise-cell demonstration).

## Assumptions
- Torque is measured at fixed speed and fixed load, with the engine centred in the table cell. Throttle and temperature must be stable.
- Fuel is already on target. Spark timing does not change the trapped mixture, because air and fuel are fixed at intake valve closing, well before the spark. Sources show this with lambda traces that overlay across timing sweeps.
- The torque measurement resolves changes smaller than the gain being judged.

## Breaks when
- **Knock-limited operation:** knock arrives while torque is still rising. MBT then lies beyond the knock threshold and cannot be reached. Practitioners give their experience that most pump-gasoline road engines, and nearly all boosted pump-gasoline engines, are knock-limited somewhere in the map. Figures quoted range from about 75 % to 98 % of cases (opinion, not a measured statistic). On high-octane race fuel, ethanol or methanol the engine usually reaches MBT before knock.
- **Very flat curves:** at light load and higher rpm, torque can barely respond over a wide timing range. Noise, throttle drift or converter slip can then look like a timing effect.
- **Low torque resolution:** at very low rpm or very light load the dyno cannot resolve the change.
- **Peak pressure limits:** a deliberate retard below MBT around peak torque can be used to limit cylinder pressure on head gaskets or connecting rods, and to smooth drivability (see Practical use).
- **Gross retard:** retard does not cause knock, but it moves heat into the exhaust. EGT, exhaust valve and turbine temperature rise, and the extra heat can push the engine back toward knock. Timing far below MBT is not automatically safe.

## Practical use
### Reading the torque response (diagnostic)
- **The size of the gain per step shows the distance from MBT.** A large jump (tens of percent from a very retarded start) means the engine is far retarded. Shrinking gains mean MBT is near. A step that gains nothing means the engine is on the plateau.
- **No gain from advance is ambiguous.** It can mean the engine is at the plateau edge, or that it is already past MBT. Tell them apart by retarding about 2 degrees below the starting value. If torque falls, the start was at MBT. If torque holds or rises, the start was over-advanced, so keep retarding until torque begins to drop. Base maps are sometimes over-advanced at cruise, so this test matters.
- **A peak point reported by sweep software is not MBT when the curve is flat.** Small drift decides where the absolute maximum falls. Take the start of the plateau instead.
- **Trend checks:** at fixed rpm, optimum advance should fall as load rises. A higher-load cell wanting more advance than the cell below it usually means the lower cell was mistuned or copied, not tested. Very large steps between neighbours also point to a measurement error.

### Choosing the value
- Not knock-limited: use the start of the plateau. It gives the same torque with the largest knock margin.
- Knock-limited: find the threshold and set a margin below it (see methodology/steady-state-ignition and principles/combustion/knock).
- When torque differences are within the noise, take the more retarded value. If a dyno cannot see the gain, a driver will not feel it.

### EGT as a secondary signal
Advancing toward MBT lowers EGT. Demonstrations show drops of roughly 70 to 110 C between a heavily retarded setting and MBT at part load. A heavily retarded part-load cell on a lean cruise target can run very hot EGT. So EGT is not a combustion temperature reading: timing moves it independently.

### Without torque feedback
On the road or on an inertia dyno, MBT cannot be found accurately. Most pump-fuel engines are knock-limited, so for them the knock threshold sets the curve, and road and dyno results converge. That convergence is one practitioner's experience. An engine on high-octane fuel needs torque feedback or a conservative known-good map. Proxies such as watching boost or manifold pressure change are judged unreliable by the practitioners.

## Worked example
At 2000 rpm and light load on a stock NA V6, a steady-state sweep showed torque rising steeply from 10 degrees, flattening from about 27 degrees, staying flat to about 36 degrees, and falling well beyond. The sweep software flagged its peak near 36 degrees. The plateau starts at about 27 to 28 degrees, so that is MBT: the same torque with about 8 degrees more knock margin. If knock had appeared near 30 degrees, backing off to about 26 degrees would lose only a few N·m.

A second check: a cell pre-set at 30 degrees shows no gain at 32. Retarding to 28 also shows no change, and only at 24 does torque fall. The original 30 was over-advanced. MBT sits near 26 to 28, and the cell above should be pre-set lower before testing.

## Disputed / conflicts
- **Mixture and burn speed:** one practitioner states that richer mixtures burn more slowly and want slightly more advance, and leaner mixtures less. Another practitioner says lean NA endurance engines need less advance because the lean burn is faster. The combustion textbook places the fastest laminar burning slightly rich of stoichiometric (about lambda 0.9). Burn speed therefore falls on both sides of that point, and very lean mixtures burn much more slowly: one anecdote from a student team needed 5 to 10 degrees more advance near lambda 1.3. The practitioner claims hold only over the range each describes. Discriminating test: sweep MBT at fixed load at several lambda values.
- **Retard as safety:** common advice is "retard if in doubt". The sources agree for unverified cells, but note that gross retard raises exhaust heat and can push the engine toward knock. They prefer timing close to optimal for the load.
- **How close to MBT to run:** some practitioners stop at the first sign of tapering gains, or one step short, accepting about 1 % torque for margin. Others say there is no reason not to run MBT when the engine is not knock-limited. This is a reliability choice, not a physics dispute. One practitioner's view for fragile engines on race fuel is to stop at the start of the plateau even when knock-free.
- **Proportion of knock-limited engines:** the 75 to 98 % figures are practitioners' estimates from experience. No measured survey supports them.
- Textbook cross-check: timing rising with rpm and falling with load agrees with an engine textbook and with the map form in an engine-control textbook.

## Citations
- engineering-texts: Engine, combustion, charging and control engineering texts.
- practice: Practitioner training and tuning practice, distilled and cross-checked.
