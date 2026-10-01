"""Polarization normalization conversion certificate.

The repository convention uses Pi_repo = Theta_2 + 6 E_repo_2.
The standard Hu-White convention uses P = (Theta_2 - sqrt(6) E_HW_2)/10.

The two conventions are related by E_HW_2 = -E_repo_2/sqrt(6),
so Pi_repo = 10 P. This module certifies only that algebraic
normalization map; it does not alter the photon hierarchy.
"""

from __future__ import annotations

from dataclasses import dataclass
import math


@dataclass(frozen=True)
class PolarizationNormalizationConversion:
    theta_2: float
    e_repo_2: float
    e_hu_white_2: float
    pi_repo: float
    p_hu_white: float
    conversion_residual: float
    normalization_equivalent: bool


def polarization_normalization_conversion(
    *,
    theta_2: float,
    e_repo_2: float,
    closure_tolerance: float = 1.0e-12,
) -> PolarizationNormalizationConversion:
    """Certify the repository-to-Hu-White scalar polarization map."""

    for name, value in (
        ("theta_2", theta_2),
        ("e_repo_2", e_repo_2),
        ("closure_tolerance", closure_tolerance),
    ):
        if not math.isfinite(value):
            raise ValueError(f"{name} must be finite")

    if closure_tolerance < 0.0:
        raise ValueError("closure_tolerance must be nonnegative")

    e_hu_white_2 = -e_repo_2 / math.sqrt(6.0)
    pi_repo = theta_2 + 6.0 * e_repo_2
    p_hu_white = (
        theta_2 - math.sqrt(6.0) * e_hu_white_2
    ) / 10.0
    conversion_residual = pi_repo - 10.0 * p_hu_white
    scale = max(1.0, abs(pi_repo))

    return PolarizationNormalizationConversion(
        theta_2=float(theta_2),
        e_repo_2=float(e_repo_2),
        e_hu_white_2=float(e_hu_white_2),
        pi_repo=float(pi_repo),
        p_hu_white=float(p_hu_white),
        conversion_residual=float(conversion_residual),
        normalization_equivalent=(
            abs(conversion_residual) <= closure_tolerance * scale
        ),
    )
