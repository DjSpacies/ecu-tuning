"""D2 simulated engine (docs/VALIDATION.md). A small model with hidden truth, used to find mistakes in workflows.

Hidden from the agent: the true VE surface, MBT and the knock limit. The agent sees only logs and measured torque.
Keep this simple and do not change it to make a workflow pass: a simple simulator is easy to game.
"""
import math, random, sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path[:0] = [str(ROOT / "tools" / "log-schema"), str(ROOT / "tools" / "analysis")]
from schema import Log, Table  # noqa: E402

RPM = [1000, 2000, 3000, 4000, 5000, 6000, 7000]
LOAD = [40, 60, 80, 100, 120, 140, 160]

class Engine:
    FAULTS = {"none", "wideband_offset", "wideband_stuck", "noise", "lag", "transients", "boost_failure", "wideband_dropout", "cold_engine"}

    def __init__(self, seed=0, fault="none"):
        if fault not in self.FAULTS: raise ValueError(fault)
        self.rng = random.Random(seed); self.fault = fault; r = self.rng
        self.peak_rpm = r.uniform(4000, 5500); self.width = r.uniform(3500, 5500); self.base_ve = r.uniform(78, 96)
        self.load_slope = r.uniform(0.02, 0.07)
        self.true_mbt_base = r.uniform(24, 34)
        self.knock_margin = r.uniform(-4.0, 3.0)   # below zero means knock-limited before MBT
        self.wideband_offset = r.choice([-0.06, 0.06]) if fault == "wideband_offset" else 0.0
        self.delay_s = 0.25 if fault == "lag" else 0.1
        self.noise = 0.05 if fault == "noise" else 0.004

    # ---- hidden truth ----
    def true_ve(self, rpm, load):
        return self.base_ve * math.exp(-((rpm - self.peak_rpm) / self.width) ** 2) * (1 + self.load_slope * (load - 100) / 100.0)

    def mbt(self, rpm, load): return self.true_mbt_base + (rpm - 4000) / 1000.0 - (load - 100) * 0.09
    def knock_limit(self, rpm, load): return self.mbt(rpm, load) + self.knock_margin

    def true_lambda(self, tuned_ve, rpm, load, target):
        """Air scales with true VE and fuel with the tuned number, so lambda moves by their ratio."""
        return target * self.true_ve(rpm, load) / tuned_ve

    def torque(self, rpm, load, advance):
        """Peak at MBT, flat near it, with a measurement noise the same size as a real dyno's repeatability."""
        tau = self.mbt(rpm, load) - advance
        return (load * 3.0 + self.true_ve(rpm, load)) * (1 - 0.0009 * tau * tau) * (1 + self.rng.gauss(0, 0.0015))

    def knocks(self, rpm, load, advance): return advance > self.knock_limit(rpm, load)
    def damaging_knock(self, rpm, load, advance): return advance > self.knock_limit(rpm, load) + 3.0

    # ---- what the agent can see ----
    def hold(self, tuned_ve_table, target_table, points, seconds=3.0, rate=20.0, advance=None):
        """Steady holds at each (rpm, load), concatenated into one log."""
        r = self.rng
        t, ch = 0.0, {k: [] for k in ("rpm", "map_kpa", "tps", "ect", "iat", "lambda", "battery_v", "accel_enrich")}
        times = []
        sensed = None
        for rpm, load in points:
            tuned = tuned_ve_table.lookup(rpm, load); target = target_table.lookup(rpm, load)
            true = self.true_lambda(tuned, rpm, load, target)
            n = int(seconds * rate)
            sensed = true if sensed is None else sensed
            for i in range(n):
                wobble = 1 + r.gauss(0, self.noise)
                alpha = 1.0 / rate / max(self.delay_s, 1.0 / rate)
                sensed += (true - sensed) * alpha
                reading = 0.95 if self.fault == "wideband_stuck" else sensed * wobble + self.wideband_offset
                if self.fault == "wideband_dropout" and i % 4 == 0: reading = 0.0
                enrich = 5.0 if self.fault == "transients" and i < n * 0.5 else 0.0
                for k, v in (("rpm", rpm + r.gauss(0, 3)), ("map_kpa", load + r.gauss(0, 0.2)), ("tps", 50.0), ("ect", 40.0 if self.fault == "cold_engine" else 90.0), ("iat", 30.0), ("lambda", reading), ("battery_v", 14.1), ("accel_enrich", enrich)): ch[k].append(v)
                times.append(t); t += 1.0 / rate
            t += 1.0                # settle time between points, which is not logged
        return Log(times, ch, dict(adapter="sim"))

def starting_tables(engine, error_pct=12.0):
    """A tune whose fuel table is wrong in a plausible, cell-independent way."""
    r = random.Random(engine.rng.random())
    ve = [[engine.true_ve(x, y) * (1 + r.uniform(-error_pct, error_pct) / 100.0) for x in RPM] for y in LOAD]
    target = [[1.0 if y <= 100 else 0.85 for _ in RPM] for y in LOAD]
    return Table("ve", list(RPM), list(LOAD), ve, "%", native_name="sim_ve"), Table("lambda_target", list(RPM), list(LOAD), target, "lambda", native_name="sim_target")
