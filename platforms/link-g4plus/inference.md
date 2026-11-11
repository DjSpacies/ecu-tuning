---
id: platforms/link-g4plus/inference
title: What Link G4+ files reveal about the hardware
layer: L3
status: draft
confidence: medium
sources: [vendor-documentation, file-format-analysis]
verified: 2026-11-10
applies_to: {fuels: [gasoline, ethanol, methanol], engines: [all]}
depends_on: []
supersedes: []
---

# What Link G4+ files reveal about the hardware

| Field | Source | Confidence |
|---|---|---|
| Fuel equation mode | Tune scalar 3737; enum order assumed from the help | medium |
| Stoichiometric ratio configured | Tune scalar 2876; tells what fuel the tune was built for, not what is in the tank | high for the setting |
| Engine capacity, injector flow, rated pressure, density | Tune scalars 3002, 2868, 2841, 2867; meaningful only in Modelled modes | medium |
| Aspiration | Peak manifold pressure against baro in a log | medium |
| Injector headroom | Peak duty in a log | high |
| Knock system in use | Knock channels logged and moving; zero does not prove it is working | low |

A Traditional-mode tune hides injector size and capacity inside Master Fuel, so ask for those instead of inferring them.

| Field | Source | Confidence |
|---|---|---|
| Dead time at each voltage point | Array 2987, ten points; check against a published injector dataset | medium |
| Configured rev and MAP limits | Arrays 1623 and 1624; highest active value reported | medium |
| Whether a second fuel or ignition table is configured | Table 2 axes not flat | medium |
| Likely injector generation or size in Traditional mode | Pattern of dead time and Master Fuel only, too weak to rely on | low |

