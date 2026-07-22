"""Action-consistent DFM-MKC amplitude perturbation equation.

The supplied Newtonian-gauge Fourier equation is

    alpha [
        delta_phi''
        + 2 Hc delta_phi'
        + (k^2 + a^2 U''(phi_bar)) delta_phi
        - phi_bar' (Psi' + 3 Phi')
        + 2 a^2 Psi U'(phi_bar)
    ]
    - beta [
        delta_phi theta_bar'^2
        + 2 phi_bar theta_bar' delta_theta'
        - 2 phi_bar theta_bar'^2 Psi
    ]
    = 0.

For

    U(phi)
      = rho_star
        + (1 / 2) m_phi_squared phi^2
        + (1 / 4) lambda_phi phi^4,

this module solves the equation algebraically for delta_phi'' and
evaluates its residual.

Metric derivatives and the phase perturbation remain supplied inputs.
This does not yet close or numerically evolve the complete Fourier-mode
cosmological perturbation system.
"""

from __future__ import annotations

import math
from dataclasses import dataclass


@dataclass(frozen=True)
class AmplitudePerturbationCertificate:
    potential_slope: float
    potential_curvature: float
    metric_derivative_combination: float
    phase_coupling_bracket: float
    effective_frequency_squared: float
    delta_phi_double_prime: float
    amplitude_equation_residual: float
    action_consistent_amplitude_equation_supplied: bool
    metric_derivatives_solved: bool
    complete_perturbation_system_closed: bool


def _require_finite(name: str, value: float) -> None:
    if not math.isfinite(value):
        raise ValueError(f"{name} must be finite")


def _dark_sector_amplitude_perturbation_k_squared_impl(
    *,
    scale_factor: float,
    conformal_hubble: float,
    wave_number_squared: float,
    phi_background: float,
    phi_prime_background: float,
    theta_prime_background: float,
    delta_phi: float,
    delta_phi_prime: float,
    delta_theta_prime: float,
    psi_metric: float,
    psi_metric_prime: float,
    phi_metric_prime: float,
    alpha: float,
    beta: float,
    m_phi_squared: float,
    lambda_phi: float,
) -> AmplitudePerturbationCertificate:
    """Solve the supplied amplitude equation for delta_phi_double_prime."""

    for name, value in (
        ("scale_factor", scale_factor),
        ("conformal_hubble", conformal_hubble),
        ("wave_number_squared", wave_number_squared),
        ("phi_background", phi_background),
        ("phi_prime_background", phi_prime_background),
        ("theta_prime_background", theta_prime_background),
        ("delta_phi", delta_phi),
        ("delta_phi_prime", delta_phi_prime),
        ("delta_theta_prime", delta_theta_prime),
        ("psi_metric", psi_metric),
        ("psi_metric_prime", psi_metric_prime),
        ("phi_metric_prime", phi_metric_prime),
        ("alpha", alpha),
        ("beta", beta),
        ("m_phi_squared", m_phi_squared),
        ("lambda_phi", lambda_phi),
    ):
        _require_finite(name, value)

    if scale_factor <= 0.0:
        raise ValueError("scale_factor must be positive")
    if wave_number_squared < 0.0:
        raise ValueError(
            "wave_number_squared must be nonnegative"
        )
    if alpha <= 0.0:
        raise ValueError("alpha must be positive")
    if beta <= 0.0:
        raise ValueError("beta must be positive")
    if lambda_phi < 0.0:
        raise ValueError("lambda_phi must be nonnegative")

    potential_slope = (
        m_phi_squared * phi_background
        + lambda_phi * phi_background**3
    )

    potential_curvature = (
        m_phi_squared
        + 3.0 * lambda_phi * phi_background**2
    )

    metric_derivative_combination = (
        psi_metric_prime + 3.0 * phi_metric_prime
    )

    phase_coupling_bracket = (
        delta_phi * theta_prime_background**2
        + 2.0
        * phi_background
        * theta_prime_background
        * delta_theta_prime
        - 2.0
        * phi_background
        * theta_prime_background**2
        * psi_metric
    )

    effective_frequency_squared = (
        wave_number_squared
        + scale_factor**2 * potential_curvature
        - (beta / alpha) * theta_prime_background**2
    )

    delta_phi_double_prime = (
        -2.0 * conformal_hubble * delta_phi_prime
        - (
            wave_number_squared
            + scale_factor**2 * potential_curvature
        )
        * delta_phi
        + phi_prime_background
        * metric_derivative_combination
        - 2.0
        * scale_factor**2
        * psi_metric
        * potential_slope
        + (beta / alpha) * phase_coupling_bracket
    )

    amplitude_equation_residual = (
        alpha
        * (
            delta_phi_double_prime
            + 2.0
            * conformal_hubble
            * delta_phi_prime
            + (
                wave_number_squared
                + scale_factor**2 * potential_curvature
            )
            * delta_phi
            - phi_prime_background
            * metric_derivative_combination
            + 2.0
            * scale_factor**2
            * psi_metric
            * potential_slope
        )
        - beta * phase_coupling_bracket
    )

    for name, value in (
        ("potential_slope", potential_slope),
        ("potential_curvature", potential_curvature),
        (
            "metric_derivative_combination",
            metric_derivative_combination,
        ),
        ("phase_coupling_bracket", phase_coupling_bracket),
        (
            "effective_frequency_squared",
            effective_frequency_squared,
        ),
        (
            "delta_phi_double_prime",
            delta_phi_double_prime,
        ),
        (
            "amplitude_equation_residual",
            amplitude_equation_residual,
        ),
    ):
        _require_finite(name, value)

    return AmplitudePerturbationCertificate(
        potential_slope=potential_slope,
        potential_curvature=potential_curvature,
        metric_derivative_combination=(
            metric_derivative_combination
        ),
        phase_coupling_bracket=phase_coupling_bracket,
        effective_frequency_squared=(
            effective_frequency_squared
        ),
        delta_phi_double_prime=delta_phi_double_prime,
        amplitude_equation_residual=(
            amplitude_equation_residual
        ),
        action_consistent_amplitude_equation_supplied=True,
        metric_derivatives_solved=False,
        complete_perturbation_system_closed=False,
    )
