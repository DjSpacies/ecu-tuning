#!/usr/bin/env python3
"""Run any calculator from the command line; prints JSON.

  python3 -I principles/calculators/cli.py list
  python3 -I principles/calculators/cli.py air_density --p_kpa 101.325 --t_k 288.15
  python3 -I principles/calculators/cli.py lambda_to_afr --lam 0.8 --fuel E85
"""
import argparse, inspect, json, sys
from dataclasses import asdict, is_dataclass
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import air, airflow, boost, correction, fuels, injector, power, units  # noqa: E402

MODULES = [units, air, fuels, airflow, injector, power, boost, correction]

def exported():
    out = {}
    for m in MODULES:
        for n, f in vars(m).items():
            if inspect.isfunction(f) and f.__module__ == m.__name__ and not n.startswith("_"): out[n] = f
    return out

def main(argv=None):
    fns = exported()
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = ap.add_subparsers(dest="cmd", required=True); sub.add_parser("list")
    for n, f in fns.items():
        p = sub.add_parser(n, help=(f.__doc__ or "").split("\n")[0])
        for pn, prm in inspect.signature(f).parameters.items():
            ty = int if prm.annotation is int else str if prm.annotation is str else float
            p.add_argument("--" + pn, type=ty, required=prm.default is inspect.Parameter.empty, default=None if prm.default is inspect.Parameter.empty else prm.default)
    a = vars(ap.parse_args(argv)); cmd = a.pop("cmd")
    if cmd == "list":
        for n, f in sorted(fns.items()): print(f"{n}{inspect.signature(f)}")
        return
    r = fns[cmd](**a)
    print(json.dumps({"result": asdict(r) if is_dataclass(r) else r}))

if __name__ == "__main__":
    main()
