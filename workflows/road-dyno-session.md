# Plan and run a road or dyno session

## Inputs
- Required: mode (road or dyno), fuel, knock detection method, rev limit. Safety critical: all of them.
- Useful: which cells need data, gears available, a second person.
- Irrelevant: everything else; do not ask for it.

## Load only
- methodology/road-procedure or methodology/dyno-procedure
- methodology/data-quality, methodology/full-load
- safety/limits.yaml and safety/aborts.yaml

## Steps
1. Build the setup profile and ask once. Road tuning: confirm a legal, clear, safe place; recommend a dyno where the risk is high.
2. Generate cards: `python3 -I tools/runcards/runcards.py --mode road --cells '[[2000,60,"fuel"]]' --max-rpm N`.
3. Read each card before moving. Voice rules (docs/OPERATING-MODES.md): at most 15 words an utterance, one instruction at a time, only safety and abort calls during a pull. `runcards.validate_utterance` checks them.
4. Log, stop, review with the offline workflows, then state any change in one sentence and wait for yes or no. Nothing changes while moving.
5. Any abort condition ends the run. Report the ledger at the end.

## Refuse when
Road conditions are unsafe, the rev limit or knock detection is unknown, or data gates keep failing. Recommend a dyno instead of guessing.
