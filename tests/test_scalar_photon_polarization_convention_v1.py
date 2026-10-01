from dfm_mkc_solver.scalar_photon_polarization_convention_v1 import (
    scalar_photon_polarization_convention,
)


def test_scalar_photon_polarization_convention_certificate():
    certificate = scalar_photon_polarization_convention(
        theta_2=2.0,
        e_2=0.5,
        e_1=0.0,
        b_multipoles=(0.0, 0.0, 0.0),
    )

    assert certificate.pi == 5.0
    assert certificate.e1_boundary_residual == 0.0
    assert certificate.scalar_b_residual == 0.0
    assert certificate.polarization_convention_closed is True
