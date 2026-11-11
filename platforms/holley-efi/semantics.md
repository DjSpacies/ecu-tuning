---
id: platforms/holley-efi/semantics
title: Holley EFI fuel tables
layer: L3
status: draft
confidence: low
sources: [vendor-documentation]
verified: 2026-11-10
applies_to: {fuels: [gasoline, ethanol, methanol], engines: [all]}
depends_on: []
supersedes: []
---

# Holley EFI fuel tables

From the V6 software help (`vendor-doc`), read at topic level.

- Tuning uses Base Fuel and Target Air Fuel Ratio tables with a Learn Table.
- The Learn Table is view-only. If it reaches the Learn Compensation limits during learning, those limits need increasing, which also means the base fuel is that far out.

Further facts from the V6 help (`vendor-doc`):
- Learned corrections are transferred to the Base Fuel table only after all areas are learned, then the table is smoothed by hand; do not over-smooth.
- The Base Fuel table must be smooth and rise with rpm or load. Learning requires closed loop to be active.
- Tune the lowest boost allowed by the spring first; TPS-based boost modulation is recommended in nearly all applications.
