---
id: principles/airflow/volumetric-efficiency
title: Volumetric efficiency and cylinder filling
layer: L1
status: draft
confidence: high
sources: [engineering-texts, practice]
verified: 2026-11-11
applies_to: {fuels: [gasoline, ethanol, methanol], engines: [all]}
depends_on: [principles/thermo/air-density, principles/boost/exhaust-back-pressure]
supersedes: []
---

# Volumetric efficiency and cylinder filling

## Claim
Volumetric efficiency (VE) is the mass of air the engine traps per cycle relative to the mass that would fill its displacement at a reference density, so its value depends on the reference chosen. Because torque is mostly trapped air, the full-load VE curve has roughly the shape of the torque curve and peaks near peak-torque rpm. Boost raises charge density; it raises VE only to the extent that it overcomes flow losses, and VE flattens or falls once exhaust back pressure climbs.

## Why (derivation)
### Definition and air flow
For a four-stroke, air mass flow m_dot = VE x rho_ref x V_d x N / 2, with N in rev/s, V_d in m3 and rho_ref in kg/m3 (each cylinder has one intake stroke per two revolutions, 720 crank degrees per cycle). rho = p / (R T), R = 287 J/(kg K).
Referenced to ambient density, VE is the whole intake system's performance; referenced to manifold density it describes the cylinder and valves alone. A speed-density fuel model uses the manifold-referenced form, which is why manifold pressure and charge temperature appear in its equation and VE stays a filling efficiency even in boost.
Filling is driven by the pressure difference between the manifold and the cylinder. A naturally aspirated (NA) engine is capped by atmospheric pressure upstream of the throttle; boost raises the manifold side.

### Why VE follows torque
Brake work per cycle is W = eta_f x m_a x Q_LHV / AFR, where eta_f is fuel conversion efficiency, m_a trapped air mass per cycle, Q_LHV the fuel's lower heating value (J/kg) and AFR the air-fuel mass ratio. Torque for a four-stroke is T = W / (4 pi). At near-constant eta_f and mixture, T is proportional to m_a, and m_a is proportional to VE x rho. So at full load the VE curve and the torque curve share a shape, and VE peaks where torque peaks. Adding fuel beyond what the air can burn adds no power; air is the limit.

### What shapes VE
Valve timing and cam profile, pressure waves in the intake and exhaust (ram and scavenging, which can push VE above 100 % because air is compressible and more mass, not more volume, is trapped), flow losses in filter, ducts, throttle and ports, heat pick-up from manifold and ports, and residual gas set by the ratio of exhaust to intake pressure. Port flow on a bench is not VE: air speed matters as much as flow, so an over-enlarged port can raise bench flow and top-end power while losing low and mid-range torque.

## Assumptions
Reference conditions are known and the sensors represent them. A fuel model's VE number may be scaled in a way particular to that model, so the number is a model value, not necessarily the engine's physical VE. Timing is near optimal when VE is read from torque.

## Breaks when
- Boost and high back pressure: residual gas changes trapped air independently of manifold density. A turbo pushed past its efficient range raises exhaust pressure, and VE falls while manifold pressure still rises.
- Mechanical changes (cams, intake, exhaust, capacity) move the whole shape of the table; a speed-density model cannot see them, whereas a mass airflow (MAF) meter measures the new air directly.
- Large cam overlap: at low rpm reversion pushes charge back into the intake, giving narrow VE holes and jagged low-rpm tables; a MAF upstream can count the same air more than once.
- Knock-limited operation: when timing must be pulled, torque per unit air falls, so the torque curve under-reads VE (a pump-fuel engine makes less power per unit airflow than the same engine on a fuel that allows near-optimal timing).
- Switched devices (two-stage cams, runner flaps, variable runners) produce abrupt VE steps, and with variable cam phasing on both shafts VE is no longer a function of rpm and load alone.
- Model artefacts: generic aftermarket VE models are imperfect, and wrong injector or capacity data distorts the VE shape; the same engine on different ECUs gives different VE tables.

## Practical use
Use `principles/calculators/airflow.py`. Check that any VE number uses the same reference and model before comparing it, and never carry a VE table across a mechanical change without re-validating it.

### Sanity ranges, as the sources present them (not limits)
- Typical in the sources: NA peaks around 80-90 %; two-valve engines about 85-95 %; good modern four-valve engines about 95-100 %; well-developed race engines with tuned intake and exhaust 105-110 % or more. OEM engines often fill less than they could because breadth, refinement and economy take priority.
- In ECU fuel models, boosted engines commonly read 110-120 %, and one practitioner saw a stock four-valve NA V6 read 115-120 % at high rpm; treat absolute model VE with caution and judge the model by whether it hits lambda targets.
- One practitioner's ballpark for a turbo engine part-throttle table: idle about 40-50 %, light part throttle about 55-75 %, rising with load and with rpm to peak torque.
- Idle air mass check (one practitioner): a warm four-cylinder idling near 900-1000 rpm draws roughly 4.5-5 g/s. If the model's estimated air per cylinder, converted to g/s, is far from that, the VE values are not describing real filling, and a lambda error at idle should not be blamed on the injectors until the air side is believed.
- A model VE near 200 is not plausible; suspect wrong injector flow or wrong capacity entry (dead-time error mainly affects short pulses and cannot explain it).

