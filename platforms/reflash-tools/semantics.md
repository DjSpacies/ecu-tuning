---
id: platforms/reflash-tools/semantics
title: Factory ECU reflash tools
layer: L3
status: draft
confidence: low
sources: [vendor-documentation]
verified: 2026-11-10
applies_to: {fuels: [gasoline, ethanol, methanol], engines: [all]}
depends_on: []
supersedes: []
---

# Factory ECU reflash tools

Rules read from the vendor manuals at rule-sentence level (`vendor-doc`). Table names and strategy are specific to each ECU family and version: nothing here applies across families.

## General to reflash work
- Factory ECUs often target torque or load, not boost. Raise the limits a target passes through, or the target is clipped.
- Stock limits exist for a reason: boost cuts, MAP sensor range, and torque limits on transmissions. Keep a cut slightly under the sensor limit, so the sensor can still see the excess.
- Changing injectors means rescaling the injector data in the supplied way, and sensor rescaling comes before starting, on engines whose cranking fuel depends on it.

## COBB
Work in lambda when fuel chemistry varies. Tapering the load request as timing corrections rise is suggested on some BMW engines. Tuning order for Mitsubishi differs by turbo: MAF first with stock, MAP first with upgraded. Leave headroom in injector duty at low fuel tank levels on trucks with flex fuel.

## EcuTek
Oversized injectors are discouraged where a smaller size meets the power target. Set the boost limit about 25 % above the target load on some Mitsubishi calibrations, so the limit is not hit in normal use. Desired boost targets and the boost control maximum must be consistent, or boost is unstable or capped.

## Hondata
The stock MAP sensor range (about 11 lbs) limits boost and boost cut. The boost cut must be below the sensor's range. Warnings: running leaner than stoichiometric raises exhaust temperature; do not set per-cylinder fuel trim from reading spark plugs; do not rely on the knock sensor to retard timing, and de-sensitising it for noisy cams means knock cannot be trusted.

## HP Tuners
Understand its VE and MAF tables before using its AI fuel control. The vehicle must be safe across the whole range with the current tune first. Its boost documents include an over boost hard limiter as the final safeguard.

## WinOLS
A general calibration editor; it has no strategy of its own. Table meaning comes from the ECU's definition, which the user must supply.
