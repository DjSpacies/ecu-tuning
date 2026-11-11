"""Unit conversions. Internal convention: kPa, K, kg/s, ms, m^3 (docs/KB-ENTRY-SCHEMA.md)."""
PSI_KPA = 6.894757
INHG_KPA = 3.386389
HP_KW = 0.7457       # mechanical horsepower
PS_KW = 0.73549875   # metric horsepower
LBHR_KGS = 0.45359237 / 3600.0

def c_to_k(c: float) -> float: return c + 273.15
def k_to_c(k: float) -> float: return k - 273.15
def f_to_c(f: float) -> float: return (f - 32.0) / 1.8
def psi_to_kpa(psi: float) -> float: return psi * PSI_KPA
def kpa_to_psi(kpa: float) -> float: return kpa / PSI_KPA
def bar_to_kpa(bar: float) -> float: return bar * 100.0
def kpa_to_bar(kpa: float) -> float: return kpa / 100.0
def inhg_to_kpa(inhg: float) -> float: return inhg * INHG_KPA
def hp_to_kw(hp: float) -> float: return hp * HP_KW
def kw_to_hp(kw: float) -> float: return kw / HP_KW
def l_to_m3(l: float) -> float: return l / 1000.0
def lbhr_to_kgs(lbhr: float) -> float: return lbhr * LBHR_KGS
def kgs_to_lbhr(kgs: float) -> float: return kgs / LBHR_KGS

def ccmin_to_kgs(cc_min: float, density_kg_m3: float) -> float:
    """Volumetric injector flow (cc/min) to mass flow (kg/s) at the given liquid density."""
    return cc_min * 1e-6 / 60.0 * density_kg_m3

def kgs_to_ccmin(kgs: float, density_kg_m3: float) -> float:
    return kgs / density_kg_m3 * 60.0 * 1e6
