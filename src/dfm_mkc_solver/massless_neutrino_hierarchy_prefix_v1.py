"""Exact finite prefix of the collisionless massless-neutrino hierarchy.

For multipoles F_l with l >= 3, the conformal-Newtonian collisionless
recurrence is

    F_l' = k / (2 l + 1) [l F_{l-1} - (l + 1) F_{l+1}].

The relation F_2 = 2 sigma_nu matches the neutrino shear convention used by
``radiation_species_coupled_fourier_rhs_v1``.

This module deliberately requires the terminal value F_{l_max+1} as an
explicit input. It therefore closes the exact finite prefix but does not
claim that the infinite hierarchy has been truncated accurately.
"""

from __future__ import annotations

from dataclasses import dataclass
import math
from typing import Sequence

from .radiation_species_coupled_fourier_rhs_v1 import (
    RadiationSpeciesCoupledFourierRightHandSideCertificate,
    radiation_species_coupled_fourier_right_hand_side_k_squared,
)


@dataclass(frozen=True)
class MasslessNeutrinoHierarchyPrefix:
    l_max: int
    multipoles_l3_to_lmax: tuple[float, ...]
    tail_multipole_lmax_plus_one: float
    derivatives_l3_to_lmax: tuple[float, ...]
    recurrence_residuals_l3_to_lmax: tuple[float, ...]
    maximum_recurrence_residual: float
    finite_prefix_closed: bool
    terminal_tail_evolution_supplied: bool
    infinite_hierarchy_closed: bool


@dataclass(frozen=True)
class RadiationSpeciesHierarchyPrefixCertificate:
    species_rhs: RadiationSpeciesCoupledFourierRightHandSideCertificate
    neutrino_hierarchy: MasslessNeutrinoHierarchyPrefix
    coupled_prefix_closed: bool
    physical_radiation_microphysics_closed: bool
    physical_mode_integration_run: bool


def _finite_tuple(
    name: str,
    values: Sequence[float],
) -> tuple[float, ...]:
    result = tuple(float(value) for value in values)
    for index, value in enumerate(result):
        if not math.isfinite(value):
            raise ValueError(f"{name}[{index}] must be finite")
    return result


def massless_neutrino_hierarchy_prefix(
    *,
    wave_number_squared: float,
    neutrino_anisotropic_stress: float,
    multipoles_l3_to_lmax: Sequence[float],
    tail_multipole_lmax_plus_one: float,
    closure_tolerance: float = 1.0e-12,
) -> MasslessNeutrinoHierarchyPrefix:
    """Evaluate the exact recurrence for l=3,...,l_max."""

    for name, value in (
        ("wave_number_squared", wave_number_squared),
        (
            "neutrino_anisotropic_stress",
            neutrino_anisotropic_stress,
        ),
        (
            "tail_multipole_lmax_plus_one",
            tail_multipole_lmax_plus_one,
        ),
        ("closure_tolerance", closure_tolerance),
    ):
        if not math.isfinite(value):
            raise ValueError(f"{name} must be finite")

    if wave_number_squared <= 0.0:
        raise ValueError("wave_number_squared must be positive")
    if closure_tolerance < 0.0:
        raise ValueError("closure_tolerance must be nonnegative")

    multipoles = _finite_tuple(
        "multipoles_l3_to_lmax",
        multipoles_l3_to_lmax,
    )
    if not multipoles:
        raise ValueError(
            "at least the neutrino octupole F_3 is required"
        )

    wave_number = math.sqrt(wave_number_squared)
    l_max = len(multipoles) + 2
    f2 = 2.0 * neutrino_anisotropic_stress

    derivatives: list[float] = []
    residuals: list[float] = []

    for ell in range(3, l_max + 1):
        f_l_minus_one = (
            f2
            if ell == 3
            else multipoles[ell - 4]
        )
        f_l_plus_one = (
            multipoles[ell - 2]
            if ell < l_max
            else tail_multipole_lmax_plus_one
        )
        derivative = (
            wave_number
            / (2.0 * ell + 1.0)
            * (
                ell * f_l_minus_one
                - (ell + 1.0) * f_l_plus_one
            )
        )
        residual = (
            derivative
            - wave_number
            / (2.0 * ell + 1.0)
            * (
                ell * f_l_minus_one
                - (ell + 1.0) * f_l_plus_one
            )
        )
        derivatives.append(float(derivative))
        residuals.append(float(residual))

    maximum_residual = max(abs(value) for value in residuals)
    finite_prefix_closed = (
        maximum_residual <= closure_tolerance
    )

    return MasslessNeutrinoHierarchyPrefix(
        l_max=l_max,
        multipoles_l3_to_lmax=multipoles,
        tail_multipole_lmax_plus_one=float(
            tail_multipole_lmax_plus_one
        ),
        derivatives_l3_to_lmax=tuple(derivatives),
        recurrence_residuals_l3_to_lmax=tuple(residuals),
        maximum_recurrence_residual=float(maximum_residual),
        finite_prefix_closed=finite_prefix_closed,
        terminal_tail_evolution_supplied=False,
        infinite_hierarchy_closed=False,
    )


def radiation_species_with_neutrino_hierarchy_prefix_k_squared(
    *,
    multipoles_l3_to_lmax: Sequence[float],
    tail_multipole_lmax_plus_one: float,
    closure_tolerance: float = 1.0e-10,
    **species_inputs: float,
) -> RadiationSpeciesHierarchyPrefixCertificate:
    """Couple an exact neutrino hierarchy prefix to the species RHS."""

    if "wave_number_squared" not in species_inputs:
        raise ValueError("wave_number_squared is required")
    if "neutrino_anisotropic_stress" not in species_inputs:
        raise ValueError(
            "neutrino_anisotropic_stress is required"
        )

    multipoles = _finite_tuple(
        "multipoles_l3_to_lmax",
        multipoles_l3_to_lmax,
    )
    if not multipoles:
        raise ValueError(
            "at least the neutrino octupole F_3 is required"
        )

    species_arguments = dict(species_inputs)
    species_arguments["neutrino_octupole"] = multipoles[0]
    species_arguments["closure_tolerance"] = closure_tolerance

    species_rhs = (
        radiation_species_coupled_fourier_right_hand_side_k_squared(
            **species_arguments
        )
    )
    hierarchy = massless_neutrino_hierarchy_prefix(
        wave_number_squared=float(
            species_inputs["wave_number_squared"]
        ),
        neutrino_anisotropic_stress=float(
            species_inputs["neutrino_anisotropic_stress"]
        ),
        multipoles_l3_to_lmax=multipoles,
        tail_multipole_lmax_plus_one=(
            tail_multipole_lmax_plus_one
        ),
        closure_tolerance=closure_tolerance,
    )

    coupled_prefix_closed = (
        species_rhs.species_rhs_closed
        and hierarchy.finite_prefix_closed
    )

    return RadiationSpeciesHierarchyPrefixCertificate(
        species_rhs=species_rhs,
        neutrino_hierarchy=hierarchy,
        coupled_prefix_closed=coupled_prefix_closed,
        physical_radiation_microphysics_closed=False,
        physical_mode_integration_run=False,
    )
