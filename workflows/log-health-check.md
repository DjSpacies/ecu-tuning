# Check a log before relying on it

## Inputs
- Required: log. Safety critical: none.
- Useful: tune (lets it check axis channels).
- Irrelevant: everything else; do not ask for it.

## Load only
- methodology/data-quality
- principles/data/statistics-for-tuning
- safety/limits.yaml and safety/aborts.yaml
- the platform's semantics.md and quirks.md

## Steps
1. Build the setup profile (docs/SETUP-PROFILE.md). Ask once for what inference could not supply.
2. Run `python3 -I tools/analysis/run.py log-health-check --platform <ecu> --log LOG [--tune TUNE] [--profile P.json]`.
3. Run the health analysis. Report missing channels, sample rate, gaps, implausible sensor values, flat sensors, voltage and how many samples pass the gates. Do not analyse fuel or ignition on a log that fails this.
4. Report the result with the evidence ledger: what was measured, inferred, assumed, asked, and any change withheld and why.

## Refuse when
A safety-critical input is unknown, the log fails its health check, or any limit the change depends on is `unknown`. "Not enough data to change this safely" is a correct answer.
