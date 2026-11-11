"""Compressor and intercooler relations. Pressures absolute in kPa, temperatures in K."""
import math

GAMMA_AIR = 1.4

def absolute_from_gauge(boost_kpa: float, baro_kpa: float) -> float: return boost_kpa + baro_kpa

def pressure_ratio(manifold_abs_kpa: float, baro_kpa: float, inlet_loss_kpa: float = 0.0, charge_loss_kpa: float = 0.0) -> float:
    """Compressor outlet pressure over compressor inlet pressure, with intake and charge-side losses."""
    inlet = baro_kpa - inlet_loss_kpa
    if inlet <= 0: raise ValueError("inlet pressure must be positive")
    return (manifold_abs_kpa + charge_loss_kpa) / inlet

def compressor_outlet_k(inlet_k: float, pr: float, efficiency: float, gamma: float = GAMMA_AIR) -> float:
    if not 0 < efficiency <= 1: raise ValueError("efficiency is a fraction in (0, 1]")
    if pr < 1: raise ValueError("pressure ratio below 1 is not compression")
    return inlet_k * (1 + (pr ** ((gamma - 1) / gamma) - 1) / efficiency)

def intercooler_effectiveness(hot_in_k: float, hot_out_k: float, coolant_in_k: float) -> float:
    if hot_in_k <= coolant_in_k: raise ValueError("no temperature difference to work with")
    return (hot_in_k - hot_out_k) / (hot_in_k - coolant_in_k)

def intercooler_outlet_k(hot_in_k: float, coolant_in_k: float, effectiveness: float) -> float:
    return hot_in_k - effectiveness * (hot_in_k - coolant_in_k)

def corrected_flow_kgs(mdot_kgs: float, inlet_k: float, inlet_kpa: float, ref_k: float = 298.0, ref_kpa: float = 100.0) -> float:
    """Mass flow referred to the compressor map's reference inlet state."""
    return mdot_kgs * math.sqrt(inlet_k / ref_k) / (inlet_kpa / ref_kpa)
