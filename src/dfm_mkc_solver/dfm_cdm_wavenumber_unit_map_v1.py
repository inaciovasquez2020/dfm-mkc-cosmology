"""Physical wavenumber map for the H0-normalized DFM-as-CDM branch.

The DFM-CDM background uses dimensionless code units with ``H0_code = 1``.
Restoring the speed of light gives the comoving length unit

    L_H = c / H0,

so a physical comoving wavenumber and length map to code units as

    k_code = k_Mpc^-1 * c / H0,
    L_code = L_Mpc * H0 / c.

For the common ``h Mpc^-1`` wavenumber convention, with ``h = H0/100``,

    k_code = k_(h/Mpc) * c / 100.

This module certifies only the unit conversion.  It does not construct a
primordial power spectrum, a transfer function, sigma8, f sigma8, a survey
window projection, or an observational likelihood.
"""

from __future__ import annotations

import math
from dataclasses import dataclass

from .charge_reduced_background_v1 import SPEED_OF_LIGHT_KM_S


def _require_finite_positive(name: str, value: float) -> float:
    value = float(value)
    if not math.isfinite(value) or value <= 0.0:
        raise ValueError(f"{name} must be finite and positive")
    return value


def _require_finite_nonnegative(name: str, value: float) -> float:
    value = float(value)
    if not math.isfinite(value) or value < 0.0:
        raise ValueError(f"{name} must be finite and nonnegative")
    return value


@dataclass(frozen=True)
class DFMCDMWavenumberUnitMap:
    """Convert comoving lengths and wavenumbers to H0-normalized code units."""

    H0_km_s_Mpc: float
    speed_of_light_km_s: float = SPEED_OF_LIGHT_KM_S

    def __post_init__(self) -> None:
        _require_finite_positive("H0_km_s_Mpc", self.H0_km_s_Mpc)
        _require_finite_positive(
            "speed_of_light_km_s",
            self.speed_of_light_km_s,
        )

    @property
    def h(self) -> float:
        return self.H0_km_s_Mpc / 100.0

    @property
    def hubble_length_Mpc(self) -> float:
        return self.speed_of_light_km_s / self.H0_km_s_Mpc

    @property
    def r8_Mpc(self) -> float:
        """Return 8 h^-1 Mpc in physical comoving Mpc."""
        return 8.0 / self.h

    @property
    def r8_code(self) -> float:
        """Return the sigma8 top-hat radius in H0-normalized code length."""
        return self.length_code_from_Mpc(self.r8_Mpc)

    def wavenumber_code_from_Mpc_inverse(self, value: float) -> float:
        value = _require_finite_nonnegative("wavenumber_Mpc_inverse", value)
        return value * self.hubble_length_Mpc

    def wavenumber_Mpc_inverse_from_code(self, value: float) -> float:
        value = _require_finite_nonnegative("wavenumber_code", value)
        return value / self.hubble_length_Mpc

    def wavenumber_code_from_h_Mpc_inverse(self, value: float) -> float:
        value = _require_finite_nonnegative(
            "wavenumber_h_Mpc_inverse",
            value,
        )
        return self.wavenumber_code_from_Mpc_inverse(value * self.h)

    def wavenumber_h_Mpc_inverse_from_code(self, value: float) -> float:
        return self.wavenumber_Mpc_inverse_from_code(value) / self.h

    def length_code_from_Mpc(self, value: float) -> float:
        value = _require_finite_positive("length_Mpc", value)
        return value / self.hubble_length_Mpc

    def length_Mpc_from_code(self, value: float) -> float:
        value = _require_finite_positive("length_code", value)
        return value * self.hubble_length_Mpc


def build_dfm_cdm_wavenumber_unit_map(
    *,
    H0_km_s_Mpc: float,
) -> DFMCDMWavenumberUnitMap:
    """Build the physical/code wavenumber conversion for one H0 value."""
    return DFMCDMWavenumberUnitMap(H0_km_s_Mpc=H0_km_s_Mpc)
