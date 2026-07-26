"""Initial-slice gauge-invariant normalization of the regular mode.

The action convention is

    g_ij = a^2 [(1 - 2 psi) delta_ij + ...],

so an e-fold time shift ``sigma = H_conformal T`` gives
``psi -> psi + sigma``.  The Newtonian constraint code calls this same
curvature potential ``phi``; its variable called ``psi`` is instead the
lapse potential.  With ``delta_rho -> delta_rho - rho_N sigma``,

    zeta = -psi - delta_rho / rho_N

is invariant by direct algebra.  This module certifies only that initial
slice identity and the resulting normalization of one mode ray.
"""

from __future__ import annotations

import math
from dataclasses import dataclass
from typing import Iterable


State = tuple[float, ...]


def _finite(name: str, value: float) -> float:
    value = float(value)
    if not math.isfinite(value):
        raise ValueError(f"{name} must be finite")
    return value


def uniform_density_curvature(
    psi: float, delta_rho: float, rho_N: float
) -> float:
    """Return ``zeta = -psi - delta_rho/rho_N``."""
    return -float(psi) - float(delta_rho) / float(rho_N)


def transformed_uniform_density_curvature(
    psi: float, delta_rho: float, rho_N: float, sigma: float
) -> float:
    """Return zeta after the declared scalar e-fold time shift."""
    return uniform_density_curvature(
        float(psi) + float(sigma),
        float(delta_rho) - float(rho_N) * float(sigma),
        rho_N,
    )


def gauge_invariance_residual(zeta: float, zeta_transformed: float) -> float:
    """Return the signed floating-point gauge-invariance residual."""
    return float(zeta_transformed) - float(zeta)


def normalized_initial_state(
    initial_state: Iterable[float], zeta: float
) -> State:
    """Remove the common mode amplitude by division by nonzero zeta."""
    return tuple(float(value) / float(zeta) for value in initial_state)


def background_density_derivative_separated(
    rho_N: float, tolerance: float
) -> bool:
    return abs(float(rho_N)) > float(tolerance)


def initial_uniform_density_curvature_gauge_invariant(
    residual: float, tolerance: float
) -> bool:
    return abs(float(residual)) <= float(tolerance)


def gauge_invariant_normalization_closed(
    *,
    denominator_separated: bool,
    zeta_separated: bool,
    gauge_invariant: bool,
) -> bool:
    return denominator_separated and zeta_separated and gauge_invariant


@dataclass(frozen=True)
class GaugeInvariantRegularModeNormalizationCertificate:
    uniform_density_curvature: float
    transformed_uniform_density_curvature: float
    gauge_invariance_residual: float
    gauge_invariance_residual_tolerance: float
    background_density_derivative_separation_tolerance: float
    uniform_density_curvature_separation_tolerance: float
    background_density_derivative_separated: bool
    initial_uniform_density_curvature_gauge_invariant: bool
    normalized_initial_state: State
    gauge_invariant_normalization_closed: bool
    global_gauge_invariant_observable_completed: bool
    lcdm_tangent_separation_completed: bool
    observational_calibration_completed: bool


def certify_gauge_invariant_regular_mode_normalization(
    *,
    psi: float,
    delta_rho: float,
    rho_N: float,
    initial_state: Iterable[float],
    sigma: float = 0.0,
    residual_relative_tolerance: float = 1.0e-12,
    residual_absolute_tolerance: float = 1.0e-15,
    denominator_separation_tolerance: float = 1.0e-14,
    zeta_separation_tolerance: float = 1.0e-14,
) -> GaugeInvariantRegularModeNormalizationCertificate:
    """Certify the algebraic initial-slice invariant and normalize its ray."""
    psi = _finite("psi", psi)
    delta_rho = _finite("delta_rho", delta_rho)
    rho_N = _finite("rho_N", rho_N)
    sigma = _finite("sigma", sigma)
    values = tuple(_finite("initial_state value", x) for x in initial_state)
    for name, tolerance in (
        ("residual_relative_tolerance", residual_relative_tolerance),
        ("residual_absolute_tolerance", residual_absolute_tolerance),
        ("denominator_separation_tolerance", denominator_separation_tolerance),
        ("zeta_separation_tolerance", zeta_separation_tolerance),
    ):
        if not math.isfinite(tolerance) or tolerance <= 0.0:
            raise ValueError(f"{name} must be finite and positive")

    denominator_closed = background_density_derivative_separated(
        rho_N, denominator_separation_tolerance
    )
    if not denominator_closed:
        raise ValueError("rho_N is zero or insufficiently separated from zero")

    zeta = uniform_density_curvature(psi, delta_rho, rho_N)
    transformed = transformed_uniform_density_curvature(
        psi, delta_rho, rho_N, sigma
    )
    residual = gauge_invariance_residual(zeta, transformed)
    residual_scale = max(
        abs(zeta),
        abs(transformed),
        abs(psi),
        abs(delta_rho / rho_N),
        1.0e-300,
    )
    residual_tolerance = (
        residual_absolute_tolerance
        + residual_relative_tolerance * residual_scale
    )
    invariant = initial_uniform_density_curvature_gauge_invariant(
        residual, residual_tolerance
    )
    zeta_closed = abs(zeta) > zeta_separation_tolerance
    if not zeta_closed:
        raise ValueError("zeta is zero or insufficiently separated from zero")

    normalized = normalized_initial_state(values, zeta)
    closed = gauge_invariant_normalization_closed(
        denominator_separated=denominator_closed,
        zeta_separated=zeta_closed,
        gauge_invariant=invariant,
    )
    return GaugeInvariantRegularModeNormalizationCertificate(
        uniform_density_curvature=zeta,
        transformed_uniform_density_curvature=transformed,
        gauge_invariance_residual=residual,
        gauge_invariance_residual_tolerance=residual_tolerance,
        background_density_derivative_separation_tolerance=(
            denominator_separation_tolerance
        ),
        uniform_density_curvature_separation_tolerance=(
            zeta_separation_tolerance
        ),
        background_density_derivative_separated=denominator_closed,
        initial_uniform_density_curvature_gauge_invariant=invariant,
        normalized_initial_state=normalized,
        gauge_invariant_normalization_closed=closed,
        global_gauge_invariant_observable_completed=False,
        lcdm_tangent_separation_completed=False,
        observational_calibration_completed=False,
    )
