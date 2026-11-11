# Review ignition and knock

## Inputs
- Required: log, tune. Safety critical: knock detection method (safety critical).
- Also required for a change: ignition table.
- Useful: torque data.
- Irrelevant: everything else; do not ask for it.

## Load only
- methodology/knock-assessment
- methodology/steady-state-ignition
- principles/combustion/knock
- principles/combustion/mbt-timing
- safety/limits.yaml and safety/aborts.yaml
- the platform's semantics.md and quirks.md

## Steps
1. Build the setup profile (docs/SETUP-PROFILE.md). Ask once for what inference could not supply.
2. Run `python3 -I tools/analysis/run.py ignition-knock-review --platform <ecu> --log LOG [--tune TUNE] [--profile P.json]`.
3. Find knock events and map roughness. Propose only reductions. Advance is never proposed from a log: it needs measured torque and knock monitoring (see methodology/steady-state-ignition).
4. Report the result with the evidence ledger: what was measured, inferred, assumed, asked, and any change withheld and why.

## Refuse when
A safety-critical input is unknown, the log fails its health check, or any limit the change depends on is `unknown`. "Not enough data to change this safely" is a correct answer.
