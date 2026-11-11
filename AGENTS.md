# AGENTS.md
This repository is an agent skill. Entry point: SKILL.md. Read docs/ARCHITECTURE.md
before modifying the structure. Rules for contributors/agents:
- No model- or vendor-specific features in the core (plain markdown, YAML, Python).
- Never put a specific user's vehicle/setup data in the repo.
- Never commit anything under collateral/ or inbox/.
- Every KB claim needs a source tier and confidence (docs/KB-ENTRY-SCHEMA.md).
- ~/Projects/reverse-engineering/pclink-g4plus is a READ-ONLY reference. Never write there.
- Diesel is out of scope.
