---
id: methodology/fuel-system-sizing
title: Fuel system sizing
layer: L2
status: draft
confidence: medium
sources: [practice]
verified: 2026-11-11
applies_to: {fuels: [gasoline, ethanol, methanol], engines: [all]}
depends_on: [principles/fueling/injector-flow-and-dead-time, principles/fuels/energy-and-charge-cooling]
supersedes: []
---

# Fuel system sizing

## Claim
The pump, wiring, lines, regulator and injectors must be sized together with margin, and checked as installed. What the injector sees is differential pressure; what the pump sees is rail pressure (base plus boost with a referenced regulator) at the voltage that actually reaches it. An alcohol fuel changes the whole calculation. A fuel supply shortfall cannot be tuned around: it shows as a lean trend that fuel-table changes do not fix.

## Why (derivation)
- Injector limit: duty at peak fuel demand. Demand per cycle is set by power and fuel; duty also rises with rpm because cycle time shrinks (`principles/fueling/injector-flow-and-dead-time`).
- Supply limit: pump flow against pressure and voltage. Pump flow falls as pressure rises and current rises with it; flow also falls steeply with supply voltage. With a referenced regulator the pump works against base plus boost exactly when demand peaks. If the injectors at full duty can consume everything the pump delivers, rail pressure collapses.
- With a fixed-pressure rail, boost subtracts directly from differential pressure, eroding injector flow as boost rises: 400 kPa rail at 100 kPa boost leaves 300 kPa across the injector.
- The regulator must be able to bypass the pump's full flow when injectors are nearly shut (idle, overrun); otherwise pressure rises above the set point.
- Raising fuel pressure gains injector flow only as the square root of pressure, and costs pump flow, current and dead time.

### Fuel quantity by fuel
For the same power, the sources plan on about 35 to 40 % more fuel volume for E85 than pump gasoline, and about 2.3 times the mass at stoichiometry for methanol, or 2.5 to 3 times the gasoline flow once methanol's richer targets are included. Staged injection is commonly needed on high-power alcohol builds (see `methodology/staged-injectors`).

## Assumptions
Fuel flow demand is estimated from a target power, a brake specific fuel consumption (BSFC) guess and the fuel type, so the result is a ballpark to round up, not a design figure. Engine-specific BSFC is rarely known without an engine dyno.

## Breaks when
- Voltage drop to the pump (factory wiring with an upgraded pump, poor earths, a failing alternator feeding a voltage booster) reduces flow far below the rating.
- Pump data read at the wrong pressure: advertised power ratings usually assume naturally aspirated rail pressure (about 300 kPa), so a pump rated for a given power may support only about 60 % of it at 480 to 550 kPa rail pressure.
- Very high rpm engines (bikes, rotaries): a BSFC formula ignores rpm and undersizes injectors.
- Fuel surge: a tank without a surge pot or tank uncovers the pickup below about half full under hard acceleration, braking or cornering; pressure collapses and the engine stumbles lean. A full-tank test will not show it.
- Partly blocked filters; pulsation from rails with dampers removed; pressure steps when a second pump is switched in by a pressure switch.

## Practical use

### Size before the session
A shortfall usually shows only once high-power runs begin, after an hour or two of work that then has to be redone. Check injector and pump sizing for the power target, and measure pump terminal voltage while running, before the dyno session.

