import sympy as sp

from dfm_mkc_solver import (
    scalar_reduced_time_gauge_direction_v1 as time_gauge,
)
from dfm_mkc_solver import scalar_spatial_gauge_quotient_v1 as quotient
from dfm_mkc_solver import total_scalar_lapse_shift_hessian_v1 as total


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


def test_exact_reduced_first_jet_prolongation():
    data = (
        time_gauge
        .reduced_time_gauge_first_jet_prolongation_data()
    )
    exact = (
        time_gauge
        .exact_reduced_time_gauge_first_jet_prolongation_certificate()
    )
    z = total._symbols()

    assert data["field_order"] == quotient.QUOTIENT_FIELDS
    assert tuple(exact) == (
        "active_psi_direction",
        "active_radial_direction",
        "active_phase_direction",
        "active_vector_reconstruction",
        "configuration_full_generator_restriction",
        "first_jet_product_rule",
        "first_jet_full_generator_restriction",
    )
    assert all(value == 0 for value in exact.values())

    for family in (
        data["configuration_restriction_residuals"],
        data["first_jet_product_rule_residuals"],
        data["full_jet_restriction_residuals"],
        data["second_time_parameter_jet_absence_residuals"],
    ):
        assert tuple(family) == quotient.QUOTIENT_FIELDS
        assert all(value == 0 for value in family.values())

    assert tuple(
        data["configuration_coefficients"][field]
        for field in time_gauge.ACTIVE_FIELDS
    ) == (z["H"], -z["php"], -z["thp"])

    assert len(data["configuration_shifts"]) == 9
    assert len(data["first_jet_shifts"]) == 9
    assert all(
        not shift.has(
            sp.Symbol("T_double_prime")
        )
        for shift in data["first_jet_shifts"].values()
    )


def test_extended_direction_certificate_is_additive_and_exact():
    certificate = time_gauge.certificate()

    assert certificate.active_field_count == 3
    assert certificate.kinetic_generator_residuals_zero is True
    assert certificate.cofactor_parallelism_residuals_zero is True
    assert certificate.cofactor_nonzero_on_pivot_domain is True
    assert certificate.generator_nonzero_domain_required is True
    assert certificate.rank_domain_required is True
    assert certificate.time_gauge_direction_identified is True
    assert certificate.identification_conditional is True

    assert certificate.reduced_field_count == 9
    assert certificate.configuration_generator_complete is True
    assert certificate.first_jet_prolongation_explicit is True
    assert certificate.first_jet_product_rule_residuals_zero is True
    assert (
        certificate.full_configuration_restriction_residuals_zero
        is True
    )
    assert certificate.full_jet_restriction_residuals_zero is True
    assert certificate.second_time_parameter_jet_absent is True
    assert certificate.time_gauge_quotient_applied is False
