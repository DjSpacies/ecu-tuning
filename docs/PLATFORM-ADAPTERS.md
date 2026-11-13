# Platform adapters

An adapter lives in platforms/<ecu>/ and is the only place ECU-specific knowledge lives.

## Contract
- `README.md`: family, firmware versions covered, tooling (e.g. PCLink), file types.
- `formats.md`: tune and log file formats (what is known, how to parse, uncertainty).
- `channels.yaml`: native log channel -> canonical channel, units, lag/filtering notes.
- `tables.yaml`: native table/parameter -> role tag, axes, units, scaling.
- `semantics.md`: how fuel/ign/boost/trim/closed-loop modes behave on this ECU (what a table
  value actually does).
- `quirks.md`: gotchas, known firmware behaviours.
- `inference.md`: what the tune/log reveals about hardware on this platform (injector scaling, MAP range, ...).
- `parser/`: code to read tune and log files into the normalised models (tools/log-schema). Tune writing is not supported.
- `mcp-map.yaml`: mapping for a live tool, when one exists.
