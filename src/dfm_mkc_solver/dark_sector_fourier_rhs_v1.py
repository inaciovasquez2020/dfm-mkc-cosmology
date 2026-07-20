"""Closed instantaneous DFM-MKC Fourier-mode right-hand side.

This module composes the existing action-derived objects:

* dark-sector stress-energy perturbations;
* Newtonian-gauge metric-constraint elimination;
* amplitude perturbation evolution;
* phase-current perturbation evolution.

The closure is restricted to nonzero Fourier modes with zero total scalar
anisotropic stress. Visible-sector density and momentum sources may be
supplied instantaneously, but their evolution is not solved here.

Because the dark-sector density perturbation depends linearly on Psi,

    delta_rho_dark
      = delta_rho_dark_at_Psi_zero
        - (rho_dark + p_dark) Psi,

the Poisson and momentum constraints give the algebraic solution

    [k^2 - 4 pi G a^2 (rho_dark + p_dark)] Psi
      = -4 pi G a^2 delta_rho_at_Psi_zero
        - 3 Hc (4 pi G a^2 / k^2) momentum_total.

The resulting metric variables are inserted into the amplitude and phase
equations to produce delta_phi'' and delta_theta''.

This is an instantaneous dark-sector right-hand-side certificate. It does
not evolve visible species, close a Boltzmann hierarchy, integrate a mode,
or compute an observable.
"""

from __future__ import annotations

import math
from dataclasses import dataclass

from .dark_sector_amplitude_perturbation_v1 import (
    AmplitudePerturbationCertificate,
    dark_sector_amplitude_perturbation,
)
from .dark_sector_phase_perturbation_v1 import (
    PhasePerturbationCertificate,
    dark_sector_phase_perturbation,
)
from .dark_sector_stress_energy_perturbations_v1 import (
    DarkSectorStressEnergyPerturbationCertificate,
    dark_sector_stress_energy_perturbations,
)
from .metric_constraint_elimination_v1 import (
    MetricConstraintEliminationCertificate,
    eliminate_newtonian_metric_constraints,
)


@dataclass(frozen=True)
class DarkSectorFourierRightHandSideCertificate:
    constraint_denominator: float
    metric_potential: float
    metric_potential_prime: float
    delta_phi_double_prime: float
    delta_theta_double_prime: float
    total_delta_energy_density: float
    total_momentum_divergence_source: float
    density_reconstruction_residual: float
    metric_closure_residual: float
    stress_energy: DarkSectorStressEnergyPerturbationCertificate
    metric_constraints: MetricConstraintEliminationCertificate
    amplitude_equation: AmplitudePerturbationCertificate
    phase_equation: PhasePerturbationCertificate
    instantaneous_dark_sector_rhs_closed: bool
    visible_sector_evolution_closed: bool
    numerical_mode_evolution_run: bool


def _require_finite(name: str, value: float) -> None:
    if not math.isfinite(value):
        raise ValueError(f"{name} must be finite")


