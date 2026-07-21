"""Conditional averaged-to-full-field initial matching surface.

For a nonzero Fourier mode, the two averaged variables (delta, delta_N) do
not uniquely determine the four full-field variables
(delta_phi, delta_phi', delta_theta, delta_theta').  This module closes that
initial-slice underdetermination by imposing two explicit conditions:

1. zero initial dark-sector pressure perturbation, delta_p = 0;
2. zero normalized phase-current perturbation, B = 0.

The momentum potential is fixed by the pressureless continuity
identification

    delta_N = -k^2 q / (Hc rho) + 3 Phi_N.

The resulting state is checked by the repository's action-derived
stress-energy source formulas.  This module does not solve metric
constraints, evolve the full field, or compute a cycle average.
"""

from __future__ import annotations

import math
from dataclasses import dataclass

from .dark_sector_stress_energy_perturbations_v1 import (
    dark_sector_stress_energy_perturbations,
)

State4 = tuple[float, float, float, float]


@dataclass(frozen=True)
class FullFieldDensityContrastCertificate:
    density_contrast: float
    background_energy_density: float
    delta_energy_density: float
    action_derived_projection_computed: bool
    full_field_evolution_solved: bool
    cycle_averaged_observable_computed: bool


@dataclass(frozen=True)
class AveragedFullFieldInitialMatchingCertificate:
    initial_state: State4
    target_density_contrast: float
    target_density_contrast_n: float
    reconstructed_density_contrast: float
    reconstructed_density_contrast_n: float
    target_momentum_potential: float
    reconstructed_momentum_potential: float
    density_contrast_residual: float
    density_contrast_n_residual: float
    pressure_residual: float
    momentum_potential_residual: float
    normalized_phase_current_residual: float
    pressureless_slice_imposed: bool
    phase_current_lock_imposed: bool
    dust_continuity_identification_imposed: bool
    matching_surface_closed: bool
    metric_constraints_solved: bool
    full_field_evolution_solved: bool
    cycle_averaged_observable_computed: bool


def _require_finite(name: str, value: float) -> None:
    if not math.isfinite(value):
        raise ValueError(f"{name} must be finite")


def _require_nonzero(name: str, value: float, tolerance: float) -> None:
    if abs(value) <= tolerance:
        raise ValueError(f"{name} must be nonzero on the matching surface")


def full_field_density_contrast(
    *,
    scale_factor: float,
    wave_number: float,
    phi_background: float,
    phi_prime_background: float,
    theta_prime_background: float,
    state: State4,
    psi_metric: float,
    alpha: float,
    beta: float,
    rho_star: float,
    m_phi_squared: float,
    lambda_phi: float,
) -> FullFieldDensityContrastCertificate:
    """Project one full-field state to delta_rho / rho."""
    source = dark_sector_stress_energy_perturbations(
        scale_factor=scale_factor,
        wave_number=wave_number,
        phi_background=phi_background,
        phi_prime_background=phi_prime_background,
        theta_prime_background=theta_prime_background,
        delta_phi=state[0],
        delta_phi_prime=state[1],
        delta_theta=state[2],
        delta_theta_prime=state[3],
        psi_metric=psi_metric,
        alpha=alpha,
        beta=beta,
        rho_star=rho_star,
        m_phi_squared=m_phi_squared,
        lambda_phi=lambda_phi,
    )
    if source.background_energy_density <= 0.0:
        raise ValueError("background energy density must be positive")
    density_contrast = (
        source.delta_energy_density / source.background_energy_density
    )
    _require_finite("density_contrast", density_contrast)
    return FullFieldDensityContrastCertificate(
        density_contrast=density_contrast,
        background_energy_density=source.background_energy_density,
        delta_energy_density=source.delta_energy_density,
        action_derived_projection_computed=True,
        full_field_evolution_solved=False,
        cycle_averaged_observable_computed=False,
    )


