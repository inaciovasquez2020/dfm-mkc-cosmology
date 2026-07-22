"""Action-derived linear DFM-MKC stress-energy perturbations.

The conventions are

    signature = (-,+,+,+),

    ds^2 = a(eta)^2 [
        -(1 + 2 Psi) d eta^2
        + (1 - 2 Phi) delta_ij dx^i dx^j
    ],

and

    L_DFM_MKC
      = -(alpha / 2) (nabla phi)^2
        -(beta / 2) phi^2 (nabla theta)^2
        - U(phi),

    U(phi)
      = rho_star
        + (1 / 2) m_phi_squared phi^2
        + (1 / 4) lambda_phi phi^4.

For homogeneous background fields, linear spatial-gradient energies vanish.
The resulting conformal-time source perturbations are

    delta rho
      = alpha / a^2 [
          phi_bar' delta_phi'
          - phi_bar'^2 Psi
        ]
        + beta / a^2 [
          phi_bar^2 theta_bar' delta_theta'
          + phi_bar theta_bar'^2 delta_phi
          - phi_bar^2 theta_bar'^2 Psi
        ]
        + U'(phi_bar) delta_phi,

    delta p
      = the same kinetic perturbation
        - U'(phi_bar) delta_phi.

Define the scalar momentum potential q by

    delta T^0_i = -partial_i q.

Then

    q = [
        alpha phi_bar' delta_phi
        + beta phi_bar^2 theta_bar' delta_theta
    ] / a^2,

and the Fourier momentum-divergence source appearing in the supplied
constraint is k^2 q.

Minimally coupled scalar fields on a homogeneous background have zero
linear scalar anisotropic stress.

This module does not evolve perturbations, solve initial conditions, close
the visible-sector hierarchy, or establish observational viability.
"""

from __future__ import annotations

import math
from dataclasses import dataclass


@dataclass(frozen=True)
class DarkSectorStressEnergyPerturbationCertificate:
    potential: float
    potential_slope: float
    background_energy_density: float
    background_pressure: float
    background_enthalpy: float
    kinetic_source_perturbation: float
    potential_source_perturbation: float
    delta_energy_density: float
    delta_pressure: float
    momentum_potential: float
    momentum_divergence_source: float
    scalar_anisotropic_stress: float
    energy_pressure_difference_residual: float
    enthalpy_identity_residual: float
    action_derived_sources_supplied: bool
    perturbation_evolution_solved: bool
    observational_prediction_computed: bool


def _require_finite(name: str, value: float) -> None:
    if not math.isfinite(value):
        raise ValueError(f"{name} must be finite")