def dark_sector_amplitude_perturbation(
    *,
    scale_factor: float,
    conformal_hubble: float,
    wave_number: float,
    phi_background: float,
    phi_prime_background: float,
    theta_prime_background: float,
    delta_phi: float,
    delta_phi_prime: float,
    delta_theta_prime: float,
    psi_metric: float,
    psi_metric_prime: float,
    phi_metric_prime: float,
    alpha: float,
    beta: float,
    m_phi_squared: float,
    lambda_phi: float,
) -> AmplitudePerturbationCertificate:
    """Solve the amplitude equation using the legacy k surface."""

    _require_finite("wave_number", wave_number)
    if wave_number < 0.0:
        raise ValueError("wave_number must be nonnegative")

    return _dark_sector_amplitude_perturbation_k_squared_impl(
        scale_factor=scale_factor,
        conformal_hubble=conformal_hubble,
        wave_number_squared=wave_number**2,
        phi_background=phi_background,
        phi_prime_background=phi_prime_background,
        theta_prime_background=theta_prime_background,
        delta_phi=delta_phi,
        delta_phi_prime=delta_phi_prime,
        delta_theta_prime=delta_theta_prime,
        psi_metric=psi_metric,
        psi_metric_prime=psi_metric_prime,
        phi_metric_prime=phi_metric_prime,
        alpha=alpha,
        beta=beta,
        m_phi_squared=m_phi_squared,
        lambda_phi=lambda_phi,
    )


def dark_sector_amplitude_perturbation_k_squared(
    *,
    scale_factor: float,
    conformal_hubble: float,
    wave_number_squared: float,
    phi_background: float,
    phi_prime_background: float,
    theta_prime_background: float,
    delta_phi: float,
    delta_phi_prime: float,
    delta_theta_prime: float,
    psi_metric: float,
    psi_metric_prime: float,
    phi_metric_prime: float,
    alpha: float,
    beta: float,
    m_phi_squared: float,
    lambda_phi: float,
) -> AmplitudePerturbationCertificate:
    """Solve the amplitude equation directly in x = k^2."""

    return _dark_sector_amplitude_perturbation_k_squared_impl(
        scale_factor=scale_factor,
        conformal_hubble=conformal_hubble,
        wave_number_squared=wave_number_squared,
        phi_background=phi_background,
        phi_prime_background=phi_prime_background,
        theta_prime_background=theta_prime_background,
        delta_phi=delta_phi,
        delta_phi_prime=delta_phi_prime,
        delta_theta_prime=delta_theta_prime,
        psi_metric=psi_metric,
        psi_metric_prime=psi_metric_prime,
        phi_metric_prime=phi_metric_prime,
        alpha=alpha,
        beta=beta,
        m_phi_squared=m_phi_squared,
        lambda_phi=lambda_phi,
    )
