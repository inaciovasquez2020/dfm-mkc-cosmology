"""Averaged quadratic DFM-MKC matter-era growth suppression.

This module evolves the cycle-averaged quadratic oscillatory branch with
N = ln(a). It does not evolve the instantaneous phi/theta carrier fields.

Equations:

    d rho / dN = -3 rho
    H^2 = (8 pi G / 3) rho

    delta_D,NN + (1/2) delta_D,N
      + [k^4 / (4 mu^2 a^4 H^2) - 3/2] delta_D = 0

    delta_C,NN + (1/2) delta_C,N - (3/2) delta_C = 0

Observable:

    S(k, a_f) = D_DFM(k, a_f) / D_CDM(a_f)
"""

from __future__ import annotations

import math
from dataclasses import dataclass


State5 = tuple[float, float, float, float, float]


@dataclass(frozen=True)
class AveragedMatterGrowthCertificate:
    scale_factor_initial: float
    scale_factor_final: float
    steps: int
    step_size: float
    wave_number: float
    mass_frequency: float
    hubble_at_unit_scale_factor: float
    gravitational_constant: float
    initial_state: State5
    final_state: State5
    final_dfm_growth: float
    final_cdm_growth: float
    final_growth_ratio: float
    final_growth_suppression: float
    final_pressure_to_gravity_ratio: float
    maximum_pressure_to_gravity_ratio: float
    maximum_relative_density_scaling_error: float
    maximum_relative_hubble_scaling_error: float
    maximum_friedmann_residual: float
    maximum_cdm_growing_mode_error: float
    all_values_finite: bool
    averaged_matter_background_evolved: bool
    averaged_dfm_growth_evolved: bool
    instantaneous_field_background_evolved: bool
    observable_computed: bool


def _require_finite(name: str, value: float) -> None:
    if not math.isfinite(value):
        raise ValueError(f"{name} must be finite")


def _add_scaled(
    state: State5,
    derivative: State5,
    scale: float,
) -> State5:
    return (
        state[0] + scale * derivative[0],
        state[1] + scale * derivative[1],
        state[2] + scale * derivative[2],
        state[3] + scale * derivative[3],
        state[4] + scale * derivative[4],
    )


def _rhs(
    log_scale_factor: float,
    state: State5,
    *,
    wave_number: float,
    mass_frequency: float,
    gravitational_constant: float,
) -> State5:
    density, dfm_delta, dfm_delta_n, cdm_delta, cdm_delta_n = state

    if density <= 0.0:
        raise ValueError("density must remain positive")

    scale_factor = math.exp(log_scale_factor)
    hubble_squared = (
        8.0 * math.pi * gravitational_constant * density / 3.0
    )
    pressure_term = (
        wave_number**4
        / (
            4.0
            * mass_frequency**2
            * scale_factor**4
            * hubble_squared
        )
    )

    return (
        -3.0 * density,
        dfm_delta_n,
        -0.5 * dfm_delta_n + (1.5 - pressure_term) * dfm_delta,
        cdm_delta_n,
        -0.5 * cdm_delta_n + 1.5 * cdm_delta,
    )


def _rk4_step(
    log_scale_factor: float,
    state: State5,
    step_size: float,
    *,
    wave_number: float,
    mass_frequency: float,
    gravitational_constant: float,
) -> State5:
    def evaluate(time: float, value: State5) -> State5:
        return _rhs(
            time,
            value,
            wave_number=wave_number,
            mass_frequency=mass_frequency,
            gravitational_constant=gravitational_constant,
        )

    k1 = evaluate(log_scale_factor, state)
    k2 = evaluate(
        log_scale_factor + 0.5 * step_size,
        _add_scaled(state, k1, 0.5 * step_size),
    )
    k3 = evaluate(
        log_scale_factor + 0.5 * step_size,
        _add_scaled(state, k2, 0.5 * step_size),
    )
    k4 = evaluate(
        log_scale_factor + step_size,
        _add_scaled(state, k3, step_size),
    )

    return (
        state[0] + step_size * (k1[0] + 2*k2[0] + 2*k3[0] + k4[0]) / 6.0,
        state[1] + step_size * (k1[1] + 2*k2[1] + 2*k3[1] + k4[1]) / 6.0,
        state[2] + step_size * (k1[2] + 2*k2[2] + 2*k3[2] + k4[2]) / 6.0,
        state[3] + step_size * (k1[3] + 2*k2[3] + 2*k3[3] + k4[3]) / 6.0,
        state[4] + step_size * (k1[4] + 2*k2[4] + 2*k3[4] + k4[4]) / 6.0,
    )


