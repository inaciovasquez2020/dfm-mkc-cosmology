"""Action-derived principal symbol for DFM-MKC dark-sector scalars.

For

    L_dark =
        -(alpha / 2) (nabla phi)^2
        -(beta / 2) phi^2 (nabla theta)^2
        -U(phi),

expanded around a homogeneous FLRW background, the principal quadratic
scalar action is

    S2_principal = (1 / 2) integral a^2 [
        alpha ((delta phi')^2 - |grad delta phi|^2)
        + beta phi_bar^2
          ((delta theta')^2 - |grad delta theta|^2)
    ].

Therefore the field-sector kinetic and gradient matrices are both

    a^2 diag(alpha, beta phi_bar^2).

This module certifies only that action-derived principal field block. It
does not eliminate metric constraints, prove global stability, exclude
tachyonic lower-order terms, or establish full perturbative well-posedness.
"""

from __future__ import annotations

import math
from dataclasses import dataclass


Matrix2 = tuple[tuple[float, float], tuple[float, float]]


@dataclass(frozen=True)
class DarkSectorPrincipalCertificate:
    kinetic_matrix: Matrix2
    gradient_matrix: Matrix2
    kinetic_eigenvalues: tuple[float, float]
    gradient_eigenvalues: tuple[float, float]
    principal_rank: int
    kinetic_positive_definite: bool
    gradient_positive_definite: bool
    phase_degenerate: bool
    principal_sound_speed_squared: tuple[float, float] | None


def _require_finite(name: str, value: float) -> None:
    if not math.isfinite(value):
        raise ValueError(f"{name} must be finite")


def dark_sector_principal_certificate(
    *,
    scale_factor: float,
    phi_background: float,
    alpha: float,
    beta: float,
) -> DarkSectorPrincipalCertificate:
    """Return the exact two-field principal stability certificate."""

    for name, value in (
        ("scale_factor", scale_factor),
        ("phi_background", phi_background),
        ("alpha", alpha),
        ("beta", beta),
    ):
        _require_finite(name, value)

    if scale_factor <= 0.0:
        raise ValueError("scale_factor must be positive")
    if alpha <= 0.0:
        raise ValueError("alpha must be positive")
    if beta <= 0.0:
        raise ValueError("beta must be positive")

    amplitude_coefficient = scale_factor**2 * alpha
    phase_coefficient = (
        scale_factor**2
        * beta
        * phi_background**2
    )

    _require_finite("amplitude_coefficient", amplitude_coefficient)
    _require_finite("phase_coefficient", phase_coefficient)

    matrix: Matrix2 = (
        (amplitude_coefficient, 0.0),
        (0.0, phase_coefficient),
    )
    phase_degenerate = phase_coefficient == 0.0
    positive_definite = (
        amplitude_coefficient > 0.0
        and phase_coefficient > 0.0
    )

    return DarkSectorPrincipalCertificate(
        kinetic_matrix=matrix,
        gradient_matrix=matrix,
        kinetic_eigenvalues=(
            amplitude_coefficient,
            phase_coefficient,
        ),
        gradient_eigenvalues=(
            amplitude_coefficient,
            phase_coefficient,
        ),
        principal_rank=1 if phase_degenerate else 2,
        kinetic_positive_definite=positive_definite,
        gradient_positive_definite=positive_definite,
        phase_degenerate=phase_degenerate,
        principal_sound_speed_squared=(
            None if phase_degenerate else (1.0, 1.0)
        ),
    )


@dataclass(frozen=True)
class DarkSectorLowerOrderCertificate:
    """Fixed-background, uneliminated scalar lower-order block."""

    potential_curvature: float
    phase_velocity_shift: float
    amplitude_mass_numerator: float
    amplitude_mass_squared: float
    phase_mass_squared: float
    derivative_mixing_coefficient: float
    uneliminated_mass_matrix: Matrix2
    amplitude_tachyon_free: bool
    phase_shift_symmetry_preserved: bool
    metric_constraints_eliminated: bool
    complete_scalar_stability_certified: bool


def dark_sector_lower_order_certificate(
    *,
    phi_background: float,
    theta_dot_background: float,
    alpha: float,
    beta: float,
    m_phi_squared: float,
    lambda_phi: float,
) -> DarkSectorLowerOrderCertificate:
    """Return the action-derived fixed-background lower-order field block.

    For the quartic potential

        U(phi) = rho_star
                 + (1 / 2) m_phi_squared phi^2
                 + (1 / 4) lambda_phi phi^4,

    the amplitude curvature is

        U''(phi_bar)
        = m_phi_squared + 3 lambda_phi phi_bar^2.

    Expanding the phase kinetic term around a homogeneous background adds

        +(beta / 2) theta_dot_bar^2 (delta phi)^2

    and the derivative mixing

        2 beta phi_bar theta_dot_bar
        delta phi delta theta_dot.

    Before metric-constraint elimination, the algebraic field block is

        M_uneliminated
        = diag(
            U''(phi_bar) - beta theta_dot_bar^2,
            0,
          ).

    The zero phase entry follows from theta shift symmetry. This result does
    not diagonalize the derivative mixing, eliminate metric constraints, or
    certify the complete scalar perturbation system.
    """

    for name, value in (
        ("phi_background", phi_background),
        ("theta_dot_background", theta_dot_background),
        ("alpha", alpha),
        ("beta", beta),
        ("m_phi_squared", m_phi_squared),
        ("lambda_phi", lambda_phi),
    ):
        _require_finite(name, value)

    if alpha <= 0.0:
        raise ValueError("alpha must be positive")
    if beta <= 0.0:
        raise ValueError("beta must be positive")
    if lambda_phi < 0.0:
        raise ValueError("lambda_phi must be nonnegative")

    potential_curvature = (
        m_phi_squared
        + 3.0 * lambda_phi * phi_background**2
    )
    phase_velocity_shift = (
        beta * theta_dot_background**2
    )
    amplitude_mass_numerator = (
        potential_curvature - phase_velocity_shift
    )
    amplitude_mass_squared = (
        amplitude_mass_numerator / alpha
    )
    derivative_mixing_coefficient = (
        2.0
        * beta
        * phi_background
        * theta_dot_background
    )

    for name, value in (
        ("potential_curvature", potential_curvature),
        ("phase_velocity_shift", phase_velocity_shift),
        ("amplitude_mass_numerator", amplitude_mass_numerator),
        ("amplitude_mass_squared", amplitude_mass_squared),
        (
            "derivative_mixing_coefficient",
            derivative_mixing_coefficient,
        ),
    ):
        _require_finite(name, value)

    mass_matrix: Matrix2 = (
        (amplitude_mass_numerator, 0.0),
        (0.0, 0.0),
    )

    return DarkSectorLowerOrderCertificate(
        potential_curvature=potential_curvature,
        phase_velocity_shift=phase_velocity_shift,
        amplitude_mass_numerator=amplitude_mass_numerator,
        amplitude_mass_squared=amplitude_mass_squared,
        phase_mass_squared=0.0,
        derivative_mixing_coefficient=(
            derivative_mixing_coefficient
        ),
        uneliminated_mass_matrix=mass_matrix,
        amplitude_tachyon_free=(
            amplitude_mass_squared >= 0.0
        ),
        phase_shift_symmetry_preserved=True,
        metric_constraints_eliminated=False,
        complete_scalar_stability_certified=False,
    )
