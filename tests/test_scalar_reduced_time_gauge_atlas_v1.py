import sympy as sp

from dfm_mkc_solver import (
    scalar_reduced_time_gauge_atlas_v1 as atlas,
)
from dfm_mkc_solver import (
    total_scalar_lapse_shift_hessian_v1 as total,
)


def test_conditional_three_chart_reduced_time_gauge_atlas():
    data = atlas.reduced_time_gauge_atlas()
    certificate = atlas.certificate()
    z = total._symbols()

    assert len(data["field_order"]) == 9

    assert data["chart_pivots"] == (
        "psi",
        "delta_phi",
        "delta_theta",
    )

    assert data["time_generator_coefficients"]["psi"] == z["H"]
    assert (
        data["time_generator_coefficients"]["delta_phi"]
        == -z["php"]
    )
    assert (
        data["time_generator_coefficients"]["delta_theta"]
        == -z["thp"]
    )

    assert len(data["chart_domains"]) == 3
    assert len(data["chart_shifts"]) == 3
    assert len(data["chart_representatives"]) == 3
    assert len(data["transition_shifts"]) == 9
    assert len(data["transition_residuals"]) == 9

    assert isinstance(data["atlas_domain"], sp.Or)

    for pivot in data["chart_pivots"]:
        assert data["chart_representatives"][pivot][pivot] == 0

    assert all(
        residual == 0
        for chart_residuals in data[
            "orbit_invariance_residuals"
        ].values()
        for residual in chart_residuals.values()
    )

    assert all(
        residual == 0
        for transition_residuals in data[
            "transition_residuals"
        ].values()
        for residual in transition_residuals.values()
    )

    assert certificate.field_count == 9
    assert certificate.chart_count == 3
    assert certificate.active_generator_direction_exact is True
    assert certificate.chart_slices_exact is True
    assert certificate.chart_maps_orbit_invariant is True
    assert certificate.transition_maps_exact is True
    assert certificate.atlas_cover_exact is True
    assert certificate.global_single_chart_not_assumed is True
    assert (
        certificate.time_gauge_field_atlas_constructed
        is True
    )
    assert (
        certificate.quotient_action_atlas_constructed
        is False
    )
    assert certificate.construction_conditional is True
