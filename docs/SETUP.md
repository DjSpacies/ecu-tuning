# Setup and quickstart

## Requirements
- Python 3.10 or newer, standard library only (every tool runs as `python3 -I ...`; no packages to install).
- For Link G4+ tune files (.pclr): a local copy of PCLink G4+ (the decoding key is read from your own PCLink.exe at run
  time and never stored). Point to it with `export PCLINK_EXE=/path/to/PCLink.exe` or `--exe`.
- Logs (.llg), Haltech CSV exports and TunerStudio .msq tunes need nothing extra.

## Install the skill (Claude Code)
    git clone <repo-url> ~/.claude/skills/ecu-tuning

The skill is then available in every Claude Code session. Other agent harnesses: point the agent at SKILL.md
(AGENTS.md says the same).

## Start a tuning project
One folder per vehicle, outside the skill repository:

    python3 -I ~/.claude/skills/ecu-tuning/tools/project/new_project.py ~/tuning-projects/my-car --platform link-g4plus
    cp my-tune.pclr ~/tuning-projects/my-car/tunes/2026-11-11_current.pclr
    cp my-log.llg   ~/tuning-projects/my-car/logs/
    cd ~/tuning-projects/my-car && claude

Then ask, for example: "Use the ecu-tuning skill. Review this log and tune", or "How should I record a log for fuel
tuning?". The project's CLAUDE.md tells the agent where things are and how to keep history.

## Supported
| Area | Support |
|---|---|
| Link G4+ logs (.llg) and tunes (.pclr) | read |
| Haltech CSV logs | read (check column names against your export) |
| Speeduino / rusEFI / MegaSquirt tunes (.msq) | read |
| Other ECUs (see platforms/) | documentation only |
| Workflows | log capture plan and review, log health, fuel trim, VE correction, ignition and knock, boost, injector duty, protection review, road/dyno run cards, live session |
| Tune diff | any two tunes of a supported platform |
| Writing tunes | not supported by design: proposals are diffs for a person to enter |
| Live ECU connection | through any tool implementing docs/MCP-INTERFACE.md |

## Updating
    cd ~/.claude/skills/ecu-tuning && git pull
