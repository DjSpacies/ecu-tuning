import re, sys, unittest
from pathlib import Path
ROOT = Path(__file__).resolve().parents[2]
sys.path[:0] = [str(ROOT / "tools" / "analysis"), str(ROOT / "tools" / "glossary")]
import miniyaml
from limits import Limits

REG = set(re.findall(r"^  - id:\s*(\S+)", (ROOT / "sources/registry.yaml").read_text(), re.M))
D = miniyaml.load((ROOT / "safety/limits.yaml").read_text())

class Schema(unittest.TestCase):
    def test_every_value_is_sourced_or_unknown(self):
        for e in D["limits"]:
            if e["value"] == "unknown": self.assertIn("reason", e, e["id"])
            else:
                self.assertIn(e["source"], REG, e["id"]); self.assertTrue(e["locator"], e["id"]); self.assertIsInstance(e["value"], (int, float), e["id"]); self.assertIn(e["bound"], ("min", "max"), e["id"])
    def test_ids_unique(self):
        ids = [e["id"] for e in D["limits"]]; self.assertEqual(len(ids), len(set(ids)))
    def test_abort_limits_resolve(self):
        ids = {e["id"] for e in D["limits"]}
        for a in miniyaml.load((ROOT / "safety/aborts.yaml").read_text())["aborts"]:
            if "limit" in a: self.assertIn(a["limit"], ids)
            self.assertTrue(a["action"])
    def test_user_limits_only_tighten(self):
        with self.assertRaises(ValueError): Limits({"boost_step_kpa": 50})
        self.assertEqual(Limits({"boost_step_kpa": 10}).get("boost_step_kpa"), 10.0)
        self.assertEqual(Limits({"max_boost_kpa": 180}).get("max_boost_kpa"), 180.0)
    def test_unknown_key_refused(self):
        with self.assertRaises(KeyError): Limits({"madeup": 1})

if __name__ == "__main__":
    unittest.main()
