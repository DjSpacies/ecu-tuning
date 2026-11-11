# Link G4+ adapter (draft)

Family: Link G4+ (PCLink 5.6.x). Reads tunes (.pclr or decoded XML) and ECU logs (.llg). Does not write tunes.

Built from the vendor help, 45 vendor sample tunes, two vendor sample logs and read-only reverse-engineering notes.
**Not yet verified against the user's own files.** Each fact is tagged `vendor-doc`, `re-derived` or `sample-observed`.

| File | Holds |
|---|---|
| `formats.md` | File formats |
| `channels.yaml` | Native log channel to canonical channel |
| `tables.yaml` | Native table to role |
| `semantics.md`, `quirks.md`, `inference.md` | Behaviour, gotchas, what files reveal |
| `parser/` | `llg.py`, `pclr.py`, `adapter.py`, tests over the samples |
| `terms.yaml` | Vocabulary, generated |
