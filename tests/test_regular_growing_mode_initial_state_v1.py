"""Local regular-growing-mode construction tests."""

from __future__ import annotations

import math

import numpy as np

from dfm_mkc_solver.regular_growing_mode_initial_state_v1 import (
    construct_regular_growing_mode_initial_state,
)


def _construct(amplitude: float):
    scale_factor = 0.25
    conformal_hubble = 0.1
    gravitational_constant = 1.0e-4
    phi_background = 1.0
    phi_prime_background = 2.5e-5
    theta_prime_background = 0.00625
    cosmic_hubble = conformal_hubble / scale_factor
    dark_enthalpy = (
        (phi_prime_background / scale_factor) ** 2
        + phi_background**2
        * (theta_prime_background / scale_factor) ** 2
    )
    return construct_regular_growing_mode_initial_state(
        source_log_scale_factor=math.log(0.25),
        scale_factor=scale_factor,
        conformal_hubble=conformal_hubble,
        wave_number=0.005,
        gravitational_constant=gravitational_constant,
        phi_background=phi_background,
        phi_prime_background=phi_prime_background,
        theta_prime_background=theta_prime_background,
        cosmic_hubble_n=(
            -4.0
            * math.pi
            * gravitational_constant
            * dark_enthalpy
            / cosmic_hubble
        ),
        alpha=1.0,
        beta=1.0,
        rho_star=0.0,
        m_phi_squared=1.0e-2,
        lambda_phi=0.0,
        amplitude=amplitude,
    )


def test_constructs_one_dimensional_local_mode_ray() -> None:
    certificate = _construct(1.0e-6)
    operator = np.asarray(certificate.linear_operator)
    vector = np.asarray(certificate.selected_eigenvector)
    boundary = np.asarray(certificate.boundary_matrix)

    assert certificate.variable_order == (
        "delta_phi",
        "delta_phi_prime",
        "delta_theta",
        "delta_theta_prime",
    )
    assert certificate.local_regular_growing_mode_selected
    assert certificate.local_numerical_rank_certified
    assert not certificate.exact_rank_proved
    assert certificate.certified_rank == 3
    assert certificate.nullity == 1
    assert certificate.spectral_gap > 0.0
    assert certificate.eigenpair_residual < 1.0e-10
    assert certificate.maximum_linearity_residual < 1.0e-12
    assert certificate.metric_constraints_solved
    assert certificate.initial_matching_surface_closed
    assert certificate.total_density_derivative_certified
    assert certificate.minimum_abs_constraint_denominator > 1.0e-14
    assert certificate.maximum_initial_constraint_residual < 1.0e-10
    for field in (
        "poisson_residual",
        "momentum_constraint_residual",
        "anisotropy_constraint_residual",
        "metric_closure_residual",
        "density_reconstruction_residual",
        "amplitude_equation_residual",
        "phase_equation_residual",
    ):
        assert abs(getattr(certificate, field)) < 1.0e-10
    assert certificate.density_contrast_chain_rule_residual < 1.0e-16
    assert certificate.density_contrast_finite_difference_error < (
        2.0e-8 * abs(certificate.derived_density_contrast_n)
    )
    assert certificate.density_contrast_finite_difference_converged
    assert certificate.density_contrast_finite_difference_error < (
        certificate.density_contrast_finite_difference_coarse_error
    )
    assert abs(certificate.frozen_background_shortcut_error) > 1.0e-12
    assert np.linalg.norm(
        operator @ vector - certificate.selected_eigenvalue * vector
    ) < 1.0e-9
    assert np.linalg.norm(boundary @ vector, ord=np.inf) < 1.0e-12
    assert math.isclose(
        certificate.rank_minor,
        vector[certificate.pivot_index] ** 3,
        rel_tol=1.0e-12,
        abs_tol=1.0e-12,
    )


def test_state_and_density_pair_scale_with_common_amplitude() -> None:
    positive = _construct(1.0e-6)
    doubled = _construct(2.0e-6)
    negative = _construct(-1.0e-6)

    assert np.allclose(
        doubled.initial_state,
        2.0 * np.asarray(positive.initial_state),
        rtol=2.0e-13,
        atol=1.0e-20,
    )
    assert np.allclose(
        negative.initial_state,
        -np.asarray(positive.initial_state),
        rtol=2.0e-13,
        atol=1.0e-20,
    )
    for field in ("derived_density_contrast", "derived_density_contrast_n"):
        value = getattr(positive, field)
        assert math.isclose(getattr(doubled, field), 2.0 * value, rel_tol=1e-12)
        assert math.isclose(getattr(negative, field), -value, rel_tol=1e-12)
