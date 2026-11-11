# Work through a live ECU tool

## Inputs
- Required: a tool implementing docs/MCP-INTERFACE.md, and everything the underlying workflow requires. Safety critical: an approval path that is a human, and declared limits.
- Useful: the tool's capabilities and its protections.
- Irrelevant: everything else; do not ask for it.

## Load only
- docs/MCP-INTERFACE.md
- the workflow for the task
- safety/limits.yaml and safety/aborts.yaml

## Steps
1. Call `capabilities()` and adapt. Missing read or log operations mean falling back to file-based work.
2. Read only, by default. The autonomy ladder starts at advise (docs/OPERATING-MODES.md). This skill has not passed D3 bench testing on any ECU, so treat every write path as unproven.
3. For any change: take a `backup`, then `propose_write`, show the diff, and wait for the human's token. Then `apply_write`, and read the cell back.
4. Roll back with `restore` on any surprise.

## Refuse when
The approval path is not a human, a backup fails, the tool lacks bounds, or the vehicle is moving.
