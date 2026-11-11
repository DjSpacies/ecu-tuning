"""Injector flow, pulse width and duty for a four-stroke with one injection per cycle per cylinder."""
import math
from units import ccmin_to_kgs
from fuels import get_fuel

def flow_at_pressure(rated_cc_min: float, rated_dp_kpa: float, actual_dp_kpa: float) -> float:
    """Flow scales with the square root of differential pressure across the injector (incompressible orifice)."""
    if rated_dp_kpa <= 0 or actual_dp_kpa <= 0: raise ValueError("differential pressure must be positive")
    return rated_cc_min * math.sqrt(actual_dp_kpa / rated_dp_kpa)

def differential_pressure_kpa(rail_abs_kpa: float, manifold_abs_kpa: float) -> float:
    return rail_abs_kpa - manifold_abs_kpa

def fuel_mass_mg(air_mass_mg: float, lam: float, fuel: str) -> float:
    return air_mass_mg / (lam * get_fuel(fuel).stoich_afr)

def effective_pulse_ms(fuel_mass_mg_: float, flow_cc_min: float, density_kg_m3: float) -> float:
    return fuel_mass_mg_ * 1e-6 / ccmin_to_kgs(flow_cc_min, density_kg_m3) * 1000.0

def pulse_width_ms(fuel_mass_mg_: float, flow_cc_min: float, fuel: str, dead_time_ms: float) -> float:
    """Commanded pulse: time to deliver the fuel at static flow, plus the injector dead time."""
    if dead_time_ms < 0: raise ValueError("dead time cannot be negative")
    return effective_pulse_ms(fuel_mass_mg_, flow_cc_min, get_fuel(fuel).density_kg_m3) + dead_time_ms

def cycle_time_ms(rpm: float) -> float:
    if rpm <= 0: raise ValueError("rpm must be positive")
    return 120000.0 / rpm

def duty_pct(pulse_ms: float, rpm: float) -> float:
    return pulse_ms / cycle_time_ms(rpm) * 100.0

def required_flow_cc_min(power_kw: float, bsfc_g_kwh: float, cylinders: int, fuel: str, max_duty_pct: float = 85.0) -> float:
    """Static flow per injector needed at the given brake power, specific fuel use and duty ceiling."""
    if not 0 < max_duty_pct <= 100: raise ValueError("duty ceiling must be in (0, 100]")
    per_injector_kgs = power_kw * bsfc_g_kwh / 3.6e6 / cylinders / (max_duty_pct / 100.0)
    return per_injector_kgs / get_fuel(fuel).density_kg_m3 * 60.0 * 1e6

def bsfc_for_fuel(reference_bsfc_g_kwh: float, fuel: str, reference: str = "gasoline") -> float:
    """Scale specific fuel use by heating value, for the same brake efficiency."""
    return reference_bsfc_g_kwh * get_fuel(reference).lhv_mj_kg / get_fuel(fuel).lhv_mj_kg
