"""A new platform working through the unmodified core: the point of this adapter."""
import csv, importlib.util, sys, tempfile, unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[4]
sys.path[:0] = [str(ROOT / "tools" / "analysis")]
import run as R  # noqa: E402
from profile import Profile  # noqa: E402

class Csv(unittest.TestCase):
    def setUp(self):
        self.d = tempfile.TemporaryDirectory(); self.p = Path(self.d.name) / "log.csv"
        with open(self.p, "w", newline="") as f:
            w = csv.writer(f); w.writerow(["Time", "Engine Speed", "Manifold Pressure", "Coolant Temperature", "Lambda 1", "Injector Duty Cycle"])
            for i in range(200): w.writerow([i * 0.05, 3000 + i, 100, 90, 0.9 + (i % 3) * 0.001, 93.0])
    def tearDown(self): self.d.cleanup()
    def test_runs_through_the_core(self):
        ad = R.load_adapter("haltech"); log = ad.load_log(self.p)
        self.assertEqual(len(log), 200); self.assertTrue(log.has("lambda"))
        out = R.execute("injector-duty-review", log, None, Profile())
        self.assertEqual(out["findings"][0]["id"], "peak_duty"); self.assertEqual(out["findings"][0]["severity"], "fault")
    def test_health_runs(self):
        ad = R.load_adapter("haltech"); out = R.execute("log-health-check", ad.load_log(self.p), None, Profile())
        self.assertIn("missing_iat", [f["id"] for f in out["findings"]])
    def test_tune_is_refused(self):
        with self.assertRaises(ValueError): R.load_adapter("haltech").load_tune("x")
    def test_bad_csv(self):
        q = Path(self.d.name) / "bad.csv"; q.write_text("a,b\n1,2\n")
        with self.assertRaises(ValueError): R.load_adapter("haltech").load_log(q)

if __name__ == "__main__":
    unittest.main()
