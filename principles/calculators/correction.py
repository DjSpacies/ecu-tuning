"""Atmospheric correction of wide-open-throttle power, from one-dimensional compressible flow past the throttle.

This is the textbook form, not the current SAE J1349 factor: the J1349 copy on hand stops before its formula. The
reference state defaults to J1349's published reference conditions (99 kPa dry air, 25 C).
"""
import math

REF_DRY_KPA, REF_K = 99.0, 298.15

def power_correction_factor(baro_kpa: float, vapour_kpa: float, air_k: float, ref_dry_kpa: float = REF_DRY_KPA, ref_k: float = REF_K) -> float:
    dry = baro_kpa - vapour_kpa
    if dry <= 0 or air_k <= 0: raise ValueError("dry air pressure and temperature must be positive")
    return ref_dry_kpa / dry * math.sqrt(air_k / ref_k)

def ve_correction_factor(air_k: float, ref_k: float = REF_K) -> float:
    return math.sqrt(ref_k / air_k)

def corrected_power_kw(measured_kw: float, baro_kpa: float, vapour_kpa: float, air_k: float) -> float:
    return measured_kw * power_correction_factor(baro_kpa, vapour_kpa, air_k)
