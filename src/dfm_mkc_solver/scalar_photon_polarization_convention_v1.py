"""Scalar photon polarization convention for the DFM-MKC hierarchy.

This module fixes the scalar polarization variables before a numerical
Boltzmann implementation is attempted.

Convention
----------
Theta_l is the photon temperature multipole, E_l and B_l are the scalar
polarization multipoles, and the Thomson polarization source is

    Pi = Theta_2 + 6 E_2.

For scalar perturbations the magnetic-parity hierarchy is identically zero,
and the E hierarchy starts at l=2.  Thus E_1 is a boundary value, not a
dynamical scalar multipole:

    E_1 = 0,
    B_l = 0.

This module is a convention/boundary certificate only.  It does not claim a
closed photon hierarchy, recombination model, or numerical CMB solution.
"""

from __future__ import annotations

from dataclasses import dataclass
import math
from typing import Sequence


@dataclass(frozen=True)
class ScalarPhotonPolarizationConvention:
    """Repository-level scalar photon polarization convention."""

    theta_2: float
    e_2: float
    e_1: float
    b_multipoles: tuple[float, ...]
    pi: float
    e1_boundary_residual: float
    scalar_b_residual: float
    polarization_convention_closed: bool


def _require_finite(name: str, value: float) -> None:
    if not math.isfinite(value):
        raise ValueError(f"{name} must be finite")


def scalar_photon_polarization_convention(
    *,
    theta_2: float,
    e_2: float,
    e_1: float = 0.0,
    b_multipoles: Sequence[float] = (),
    closure_tolerance: float = 1.0e-12,
) -> ScalarPhotonPolarizationConvention:
    """Certify the scalar polarization convention and l=1 boundary."""

    for name, value in (
        ("theta_2", theta_2),
        ("e_2", e_2),
        ("e_1", e_1),
        ("closure_tolerance", closure_tolerance),
    ):
        _require_finite(name, value)

    if closure_tolerance < 0.0:
        raise ValueError("closure_tolerance must be nonnegative")

    b_values = tuple(float(value) for value in b_multipoles)
    for index, value in enumerate(b_values):
        _require_finite(f"b_multipoles[{index}]", value)

    pi = theta_2 + 6.0 * e_2
    e1_boundary_residual = e_1
    scalar_b_residual = (
        max((abs(value) for value in b_values), default=0.0)
    )

    scale = max(1.0, abs(pi))
    polarization_convention_closed = (
        abs(e1_boundary_residual) <= closure_tolerance * scale
        and scalar_b_residual <= closure_tolerance * scale
    )

    return ScalarPhotonPolarizationConvention(
        theta_2=float(theta_2),
        e_2=float(e_2),
        e_1=float(e_1),
        b_multipoles=b_values,
        pi=float(pi),
        e1_boundary_residual=float(e1_boundary_residual),
        scalar_b_residual=float(scalar_b_residual),
        polarization_convention_closed=(
            polarization_convention_closed
        ),
    )
