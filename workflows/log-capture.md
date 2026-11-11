# Plan a log, then check it was captured properly

Use this before any offline analysis when the user has no suitable log yet, and on every log before fuel or ignition
work. The quality of a log sets the quality of every answer drawn from it.

## Inputs
- Required: the analysis the user wants (fuel, warm-up, ignition, boost, general health). For the review: the log.
- Safety critical for full-load phases: max_rpm, max_boost_kpa (boosted engines), fuel, knock_detection. Without them,
  the plan leaves full-load pulls out and says why.
- Useful: the tune (so the plan can name the ECU's own channel and table-output names).
- Irrelevant: everything else; do not ask for it.

## Load only
- methodology/log-capture-protocol
- methodology/data-quality
- safety/limits.yaml and safety/aborts.yaml
- the platform's semantics.md and channels.yaml

## Steps
1. **Plan.** From methodology/log-capture-protocol, give the user a short capture plan for their analysis: what to save
   first, which channels to add (using the platform's names), whether closed loop should be off, and the phases to
   record in order. Leave out phases the analysis does not need. Leave out full-load pulls unless every
   safety-critical input above is declared and the user has a dyno, track or closed road.
2. **Record the session facts.** Ask once, after the log: was anything changed in the ECU while it recorded; is the
   tune file the one that was in the ECU, saved after the last change; was closed loop on; which fuel.
   A log holds no record of live edits, so these answers are evidence, not formalities.
3. **Review.** Run `python3 -I tools/analysis/run.py log-capture-review --platform <ecu> --log LOG [--tune TUNE]`, then
   `log-health-check`. When a tune is given, every workflow also compares logged table outputs with the tune file.
4. **Report** which phases the log holds, what is missing, whether the tune file matches what ran, and the exact
   changes to make for the next log. Analyse only the phases that are present.

## Refuse when
Asked to plan full-load pulls with the rev limit, boost ceiling, fuel or knock detection unknown, or on a public road.
Refuse fuel or ignition changes from a log whose tune file does not match what ran, or whose live edits are unknown.
