"""Spherical-Bessel terminal relation for massless-neutrino multipoles.

For a freely streaming angular hierarchy with x = k chi, the spherical-Bessel
recurrence gives

    F_(l+1) = (2 l + 1) F_l / x - F_(l-1).

Substituting this into the exact collisionless recurrence yields the standard
terminal derivative

    F_l' = k F_(l-1) - (l + 1) F_l / chi.

Here chi is the positive conformal free-streaming interval.  The relation
closes a finite hierarchy algebraically.  It does not by itself certify that a
chosen l_max is large enough for a coupled cosmological observable.
"""

from __future__ import annotations

from dataclasses import dataclass
import math
from typing import Sequence

from .massless_neutrino_hierarchy_prefix_v1 import (
    MasslessNeutrinoHierarchyPrefix,
    massless_neutrino_hierarchy_prefix,
)


@dataclass(frozen=True)
class MasslessNeutrinoBesselTerminalClosure:
    l_max: int
    wave_number: float
    conformal_free_streaming_interval: float
    free_streaming_phase: float
    multipole_lmax_minus_one: float
    multipole_lmax: float
    estimated_tail_multipole_lmax_plus_one: float
    recurrence_terminal_derivative: float
    reduced_terminal_derivative: float
    derivative_identity_residual: float
    bessel_terminal_relation_closed: bool
    coupled_lmax_convergence_certified: bool


@dataclass(frozen=True)
class MasslessNeutrinoClosedPrefixCertificate:
    terminal_closure: MasslessNeutrinoBesselTerminalClosure
    hierarchy_prefix: MasslessNeutrinoHierarchyPrefix
    finite_hierarchy_algebraically_closed: bool
    coupled_lmax_convergence_certified: bool
    physical_mode_integration_run: bool


def massless_neutrino_bessel_terminal_closure(
    *,
    wave_number_squared: float,
    conformal_free_streaming_interval: float,
    l_max: int,
    multipole_lmax_minus_one: float,
    multipole_lmax: float,
    closure_tolerance: float = 1.0e-12,
) -> MasslessNeutrinoBesselTerminalClosure:
    """Return the Bessel-recurrence terminal tail and derivative."""

    for name, value in (
        ("wave_number_squared", wave_number_squared),
        (
            "conformal_free_streaming_interval",
            conformal_free_streaming_interval,
        ),
        (
            "multipole_lmax_minus_one",
            multipole_lmax_minus_one,
        ),
        ("multipole_lmax", multipole_lmax),
        ("closure_tolerance", closure_tolerance),
    ):
        if not math.isfinite(value):
            raise ValueError(f"{name} must be finite")

    if wave_number_squared <= 0.0:
        raise ValueError("wave_number_squared must be positive")
    if conformal_free_streaming_interval <= 0.0:
        raise ValueError(
            "conformal_free_streaming_interval must be positive"
        )
    if isinstance(l_max, bool) or not isinstance(l_max, int):
        raise TypeError("l_max must be an integer")
    if l_max < 3:
        raise ValueError("l_max must be at least 3")
    if closure_tolerance < 0.0:
        raise ValueError("closure_tolerance must be nonnegative")

    wave_number = math.sqrt(wave_number_squared)
    phase = wave_number * conformal_free_streaming_interval

    estimated_tail = (
        (2.0 * l_max + 1.0)
        * multipole_lmax
        / phase
        - multipole_lmax_minus_one
    )
    recurrence_derivative = (
        wave_number
        / (2.0 * l_max + 1.0)
        * (
            l_max * multipole_lmax_minus_one
            - (l_max + 1.0) * estimated_tail
        )
    )
    reduced_derivative = (
        wave_number * multipole_lmax_minus_one
        - (l_max + 1.0)
        * multipole_lmax
        / conformal_free_streaming_interval
    )
    identity_residual = (
        recurrence_derivative - reduced_derivative
    )

    values = (
        wave_number,
        phase,
        estimated_tail,
        recurrence_derivative,
        reduced_derivative,
        identity_residual,
    )
    if not all(math.isfinite(value) for value in values):
        raise RuntimeError(
            "massless-neutrino terminal closure became nonfinite"
        )

    scale = max(
        1.0,
        abs(recurrence_derivative),
        abs(reduced_derivative),
    )
    closed = bool(
        abs(identity_residual) <= closure_tolerance * scale
    )

    return MasslessNeutrinoBesselTerminalClosure(
        l_max=l_max,
        wave_number=float(wave_number),
        conformal_free_streaming_interval=float(
            conformal_free_streaming_interval
        ),
        free_streaming_phase=float(phase),
        multipole_lmax_minus_one=float(
            multipole_lmax_minus_one
        ),
        multipole_lmax=float(multipole_lmax),
        estimated_tail_multipole_lmax_plus_one=float(
            estimated_tail
        ),
        recurrence_terminal_derivative=float(
            recurrence_derivative
        ),
        reduced_terminal_derivative=float(
            reduced_derivative
        ),
        derivative_identity_residual=float(identity_residual),
        bessel_terminal_relation_closed=closed,
        coupled_lmax_convergence_certified=False,
    )


