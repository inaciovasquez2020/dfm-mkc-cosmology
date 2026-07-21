"""Time-dependent averaged-versus-full-field growth comparison.

This module removes the fixed-background limitation by composing:

* the charge-reduced homogeneous carrier-field evolution;
* the action-derived Fourier perturbation right-hand side;
* the conditional averaged-to-full-field initial matching surface;
* phase-cycle averaging of the full-field density contrast;
* the averaged matter-era growth calculation.

The initial perturbation slice remains conditional on the pressureless,
phase-current-locked matching prescription. The result is not an
observationally calibrated matter-power prediction.
"""

from __future__ import annotations

import math
from dataclasses import dataclass

import numpy as np
from scipy.integrate import solve_ivp

from .averaged_full_field_metric_fixed_point_v1 import (
    solve_initial_metric_fixed_point,
)
from .charge_perturbed_zero_velocity_matching_v1 import (
    solve_charge_perturbed_zero_velocity_matching,
)
from .averaged_matter_growth_suppression_v1 import (
    integrate_averaged_matter_growth_suppression,
)
from .charge_reduced_background_v1 import (
    ChargeReducedInitialData,
    ChargeReducedParameters,
    ChargeReducedSolverConfig,
    solve_charge_reduced_background,
)
from .dark_sector_fourier_rhs_v1 import (
    DarkSectorFourierRightHandSideCertificate,
    dark_sector_fourier_right_hand_side,
)

State4 = tuple[float, float, float, float]


@dataclass(frozen=True)
class AveragedFullFieldTimeDependentComparisonCertificate:
    log_scale_factors: tuple[float, ...]
    scale_factors: tuple[float, ...]
    carrier_phases: tuple[float, ...]
    full_field_states: tuple[State4, ...]
    instantaneous_density_contrasts: tuple[float, ...]
    initial_cycle_average: float
    final_cycle_average: float
    full_field_growth_factor: float
    averaged_growth_factor: float
    full_to_averaged_growth_ratio: float
    relative_growth_difference: float
    initial_cycle_midpoint_scale_factor: float
    final_cycle_midpoint_scale_factor: float
    phase_span: float
    cycle_width: float
    maximum_rhs_residual: float
    minimum_abs_constraint_denominator: float
    initial_matching_surface_closed: bool
    initial_metric_fixed_point_solved: bool
    time_dependent_background_evolved: bool
    time_dependent_full_field_evolved: bool
    metric_constraints_solved_at_each_sample: bool
    phase_cycle_averaging_computed: bool
    averaged_full_field_comparison_computed: bool
    observational_calibration_completed: bool


def _require_finite(name: str, value: float) -> None:
    if not math.isfinite(value):
        raise ValueError(f"{name} must be finite")


def _interpolate(
    log_scale_factor: float,
    grid: np.ndarray,
    values: np.ndarray,
) -> float:
    return float(np.interp(log_scale_factor, grid, values))


def _rhs_residual(
    certificate: DarkSectorFourierRightHandSideCertificate,
) -> float:
    return max(
        abs(certificate.density_reconstruction_residual),
        abs(certificate.metric_closure_residual),
        abs(certificate.metric_constraints.poisson_residual),
        abs(certificate.metric_constraints.momentum_residual),
        abs(certificate.metric_constraints.anisotropy_residual),
        abs(
            certificate
            .amplitude_equation
            .amplitude_equation_residual
        ),
        abs(
            certificate
            .phase_equation
            .normalized_equation_residual
        ),
    )


def _cycle_average(
    phase: np.ndarray,
    values: np.ndarray,
    phase_lower: float,
    phase_upper: float,
) -> float:
    if phase_upper <= phase_lower:
        raise ValueError("phase_upper must exceed phase_lower")
    if phase_lower < phase[0] or phase_upper > phase[-1]:
        raise ValueError("cycle interval lies outside the phase grid")

    interior = (phase > phase_lower) & (phase < phase_upper)
    phase_segment = np.concatenate(
        (
            np.asarray([phase_lower]),
            phase[interior],
            np.asarray([phase_upper]),
        )
    )
    value_segment = np.interp(phase_segment, phase, values)

    integral = float(
        np.sum(
            0.5
            * (value_segment[1:] + value_segment[:-1])
            * np.diff(phase_segment)
        )
    )
    return integral / (phase_upper - phase_lower)


