"""Tests over vendor sample files, which live outside the repo; they skip when absent."""
import math, os, sys, unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
import adapter, llg, pclr   # noqa: E402

RE = Path(os.environ.get("PCLINK_RE", Path.home() / "Projects/reverse-engineering/pclink-g4plus"))
LOGS = RE / "extracted/payload/app/PCLink G4+/Logs"
DECODED = RE / "analysis/tune-format/decoded"
EXE = RE / "extracted/payload/app/PCLink G4+/PCLink.exe"
BASE = Path(__file__).resolve().parents[4] / "collateral/vendor/link/base-maps/g4plus-5.6.8"

@unittest.skipUnless(LOGS.exists(), "sample logs not present")
class Logs(unittest.TestCase):
    def test_both_files(self):
        for f, n, chans in (("Sample Drag.llg", 1530, 67), ("Sample Circuit.llg", 13394, 19)):
            r = llg.parse_llg(LOGS / f)
            self.assertEqual(len(r["channels"]), chans, f)
            self.assertEqual(len(r["channels"]["Engine Speed"]["values"]), n, f)
    def test_values_are_physically_plausible(self):
        c = llg.parse_llg(LOGS / "Sample Drag.llg")["channels"]
        self.assertTrue(5000 < max(c["Engine Speed"]["values"]) < 12000)
        self.assertTrue(90 < max(c["BAP"]["values"]) < 110)
        self.assertAlmostEqual(c["Engine Speed"]["times"][1] - c["Engine Speed"]["times"][0], 0.05, places=3)
    def test_map_equals_mgp_plus_baro_when_running(self):
        c = llg.parse_llg(LOGS / "Sample Drag.llg")["channels"]
        pts = [i for i, r in enumerate(c["Engine Speed"]["values"]) if r > 1000]
        for i in pts[::50]: self.assertAlmostEqual(c["MAP"]["values"][i], c["MGP"]["values"][i] + c["BAP"]["values"][i], delta=2.0)
    def test_normalised(self):
        log = adapter.load_log(LOGS / "Sample Drag.llg")
        for ch in ("rpm", "map_kpa", "tps", "ect", "iat", "ign_adv", "inj_pw", "lambda", "battery_v"): self.assertTrue(log.has(ch), ch)
        self.assertAlmostEqual(log.sample_rate_hz(), 20.0, delta=0.5)
        self.assertLess(max(log.channels["lambda"]), 1.2)
    def test_rejects_other_files(self):
        with self.assertRaises(ValueError): llg.parse_llg(Path(__file__))

@unittest.skipUnless(DECODED.exists(), "decoded sample tunes not present")
class Tunes(unittest.TestCase):
    def files(self): return sorted(DECODED.glob("*.pclr.xml"))
    def test_all_samples_parse(self):
        fs = self.files(); self.assertEqual(len(fs), 45)
        for f in fs:
            t = pclr.parse_xml(f.read_bytes()); self.assertTrue(t["tables"], f.name)
    def test_fuel_ignition_shapes(self):
        n = 0
        for f in self.files():
            tabs = adapter.tune_tables(pclr.parse_xml(f.read_bytes()))
            if "ve" in tabs and "ign_base" in tabs:
                n += 1
                self.assertEqual(len(tabs["ve"].values), len(tabs["ve"].y_axis)); self.assertTrue(all(len(r) == len(tabs["ve"].x_axis) for r in tabs["ve"].values))
                self.assertTrue(all(-20 < v < 90 for r in tabs["ign_base"].values for v in r), f.name)
        self.assertGreater(n, 30)
    def test_atom_sample_values(self):
        tabs = adapter.tune_tables(pclr.parse_xml((DECODED / "G4+ Atom Sample.pclr.xml").read_bytes()))
        ve = tabs["ve"]
        self.assertEqual(ve.x_axis[:4], [0, 500, 750, 1000]); self.assertEqual(ve.y_axis[0], -85); self.assertEqual(ve.y_channel, "mgp_kpa")
        self.assertEqual(ve.values[0][0], 62.3)
    def test_dead_time_row_exposed(self):
        t = adapter.load_tune(DECODED / "G4+ Atom Sample.pclr.xml")
        self.assertEqual(len(t["arrays"]["injector_dead_time_ms"]), 10)
        self.assertIn("firmware", {k.lower() for k in t["meta"]})
    def test_protections_and_second_tables(self):
        t = adapter.load_tune(DECODED / "G4+ Atom Sample.pclr.xml")
        self.assertIn("map_limit_kpa", t["protections"]); self.assertIn("rpm_limit", t["protections"])
        n = 0
        for f in self.files():
            s = adapter.load_tune(f)
            if s["protections"]["rpm_limit"] is not None: n += 1; self.assertTrue(500 < s["protections"]["rpm_limit"] < 20000, f.name)
            self.assertIn("injector_dead_time_ms", s["arrays"])
        self.assertGreater(n, 30)
    def test_refuses_entity_declarations(self):
        with self.assertRaises(ValueError): pclr.parse_xml('<!DOCTYPE x [<!ENTITY a "b">]><LinkStorage/>')

