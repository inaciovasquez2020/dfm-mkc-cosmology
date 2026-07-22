"""Action-derived linear phase-current perturbation equation.

For

    nabla_mu(beta phi^2 nabla^mu theta) = 0

in Newtonian gauge,

    ds^2 = a^2 [
        -(1 + 2 Psi) d eta^2
        + (1 - 2 Phi) delta_ij dx^i dx^j
    ],

the homogeneous background equation is

    theta_bar''
      + 2 (Hc + phi_bar' / phi_bar) theta_bar'
      = 0.

For a Fourier mode k, define

    B
      = delta_theta'
        + 2 theta_bar' delta_phi / phi_bar
        - theta_bar' (Psi + 3 Phi).

The complete linear phase equation is

    B'
      + 2 (Hc + phi_bar' / phi_bar) B
      + k^2 delta_theta
      = 0.

This supplies the previously unresolved metric and amplitude source terms.
It remains conditional on supplied metric perturbations and amplitude-field
perturbations and does not close the complete cosmological system.
"""

from __future__ import annotations

import math
from dataclasses import dataclass


@dataclass(frozen=True)
class PhasePerturbationCertificate:
    theta_background_double_prime: float
    metric_combination: float
    metric_combination_prime: float
    normalized_current_perturbation: float
    current_perturbation: float
    delta_theta_double_prime: float
    normalized_equation_residual: float
    full_equation_residual: float
    action_derived_phase_sources_supplied: bool
    metric_sources_solved: bool
    complete_perturbation_system_closed: bool


def _require_finite(name: str, value: float) -> None:
    if not math.isfinite(value):
        raise ValueError(f"{name} must be finite")


def _dark_sector_phase_perturbation_k_squared_impl(
    *,
    scale_factor: float,
    conformal_hubble: float,
    wave_number_squared: float,
    phi_background: float,
    phi_prime_background: float,
    theta_prime_background: float,
    delta_phi: float,
    delta_phi_prime: float,
    delta_theta: float,
    delta_theta_prime: float,
    psi_metric: float,
    psi_metric_prime: float,
    phi_metric: float,
    phi_metric_prime: float,
    beta: float,
) -> PhasePerturbationCertificate:
    """Solve the linear phase-current equation for delta_theta_double_prime."""

    for name, value in (
        ("scale_factor", scale_factor),
        ("conformal_hubble", conformal_hubble),
        ("wave_number_squared", wave_number_squared),
        ("phi_background", phi_background),
        ("phi_prime_background", phi_prime_background),
        ("theta_prime_background", theta_prime_background),
        ("delta_phi", delta_phi),
        ("delta_phi_prime", delta_phi_prime),
        ("delta_theta", delta_theta),
        ("delta_theta_prime", delta_theta_prime),
        ("psi_metric", psi_metric),
        ("psi_metric_prime", psi_metric_prime),
        ("phi_metric", phi_metric),
        ("phi_metric_prime", phi_metric_prime),
        ("beta", beta),
    ):
        _require_finite(name, value)

    if scale_factor <= 0.0:
        raise ValueError("scale_factor must be positive")
    if wave_number_squared < 0.0:
        raise ValueError(
            "wave_number_squared must be nonnegative"
        )
    if phi_background == 0.0:
        raise ValueError("phi_background must be nonzero")
    if beta <= 0.0:
        raise ValueError("beta must be positive")

    logarithmic_background_rate = (
        conformal_hubble
        + phi_prime_background / phi_background
    )

    theta_background_double_prime = (
        -2.0
        * logarithmic_background_rate
        * theta_prime_background
    )

    metric_combination = (
        psi_metric + 3.0 * phi_metric
    )

    metric_combination_prime = (
        psi_metric_prime + 3.0 * phi_metric_prime
    )

    normalized_current_perturbation = (
        delta_theta_prime
        + 2.0
        * theta_prime_background
        * delta_phi
        / phi_background
        - theta_prime_background
        * metric_combination
    )

    delta_theta_double_prime = (
        -2.0
        * logarithmic_background_rate
        * normalized_current_perturbation
        - wave_number_squared * delta_theta
        - 2.0
        * theta_background_double_prime
        * delta_phi
        / phi_background
        - 2.0
        * theta_prime_background
        * delta_phi_prime
        / phi_background
        + 2.0
        * theta_prime_background
        * delta_phi
        * phi_prime_background
        / phi_background**2
        + theta_background_double_prime
        * metric_combination
        + theta_prime_background
        * metric_combination_prime
    )

    normalized_current_perturbation_prime = (
        delta_theta_double_prime
        + 2.0
        * theta_background_double_prime
        * delta_phi
        / phi_background
        + 2.0
        * theta_prime_background
        * delta_phi_prime
        / phi_background
        - 2.0
        * theta_prime_background
        * delta_phi
        * phi_prime_background
        / phi_background**2
        - theta_background_double_prime
        * metric_combination
        - theta_prime_background
        * metric_combination_prime
    )

    normalized_equation_residual = (
        normalized_current_perturbation_prime
        + 2.0
        * logarithmic_background_rate
        * normalized_current_perturbation
        + wave_number_squared * delta_theta
    )

    current_prefactor = (
        beta
        * scale_factor**2
        * phi_background**2
    )

    current_perturbation = (
        current_prefactor
        * normalized_current_perturbation
    )

    full_equation_residual = (
        current_prefactor
        * normalized_equation_residual
    )

    for name, value in (
        (
            "theta_background_double_prime",
            theta_background_double_prime,
        ),
        ("metric_combination", metric_combination),
        (
            "metric_combination_prime",
            metric_combination_prime,
        ),
        (
            "normalized_current_perturbation",
            normalized_current_perturbation,
        ),
        ("current_perturbation", current_perturbation),
        (
            "delta_theta_double_prime",
            delta_theta_double_prime,
        ),
        (
            "normalized_equation_residual",
            normalized_equation_residual,
        ),
        ("full_equation_residual", full_equation_residual),
    ):
        _require_finite(name, value)

    return PhasePerturbationCertificate(
        theta_background_double_prime=(
            theta_background_double_prime
        ),
        metric_combination=metric_combination,
        metric_combination_prime=metric_combination_prime,
        normalized_current_perturbation=(
            normalized_current_perturbation
        ),
        current_perturbation=current_perturbation,
        delta_theta_double_prime=delta_theta_double_prime,
        normalized_equation_residual=(
            normalized_equation_residual
        ),
        full_equation_residual=full_equation_residual,
        action_derived_phase_sources_supplied=True,
        metric_sources_solved=False,
        complete_perturbation_system_closed=False,
    )
