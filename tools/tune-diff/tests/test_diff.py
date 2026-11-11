import sys, unittest
from pathlib import Path
ROOT = Path(__file__).resolve().parents[3]
sys.path[:0] = [str(ROOT / "tools" / "tune-diff"), str(ROOT / "tools" / "log-schema")]
from diff import diff_tunes   # noqa: E402
from schema import Table      # noqa: E402

def t(vals, x=(1000, 3000), y=(50, 100)): return Table("ve", list(x), list(y), vals, "%", native_name="Fuel Table 1")

class Diff(unittest.TestCase):
    def test_cells_and_ranges(self):
        d = diff_tunes(dict(tables={"ve": t([[50, 60], [70, 80]])}), dict(tables={"ve": t([[50, 66], [70, 80]])}))
        v = d["tables"]["ve"]; self.assertEqual(v["cells_changed"], 1); self.assertEqual(v["rpm_range"], [3000, 3000]); self.assertEqual(v["cells"][0]["change_pct"], 10.0)
    def test_whole_table_scale_recognised(self):
        d = diff_tunes(dict(tables={"ve": t([[50, 60], [70, 80]])}), dict(tables={"ve": t([[55, 66], [77, 88]])}))
        self.assertIn("scaled by about +10.0", d["tables"]["ve"]["pattern"])
    def test_axes_change_not_reported_as_cells(self):
        d = diff_tunes(dict(tables={"ve": t([[1, 2], [3, 4]])}), dict(tables={"ve": t([[1, 2], [3, 4]], x=(1000, 4000))}))
        self.assertTrue(d["tables"]["ve"]["axes_changed"])
    def test_zeroed_setting_flagged(self):
        d = diff_tunes(dict(scalars={"injector_dead_time_ms": "0.9"}), dict(scalars={"injector_dead_time_ms": "0"}))
        self.assertEqual(d["scalars"]["injector_dead_time_ms"]["note"], "set to zero")
    def test_identical(self):
        d = diff_tunes(dict(tables={"ve": t([[1, 2], [3, 4]])}), dict(tables={"ve": t([[1, 2], [3, 4]])}))
        self.assertEqual(d["tables"], {})

if __name__ == "__main__":
    unittest.main()
