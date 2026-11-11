# KB entry schema

Every entry in principles/, methodology/, platforms/, applications/ is a markdown file
with YAML frontmatter:

```yaml
---
id: principles/combustion/knock-basics
title: Knock fundamentals
layer: L1                 # L0|L1|L2|L3|L4
status: draft             # draft|reviewed|established|disputed|deprecated
confidence: medium        # low|medium|high
sources: [engineering-texts, practice]    # ids from sources/registry.yaml
verified: 2026-11-06
applies_to: {fuels: [gasoline, e85, methanol], engines: [all]}
depends_on: [principles/thermo/ideal-gas]
supersedes: []
---
```

## Body sections (in order)
1. **Claim**: short, testable statement.
2. **Why (derivation)**: equations with units and symbols defined; reasoning from L0.
3. **Assumptions**: when the claim holds.
4. **Breaks when**: known exceptions/failure modes.
5. **Practical use**: how an agent applies it; what to measure.
6. **Worked example**: with numbers and units.
7. **Disputed / conflicts**: positions, sources, discriminating test.
8. **Citations**: source ids + locator (chapter/timestamp/section), paraphrased only.

Rules: SI internally (kPa, K, kg/s, ms) with explicit unit conversions; one idea per file;
no setup-specific data; calculators referenced by path when they exist.
