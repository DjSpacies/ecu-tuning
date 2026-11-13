# Contributing

| To add | Where | Must include |
|---|---|---|
| Knowledge | principles/ (L0-L1), methodology/ (L2), applications/ (L4) | the entry schema (docs/KB-ENTRY-SCHEMA.md) with source tier and confidence; no vendor names in core layers |
| A platform | platforms/<name>/ | README, semantics.md, quirks.md; channels.yaml, tables.yaml and parser/adapter.py (load_log/load_tune returning the models in tools/log-schema) if files are read |
| A workflow | workflows/<name>.md + tools/analysis | inputs, what to load, steps, refusal rules; the analysis in analyses.py |
| A limit | safety/limits.yaml | a source; limits only tighten through the user profile |
| A live tool (MCP) | follow docs/MCP-INTERFACE.md | every operation and the approval path |

Rules: no user vehicle data in the repository; sources are paraphrased, never reproduced; diesel is out of scope; a
safety-critical unknown withholds a change.
