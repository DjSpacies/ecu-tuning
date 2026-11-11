"""Fuel properties, blends and lambda/AFR. See principles/fuels/ for sources and derivations.

Stoichiometric AFR of a pure compound is computed from its formula. Gasoline is a varying mixture: its entry is a
nominal value and `lhv_range` shows the spread in the references, so callers must treat it as approximate.
"""
from dataclasses import dataclass
import re
from air import CP_AIR

O2_AIR_MOLE_RATIO = 4.773   # mol air per mol O2
M_AIR, M_C, M_H, M_O = 28.96, 12.011, 1.008, 15.999

def stoich_afr_from_formula(c: float, h: float, o: float = 0.0) -> float:
    """Mass air-fuel ratio for complete combustion of CcHhOo."""
    o2 = c + h / 4.0 - o / 2.0
    return o2 * O2_AIR_MOLE_RATIO * M_AIR / (c * M_C + h * M_H + o * M_O)

@dataclass(frozen=True)
class Fuel:
    name: str
    stoich_afr: float
    lhv_mj_kg: float
    density_kg_m3: float
    hfg_kj_kg: float
    lhv_range: tuple = ()

GASOLINE = Fuel("gasoline", 14.7, 43.0, 745.0, 310.0, (40.1, 44.5))
ETHANOL = Fuel("ethanol", stoich_afr_from_formula(2, 6, 1), 26.8, 789.0, 850.0)
METHANOL = Fuel("methanol", stoich_afr_from_formula(1, 4, 1), 19.9, 792.0, 1215.0)

def ethanol_blend(vol_pct: float) -> Fuel:
    """Gasoline/ethanol blend by volume percent ethanol. AFR, LHV and hfg combine by mass; density by volume."""
    if not 0.0 <= vol_pct <= 100.0: raise ValueError("ethanol content must be 0-100 %")
    v = vol_pct / 100.0
    m_e, m_g = v * ETHANOL.density_kg_m3, (1 - v) * GASOLINE.density_kg_m3
    y = m_e / (m_e + m_g)
    mix = lambda a, b: y * a + (1 - y) * b
    return Fuel(f"E{vol_pct:g}", mix(ETHANOL.stoich_afr, GASOLINE.stoich_afr), mix(ETHANOL.lhv_mj_kg, GASOLINE.lhv_mj_kg),
                m_e + m_g, mix(ETHANOL.hfg_kj_kg, GASOLINE.hfg_kj_kg))

def get_fuel(name: str) -> Fuel:
    n = name.strip().lower()
    if n in ("gasoline", "petrol", "pump"): return GASOLINE
    if n in ("ethanol", "e100"): return ETHANOL
    if n in ("methanol", "m100"): return METHANOL
    m = re.fullmatch(r"e(\d{1,3}(?:\.\d+)?)", n)
    if m: return ethanol_blend(float(m.group(1)))
    raise ValueError(f"unknown fuel '{name}' (gasoline, ethanol, methanol, or E<n>)")

def lambda_to_afr(lam: float, fuel: str) -> float: return lam * get_fuel(fuel).stoich_afr
def afr_to_lambda(afr: float, fuel: str) -> float: return afr / get_fuel(fuel).stoich_afr

def gasoline_scale_afr_to_lambda(displayed_afr: float) -> float:
    """Lambda from a wideband display scaled for gasoline: the sensor measures lambda whatever the display says."""
    return displayed_afr / GASOLINE.stoich_afr

def fuel_mass_ratio(fuel: str, reference: str = "gasoline") -> float:
    """Fuel mass needed relative to the reference fuel for the same air and lambda."""
    return get_fuel(reference).stoich_afr / get_fuel(fuel).stoich_afr

def mixture_energy_mj_per_kg_air(fuel: str, lam: float = 1.0) -> float:
    """Heat released per kg of air at lambda <= 1 is capped by the air, so lambda < 1 is clamped to 1."""
    f = get_fuel(fuel)
    return f.lhv_mj_kg / (f.stoich_afr * max(lam, 1.0))

def ideal_charge_cooling_k(fuel: str, lam: float = 1.0) -> float:
    """Upper bound on charge temperature drop: all the fuel evaporates using heat from the air alone."""
    f = get_fuel(fuel)
    return f.hfg_kj_kg / (lam * f.stoich_afr) / CP_AIR
