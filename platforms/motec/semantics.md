---
id: platforms/motec/semantics
title: How MoTeC M1 fuel and ignition behave
layer: L3
status: draft
confidence: low
sources: [vendor-documentation]
verified: 2026-11-10
applies_to: {fuels: [gasoline, ethanol, methanol], engines: [all]}
depends_on: []
supersedes: []
---

# How MoTeC M1 fuel and ignition behave

From the M1 GPRP Pro Setup and Tuning Guide and M1 Tune 1.5 help (`vendor-doc`), for those versions. Package behaviour differs between M1 packages.

- Fuel is built on an engine-efficiency model: Engine Load, the mass of air per induction, comes from the Engine Efficiency table. Fuel Mixture Aim sets the target mixture.
- The torque model assumes optimum timing has been tuned in Ignition Timing Main.
- Quick Lambda applies a correction to a site using the current lambda and the aim value for that site.
- GPRP has adaption and sample tables for Engine Efficiency.
- For multi-throttle engines, a vendor technical note describes a method that avoids tuning the Engine Efficiency table directly, because of the variables involved.

Further facts (`vendor-doc`):
- Confirm a fuel composition sensor independently if a custom calibration is used. Batch-fire offset timing should not be used on direct injection.