def compare_averaged_and_time_dependent_full_field_growth(
    *,
    parameters: ChargeReducedParameters,
    initial_data: ChargeReducedInitialData,
    config: ChargeReducedSolverConfig,
    wave_number: float,
    target_density_contrast: float = 1.0e-6,
    target_density_contrast_n: float = 1.0e-6,
    cycle_count: int = 1,
    denominator_tolerance: float = 1.0e-14,
    perturbation_rtol: float = 1.0e-8,
    perturbation_atol: float = 1.0e-10,
) -> AveragedFullFieldTimeDependentComparisonCertificate:
    """Evolve and compare one averaged and one full-field growth mode."""
    for name, value in (
        ("wave_number", wave_number),
        ("target_density_contrast", target_density_contrast),
        ("target_density_contrast_n", target_density_contrast_n),
        ("denominator_tolerance", denominator_tolerance),
        ("perturbation_rtol", perturbation_rtol),
        ("perturbation_atol", perturbation_atol),
    ):
        _require_finite(name, value)

    if wave_number <= 0.0:
        raise ValueError("wave_number must be positive")
    if isinstance(cycle_count, bool) or not isinstance(cycle_count, int):
        raise TypeError("cycle_count must be an integer")
    if cycle_count <= 0:
        raise ValueError("cycle_count must be positive")
    if denominator_tolerance <= 0.0:
        raise ValueError("denominator_tolerance must be positive")
    if perturbation_rtol <= 0.0 or perturbation_atol <= 0.0:
        raise ValueError("perturbation tolerances must be positive")
    if parameters.m_phi_squared <= 0.0:
        raise ValueError(
            "m_phi_squared must be positive for the averaged comparison"
        )

    background = solve_charge_reduced_background(
        parameters=parameters,
        initial_data=initial_data,
        config=config,
    )
    if not background.success:
        raise RuntimeError(background.message)
    if not (
        float(background.N[0])
        <= 0.0
        <= float(background.N[-1])
    ):
        raise ValueError(
            "background interval must contain N = 0 for H(a=1)"
        )
    if np.min(np.abs(background.phi)) <= denominator_tolerance:
        raise ValueError("carrier amplitude crosses zero")

    scale_factor_initial = float(background.a[0])
    conformal_hubble_initial = (
        scale_factor_initial * float(background.H[0])
    )
    phi_prime_initial = (
        scale_factor_initial * float(background.v[0])
    )
    theta_prime_initial = (
        scale_factor_initial * float(background.theta_dot[0])
    )

    if phi_prime_initial == 0.0:
        zero_velocity_matching = (
            solve_charge_perturbed_zero_velocity_matching(
                scale_factor=scale_factor_initial,
                conformal_hubble=conformal_hubble_initial,
                wave_number=wave_number,
                gravitational_constant=parameters.G,
                phi_background=float(background.phi[0]),
                phi_prime_background=phi_prime_initial,
                theta_prime_background=theta_prime_initial,
                target_density_contrast=target_density_contrast,
                alpha=parameters.alpha,
                beta=parameters.beta,
                rho_star=parameters.rho_star,
                m_phi_squared=parameters.m_phi_squared,
                lambda_phi=parameters.lambda_phi,
            )
        )
        initial_state = zero_velocity_matching.initial_state
        initial_matching_surface_closed = (
            zero_velocity_matching.matching_surface_closed
        )
        initial_metric_fixed_point_solved = (
            zero_velocity_matching.metric_constraints_solved
            and zero_velocity_matching.instantaneous_rhs_closed
        )
    else:
        fixed_point = solve_initial_metric_fixed_point(
            scale_factor=scale_factor_initial,
            conformal_hubble=conformal_hubble_initial,
            wave_number=wave_number,
            gravitational_constant=parameters.G,
            phi_background=float(background.phi[0]),
            phi_prime_background=phi_prime_initial,
            theta_prime_background=theta_prime_initial,
            target_density_contrast=target_density_contrast,
            target_density_contrast_n=target_density_contrast_n,
            alpha=parameters.alpha,
            beta=parameters.beta,
            rho_star=parameters.rho_star,
            m_phi_squared=parameters.m_phi_squared,
            lambda_phi=parameters.lambda_phi,
            denominator_tolerance=denominator_tolerance,
        )
        if not fixed_point.initial_metric_fixed_point_solved:
            raise RuntimeError(
                "initial metric fixed-point matching did not close"
            )
        initial_state = fixed_point.initial_state
        initial_matching_surface_closed = (
            fixed_point.matching_surface_closed
        )
        initial_metric_fixed_point_solved = (
            fixed_point.initial_metric_fixed_point_solved
        )

    def evaluate(
        log_scale_factor: float,
        state: np.ndarray,
    ) -> tuple[
        np.ndarray,
        DarkSectorFourierRightHandSideCertificate,
    ]:
        scale_factor = math.exp(log_scale_factor)
        hubble = _interpolate(
            log_scale_factor,
            background.N,
            background.H,
        )
        conformal_hubble = scale_factor * hubble
        if conformal_hubble <= 0.0:
            raise ValueError(
                "conformal Hubble rate must remain positive"
            )

        phi_background = _interpolate(
            log_scale_factor,
            background.N,
            background.phi,
        )
        phi_prime_background = (
            scale_factor
            * _interpolate(
                log_scale_factor,
                background.N,
                background.v,
            )
        )
        theta_prime_background = (
            scale_factor
            * _interpolate(
                log_scale_factor,
                background.N,
                background.theta_dot,
            )
        )

        certificate = dark_sector_fourier_right_hand_side(
            scale_factor=scale_factor,
            conformal_hubble=conformal_hubble,
            wave_number=wave_number,
            gravitational_constant=parameters.G,
            phi_background=phi_background,
            phi_prime_background=phi_prime_background,
            theta_prime_background=theta_prime_background,
            delta_phi=float(state[0]),
            delta_phi_prime=float(state[1]),
            delta_theta=float(state[2]),
            delta_theta_prime=float(state[3]),
            alpha=parameters.alpha,
            beta=parameters.beta,
            rho_star=parameters.rho_star,
            m_phi_squared=parameters.m_phi_squared,
            lambda_phi=parameters.lambda_phi,
            denominator_tolerance=denominator_tolerance,
        )

        derivative = np.asarray(
            [
                state[1] / conformal_hubble,
                certificate.delta_phi_double_prime
                / conformal_hubble,
                state[3] / conformal_hubble,
                certificate.delta_theta_double_prime
                / conformal_hubble,
            ],
            dtype=float,
        )
        if not np.all(np.isfinite(derivative)):
            raise ValueError(
                "full-field derivative became nonfinite"
            )
        return derivative, certificate

    perturbation_grid = np.asarray(
        background.N,
        dtype=float,
    )
    perturbation_grid_steps = np.diff(
        perturbation_grid
    )

    if (
        perturbation_grid.ndim != 1
        or perturbation_grid.size < 2
        or np.any(perturbation_grid_steps <= 0.0)
    ):
        raise ValueError(
            "background log-scale-factor grid must be "
            "strictly increasing"
        )

    minimum_grid_step = float(
        np.min(perturbation_grid_steps)
    )

    integration = solve_ivp(
        lambda log_scale_factor, state: evaluate(
            log_scale_factor,
            state,
        )[0],
        (
            float(perturbation_grid[0]),
            float(perturbation_grid[-1]),
        ),
        np.asarray(initial_state, dtype=float),
        t_eval=perturbation_grid,
        method="DOP853",
        rtol=min(perturbation_rtol, 1.0e-11),
        atol=min(perturbation_atol, 1.0e-13),
        max_step=minimum_grid_step / 2.0,
    )
    if not integration.success:
        raise RuntimeError(
            "time-dependent full-field integration failed: "
            f"{integration.message}"
        )

    density_contrasts: list[float] = []
    maximum_rhs_residual = 0.0
    minimum_abs_constraint_denominator = math.inf
    all_metric_constraints_closed = True

    for index, log_scale_factor in enumerate(integration.t):
        state = integration.y[:, index]
        _, certificate = evaluate(
            float(log_scale_factor),
            state,
        )
        background_density = (
            certificate.stress_energy.background_energy_density
        )
        if background_density <= 0.0:
            raise ValueError(
                "full-field background density must remain positive"
            )

        density_contrast = (
            certificate.stress_energy.delta_energy_density
            / background_density
        )
        _require_finite("density_contrast", density_contrast)
        density_contrasts.append(density_contrast)

        maximum_rhs_residual = max(
            maximum_rhs_residual,
            _rhs_residual(certificate),
        )
        minimum_abs_constraint_denominator = min(
            minimum_abs_constraint_denominator,
            abs(certificate.constraint_denominator),
        )
        all_metric_constraints_closed = (
            all_metric_constraints_closed
            and certificate.instantaneous_dark_sector_rhs_closed
        )

    raw_phase = np.asarray(background.theta, dtype=float)
    phase_direction = (
        1.0 if raw_phase[-1] > raw_phase[0] else -1.0
    )
    phase = phase_direction * raw_phase
    if np.any(np.diff(phase) <= 0.0):
        raise ValueError("carrier phase must be strictly monotone")

    density_array = np.asarray(density_contrasts, dtype=float)
    cycle_width = 2.0 * math.pi * cycle_count
    phase_span = float(phase[-1] - phase[0])
    if phase_span < cycle_width:
        raise ValueError(
            "background does not contain the requested "
            "complete phase cycle"
        )

    initial_phase_lower = float(phase[0])
    initial_phase_upper = initial_phase_lower + cycle_width
    final_phase_upper = float(phase[-1])
    final_phase_lower = final_phase_upper - cycle_width

    initial_cycle_average = _cycle_average(
        phase,
        density_array,
        initial_phase_lower,
        initial_phase_upper,
    )
    final_cycle_average = _cycle_average(
        phase,
        density_array,
        final_phase_lower,
        final_phase_upper,
    )

    if abs(initial_cycle_average) <= denominator_tolerance:
        raise ValueError(
            "initial cycle average is numerically zero"
        )

    full_field_growth_factor = (
        final_cycle_average / initial_cycle_average
    )

    initial_phase_midpoint = 0.5 * (
        initial_phase_lower + initial_phase_upper
    )
    final_phase_midpoint = 0.5 * (
        final_phase_lower + final_phase_upper
    )
    initial_cycle_midpoint_n = float(
        np.interp(
            initial_phase_midpoint,
            phase,
            background.N,
        )
    )
    final_cycle_midpoint_n = float(
        np.interp(
            final_phase_midpoint,
            phase,
            background.N,
        )
    )
    initial_cycle_midpoint_scale_factor = math.exp(
        initial_cycle_midpoint_n
    )
    final_cycle_midpoint_scale_factor = math.exp(
        final_cycle_midpoint_n
    )

    if (
        final_cycle_midpoint_scale_factor
        <= initial_cycle_midpoint_scale_factor
    ):
        raise ValueError(
            "cycle midpoint scale factors are not time ordered"
        )

    hubble_at_unit_scale_factor = _interpolate(
        0.0,
        background.N,
        background.H,
    )
    mass_frequency = math.sqrt(
        parameters.m_phi_squared / parameters.alpha
    )

    averaged = integrate_averaged_matter_growth_suppression(
        scale_factor_initial=(
            initial_cycle_midpoint_scale_factor
        ),
        scale_factor_final=(
            final_cycle_midpoint_scale_factor
        ),
        steps=max(512, config.samples - 1),
        wave_number=wave_number,
        mass_frequency=mass_frequency,
        hubble_at_unit_scale_factor=(
            hubble_at_unit_scale_factor
        ),
        gravitational_constant=parameters.G,
    )
    averaged_growth_factor = averaged.final_dfm_growth
    if abs(averaged_growth_factor) <= denominator_tolerance:
        raise ValueError(
            "averaged growth factor is numerically zero"
        )

    full_to_averaged_growth_ratio = (
        full_field_growth_factor / averaged_growth_factor
    )
    relative_growth_difference = (
        full_to_averaged_growth_ratio - 1.0
    )

    for name, value in (
        ("initial_cycle_average", initial_cycle_average),
        ("final_cycle_average", final_cycle_average),
        ("full_field_growth_factor", full_field_growth_factor),
        ("averaged_growth_factor", averaged_growth_factor),
        (
            "full_to_averaged_growth_ratio",
            full_to_averaged_growth_ratio,
        ),
        (
            "relative_growth_difference",
            relative_growth_difference,
        ),
        ("phase_span", phase_span),
        ("cycle_width", cycle_width),
        ("maximum_rhs_residual", maximum_rhs_residual),
        (
            "minimum_abs_constraint_denominator",
            minimum_abs_constraint_denominator,
        ),
    ):
        _require_finite(name, value)

    states: tuple[State4, ...] = tuple(
        (
            float(integration.y[0, index]),
            float(integration.y[1, index]),
            float(integration.y[2, index]),
            float(integration.y[3, index]),
        )
        for index in range(integration.y.shape[1])
    )

    return AveragedFullFieldTimeDependentComparisonCertificate(
        log_scale_factors=tuple(
            float(value) for value in integration.t
        ),
        scale_factors=tuple(
            math.exp(float(value))
            for value in integration.t
        ),
        carrier_phases=tuple(
            float(value) for value in raw_phase
        ),
        full_field_states=states,
        instantaneous_density_contrasts=tuple(
            density_contrasts
        ),
        initial_cycle_average=initial_cycle_average,
        final_cycle_average=final_cycle_average,
        full_field_growth_factor=full_field_growth_factor,
        averaged_growth_factor=averaged_growth_factor,
        full_to_averaged_growth_ratio=(
            full_to_averaged_growth_ratio
        ),
        relative_growth_difference=(
            relative_growth_difference
        ),
        initial_cycle_midpoint_scale_factor=(
            initial_cycle_midpoint_scale_factor
        ),
        final_cycle_midpoint_scale_factor=(
            final_cycle_midpoint_scale_factor
        ),
        phase_span=phase_span,
        cycle_width=cycle_width,
        maximum_rhs_residual=maximum_rhs_residual,
        minimum_abs_constraint_denominator=(
            minimum_abs_constraint_denominator
        ),
        initial_matching_surface_closed=(
            initial_matching_surface_closed
        ),
        initial_metric_fixed_point_solved=(
            initial_metric_fixed_point_solved
        ),
        time_dependent_background_evolved=True,
        time_dependent_full_field_evolved=True,
        metric_constraints_solved_at_each_sample=(
            all_metric_constraints_closed
        ),
        phase_cycle_averaging_computed=True,
        averaged_full_field_comparison_computed=True,
        observational_calibration_completed=False,
    )
