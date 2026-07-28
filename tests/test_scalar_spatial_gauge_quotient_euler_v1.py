from dfm_mkc_solver import (
    scalar_spatial_gauge_quotient_euler_v1 as euler,
)


def test_exact_nine_field_quotient_euler_operator():
    data = euler.quotient_euler_data()
    certificate = euler.certificate()

    assert len(data["field_order"]) == 9
    assert len(data["canonical_momenta"]) == 9
    assert len(data["euler_rows"]) == 9
    assert len(data["qpp"]) == 9

    assert set(data["field_order"]) == set(data["euler_rows"])
    assert set(data["field_order"]) == set(data["canonical_momenta"])

    assert data["determinant"] != 0
    assert data["determinant_domain"] is not None

    assert certificate.field_count == 9
    assert certificate.euler_row_count == 9
    assert certificate.maximum_perturbation_derivative_order == 2
    assert certificate.determinant_domain_inherited is True
    assert certificate.constraint_symbols_absent is True
    assert certificate.spatial_gauge_symbols_absent is True
    assert certificate.third_perturbation_jets_absent is True
    assert certificate.euler_definition_residuals_zero is True
    assert (
        certificate.exact_nine_field_euler_operator_constructed
        is True
    )