### Injectors
- Per-injector flow (lb/h) = flywheel power (hp) x BSFC (lb/hp/h) / (injectors x maximum duty), then convert (about 10.2 cc/min per lb/h on gasoline) and round up. The sources' typical BSFC values for gasoline: about 0.45 to 0.55 naturally aspirated, about 0.55 to 0.65 forced induction, 0.70 or worse for air-cooled or very rich engines. Pick the high side.
- Quick rule from one practitioner: about 1 L/min of total injector flow per 200 hp on gasoline at 100 % duty, x 1.35 to 1.4 for E85 and about x 2.5 for methanol. It ignores pressure, rpm, lambda target (0.82 vs 0.75 is a large difference) and BSFC.
- For engines revving past about 7000 to 8000 rpm, use an rpm-aware fuel flow calculator. In one example, a 725 cc injector at 85 % duty with a 7000 rpm limit needed about 1000 cc to stay near 89 % at 10000 rpm. One such calculator's tuner data average about 0.35 L of gasoline per wheel horsepower per hour.
- BSFC moves with octane: a higher-octane fuel that removes the knock limit allows more timing and more power from similar fuel.
- Size against idle as well: very large injectors put idle pulses into the non-linear region unless they are linear at short pulses. A modest oversize (about 300 cc/min) for future growth rarely hurts idle with modern injectors; one naturally aspirated 1.8 L engine ran 1000 cc injectors at about 37 % peak duty and drove normally. Extremely large injectors waste resolution.
- Lower peak duty also leaves room to move injection timing; injectors near 80 to 90 % duty have almost none.
- When in doubt about spray: some practitioners have seen full-load problems (black smoke with apparently correct lambda) cured by an injector with narrower spray. A wideband reads only what burned; poorly atomised or wall-wetted fuel passes through unburnt and is not seen as rich. Do not lean the tune to cure that.

### Pump, wiring, lines, regulator
- Size the pump for about 20 to 30 % more flow than total injector demand at full duty (sources quote 20-30, 25, and 25-30 %). Check that against the pump's flow curve at base pressure plus peak boost and at the voltage it will really see.
- Wire the pump so full charging voltage reaches it (heavier feed and earth, relay). Measure voltage at the pump connector during a full-load run; on factory wiring an upgraded pump often sees 10.5 to 12 V instead of about 14 V.
- Line sizes from one practitioner: about -6 AN feed up to roughly 400 hp, -8 AN from about 400 to 800 hp, return one size smaller; low-permeation lined hose in street cars with boot-mounted systems. For a mild upgrade the factory hard lines may be the limit, so new soft lines alone gain nothing.
- Use a regulator sized for the pump; a large pump on a small or factory regulator raises base pressure, can push toward the pump's internal relief and drops flow. Most factory regulators cope with a moderate pump upgrade.
- Surge systems: lift pump(s) feed a tall, narrow surge tank; the main pump draws from its bottom. Lift pumps work against almost no pressure and so flow much more, often allowing a factory pump as a lift pump. One practitioner returns to the surge tank with an overflow to the main tank, accepting that recirculated fuel warms, especially at idle.
- Boosted conversions of fixed-pressure cars commonly retrofit a manifold-referenced regulator and return line, or rely on the ECU to model differential pressure.
- Mechanical (engine-driven) pumps give flow proportional to rpm and almost no pressure at cranking speed; they need a primer pump or starting fluid, and a regulator with a large bypass, or pressure spikes on a high-rpm lift. Modern brushless electric pumps with speed control hold flow nearly constant with pressure, at high current (one tested unit about 38 A at about 520 kPa and 70 A at about 1030 kPa), which is why total-loss drag cars often stay mechanical.
- Pump speed control (factory PWM or staged speeds) reduces recirculation heating and noise. Staging points in the sources sit around 3000 to 5000 rpm or 10 to 30 % fuel flow.
- E85 and alcohol: confirm every component is compatible (pumps, seals, lines, injector internals), and consider corrosion inhibitors in humid climates since ethanol absorbs water.
- Fuel temperature changes density; logging it is cheap, and some ECUs can trim for it.

