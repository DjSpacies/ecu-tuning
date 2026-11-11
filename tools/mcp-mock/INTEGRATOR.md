# Implementing the ECU tool interface

For anyone connecting a real ECU tool to this skill. Contract: docs/MCP-INTERFACE.md.

1. **Declare capabilities.** A read-only tool is valid; the skill adapts. Offer only what works.
2. **Use canonical names.** Channels and table roles are in `tools/log-schema/schema.py`. Keep the native name alongside, and put your mapping in `platforms/<ecu>/mcp-map.yaml`.
3. **Make units explicit** on every value.
4. **Enforce safety in the tool.** Bounds, backup before write and approval tokens live on your side as well. The skill's own checks are not a substitute.
5. **Run conformance.** Change `make_tool` in `conformance.py` to build your server, then run it. All tests must pass before the skill connects.
6. **Then bench test** (docs/VALIDATION.md, D3): engine off, read, write, read back, revert. Every write must land in the intended cell with the intended units. Passing the mock does not prove this.

No real ECU has been connected to this interface yet.
