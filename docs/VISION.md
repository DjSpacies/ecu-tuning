# Vision

## Goal
An agent skill that can perform the full range of tuning tasks on gasoline, ethanol
and methanol performance engines, from static analysis of a log and tune file through
to guided road/dyno sessions and live tuning via an ECU interface (MCP) when it exists.

## The brief (keep to it)
Build a tuning equivalent of REA (Reverse Engineer Anything): a skill that is **buildable**
(useful from the first module, grown piece by piece), **expandable** (new knowledge, ECUs, tools and
modes slot in without rewrites), **platform-agnostic** (the core knows physics and method, never a
specific ECU) and **split into small sub-modules** that an agent loads only when a task needs them.

Design rules that stop us building into a corner:
- Core layers (L0-L2, workflows, safety) never name an ECU, tool or vendor table. They speak in
  canonical channels and table roles (docs/ARCHITECTURE.md); adapters translate.
- A new ECU is a new `platforms/<ecu>/` folder and nothing else. If adding one needs a core edit,
  the core is wrong; fix the abstraction, don't special-case.
- A new tool or live interface implements the MCP contract (docs/MCP-INTERFACE.md); workflows don't
  change.
- One idea per KB file, with provenance and status, so knowledge is refined or superseded, not rewritten.
- Workflows declare their required inputs and the exact files they load (progressive disclosure),
  so the skill stays usable on small-context models.
- Everything is plain markdown/YAML/stdlib Python; no harness- or model-specific features in the core.
- What the agent learns in use goes back in through the same channels (KB entries, adapter quirks,
  evals; docs/VALIDATION.md), never as ad-hoc patches in prompts.

## Principles
1. **Physics first.** Methodology is derived from, and checked against, first principles
   (thermodynamics, combustion, fluid dynamics, control theory, statistics). Folklore is
   not knowledge.
2. **Source discipline.** Tiered sources (docs/SOURCE-POLICY.md). Forum/Facebook claims
   are hypotheses to test, never facts.
3. **Discover, then ask.** Unlike reverse engineering, key inputs (cams, turbo, injectors,
   fuel, compression, intended use) are often not in the files. Infer what can be inferred,
   ask for the rest, never silently assume anything safety-relevant.
4. **No stored user data.** The repo holds knowledge, never a particular car's details.
5. **Safety is structural.** Limits, step sizes, backups, abort conditions are built into
   every workflow, not bolted on (docs/SAFETY.md).
6. **Portable.** Plain markdown/YAML/Python. Works across models and agent harnesses.
7. **Future-proof.** New ECUs = new adapter folder. New tools = implement the MCP interface.
   Knowledge is versioned with provenance so it can be refined without being lost.
8. **Honest.** Output states what was measured, inferred, assumed, or asked, with confidence.

## Non-goals
- Diesel engines (compression ignition) of any kind.
- Emissions-defeat or anything illegal; the skill is for competition/off-road/legal
  jurisdictions and the user is responsible for legality.
- Replacing the ECU's own protections or a competent human on the dyno/road.
- Reproducing licensed course material.
