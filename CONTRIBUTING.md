# Contributing

The skill is built to grow by small, testable pieces. Run `sh tools/test_all.sh` before and after any change, and
`sh tools/release_check.sh` before pushing.

| To add | Where | Must include |
|---|---|---|
| Knowledge | principles/ (L0-L1), methodology/ (L2), applications/ (L4) | the 8-section schema (docs/KB-ENTRY-SCHEMA.md), sources from sources/registry.yaml, status draft; `tools/kb-lint/lint.py` clean; no vendor names in core layers |
| A platform | platforms/<name>/ | README, semantics.md, quirks.md, channels.yaml/tables.yaml if parsed, parser/adapter.py with load_log/load_tune returning the models in tools/log-schema, tests with synthetic files |
| A workflow | workflows/<name>.md + tools/analysis | inputs, what to load, steps, refusal rules; the analysis in analyses.py; eval cases in evals/cases |
| A limit | safety/limits.yaml | a source; limits only tighten through the user profile |
| A live tool (MCP) | follow docs/MCP-INTERFACE.md | pass tools/mcp-mock/conformance.py |

Rules (from AGENTS.md): no user vehicle data in the repo; nothing from collateral/ or inbox/ is committed; collateral
is distilled and paraphrased, never reproduced (`tools/verbatim-check/check.py`); diesel is out of scope; a
safety-critical unknown withholds a change.
