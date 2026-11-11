"""Each expected value is worked by hand or taken from a cited table, not produced by the code under test."""
import math, sys, unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
import air, airflow, boost, correction, fuels, injector, power, units  # noqa: E402
import cli  # noqa: E402

class Units(unittest.TestCase):
    def test_pressure(self):
        self.assertAlmostEqual(units.psi_to_kpa(14.7), 101.355, places=2)
        self.assertAlmostEqual(units.kpa_to_psi(units.psi_to_kpa(22.5)), 22.5)
        self.assertAlmostEqual(units.bar_to_kpa(1.4), 140.0)
    def test_temperature(self):
        self.assertAlmostEqual(units.c_to_k(25), 298.15)
        self.assertAlmostEqual(units.f_to_c(212), 100.0)
    def test_flow(self):
        # 1000 cc/min of 745 kg/m3 fuel: 1e-3 m3/min * 745 / 60 = 0.012417 kg/s
        self.assertAlmostEqual(units.ccmin_to_kgs(1000, 745), 0.0124167, places=6)
        self.assertAlmostEqual(units.kgs_to_ccmin(units.ccmin_to_kgs(550, 789), 789), 550)
    def test_power(self):
        self.assertAlmostEqual(units.hp_to_kw(100), 74.57)

class Air(unittest.TestCase):
    def test_density_dry_standard(self):
        # an engine textbook p.65: dry air, 1 atm, 25 C = 1.184 kg/m3
        self.assertAlmostEqual(air.air_density(101.325, 298.15), 1.184, places=3)
    def test_boost_density_scales_with_pressure(self):
        self.assertAlmostEqual(air.air_density(200, 300) / air.air_density(100, 300), 2.0)
    def test_saturation_water_25c(self):
        # NIST WebBook / steam tables: 3.17 kPa at 25 C
        self.assertAlmostEqual(air.saturation_vapour_pressure_kpa(298.15), 3.17, delta=0.02)
    def test_humid_air_is_less_dense(self):
        self.assertLess(air.air_density(100, 303, 80), air.air_density(100, 303, 0))
    def test_rejects_gauge(self):
        with self.assertRaises(ValueError): air.air_density(-20, 300)
        with self.assertRaises(ValueError): air.air_density(100, 300, 120)

class Fuels(unittest.TestCase):
    def test_stoich_from_formula(self):
        # an engine textbook p.292: methanol 6.43, ethanol 8.94; isooctane 15.03 on p.95 (their air model)
        self.assertAlmostEqual(fuels.METHANOL.stoich_afr, 6.47, delta=0.05)
        self.assertAlmostEqual(fuels.ETHANOL.stoich_afr, 8.97, delta=0.05)
        self.assertAlmostEqual(fuels.stoich_afr_from_formula(8, 18), 15.1, delta=0.1)
    def test_e85_stoich_near_handbook(self):
        # By hand: v=.85: me=670.65, mg=111.75, y=.8572; .8572*8.97+.1428*14.7 = 9.79
        self.assertAlmostEqual(fuels.get_fuel("E85").stoich_afr, 9.79, delta=0.03)
    def test_blend_endpoints(self):
        self.assertAlmostEqual(fuels.get_fuel("E0").stoich_afr, 14.7)
        self.assertAlmostEqual(fuels.get_fuel("E100").stoich_afr, fuels.ETHANOL.stoich_afr)
    def test_lambda_afr(self):
        self.assertAlmostEqual(fuels.lambda_to_afr(0.8, "gasoline"), 11.76)
        self.assertAlmostEqual(fuels.afr_to_lambda(fuels.lambda_to_afr(0.85, "E30"), "E30"), 0.85)
    def test_gasoline_scale_display(self):
        self.assertAlmostEqual(fuels.gasoline_scale_afr_to_lambda(11.76), 0.8)
    def test_methanol_needs_about_2_3x_fuel(self):
        self.assertAlmostEqual(fuels.fuel_mass_ratio("methanol"), 2.27, delta=0.03)
    def test_mixture_energy_near_equal_across_fuels(self):
        # F&K p.292 stoichiometric LHV per kg air: methanol 3.09, ethanol 3.00, gasoline 2.96
        self.assertAlmostEqual(fuels.mixture_energy_mj_per_kg_air("methanol"), 3.08, delta=0.05)
        self.assertAlmostEqual(fuels.mixture_energy_mj_per_kg_air("ethanol"), 2.99, delta=0.05)
        self.assertAlmostEqual(fuels.mixture_energy_mj_per_kg_air("gasoline"), 43.0 / 14.7)
    def test_rich_mixture_adds_no_energy(self):
        self.assertEqual(fuels.mixture_energy_mj_per_kg_air("gasoline", 0.8), fuels.mixture_energy_mj_per_kg_air("gasoline", 1.0))
    def test_charge_cooling_bound(self):
        # gasoline: 310/14.7/1.005 = 20.98 K; methanol: 1215/6.47/1.005 = 186.9 K
        self.assertAlmostEqual(fuels.ideal_charge_cooling_k("gasoline"), 20.98, delta=0.05)
        self.assertAlmostEqual(fuels.ideal_charge_cooling_k("methanol"), 186.9, delta=1.5)
    def test_unknown_fuel_refused(self):
        with self.assertRaises(ValueError): fuels.get_fuel("diesel")
        with self.assertRaises(ValueError): fuels.ethanol_blend(120)

