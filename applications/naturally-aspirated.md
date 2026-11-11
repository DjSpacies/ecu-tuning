---
id: applications/naturally-aspirated
title: Naturally aspirated profile
layer: L4
status: draft
confidence: medium
sources: [practice]
verified: 2026-11-11
applies_to: {fuels: [gasoline, ethanol, methanol], engines: [na]}
depends_on: [principles/airflow/volumetric-efficiency, methodology/full-load, methodology/base-setup]
supersedes: []
---

# Naturally aspirated profile

## Claim
A naturally aspirated engine has no boost to control, so its limits are thermal and knock limits at about atmospheric pressure, and its airflow comes from VE alone. Its full-load row is rarely exactly the atmospheric row: intake restriction and altitude pull it below, and intake ram effect can push it slightly above.

## Why (derivation)
Load tops out near atmospheric, so a smaller range of cylinder pressure is in play. Best power usually falls in a broad lambda band, and many engines reach MBT before knock.

Because nothing raises manifold pressure, everything that lowers it shows directly in the load the ECU sees at full throttle: intake pressure loss rises with flow, so manifold pressure falls with rpm, and barometric pressure falls with altitude. One demonstration at altitude showed full-throttle manifold pressure of about 96 kPa absolute at low rpm falling to about 92 kPa by 6000 rpm; a restrictive intake can lose 10 to 15 kPa at high rpm. With a well-shaped intake the ram effect can push manifold pressure slightly above atmospheric at speed.

Big cams and cam-lobe switching make VE change sharply over a narrow rpm band. Those engines need extra breakpoints where it happens, or separate tables for each cam mode.

## Assumptions
Pump or better fuel, and a typical compression ratio. Manifold pressure as the load axis, unless the engine uses individual throttles (applications/individual-throttle-bodies).

## Breaks when
- High-compression builds can become knock-limited even at atmospheric pressure, and pump fuel makes that more likely.
- Individual throttle bodies or very large cams give a weak manifold pressure signal; throttle position may be the better load axis.
- A naturally aspirated factory ECU used with an added turbo or supercharger usually cannot read load into boost without code changes (methodology/reflash-tuning).

## Practical use
Expect a 100 kPa row at full load that can dip with intake restriction, so do not copy it blindly to higher speeds. Use the MBT procedure if torque is measured.

- **Load axis.** Remove boost rows. Most sources stop the load axis at 100 kPa; some extend it slightly above atmospheric (one practitioner uses about 2 psi, roughly 14 kPa, of gauge pressure) so ram-effect readings stay inside the table.
- **Find where full load really sits.** Log manifold pressure through every pull and use the ECU's table cursor; at altitude or with a restrictive intake the ECU interpolates between the atmospheric row and the one below, so a full-load correction is applied to every row it straddles.
- **Starting VE.** VE is broadly similar between engines, so a shaped start is portable on a VE-model ECU: one practitioner seeds idle around 40 to 50 %, cruise around 60 to 75 % and full load around 80 to 100 %, then tunes from there. A flat 50 % is the common alternative.
- **Rev limit.** Set it from where the cams stop making power and from the engine's mechanical limits, not from what the hardware could survive. One practitioner's example: a high-compression engine with an upgraded oil pump could rev far higher than its cams make power, and the limit followed the cams.
- **Cam switching.** During base setup one practitioner moves the cam-switch point out of reach (for example to 9000 rpm) so the engine runs on one cam mode while the base map is proven; the high-cam table and switch point are dealt with later.
- **Factory ECUs on naturally aspirated engines** often have no 3D mixture target: closed loop at stoichiometric, a 2D enrichment table against rpm, and a throttle threshold that falls with rpm because less throttle makes high load at high rpm. Most reflash work on these engines is the enrichment table and full-load timing.

## Worked example
At full load a target of 0.88 is inside the 0.85 to 0.92 band usually giving best power. Confirm on a dyno; the plateau is wide.

A pull at 350 m altitude shows the ECU reading between the 0 and -10 kPa gauge rows. Measured lambda is 0.93 against a 0.89 target, about 4 % lean, so 4 % is added to the cells on both rows that were being interpolated, not only to the 0 kPa row.

## Disputed / conflicts
- **Top of the load axis.** Several course examples stop at 100 kPa on a naturally aspirated engine; one practitioner extends slightly above atmospheric for ram effect. The difference matters only where the intake can actually exceed atmospheric; logging manifold pressure at speed decides it.
- **Expected gains from converting a carburettor to injection.** One practitioner's view is that a well set-up carburettor already fuels full throttle adequately, so the gains of injection are part-throttle response, mid-range torque, driveability, economy and emissions rather than peak power. This runs against the common expectation of an immediate full-throttle gain.

## Citations
- practice: Practitioner training and tuning practice, distilled and cross-checked.
