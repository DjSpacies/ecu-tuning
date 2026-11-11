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
- `parser/`: code to read tune/log into the normalised models and write modified tunes (write support only after verification).
- `mcp-map.yaml`: mapping for a live tool, when one exists.

## Link G4+ (first)
Reference for formats and semantics: ~/Projects/reverse-engineering/pclink-g4plus (READ-ONLY).
Its notes report: tune open/save recovery in analysis/tune-format/, a decoder that parsed 44 bundled
tunes and an ECU definition database (2,945 definitions with IDs), and communications analysis.
We will mine that for table IDs/semantics/units, verify against the user's real tune/log files in inbox/,
and cite which facts are RE-derived (tier B-equivalent after verification) vs vendor documentation (tier B).
No file in that project is modified; no live ECU access is performed by this project.