class Airflow(unittest.TestCase):
    def test_mass_flow_by_hand(self):
        # 2.0 L at 6000 rpm, VE 1, 100 kPa, 300 K: rho = 100000/(287.05*300) = 1.16122; 0.002*50 rev-pairs/s = 0.1 m3/s
        self.assertAlmostEqual(airflow.mass_airflow_kgs(1.0, 100, 300, 0.002, 6000), 0.116122, places=5)
    def test_ve_round_trip(self):
        m = airflow.mass_airflow_kgs(0.87, 145, 320, 0.0025, 4500)
        self.assertAlmostEqual(airflow.ve_from_airflow(m, 145, 320, 0.0025, 4500), 0.87)
    def test_cylinder_mass_by_hand(self):
        # 0.5 L per cylinder at 1.16122 kg/m3 = 0.58061 g = 580.61 mg, VE 1
        self.assertAlmostEqual(airflow.cylinder_air_mass_mg(1.0, 100, 300, 0.002, 4), 580.61, delta=0.05)
    def test_ve_correction_direction(self):
        # Measured 0.92 against target 0.85 is lean: more air than modelled, so VE must rise
        self.assertAlmostEqual(airflow.corrected_ve(0.80, 0.92, 0.85), 0.8659, places=3)

class Injector(unittest.TestCase):
    def test_square_root_pressure(self):
        # Doubling differential pressure gives sqrt(2) times the flow
        self.assertAlmostEqual(injector.flow_at_pressure(1000, 300, 600), 1414.21, places=1)
    def test_fuel_mass(self):
        self.assertAlmostEqual(injector.fuel_mass_mg(580.61, 1.0, "gasoline"), 39.497, places=2)
    def test_pulse_width_by_hand(self):
        # 40 mg of 745 kg/m3 at 1000 cc/min (12.4167 g/s): 3.2215 ms + 0.8 dead = 4.0215 ms
        self.assertAlmostEqual(injector.pulse_width_ms(40, 1000, "gasoline", 0.8), 4.0215, places=3)
    def test_duty(self):
        # 6000 rpm cycle = 20 ms; 15 ms pulse = 75 %
        self.assertAlmostEqual(injector.duty_pct(15, 6000), 75.0)
    def test_sizing_by_hand(self):
        # 300 kW * 300 g/kWh = 90 kg/h = 0.025 kg/s; /4/0.85 = 7.353 g/s; /745 kg/m3 *60e6 = 592.2 cc/min
        self.assertAlmostEqual(injector.required_flow_cc_min(300, 300, 4, "gasoline"), 592.2, delta=0.5)
    def test_bsfc_scaling(self):
        self.assertAlmostEqual(injector.bsfc_for_fuel(300, "ethanol"), 300 * 43.0 / 26.8)
    def test_rejects_negative_dead_time(self):
        with self.assertRaises(ValueError): injector.pulse_width_ms(10, 500, "gasoline", -1)

