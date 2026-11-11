# Validation: dry runs before real tuning, and learning from use

The agent will make mistakes and hit uncertainty, especially with tuning-software nuances (table
addressing, units, interpolation, which value is active, firmware differences). It earns each step
toward a real engine by passing the one before it. Nothing here weakens docs/SAFETY.md.

## Dry-run ladder
| Stage | What runs | Can touch an ECU? | Passes when |
|---|---|---|---|
| D0 Offline evals | Saved tunes + logs with known-good answers (evals/) | No | Correct, safe output on eval cases across >= 2 models |
| D1 Replay | MCP mock server replays a real log + tune; agent proposes, `propose_write` dry-runs only | No | Proposals match eval expectations; no safety-gate violations |
| D2 Simulated engine | Small physics model with a hidden "true" VE/ignition response; agent tunes it closed-loop | No | Converges within step caps; never crosses lambda/knock/boost limits; recovers from injected faults (bad wideband, lag, noise) |
| D3 Bench ECU | Real ECU on the bench, engine not running (or a spare unit): read tables, write, read back, revert | Yes, engine off | Every write lands in the intended cell with the intended units; backups and rollback verified |
| D4 Advisory on car | Engine running; agent proposes, human applies by hand | No direct writes | Human agrees with proposals; disagreements logged and resolved |
| D5 Supervised live | `live propose, human approves`, smallest step caps | Yes | Per docs/OPERATING-MODES.md autonomy ladder |

D2 is also the cheapest place to find step-size, data-gate and abort-rule mistakes.

## Learning loop (RL in spirit, not in weights)
We do not train or fine-tune a model; the skill must stay portable across models. Instead each
session produces feedback that a reviewed build step turns into durable improvements:
1. **Session log.** The agent records every uncertainty, wrong assumption, rejected proposal and
   software surprise (what it expected vs what happened).
2. **Triage** (human + build-time model): which layer was wrong? Physics/method -> KB entry fix;
   software nuance -> `platforms/<ecu>/quirks`; missing input -> setup-profile question; unsafe ->
   safety rule or limit.
3. **Regression eval.** Each fixed mistake becomes an eval case (anonymised; no user car data in the
   repo), so it cannot come back.
4. **Re-run** the ladder stage where it was found.

The D2 simulator gives a reward-like score (lambda error, steps to converge, limit violations as hard
fails) for comparing workflow versions. Optimise the workflows and KB against it, never the
simulator itself: a simple simulator is easy to game.
