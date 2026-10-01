"""Scalar photon polarization hierarchy in the repository photon convention.

The intensity variables use
    delta_gamma = 4 Theta_0
    theta_gamma = 3 k Theta_1

and the scalar E-mode multipoles are normalized so that the Thomson
polarization source is

    Pi = Theta_2 + 6 E_2.

For scalar modes there is no B-mode hierarchy.  This module supplies only
the polarization hierarchy and its Thomson collision source; recombination
and the time-dependent opacity remain separate physical-microphysics inputs.
"""

from __future__ import annotations

from dataclasses import dataclass
import math


@dataclass(frozen=True)
class PhotonPolarizationHierarchyStep:
    theta_ell_prime: float
    e_ell_prime: float


def _finite(name: str, value: float) -> None:
    if not math.isfinite(value):
        raise ValueError(f"{name} must be finite")


def photon_scalar_polarization_step(
    *,
    ell: int,
    wave_number: float,
    thomson_scattering_rate: float,
    theta_ell_minus_1: float,
    theta_ell: float,
    theta_ell_plus_1: float,
    e_ell_minus_1: float,
    e_ell: float,
    e_ell_plus_1: float,
    theta_2: float,
    e_2: float,
) -> PhotonPolarizationHierarchyStep:
    """Advance one scalar intensity/E-polarization multipole."""

    if ell < 2:
        raise ValueError("ell must be at least 2")
    for name, value in (
        ("wave_number", wave_number),
        ("thomson_scattering_rate", thomson_scattering_rate),
        ("theta_ell_minus_1", theta_ell_minus_1),
        ("theta_ell", theta_ell),
        ("theta_ell_plus_1", theta_ell_plus_1),
        ("e_ell_minus_1", e_ell_minus_1),
        ("e_ell", e_ell),
        ("e_ell_plus_1", e_ell_plus_1),
        ("theta_2", theta_2),
        ("e_2", e_2),
    ):
        _finite(name, value)
    if wave_number < 0.0:
        raise ValueError("wave_number must be nonnegative")
    if thomson_scattering_rate < 0.0:
        raise ValueError("thomson_scattering_rate must be nonnegative")

    k = wave_number
    Pi = theta_2 + 6.0 * e_2

    intensity_prime = (
        k
        / (2.0 * ell + 1.0)
        * (
            ell * theta_ell_minus_1
            - (ell + 1.0) * theta_ell_plus_1
        )
    )

    if ell == 2:
        intensity_prime += thomson_scattering_rate * (
            -theta_ell + Pi / 10.0
        )
        polarization_prime = (
            k / 5.0
            * (2.0 * e_ell_minus_1 - 3.0 * e_ell_plus_1)
            + thomson_scattering_rate * (
                -e_ell + Pi / 10.0
            )
        )
    else:
        intensity_prime -= thomson_scattering_rate * theta_ell
        polarization_prime = (
            k
            / (2.0 * ell + 1.0)
            * (
                ell * e_ell_minus_1
                - (ell + 1.0) * e_ell_plus_1
            )
            - thomson_scattering_rate * e_ell
        )

    return PhotonPolarizationHierarchyStep(
        theta_ell_prime=float(intensity_prime),
        e_ell_prime=float(polarization_prime),
    )
