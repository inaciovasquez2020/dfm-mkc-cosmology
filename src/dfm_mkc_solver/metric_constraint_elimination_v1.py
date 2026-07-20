"""Source-level Newtonian-gauge metric-constraint elimination.

For a nonzero Fourier mode k, the supplied scalar constraints are

    k^2 Phi + 3 Hc (Phi' + Hc Psi)
        = -4 pi G a^2 delta_rho_total,

    k^2 (Phi' + Hc Psi)
        = 4 pi G a^2 momentum_source,

    k^2 (Phi - Psi)
        = 12 pi G a^2 enthalpy_sigma_total.

These equations algebraically determine Phi, Psi, and Phi' from the
instantaneous matter and dark-sector sources.

This module does not derive the source perturbations, eliminate constraints
from the quadratic action, close the Boltzmann hierarchy, or prove full
scalar-sector well-posedness.
"""

from __future__ import annotations

import math
from dataclasses import dataclass


@dataclass(frozen=True)
class MetricConstraintEliminationCertificate:
    phi: float
    psi: float
    phi_prime: float
    momentum_combination: float
    anisotropy_difference: float
    poisson_residual: float
    momentum_residual: float
    anisotropy_residual: float
    source_level_constraints_eliminated: bool
    constrained_quadratic_action_derived: bool
    perturbation_system_closed: bool


def _require_finite(name: str, value: float) -> None:
    if not math.isfinite(value):
        raise ValueError(f"{name} must be finite")


def eliminate_newtonian_metric_constraints(
    *,
    wave_number: float,
    scale_factor: float,
    conformal_hubble: float,
    gravitational_constant: float,
    delta_rho_total: float,
    momentum_source: float,
    enthalpy_sigma_total: float,
) -> MetricConstraintEliminationCertificate:
    """Eliminate the three supplied scalar metric constraints for k != 0."""

    for name, value in (
        ("wave_number", wave_number),
        ("scale_factor", scale_factor),
        ("conformal_hubble", conformal_hubble),
        ("gravitational_constant", gravitational_constant),
        ("delta_rho_total", delta_rho_total),
        ("momentum_source", momentum_source),
        ("enthalpy_sigma_total", enthalpy_sigma_total),
    ):
        _require_finite(name, value)

    if wave_number == 0.0:
        raise ValueError("wave_number must be nonzero")
    if scale_factor <= 0.0:
        raise ValueError("scale_factor must be positive")
    if gravitational_constant <= 0.0:
        raise ValueError("gravitational_constant must be positive")

    wave_number_squared = wave_number**2
    gravitational_prefactor = (
        4.0
        * math.pi
        * gravitational_constant
        * scale_factor**2
    )

    momentum_combination = (
        gravitational_prefactor
        * momentum_source
        / wave_number_squared
    )

    phi = (
        -gravitational_prefactor * delta_rho_total
        - 3.0 * conformal_hubble * momentum_combination
    ) / wave_number_squared

    anisotropy_difference = (
        3.0
        * gravitational_prefactor
        * enthalpy_sigma_total
        / wave_number_squared
    )

    psi = phi - anisotropy_difference
    phi_prime = (
        momentum_combination
        - conformal_hubble * psi
    )

    poisson_residual = (
        wave_number_squared * phi
        + 3.0
        * conformal_hubble
        * (phi_prime + conformal_hubble * psi)
        + gravitational_prefactor * delta_rho_total
    )

    momentum_residual = (
        wave_number_squared
        * (phi_prime + conformal_hubble * psi)
        - gravitational_prefactor * momentum_source
    )

    anisotropy_residual = (
        wave_number_squared * (phi - psi)
        - 3.0
        * gravitational_prefactor
        * enthalpy_sigma_total
    )

    for name, value in (
        ("phi", phi),
        ("psi", psi),
        ("phi_prime", phi_prime),
        ("momentum_combination", momentum_combination),
        ("anisotropy_difference", anisotropy_difference),
        ("poisson_residual", poisson_residual),
        ("momentum_residual", momentum_residual),
        ("anisotropy_residual", anisotropy_residual),
    ):
        _require_finite(name, value)

    return MetricConstraintEliminationCertificate(
        phi=phi,
        psi=psi,
        phi_prime=phi_prime,
        momentum_combination=momentum_combination,
        anisotropy_difference=anisotropy_difference,
        poisson_residual=poisson_residual,
        momentum_residual=momentum_residual,
        anisotropy_residual=anisotropy_residual,
        source_level_constraints_eliminated=True,
        constrained_quadratic_action_derived=False,
        perturbation_system_closed=False,
    )
