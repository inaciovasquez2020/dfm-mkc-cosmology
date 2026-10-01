from dfm_mkc_solver.polarization_normalization_conversion_v1 import (
    polarization_normalization_conversion,
)


def test_polarization_normalization_conversion():
    certificate = polarization_normalization_conversion(
        theta_2=2.0,
        e_repo_2=0.5,
    )

    assert certificate.e_hu_white_2 == -(6.0 ** 0.5) * 0.5
    assert certificate.pi_repo == 5.0
    assert certificate.p_hu_white == 0.5
    assert certificate.conversion_residual == 0.0
    assert certificate.normalization_equivalent is True
