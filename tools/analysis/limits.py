"""Load safety/limits.yaml and apply user-declared limits. Stdlib only.

A limit whose value is `unknown` stays None unless the user declared one. User limits can only tighten: a user value
looser than a sourced default is rejected, so a typo cannot widen the envelope.
"""
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "tools" / "glossary"))
import miniyaml  # noqa: E402

UNKNOWN = "unknown"

class Limits:
    def __init__(self, user=None, path=None):
        data = miniyaml.load((Path(path) if path else ROOT / "safety" / "limits.yaml").read_text(encoding="utf8"))
        self.entries = {e["id"]: e for e in data["limits"]}
        self.user = {}
        for k, v in (user or {}).items():
            if k not in self.entries: raise KeyError(f"unknown limit {k}")
            default = self.number(k)
            bound = self.entries[k].get("bound")
            if default is not None and ((bound == "max" and v > default) or (bound == "min" and v < default)):
                raise ValueError(f"user limit {k}={v} is less conservative than the default {default}")
            self.user[k] = float(v)

    def number(self, key):
        v = self.entries[key]["value"]
        return None if v == UNKNOWN else float(v)

    def get(self, key):
        """The limit in force, or None when nothing supports a number."""
        if key not in self.entries: raise KeyError(key)
        return self.user[key] if key in self.user else self.number(key)

    def is_known(self, key): return self.get(key) is not None
    def unknown(self): return sorted(k for k in self.entries if not self.is_known(k))
