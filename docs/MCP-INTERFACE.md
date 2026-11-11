# ECU tool interface (v1, draft)

Few/no ECU vendors expose MCP today. This is a vendor-neutral contract so a vendor or
community project can implement it, and the skill can use any implementation.

## Principles
- **Capability negotiation:** `capabilities()` returns what is supported; the skill adapts.
  A read-only tool still gets full analysis.
- **Safety in the tool, not just the agent:** tools should enforce backup-before-write and bounds.
- **Units explicit** in every value. **Canonical channel names** with `native_name` mapping.
- **Idempotent, versioned** operations; every write returns the before/after.

## Operations (draft)
| Op | Description | Cap flag |
|---|---|---|
| `capabilities()` | ecu family, firmware, supported ops, limits | always |
| `connection_status()` | connected, engine running, logging state | always |
| `list_channels()` / `read_channels(names, rate?)` | live values; canonical + native names, units | read_live |
| `start_log(channels)` / `stop_log()` / `get_log(id)` | logging, normalised schema export | logging |
| `list_tables()` / `get_table(id)` | axes, values, units, role tag | read_tables |
| `get_scalar(id)` / `list_scalars()` | single parameters | read_tables |
| `backup(label)` / `restore(backup_id)` | full tune backup | backup |
| `propose_write(changes[])` | dry run: validate bounds, return diff, no effect | write_dryrun |
| `apply_write(proposal_id, approval_token)` | applies approved proposal; returns before/after | write |
| `set_trim_live(...)` | optional bounded real-time adjustment | live_trim |
| `get_protections()` | ECU-side limits/cuts configured | read_tables |
| `event_stream()` | faults, cuts, knock events | events |

## Write approval
`apply_write` requires an approval token issued by the human via the harness (or by a
pre-authorised policy within safety/limits). Tools must reject writes outside declared bounds.

## Transport
JSON-RPC 2.0, one object per line, with method names as the operation names above and parameters by name. An MCP server can expose the same operations as tools. A method not supported returns error code -32601; bad parameters -32602; a refused operation -32000 with `data.reason`.

## Error reasons
`unknown_channel`, `unknown_table`, `unknown_scalar`, `unknown_log`, `unknown_backup`, `unknown_proposal`, `out_of_range`, `out_of_bounds`, `not_approved`, `no_backup`, `not_logging`.

## Write rules (normative)
- `propose_write(changes)`: each change is `{table, row, col, value}`. It has no effect, returns a `proposal_id` and a diff with `before` and `after`, and rejects anything outside bounds.
- `apply_write(proposal_id, approval_token)`: requires a backup taken first and a human-issued token. Tokens and proposals are single use.
- A tool must not offer a write path that skips these.

## For integrators
See tools/mcp-mock/INTEGRATOR.md. `tools/mcp-mock/conformance.py` is the test suite; `server.py` is a replay implementation over a saved log and tune.