def massless_neutrino_hierarchy_prefix_with_bessel_terminal_closure(
    *,
    wave_number_squared: float,
    conformal_free_streaming_interval: float,
    neutrino_anisotropic_stress: float,
    multipoles_l3_to_lmax: Sequence[float],
    closure_tolerance: float = 1.0e-12,
) -> MasslessNeutrinoClosedPrefixCertificate:
    """Close an exact finite hierarchy prefix with the Bessel tail."""

    multipoles = tuple(
        float(value) for value in multipoles_l3_to_lmax
    )
    if not multipoles:
        raise ValueError(
            "at least the neutrino octupole F_3 is required"
        )
    for index, value in enumerate(multipoles):
        if not math.isfinite(value):
            raise ValueError(
                f"multipoles_l3_to_lmax[{index}] must be finite"
            )
    if not math.isfinite(neutrino_anisotropic_stress):
        raise ValueError(
            "neutrino_anisotropic_stress must be finite"
        )

    l_max = len(multipoles) + 2
    f_lmax = multipoles[-1]
    f_lmax_minus_one = (
        multipoles[-2]
        if len(multipoles) >= 2
        else 2.0 * neutrino_anisotropic_stress
    )

    terminal = massless_neutrino_bessel_terminal_closure(
        wave_number_squared=wave_number_squared,
        conformal_free_streaming_interval=(
            conformal_free_streaming_interval
        ),
        l_max=l_max,
        multipole_lmax_minus_one=f_lmax_minus_one,
        multipole_lmax=f_lmax,
        closure_tolerance=closure_tolerance,
    )
    prefix = massless_neutrino_hierarchy_prefix(
        wave_number_squared=wave_number_squared,
        neutrino_anisotropic_stress=(
            neutrino_anisotropic_stress
        ),
        multipoles_l3_to_lmax=multipoles,
        tail_multipole_lmax_plus_one=(
            terminal.estimated_tail_multipole_lmax_plus_one
        ),
        closure_tolerance=closure_tolerance,
    )

    terminal_derivative_residual = (
        prefix.derivatives_l3_to_lmax[-1]
        - terminal.recurrence_terminal_derivative
    )
    derivative_scale = max(
        1.0,
        abs(prefix.derivatives_l3_to_lmax[-1]),
        abs(terminal.recurrence_terminal_derivative),
    )
    derivative_agreement = (
        abs(terminal_derivative_residual)
        <= closure_tolerance * derivative_scale
    )

    finite_closed = bool(
        terminal.bessel_terminal_relation_closed
        and prefix.finite_prefix_closed
        and derivative_agreement
    )

    return MasslessNeutrinoClosedPrefixCertificate(
        terminal_closure=terminal,
        hierarchy_prefix=prefix,
        finite_hierarchy_algebraically_closed=finite_closed,
        coupled_lmax_convergence_certified=False,
        physical_mode_integration_run=False,
    )
