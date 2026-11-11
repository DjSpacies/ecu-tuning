# Review boost control

## Inputs
- Required: log. Safety critical: aspiration, boost ceiling (safety critical).
- Also required for a change: boost target channel.
- Useful: wastegate duty, boost target table.
- Irrelevant: everything else; do not ask for it.

## Load only
- methodology/boost-control
- principles/boost/compressor-and-surge
- principles/control/feedback-and-pid
- safety/limits.yaml and safety/aborts.yaml
- the platform's semantics.md and quirks.md

## Steps
1. Build the setup profile (docs/SETUP-PROFILE.md). Ask once for what inference could not supply.
2. Run `python3 -I tools/analysis/run.py boost-control-review --platform <ecu> --log LOG [--tune TUNE] [--profile P.json]`.
3. Check peak, ceiling, overshoot, oscillation and duty saturation. Do not propose raising boost: state what must be proven first, and refuse if no ceiling is declared.
4. Report the result with the evidence ledger: what was measured, inferred, assumed, asked, and any change withheld and why.

## Refuse when
A safety-critical input is unknown, the log fails its health check, or any limit the change depends on is `unknown`. "Not enough data to change this safely" is a correct answer.
