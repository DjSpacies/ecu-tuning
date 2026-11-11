# Correct the volumetric efficiency table

## Inputs
- Required: log, tune. Safety critical: same as fuel-trim-analysis.
- Also required for a change: correct injector data.
- Useful: none.
- Irrelevant: everything else; do not ask for it.

## Load only
- methodology/steady-state-fuel
- methodology/compensations
- principles/fueling/injector-flow-and-dead-time
- safety/limits.yaml and safety/aborts.yaml
- the platform's semantics.md and quirks.md

## Steps
1. Build the setup profile (docs/SETUP-PROFILE.md). Ask once for what inference could not supply.
2. Run `python3 -I tools/analysis/run.py fuel-trim-analysis --platform <ecu> --log LOG [--tune TUNE] [--profile P.json]`.
3. Use fuel-trim-analysis. A pattern across many cells at low pulse width points to injector data, and across all cells to a global scaling or fuel pressure error: fix the cause, not the table. Report proposals as a diff for a person to enter; never edit a tune file.
4. Report the result with the evidence ledger: what was measured, inferred, assumed, asked, and any change withheld and why.

## Blind spot
A constant error in the wideband itself cannot be detected from a log with no second reference: the simulator showed the workflow converging to a mixture about 6 % off, with nothing to reveal it. Before relying on the result, confirm the sensor's calibration against the ECU input, and if possible against a second sensor, or a free-air check.

## Refuse when
A safety-critical input is unknown, the log fails its health check, or any limit the change depends on is `unknown`. "Not enough data to change this safely" is a correct answer.
