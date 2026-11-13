# ECU tuning skill

An agent skill and knowledge ecosystem for **ECU tuning of gasoline / ethanol /
methanol engines** (performance-oriented). Diesel is out of scope.

It lets an agent (any capable model/harness) go from a tune file + log file, to
guided road/dyno sessions, to live tuning through an ECU tool interface (MCP). Design is top-down: a strong first-principles foundation, then methodology, then platform and
application specifics.

**Quickstart: docs/SETUP.md.** Contributing: CONTRIBUTING.md.

## Start here
- docs/ARCHITECTURE.md     layers, repo layout, data flow
- docs/SOURCE-POLICY.md    source-of-truth tiers and conflict handling
- docs/SETUP-PROFILE.md    how the agent discovers unknowns and asks questions
- docs/KB-ENTRY-SCHEMA.md  format for every knowledge-base entry
- docs/OPERATING-MODES.md  offline / road (incl. voice) / dyno / live
- docs/MCP-INTERFACE.md    ECU-tool interface for integrators
- docs/SAFETY.md           safety model and hard rules
- docs/PLATFORM-ADAPTERS.md  adapter contract
