---
name: ecu-tuning
description: Tune gasoline/ethanol/methanol performance engines via ECU tune files, logs, road/dyno sessions, or a live ECU tool. Use for fuel/ignition/boost/VE calibration, log analysis, and guided tuning sessions. Not for diesel.
---

# ECU tuning

## Router
Paths below are relative to this skill's directory. Work for one vehicle lives in a project folder outside it
(`tools/project/new_project.py`, docs/SETUP.md); read that project's profile.json and history.md first.

1. **Scope.** Gasoline, ethanol blends and methanol only. Decline diesel.
2. **Inputs and mode.** Tune, log, live tool? Pick the mode (docs/OPERATING-MODES.md; default offline) and the platform folder in `platforms/`. A platform with no `parser/` has documentation only.
3. **Task.** Load one file from `workflows/`:

| Task | Workflow |
|---|---|
| How should I record a log? / Was this log captured well? | `log-capture` |
| Is this log any good? | `log-health-check` |
| Fuel or lambda errors | `fuel-trim-analysis` |
| Correct the fuel table | `ve-correction` |
| Knock and ignition | `ignition-knock-review` |
| Boost behaviour | `boost-control-review` |
| Are protections set? | `protection-review` |
| What changed between two tunes? | `tools/tune-diff/diff.py` (then ask why, and record it in the project's history.md) |
| Plan road or dyno runs | `road-dyno-session` |
| Live tool | `live-session` |

4. **Tune and log.** A log does not record live edits. Where the log holds table outputs, the runner checks the tune file against them; otherwise ask whether the tune file is what ran.
5. **Profile.** Infer from the files first, then ask one batched question block; "I don't know" is always valid (docs/SETUP-PROFILE.md).
6. **Load only what the workflow lists.** Calculators: `principles/calculators/cli.py`.
7. **Safety.** `safety/limits.yaml` and `safety/aborts.yaml` apply to everything. A limit marked `unknown` needs a value from the user, or the change is withheld. Never recommend disabling a protection, and never apply a change with a safety-critical input unknown.
8. **Report.** State what was measured, inferred, assumed and asked, and which changes were withheld and why. "Not enough data to change this safely" is a correct answer.

Output is advice or a proposed diff for a person to enter. This skill does not write tune files.