def integrate_averaged_matter_growth_suppression(
    *,
    scale_factor_initial: float,
    scale_factor_final: float,
    steps: int,
    wave_number: float,
    mass_frequency: float,
    hubble_at_unit_scale_factor: float,
    gravitational_constant: float,
) -> AveragedMatterGrowthCertificate:
    for name, value in (
        ("scale_factor_initial", scale_factor_initial),
        ("scale_factor_final", scale_factor_final),
        ("wave_number", wave_number),
        ("mass_frequency", mass_frequency),
        ("hubble_at_unit_scale_factor", hubble_at_unit_scale_factor),
        ("gravitational_constant", gravitational_constant),
    ):
        _require_finite(name, value)

    if scale_factor_initial <= 0.0:
        raise ValueError("scale_factor_initial must be positive")
    if scale_factor_final <= scale_factor_initial:
        raise ValueError(
            "scale_factor_final must exceed scale_factor_initial"
        )
    if steps <= 0:
        raise ValueError("steps must be positive")
    if wave_number < 0.0:
        raise ValueError("wave_number must be nonnegative")
    if mass_frequency <= 0.0:
        raise ValueError("mass_frequency must be positive")
    if hubble_at_unit_scale_factor <= 0.0:
        raise ValueError(
            "hubble_at_unit_scale_factor must be positive"
        )
    if gravitational_constant <= 0.0:
        raise ValueError("gravitational_constant must be positive")

    n_initial = math.log(scale_factor_initial)
    n_final = math.log(scale_factor_final)
    step_size = (n_final - n_initial) / steps

    density_at_unit_scale_factor = (
        3.0
        * hubble_at_unit_scale_factor**2
        / (8.0 * math.pi * gravitational_constant)
    )
    initial_density = (
        density_at_unit_scale_factor * scale_factor_initial**-3
    )
    initial_state: State5 = (
        initial_density,
        1.0,
        1.0,
        1.0,
        1.0,
    )

    log_scale_factor = n_initial
    state = initial_state

    max_density_error = 0.0
    max_hubble_error = 0.0
    max_friedmann_residual = 0.0
    max_cdm_error = 0.0
    max_pressure_ratio = 0.0
    final_pressure_ratio = 0.0
    all_values_finite = True

    def record() -> None:
        nonlocal max_density_error
        nonlocal max_hubble_error
        nonlocal max_friedmann_residual
        nonlocal max_cdm_error
        nonlocal max_pressure_ratio
        nonlocal final_pressure_ratio
        nonlocal all_values_finite

        density, _, _, cdm_delta, _ = state
        scale_factor = math.exp(log_scale_factor)
        hubble_squared = (
            8.0 * math.pi * gravitational_constant * density / 3.0
        )
        hubble = math.sqrt(hubble_squared)

        expected_density = (
            density_at_unit_scale_factor * scale_factor**-3
        )
        expected_hubble = (
            hubble_at_unit_scale_factor * scale_factor**-1.5
        )
        expected_cdm = scale_factor / scale_factor_initial

        max_density_error = max(
            max_density_error,
            abs(density - expected_density) / expected_density,
        )
        max_hubble_error = max(
            max_hubble_error,
            abs(hubble - expected_hubble) / expected_hubble,
        )
        max_friedmann_residual = max(
            max_friedmann_residual,
            abs(
                hubble_squared
                - 8.0
                * math.pi
                * gravitational_constant
                * density
                / 3.0
            ),
        )
        max_cdm_error = max(
            max_cdm_error,
            abs(cdm_delta - expected_cdm) / expected_cdm,
        )

        pressure_term = (
            wave_number**4
            / (
                4.0
                * mass_frequency**2
                * scale_factor**4
                * hubble_squared
            )
        )
        final_pressure_ratio = pressure_term / 1.5
        max_pressure_ratio = max(
            max_pressure_ratio,
            final_pressure_ratio,
        )

        all_values_finite = all_values_finite and all(
            math.isfinite(value) for value in state
        )

    record()

    for _ in range(steps):
        state = _rk4_step(
            log_scale_factor,
            state,
            step_size,
            wave_number=wave_number,
            mass_frequency=mass_frequency,
            gravitational_constant=gravitational_constant,
        )
        log_scale_factor += step_size
        record()

    final_dfm_growth = state[1]
    final_cdm_growth = state[3]

    if final_cdm_growth == 0.0:
        raise ValueError("final CDM growth must be nonzero")

    final_growth_ratio = final_dfm_growth / final_cdm_growth

    return AveragedMatterGrowthCertificate(
        scale_factor_initial=scale_factor_initial,
        scale_factor_final=scale_factor_final,
        steps=steps,
        step_size=step_size,
        wave_number=wave_number,
        mass_frequency=mass_frequency,
        hubble_at_unit_scale_factor=hubble_at_unit_scale_factor,
        gravitational_constant=gravitational_constant,
        initial_state=initial_state,
        final_state=state,
        final_dfm_growth=final_dfm_growth,
        final_cdm_growth=final_cdm_growth,
        final_growth_ratio=final_growth_ratio,
        final_growth_suppression=1.0 - final_growth_ratio,
        final_pressure_to_gravity_ratio=final_pressure_ratio,
        maximum_pressure_to_gravity_ratio=max_pressure_ratio,
        maximum_relative_density_scaling_error=max_density_error,
        maximum_relative_hubble_scaling_error=max_hubble_error,
        maximum_friedmann_residual=max_friedmann_residual,
        maximum_cdm_growing_mode_error=max_cdm_error,
        all_values_finite=all_values_finite,
        averaged_matter_background_evolved=True,
        averaged_dfm_growth_evolved=True,
        instantaneous_field_background_evolved=False,
        observable_computed=True,
    )
