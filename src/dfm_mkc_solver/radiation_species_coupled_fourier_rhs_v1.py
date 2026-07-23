"""Separate baryon, photon, and massless-neutrino perturbation carrier.

The state supplied here contains the baryon and photon monopole/dipole
variables and the massless-neutrino monopole, dipole, and quadrupole:

    (delta_b, theta_b, delta_gamma, theta_gamma,
     delta_nu, theta_nu, sigma_nu).

An explicit neutrino octupole F_nu3 is accepted so the quadrupole derivative
is not silently truncated.  The octupole evolution and higher hierarchy are
not supplied, so this module does not claim a closed physical Boltzmann
hierarchy.

A nonnegative conformal Thomson rate Gamma_T is also accepted.  Its baryon and
photon Euler terms are constructed to conserve their total momentum exactly.
"""

from __future__ import annotations

from dataclasses import dataclass
import math

from .dark_sector_fourier_rhs_v1 import (
    DarkSectorFourierRightHandSideCertificate,
    dark_sector_fourier_right_hand_side_k_squared,
)


@dataclass(frozen=True)
class RadiationSpeciesCoupledFourierRightHandSideCertificate:
    dark_sector_rhs: DarkSectorFourierRightHandSideCertificate
    visible_delta_energy_density: float
    visible_momentum_divergence_source: float
    visible_enthalpy_sigma_total: float
    visible_enthalpy_sigma_total_prime: float
    baryon_density_contrast_prime: float
    baryon_velocity_divergence_prime: float
    photon_density_contrast_prime: float
    photon_velocity_divergence_prime: float
    neutrino_density_contrast_prime: float
    neutrino_velocity_divergence_prime: float
    neutrino_anisotropic_stress_prime: float
    baryon_continuity_residual: float
    baryon_euler_residual: float
    photon_continuity_residual: float
    photon_euler_residual: float
    neutrino_continuity_residual: float
    neutrino_euler_residual: float
    neutrino_quadrupole_residual: float
    thomson_momentum_exchange_residual: float
    species_rhs_closed: bool
    photon_baryon_scattering_closed: bool
    neutrino_hierarchy_closed: bool
    physical_radiation_microphysics_closed: bool


def _require_finite(name: str, value: float) -> None:
    if not math.isfinite(value):
        raise ValueError(f"{name} must be finite")


