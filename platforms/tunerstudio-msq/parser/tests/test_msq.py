"""Synthetic .msq files only; the public tune corpus lives in collateral/ and is not needed here."""
import sys, tempfile, unittest
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
import adapter, msq   # noqa: E402

def write(sig, body):
    p = Path(tempfile.mkdtemp()) / "t.msq"
    p.write_text(f'<?xml version="1.0" encoding="ISO-8859-1"?>\n<msq xmlns="http://www.msefi.com/:msq"><versionInfo fileFormat="5.0" signature="{sig}"/><page>{body}</page></msq>')
    return p

def arr(name, rows, cols, vals, units=""):
    return f'<constant name="{name}" rows="{rows}" cols="{cols}" units="{units}">{" ".join(str(v) for v in vals)}</constant>'

RUSEFI = (arr("veTable", 2, 3, [40, 50, 60, 70, 80, 90], "%") + arr("veRpmBins", 3, 1, [1000, 3000, 6000]) + arr("veLoadBins", 2, 1, [30, 100], "kPa")
          + arr("lambdaTable", 2, 3, [14.7, 14.7, 14.7, 12.5, 12.0, 11.8], "afr") + arr("lambdaRpmBins", 3, 1, [1000, 3000, 6000]) + arr("lambdaLoadBins", 2, 1, [30, 100])
          + arr("ignitionTable", 2, 3, [30, 35, 38, 20, 24, 28], "deg") + arr("ignitionRpmBins", 3, 1, [1000, 3000, 6000]) + arr("ignitionLoadBins", 2, 1, [30, 100])
          + '<constant name="stoichRatioPrimary" units=":1">14.7</constant><constant name="rpmHardLimit">7000.0</constant><constant name="fuelAlgorithm">"Speed Density"</constant>')

class MSQ(unittest.TestCase):
    def test_rusefi_tables_and_afr_conversion(self):
        t = adapter.load_tune(write("rusEFI master.2024", RUSEFI))
        self.assertEqual(t["meta"]["family"], "rusefi")
        self.assertEqual(t["tables"]["ve"].lookup(3000, 100), 80.0)       # row 0 is the lowest load bin
        self.assertAlmostEqual(t["tables"]["lambda_target"].lookup(6000, 100), 11.8 / 14.7, places=4)
        self.assertEqual(t["protections"]["rpm_limit"], 7000.0)
    def test_flat_older_layout_reshaped(self):
        body = RUSEFI.replace('name="veTable" rows="2" cols="3"', 'name="veTable"')
        self.assertEqual(adapter.load_tune(write("rusEFI 2019", body))["tables"]["ve"].values[1], [70.0, 80.0, 90.0])
    def test_unused_trailing_bins_trimmed(self):
        body = arr("veTable", 2, 3, [1, 2, 3, 4, 5, 6]) + arr("rpmBins", 3, 1, [1000, 3000, 3000]) + arr("fuelLoadBins", 2, 1, [30, 100]) + '<constant name="algorithm">"MAP"</constant>'
        self.assertEqual(adapter.load_tune(write("speeduino 202310", body))["tables"]["ve"].x_axis, [1000.0, 3000.0])
    def test_rejects_entities_and_unknown(self):
        p = Path(tempfile.mkdtemp()) / "x.msq"; p.write_text('<?xml version="1.0"?><!DOCTYPE m [<!ENTITY a "b">]><msq>&a;</msq>')
        with self.assertRaises(ValueError): msq.parse_msq(p)
        with self.assertRaises(ValueError): adapter.load_tune(write("SomethingElse", RUSEFI))

if __name__ == "__main__":
    unittest.main()
