"""CSV log reader for this platform. Column names are assumptions recorded in ../channels.yaml; see ../formats.md."""
import csv, sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[2]
sys.path[:0] = [str(ROOT / "tools" / "log-schema"), str(ROOT / "tools" / "common")]
import miniyaml        # noqa: E402
from schema import Log # noqa: E402

def load_log(path):
    cfg = miniyaml.load((HERE.parent / "channels.yaml").read_text(encoding="utf8"))
    with open(path, newline="", encoding="utf8") as f:
        rows = list(csv.DictReader(f))
    if not rows or "Time" not in rows[0]: raise ValueError("expected a CSV with a Time column")
    channels = {c["canonical"]: [float(r[c["column"]]) for r in rows] for c in cfg["channels"] if c["column"] in rows[0]}
    return Log([float(r["Time"]) for r in rows], channels, dict(adapter="haltech", notes=["CSV column names are assumed, not confirmed"]))

def load_tune(path, key=None, exe=None):
    raise ValueError("this adapter cannot read tune files")
