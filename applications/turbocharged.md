---
id: applications/turbocharged
title: Turbocharged profile
layer: L4
status: draft
confidence: high
sources: [practice, engineering-texts]
verified: 2026-11-11
applies_to: {fuels: [gasoline, ethanol, methanol], engines: [turbo]}
depends_on: [principles/boost/compressor-and-surge, principles/boost/exhaust-back-pressure, principles/boost/intercooling, methodology/boost-control, methodology/thermo-charge-temp-estimation]
supersedes: []
---

# Turbocharged profile

## Claim
A turbocharged engine responds to fuel and timing exactly as an NA engine does; what differs is that it runs knock-limited over much of its boosted range, builds heat quickly, and leaves less margin for error at its higher specific output. Its fuelling and timing must be proven at minimum boost first and then in small boost steps, with richer targets and less timing as boost rises, a declared boost ceiling, and protection set before the first boosted run.

## Why (derivation)
Boost multiplies air mass and cylinder pressure. A denser charge burns faster, so MBT needs less advance as boost rises, while more fuel and air burned means more heat, so lambda targets move richer through positive boost. Back pressure, charge temperature and turbine response tie boost to rpm, gear and thermal history, so the load the engine reaches depends on how it got there. Higher specific power means a lean spot or knock does damage faster, and an overboost can take the engine out of its tuned range in moments.
Two terms are often confused. Boost threshold is the lowest rpm at which full throttle can make full boost, set by available exhaust energy against required shaft speed. Lag is the delay to regain boost after a lift when already above threshold, set mainly by rotating inertia (on modern turbos it is of the order of a tenth of a second). Lighter turbine wheels improve both.

## Assumptions
Boost control is stable and a limit is configured. Load axes extend past the boost target. Coolant, intake and oil temperatures are monitored throughout.

## Breaks when
- A very high minimum (spring) boost changes which cells can be reached in steady state.
- Heat soak changes the limit during a pull, and holding a boost cell lets boost drift upward as the exhaust heats, blending into the next load row.
- At low rpm the turbo lacks the exhaust energy to reach the upper load rows at all; those cells must be extrapolated.
- A small turbo pushed past its efficiency at high rpm reduces VE through back pressure, so mixture tapers rich if the fuel model assumes VE unchanged.
- The same manifold pressure at part throttle with a high boost setting carries much less airflow than at full throttle on low boost, because the throttle is doing the restricting; a single-throttle engine can still benefit from throttle position with a MAP overlay.
- Early ceramic turbine wheels in some factory turbos are known to separate at higher boost.
- Coolant pushed to the overflow under boost on a high-boost engine indicates the head lifting and the gasket failing (a common stopping point; burnt discolouration of the gasket coating between stud holes confirms it on teardown).

## Practical use
### Order of work
1. Tune at wastegate spring pressure with boost control disabled and a conservative boost cut. Build the whole map there, steady state then full-throttle ramp runs.
2. Remember a turbo engine's cruise region extends into light boost at low to mid rpm (roughly 2000 to 4500 rpm in one course), and 100 kPa can be a light-throttle load; extend steady-state tuning up into partial boost there.
3. Limit steady-state work in boost. The sources put the ceiling around 120 to 140 kPa for timing work, or about 200 kPa and two-thirds of the rev limit for fuel on high-spring-pressure engines; above that, use ramp runs extended a few hundred rpm at a time, aborting to check lambda and listening for knock. The mid-boost, mid-rpm region is only passed through, so fill it by interpolation between the steady-state area and the full-load row and spot-check a few cells. Take most care in the spool region, where boost and airflow change fastest.
4. When a boosted cell needs a change, back out into vacuum, edit, then return to check, rather than holding boost while editing.
5. Raise boost about 20 kPa at a time (see `methodology/boost-control`).

### Extrapolating ahead of each boost step
Pre-fill cells above the tuned boost before raising it. A course example showed VE rising about 3 % per 20 kPa and timing falling about 2 degrees per 20 kPa through boost; extrapolate the VE trend erring rich and the timing trend erring retarded, then retard much more aggressively above the intended maximum so an overboost lands in safe cells. When starting from cells never optimised in steady state, begin with retarded timing and a little extra fuel in the full-boost rows so the first runs have fuel to remove and timing to add. Rich is the acceptable direction for a guess.

