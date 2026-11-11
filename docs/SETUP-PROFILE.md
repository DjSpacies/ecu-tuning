# Setup profile and the discover-then-ask protocol

The agent never assumes a vehicle. It builds a **session-scoped setup profile** per use case.
The repo stores the schema, never a user's values (users may export `*.profile.yaml`, gitignored).

## Evidence ledger
Every profile field carries `value`, `origin`, `confidence`, `evidence`:
- `measured`  : directly in a log (e.g. peak boost 1.4 bar)
- `inferred`  : derived from data with a stated method (e.g. injector size class from pulse width vs. fuel load)
- `user`      : stated by the user
- `assumed`   : default used because unknown; MUST be flagged in output
- `unknown`   : not known and not yet needed

## Fields (initial set)
engine: cylinders, displacement, compression ratio, configuration, aspiration, cam (duration/lift/LSA/VVT), ITB/plenum, exhaust/header
forced induction: type, turbo/SC model, wastegate (internal/external, spring), BOV/BPV, intercooler, boost control solenoid
fuel: type/blend, flex sensor present, injector model/flow/pressure/dead-time, fuel pump/rail/regulator, DI/port/dual
ignition: coil type, plug heat range/gap, knock detection method (sensor type/location)
sensors: MAP range, wideband type, IAT/ECT, baro, other
drivetrain/use: transmission, intended use (street/track/drag/rally), dyno or road, octane/fuel quality available
limits: user-declared max boost, max RPM, max EGT, risk appetite

## Protocol
1. **Ingest** tune/log/MCP. Run inference playbook (platform/<ecu>/ + methodology/inference-*.md)
   to fill what can be inferred, each with confidence.
2. **Select workflow.** The workflow file declares inputs as `required`, `useful`, `irrelevant`,
   each with: why it matters, how to infer it, a safe default (if any), and whether it is
   `safety_critical`.
3. **Ask once, batched.** Present a single question block containing only the unknowns that
   the task needs and that inference could not resolve. For each: why asked, inferred guess
   (if any) to confirm/correct, and an explicit "I don't know" option.
4. **Handle "I don't know".** If a default exists and the field is not safety-critical, proceed
   with `assumed` and flag it. If safety-critical (e.g. boost ceiling, fuel type, knock detection),
   restrict to the most conservative actions or advise how the user can find out.
5. **Ask later when needed.** New questions are allowed mid-task when new evidence makes a field
   necessary (e.g. log reveals boost control issues). Keep them minimal and explain why now.
6. **Contradictions.** If user statements conflict with data (user says E85, lambda targets/logs
   say pump gas), surface it and resolve before proceeding.
7. **Report** the ledger summary with the output (what was measured/inferred/assumed/asked).

## Voice-mode variant
In voice sessions (docs/OPERATING-MODES.md) questions are asked before driving, as a short
spoken list, one at a time if the user prefers, with answers recorded to the ledger.
