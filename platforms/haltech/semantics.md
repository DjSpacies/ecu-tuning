---
id: platforms/haltech/semantics
title: How Haltech fuel tables behave
layer: L3
status: draft
confidence: low
sources: [vendor-documentation]
verified: 2026-11-10
applies_to: {fuels: [gasoline, ethanol, methanol], engines: [all]}
depends_on: []
supersedes: []
---

# How Haltech fuel tables behave

From the Elite Series help (ESP 2.59.3, `vendor-doc`), for that version.

- The Tuning Method decides what the Fuel Base table means and must be chosen before tuning: Volumetric Efficiency (values reflect engine efficiency, and the Target Lambda table feeds the final calculation), Mass Air Flow (values are a multiplier on the sensor curve, starting at 1.000), or Injection Time (values are time).
- Fuel Type can be Petrol, Ethanol, Ethanol Petrol Blend, Flex Fuel or Methanol.
- Auto V.E. Air Temp Compensation, when enabled, makes the air temperature table a correction to the automatic calculation.
- Datalogging can run to internal memory, conditionally on a channel or switch, or to a laptop through the software.

A proposed percentage change applies directly to the VE method. Under Injection Time it is the same relative change, but under Mass Air Flow it is a multiplier change: state which method is active before proposing anything.

Further facts (`vendor-doc`):
- Boost control: set start duty close to the target and let boost come in just under it; raise derivative slowly, as it is sensitive. Knock frequency should be where the signal differs most between no-knock and knock.
- A vehicle speed sensor is highly recommended with idle control.

Further facts from the Haltech knowledge base (`vendor-doc`):
- Tune rich, then lean out slowly. Keep sustained high load and speed short to limit heat.
- The MAP signal must be averaged over at least one cylinder period because intake pressure varies with the cycle.
- VE tuning needs the correct engine capacity, injector flow and target table.
- Dead time: if VE numbers are strange, correct dead time, and do not assume every rough idle is a dead-time fault. Short pulse adder final cell should be 0 ms.
- Torque management never advances timing past the base ignition table. Long-term fuel trim corrections apply to two tables and one base table, so they are applied in a specific way.
- The timing light should be a simple fixed unit. Mount a MAP sensor above the injector level, so fuel cannot run into it.
