import math

import pytest

from dfm_mkc_solver.dark_sector_fourier_rhs_v1 import (
    dark_sector_fourier_right_hand_side,
)


def test_zero_perturbation_is_a_closed_zero_rhs():
    certificate = dark_sector_fourier_right_hand_side(
        scale_factor=2.0,
        conformal_hubble=0.5,
        wave_number=3.0,
        gravitational_constant=1.0 / (8.0 * math.pi),
        phi_background=4.0,
        phi_prime_background=0.0,
        theta_prime_background=0.0,
        delta_phi=0.0,
        delta_phi_prime=0.0,
        delta_theta=0.0,
        delta_theta_prime=0.0,
        alpha=2.0,
        beta=3.0,
        rho_star=5.0,
        m_phi_squared=7.0,
        lambda_phi=11.0,
    )

    assert certificate.metric_potential == pytest.approx(0.0)
    assert certificate.metric_potential_prime == pytest.approx(0.0)
    assert certificate.delta_phi_double_prime == pytest.approx(0.0)
    assert certificate.delta_theta_double_prime == pytest.approx(0.0)

    assert abs(certificate.density_reconstruction_residual) < 1.0e-14
    assert abs(certificate.metric_closure_residual) < 1.0e-14
    assert certificate.instantaneous_dark_sector_rhs_closed is True
    assert certificate.visible_sector_evolution_closed is False
    assert certificate.numerical_mode_evolution_run is False


def test_nontrivial_rhs_closes_every_component_residual():
    certificate = dark_sector_fourier_right_hand_side(
        scale_factor=2.0,
        conformal_hubble=0.5,
        wave_number=6.0,
        gravitational_constant=1.0 / (8.0 * math.pi),
        phi_background=3.0,
        phi_prime_background=4.0,
        theta_prime_background=5.0,
        delta_phi=0.1,
        delta_phi_prime=0.2,
        delta_theta=0.3,
        delta_theta_prime=0.4,
        alpha=2.0,
        beta=3.0,
        rho_star=13.0,
        m_phi_squared=7.0,
        lambda_phi=11.0,
        visible_delta_energy_density=0.2,
        visible_momentum_divergence_source=0.1,
    )

    assert math.isfinite(certificate.metric_potential)
    assert math.isfinite(certificate.metric_potential_prime)
    assert math.isfinite(certificate.delta_phi_double_prime)
    assert math.isfinite(certificate.delta_theta_double_prime)

    assert abs(certificate.density_reconstruction_residual) < 1.0e-12
    assert abs(certificate.metric_closure_residual) < 1.0e-12
    assert abs(
        certificate.metric_constraints.poisson_residual
    ) < 1.0e-10
    assert abs(
        certificate.metric_constraints.momentum_residual
    ) < 1.0e-10
    assert abs(
        certificate.metric_constraints.anisotropy_residual
    ) < 1.0e-10
    assert abs(
        certificate.amplitude_equation.amplitude_equation_residual
    ) < 1.0e-10
    assert abs(
        certificate.phase_equation.normalized_equation_residual
    ) < 1.0e-10

    assert certificate.instantaneous_dark_sector_rhs_closed is True


def test_singular_metric_constraint_surface_is_rejected():
    with pytest.raises(
        ValueError,
        match="metric constraint denominator is singular",
    ):
        dark_sector_fourier_right_hand_side(
            scale_factor=1.0,
            conformal_hubble=0.0,
            wave_number=1.0,
            gravitational_constant=1.0 / (4.0 * math.pi),
            phi_background=1.0,
            phi_prime_background=1.0,
            theta_prime_background=0.0,
            delta_phi=0.0,
            delta_phi_prime=0.0,
            delta_theta=0.0,
            delta_theta_prime=0.0,
            alpha=1.0,
            beta=1.0,
            rho_star=0.0,
            m_phi_squared=0.0,
            lambda_phi=0.0,
        )
