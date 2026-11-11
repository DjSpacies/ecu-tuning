#!/usr/bin/env python3
"""Replay mock of the ECU tool interface (docs/MCP-INTERFACE.md), for developing workflows without hardware.

Implements every operation over a normalised Log and tables. `apply_write` exists only here and changes only the
in-memory copy. It runs as JSON-RPC 2.0 over stdin/stdout (one object per line) so any harness can drive it.
"""
import copy, json, sys, uuid
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path[:0] = [str(ROOT / "tools" / "log-schema"), str(ROOT / "tools" / "analysis")]
from schema import Log, Table, CHANNELS   # noqa: E402

class ToolError(Exception):
    def __init__(self, code, message): super().__init__(message); self.code = code

CAPABILITIES = ["read_live", "logging", "read_tables", "backup", "write_dryrun", "write"]

class MockTool:
    def __init__(self, log, tables, bounds=None, scalars=None, approvals=None, ecu="mock"):
        self.log, self.tables = log, {t.role: copy.deepcopy(t) for t in tables}
        self.bounds = bounds or {}          # role -> (min, max)
        self.scalars = dict(scalars or {})
        self.approvals = set(approvals or ())
        self.cursor = 0; self.backups, self.proposals, self.logs = {}, {}, {}
        self.logging = None; self.ecu = ecu; self.has_backup = False

    # ---- always available ----
    def capabilities(self): return dict(ecu_family=self.ecu, firmware="replay", ops=CAPABILITIES, limits=dict(self.bounds))
    def connection_status(self): return dict(connected=True, engine_running=self.cursor < len(self.log), logging=self.logging is not None, replay=True)

    # ---- live data ----
    def list_channels(self): return [dict(name=n, unit=CHANNELS[n], native_name=self.log.meta.get("native_names", {}).get(n, n)) for n in self.log.channels]
    def read_channels(self, names, rate=None):
        for n in names:
            if n not in self.log.channels: raise ToolError("unknown_channel", n)
        i = min(self.cursor, len(self.log) - 1); self.cursor += 1
        return dict(time_s=self.log.time_s[i], values={n: dict(value=self.log.channels[n][i], unit=CHANNELS[n]) for n in names})

    # ---- logging ----
    def start_log(self, channels):
        for n in channels:
            if n not in self.log.channels: raise ToolError("unknown_channel", n)
        self.logging = dict(channels=channels, start=self.cursor); return dict(started=True)
    def stop_log(self):
        if not self.logging: raise ToolError("not_logging", "no log in progress")
        id_ = uuid.uuid4().hex[:8]; self.logs[id_] = (self.logging, self.cursor); self.logging = None; return dict(id=id_)
    def get_log(self, id):
        if id not in self.logs: raise ToolError("unknown_log", id)
        (spec, end) = self.logs[id]; a, b = spec["start"], max(end, spec["start"] + 1)
        return dict(time_s=self.log.time_s[a:b], channels={n: self.log.channels[n][a:b] for n in spec["channels"]}, units={n: CHANNELS[n] for n in spec["channels"]})

    # ---- tables ----
    def list_tables(self): return [dict(id=r, role=r, native_name=t.native_name, unit=t.unit) for r, t in self.tables.items()]
    def _table(self, id_):
        if id_ not in self.tables: raise ToolError("unknown_table", id_)
        return self.tables[id_]
    def get_table(self, id):
        t = self._table(id); return dict(id=id, role=t.role, x_axis=t.x_axis, y_axis=t.y_axis, values=t.values, unit=t.unit, native_name=t.native_name)
    def list_scalars(self): return sorted(self.scalars)
    def get_scalar(self, id):
        if id not in self.scalars: raise ToolError("unknown_scalar", id)
        return dict(id=id, value=self.scalars[id])

    # ---- backup ----
    def backup(self, label):
        id_ = uuid.uuid4().hex[:8]; self.backups[id_] = dict(label=label, tables=copy.deepcopy(self.tables)); self.has_backup = True
        return dict(backup_id=id_, label=label)
    def restore(self, backup_id):
        if backup_id not in self.backups: raise ToolError("unknown_backup", backup_id)
        self.tables = copy.deepcopy(self.backups[backup_id]["tables"]); return dict(restored=True)

    # ---- writes ----
    def _check(self, ch):
        t = self._table(ch["table"]); r, c = ch["row"], ch["col"]
        if not (0 <= r < len(t.values) and 0 <= c < len(t.values[0])): raise ToolError("out_of_range", f"cell {r},{c}")
        lo, hi = self.bounds.get(ch["table"], (float("-inf"), float("inf")))
        if not lo <= ch["value"] <= hi: raise ToolError("out_of_bounds", f"{ch['value']} outside {lo} to {hi}")
        return t, r, c

    def propose_write(self, changes):
        """Dry run: validates bounds and returns a diff. Has no effect."""
        diff = []
        for ch in changes:
            t, r, c = self._check(ch); diff.append(dict(ch, before=t.values[r][c], after=ch["value"]))
        id_ = uuid.uuid4().hex[:8]; self.proposals[id_] = dict(changes=copy.deepcopy(changes), diff=diff)
        return dict(proposal_id=id_, diff=diff)

    def apply_write(self, proposal_id, approval_token):
        if proposal_id not in self.proposals: raise ToolError("unknown_proposal", proposal_id)
        if approval_token not in self.approvals: raise ToolError("not_approved", "a human-issued approval token is required")
        if not self.has_backup: raise ToolError("no_backup", "take a backup first")
        p = self.proposals.pop(proposal_id); self.approvals.discard(approval_token)
        result = []
        for ch in p["changes"]:
            t, r, c = self._check(ch); before = t.values[r][c]; t.values[r][c] = ch["value"]; result.append(dict(ch, before=before, after=t.values[r][c]))
        return dict(applied=True, changes=result)

    def get_protections(self): return dict(limits=dict(self.bounds))
    def event_stream(self): return []

OPS = ["capabilities", "connection_status", "list_channels", "read_channels", "start_log", "stop_log", "get_log", "list_tables", "get_table", "get_scalar", "list_scalars", "backup", "restore", "propose_write", "apply_write", "get_protections", "event_stream"]

def handle(tool, req):
    """One JSON-RPC 2.0 request to one response."""
    rid = req.get("id"); method = req.get("method"); params = req.get("params") or {}
    if method not in OPS: return dict(jsonrpc="2.0", id=rid, error=dict(code=-32601, message=f"unknown method {method}"))
    try: return dict(jsonrpc="2.0", id=rid, result=getattr(tool, method)(**params))
    except ToolError as e: return dict(jsonrpc="2.0", id=rid, error=dict(code=-32000, message=str(e), data=dict(reason=e.code)))
    except TypeError as e: return dict(jsonrpc="2.0", id=rid, error=dict(code=-32602, message=str(e)))

def serve(tool, stdin=sys.stdin, stdout=sys.stdout):
    for line in stdin:
        if line.strip(): stdout.write(json.dumps(handle(tool, json.loads(line))) + "\n"); stdout.flush()