def dark_sector_fourier_right_hand_side(
    *,
    scale_factor: float,
    conformal_hubble: float,
    wave_number: float,
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
    visible_delta_energy_density: float = 0.0,
    visible_momentum_divergence_source: float = 0.0,
    denominator_tolerance: float = 1.0e-14,
) -> DarkSectorFourierRightHandSideCertificate:
    """Return the closed instantaneous dark-sector Fourier-mode RHS."""

    for name, value in (
        ("scale_factor", scale_factor),
        ("conformal_hubble", conformal_hubble),
        ("wave_number", wave_number),
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
        (
            "visible_delta_energy_density",
            visible_delta_energy_density,
        ),
        (
            "visible_momentum_divergence_source",
            visible_momentum_divergence_source,
        ),
        ("denominator_tolerance", denominator_tolerance),
    ):
        _require_finite(name, value)

    if wave_number == 0.0:
        raise ValueError("wave_number must be nonzero")
    if denominator_tolerance <= 0.0:
        raise ValueError("denominator_tolerance must be positive")

    zero_metric_stress = dark_sector_stress_energy_perturbations(
        scale_factor=scale_factor,
        wave_number=abs(wave_number),
        phi_background=phi_background,
        phi_prime_background=phi_prime_background,
        theta_prime_background=theta_prime_background,
        delta_phi=delta_phi,
        delta_phi_prime=delta_phi_prime,
        delta_theta=delta_theta,
        delta_theta_prime=delta_theta_prime,
        psi_metric=0.0,
        alpha=alpha,
        beta=beta,
        rho_star=rho_star,
        m_phi_squared=m_phi_squared,
        lambda_phi=lambda_phi,
    )

    gravitational_prefactor = (
        4.0
        * math.pi
        * gravitational_constant
        * scale_factor**2
    )

    wave_number_squared = wave_number**2

    total_momentum_divergence_source = (
        visible_momentum_divergence_source
        + zero_metric_stress.momentum_divergence_source
    )

    zero_metric_total_density = (
        visible_delta_energy_density
        + zero_metric_stress.delta_energy_density
    )

    constraint_denominator = (
        wave_number_squared
        - gravitational_prefactor
        * zero_metric_stress.background_enthalpy
    )

    if abs(constraint_denominator) <= denominator_tolerance:
        raise ValueError(
            "metric constraint denominator is singular"
        )

    metric_potential = (
        -gravitational_prefactor
        * zero_metric_total_density
        - 3.0
        * conformal_hubble
        * gravitational_prefactor
        * total_momentum_divergence_source
        / wave_number_squared
    ) / constraint_denominator

    stress_energy = dark_sector_stress_energy_perturbations(
        scale_factor=scale_factor,
        wave_number=abs(wave_number),
        phi_background=phi_background,
        phi_prime_background=phi_prime_background,
        theta_prime_background=theta_prime_background,
        delta_phi=delta_phi,
        delta_phi_prime=delta_phi_prime,
        delta_theta=delta_theta,
        delta_theta_prime=delta_theta_prime,
        psi_metric=metric_potential,
        alpha=alpha,
        beta=beta,
        rho_star=rho_star,
        m_phi_squared=m_phi_squared,
        lambda_phi=lambda_phi,
    )

    total_delta_energy_density = (
        visible_delta_energy_density
        + stress_energy.delta_energy_density
    )

    metric_constraints = eliminate_newtonian_metric_constraints(
        wave_number=wave_number,
        scale_factor=scale_factor,
        conformal_hubble=conformal_hubble,
        gravitational_constant=gravitational_constant,
        delta_rho_total=total_delta_energy_density,
        momentum_source=total_momentum_divergence_source,
        enthalpy_sigma_total=0.0,
    )

    density_reconstruction_residual = (
        stress_energy.delta_energy_density
        - (
            zero_metric_stress.delta_energy_density
            - zero_metric_stress.background_enthalpy
            * metric_potential
        )
    )

    metric_closure_residual = (
        metric_constraints.psi - metric_potential
    )

    amplitude_equation = dark_sector_amplitude_perturbation(
        scale_factor=scale_factor,
        conformal_hubble=conformal_hubble,
        wave_number=abs(wave_number),
        phi_background=phi_background,
        phi_prime_background=phi_prime_background,
        theta_prime_background=theta_prime_background,
        delta_phi=delta_phi,
        delta_phi_prime=delta_phi_prime,
        delta_theta_prime=delta_theta_prime,
        psi_metric=metric_constraints.psi,
        psi_metric_prime=metric_constraints.phi_prime,
        phi_metric_prime=metric_constraints.phi_prime,
        alpha=alpha,
        beta=beta,
        m_phi_squared=m_phi_squared,
        lambda_phi=lambda_phi,
    )

    phase_equation = dark_sector_phase_perturbation(
        scale_factor=scale_factor,
        conformal_hubble=conformal_hubble,
        wave_number=abs(wave_number),
        phi_background=phi_background,
        phi_prime_background=phi_prime_background,
        theta_prime_background=theta_prime_background,
        delta_phi=delta_phi,
        delta_phi_prime=delta_phi_prime,
        delta_theta=delta_theta,
        delta_theta_prime=delta_theta_prime,
        psi_metric=metric_constraints.psi,
        psi_metric_prime=metric_constraints.phi_prime,
        phi_metric=metric_constraints.phi,
        phi_metric_prime=metric_constraints.phi_prime,
        beta=beta,
    )

    for name, value in (
        ("constraint_denominator", constraint_denominator),
        ("metric_potential", metric_potential),
        (
            "metric_potential_prime",
            metric_constraints.phi_prime,
        ),
        (
            "delta_phi_double_prime",
            amplitude_equation.delta_phi_double_prime,
        ),
        (
            "delta_theta_double_prime",
            phase_equation.delta_theta_double_prime,
        ),
        (
            "total_delta_energy_density",
            total_delta_energy_density,
        ),
        (
            "total_momentum_divergence_source",
            total_momentum_divergence_source,
        ),
        (
            "density_reconstruction_residual",
            density_reconstruction_residual,
        ),
        ("metric_closure_residual", metric_closure_residual),
    ):
        _require_finite(name, value)

    closure_tolerance = 1.0e-10

    instantaneous_dark_sector_rhs_closed = (
        abs(density_reconstruction_residual)
        <= closure_tolerance
        and abs(metric_closure_residual)
        <= closure_tolerance
        and abs(metric_constraints.poisson_residual)
        <= closure_tolerance
        and abs(metric_constraints.momentum_residual)
        <= closure_tolerance
        and abs(metric_constraints.anisotropy_residual)
        <= closure_tolerance
        and abs(amplitude_equation.amplitude_equation_residual)
        <= closure_tolerance
        and abs(phase_equation.normalized_equation_residual)
        <= closure_tolerance
    )

    return DarkSectorFourierRightHandSideCertificate(
        constraint_denominator=constraint_denominator,
        metric_potential=metric_potential,
        metric_potential_prime=metric_constraints.phi_prime,
        delta_phi_double_prime=(
            amplitude_equation.delta_phi_double_prime
        ),
        delta_theta_double_prime=(
            phase_equation.delta_theta_double_prime
        ),
        total_delta_energy_density=total_delta_energy_density,
        total_momentum_divergence_source=(
            total_momentum_divergence_source
        ),
        density_reconstruction_residual=(
            density_reconstruction_residual
        ),
        metric_closure_residual=metric_closure_residual,
        stress_energy=stress_energy,
        metric_constraints=metric_constraints,
        amplitude_equation=amplitude_equation,
        phase_equation=phase_equation,
        instantaneous_dark_sector_rhs_closed=(
            instantaneous_dark_sector_rhs_closed
        ),
        visible_sector_evolution_closed=False,
        numerical_mode_evolution_run=False,
    )
