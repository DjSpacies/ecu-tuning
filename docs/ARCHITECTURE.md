# Architecture

## Layers (each depends only on those above)
```
L0 First principles   physics, thermo, combustion, fluids, control theory, statistics
L1 Engine systems     airflow/VE, fueling, ignition/knock, boost, thermal, torque model, idle, transients
L2 Methodology        brand-neutral tuning procedures, validation, data-quality gates
L3 Platform adapters  per-ECU: file formats, tables, units, quirks
L4 Applications       engine/fuel profiles: NA, turbo, SC, ITB, E85, methanol, DI, etc.
L5 Execution modes    offline | road (solo/two-person, voice) | dyno | live (MCP)
```

## Repo layout
```
SKILL.md              router (entry point for any agent)
AGENTS.md             contributor/agent rules
docs/                 design documents (this folder)
principles/           L0/L1 knowledge; calculators/ = tested Python; glossary/ = canonical terms
methodology/          L2 procedures
platforms/<ecu>/      L3 adapters (link-g4plus first); terms.yaml = platform vocabulary
applications/         L4 profiles
workflows/            task recipes with declared required inputs
tools/                log-schema/ (normalised models), analysis/ (brand-neutral analyses, run.py), sim/ (D2 engine),
                      runcards/, mcp-mock/ (replay server, conformance), kb-lint/, verbatim-check/, test_all.sh
safety/               machine-readable limits, step caps, abort rules
sources/              registry.yaml: every source, tier, status
evals/                cases with known-good answers; scoring
```

## Data flow
```
tune file / log / live MCP
        -> platform adapter  (parse, units, channel names)
        -> normalised model  (Log schema + Table model)
        -> setup profile     (evidence ledger: measured/inferred/user/assumed/unknown)
        -> workflow          (declares required inputs; pulls L0-L2 knowledge)
        -> safety gate       (limits, data-quality gates)
        -> output            (advice | modified tune + diff | run cards | live proposals)
```

## Normalised models
- **Log schema:** time-indexed channels with canonical names, units, sample rate, and
  adapter-supplied metadata (sensor lag, source ECU channel name). Canonical channel set
  defined in tools/log-schema/ (rpm, map_kpa, tps, lambda, ect, iat, ign_adv, inj_pw, ...).
- **Table model:** axes + values + units + interpolation rule + role tag
  (e.g. role: ve, ign_base, lambda_target, boost_target). Roles let methodology
  reference tables without knowing ECU-specific names.

## Progressive disclosure
SKILL.md stays small. Workflows list exactly which principle/methodology/platform files
to load, so small-context models are not flooded.

## Calculators
principles/calculators/ holds small tested Python (CLI-callable) for conversions,
stoichiometry, injector scaling, VE/airflow, boost/pressure ratio, etc. The KB also gives
formulas and worked examples so agents without code execution can still follow them.
