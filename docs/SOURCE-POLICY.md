# Source policy

| Tier | Examples | Role |
|---|---|---|
| A | Textbooks/papers (an engine textbook, SAE, Bosch handbooks), standards, ISO/ASTM fuel specs | Governs L0/L1 |
| B | practitioner training, practitioner training Tuning, ECU maker manuals/datasheets (Link, MoTeC, Haltech), sensor/injector manufacturer data | Governs methodology and platform facts |
| C | Respected individual tuners/shops, reputable books | Corroboration only; flagged |
| D | Forums, Facebook, YouTube comments, hearsay | Never a source. May be logged as a "claim to test" |

## Rules
- A claim is **established** only with A/B support, or two independent B/C sources that agree
  and no contradicting A/B source.
- Conflicts are **recorded, not resolved by fiat**: keep both positions, the contexts where each
  holds, and what experiment would distinguish them.
- Physics (tier A) outranks methodology (tier B) when they conflict; flag for review.
- **Vendor documentation is the authority for its own platform** (user decision 2026-11-08): what a
  parameter, table or mode does, its units, ranges and software behaviour. On those facts it outranks
  courses, videos and other vendors, and a single vendor source is enough for `established` on that
  platform, for the software/firmware version it documents. Tuning advice or theory written in a vendor
  manual is ordinary tier B: it still needs physics or a second source, and physics still arbitrates.
- Version matters: a vendor fact is recorded with the product and version it came from (frontmatter
  `product`/`version`), and is not assumed to carry over to other versions without checking.
- Every KB entry has provenance + confidence + last-verified date (docs/KB-ENTRY-SCHEMA.md).
- A `myths/` collection records common misbeliefs, with the correct explanation, because
  users will state them as fact.
  No verbatim reproduction.
- sources/registry.yaml lists every source with id, tier, licence/usage terms, and status.