def dark_sector_phase_perturbation(
    *,
    scale_factor: float,
    conformal_hubble: float,
    wave_number: float,
    phi_background: float,
    phi_prime_background: float,
    theta_prime_background: float,
    delta_phi: float,
    delta_phi_prime: float,
    delta_theta: float,
    delta_theta_prime: float,
    psi_metric: float,
    psi_metric_prime: float,
    phi_metric: float,
    phi_metric_prime: float,
    beta: float,
) -> PhasePerturbationCertificate:
    """Solve the phase equation using the legacy k surface."""

    _require_finite("wave_number", wave_number)
    if wave_number < 0.0:
        raise ValueError("wave_number must be nonnegative")

    return _dark_sector_phase_perturbation_k_squared_impl(
        scale_factor=scale_factor,
        conformal_hubble=conformal_hubble,
        wave_number_squared=wave_number**2,
        phi_background=phi_background,
        phi_prime_background=phi_prime_background,
        theta_prime_background=theta_prime_background,
        delta_phi=delta_phi,
        delta_phi_prime=delta_phi_prime,
        delta_theta=delta_theta,
        delta_theta_prime=delta_theta_prime,
        psi_metric=psi_metric,
        psi_metric_prime=psi_metric_prime,
        phi_metric=phi_metric,
        phi_metric_prime=phi_metric_prime,
        beta=beta,
    )


def dark_sector_phase_perturbation_k_squared(
    *,
    scale_factor: float,
    conformal_hubble: float,
    wave_number_squared: float,
    phi_background: float,
    phi_prime_background: float,
    theta_prime_background: float,
    delta_phi: float,
    delta_phi_prime: float,
    delta_theta: float,
    delta_theta_prime: float,
    psi_metric: float,
    psi_metric_prime: float,
    phi_metric: float,
    phi_metric_prime: float,
    beta: float,
) -> PhasePerturbationCertificate:
    """Solve the phase equation directly in x = k^2."""

    return _dark_sector_phase_perturbation_k_squared_impl(
        scale_factor=scale_factor,
        conformal_hubble=conformal_hubble,
        wave_number_squared=wave_number_squared,
        phi_background=phi_background,
        phi_prime_background=phi_prime_background,
        theta_prime_background=theta_prime_background,
        delta_phi=delta_phi,
        delta_phi_prime=delta_phi_prime,
        delta_theta=delta_theta,
        delta_theta_prime=delta_theta_prime,
        psi_metric=psi_metric,
        psi_metric_prime=psi_metric_prime,
        phi_metric=phi_metric,
        phi_metric_prime=phi_metric_prime,
        beta=beta,
    )
