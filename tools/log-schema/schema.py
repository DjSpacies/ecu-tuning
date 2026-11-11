"""Normalised Log and Table models. The core works only with these; adapters translate native files into them.

Canonical channels follow principles/glossary/terms.yaml, and table roles likewise. Units are fixed per channel.
"""
from dataclasses import dataclass, field
from bisect import bisect_right

CHANNELS = {
    "rpm": "rpm", "map_kpa": "kPa abs", "mgp_kpa": "kPa gauge", "baro_kpa": "kPa abs", "tps": "%", "lambda": "lambda", "lambda_target": "lambda",
    "ect": "C", "iat": "C", "ign_adv": "deg BTDC", "inj_pw": "ms", "inj_duty": "%", "fuel_pressure_kpa": "kPa", "battery_v": "V",
    "knock_level": "", "knock_count": "count", "boost_target_kpa": "kPa abs", "wastegate_duty": "%", "fuel_trim": "%",
    "accel_enrich": "%", "ethanol_pct": "%", "torque_nm": "Nm", "egt": "C", "oil_pressure_kpa": "kPa", "gear": "",
    "vehicle_speed": "km/h", "fuel_cut": "bool", "limiter_active": "bool", "wideband_ok": "bool",
    # The value the ECU itself read from a table at each sample. Where logged, it shows which calibration actually ran.
    "ve_out": "%", "ve_2_out": "%", "ign_out": "deg BTDC", "ign_2_out": "deg BTDC",
}
ROLES = {"ve", "ve_2", "fuel_ms", "ign_base", "ign_base_2", "lambda_target", "lambda_target_2", "boost_target", "wastegate_duty", "injector_dead_time", "injector_short_pulse",
         "cranking_fuel", "post_start_fuel", "warmup_fuel", "injection_timing", "dwell", "iat_fuel_comp", "ect_fuel_comp"}

@dataclass
class Log:
    time_s: list
    channels: dict
    meta: dict = field(default_factory=dict)

    def __post_init__(self):
        n = len(self.time_s)
        for name, values in self.channels.items():
            if name not in CHANNELS: raise ValueError(f"not a canonical channel: {name}")
            if len(values) != n: raise ValueError(f"channel {name} has {len(values)} samples, time has {n}")
        if any(b <= a for a, b in zip(self.time_s, self.time_s[1:])): raise ValueError("time must increase strictly")

    def __len__(self): return len(self.time_s)
    def has(self, name): return name in self.channels
    def sample_rate_hz(self):
        if len(self.time_s) < 2: return 0.0
        return (len(self.time_s) - 1) / (self.time_s[-1] - self.time_s[0])

def _bracket(axis, v):
    """Lower index and fraction of v on an increasing axis, clamped at both ends."""
    if v <= axis[0]: return 0, 0.0
    if v >= axis[-1]: return len(axis) - 2, 1.0
    i = bisect_right(axis, v) - 1
    return i, (v - axis[i]) / (axis[i + 1] - axis[i])

@dataclass
class Table:
    role: str
    x_axis: list
    y_axis: list
    values: list             # rows indexed by y, columns by x
    unit: str = ""
    x_channel: str = "rpm"
    y_channel: str = "map_kpa"
    native_name: str = ""

    def __post_init__(self):
        if self.role not in ROLES: raise ValueError(f"unknown table role {self.role}")
        for ax in (self.x_axis, self.y_axis):
            if len(ax) < 2 or any(b <= a for a, b in zip(ax, ax[1:])): raise ValueError("axes need at least two increasing points")
        if len(self.values) != len(self.y_axis) or any(len(r) != len(self.x_axis) for r in self.values): raise ValueError("table shape does not match axes")

    def cell(self, x, y):
        """Nearest cell (row, col) to an operating point."""
        ci, cf = _bracket(self.x_axis, x); ri, rf = _bracket(self.y_axis, y)
        return ri + (rf >= 0.5), ci + (cf >= 0.5)

    def weights(self, x, y):
        """[(row, col, weight)] bilinear contributions of the four surrounding cells; weights sum to 1."""
        ci, cf = _bracket(self.x_axis, x); ri, rf = _bracket(self.y_axis, y)
        out = [(ri, ci, (1 - rf) * (1 - cf)), (ri, ci + 1, (1 - rf) * cf), (ri + 1, ci, rf * (1 - cf)), (ri + 1, ci + 1, rf * cf)]
        return [w for w in out if w[2] > 0]

    def lookup(self, x, y):
        return sum(self.values[r][c] * w for r, c, w in self.weights(x, y))
