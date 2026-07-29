from types import MappingProxyType

from dfm_mkc_solver.scalar_prepared_auxiliary_first_jet_elimination_v1 import (
    exact_scalar_prepared_auxiliary_first_jet_certificate,
    scalar_prepared_auxiliary_first_jet_data,
    scalar_prepared_auxiliary_first_jet_theorem,
)


EXPECTED_CERTIFICATE_KEYS = {
    "imported_auxiliary_solution",
    "background_generator_derivative_equivalence",
    "h_chart_generator_derivative_equivalence",
    "auxiliary_derivative_jet_stratification",
    "implicit_auxiliary_derivative_identity",
    "structured_auxiliary_first_jet_solution",
    "differentiated_auxiliary_reconstruction",
}


def test_exact_first_jet_certificate():
    certificate = exact_scalar_prepared_auxiliary_first_jet_certificate()
    assert isinstance(certificate, MappingProxyType)
    assert set(certificate) == EXPECTED_CERTIFICATE_KEYS
    assert all(value == 0 for value in certificate.values())


def test_first_jet_shapes_and_stratification():
    data = scalar_prepared_auxiliary_first_jet_data()
    assert isinstance(data, MappingProxyType)
    assert data["auxiliary_order"] == ("delta_J_b_L", "delta_J_r_L")
    assert data["second_order_fields"] == ("delta_phi", "delta_theta")
    assert data["canonical_fields"] == (
        "delta_J_b_0",
        "delta_ell_b",
        "delta_J_r_0",
        "delta_ell_r",
    )
    assert data["auxiliary_first_jet_solution"].shape == (2, 1)
    assert data["acceleration_coefficient_matrix"].shape == (2, 2)
    assert data["canonical_prime_coefficient_matrix"].shape == (2, 4)
    assert data["affine_offset"].is_zero_matrix
    assert all(data["structural_checks"].values())
    assert not data["unresolved_factors"]


def test_theorem_has_only_checkpoint_claims_and_limitations():
    theorem = scalar_prepared_auxiliary_first_jet_theorem()
    assert isinstance(theorem, MappingProxyType)
    assert set(theorem) == {"claims", "limitations"}
    assert len(theorem["claims"]) == 6
    assert len(theorem["limitations"]) == 5