@unittest.skipUnless(EXE.exists() and BASE.exists(), "PCLink.exe or base maps not present")
class Container(unittest.TestCase):
    def test_decode_matches_reference(self):
        key = pclr.key_from_exe(EXE)
        for f in sorted(BASE.glob("*.pclr"))[:5]:
            self.assertEqual(pclr.decode_container(f.read_bytes(), key), (DECODED / (f.name + ".xml")).read_bytes(), f.name)


def _lf3(channels, holes=()):
    """Build a synthetic newer-format log: header blocks, then one 'ds3' block per channel (see ../../formats.md)."""
    import struct
    def blk(tag, body): return struct.pack("<I", 7 + len(body)) + tag + body
    def u16(s, n=200): return s.encode("utf-16le").ljust(n, b"\0")
    out = blk(b"lf3", b"\x17\x02" + bytes(206)) + blk(b"ld2", bytes(4) + u16("G4+ Test") + bytes(100)) + blk(b"lm1", bytes(4) + u16("ECU Reconnected"))
    for cid, (name, unit, pairs) in enumerate(channels, 1000):
        h = bytearray(0x285); h[0:4] = struct.pack("<I", 0x285); h[4:7] = b"ds3"; h[7:11] = struct.pack("<I", len(pairs))
        h[0xd3:0xd7] = struct.pack("<I", cid); h[0xd7:0xd7 + 200] = u16(name); h[0x19f:0x19f + 200] = u16(unit)
        h[0x26c:0x274] = struct.pack("<d", 0.025)
        out += bytes(h) + b"".join(struct.pack("<ff", t, v) for t, v in pairs)
    return out

class NewerFormat(unittest.TestCase):
    """The lf3 layout was first seen in a user's own logs (PCLink 5.6.8); these synthetic files hold no user data."""
    def write(self, chans):
        import tempfile
        d = tempfile.mkdtemp(); p = Path(d) / "t.llg"; p.write_bytes(_lf3(chans)); return p
    def test_parse_and_resample(self):
        rpm = [(-1.0 + 0.1 * i, 900.0 + 10 * i) for i in range(50)]
        p = self.write([("Engine Speed", "RPM", rpm), ("MAP", "Pressure", [(-1.0, 40.0), (2.0, 60.0), (3.9, 60.0)]),
                        ("BAP", "Pressure", [(-1.0, 100.0), (3.9, 100.0)]), ("Lambda 1", "Lambda", [(-1.0, 1.0), (3.9, 0.98)]),
                        ("MAP Limit", "", [(-1.0, 235.0), (3.9, 235.0)]), ("MAP Limit", "", [(-1.0, 0.0), (3.9, 0.0)]),
                        ("Oil Pressure", "", [(-1.0, 0.0), (3.9, 0.0)]), ("Oil Pressure", "Pressure", [(-1.0, 300.0), (1.0, 350.0), (3.9, 400.0)])])
        r = llg.parse_llg(p)
        self.assertEqual(r["format"], "lf3")
        self.assertEqual(r["channels"]["Oil Pressure"]["unit"], "Pressure")      # the recorded one keeps the plain name
        log = adapter.load_log(p)
        self.assertAlmostEqual(log.sample_rate_hz(), 40.0, delta=0.5)
        i = min(range(len(log)), key=lambda k: abs(log.time_s[k] - 2.5))
        self.assertEqual(log.channels["map_kpa"][i], 60.0)                       # held from the 2.0 s sample
        self.assertEqual(log.channels["oil_pressure_kpa"][i], 350.0)
        self.assertFalse(any(log.channels.get("limiter_active", [])))            # a setpoint is not a limiter flag
    def test_recording_hole_not_held(self):
        rpm = [(t, 1000.0) for t in (0.0, 0.5, 1.0, 4.0, 4.5, 5.0)]
        log = adapter.load_log(self.write([("Engine Speed", "RPM", rpm), ("BAP", "Pressure", [(0.0, 100.0), (5.0, 100.0)])]))
        self.assertFalse(any(1.1 < t < 3.9 for t in log.time_s))
    def test_broken_chain_rejected(self):
        import tempfile
        p = Path(tempfile.mkdtemp()) / "b.llg"; p.write_bytes(_lf3([("Engine Speed", "RPM", [(0.0, 1.0), (1.0, 2.0)])])[:-5])
        with self.assertRaises(ValueError): llg.parse_llg(p)

if __name__ == "__main__":
    unittest.main()
