#!/usr/bin/env python3
"""Conformance tests for any implementation of docs/MCP-INTERFACE.md. Point `make_tool` at your own server to use them.

Usage: python3 -I tools/mcp-mock/conformance.py
"""
import sys, unittest
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
import server as S  # noqa: E402
from schema import Log, Table  # noqa: E402

def make_tool(approvals=("tok1",)):
    log = Log([0.0, 0.05, 0.1, 0.15], {"rpm": [3000.0] * 4, "map_kpa": [100.0, 101.0, 102.0, 103.0]}, {})
    t = Table("ve", [2000.0, 3000.0], [80.0, 100.0], [[70.0, 75.0], [80.0, 85.0]], "%", native_name="VE")
    return S.MockTool(log, [t], bounds={"ve": (40.0, 130.0)}, scalars={"stoich": 14.7}, approvals=approvals)

class Interface(unittest.TestCase):
    def setUp(self): self.t = make_tool()
    def test_capabilities_and_status(self):
        self.assertIn("read_tables", self.t.capabilities()["ops"]); self.assertTrue(self.t.connection_status()["connected"])
    def test_every_listed_op_exists(self):
        for op in S.OPS: self.assertTrue(callable(getattr(self.t, op)), op)
    def test_units_explicit(self):
        v = self.t.read_channels(["map_kpa"])["values"]["map_kpa"]; self.assertIn("unit", v); self.assertEqual(v["unit"], "kPa abs")
    def test_canonical_channels_listed(self): self.assertEqual({c["name"] for c in self.t.list_channels()}, {"rpm", "map_kpa"})
    def test_unknown_channel(self):
        with self.assertRaises(S.ToolError): self.t.read_channels(["nope"])
    def test_log_round_trip(self):
        self.t.start_log(["rpm"]); self.t.read_channels(["rpm"]); self.t.read_channels(["rpm"])
        lid = self.t.stop_log()["id"]; g = self.t.get_log(lid)
        self.assertEqual(len(g["channels"]["rpm"]), 2); self.assertEqual(g["units"]["rpm"], "rpm")
    def test_table_read(self):
        g = self.t.get_table("ve"); self.assertEqual(g["values"][1][1], 85.0); self.assertEqual(g["unit"], "%"); self.assertEqual(g["role"], "ve")

class Writes(unittest.TestCase):
    CH = [dict(table="ve", row=0, col=0, value=72.0)]
    def setUp(self): self.t = make_tool()
    def test_propose_has_no_effect_and_returns_diff(self):
        d = self.t.propose_write(self.CH); self.assertEqual(self.t.get_table("ve")["values"][0][0], 70.0)
        self.assertEqual(d["diff"][0]["before"], 70.0); self.assertEqual(d["diff"][0]["after"], 72.0)
    def test_out_of_bounds_rejected(self):
        with self.assertRaises(S.ToolError) as c: self.t.propose_write([dict(table="ve", row=0, col=0, value=500.0)])
        self.assertEqual(c.exception.code, "out_of_bounds")
    def test_bad_cell_rejected(self):
        with self.assertRaises(S.ToolError): self.t.propose_write([dict(table="ve", row=9, col=0, value=70.0)])
    def test_write_needs_token(self):
        self.t.backup("b"); p = self.t.propose_write(self.CH)["proposal_id"]
        with self.assertRaises(S.ToolError) as c: self.t.apply_write(p, "forged")
        self.assertEqual(c.exception.code, "not_approved"); self.assertEqual(self.t.get_table("ve")["values"][0][0], 70.0)
    def test_write_needs_backup(self):
        p = self.t.propose_write(self.CH)["proposal_id"]
        with self.assertRaises(S.ToolError) as c: self.t.apply_write(p, "tok1")
        self.assertEqual(c.exception.code, "no_backup")
    def test_apply_returns_before_after(self):
        self.t.backup("b"); p = self.t.propose_write(self.CH)["proposal_id"]; r = self.t.apply_write(p, "tok1")
        self.assertEqual(r["changes"][0]["before"], 70.0); self.assertEqual(r["changes"][0]["after"], 72.0); self.assertEqual(self.t.get_table("ve")["values"][0][0], 72.0)
    def test_token_is_single_use(self):
        self.t.backup("b"); p = self.t.propose_write(self.CH)["proposal_id"]; self.t.apply_write(p, "tok1")
        p2 = self.t.propose_write(self.CH)["proposal_id"]
        with self.assertRaises(S.ToolError): self.t.apply_write(p2, "tok1")
    def test_proposal_is_single_use(self):
        self.t.backup("b"); p = self.t.propose_write(self.CH)["proposal_id"]; self.t.apply_write(p, "tok1")
        with self.assertRaises(S.ToolError): self.t.apply_write(p, "tok1")
    def test_restore(self):
        b = self.t.backup("b")["backup_id"]; p = self.t.propose_write(self.CH)["proposal_id"]; self.t.apply_write(p, "tok1"); self.t.restore(b)
        self.assertEqual(self.t.get_table("ve")["values"][0][0], 70.0)

class Rpc(unittest.TestCase):
    def test_success_and_errors(self):
        t = make_tool(); r = S.handle(t, dict(jsonrpc="2.0", id=1, method="get_table", params=dict(id="ve")))
        self.assertEqual(r["result"]["role"], "ve")
        self.assertEqual(S.handle(t, dict(id=2, method="format_ecu"))["error"]["code"], -32601)
        self.assertEqual(S.handle(t, dict(id=3, method="get_table", params=dict(id="zz")))["error"]["data"]["reason"], "unknown_table")
        self.assertEqual(S.handle(t, dict(id=4, method="get_table", params=dict(bad=1)))["error"]["code"], -32602)

if __name__ == "__main__":
    unittest.main()
