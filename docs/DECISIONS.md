# Decision log
| Date | Decision | Reason |
|---|---|---|
| 2026-11-06 | Top-down layered architecture (L0 physics -> L5 modes) | Mirrors REA; keeps physics as arbiter |
| 2026-11-06 | Source tiers A-D; forums never a source | Misinformation prevalence |
| 2026-11-06 | Session-scoped setup profile, no user data in repo | Skill must work for any setup |
| 2026-11-06 | One batched upfront question block, "I don't know" allowed, later questions permitted | User preference |
| 2026-11-06 | Link G4+ is first platform; pclink-g4plus RE project is read-only reference | User's own car; existing RE work |
| 2026-11-06 | Gasoline/ethanol/methanol only; diesel unsupported | Scope |
| 2026-11-06 | Portable core: markdown/YAML/Python, router SKILL.md, AGENTS.md | Support all popular models/agents |
| 2026-11-06 | MCP interface designed ahead of vendor support; mock replay server | No tools exist yet |
| 2026-11-06 | Voice content protocol for solo road tuning (STT/TTS supplied by harness) | User requirement |
| 2026-11-06 | practitioner training collateral is private training input, distilled not reproduced | Licence/permission scope |
| 2026-11-06 | Project dir ~/Projects/tuning-skill, working name | User; real name later |
| 2026-11-07 | Collect practitioner training free training sessions (EFI Tuning filter) as private collateral; transcribe the ones without transcripts locally | Many early training sessions have no transcript |
| 2026-11-07 | Local transcription on the host GPU (whisper.cpp Vulkan, medium.en), not cloud | Private material; RX 570 has no CUDA; ~98% agreement in benchmark |
| 2026-11-07 | English audio only; reject Vimeo's AI-dubbed Spanish track | Source is English; dubbing adds error |
| 2026-11-07 | Transcript provenance recorded per file (`transcript_source`) and ranked official > whisper > youtube-auto | Weight claims by transcript quality |
| 2026-11-07 | training courses: only courses the user's account owns; respect server "access denied"; no workarounds | Licence and access terms |
| 2026-11-07 | Prefer official course transcripts over audio+Whisper; audio only for lessons without one | Quality and GPU time |
| 2026-11-07 | practitioner training captions fetched from the host, not the VM | VM persistently rate-limited; host works |
| 2026-11-07 | Build a corpus index + gap report before ingestion; don't run it until collection is complete | Decide on extra sources from the gaps |
| 2026-11-07 | training course collection limited to the 3 courses already fetched; the other 16 won't be added | User decision |
| 2026-11-08 | practitioner training: audio + Whisper allowed for the 16 Link/EFI Advanced videos with no YouTube captions (exception to captions-only); Link G5 Teasers added to scope | User decision |
| 2026-11-08 | Brief restated: REA-style, buildable, expandable, platform-agnostic, small sub-modules; design rules in docs/VISION.md | User; avoid building into a corner |
| 2026-11-08 | Dry-run ladder D0-D5 before real tuning; learning loop via session logs -> KB/quirks/evals, no model training | Agent will err on software nuances; portability |
| 2026-11-08 | Vendor documentation is the authority for its own platform's facts (version-specific); collected for 9 standalone vendors | User: high trust in vendor docs |
| 2026-11-08 | Reflash/OEM-ECU tools in scope (HP Tuners, Hondata, COBB, EcuTek, WinOLS, EcuFlash); an engine textbook and Bosch textbooks in scope (user-owned copies) | User decision |
| 2026-11-08 | One canonical glossary (principles/glossary/terms.yaml, brand-neutral); per-platform vocabulary in platforms/<ecu>/terms.yaml generated from vendor docs with confirmed labels as overrides | Platform-agnostic core; new ECU = regenerate, no core change |
| 2026-11-08 | Transcript clean-up by rules + noise detection on copies at ingestion; whole garbage files dropped and re-transcribed with Whisper (10 practitioner training files), no blanket re-encoding | User: sample-and-fix, not re-encode everything |
| 2026-11-08 | Textbooks only from user-owned or purchased copies; provenance checked before ingestion; the user confirmed an engine-control textbook, an engine textbook, Turns and the ASTM standards are purchased | No piracy |
| 2026-11-09 | Corpus gap report scores long documents by passage, checks each topic against the source classes it needs, and leaves out diesel passages; flagged gaps are verified against the text before any source is added | First run was misleading: English words matched as jargon and whole books scored as one document |
| 2026-11-10 | Phase 3 built from vendor samples and the read-only RE notes while inbox/ is empty; every adapter fact tagged vendor-doc, re-derived or sample-observed | User lifted the hold for the unattended run |
| 2026-11-10 | Safety limits hold only sourced values; a value with no source stays `unknown` and needs a user limit before a change is proposed; user limits may only tighten | No invented safety numbers |
| 2026-11-10 | All KB entries, limits and workflows stay `draft` until a human promotes them; tune writing stays off | Unattended run; verification on real files is not possible yet |
| 2026-11-10 | The vendor decoding key is never stored in the repo; the parser reads it from a local PCLink.exe | Keep vendor material out of tracked files |
| 2026-11-10 | Data-gate thresholds are labelled project defaults in tools/analysis/gates.py rather than placed in limits.yaml | They set what data is usable, not how far a tune may change, and have no published source |



## Practitioner knowledge (2026-11-10)
Tacit tuner knowledge is learned from the whole corpus, not added case by case. The skill does not keep per-anecdote
entries or debriefs. Where practice in the sources rests on an observable test, the test goes into the analyses so the
skill checks the situation rather than copying an action. Practice that reduces protection is explained with its
trade-off and never recommended.
