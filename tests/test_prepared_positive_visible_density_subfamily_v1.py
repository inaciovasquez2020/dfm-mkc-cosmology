from types import MappingProxyType

import sympy as sp

from dfm_mkc_solver import (
    prepared_alpha_family_existence_v1 as generic,
)
from dfm_mkc_solver import (
    prepared_positive_visible_density_subfamily_v1 as positive,
)
from dfm_mkc_solver import (
    scalar_prepared_lapse_shift_determinant_v1 as determinant,
)


EXPECTED_KEYS = {
    "baryon_scale_factor_solution",
    "radiation_scale_factor_solution",
    "baryon_conservation_equation",
    "radiation_conservation_equation",
    "baryon_initial_value",
    "radiation_initial_value",
    "baryon_current_reconstruction",
    "radiation_current_reconstruction",
    "baryon_density_reconstruction",
    "radiation_density_reconstruction",
}


def test_exact_positive_subfamily_certificate():
    residuals = (
        positive
        .exact_prepared_positive_visible_density_subfamily_certificate()
    )
    assert set(residuals) == EXPECTED_KEYS
    assert all(value == 0 for value in residuals.values())


def test_strict_claims_and_complete_interval_are_structured():
    data = positive.prepared_positive_visible_density_subfamily_data()
    claims = data["strict_claims"]

    assert data["rho_b0"].is_positive
    assert data["rho_r0"].is_positive
    assert data["m_b"].is_positive
    assert data["kappa_r"].is_positive
    assert data["a_i"] == sp.Rational(100, 333)
    assert float(data["a_i"]) == generic.A_INITIAL
    assert all(claims.values())
    assert set(claims) == {
        "rho_b0_positive",
        "rho_r0_positive",
        "scale_factor_positive",
        "rho_b_positive",
        "rho_r_positive",
        "Jbar_b_0_positive",
        "Jbar_r_0_positive",
        "complete_prepared_interval_covered",
    }


def test_current_and_density_positivity_follow_from_branch_symbols():
    data = positive.prepared_positive_visible_density_subfamily_data()

    assert data["rho_b_a"].is_positive
    assert data["rho_r_a"].is_positive
    assert data["Jbar_b_0"].is_positive
    assert data["Jbar_r_0"].is_positive
    assert data["positive_variables"] == (
        "rho_b0", "rho_r0", "a", "m_b", "kappa_r",
    )


def test_determinant_mapping_compatibility():
    data = positive.prepared_positive_visible_density_subfamily_data()
    det_data = determinant.scalar_prepared_lapse_shift_determinant_data()

    assert (
        data["determinant_density_mappings"]
        is det_data["current_density_substitution"]
    )


def test_theorem_is_immutable_and_excludes_boundary_models():
    theorem = (
        positive.prepared_positive_visible_density_subfamily_theorem()
    )

    assert isinstance(theorem, MappingProxyType)
    assert theorem["subfamily_assumptions"] == (
        "rho_b0>0", "rho_r0>0",
    )
    assert theorem["independent_determinant_nonvanishing_assumed"] is False
    assert any(
        "generic prepared theorem still permits zero" in item
        for item in theorem["limitations"]
    )
    assert any(
        "Zero-species boundary models require separate" in item
        for item in theorem["limitations"]
    )
