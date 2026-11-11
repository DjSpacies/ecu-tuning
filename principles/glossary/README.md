# Glossary

One canonical vocabulary for the whole skill, so that knowledge from any source (a course, a vendor manual, a
forum, a textbook) and any platform lands on the same concept.

| File | What it holds | Layer |
|---|---|---|
| `principles/glossary/terms.yaml` | Canonical terms: id, name, abbreviations, every other name in use, kind, one-line definition | brand-neutral core |
| `platforms/<ecu>/terms.yaml` | Which of those names that platform's own docs use (generated, with doc counts), plus confirmed on-screen labels under `overrides` | L3 |
| `tools/glossary/asr_fixes.yaml` | Known speech-to-text mis-hearings and their corrections, for transcripts only | tooling |

## terms.yaml fields
- `id`: snake_case, stable; KB entries, workflows and evals refer to concepts by this id.
- `term`: canonical display name. `abbr`: abbreviations. `also`: every other name a source may use
  (generic or vendor-coined), never an ECU brand name.
- `kind`: quantity | unit | table | strategy | component | concept | procedure.
- `layer`: where the concept belongs (L0-L5, see docs/ARCHITECTURE.md).
- `channel` / `role`: the canonical log channel or table role in the normalised models, when there is one.
- `def`: one sentence in our own words. The full explanation belongs in a KB entry, not here.

The file uses a strict YAML subset (flat mappings, flow lists) so tools read it with the standard library
(`tools/glossary/miniyaml.py`).

## How agents use it
- **Ingestion:** map each source's wording to term ids before writing KB entries. Transcripts are corrected
  first with `asr_scan.py` (see tools/glossary/README.md).
- **Platform work:** look up `platforms/<ecu>/terms.yaml`. Use `overrides.label` when present; otherwise
  `top` is the most-used name in that vendor's docs, which is not necessarily the on-screen label.
- **Talking to the user:** use the platform's own label for anything they must find in the software, and the
  canonical term when explaining a principle.

## Adding a term or platform
1. Add or extend the term in `terms.yaml` (check `id` is unused; keep `def` to one sentence).
2. Re-run `python3 -I tools/glossary/platform_terms.py --write` to refresh every platform file. Overrides
   are preserved.
3. For a new ECU, add its collateral folder to `PLATFORMS` in `platform_terms.py`.
