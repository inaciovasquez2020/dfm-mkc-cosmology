from types import MappingProxyType

import sympy as sp

from dfm_mkc_solver.scalar_prepared_time_gauge_quotient_action_v1 import (
    exact_scalar_prepared_time_gauge_quotient_certificate,
    scalar_prepared_physical_principal_system,
    scalar_prepared_time_gauge_quotient_action,
    scalar_prepared_time_gauge_quotient_theorem,
)


EXPECTED_KEYS = {
    "h_chart_configuration_condition",
    "h_chart_jet_condition",
    "h_chart_retraction_identity",
    "h_chart_projection_idempotence",
    "h_chart_orbit_annihilation",
    "quadratic_projection_reconstruction",
    "linear_projection_reconstruction",
    "quotient_density_pullback",
    "quotient_euler_reconstruction",
    "baryon_canonical_block",
    "radiation_canonical_block",
    "auxiliary_solution_reconstruction",
    "physical_principal_determinant",
    "weyl_reconstruction",
}


def test_exact_certificate_and_action_derived_orientation():
    residuals = exact_scalar_prepared_time_gauge_quotient_certificate()
    data = scalar_prepared_time_gauge_quotient_action()
    assert isinstance(residuals, MappingProxyType)
    assert set(residuals) == EXPECTED_KEYS
    assert all(value == 0 for value in residuals.values())
    assert data["canonical_orientation_coefficients"] == {
        "baryon": -1,
        "radiation": -1,
    }
    assert data["canonical_pairings"] == (
        ("delta_J_b_0", "delta_ell_b", -1),
        ("delta_J_r_0", "delta_ell_r", -1),
    )
    expected = sp.Matrix(((0, -1), (1, 0)))
    assert data["baryon_canonical_block"] == expected
    assert data["radiation_canonical_block"] == expected


def test_physical_principal_system_and_theorem():
    principal = scalar_prepared_physical_principal_system()
    theorem = scalar_prepared_time_gauge_quotient_theorem()
    assert principal["physical_state_order"] == (
        "delta_phi",
        "delta_theta",
        "delta_J_b_0",
        "delta_ell_b",
        "delta_J_r_0",
        "delta_ell_r",
    )
    assert principal["strictly_positive"] is True
    assert principal["independent_determinant_assumption"] is False
    assert theorem["global_prepared_chart"] == "psi=0"
    assert theorem["canonical_orientation_derived_from_action"] is True
    assert theorem["physical_principal_determinant_strictly_positive"] is True


def test_structural_and_auxiliary_data_are_complete():
    data = scalar_prepared_time_gauge_quotient_action()
    assert data["spatial_quotient_field_order"] == (
        "psi",
        "delta_phi",
        "delta_theta",
        "delta_J_b_0",
        "delta_J_b_L",
        "delta_ell_b",
        "delta_J_r_0",
        "delta_J_r_L",
        "delta_ell_r",
    )
    assert data["second_order_fields"] == ("delta_phi", "delta_theta")
    assert data["auxiliary_fields"] == ("delta_J_b_L", "delta_J_r_L")
    assert all(data["structural_checks"].values())
    assert not data["unresolved_factors"]
