"""Setup profile with evidence ledger (docs/SETUP-PROFILE.md). Session-scoped; nothing here is ever stored in the repo."""
from dataclasses import dataclass, asdict

ORIGINS = ("measured", "inferred", "user", "assumed", "unknown")
SAFETY_CRITICAL = {"tune_matches_log", "live_edits_during_log", "fuel", "knock_detection", "max_boost_kpa", "max_rpm", "wideband_valid", "fuel_system_capacity"}
QUESTIONS = {
    "fuel": "What fuel is the engine running now (pump gasoline with octane, E-blend with percentage, methanol)?",
    "knock_detection": "How is knock detected: audio equipment, ECU knock control, both, or none?",
    "max_boost_kpa": "What is the most boost this engine should see, in kPa absolute?",
    "max_rpm": "What is the engine's rev limit?",
    "wideband_valid": "Is the wideband sensor healthy, warmed up and calibrated to the ECU input?",
    "aspiration": "Is the engine naturally aspirated, turbocharged or supercharged?",
    "fuel_system_capacity": "Is the fuel system known to have enough capacity at the power being tuned for?",
    "tune_matches_log": "Is this tune file exactly what was in the ECU for the whole log, saved after the last change?",
    "live_edits_during_log": "Was anything changed in the ECU while this log was recording (live edits, trims, switches)?",
}

@dataclass
class Field:
    value: object = None
    origin: str = "unknown"
    confidence: str = "low"
    evidence: str = ""

class Profile:
    def __init__(self, user=None):
        self.fields, self.limits, self.contradictions = {}, {}, []
        for k, v in (user or {}).items():
            # A project profile carries "_" comment keys and blank fields that mean "not answered yet".
            if k.startswith("_") or v is None or v == "": continue
            if k == "limits": self.limits = {a: b for a, b in dict(v).items() if not a.startswith("_") and b is not None}
            else: self.set(k, v, "user", "high", "stated by the user")

    def set(self, name, value, origin, confidence, evidence):
        if origin not in ORIGINS: raise ValueError(f"bad origin {origin}")
        self.fields[name] = Field(value, origin, confidence, evidence)

    def infer(self, name, value, confidence, evidence):
        """Record an inference; a user statement is kept, and a disagreement is surfaced instead of overwritten."""
        cur = self.fields.get(name)
        if cur and cur.origin == "user":
            if cur.value != value: self.contradictions.append(f"{name}: user says {cur.value}; {evidence} suggests {value}")
            return
        self.set(name, value, "inferred", confidence, evidence)

    def value(self, name): return self.fields[name].value if name in self.fields else None
    def known(self, name): return name in self.fields and self.fields[name].origin in ("measured", "inferred", "user") and self.fields[name].value not in (None, "unknown", "i don't know")

    def missing(self, required):
        return [n for n in required if not self.known(n)]

    def question_block(self, required):
        """One batched block for what inference could not resolve; "I don't know" is always accepted."""
        return [dict(field=n, question=QUESTIONS.get(n, f"What is {n}?"), safety_critical=n in SAFETY_CRITICAL, allow_unknown=True) for n in self.missing(required)]

    def ledger(self): return {k: asdict(v) for k, v in sorted(self.fields.items())}

def infer_from_log(p, log):
    ch = log.channels
    if "map_kpa" in ch and "baro_kpa" in ch and ch["baro_kpa"]:
        baro = max(ch["baro_kpa"]); peak = max(ch["map_kpa"])
        p.infer("aspiration", "forced" if peak > baro + 15 else "na_or_unboosted", "medium", f"peak manifold {peak:.0f} kPa against baro {baro:.0f} kPa")
    if "knock_level" in ch or "knock_count" in ch:
        active = any(ch.get("knock_level", [])) or any(ch.get("knock_count", []))
        p.fields.setdefault("knock_channel_active", Field(bool(active), "measured", "high", "knock channel in log"))
    if "ethanol_pct" in ch and ch["ethanol_pct"]:
        e = sorted(ch["ethanol_pct"]); lo, hi = e[0], e[-1]
        # Recorded as evidence only: the fuel question stays with the user, but a mismatch is raised.
        p.fields.setdefault("ethanol_measured_pct", Field((lo, hi), "measured", "medium", f"ethanol content sensor reads {lo:.0f} to {hi:.0f} %"))
        cur = p.value("fuel")
        if cur and p.fields["fuel"].origin == "user":
            said = str(cur).lower()
            if said.startswith(("gas", "pump", "petrol")) and hi > 15:
                p.contradictions.append(f"fuel: user says {cur}; the ethanol sensor reads up to {hi:.0f} %")
            if said.startswith("meth"):
                p.contradictions.append(f"fuel: user says {cur}; an ethanol content sensor is fitted and reads {lo:.0f} to {hi:.0f} %")

def infer_from_tune(p, tune):
    s = tune.get("scalars", {})
    try:
        stoich = float(s.get("stoich_ratio") or 0)
    except ValueError:
        stoich = 0
    if stoich:
        guess = "gasoline" if stoich > 13.0 else "ethanol_blend" if stoich > 7.5 else "methanol"
        p.fields.setdefault("tune_stoich", Field(stoich, "measured", "high", "stoichiometric ratio set in the tune"))
        cur = p.value("fuel")
        if cur and p.fields["fuel"].origin == "user":
            fam = "gasoline" if str(cur).lower().startswith(("gas", "pump", "petrol")) else "methanol" if str(cur).lower().startswith("meth") else "ethanol_blend"
            # A flex or multi-fuel tune keeps the first fuel's ratio while a blend runs, so with an ethanol sensor the
            # sensor, not the ratio, is the evidence (checked in infer_from_log).
            if fam != guess and "ethanol_measured_pct" not in p.fields:
                p.contradictions.append(f"fuel: user says {cur}; tune stoichiometric ratio {stoich} suggests {guess}")
