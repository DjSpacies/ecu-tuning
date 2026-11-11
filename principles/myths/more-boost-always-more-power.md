---
id: principles/myths/more-boost-always-more-power
title: Myth: a higher boost number always means more power
layer: L1
status: draft
confidence: medium
sources: [practice, engineering-texts]
verified: 2026-11-11
applies_to: {fuels: [gasoline, ethanol, methanol], engines: [turbo, supercharged]}
depends_on: [principles/boost/compressor-and-surge, principles/boost/exhaust-back-pressure]
supersedes: []
---

# Myth: a higher boost number always means more power

## Claim
A boost figure says nothing without pressure ratio, temperature and turbine conditions. Boost mainly reflects how hard the engine resists the flow pushed into it. Past a turbo's efficient range, more boost can bring little extra air, more heat, higher exhaust back pressure and less knock margin, so power plateaus or falls.

## Why (derivation)
Air mass depends on density, which falls with temperature. Compressor efficiency falls away from its islands and outside them extra pressure ratio mostly adds heat; past choke the compressor delivers little extra mass flow while outlet temperature soars. A small turbine raises exhaust back pressure steeply as boost rises, cutting VE and adding residuals. On a knock-limited fuel each extra unit of boost forces timing away from MBT. The same boost therefore makes very different power with a large versus a small turbo, and on a stock versus a free-flowing engine (higher VE moves more air at the same pressure). A small engine needs far higher boost than a large one to pass the same airflow.

## Assumptions
Turbocharged or supercharged engine.

## Breaks when
Within the compressor's efficient range, with turbine back pressure modest and timing not knock-limited, power does generally follow boost. Holding a flatter curve on a small factory turbo that tapers often gains power, up to the point where it is driven far beyond its efficiency.

## Practical use
Compare airflow, charge temperature and power, not gauge numbers. Signs that more boost has stopped paying, from the sources:
- Gain per psi shrinks, then plateaus while timing must come out for knock: stop around the onset of diminishing returns on a road car (one practitioner's practice).
- Exhaust manifold pressure climbing past intake pressure while power stalls.
- Outlet or manifold temperature rising sharply for little extra flow.
- Power lost when boost rose: in one anecdote a heavily built drag engine lost about 15 to 20 hp going from 45 to 55 psi, the compressor being past choke.
On pump fuel, one practitioner prefers a little more boost with timing kept further from the knock threshold over less boost with timing right on it, because off-dyno conditions are often worse.

Related misbeliefs, recorded because users state them as fact:
- A fixed charge temperature rise per psi of boost: no, it depends on compressor efficiency and where on the map the point lies.
- Lean or retarded spool for faster boost: one practitioner's dyno testing found no meaningful gain over load-appropriate targets (around 0.95 lambda coming onto boost, richening to the full-boost target); MBT timing in the spool cells gave better spool and performance than retard despite lower exhaust temperature. Retard belongs to anti-lag and launch control. Only an overly rich spool zone clearly hurts.
- Holding the same manifold boost up a mountain keeps power constant: the wastegate must close further, pre-turbine pressure rises and the turbo may overspeed, so power still falls.
- Billet compressor wheels flow more: a billet wheel with the same aerodynamic profile does not; its real advantages are strength at extreme speed and boost and a slightly thinner hub.
- A big wastegate offsets a tight turbine housing: the turbine still needs its energy for the target, so back pressure stays high.

## Worked example
Two turbos at the same 200 kPa may have very different power, since one is working well outside its efficient range. A worked comparison with 300 K inlet air: compressor A runs PR 2.0 at 75 % efficiency, outlet about 388 K. Compressor B, smaller and fed through a restrictive intake, needs PR 2.3 for the same manifold pressure and sits at about 60 % efficiency, outlet about 434 K. After an intercooler of effectiveness 0.7 with 300 K cooling air, the charges are about 326 K and 340 K: at identical boost, B's charge is about 4 % less dense, with less knock margin, before counting any extra turbine back pressure.

## Disputed / conflicts
- Where to stop raising boost is judgement: road-car practitioners stop at diminishing returns; record-chasing drag cars accept more heat and stress for the last gains.
- Lean spool and retarded spool are popular in parts of the tuning community; the counter-evidence is one practitioner's testing (opinion strength). Discriminating test: back-to-back ramp runs with only the spool-region target or timing changed, comparing boost onset rpm and mid-range torque with the exhaust preconditioned equally.

## Citations
- practice: Practitioner training and tuning practice, distilled and cross-checked.
- engineering-texts: Engine, combustion, charging and control engineering texts.
