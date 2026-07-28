from dfm_mkc_solver import (
    scalar_constraint_variational_bridge_v1 as bridge,
)
from dfm_mkc_solver import (
    total_scalar_lapse_shift_hessian_v1 as total,
)


EXPECTED_TIME_NOETHER_ROWS = tuple(total.VARIABLES)


def test_canonical_certificate_records_full_time_noether_identity():
    certificate = (
        bridge.canonical_metric_constraint_action_binding_certificate()
    )

    print(
        "TIME_NOETHER_ROWS_ESTABLISHED := "
        f"{certificate.time_noether_rows_established}"
    )
    print(
        "TIME_NOETHER_SIX_ROW_IDENTITY_ESTABLISHED := "
        f"{certificate.time_noether_six_row_identity_established}"
    )
    print(
        "TIME_NOETHER_FULL_CANONICAL_IDENTITY_ESTABLISHED := "
        f"{certificate.time_noether_full_canonical_identity_established}"
    )
    print(
        "CANONICAL_SECOND_VARIATION_IDENTIFIED := "
        f"{certificate.canonical_second_variation_identified}"
    )
    print(
        "ACTION_BINDING_ESTABLISHED := "
        f"{certificate.action_binding_established}"
    )

    assert len(EXPECTED_TIME_NOETHER_ROWS) == 12

    assert (
        certificate.time_noether_rows_established
        == EXPECTED_TIME_NOETHER_ROWS
    )

    assert (
        certificate.time_noether_six_row_identity_established
        is True
    )

    assert (
        certificate.time_noether_full_canonical_identity_established
        is True
    )

    # The canonical traceless spatial combination now identifies
    # the zero-anisotropic-stress row. This alone does not complete
    # the canonical second-variation or full action binding.
    assert certificate.anisotropy_row_identified is True
    assert certificate.canonical_second_variation_identified is True
    assert certificate.action_binding_established is False
