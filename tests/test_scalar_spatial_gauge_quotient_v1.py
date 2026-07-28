from dfm_mkc_solver import scalar_spatial_gauge_quotient_v1 as quotient


def test_exact_spatial_scalar_gauge_quotient():
    data = quotient.scalar_spatial_gauge_quotient()
    certificate = quotient.certificate()

    assert data["spatial_gauge_field"] == "E"
    assert len(data["quotient_fields"]) == 9
    assert len(data["invariant_currents"]) == 4

    assert certificate.schur_reduced_field_count == 10
    assert certificate.quotient_field_count == 9
    assert certificate.exact_E_zero_slice is True
    assert certificate.invariant_current_combinations_exact is True
    assert certificate.quotient_density_gauge_field_free is True
    assert certificate.quotient_density_constraint_free is True
    assert certificate.quotient_basis_complete is True
    assert certificate.spatial_gauge_quotient_applied is True
