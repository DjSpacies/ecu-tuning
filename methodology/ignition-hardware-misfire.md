---
id: methodology/ignition-hardware-misfire
title: Ignition misfire and spark plug selection
layer: L2
status: draft
confidence: medium
sources: [practice]
verified: 2026-11-11
applies_to: {fuels: [gasoline, ethanol, methanol], engines: [all]}
depends_on: [principles/ignition/spark-and-dwell, methodology/pre-tune-checklist]
supersedes: []
---

# Ignition misfire and spark plug selection

## Claim
A misfire that appears only as cylinder pressure rises is usually ignition breakdown. The common causes are an over-wide or worn plug gap, a projected plug tip, tired coils, or short dwell. Rule these out before changing the fuel or timing maps. Plug heat range is chosen for the power level, fuel and duty. It does not cure knock, and it does not change how hot the engine runs.

## Why (derivation)
- Breakdown voltage rises with gas density at the gap (principles/ignition/spark-and-dwell). A plug and coil that light reliably at stock boost can fail when cylinder pressure rises, and the failure grows with pressure, so it is worst around peak torque.
- **Heat range** describes how short the heat path is from the insulator nose and ground electrode back into the plug body. Colder plugs have a shorter path and a recessed (non-projected) gap. Hotter plugs project further. A plug too hot for the duty erodes or melts its electrode and can glow, becoming a pre-ignition source, which can be far more destructive than detonation. A plug too cold does not burn off deposits, fouls over time and starts poorly.
- **Projected tips** put the spark in the middle of the charge for consistent light-off at idle and cruise. At high pressure a projected tip is more prone to misfire than a non-projected plug with the same gap.

## Assumptions
Inductive ignition, plugs of known type and condition, mixture and timing already in the right region.

## Breaks when
- **Severe misfire with a wildly wrong tune:** if timing is grossly retarded or lambda is far off target, those can cause misfire too. Get mixture and timing into the right region before blaming hardware.
- **Very small gaps:** extremely small gaps can misfire for other reasons. One practitioner treats about 0.5 mm as a practical lower bound on competition turbo engines.
- **Plug noise:** non-resistor plugs can radiate noise that upsets the ECU. The result is misfires, trigger errors or lost laptop communication, which makes diagnosis confusing. Tolerance varies between ECUs.

## Practical use
### Diagnostic sequence for misfire under load
1. **Characterise the pattern.** If the engine is clean at idle, cruise and low boost, and breaks up as boost or load rises, worst near peak torque, it is a spark-energy or breakdown pattern. On the dyno it shows as a rough sound, a spiky power curve that tracks the good run until a pressure threshold and then falls away, and lean spikes on lambda. Use live, unsmoothed dyno data to see it.
2. **Locate the cylinder.** With per-cylinder EGT, the misfiring cylinder reads cold relative to the others. EGT is slower than lambda but locates the cylinder. On engines with two plugs per combustion chamber, a dead plug can hide behind its partner. Disabling one set and seeing only a small power loss confirms the other set is firing.
3. **Plugs first (cheapest):** pull and inspect. Check the gap, and look for a projected tip, an eroded or missing ground strap, rounded electrodes and cracked ceramic. A plug with its strap worn away can still idle and cruise normally. Fresh plugs at the factory gap may not fix a boosted engine. One practitioner example: a turbo six with roughly a 1.1 to 1.2 mm factory gap needed about 0.8 to 0.9 mm once boost rose.
4. **Dwell test:** raise dwell 0.2 to 0.5 ms. If misfire falls noticeably, it was dwell-related. If a severe misfire is unchanged, suspect plugs, a coil, or the tune.
5. **Coils and igniter:** swap one item at a time to isolate it, for example fresh coils first, then the igniter. Heat-cooked coils and connectors under covers on older engines are a common cause.
6. **If the cylinder still misfires**, a leakdown check beats spending passes swapping parts blindly.
7. **Retarded base map:** if misfire appears early in tuning on a marginal system, a very retarded base map may itself be raising breakdown voltage.