### Base pressure
- No fixed rule; common factory practice is about 300 kPa differential on manifold-referenced return systems and about 400 kPa on fixed-pressure systems. Know the injector's rating pressure. A modestly higher base (for example 350 kPa) can buy headroom for ethanol, if the pump has margin.
- Set a referenced regulator with the engine running at charging voltage and the reference hose disconnected and plugged; lock the adjuster, recheck, then reconnect. Engine-off priming sees only about 11.5 to 12.5 V at the pump, so it is only a rough setting; with the hose connected at idle, manifold vacuum lowers the reading (one demonstration: about 65 kPa), so setting it that way leaves the real base too high and the wrong rows of injector data in use.
- At idle with the hose connected, expect rail gauge pressure to read base minus manifold vacuum (for example 300 kPa base at 60 kPa absolute manifold pressure reads about 260 kPa).
- Measure base pressure even on non-adjustable factory systems: an ageing pump or fault shows before dyno time is wasted, and the ECU needs the real value. Make sure the value entered in the ECU matches the regulator.
- Some ECUs need the fuel system type set (referenced, fixed, measured) for the model to use differential pressure; on fixed-pressure rails the ECU computes it from the entered pressure and measured manifold pressure.
- Naturally aspirated engines with throttle bodies per cylinder or aggressive cams have a poor, pulsing manifold signal; running fixed (unreferenced) pressure and telling the ECU so gives more stable idle mixture.
- Very high base pressure (drag racing often about 550 kPa base) does not overload injector drivers (current is set by coil resistance and voltage), but lengthens dead time, can stop older injector designs opening, and loads the pump. Claimed atomisation gains are unproven in one practitioner's experience.

### Diagnostic tests
- **Fuel table climbs while torque falls.** At full load a correct fuel or VE table broadly follows the torque curve. Numbers that keep rising toward redline while dyno torque falls, with lambda still drifting lean and additions having no effect, mean the table is compensating for a delivery shortfall. Stop adding fuel. This holds where differential pressure is constant or compensated; a time-based table on a boosted fixed-pressure rail is distorted anyway. Novices often expect fuel numbers to rise with rpm.
- **Pump or injectors?** Check duty. At or near 100 % (often without any ECU warning), the injectors are maxed, or pressure has fallen; at moderate duty (60 to 70 %) with a lean trend, the pump side is short and rail pressure is likely dropping. Confirm with a pressure log. On modified factory turbo cars lean high-rpm drift with duty headroom is most often the pump.
- **Pressure tracks boost?** With a referenced regulator, rail pressure should rise one for one with boost (300 kPa base + 140 kPa boost = 440 kPa). Rising then sagging as rpm and demand rise means pump capacity or supply voltage limits. Also check the earth, not just the feed, and the filter.
- **Steady sag vs single dip.** A steady fall of differential pressure across a pull is a real supply variable to address; a single brief dip may be pulsation seen by the sensor. A good surge-tank system held about 400 kPa within 5 to 6 kPa through a run; a fall of about 10 kPa across a run was treated as typical; a fall from 320 to 290 kPa signals a pump nearing its limit.
- **Lean excursion with pressure collapse.** Overlay fuel pressure, lambda, boost and exhaust temperature. A lean excursion coinciding with a pressure collapse (one circuit log: about 380 kPa down to 60 to 175 kPa on a long straight) is surge or supply, not a map error. A drag log drifted from lambda 0.82 to 0.84 as fuel pressure fell away from boost and exhaust temperatures climbed: the pumps were at their limit.
- **High idle pressure.** Pressure above the set point at idle that falls back under load (one case: about 378 vs 300 kPa) suggests a large pump overrunning the regulator's bypass at low demand; log under load before condemning the regulator. A regulator that cannot be set low enough, or holds pressure high in vacuum, is restricting return flow and distorts the light-load fuel table.
- **Measured return flow.** On a return system, run the return into a graduated container for 30 to 60 s with the engine running (pump at charging voltage, any speed controller forced to full), with peak boost applied to the regulator reference by hand pump. Compare with about 1 L/min per 200 hp on gasoline: 2 L in a minute supports about 400 flywheel hp. Not possible on fixed-pressure systems without an external regulator.
- **Pump current trend.** Where a power distribution module logs current, a pump drawing gradually more over sessions is working harder (clogging filter, wearing pump); a lift pump drawing much less than normal is sucking air. One module only flags undercurrent and keeps driving the output.
- **Factory pulsation.** Some factory systems resonate with injector firing at particular rpm, and the factory calibration hides it with load-based fuel compensation; a replacement system that removes the pulsation lets that compensation be zeroed.
- **Bank or cylinder differences after rail changes.** Removing factory pulsation dampers has been associated with bank-to-bank fuel differences; refit dampers on upgraded rails where possible.

