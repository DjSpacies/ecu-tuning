---
id: platforms/link-g4plus/formats
title: Link G4+ file formats
layer: L3
status: draft
confidence: medium
sources: [vendor-documentation, file-format-analysis]
verified: 2026-11-10
applies_to: {fuels: [gasoline, ethanol, methanol], engines: [all]}
depends_on: []
supersedes: []
---

# Link G4+ file formats

Evidence tags: `vendor-doc`, `re-derived`, `sample-observed`.

## Tune files (.pclr)
- `re-derived`: an encoded container of little-endian 32-bit words. Decoded plaintext is a 12-byte header (a generated word, the XML byte length, a marker word) followed by the XML and 1 to 4 padding bytes.
- `re-derived`: the key is held in PCLink.exe at virtual address 0x0094DD3C. It is not stored in this repository; `parser/pclr.py` reads it from a local PCLink.exe or takes it as an argument.
- `sample-observed`: the document is `<LinkStorage Version="100" Type=".xml">` with `Memory` (firmware, serial) and `Map`. Map entries have `DataId`, `Type`, and either `Value` or `RowCount`/`ColCount` with `RowN` value lists. All 45 vendor samples decode and parse.
- `sample-observed`: table values are stored in display units (a fuel cell reads 62.3, not a raw integer). File-format analysis leaves the precise domain of saved values partly open, so treat this as observed, not proven.
- `sample-observed`: axis arrays are padded with filler (zeros, or a repeated value) beyond the zones in use. The adapter keeps the leading increasing part.
- Writing tunes is not implemented, by design.

## Log files (.llg)
`sample-observed`; there is no published format. Two layouts exist; the parser recognises both by content and refuses a
file it cannot read.
- `lf2` (older PCLink): 4 bytes of length, then the tag `lf2` and a version byte (0x43 and 0x13 seen). Fixed 200-byte
  UTF-16 text fields for driver, vehicle, engine, ECU and session; a marker list ends with `1EOL`. One record per
  channel: a 32-bit id, a 200-byte name, a 200-byte unit, a 64-bit interval in seconds, then pairs of 32-bit floats
  (value, time). Newer files repeat the name, 204 bytes earlier, without an id.
- `lf3` (PCLink 5.6.x): tagged blocks of `[u32 size][3-byte tag]`. Each channel block holds its sample count, id,
  UTF-16 name and unit, the logging interval, then (time, value) float pairs recorded only when the value changes.
  Channels are therefore resampled onto a common time grid (zero-order hold; holes longer than 1 s are not filled).
  Pressure channels may carry the quantity name "Pressure" instead of a unit; their values are kPa.
- Channel ids match the DataId of the same parameter in the tune definition (Engine Speed = 1000, MAP = 1001).

## CSV exports
Not read; use the native .llg file.
