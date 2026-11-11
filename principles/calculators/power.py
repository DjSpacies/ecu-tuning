"""Power, torque, BMEP and efficiency for a four-stroke engine."""
import math
from fuels import get_fuel

def power_kw(torque_nm: float, rpm: float) -> float: return torque_nm * rpm * 2 * math.pi / 60.0 / 1000.0
def torque_nm(power_kw_: float, rpm: float) -> float:
    if rpm <= 0: raise ValueError("rpm must be positive")
    return power_kw_ * 1000.0 / (rpm * 2 * math.pi / 60.0)
def bmep_kpa(torque_nm_: float, displacement_m3: float) -> float: return 4 * math.pi * torque_nm_ / displacement_m3 / 1000.0
def bsfc_g_kwh(thermal_efficiency: float, fuel: str) -> float: return 3600.0 / (thermal_efficiency * get_fuel(fuel).lhv_mj_kg)

def power_from_airflow_kw(air_kgs: float, lam: float, fuel: str, thermal_efficiency: float) -> float:
    """Brake power from air mass flow. At lambda below 1 the extra fuel adds almost no heat, so the air sets the energy."""
    f = get_fuel(fuel)
    return air_kgs / (f.stoich_afr * max(lam, 1.0)) * f.lhv_mj_kg * thermal_efficiency * 1000.0

def airflow_for_power_kgs(power_kw_: float, lam: float, fuel: str, thermal_efficiency: float) -> float:
    return power_kw_ / power_from_airflow_kw(1.0, lam, fuel, thermal_efficiency)
