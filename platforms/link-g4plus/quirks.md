---
id: platforms/link-g4plus/quirks
title: Link G4+ quirks
layer: L3
status: draft
confidence: medium
sources: [vendor-documentation, file-format-analysis, practice]
verified: 2026-11-10
applies_to: {fuels: [gasoline, ethanol, methanol], engines: [all]}
depends_on: []
supersedes: []
---

# Link G4+ quirks

- `sample-observed`: load axes in the samples are often gauge (MGP), running to -85 kPa, while MAP is absolute. Check which one a table uses before reading a value across.
- `sample-observed`: most samples use Traditional mode (34 of 44 tunes with the field), 9 Modelled and 1 Multi Fuel. Do not treat a fuel table number as VE without checking the mode.
- `sample-observed`: wideband inputs are named by the tuner (`An V2 - WideBand`) and one sample logged a blank unit with AFR-scale values. The adapter flags its conversion.
- `sample-observed`: the first log sample can be all zeros.
- `sample-observed`: one vendor tune contains character references that XML 1.0 rejects, in a label field. The parser replaces them with spaces, and only there.
- `re-derived`: the same name can map to several DataIds across generations (`Fuel Table1 G4`, `FuelTable1`, `Fuel Table2`). `tables.yaml` lists only the ids seen in G4+ tunes.
- `vendor-doc`: closed-loop lambda is a minor trim. A large persistent trim means a base-map problem.
- Firmware differences beyond 5.6.5 and 5.6.6, the versions in the samples, are unknown.
- `practice` (training session 043, a machine transcript, low confidence): on rotary engines a positive trailing split value makes the trailing plug fire before the leading plug, which is dangerous. Confirm in the software before entering a split.
- `vendor-doc`: fuel table load and equation load are separate settings. The table's axis does not tell you how the equation estimates air charge.
- `re-derived`: tables outside fuel, ignition and lambda target live in generic allocation slots (`G4 Table 1` to `12`, about 40 ids). What a slot holds depends on the tune's allocation, so boost tables have no fixed id and are not parsed. Unused second tables have flat filler axes and are skipped.
- `sample-observed`: the 45 tunes carry RPM and MAP limits as 18-point arrays, lower when cold (rpm_limit sometimes 4000 to 4500 for the first few points).
- `vendor-doc`: a firmware update generally leaves the tune alone, but the help says not to update without having the tune checked on a dyno, and to save a copy first.
- `vendor-doc`: in the Quick Tune docs, "Load Centre Tolerance" and "RPM Centre Tolerance" decide when a cell counts as centred.
- `vendor-doc` and `practice` agree on scale: the help aims for about 50 at mid rpm and load, 20 to 30 at idle and 75 to 85 at full power; a course lesson aims for a maximum of 70 to 80. Master Fuel sets only the scale, and the aim is to avoid running out of adjustment.
- `vendor-doc`: the internal wideband can stay off until exhaust is hot, which is the normal mode; the help says to change that only while tuning cold start.

- `vendor-doc`: missing-tooth wheels with a poorly designed gap cause trigger errors, chiefly on high tooth counts such as 60-2, with reluctor sensors, and worse at high rpm.
