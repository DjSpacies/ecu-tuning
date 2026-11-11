---
id: platforms/maxxecu/semantics
title: How MaxxECU fuel tables behave
layer: L3
status: draft
confidence: low
sources: [vendor-documentation]
verified: 2026-11-10
applies_to: {fuels: [gasoline, ethanol, methanol], engines: [all]}
depends_on: []
supersedes: []
---

# How MaxxECU fuel tables behave

From MTune help (`vendor-doc`), for the version documented.

- The lambda table sets the target and, with the setting Multiply lambda = YES, is part of the VE fuel calculation. The help says to populate it before tuning VE.
- Only lambda targets are supported, not AFR.
- The closed-loop regulator has conditions: minimum coolant temperature, minimum run time and a transient deactivation. A narrow band target is always lambda 1.
- Some external wideband controllers may not work well cold.

Further facts from MTune help (`vendor-doc`):
- Multiply lambda must be enabled for true VE values. Start boost control in open loop base tuning, not closed loop.
- Open-loop idle must be tuned first, whichever control method is finally used. The lambda regulator is turned off briefly during acceleration.
- The overrun MAP threshold must sit below idle MAP and just above engine-braking MAP.
- The knock retard function can damage an engine with wrong settings; a cam-synced trigger is highly recommended with dual knock sensors.
