from types import MappingProxyType

import sympy as sp

from dfm_mkc_solver import (
    scalar_lapse_shift_schur_complement_v1 as schur,
)
from dfm_mkc_solver import (
    scalar_prepared_lapse_shift_determinant_v1 as prepared,
)
from dfm_mkc_solver import (
    scalar_spatial_gauge_quotient_kinetic_v1 as kinetic,
)
from dfm_mkc_solver import total_scalar_lapse_shift_hessian_v1 as total


EXPECTED_KEYS = {
    "baryon_current_density_mapping",
    "radiation_current_density_mapping",
    "prepared_phase_mapping",
    "conformal_friedmann_mapping",
    "visible_current_combination",
    "schur_factor_extraction",
    "schur_factor_on_shell_reduction",
    "schur_determinant_negative_factorization",
    "kinetic_pivot_on_shell_reduction",
    "kinetic_pivot_positive_factorization",
}


def test_exact_certificate_and_existing_sources():
    residuals = (
        prepared
        .exact_scalar_prepared_lapse_shift_determinant_certificate()
    )
    data = prepared.scalar_prepared_lapse_shift_determinant_data()

    assert set(residuals) == EXPECTED_KEYS
    assert all(value == 0 for value in residuals.values())
    assert (
        data["raw_schur_determinant"]
        == schur.scalar_lapse_shift_schur_complement()["determinant"]
    )
    assert (
        data["raw_pivot_minor"]
        == kinetic.quotient_kinetic_rank_data()["pivot_minor"]
    )


def test_action_current_and_prepared_friedmann_mappings():
    data = prepared.scalar_prepared_lapse_shift_determinant_data()
    z = total._symbols()
    symbols = data["symbols"]
    rho_b = symbols["rho_b"]
    rho_r = symbols["rho_r"]

    assert data["current_density_substitution"][z["Jb"]] == (
        z["a"]**3 * rho_b / z["mb"]
    )
    assert (
        data["current_density_substitution"][
            z["Jr"] ** sp.Rational(4, 3)
        ]
        == z["a"]**4 * rho_r / z["kr"]
    )
    assert data["friedmann_substitution"][z["H"]**2] == (
        8 * sp.pi * z["G"] * z["a"]**2 * data["rho_total"] / 3
    )


def test_strict_sign_decomposition_and_factorizations():
    data = prepared.scalar_prepared_lapse_shift_determinant_data()
    z = total._symbols()
    symbols = data["symbols"]
    mu = symbols["mu"]
    q = symbols["q"]

    positive_term = z["a"]**2 * z["k2"] * data["rho_total"]
    assert sp.expand(
        data["strict_positive_bracket"] - positive_term
    ) == sp.expand(
        data["visible_current_combination"]
        * (
            symbols["rho_b"] + symbols["rho_r"]
            + symbols["rho_lambda"]
            + data["potential_energy_density"]
        )
    )
    assert data["potential_energy_density"] == mu**2 * z["ph"]**2 / 2
    assert mu.is_positive
    assert "phi" in data["positive_variables"]

    assert data["on_shell_factor_F"] == sp.factor(
        -8 * sp.pi * z["G"] * z["a"]**6 * z["beta"]
        * z["ph"]**2 * data["strict_positive_bracket"]
    )
    assert data["on_shell_schur_determinant"] == sp.factor(
        -z["a"]**4 * z["k2"] * data["strict_positive_bracket"]
        / (6 * sp.pi * z["G"])
    )
    assert data["positive_pivot_minor_factorization"] == (
        3 * z["alpha"] * q**2 * data["positive_pivot_numerator"]
        / (
            8 * sp.pi * z["G"] * z["a"]**2 * z["beta"]
            * z["ph"]**2 * data["strict_positive_bracket"]
        )
    )


def test_immutable_theorem_has_structured_prepared_domain():
    theorem = (
        prepared.scalar_prepared_lapse_shift_determinant_theorem()
    )
    domain = theorem["nonvanishing_domain"]

    assert isinstance(theorem, MappingProxyType)
    assert isinstance(domain, MappingProxyType)
    assert theorem["schur_determinant_sign"] == "strictly negative"
    assert theorem["kinetic_pivot_sign"] == "strictly positive"
    assert theorem["finite_alpha_nonvanishing"] is True
    assert theorem["independent_determinant_domain_required"] is False
    assert domain["prepared_positive_energy"] is True
    assert domain["finite_k"] == "k2>0 and finite"
    assert domain["friedmann_identity"] == (
        "3*H^2=8*pi*G*a^2*rho_total"
    )
    assert len(domain["current_density_identities"]) == 2
    assert domain["independent_determinant_factor_condition"] is False
