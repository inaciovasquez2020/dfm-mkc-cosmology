import math

import pytest

from dfm_mkc_solver.gauge_invariant_regular_mode_normalization_v1 import (
    certify_gauge_invariant_regular_mode_normalization,
)


def _certificate(*, sigma=0.0, amplitude=1.0):
    return certify_gauge_invariant_regular_mode_normalization(
        psi=amplitude * 0.2,
        delta_rho=amplitude * 0.9,
        rho_N=-3.0,
        initial_state=tuple(amplitude * x for x in (1.0, -2.0, 3.0, -4.0)),
        sigma=sigma,
    )


@pytest.mark.parametrize("sigma", (-7.0, -0.125, 0.25, 9.0))
def test_uniform_density_curvature_is_shift_invariant(sigma):
    certificate = _certificate(sigma=sigma)
    assert math.isclose(
        certificate.transformed_uniform_density_curvature,
        certificate.uniform_density_curvature,
        rel_tol=0.0,
        abs_tol=certificate.gauge_invariance_residual_tolerance,
    )
    assert (
        abs(certificate.gauge_invariance_residual)
        <= certificate.gauge_invariance_residual_tolerance
    )
    assert certificate.initial_uniform_density_curvature_gauge_invariant
    assert certificate.gauge_invariant_normalization_closed


@pytest.mark.parametrize("rho_n", (0.0, 0.5e-14, -1.0e-14))
def test_rejects_unseparated_background_derivative(rho_n):
    with pytest.raises(ValueError, match="rho_N"):
        certify_gauge_invariant_regular_mode_normalization(
            psi=0.2, delta_rho=0.9, rho_N=rho_n, initial_state=(1.0,)
        )


@pytest.mark.parametrize("psi", (0.3, 0.3 + 0.5e-14))
def test_rejects_zero_or_unseparated_zeta(psi):
    with pytest.raises(ValueError, match="zeta"):
        certify_gauge_invariant_regular_mode_normalization(
            psi=psi, delta_rho=0.9, rho_N=-3.0, initial_state=(1.0,)
        )


def test_normalized_state_is_common_amplitude_invariant():
    certificates = [_certificate(amplitude=x) for x in (0.25, -2.0, 7.0)]
    for certificate in certificates[1:]:
        assert certificate.normalized_initial_state == pytest.approx(
            certificates[0].normalized_initial_state, rel=2.0e-15
        )
    for certificate in certificates:
        assert not certificate.global_gauge_invariant_observable_completed
        assert not certificate.lcdm_tangent_separation_completed
        assert not certificate.observational_calibration_completed