def _dark_sector_stress_energy_perturbations_k_squared_impl(
    *,
    scale_factor: float,
    wave_number_squared: float,
    phi_background: float,
    phi_prime_background: float,
    theta_prime_background: float,
    delta_phi: float,
    delta_phi_prime: float,
    delta_theta: float,
    delta_theta_prime: float,
    psi_metric: float,
    alpha: float,
    beta: float,
    rho_star: float,
    m_phi_squared: float,
    lambda_phi: float,
) -> DarkSectorStressEnergyPerturbationCertificate:
    """Evaluate the linear action-derived dark-sector source formulas."""

    for name, value in (
        ("scale_factor", scale_factor),
        ("wave_number_squared", wave_number_squared),
        ("phi_background", phi_background),
        ("phi_prime_background", phi_prime_background),
        ("theta_prime_background", theta_prime_background),
        ("delta_phi", delta_phi),
        ("delta_phi_prime", delta_phi_prime),
        ("delta_theta", delta_theta),
        ("delta_theta_prime", delta_theta_prime),
        ("psi_metric", psi_metric),
        ("alpha", alpha),
        ("beta", beta),
        ("rho_star", rho_star),
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

    inverse_scale_factor_squared = 1.0 / scale_factor**2

    potential = (
        rho_star
        + 0.5 * m_phi_squared * phi_background**2
        + 0.25 * lambda_phi * phi_background**4
    )

    potential_slope = (
        m_phi_squared * phi_background
        + lambda_phi * phi_background**3
    )

    amplitude_kinetic_density = (
        0.5
        * alpha
        * inverse_scale_factor_squared
        * phi_prime_background**2
    )

    phase_kinetic_density = (
        0.5
        * beta
        * inverse_scale_factor_squared
        * phi_background**2
        * theta_prime_background**2
    )

    background_energy_density = (
        amplitude_kinetic_density
        + phase_kinetic_density
        + potential
    )

    background_pressure = (
        amplitude_kinetic_density
        + phase_kinetic_density
        - potential
    )

    background_enthalpy = (
        alpha
        * inverse_scale_factor_squared
        * phi_prime_background**2
        + beta
        * inverse_scale_factor_squared
        * phi_background**2
        * theta_prime_background**2
    )

    amplitude_kinetic_perturbation = (
        alpha
        * inverse_scale_factor_squared
        * (
            phi_prime_background * delta_phi_prime
            - phi_prime_background**2 * psi_metric
        )
    )

    phase_kinetic_perturbation = (
        beta
        * inverse_scale_factor_squared
        * (
            phi_background**2
            * theta_prime_background
            * delta_theta_prime
            + phi_background
            * theta_prime_background**2
            * delta_phi
            - phi_background**2
            * theta_prime_background**2
            * psi_metric
        )
    )

    kinetic_source_perturbation = (
        amplitude_kinetic_perturbation
        + phase_kinetic_perturbation
    )

    potential_source_perturbation = (
        potential_slope * delta_phi
    )

    delta_energy_density = (
        kinetic_source_perturbation
        + potential_source_perturbation
    )

    delta_pressure = (
        kinetic_source_perturbation
        - potential_source_perturbation
    )

    momentum_potential = (
        inverse_scale_factor_squared
        * (
            alpha
            * phi_prime_background
            * delta_phi
            + beta
            * phi_background**2
            * theta_prime_background
            * delta_theta
        )
    )

    momentum_divergence_source = (
        wave_number_squared * momentum_potential
    )

    scalar_anisotropic_stress = 0.0

    energy_pressure_difference_residual = (
        delta_energy_density
        - delta_pressure
        - 2.0 * potential_source_perturbation
    )

    enthalpy_identity_residual = (
        background_energy_density
        + background_pressure
        - background_enthalpy
    )

    for name, value in (
        ("potential", potential),
        ("potential_slope", potential_slope),
        (
            "background_energy_density",
            background_energy_density,
        ),
        ("background_pressure", background_pressure),
        ("background_enthalpy", background_enthalpy),
        (
            "kinetic_source_perturbation",
            kinetic_source_perturbation,
        ),
        (
            "potential_source_perturbation",
            potential_source_perturbation,
        ),
        ("delta_energy_density", delta_energy_density),
        ("delta_pressure", delta_pressure),
        ("momentum_potential", momentum_potential),
        (
            "momentum_divergence_source",
            momentum_divergence_source,
        ),
        (
            "energy_pressure_difference_residual",
            energy_pressure_difference_residual,
        ),
        (
            "enthalpy_identity_residual",
            enthalpy_identity_residual,
        ),
    ):
        _require_finite(name, value)

    return DarkSectorStressEnergyPerturbationCertificate(
        potential=potential,
        potential_slope=potential_slope,
        background_energy_density=background_energy_density,
        background_pressure=background_pressure,
        background_enthalpy=background_enthalpy,
        kinetic_source_perturbation=kinetic_source_perturbation,
        potential_source_perturbation=potential_source_perturbation,
        delta_energy_density=delta_energy_density,
        delta_pressure=delta_pressure,
        momentum_potential=momentum_potential,
        momentum_divergence_source=(
            momentum_divergence_source
        ),
        scalar_anisotropic_stress=scalar_anisotropic_stress,
        energy_pressure_difference_residual=(
            energy_pressure_difference_residual
        ),
        enthalpy_identity_residual=(
            enthalpy_identity_residual
        ),
        action_derived_sources_supplied=True,
        perturbation_evolution_solved=False,
        observational_prediction_computed=False,
    )
def dark_sector_stress_energy_perturbations(
    *,
    scale_factor: float,
    wave_number: float,
    phi_background: float,
    phi_prime_background: float,
    theta_prime_background: float,
    delta_phi: float,
    delta_phi_prime: float,
    delta_theta: float,
    delta_theta_prime: float,
    psi_metric: float,
    alpha: float,
    beta: float,
    rho_star: float,
    m_phi_squared: float,
    lambda_phi: float,
) -> DarkSectorStressEnergyPerturbationCertificate:
    """Evaluate the source formulas using the legacy k surface."""

    _require_finite("wave_number", wave_number)
    if wave_number < 0.0:
        raise ValueError("wave_number must be nonnegative")

    return _dark_sector_stress_energy_perturbations_k_squared_impl(
        scale_factor=scale_factor,
        wave_number_squared=wave_number**2,
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


def dark_sector_stress_energy_perturbations_k_squared(
    *,
    scale_factor: float,
    wave_number_squared: float,
    phi_background: float,
    phi_prime_background: float,
    theta_prime_background: float,
    delta_phi: float,
    delta_phi_prime: float,
    delta_theta: float,
    delta_theta_prime: float,
    psi_metric: float,
    alpha: float,
    beta: float,
    rho_star: float,
    m_phi_squared: float,
    lambda_phi: float,
) -> DarkSectorStressEnergyPerturbationCertificate:
    """Evaluate the source formulas directly in x = k^2."""

    return _dark_sector_stress_energy_perturbations_k_squared_impl(
        scale_factor=scale_factor,
        wave_number_squared=wave_number_squared,
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