class Power(unittest.TestCase):
    def test_torque_power(self):
        # 400 Nm at 6000 rpm = 400 * 628.32 / 1000 = 251.3 kW
        self.assertAlmostEqual(power.power_kw(400, 6000), 251.33, places=1)
        self.assertAlmostEqual(power.torque_nm(power.power_kw(350, 5200), 5200), 350)
    def test_bmep(self):
        # 200 Nm from 2 L: 4*pi*200/0.002 = 1256.6 kPa
        self.assertAlmostEqual(power.bmep_kpa(200, 0.002), 1256.64, places=1)
    def test_bsfc(self):
        self.assertAlmostEqual(power.bsfc_g_kwh(0.30, "gasoline"), 3600 / (0.3 * 43.0))
    def test_power_from_air_is_capped_at_stoich(self):
        self.assertEqual(power.power_from_airflow_kw(0.2, 0.85, "gasoline", 0.3), power.power_from_airflow_kw(0.2, 1.0, "gasoline", 0.3))
    def test_airflow_round_trip(self):
        self.assertAlmostEqual(power.power_from_airflow_kw(power.airflow_for_power_kgs(300, 0.9, "E85", 0.32), 0.9, "E85", 0.32), 300)

class Boost(unittest.TestCase):
    def test_pressure_ratio(self):
        self.assertAlmostEqual(boost.pressure_ratio(200, 100), 2.0)
        self.assertAlmostEqual(boost.pressure_ratio(200, 100, 5, 10), 210 / 95)
    def test_outlet_temp_by_hand(self):
        # PR 2, 300 K inlet, eff 0.7: 2^(0.2857)=1.21901; 300*(1+.21901/.7) = 393.86 K
        self.assertAlmostEqual(boost.compressor_outlet_k(300, 2.0, 0.7), 393.86, delta=0.05)
    def test_intercooler(self):
        self.assertAlmostEqual(boost.intercooler_effectiveness(400, 330, 300), 0.7)
        self.assertAlmostEqual(boost.intercooler_outlet_k(400, 300, 0.7), 330.0)
    def test_corrected_flow(self):
        self.assertAlmostEqual(boost.corrected_flow_kgs(0.3, 298, 100), 0.3)
        self.assertAlmostEqual(boost.corrected_flow_kgs(0.3, 298, 50), 0.6)
    def test_rejects_bad_efficiency(self):
        with self.assertRaises(ValueError): boost.compressor_outlet_k(300, 2, 1.2)

class Correction(unittest.TestCase):
    def test_reference_state_is_unity(self):
        self.assertAlmostEqual(correction.power_correction_factor(99, 0, 298.15), 1.0)
    def test_hot_low_pressure_corrects_up(self):
        # 95 kPa dry, 35 C: 99/95 * sqrt(308.15/298.15) = 1.04211 * 1.01663 = 1.05944
        self.assertAlmostEqual(correction.power_correction_factor(96, 1, 308.15), 1.0594, places=3)
    def test_ve_correction_direction(self):
        self.assertGreater(correction.ve_correction_factor(320), 0.0)
        self.assertLess(correction.ve_correction_factor(320), 1.0)

class Cli(unittest.TestCase):
    def test_exports_everything(self):
        names = cli.exported()
        for n in ("air_density", "lambda_to_afr", "pulse_width_ms", "compressor_outlet_k", "power_correction_factor"): self.assertIn(n, names)

if __name__ == "__main__":
    unittest.main()
