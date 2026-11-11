"""Air properties. Humid air is treated as an ideal mixture of dry air and water vapour."""
import math

R_DRY = 287.05     # J/(kg K)
R_VAPOUR = 461.50  # J/(kg K)
CP_AIR = 1.005     # kJ/(kg K), near 300 K

def saturation_vapour_pressure_kpa(t_k: float) -> float:
    """Saturation pressure of water (Magnus form), valid about 0-60 C."""
    t = t_k - 273.15
    return 0.61094 * math.exp(17.625 * t / (t + 243.04))

def vapour_pressure_kpa(t_k: float, rh_pct: float) -> float:
    if not 0.0 <= rh_pct <= 100.0: raise ValueError("relative humidity must be 0-100 %")
    return saturation_vapour_pressure_kpa(t_k) * rh_pct / 100.0

def air_density(p_kpa: float, t_k: float, rh_pct: float = 0.0) -> float:
    """Density (kg/m^3) of air at absolute pressure p_kpa, temperature t_k, relative humidity rh_pct."""
    if p_kpa <= 0 or t_k <= 0: raise ValueError("pressure and temperature must be absolute and positive")
    pv = vapour_pressure_kpa(t_k, rh_pct) if rh_pct else 0.0
    return ((p_kpa - pv) * 1000.0 / R_DRY + pv * 1000.0 / R_VAPOUR) / t_k
