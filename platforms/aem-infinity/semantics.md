---
id: platforms/aem-infinity/semantics
title: How AEM Infinity fuel behaves
layer: L3
status: draft
confidence: low
sources: [vendor-documentation]
verified: 2026-11-10
applies_to: {fuels: [gasoline, ethanol, methanol], engines: [all]}
depends_on: []
supersedes: []
---

# How AEM Infinity fuel behaves

From InfinityTuner help (`vendor-doc`), for version 2021h.

- The ECU compares LambdaTarget with measured Lambda1 and trims each injector's fuel when feedback is active. It is designed around a VE table.
- Each injector's feedback is assigned to a Lambda1 or Lambda2 sensor in the injector setup.
- A primary injector duty limit is set in the setup wizard.

Further facts from the help (`vendor-doc`):
- Tune at the lowest boost the wastegate spring allows before adjusting boost control. Series 2 setup notes recommend leaving trim tables at zero while configuring boost.
