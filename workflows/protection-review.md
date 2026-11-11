# Review configured protections

## Inputs
- Required: tune. Safety critical: rev limit and boost ceiling the engine can take.
- Useful: engine builder's figures.
- Irrelevant: everything else; do not ask for it.

## Load only
- methodology/engine-protection
- safety/limits.yaml
- the platform's semantics.md and quirks.md

## Steps
1. Ask once for the engine's rev limit and boost ceiling.
2. Run `python3 -I tools/analysis/run.py protection-review --platform <ecu> --log LOG --tune TUNE --profile P.json`.
3. Report any limit that is missing, or above the declared ceiling. Never advise raising a protection to clear a problem.

## Refuse when
The platform's data does not expose protections.
