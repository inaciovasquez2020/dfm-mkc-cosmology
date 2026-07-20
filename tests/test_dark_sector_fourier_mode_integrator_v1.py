import math
import sys
from pathlib import Path

import pytest


sys.path.insert(
    0,
    str(Path(__file__).resolve().parents[1] / "src"),
)

from dfm_mkc_solver.dark_sector_fourier_mode_integrator_v1 import (
    dark_sector_fourier_mode_step_doubling,
    integrate_dark_sector_fourier_mode,
)


def test_zero_mode_state_remains_exactly_zero():
    certificate = integrate_dark_sector_fourier_mode(
        conformal_time_start=0.0,
        conformal_time_end=1.0,
        steps=20,
        initial_state=(0.0, 0.0, 0.0, 0.0),
        scale_factor=1.0,
        conformal_hubble=0.1,
        wave_number=2.0,
        gravitational_constant=1.0e-8,
        phi_background=1.0,
        phi_prime_background=0.0,
        theta_prime_background=0.0,
        alpha=1.0,
        beta=1.0,
        rho_star=0.0,
        m_phi_squared=1.0,
        lambda_phi=0.0,
    )

    assert certificate.final_state == (
        0.0,
        0.0,
        0.0,
        0.0,
    )
    assert len(certificate.times) == 21
    assert len(certificate.states) == 21
    assert certificate.max_component_residual == 0.0

    assert (
        certificate
        .all_instantaneous_rhs_certificates_closed
        is True
    )
    assert certificate.fixed_background_integration_completed is True
    assert certificate.cosmological_background_evolved is False
    assert certificate.visible_sector_evolved is False
    assert certificate.observable_computed is False


def test_bounded_mode_has_step_doubling_convergence():
    certificate = dark_sector_fourier_mode_step_doubling(
        base_steps=10,
        conformal_time_start=0.0,
        conformal_time_end=1.0,
        initial_state=(0.01, 0.0, 0.02, 0.0),
        scale_factor=1.0,
        conformal_hubble=0.1,
        wave_number=2.0,
        gravitational_constant=1.0e-8,
        phi_background=1.0,
        phi_prime_background=0.0,
        theta_prime_background=0.0,
        alpha=1.0,
        beta=1.0,
        rho_star=0.0,
        m_phi_squared=1.0,
        lambda_phi=0.0,
    )

    assert certificate.coarse_steps == 10
    assert certificate.medium_steps == 20
    assert certificate.fine_steps == 40

    assert math.isfinite(
        certificate.coarse_medium_difference
    )
    assert math.isfinite(
        certificate.medium_fine_difference
    )
    assert certificate.coarse_medium_difference > 0.0
    assert certificate.medium_fine_difference > 0.0

    assert (
        certificate.medium_fine_difference
        < certificate.coarse_medium_difference
    )
    assert certificate.observed_order is not None
    assert certificate.observed_order > 3.0
    assert certificate.convergence_improved is True
    assert certificate.bounded_mode_convergence_certified is True

    for integration in (
        certificate.coarse,
        certificate.medium,
        certificate.fine,
    ):
        assert all(
            math.isfinite(value)
            for value in integration.final_state
        )
        assert integration.max_component_residual < 1.0e-10
        assert (
            integration
            .all_instantaneous_rhs_certificates_closed
            is True
        )


def test_invalid_integration_domain_is_rejected():
    with pytest.raises(
        ValueError,
        match=(
            "conformal_time_end must exceed "
            "conformal_time_start"
        ),
    ):
        integrate_dark_sector_fourier_mode(
            conformal_time_start=1.0,
            conformal_time_end=1.0,
            steps=10,
            initial_state=(0.0, 0.0, 0.0, 0.0),
            scale_factor=1.0,
            conformal_hubble=0.0,
            wave_number=1.0,
            gravitational_constant=1.0,
            phi_background=1.0,
            phi_prime_background=0.0,
            theta_prime_background=0.0,
            alpha=1.0,
            beta=1.0,
            rho_star=0.0,
            m_phi_squared=0.0,
            lambda_phi=0.0,
        )
