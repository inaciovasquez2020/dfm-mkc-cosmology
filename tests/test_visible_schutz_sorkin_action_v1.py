import json
from pathlib import Path

import sympy as sp

from dfm_mkc_solver.visible_schutz_sorkin_action_v1 import (
    HELD_FIXED,
    RADIATION_EXPONENT,
    action_derived_scalar_constraint_coefficients,
    density_laws,
    equations_of_state,
    exact_certificate,
    first_metric_response,
    flrw_conservation,
    hessian_exchange_residual,
    number_density_variations,
    result_payload,
    scalar_lapse_shift_hessian,
    scalar_constraint_comparison,
    second_metric_response,
    ward_identity_residuals,
)


RESULT = (
    Path(__file__).parents[1]
    / "artifacts/cosmology/standard_visible_sector_action_binding.json"
)


def test_selected_density_laws_and_pressures_are_exact():
    laws = density_laws()
    n_b, rho_b = laws["b"]
    n_r, rho_r = laws["r"]
    m_b = next(symbol for symbol in rho_b.free_symbols if symbol.name == "m_b")
    kappa_r = next(
        symbol for symbol in rho_r.free_symbols if symbol.name == "kappa_r"
    )
    assert sp.simplify(rho_b - m_b * n_b) == 0
    assert RADIATION_EXPONENT == sp.Rational(4, 3)
    assert sp.simplify(rho_r - kappa_r * n_r ** sp.Rational(4, 3)) == 0
    eos = equations_of_state()
    assert eos["b"][1] == 0
    assert sp.simplify(eos["r"][1] - eos["r"][0] / 3) == 0


def test_held_fixed_convention_and_first_response_coefficients():
    assert HELD_FIXED == (
        "contravariant vector densities J_b^mu,J_r^mu and scalar potentials "
        "ell_b,ell_r"
    )
    expression = first_metric_response()
    symbols = {item.name: item for item in expression.free_symbols}
    q, n = symbols["q"], symbols["n"]
    rho, rho_1 = symbols["rho"], symbols["rho_1"]
    h, U_h = symbols["h"], symbols["U_h"]
    assert sp.diff(expression, h) == q * (rho - n * rho_1) / 2
    assert sp.diff(expression, U_h) == -q * n * rho_1 / 2


def test_number_density_and_complete_second_response_coefficients():
    dn_h, _, d2n = number_density_variations()
    symbols = {item.name: item for item in d2n.free_symbols}
    n = symbols["n"]
    assert sp.diff(dn_h, symbols["h"]) == n / 2
    assert sp.diff(dn_h, symbols["U_h"]) == n / 2
    assert sp.diff(d2n, symbols["hk"]) == -n / 2
    assert sp.diff(d2n, symbols["W_hk"]) == -n

    hessian = second_metric_response()
    hs = {item.name: item for item in hessian.free_symbols}
    assert sp.diff(hessian, hs["W_hk"]) == hs["n"] * hs["q"] * hs["rho_1"]
    assert sp.simplify(sp.diff(hessian, hs["rho_2"]) - (
        -hs["n"] ** 2
        * hs["q"]
        * (hs["U_h"] + hs["h"])
        * (hs["U_k"] + hs["k"])
        / 4
    )) == 0
    assert hessian_exchange_residual() == 0

    adm = scalar_lapse_shift_hessian()
    assert adm["L_NN"] != 0
    assert adm["L_Ns"] != 0
    assert adm["L_ss"] != 0
    assert adm["background_comoving"]["L_NN"] == 0
    assert adm["background_comoving"]["L_Ns"] == 0
    assert adm["background_comoving"]["L_ss"] != 0


def test_boundary_ledger_is_complete_and_not_silent():
    payload = result_payload()
    joined = " ".join(payload["boundary_terms"])
    assert "integral_boundary" in joined
    assert "temporal part vanishes" in joined
    assert "spatial part vanishes" in joined
    assert "J variation: no integration by parts" in joined
    assert "second fluid metric variations" in joined
    assert "Einstein-Hilbert boundary contacts are retained" in joined


def test_ward_identity_and_flrw_conservation_are_exact():
    payload = result_payload()
    ward = payload["euler_lagrange_equations"]
    assert ward["ell_I"] == "partial_mu J_I^mu = 0"
    assert "partial_mu ell_I = rho_I'(n_I) u_I_mu" in ward["J_I^mu"]
    assert ward_identity_residuals() == {
        "energy_projection": 0,
        "momentum_projection": 0,
    }
    flrw = flrw_conservation()
    assert flrw["b"]["dot_rho_over_H_rho"] == -3
    assert flrw["r"]["dot_rho_over_H_rho"] == -4
    assert flrw["b"]["identity_residual"] == 0
    assert flrw["r"]["identity_residual"] == 0


def test_action_derived_constraint_comparison_is_exact_not_manual():
    derived = action_derived_scalar_constraint_coefficients()
    comparison = scalar_constraint_comparison()
    G, a = sp.Symbol("G"), sp.Symbol("a", positive=True)
    assert derived == {
        "hamiltonian_delta_rho": 4 * sp.pi * G * a**2,
        "momentum_source": -4 * sp.pi * G * a**2,
        "anisotropy_enthalpy_sigma": -12 * sp.pi * G * a**2,
    }
    assert all(item["residual"] == 0 for item in comparison.values())
    payload = result_payload()
    assert (
        payload["scalar_constraint_comparison"][
            "manually_entered_visible_constraint"
        ]
        is False
    )
    certificate = exact_certificate()
    assert certificate["canonical_second_variation_ready"] is True
    assert certificate["action_binding_established"] is True


def test_result_artifact_schema_content_and_regeneration():
    payload = json.loads(RESULT.read_text(encoding="utf-8"))
    expected_fields = [
        "result_type",
        "branch_selection",
        "novelty_claimed",
        "visible_action_established",
        "equations_of_state_established",
        "first_metric_response_established",
        "second_metric_response_established",
        "boundary_contact_terms_established",
        "ward_identity_established",
        "hessian_symmetry_established",
        "canonical_second_variation_ready",
        "action_binding_established",
        "fields",
        "measure",
        "number_density_definition",
        "action_density",
        "equations_of_state",
        "variational_convention",
        "boundary_conditions",
        "boundary_terms",
        "euler_lagrange_equations",
        "stress_tensor",
        "first_metric_response",
        "second_metric_response",
        "scalar_constraint_comparison",
        "limitations",
        "provenance",
    ]
    assert list(payload) == expected_fields
    assert payload == result_payload()
    assert payload["novelty_claimed"] is False
    booleans = expected_fields[3:12]
    assert all(payload[key] is True for key in booleans)
    assert all(payload[key] for key in expected_fields[12:])
    required_limitations = {
        "photon recombination microphysics",
        "baryon-photon scattering",
        "photon polarization",
        "free-streaming neutrino anisotropic stress",
        "Boltzmann hierarchy",
        "CMB transfer function",
        "Weyl prediction vector",
        "separation from Lambda-CDM",
        "empirical evidence for DFM",
    }
    assert set(payload["limitations"]) == required_limitations