def match_averaged_mode_on_pressureless_phase_locked_slice(
    *,
    scale_factor: float,
    conformal_hubble: float,
    wave_number: float,
    phi_background: float,
    phi_prime_background: float,
    theta_prime_background: float,
    phi_metric: float,
    phi_metric_n: float,
    psi_metric: float,
    target_density_contrast: float,
    target_density_contrast_n: float,
    alpha: float,
    beta: float,
    rho_star: float,
    m_phi_squared: float,
    lambda_phi: float,
    nonzero_tolerance: float = 1.0e-14,
    residual_tolerance: float = 1.0e-10,
) -> AveragedFullFieldInitialMatchingCertificate:
    """Construct and verify the conditional four-component initial state."""
    for name, value in (
        ("scale_factor", scale_factor),
        ("conformal_hubble", conformal_hubble),
        ("wave_number", wave_number),
        ("phi_background", phi_background),
        ("phi_prime_background", phi_prime_background),
        ("theta_prime_background", theta_prime_background),
        ("phi_metric", phi_metric),
        ("phi_metric_n", phi_metric_n),
        ("psi_metric", psi_metric),
        ("target_density_contrast", target_density_contrast),
        ("target_density_contrast_n", target_density_contrast_n),
        ("alpha", alpha),
        ("beta", beta),
        ("rho_star", rho_star),
        ("m_phi_squared", m_phi_squared),
        ("lambda_phi", lambda_phi),
        ("nonzero_tolerance", nonzero_tolerance),
        ("residual_tolerance", residual_tolerance),
    ):
        _require_finite(name, value)
    if scale_factor <= 0.0:
        raise ValueError("scale_factor must be positive")
    if wave_number <= 0.0:
        raise ValueError("wave_number must be positive")
    if alpha <= 0.0:
        raise ValueError("alpha must be positive")
    if beta <= 0.0:
        raise ValueError("beta must be positive")
    if lambda_phi < 0.0:
        raise ValueError("lambda_phi must be nonnegative")
    if nonzero_tolerance <= 0.0:
        raise ValueError("nonzero_tolerance must be positive")
    if residual_tolerance <= 0.0:
        raise ValueError("residual_tolerance must be positive")

    _require_nonzero("conformal_hubble", conformal_hubble, nonzero_tolerance)
    _require_nonzero("phi_background", phi_background, nonzero_tolerance)
    _require_nonzero(
        "phi_prime_background",
        phi_prime_background,
        nonzero_tolerance,
    )
    _require_nonzero(
        "theta_prime_background",
        theta_prime_background,
        nonzero_tolerance,
    )

    background = dark_sector_stress_energy_perturbations(
        scale_factor=scale_factor,
        wave_number=wave_number,
        phi_background=phi_background,
        phi_prime_background=phi_prime_background,
        theta_prime_background=theta_prime_background,
        delta_phi=0.0,
        delta_phi_prime=0.0,
        delta_theta=0.0,
        delta_theta_prime=0.0,
        psi_metric=0.0,
        alpha=alpha,
        beta=beta,
        rho_star=rho_star,
        m_phi_squared=m_phi_squared,
        lambda_phi=lambda_phi,
    )
    if background.background_energy_density <= 0.0:
        raise ValueError("background energy density must be positive")
    _require_nonzero(
        "potential_slope",
        background.potential_slope,
        nonzero_tolerance,
    )

    target_delta_rho = (
        background.background_energy_density * target_density_contrast
    )
    target_kinetic_source = 0.5 * target_delta_rho

    delta_phi = target_delta_rho / (2.0 * background.potential_slope)
    delta_theta_prime = (
        -2.0 * theta_prime_background * delta_phi / phi_background
        + theta_prime_background * (psi_metric + 3.0 * phi_metric)
    )

    target_momentum_potential = (
        conformal_hubble
        * background.background_energy_density
        * (3.0 * phi_metric_n - target_density_contrast_n)
        / wave_number**2
    )
    delta_theta = (
        scale_factor**2 * target_momentum_potential
        - alpha * phi_prime_background * delta_phi
    ) / (beta * phi_background**2 * theta_prime_background)

    delta_phi_prime = (
        scale_factor**2 * target_kinetic_source
        + alpha * phi_prime_background**2 * psi_metric
        - beta
        * phi_background**2
        * theta_prime_background
        * delta_theta_prime
        - beta * phi_background * theta_prime_background**2 * delta_phi
        + beta
        * phi_background**2
        * theta_prime_background**2
        * psi_metric
    ) / (alpha * phi_prime_background)

    initial_state: State4 = (
        delta_phi,
        delta_phi_prime,
        delta_theta,
        delta_theta_prime,
    )
    source = dark_sector_stress_energy_perturbations(
        scale_factor=scale_factor,
        wave_number=wave_number,
        phi_background=phi_background,
        phi_prime_background=phi_prime_background,
        theta_prime_background=theta_prime_background,
        delta_phi=delta_phi,
        delta_phi_prime=delta_phi_prime,
        delta_theta=delta_theta,
        delta_theta_prime=delta_theta_prime,
        psi_metric=psi_metric,
        alpha=alpha,
        beta=beta,
        rho_star=rho_star,
        m_phi_squared=m_phi_squared,
        lambda_phi=lambda_phi,
    )

    reconstructed_density_contrast = (
        source.delta_energy_density / source.background_energy_density
    )
    reconstructed_density_contrast_n = (
        -wave_number**2
        * source.momentum_potential
        / (conformal_hubble * source.background_energy_density)
        + 3.0 * phi_metric_n
    )
    density_contrast_residual = (
        reconstructed_density_contrast - target_density_contrast
    )
    density_contrast_n_residual = (
        reconstructed_density_contrast_n - target_density_contrast_n
    )
    pressure_residual = source.delta_pressure
    momentum_potential_residual = (
        source.momentum_potential - target_momentum_potential
    )
    normalized_phase_current_residual = (
        delta_theta_prime
        + 2.0 * theta_prime_background * delta_phi / phi_background
        - theta_prime_background * (psi_metric + 3.0 * phi_metric)
    )
    residuals = (
        density_contrast_residual,
        density_contrast_n_residual,
        pressure_residual,
        momentum_potential_residual,
        normalized_phase_current_residual,
    )
    for index, value in enumerate(residuals):
        _require_finite(f"residual[{index}]", value)

    return AveragedFullFieldInitialMatchingCertificate(
        initial_state=initial_state,
        target_density_contrast=target_density_contrast,
        target_density_contrast_n=target_density_contrast_n,
        reconstructed_density_contrast=reconstructed_density_contrast,
        reconstructed_density_contrast_n=reconstructed_density_contrast_n,
        target_momentum_potential=target_momentum_potential,
        reconstructed_momentum_potential=source.momentum_potential,
        density_contrast_residual=density_contrast_residual,
        density_contrast_n_residual=density_contrast_n_residual,
        pressure_residual=pressure_residual,
        momentum_potential_residual=momentum_potential_residual,
        normalized_phase_current_residual=normalized_phase_current_residual,
        pressureless_slice_imposed=True,
        phase_current_lock_imposed=True,
        dust_continuity_identification_imposed=True,
        matching_surface_closed=all(
            abs(value) <= residual_tolerance for value in residuals
        ),
        metric_constraints_solved=False,
        full_field_evolution_solved=False,
        cycle_averaged_observable_computed=False,
    )
