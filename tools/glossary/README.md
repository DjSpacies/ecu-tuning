# tools/glossary

Stdlib-only tools behind principles/glossary/. All read collateral; none write into collateral.

| Tool | Does |
|---|---|
| `mine_terms.py acronyms DIR...` | ALL-CAPS tokens ranked by document count, per vendor (find new terms) |
| `mine_terms.py oov TRANSCRIPTS --vocab DIR...` | transcript words missing from docs + dictionary (find mis-hearings) |
| `mine_terms.py grep TERM DIR...` | documents containing a phrase, per vendor (`--case` for exact labels) |
| `mine_terms.py kwic REGEX DIR...` | keyword in context, to check a candidate before adding a rule |
| `platform_terms.py [--write]` | regenerate platforms/<ecu>/terms.yaml from vendor docs (about 1 min) |
| `miniyaml.py` | reader/writer for the YAML subset the glossary files use |

1. **Rules** in `asr_fixes.yaml` fix known mis-hearings ("G Forex" -> G4X, "volutric" -> volumetric,
   "keon" -> KOEO, "barrow" -> baro, "model mode" -> modelled mode, ...). Each rule records the evidence it
   was added on. Add rules only after checking hits with `kwic`; keep patterns narrow.
2. **Noise lines:** a line with three or more distinct words found in neither the vocabulary nor the
   glossary is prefixed `[low-confidence]`.
3. **Poor files:** low tuning-word density (with or without noise lines) marks the file
   `caption_quality: poor`. These are whole transcripts where auto-captioning produced unrelated text, usually
   over dyno or workshop noise. The ingestor drops them; re-transcribe from audio if the content matters.

First run (practitioner training youtube-auto captions, 230 files, 2026-11-08): 329 fixes, 31 noise lines (1.2 %), 10 poor

## Not yet covered
- Reflash tools (HP Tuners, COBB, EcuTek, Hondata, WinOLS) name tables after the OEM calibration, so
  `platform_terms.py` does not generate files for them yet.
- Whisper and practitioner training transcripts have not been scanned. Run the read-only report on them once Whisper has
  finished, and add any new mis-hearings as rules.
