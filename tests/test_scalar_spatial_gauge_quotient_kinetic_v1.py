import sympy as sp

from dfm_mkc_solver import (
    scalar_spatial_gauge_quotient_kinetic_v1 as kinetic,
)


def test_conditional_exact_quotient_kinetic_rank():
    data = kinetic.quotient_kinetic_rank_data()
    certificate = kinetic.certificate()

    assert data["kinetic_hessian"].shape == (9, 9)
    assert data["active_block"].shape == (3, 3)

    assert data["active_fields"] == (
        "psi",
        "delta_phi",
        "delta_theta",
    )
    assert data["pivot_fields"] == (
        "psi",
        "delta_phi",
    )

    assert len(data["zero_kinetic_fields"]) == 6
    assert len(data["zero_row_null_vectors"]) == 6

    assert data["pivot_minor"] != 0
    assert data["active_determinant"] == 0
    assert data["cofactor_null_vector"].shape == (3, 1)
    assert data["full_null_vector"].shape == (9, 1)

    assert all(
        residual == 0
        for residual in data["cofactor_null_residual"]
    )

    assert isinstance(data["rank_domain"], sp.And)

    assert certificate.field_count == 9
    assert certificate.active_field_count == 3
    assert certificate.exact_zero_row_count == 6
    assert certificate.kinetic_hessian_symmetric is True
    assert certificate.exact_zero_rows_verified is True
    assert certificate.active_determinant_zero is True
    assert certificate.pivot_minor_not_identically_zero is True
    assert certificate.cofactor_null_vector_exact is True
    assert (
        certificate.cofactor_null_vector_nonzero_on_domain
        is True
    )

    assert certificate.active_rank_on_domain == 2
    assert certificate.full_rank_on_domain == 2
    assert certificate.full_nullity_on_domain == 7

    assert certificate.determinant_domain_required is True
    assert certificate.pivot_domain_required is True
    assert certificate.time_gauge_quotient_applied is False
    assert certificate.classification_conditional is True
