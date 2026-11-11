import sys, unittest
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent))
import runcards as R

CELLS = [(4000, 120, "fuel"), (2000, 60, "fuel"), (3000, 90, "fuel")]

class Cards(unittest.TestCase):
    def test_low_risk_first(self):
        c = R.plan(CELLS, "road", max_rpm=6500)
        self.assertEqual([x.load for x in c if x.kind == "steady"], [60, 90, 120])
        self.assertTrue(all(x.kind == "steady" for x in c[:3])); self.assertTrue(all(x.kind == "pull" for x in c[3:]))
    def test_every_card_has_aborts_and_conditions(self):
        for x in R.plan(CELLS, "dyno", max_rpm=6000):
            self.assertIn("knock_event", x.aborts); self.assertTrue(x.conditions)
    def test_road_requires_safe_road(self):
        for x in R.plan(CELLS, "road", include_pulls=False): self.assertIn("legal, clear and safe road", x.conditions)
    def test_pull_needs_rev_limit(self):
        with self.assertRaises(ValueError): R.plan(CELLS, "road")
    def test_pulls_step_by_500_and_ramp_rate(self):
        p = [x for x in R.plan(CELLS, "dyno", max_rpm=5000) if x.kind == "pull"]
        self.assertEqual([x.rpm for x in p], [3500, 4000, 4500, 5000]); self.assertEqual(p[0].duration_s, 3.0)
    def test_pull_never_past_limit(self):
        self.assertLessEqual(max(x.rpm for x in R.plan(CELLS, "dyno", max_rpm=6250)), 6250)
    def test_bad_mode(self):
        with self.assertRaises(ValueError): R.plan(CELLS, "track-day")

class Voice(unittest.TestCase):
    def test_card_text_is_brief(self):
        for x in R.plan(CELLS, "road", max_rpm=6500): self.assertEqual(R.validate_utterance(R.card_text(x)), [], R.card_text(x))
    def test_long_utterance_rejected(self):
        self.assertIn("over 15 words", R.validate_utterance("one two three four five six seven eight nine ten eleven twelve thirteen fourteen fifteen sixteen"))
    def test_too_many_numbers_rejected(self):
        self.assertTrue(R.validate_utterance("0.85 at 3000, 0.90 at 4000, 0.88 at 5000"))
    def test_silent_during_pull_except_safety(self):
        s = R.VoiceState(moving=True, in_pull=True)
        self.assertTrue(R.may_speak("ABORT", s)); self.assertTrue(R.may_speak("SAFETY", s))
        self.assertFalse(R.may_speak("STATUS", s)); self.assertFalse(R.may_speak("INSTRUCTION", s)); self.assertFalse(R.may_speak("CHAT", s))
    def test_no_changes_while_moving(self):
        self.assertFalse(R.may_apply_change(R.VoiceState(moving=True))); self.assertTrue(R.may_apply_change(R.VoiceState(moving=False)))

if __name__ == "__main__":
    unittest.main()
