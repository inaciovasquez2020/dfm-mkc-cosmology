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
