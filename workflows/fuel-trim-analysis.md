# Fuel and lambda error by cell

## Inputs
- Required: log, tune. Safety critical: fuel (safety critical), wideband validity (safety critical).
- Also required for a change: lambda_target from the tune or log, user step caps for fuel changes.
- Useful: injector data, fuel equation mode.
- Irrelevant: everything else; do not ask for it.

## Load only
- methodology/steady-state-fuel
- methodology/data-quality
- principles/airflow/volumetric-efficiency
- principles/data/sensor-lag-and-delay
- principles/fuels/stoichiometry-and-lambda
- safety/limits.yaml and safety/aborts.yaml
- the platform's semantics.md and quirks.md

## Steps
1. Build the setup profile (docs/SETUP-PROFILE.md). Ask once for what inference could not supply.
2. Run `python3 -I tools/analysis/run.py fuel-trim-analysis --platform <ecu> --log LOG [--tune TUNE] [--profile P.json]`.
3. Run the analysis. Show per-cell error, sample count and spread. Offer a change only for cells that pass the gates, have enough samples and exceed the spread. Each change stays within the user-declared step cap: with no cap, report the error and withhold the change. Check whether the fuel table means VE or something else on this platform.
4. Report the result with the evidence ledger: what was measured, inferred, assumed, asked, and any change withheld and why.

## Refuse when
A safety-critical input is unknown, the log fails its health check, or any limit the change depends on is `unknown`. "Not enough data to change this safely" is a correct answer.