def radiation_species_coupled_fourier_right_hand_side_k_squared(
    *,
    scale_factor: float,
    conformal_hubble: float,
    wave_number_squared: float,
    gravitational_constant: float,
    phi_background: float,
    phi_prime_background: float,
    theta_prime_background: float,
    delta_phi: float,
    delta_phi_prime: float,
    delta_theta: float,
    delta_theta_prime: float,
    alpha: float,
    beta: float,
    rho_star: float,
    m_phi_squared: float,
    lambda_phi: float,
    baryon_background_density: float,
    photon_background_density: float,
    neutrino_background_density: float,
    baryon_density_contrast: float,
    baryon_velocity_divergence: float,
    photon_density_contrast: float,
    photon_velocity_divergence: float,
    neutrino_density_contrast: float,
    neutrino_velocity_divergence: float,
    neutrino_anisotropic_stress: float,
    neutrino_octupole: float,
    thomson_scattering_rate: float,
    denominator_tolerance: float = 1.0e-14,
    closure_tolerance: float = 1.0e-10,
) -> RadiationSpeciesCoupledFourierRightHandSideCertificate:
    """Return the split species RHS with an open neutrino hierarchy."""

    values = (
        ("scale_factor", scale_factor),
        ("conformal_hubble", conformal_hubble),
        ("wave_number_squared", wave_number_squared),
        ("gravitational_constant", gravitational_constant),
        ("phi_background", phi_background),
        ("phi_prime_background", phi_prime_background),
        ("theta_prime_background", theta_prime_background),
        ("delta_phi", delta_phi),
        ("delta_phi_prime", delta_phi_prime),
        ("delta_theta", delta_theta),
        ("delta_theta_prime", delta_theta_prime),
        ("alpha", alpha),
        ("beta", beta),
        ("rho_star", rho_star),
        ("m_phi_squared", m_phi_squared),
        ("lambda_phi", lambda_phi),
        ("baryon_background_density", baryon_background_density),
        ("photon_background_density", photon_background_density),
        ("neutrino_background_density", neutrino_background_density),
        ("baryon_density_contrast", baryon_density_contrast),
        ("baryon_velocity_divergence", baryon_velocity_divergence),
        ("photon_density_contrast", photon_density_contrast),
        ("photon_velocity_divergence", photon_velocity_divergence),
        ("neutrino_density_contrast", neutrino_density_contrast),
        ("neutrino_velocity_divergence", neutrino_velocity_divergence),
        ("neutrino_anisotropic_stress", neutrino_anisotropic_stress),
        ("neutrino_octupole", neutrino_octupole),
        ("thomson_scattering_rate", thomson_scattering_rate),
        ("denominator_tolerance", denominator_tolerance),
        ("closure_tolerance", closure_tolerance),
    )
    for name, value in values:
        _require_finite(name, value)

    if scale_factor <= 0.0:
        raise ValueError("scale_factor must be positive")
    if conformal_hubble <= 0.0:
        raise ValueError("conformal_hubble must be positive")
    if wave_number_squared <= 0.0:
        raise ValueError("wave_number_squared must be positive")
    if gravitational_constant <= 0.0:
        raise ValueError("gravitational_constant must be positive")
    if min(
        baryon_background_density,
        photon_background_density,
        neutrino_background_density,
    ) < 0.0:
        raise ValueError("background densities must be nonnegative")
    if thomson_scattering_rate < 0.0:
        raise ValueError(
            "thomson_scattering_rate must be nonnegative"
        )
    if (
        baryon_background_density == 0.0
        and thomson_scattering_rate != 0.0
    ):
        raise ValueError(
            "nonzero Thomson scattering requires baryon density"
        )
    if denominator_tolerance <= 0.0:
        raise ValueError("denominator_tolerance must be positive")
    if closure_tolerance < 0.0:
        raise ValueError("closure_tolerance must be nonnegative")

    wave_number = math.sqrt(wave_number_squared)

    neutrino_anisotropic_stress_prime = (
        (4.0 / 15.0) * neutrino_velocity_divergence
        - (3.0 / 10.0) * wave_number * neutrino_octupole
    )

    visible_delta_energy_density = (
        baryon_background_density * baryon_density_contrast
        + photon_background_density * photon_density_contrast
        + neutrino_background_density * neutrino_density_contrast
    )
    visible_momentum_divergence_source = (
        baryon_background_density * baryon_velocity_divergence
        + (4.0 / 3.0)
        * photon_background_density
        * photon_velocity_divergence
        + (4.0 / 3.0)
        * neutrino_background_density
        * neutrino_velocity_divergence
    )
    visible_enthalpy_sigma_total = (
        (4.0 / 3.0)
        * neutrino_background_density
        * neutrino_anisotropic_stress
    )
    visible_enthalpy_sigma_total_prime = (
        (4.0 / 3.0)
        * neutrino_background_density
        * (
            neutrino_anisotropic_stress_prime
            - 4.0
            * conformal_hubble
            * neutrino_anisotropic_stress
        )
    )

    dark_sector_rhs = dark_sector_fourier_right_hand_side_k_squared(
        scale_factor=scale_factor,
        conformal_hubble=conformal_hubble,
        wave_number_squared=wave_number_squared,
        gravitational_constant=gravitational_constant,
        phi_background=phi_background,
        phi_prime_background=phi_prime_background,
        theta_prime_background=theta_prime_background,
        delta_phi=delta_phi,
        delta_phi_prime=delta_phi_prime,
        delta_theta=delta_theta,
        delta_theta_prime=delta_theta_prime,
        alpha=alpha,
        beta=beta,
        rho_star=rho_star,
        m_phi_squared=m_phi_squared,
        lambda_phi=lambda_phi,
        visible_delta_energy_density=visible_delta_energy_density,
        visible_momentum_divergence_source=(
            visible_momentum_divergence_source
        ),
        visible_enthalpy_sigma_total=(
            visible_enthalpy_sigma_total
        ),
        visible_enthalpy_sigma_total_prime=(
            visible_enthalpy_sigma_total_prime
        ),
        denominator_tolerance=denominator_tolerance,
    )

    metric = dark_sector_rhs.metric_constraints
    phi_metric_prime = float(metric.phi_prime)
    psi_metric = float(metric.psi)

    photon_collision = (
        thomson_scattering_rate
        * (
            baryon_velocity_divergence
            - photon_velocity_divergence
        )
    )
    if baryon_background_density == 0.0:
        baryon_collision = 0.0
    else:
        baryon_collision = (
            (4.0 / 3.0)
            * photon_background_density
            / baryon_background_density
            * thomson_scattering_rate
            * (
                photon_velocity_divergence
                - baryon_velocity_divergence
            )
        )

    baryon_density_contrast_prime = (
        -baryon_velocity_divergence
        + 3.0 * phi_metric_prime
    )
    baryon_velocity_divergence_prime = (
        -conformal_hubble * baryon_velocity_divergence
        + wave_number_squared * psi_metric
        + baryon_collision
    )
    photon_density_contrast_prime = (
        -(4.0 / 3.0) * photon_velocity_divergence
        + 4.0 * phi_metric_prime
    )
    photon_velocity_divergence_prime = (
        wave_number_squared
        * (0.25 * photon_density_contrast + psi_metric)
        + photon_collision
    )
    neutrino_density_contrast_prime = (
        -(4.0 / 3.0) * neutrino_velocity_divergence
        + 4.0 * phi_metric_prime
    )
    neutrino_velocity_divergence_prime = (
        wave_number_squared
        * (
            0.25 * neutrino_density_contrast
            + psi_metric
            - neutrino_anisotropic_stress
        )
    )

    baryon_continuity_residual = (
        baryon_density_contrast_prime
        + baryon_velocity_divergence
        - 3.0 * phi_metric_prime
    )
    baryon_euler_residual = (
        baryon_velocity_divergence_prime
        + conformal_hubble * baryon_velocity_divergence
        - wave_number_squared * psi_metric
        - baryon_collision
    )
    photon_continuity_residual = (
        photon_density_contrast_prime
        + (4.0 / 3.0) * photon_velocity_divergence
        - 4.0 * phi_metric_prime
    )
    photon_euler_residual = (
        photon_velocity_divergence_prime
        - wave_number_squared
        * (0.25 * photon_density_contrast + psi_metric)
        - photon_collision
    )
    neutrino_continuity_residual = (
        neutrino_density_contrast_prime
        + (4.0 / 3.0) * neutrino_velocity_divergence
        - 4.0 * phi_metric_prime
    )
    neutrino_euler_residual = (
        neutrino_velocity_divergence_prime
        - wave_number_squared
        * (
            0.25 * neutrino_density_contrast
            + psi_metric
            - neutrino_anisotropic_stress
        )
    )
    neutrino_quadrupole_residual = (
        neutrino_anisotropic_stress_prime
        - (4.0 / 15.0) * neutrino_velocity_divergence
        + (3.0 / 10.0) * wave_number * neutrino_octupole
    )
    thomson_momentum_exchange_residual = (
        baryon_background_density * baryon_collision
        + (4.0 / 3.0)
        * photon_background_density
        * photon_collision
    )

    residuals = (
        baryon_continuity_residual,
        baryon_euler_residual,
        photon_continuity_residual,
        photon_euler_residual,
        neutrino_continuity_residual,
        neutrino_euler_residual,
        neutrino_quadrupole_residual,
        thomson_momentum_exchange_residual,
        dark_sector_rhs.metric_constraints.poisson_residual,
        dark_sector_rhs.metric_constraints.momentum_residual,
        dark_sector_rhs.metric_constraints.anisotropy_residual,
    )
    species_rhs_closed = (
        dark_sector_rhs.instantaneous_dark_sector_rhs_closed
        and max(abs(value) for value in residuals)
        <= closure_tolerance
    )

    return RadiationSpeciesCoupledFourierRightHandSideCertificate(
        dark_sector_rhs=dark_sector_rhs,
        visible_delta_energy_density=float(
            visible_delta_energy_density
        ),
        visible_momentum_divergence_source=float(
            visible_momentum_divergence_source
        ),
        visible_enthalpy_sigma_total=float(
            visible_enthalpy_sigma_total
        ),
        visible_enthalpy_sigma_total_prime=float(
            visible_enthalpy_sigma_total_prime
        ),
        baryon_density_contrast_prime=float(
            baryon_density_contrast_prime
        ),
        baryon_velocity_divergence_prime=float(
            baryon_velocity_divergence_prime
        ),
        photon_density_contrast_prime=float(
            photon_density_contrast_prime
        ),
        photon_velocity_divergence_prime=float(
            photon_velocity_divergence_prime
        ),
        neutrino_density_contrast_prime=float(
            neutrino_density_contrast_prime
        ),
        neutrino_velocity_divergence_prime=float(
            neutrino_velocity_divergence_prime
        ),
        neutrino_anisotropic_stress_prime=float(
            neutrino_anisotropic_stress_prime
        ),
        baryon_continuity_residual=float(
            baryon_continuity_residual
        ),
        baryon_euler_residual=float(baryon_euler_residual),
        photon_continuity_residual=float(
            photon_continuity_residual
        ),
        photon_euler_residual=float(photon_euler_residual),
        neutrino_continuity_residual=float(
            neutrino_continuity_residual
        ),
        neutrino_euler_residual=float(
            neutrino_euler_residual
        ),
        neutrino_quadrupole_residual=float(
            neutrino_quadrupole_residual
        ),
        thomson_momentum_exchange_residual=float(
            thomson_momentum_exchange_residual
        ),
        species_rhs_closed=species_rhs_closed,
        photon_baryon_scattering_closed=True,
        neutrino_hierarchy_closed=False,
        physical_radiation_microphysics_closed=False,
    )
