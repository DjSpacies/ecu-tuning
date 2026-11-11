#!/usr/bin/env python3
"""D1 replay (docs/VALIDATION.md): the fuel workflow reads through the tool interface and proposes through dry-run only.

Passes when proposals match a direct analysis, every proposal is accepted as a dry run, the table is untouched, and an
out-of-bounds proposal is refused. No real log is used: inputs come from the simulator.
"""
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path[:0] = [str(ROOT / "tools" / "mcp-mock"), str(ROOT / "tools" / "sim"), str(ROOT / "tools" / "analysis"), str(ROOT / "tools" / "log-schema")]
import server as S                       # noqa: E402
from engine import Engine, starting_tables, RPM, LOAD   # noqa: E402
import analyses                          # noqa: E402
from limits import Limits                # noqa: E402
from profile import Profile              # noqa: E402
from schema import Log, Table            # noqa: E402

CAPS = {"fuel_change_rich_max_pct": 10.0, "fuel_change_lean_max_pct": 5.0}

def replay(seed):
    eng = Engine(seed); ve, tgt = starting_tables(eng)
    log = eng.hold(ve, tgt, [(x, y) for x in RPM[1:] for y in LOAD])
    prof = Profile(dict(fuel="gasoline", wideband_valid=True, limits=CAPS))
    direct = analyses.fuel_analysis(log, ve, tgt, prof, Limits(CAPS))
    tool = S.MockTool(log, [ve, tgt], bounds={"ve": (1.0, 200.0)})
    rpc = lambda m, **p: S.handle(tool, dict(jsonrpc="2.0", id=1, method=m, params=p))
    assert "read_tables" in rpc("capabilities")["result"]["ops"]
    g = rpc("get_table", id="ve")["result"]; gt = rpc("get_table", id="lambda_target")["result"]
    before = [list(r) for r in g["values"]]
    ve2 = Table("ve", g["x_axis"], g["y_axis"], g["values"], g["unit"], native_name=g["native_name"])
    tgt2 = Table("lambda_target", gt["x_axis"], gt["y_axis"], gt["values"], gt["unit"])
    res = analyses.fuel_analysis(log, ve2, tgt2, prof, Limits(CAPS))
    assert [p["cell"] for p in res.proposals] == [p["cell"] for p in direct.proposals], "proposals differ from direct analysis"
    assert res.proposals, "expected proposals"
    changes = [dict(table="ve", row=p["cell"][0], col=p["cell"][1], value=p["proposed"]) for p in res.proposals]
    out = rpc("propose_write", changes=changes)
    assert "result" in out and len(out["result"]["diff"]) == len(changes), out
    assert rpc("get_table", id="ve")["result"]["values"] == before, "a dry run changed the table"
    bad = rpc("propose_write", changes=[dict(table="ve", row=0, col=0, value=999.0)])
    assert bad["error"]["data"]["reason"] == "out_of_bounds"
    assert rpc("apply_write", proposal_id=out["result"]["proposal_id"], approval_token="none")["error"]["data"]["reason"] == "not_approved"
    assert rpc("get_table", id="ve")["result"]["values"] == before, "an unapproved write changed the table"
    return len(changes)

if __name__ == "__main__":
    n = [replay(s) for s in range(10)]
    print(f"D1 replay: {len(n)} runs passed, {sum(n)} dry-run proposals, table never changed")
