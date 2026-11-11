# Roadmap

## Phase 0: Planning & docs (done 2026-11-07)
Exit: docs reviewed; repo skeleton exists; sources registry seeded.

- [x] training training session transcripts (159 official)
- [x] training training session audio for the 86 without transcripts: Whisper done, 88 whisper-local in collateral (2026-11-09)
- [x] training course transcripts for 3 owned courses (376 official, 11 whisper-local, 2026-11-09)
- [x] practitioner training captions (230 youtube-auto + 26 whisper-local in collateral, 2026-11-09); [ ] optional: Link G5 Teasers (137, not fetched)
- [x] Glossary: principles/glossary/terms.yaml (93 canonical terms), platforms/<ecu>/terms.yaml for 10 standalones (generated from vendor docs), ASR fix rules + scanner (tools/glossary/)
- [x] Fuels papers and injector data fetched on host; [x] textbooks (an engine textbook, an engine-management text, an engine-control textbook, an engine textbook, Turns, ASTM; an automotive handbook optional)
- [x] Vendor documentation: Link, Haltech, MoTeC, ECUMaster, MaxxECU, MS Extra, Speeduino, AEM, FuelTech (Holley/AEM-official need the host browser)
Exit: all wanted collateral on disk; gap report reviewed; extra sources chosen or deferred.

## Phase 1: Foundation (draft complete 2026-11-10; awaits human review)
KB schema in use; L0/L1 core principles (thermo, stoich/lambda per fuel, airflow/VE, injector
math, ignition/knock basics, boost basics, control theory, data-quality statistics); tested calculators.
Exit: calculators pass unit tests; each entry has sources + confidence.

## Phase 2: Collateral ingestion (first pass 2026-11-10, partial: selected lessons and pages only)
Process practitioner training street/dyno material into methodology and workflows; log conflicts.
Exit: ingestion LOG complete for provided material; methodology/ covers VE, fuel, ignition, boost, transients, idle, start.

## Phase 3: G4+ adapter + offline workflows (partial 2026-11-10: built on vendor samples, not the user's files)
Inspect user's tunes/logs (inbox/); document formats; parser to normalised models;
workflows: log health check, fuel/lambda trim analysis, VE correction, ignition/knock review,
boost control review. Evals with known outcomes.
Exit: workflows produce correct, safe recommendations on eval cases across >= 2 different models.

## Validation (runs alongside Phases 3-5; docs/VALIDATION.md) (D0 single model, D1 and D2 pass in simulation; D3-D5 not started)
D0 offline evals -> D1 replay -> D2 simulated engine -> D3 bench ECU -> D4 advisory on car -> D5
supervised live. No stage is skipped; each found mistake becomes an eval case.

## Phase 4: Road & dyno protocols (draft 2026-11-10; voice untested with real speech)
Run-card generator, voice protocol, data-quality gates, dyno grid mapping procedures.

## Phase 5: MCP (mock and conformance done 2026-11-10; no real ECU tool)
Finalise interface, build replay mock server + conformance tests, integrator guide; live-propose mode.

## Phase 6: Expand (started 2026-11-10: documentation-level adapters, application profiles)
More platforms (Haltech, MoTeC, Speeduino, ...), more application profiles.

## Ongoing
Eval growth; source registry upkeep; conflict resolution; calculator coverage.