### Gap
- With no application knowledge, the sources start around 0.8 to 1.0 mm on a modified engine and close the gap if misfire appears; when in doubt go tighter.
- High-boost alcohol drag engines in one practitioner's experience run about 0.4 to 0.5 mm.
- Ethanol misfire at high rpm after a fuel change: one example cut the gap from about 1.1 mm to about 0.7 to 0.8 mm. An ignition upgrade is the step after that.
- An acceptable gap depends on tip style, boost and ignition energy. A gap fine at moderate boost may fail at much higher boost.

### Heat range (opinions, one practitioner's scale unless noted)
- Start from the factory plug for correct fitment and baseline range, then go colder with the modification level.
  - Mild NA changes: 0 to 1 step colder.
  - Heavily modified NA, or a turbo with about 50 to 100 % more power: about 2 steps colder.
  - Alcohol or very high boost: 3 to 4 or more steps colder.
  - Other practitioners give similar figures: E85 at least two steps colder, methanol commonly very cold.
- Plug brands number heat range in opposite directions (on one major brand a higher number is colder, on another lower), so check before ordering.
- Very cold plugs can make cold starting hard. Some racers warm up on a hotter set and fit the cold set for competition.
- Water-methanol injection or nitrous does not by itself demand colder plugs. Choose by how hard the engine is pushed. A moderate street nitrous shot is treated like a turbo engine.
- **Reading heat range from a fresh plug:** note how far along the ground strap the heat discolouration reaches. About halfway suggests the heat range is about right, about a third suggests one step too cold, and all the way to the body suggests too hot. A meaningful read needs a fresh set and a cut at the operating point, without idling afterwards (idle overwrites the read). The practitioner does this only on engines making two to three times factory power.

### Other plug choices (opinions)
- Precious-metal plugs mainly buy service life. The practitioners have not seen them cure a misfire or add power.
- Indexing the gap toward the intake valves showed no measurable benefit in drag engine tests.
- Resistor plugs are the default unless there is a specific reason otherwise.
- Use a very light smear of high-temperature anti-seize on the threads.
- Cracked ceramic is dangerous: fragments damage the engine and, on a turbo car, the turbine. Melting points to a tune problem or a badly wrong plug. Fix the cause before more load running.

## Worked example
A heavily upgraded turbo four still runs factory plugs (mid heat range, about 1 mm gap, designed for stock boost). It misfires only near peak torque at the new boost level. The sequence:
1. Plugs show an eroded ground strap and discolouration all the way to the body: too hot.
2. Fitting plugs two steps colder, non-projected, gapped at about 0.8 mm, clears the misfire.
3. A further dwell increase made no difference, which confirms dwell was not the cause.

## Disputed / conflicts
- **Wider gaps for power:** some published studies claim more power from wider gaps. One practitioner reports never measuring a worthwhile gain above about 1 mm on many turbo engines, while breakdown from too wide a gap always cost a lot of power. His explanation is that OEMs use wide gaps because stock pressures allow it and wider gaps help idle and cruise emissions. The discriminating test is a back-to-back gap test at constant load, below the breakdown threshold.
- **Colder plugs against knock:** a common belief is that a colder plug reduces knock. Practitioners say heat range affects pre-ignition (a glowing electrode), not knock. Between adjacent cold ranges the plug had no measurable effect on knock sensitivity. Another practitioner adds that other hot spots (heavy carbon, oil dilution on very rich methanol) can cause pre-ignition, so a colder plug is not a guaranteed cure.
- **Oil separators and colder plugs:** in theory, less oil vapour lets a colder plug run without fouling. One practitioner's experience is that on a healthy engine breather vapour has never prevented a properly matched plug.
- **Higher voltage and coil life:** one practitioner's view is that wear from a wider gap is minor. The bigger risk is internal arcing when the spark cannot jump.

## Citations
- practice: Practitioner training and tuning practice, distilled and cross-checked.