### Protection and pump control
Fuel pressure protection is set from logged variation (see `methodology/engine-protection` for structure). The sources suggest checking differential pressure (not rail pressure) on referenced systems, gating on load or positive boost, a delay of about 250 ms because differential pressure is noisy on lifts and manifold-pressure steps, and a threshold roughly 50 kPa below normal after logging the real spread. One practitioner regards a sudden surge collapse as mostly a misfire risk and a slow sag at high load as the dangerous case. Pump logic: prime about 2 to 3 s at key-on, run only once cranking is detected, and stop a few seconds after rpm falls to zero, so a stalled car with a ruptured line does not keep pumping. Electronic fusing should allow inrush (about twice running current) with a short window and a running limit set modestly above measured draw; a long retry interval on a pump will drop fuel pressure.

## Decision rules
- Rules of thumb from the sources, all practice guides: about 1 litre per minute per 200 hp on gasoline; a pump with about 20 to 30 % more flow than the injectors need; peak injector duty kept around 85 to 90 %.
- Do not exceed the injector's rated or characterised pressure.
- Raising pressure is for a small gain only (about 5 to 15 % in the sources); otherwise fit larger injectors. When raising it, confirm the pump can hold it and recalculate injector data.
- When injectors run out of headroom at high rpm, limit boost there (taper) rather than run past the duty ceiling; add boost only where duty headroom exists.
- After larger injectors, expect the pump to be the next limit: stock pumps and stock injectors often run out at about the same point.
- Measure fuel pressure, even with a fixed system, and keep a gauge or logged sensor on during tuning. Fewer than a third of customer cars reaching one practitioner had a pressure sensor.
- Use a fuel pressure sensor in the fuel model where the ECU supports it, so pulse width corrects for pressure droop and later base-pressure changes. Compensation cannot help once duty is already near maximum.

## Data gates
Fuel pressure (ideally differential) logged under load, with battery or pump voltage and injector duty.

## Worked example
- A 400 hp gasoline target implies about 2 L/min by the rule of thumb (500 cc/min per injector on four injectors at 100 % duty). E85 needs roughly 35 to 40 % more, about 2.7 to 2.8 L/min.
- 800 flywheel hp turbo four-cylinder, BSFC 0.6, 85 % duty: 800 x 0.6 / (4 x 0.85) = 141 lb/h, about 1440 cc/min per injector before rounding up.
- Four 1000 cc injectors = 4 L/min at full duty; with 25 % margin the pump should deliver about 5 L/min (300 L/h) at base plus boost pressure and real pump voltage.
- One pump example: about 320 L/h at about 310 kPa, 285 to 290 L/h at about 410 kPa, 240 to 245 L/h at about 550 kPa, with current rising from about 12.5 to 15 A. Reading it at base pressure alone overstates boosted supply by about a quarter.

## Disputed / conflicts
- Cross-check: no textbook value for the 20 to 30 % pump margin or 1 litre per minute per 200 hp. They are practice guides from practitioners and agree with each other.
- **Supercharged vs turbo.** A claim that supercharged engines need more injector for the same power was not supported by one practitioner's experience; fuel per power follows the engine's BSFC, not compressor type.
- **Rising-rate regulators.** Several sessions call boost-referenced one-for-one regulators normal, not rising rate, and describe true rising-rate units as an obsolete workaround; an ECU that assumes one-for-one bakes in errors with them.
- **Gasoline density in unit conversion.** One source divides lb/h by 7.25 lb per gallon to get gallons per hour; gasoline is nearer 6.2 lb per US gallon (about 0.74 kg/L). Use the actual fuel's density.
- **Two pumps on a pressure switch** give a pressure step at switch-in (one practitioner's view); speed-controlled pumps vary output more smoothly.

## Citations
- practice: Practitioner training and tuning practice, distilled and cross-checked.
