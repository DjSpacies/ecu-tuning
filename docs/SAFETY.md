# Safety model

An agent making confident bad changes can destroy an engine or hurt people. Safety is part of
every workflow's definition.

## Hard rules
1. Never apply or recommend a change to a safety-critical parameter if its governing unknown
   (fuel type, knock detection, boost ceiling, fuel system capacity, wideband validity) is `unknown`.
2. Backup before any write (file copy, or tool `backup`); verify backup; state rollback path.
3. **Step limits:** per-parameter maximum change per iteration (safety/limits.yaml), smaller
   when confidence is low or margin to a limit is thin.
4. **Direction asymmetry:** changes that add risk (more timing, more boost, leaner) are held to
   a higher evidence bar and smaller steps than risk-reducing changes.
5. **Data-quality gate before any change** (warm, steady, valid sensors, enough samples).
6. **Abort conditions** defined per run: knock, lean beyond limit, boost overshoot, EGT/temps,
   oil pressure/fuel pressure if logged, ECU protection triggers.
7. Respect ECU-level protections; never advise disabling them to "get the tune to work".
8. No live writes while the vehicle is moving unless explicitly enabled and bounded (default off).
9. Road: legality and public safety outrank data; recommend dyno where risk is high.
10. State uncertainty; "not enough data to change this safely" is a valid, preferred output.

## Limits files (machine-readable, to be authored)
safety/limits.yaml: default envelopes by fuel/aspiration (lambda floors under load, timing change
per step, boost change per step, etc.), always overridden to be MORE conservative by user limits.
Values will be sourced to tier A/B and cited, not invented.

## Confidence-scaled caution
Low confidence (many assumed fields) => smaller steps, more conservative envelope, prefer
information-gathering runs over changes.
