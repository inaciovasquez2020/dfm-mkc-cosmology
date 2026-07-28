import sympy as sp

from dfm_mkc_solver import (
    scalar_reduced_time_gauge_direction_v1 as time_gauge,
)


def test_conditional_reduced_time_gauge_direction_identification():
    data = time_gauge.reduced_time_gauge_direction_data()
    certificate = time_gauge.certificate()

    assert data["active_fields"] == (
        "psi",
        "delta_phi",
        "delta_theta",
    )

    assert data["active_block"].shape == (3, 3)
    assert data["reduced_time_generator"].shape == (3, 1)
    assert data["full_reduced_time_generator"].shape == (9, 1)
    assert data["cofactor_vector"].shape == (3, 1)

    assert all(
        residual == 0
        for residual in data[
            "kinetic_generator_residuals"
        ]
    )

    assert all(
        residual == 0
        for residual in data[
            "cofactor_parallelism_residuals"
        ]
    )

    assert (
        data["cofactor_vector"][2]
        - data["pivot_minor"]
    ) == 0

    assert isinstance(data["rank_domain"], sp.And)
    assert isinstance(
        data["generator_nonzero_domain"],
        sp.Or,
    )
    assert isinstance(
        data["identification_domain"],
        sp.And,
    )

    assert certificate.active_field_count == 3
    assert (
        certificate.kinetic_generator_residuals_zero
        is True
    )
    assert (
        certificate.cofactor_parallelism_residuals_zero
        is True
    )
    assert (
        certificate.cofactor_nonzero_on_pivot_domain
        is True
    )
    assert (
        certificate.generator_nonzero_domain_required
        is True
    )
    assert certificate.rank_domain_required is True
    assert (
        certificate.time_gauge_direction_identified
        is True
    )
    assert certificate.identification_conditional is True
    assert certificate.time_gauge_quotient_applied is False
