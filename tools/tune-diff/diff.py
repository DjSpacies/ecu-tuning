#!/usr/bin/env python3
"""Compare two tunes through a platform adapter: which tables, arrays and settings changed, where and by how much.

Read-only. Prints JSON. The output is evidence for a conversation ("why was this changed?"), not a judgement.

  python3 -I tools/tune-diff/diff.py --platform link-g4plus OLD NEW [--exe PCLink.exe]
"""
import argparse, json, os, sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path[:0] = [str(ROOT / "tools" / "analysis")]

def _num(v):
    try: return float(v)
    except (TypeError, ValueError): return None

def diff_tables(a, b, tol=1e-6):
    """Cells that differ, on shared axes; a change of axes is reported as such, not as cell differences."""
    if a.x_axis != b.x_axis or a.y_axis != b.y_axis:
        return dict(axes_changed=True, old_axes=[a.x_axis, a.y_axis], new_axes=[b.x_axis, b.y_axis])
    cells = []
    for r, (ra, rb) in enumerate(zip(a.values, b.values)):
        for c, (va, vb) in enumerate(zip(ra, rb)):
            if abs(va - vb) > tol:
                cells.append(dict(row=r, col=c, x=a.x_axis[c], y=a.y_axis[r], old=va, new=vb,
                                  change=round(vb - va, 4), change_pct=round(100 * (vb - va) / va, 2) if va else None))
    if not cells: return None
    ch = [x["change"] for x in cells]
    pct = [x["change_pct"] for x in cells if x["change_pct"] is not None]
    total = len(a.x_axis) * len(a.y_axis)
    out = dict(cells_changed=len(cells), of=total, min_change=min(ch), max_change=max(ch),
               rpm_range=[min(x["x"] for x in cells), max(x["x"] for x in cells)],
               load_range=[min(x["y"] for x in cells), max(x["y"] for x in cells)], cells=cells)
    if pct and len(cells) == total and max(pct) - min(pct) < 0.5:
        out["pattern"] = f"whole table scaled by about {sum(pct) / len(pct):+.1f} %"
    elif len(set(ch)) == 1:
        out["pattern"] = f"uniform offset of {ch[0]:+g} over the changed cells"
    return out

def diff_tunes(old, new):
    out = dict(tables={}, tables_added=[], tables_removed=[], arrays={}, scalars={}, protections={})
    to, tn = old.get("tables", {}), new.get("tables", {})
    for role in sorted(set(to) | set(tn)):
        if role not in to: out["tables_added"].append(role); continue
        if role not in tn: out["tables_removed"].append(role); continue
        d = diff_tables(to[role], tn[role])
        if d: out["tables"][role] = dict(native=tn[role].native_name, **d)
    ao, an = old.get("arrays", {}), new.get("arrays", {})
    for k in sorted(set(ao) | set(an)):
        if ao.get(k) != an.get(k): out["arrays"][k] = dict(old=ao.get(k), new=an.get(k))
    for key in ("scalars", "protections"):
        so, sn = old.get(key, {}), new.get(key, {})
        for k in sorted(set(so) | set(sn)):
            if so.get(k) != sn.get(k):
                rec = dict(old=so.get(k), new=sn.get(k))
                a, b = _num(so.get(k)), _num(sn.get(k))
                if a is not None and b is not None and b == 0 and a != 0: rec["note"] = "set to zero"
                out[key][k] = rec
    out["summary"] = (f"{len(out['tables'])} tables, {len(out['arrays'])} arrays and {len(out['scalars'])} settings changed"
                      + (f"; protections changed: {', '.join(out['protections'])}" if out["protections"] else ""))
    return out

def main():
    import run
    ap = argparse.ArgumentParser(); ap.add_argument("--platform", required=True); ap.add_argument("old"); ap.add_argument("new")
    ap.add_argument("--exe", default=os.environ.get("PCLINK_EXE", "")); ap.add_argument("--cells", action="store_true", help="include every changed cell")
    a = ap.parse_args()
    ad = run.load_adapter(a.platform)
    kw = dict(exe=a.exe) if a.exe else {}
    d = diff_tunes(ad.load_tune(a.old, **kw), ad.load_tune(a.new, **kw))
    if not a.cells:
        for t in d["tables"].values(): t.pop("cells", None)
    print(json.dumps(d, indent=1, default=str))

if __name__ == "__main__":
    main()
