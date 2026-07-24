import json
from pathlib import Path

import sympy as sp

from dfm_mkc_solver.visible_sector_action_v1 import (
    BOUNDARY_TERMS,
    HELD_FIXED_METRIC_VARIABLES,
    LIMITATIONS,
    RADIATION_EXPONENT,
    equations_of_state,
    first_metric_response,
    flrw_conservation_residuals,
    kappa_r,
    m_b,
    n,
    result_payload,
    rho_b,
    rho_r,
    scalar_constraint_comparison,
    second_metric_response,
    symbolic_certificate,
    ward_identity_components,
    ward_identity_residual,
)


RESULT = (
    Path(__file__).parents[1]
    / "artifacts"
    / "dfm_mkc"
    / "standard_visible_sector_action_binding_v1.json"
)


def test_selected_density_laws_and_pressure_identities_are_exact():
    assert rho_b == m_b * n
    assert RADIATION_EXPONENT == sp.Rational(4, 3)
    assert rho_r == kappa_r * n ** sp.Rational(4, 3)
    eos = equations_of_state()
    assert eos["p_b"] == 0
    assert sp.simplify(eos["p_r"] - rho_r / 3) == 0


def test_held_fixed_convention_and_first_response_coefficients():
    assert HELD_FIXED_METRIC_VARIABLES == (
        "contravariant vector densities J_b^mu and J_r^mu; "
        "scalar potentials ell_b and ell_r"
    )
    D, rho, rho1, nn, G, U = sp.symbols("D rho rho1 nn G U")
    response = first_metric_response(
        measure=D,
        density=rho,
        density_prime=rho1,
        number_density=nn,
        h_trace=G,
        h_velocity=U,
    )
    assert sp.simplify(
        sp.Poly(response, G, U).coeff_monomial(G)
        - D * (rho - nn * rho1) / 2
    ) == 0
    assert sp.Poly(response, G, U).coeff_monomial(U) == -D * nn * rho1 / 2


def test_complete_second_response_coefficients_and_exchange_symmetry():
    D, rho, r1, r2, nn = sp.symbols("D rho r1 r2 nn")
    Gh, Gk, Uh, Uk, HK, UHK = sp.symbols("Gh Gk Uh Uk HK UHK")
    kwargs = dict(
        measure=D,
        density=rho,
        density_prime=r1,
        density_second=r2,
        number_density=nn,
        h_trace=Gh,
        k_trace=Gk,
        h_velocity=Uh,
        k_velocity=Uk,
        h_metric_k=HK,
        velocity_h_metric_k_velocity=UHK,
    )
    response = second_metric_response(**kwargs)
    polynomial = sp.Poly(response, Gh, Gk, Uh, Uk, HK, UHK)
    assert sp.simplify(
        polynomial.coeff_monomial(HK) - D * (-rho + nn * r1) / 2
    ) == 0
    assert polynomial.coeff_monomial(UHK) == D * nn * r1
    assert sp.simplify(
        polynomial.coeff_monomial(Gh * Gk)
        - D * (-rho + nn * r1 - nn**2 * r2) / 4
    ) == 0
    assert sp.simplify(
        polynomial.coeff_monomial(Uh * Uk)
        - D * (nn * r1 - nn**2 * r2) / 4
    ) == 0
    exchanged = second_metric_response(
        **{
            **kwargs,
            "h_trace": Gk,
            "k_trace": Gh,
            "h_velocity": Uk,
            "k_velocity": Uh,
        }
    )
    assert sp.simplify(response - exchanged) == 0


def test_hessian_matches_independent_direct_matrix_differentiation():
    e, f, j = sp.symbols("e f j", positive=True)
    h00, h01, h11, k00, k01, k11 = sp.symbols(
        "h00 h01 h11 k00 k01 k11"
    )
    h = sp.Matrix([[h00, h01], [h01, h11]])
    k = sp.Matrix([[k00, k01], [k01, k11]])
    inverse_metric = sp.diag(-1, 1) + e * h + f * k
    metric = inverse_metric.inv()
    measure = sp.sqrt(-1 / inverse_metric.det())
    current = sp.Matrix([j, 0])
    direct_n = sp.sqrt(-(current.T * metric * current)[0]) / measure
    direct_lagrangian = -measure * direct_n**2
    direct_hessian = sp.simplify(
        sp.diff(direct_lagrangian, e, f).subs({e: 0, f: 0})
    )

    invariant_hessian = second_metric_response(
        measure=1,
        density=j**2,
        density_prime=2 * j,
        density_second=2,
        number_density=j,
        h_trace=-h00 + h11,
        k_trace=-k00 + k11,
        h_velocity=h00,
        k_velocity=k00,
        h_metric_k=h00 * k00 - 2 * h01 * k01 + h11 * k11,
        velocity_h_metric_k_velocity=-h00 * k00 + h01 * k01,
    )
    assert sp.simplify(direct_hessian - invariant_hessian) == 0


def test_all_boundary_terms_are_explicit_and_none_are_silent():
    assert len(BOUNDARY_TERMS) == 7
    text = " ".join(BOUNDARY_TERMS)
    for required in (
        "initial and final",
        "spatial",
        "compact spatial support",
        "no integration by parts",
        "no derivative boundary term",
        "Einstein-Hilbert",
        "diffeomorphism",
    ):
        assert required in text


def test_ward_identity_and_flrw_conservation_are_exact():
    assert ward_identity_components() == {
        "u_projection": 0,
        "orthogonal_projection": 0,
    }
    assert ward_identity_residual() == 0
    assert flrw_conservation_residuals() == {
        "dot_rho_b_plus_3Hrho_b": 0,
        "dot_rho_r_plus_4Hrho_r": 0,
    }


def test_scalar_constraint_is_action_derived_and_matches_carrier():
    comparison = scalar_constraint_comparison()
    assert comparison["origin"].startswith("mixed scalar lapse-density")
    assert comparison["exact"] is True
    assert comparison["residual"] == (0, 0, 0)
    assert comparison["derived_coefficients"] == comparison["carrier_coefficients"]
    cert = symbolic_certificate()
    assert cert.canonical_second_variation_ready is True
    assert cert.action_binding_established is True


def test_result_artifact_contract_novelty_and_limitations():
    payload = json.loads(RESULT.read_text())
    assert payload == result_payload()
    assert list(payload) == [
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
    assert payload["novelty_claimed"] is False
    boolean_keys = [
        key for key, value in payload.items() if isinstance(value, bool)
    ]
    assert all(payload[key] is True for key in boolean_keys if key != "novelty_claimed")
    for key in list(payload)[12:]:
        assert payload[key]
    assert payload["limitations"] == list(LIMITATIONS)
