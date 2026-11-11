"""Four-stroke airflow from speed-density. Volumes in m^3, pressure kPa, temperature K, mass flow kg/s."""
from air import air_density

def cylinder_air_mass_mg(ve: float, map_kpa: float, charge_k: float, displacement_m3: float, cylinders: int) -> float:
    """Trapped air per cylinder per cycle (mg). `ve` is a fraction, referenced to manifold conditions."""
    return ve * air_density(map_kpa, charge_k) * displacement_m3 / cylinders * 1e6

def mass_airflow_kgs(ve: float, map_kpa: float, charge_k: float, displacement_m3: float, rpm: float) -> float:
    return ve * air_density(map_kpa, charge_k) * displacement_m3 * rpm / 120.0

def ve_from_airflow(mdot_kgs: float, map_kpa: float, charge_k: float, displacement_m3: float, rpm: float) -> float:
    """Volumetric efficiency (fraction) from a measured air mass flow."""
    if rpm <= 0: raise ValueError("rpm must be positive")
    return mdot_kgs / (air_density(map_kpa, charge_k) * displacement_m3 * rpm / 120.0)

def corrected_ve(ve: float, lambda_measured: float, lambda_target: float) -> float:
    """VE that would have produced the target lambda, assuming the fuel delivered is known correct."""
    if lambda_measured <= 0 or lambda_target <= 0: raise ValueError("lambda must be positive")
    return ve * lambda_measured / lambda_target