### Reading VE against torque
- At full load, compare the VE row with the dyno torque curve. A rich spot where torque is falling is the engine passing its VE peak, not a fault; a lean spot where torque rises sharply means VE rose and the fuel copied from below is short.
- One VE table per cam state: a low-cam table peaks at low rpm and falls away high; a high-cam table can be lower than the low cam in the mid range and peaks high. The crossover tells you where each profile flows.
- How VE behaves with boost (several sources): it rises steeply just above atmospheric, plateaus, then noses over as the compressor leaves its efficient region and back pressure rises. An practitioner demonstration at 5000 rpm showed about 95.4 % at 140 kPa and about 96.5-96.8 % from 160 kPa upward. Expect extrapolated boost rows to flatten.

### Finding intake restrictions
- NA engine: log manifold pressure through a full-throttle ramp. It should start near ambient; the drop toward redline measures the restriction of the whole inlet path but not its location. Sources treat up to about 5 kPa as acceptable and 10-15 kPa as worth fixing. Remember that full throttle is not 100 kPa: baro at the site and restriction both lower it.
- To locate the restriction, measure depression at successive points (before filter, after filter, after the meter, before the throttle) during full-throttle pulls; a liquid manometer resolves the small pressure drops better than a spare MAP sensor. On a boosted engine plenum pressure shows only how hard the turbo works; compare pressure before and after the throttle instead.
- Throttle size: compare cross-sectional area (less the shaft and blade at full throttle), not diameter. Restrictor racing shows how little area a given power needs. A larger throttle on a factory manifold often gains nothing because the manifold inlet becomes the limit, and a step can lose power; a stock throttle usually becomes a restriction only after VE is raised substantially.
- Individual throttle bodies (ITBs): a larger bore lowers port velocity, often trading a small top-end gain for lost low-rpm torque; shorter trumpets favour high rpm, longer favour low rpm (one source's reference point scales length inversely with rpm). Calculation finds the region; the dyno decides.
- Inlet layout matters more than filter element in many back-to-back tests in the sources: convoluted resonator paths, corrugated pipes and tight bends just ahead of the throttle cost power on some engines, while some factory airboxes are not restrictive even at doubled power. Test rather than assume, and remember that any change upstream of a MAF invalidates its calibration.
- A low-mounted filter can ingest water and hydraulically lock the engine.

## Worked example
Full load: 2.0 L at 6000 rpm, manifold 150 kPa, 320 K, VE 0.95: rho = 150000 / (287 x 320) = 1.633 kg/m3; flow = 0.95 x 1.633 x 0.002 x 6000/120 = 0.155 kg/s.
Measured VE: a 6.59 L engine at 6000 rpm displaces 0.00659 x 6000/120 = 0.329 m3/s (about 698 cfm). A measured 0.270 m3/s at standard density (572 cfm) gives VE = 0.270 / 0.329 = 0.82.
Idle check: a 2.4 L four at 1000 rpm, 38 kPa, charge 310 K, model VE 0.55: rho = 38000 / (287 x 310) = 0.427 kg/m3; flow = 0.55 x 0.427 x 0.0024 x 1000/120 = 0.0047 kg/s = 4.7 g/s, inside the typical range above. A model needing VE 0.30 to hit lambda at the same point would point at the fuel side (injector data), not the engine.
Calculation-derived VE: a pulse width computed for AFR 12.5 at 100 % VE measured 11.5 on the dyno; 11.5 / 12.5 = 0.92 suggests the engine is filling about 92 % at that point.

## Disputed / conflicts
- VE and boost: a common belief is that VE keeps rising with boost. Several training sessions say it plateaus and can fall; power still rises because density rises. Discriminating test: log model VE versus manifold pressure at fixed rpm with lambda on target.
- Table smoothness: one practitioner treats a smooth VE table that follows torque as the sign of a good tune and irregularities as fudging for model or injector errors; other training lessons say NA engines with aggressive cams genuinely show jagged low-rpm VE and that tracking lambda target with optimal timing is the real test. Both agree an isolated odd cell deserves a retest.
- High-rpm fall-off: sources usually expect VE to drop after peak torque, yet one course engine's VE stayed flatter than expected and needed fuel added. Shape expectations are a starting guess only.
- Absolute VE: textbooks define VE physically; tuners report that ECU model values exceed physical plausibility and differ between ECUs. Treat model VE as relative within one model.
- ITB power and response claims: one practitioner sees no guaranteed advantage over a good single throttle and plenum (opinion, not back-to-back tested for response).

## Citations
- engineering-texts: Engine, combustion, charging and control engineering texts.
- practice: Practitioner training and tuning practice, distilled and cross-checked.
