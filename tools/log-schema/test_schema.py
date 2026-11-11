import sys, unittest
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent))
from schema import Log, Table

def T(): return Table("ve", [1000.0, 2000.0], [50.0, 100.0], [[10.0, 20.0], [30.0, 40.0]], "%")

class Models(unittest.TestCase):
    def test_bilinear_middle(self): self.assertAlmostEqual(T().lookup(1500, 75), 25.0)
    def test_corners_and_clamp(self):
        self.assertEqual(T().lookup(1000, 50), 10.0); self.assertEqual(T().lookup(500, 40), 10.0); self.assertEqual(T().lookup(9000, 900), 40.0)
    def test_weights_sum_to_one(self): self.assertAlmostEqual(sum(w for _, _, w in T().weights(1300, 80)), 1.0)
    def test_nearest_cell(self): self.assertEqual(T().cell(1900, 60), (0, 1))
    def test_bad_axis_shape_role(self):
        with self.assertRaises(ValueError): Table("ve", [2.0, 1.0], [1.0, 2.0], [[1, 2], [3, 4]])
        with self.assertRaises(ValueError): Table("ve", [1.0, 2.0], [1.0, 2.0], [[1, 2]])
        with self.assertRaises(ValueError): Table("nonsense", [1.0, 2.0], [1.0, 2.0], [[1, 2], [3, 4]])
    def test_log_validation(self):
        with self.assertRaises(ValueError): Log([0.0, 1.0], {"rpm": [1.0]})
        with self.assertRaises(ValueError): Log([0.0, 1.0], {"madeup": [1.0, 2.0]})
        with self.assertRaises(ValueError): Log([1.0, 1.0], {"rpm": [1.0, 2.0]})

if __name__ == "__main__":
    unittest.main()