### Reading results
- Boost peaking then tapering at high rpm on a small factory turbo is normal turbine restriction, not a control fault; a flat curve to redline is unrealistic on stock sizing.
- After a timing change, a torque difference in the spool region on an overlaid run is usually spool variation from a hotter exhaust, not the change; credit gains only to the region that was changed.
- More boost giving mid-range gains but nothing at the top: candidates are running out of turbo, an over-rich mixture, and conservative timing. One course demonstration tested these by cautiously adding a little timing in the high-boost rows and leaning slightly, and gained power, though run-to-run open-loop boost variation also contributed.
- Accept close-enough fuelling in the spring-pressure row (within about 1 %) on engines that only pass through it, and move on.

### Heat
Watch coolant, intake and oil temperature after every cell; set alarms. Holding boost steady state is not inherently dangerous if temperatures are watched (one course held low boost at full throttle for about a minute with coolant stable), but long holds heat-soak the intercooler and engine bay far beyond road conditions. Turbine housings and manifolds glowing is normal, but the dyno cannot provide road-speed under-bonnet airflow; return to idle to recover between tests.

### Turbo selection notes
- Too large gives no low-rpm boost; too small chokes at high rpm. Pick by where in the rev range power is needed.
- Size the compressor from its map and airflow need; the turbine is a balance of response and back pressure (wheel is the coarse adjustment, housing A/R the fine one). Twin-scroll housings with a paired manifold give better response, or allow a larger A/R for the same response.
- Simple online selectors give a ballpark; detailed matching calculators need realistic VE, intercooler efficiency and drop, filter restriction and post-turbine back pressure, and their outputs should be re-run with the actual map efficiencies. Platform specialists and many consistent results for the same combination are useful, bearing in mind hidden supporting changes and dyno differences.
- A response gain (in one practitioner's example, boost 500 to 800 rpm earlier) can make a street or hill-climb car faster overall even at some cost in peak power.
- Compression ratio mostly sets how much boost the fuel tolerates without pulling timing far from MBT; it also slightly helps spool through better off-boost torque.

### Other turbo-specific points
- Throttle size: higher upstream pressure pushes more mass through the same bore, so boosted engines tolerate a smaller throttle; one practitioner's view is to spend on the turbo first.
- Nitrous used continuously adds exhaust flow; dedicated builds want a larger turbine, and a big shot on a large turbo can drive the compressor into surge.
- Break-in: run on spring pressure with limited throttle, only a few psi early, stepping up as break-in progresses.
- Twin turbos: compare banks; differing spring tension can make one turbo work harder.
- Rally classes often require an inlet restrictor, which dominates the achievable boost curve.
- Modern water-cooled turbos rarely need a turbo timer unless driven extremely hard right up to shutdown (one practitioner's view).
- Boost by gear shapes power to traction on drag cars: logged examples step boost up through each gear.

## Worked example
At 170 kPa target, cells at 180 to 200 kPa carry several degrees less timing than the 170 row as a backstop: tuned timing of 23, 20 and 19 degrees at 100, 120 and 140 kPa is extended by about 2 degrees per 20 kPa to the target, then about 4 degrees comes out between 170 and 180 kPa, leaving only a few degrees at 200 kPa. Fuel for the same rows follows the VE trend (88, 91.6, 94.3 % at 100, 120, 140 kPa) to about 97 to 98, 101 and 104 %, set on the rich side.

## Disputed / conflicts
- How far to steady-state tune in boost: course lessons differ between about 120 to 140 kPa and about 200 kPa, and between holding boost only briefly and holding low boost at full throttle for a minute. The common ground: low-spring-pressure engines can be steady-state tuned to full throttle at spring pressure because that range is used, while high-spring-pressure engines cannot hold the upper region in real driving and are better developed with ramp runs.
- Boost steps: 20 kPa for learners; 40 kPa with interpolation by experienced tuners, accepting that interpolated values are close but not perfect.
- Turbo timers and blow-off valves: opinions vary by bearing type and use (see `principles/boost/compressor-and-surge`).

## Citations
- practice: Practitioner training and tuning practice, distilled and cross-checked.
- engineering-texts: Engine, combustion, charging and control engineering texts.
