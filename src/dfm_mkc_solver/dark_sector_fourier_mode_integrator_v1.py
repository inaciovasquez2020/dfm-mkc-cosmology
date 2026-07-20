"""Bounded fixed-background DFM-MKC Fourier-mode integration.

This module integrates the four-dimensional perturbation state

    y = (
        delta_phi,
        delta_phi_prime,
        delta_theta,
        delta_theta_prime,
    )

using the repository's closed instantaneous Fourier-mode right-hand side.

The background quantities are held fixed throughout each bounded run.
Classical fourth-order Runge-Kutta integration is used. A step-doubling
certificate compares N, 2N, and 4N-step integrations.

This is a numerical fixed-background mode diagnostic. It does not evolve
the cosmological background, visible species, recombination, a Boltzmann
hierarchy, transfer functions, or observables.
"""

from __future__ import annotations

import math
from dataclasses import dataclass
from typing import Optional

from .dark_sector_fourier_rhs_v1 import (
    DarkSectorFourierRightHandSideCertificate,
    dark_sector_fourier_right_hand_side,
)


State4 = tuple[float, float, float, float]


@dataclass(frozen=True)
class FourierModeIntegrationCertificate:
    conformal_time_start: float
    conformal_time_end: float
    steps: int
    step_size: float
    initial_state: State4
    final_state: State4
    times: tuple[float, ...]
    states: tuple[State4, ...]
    max_component_residual: float
    max_metric_potential_abs: float
    minimum_abs_constraint_denominator: float
    all_instantaneous_rhs_certificates_closed: bool
    fixed_background_integration_completed: bool
    cosmological_background_evolved: bool
    visible_sector_evolved: bool
    observable_computed: bool


@dataclass(frozen=True)
class FourierModeStepDoublingCertificate:
    coarse_steps: int
    medium_steps: int
    fine_steps: int
    coarse_medium_difference: float
    medium_fine_difference: float
    observed_order: Optional[float]
    convergence_improved: bool
    coarse: FourierModeIntegrationCertificate
    medium: FourierModeIntegrationCertificate
    fine: FourierModeIntegrationCertificate
    bounded_mode_convergence_certified: bool


def _require_finite(name: str, value: float) -> None:
    if not math.isfinite(value):
        raise ValueError(f"{name} must be finite")


def _state_add_scaled(
    state: State4,
    derivative: State4,
    scale: float,
) -> State4:
    return (
        state[0] + scale * derivative[0],
        state[1] + scale * derivative[1],
        state[2] + scale * derivative[2],
        state[3] + scale * derivative[3],
    )


def _state_rk4_update(
    state: State4,
    step_size: float,
    k1: State4,
    k2: State4,
    k3: State4,
    k4: State4,
) -> State4:
    factor = step_size / 6.0

    return (
        state[0]
        + factor
        * (
            k1[0]
            + 2.0 * k2[0]
            + 2.0 * k3[0]
            + k4[0]
        ),
        state[1]
        + factor
        * (
            k1[1]
            + 2.0 * k2[1]
            + 2.0 * k3[1]
            + k4[1]
        ),
        state[2]
        + factor
        * (
            k1[2]
            + 2.0 * k2[2]
            + 2.0 * k3[2]
            + k4[2]
        ),
        state[3]
        + factor
        * (
            k1[3]
            + 2.0 * k2[3]
            + 2.0 * k3[3]
            + k4[3]
        ),
    )


def _state_distance(left: State4, right: State4) -> float:
    return math.sqrt(
        sum(
            (left[index] - right[index]) ** 2
            for index in range(4)
        )
    )


def _certificate_component_residual(
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


def _evaluate_state(
    state: State4,
    *,
    scale_factor: float,
    conformal_hubble: float,
    wave_number: float,
    gravitational_constant: float,
    phi_background: float,
    phi_prime_background: float,
    theta_prime_background: float,
    alpha: float,
    beta: float,
    rho_star: float,
    m_phi_squared: float,
    lambda_phi: float,
    visible_delta_energy_density: float,
    visible_momentum_divergence_source: float,
    denominator_tolerance: float,
) -> tuple[
    State4,
    DarkSectorFourierRightHandSideCertificate,
]:
    certificate = dark_sector_fourier_right_hand_side(
        scale_factor=scale_factor,
        conformal_hubble=conformal_hubble,
        wave_number=wave_number,
        gravitational_constant=gravitational_constant,
        phi_background=phi_background,
        phi_prime_background=phi_prime_background,
        theta_prime_background=theta_prime_background,
        delta_phi=state[0],
        delta_phi_prime=state[1],
        delta_theta=state[2],
        delta_theta_prime=state[3],
        alpha=alpha,
        beta=beta,
        rho_star=rho_star,
        m_phi_squared=m_phi_squared,
        lambda_phi=lambda_phi,
        visible_delta_energy_density=(
            visible_delta_energy_density
        ),
        visible_momentum_divergence_source=(
            visible_momentum_divergence_source
        ),
        denominator_tolerance=denominator_tolerance,
    )

    derivative: State4 = (
        state[1],
        certificate.delta_phi_double_prime,
        state[3],
        certificate.delta_theta_double_prime,
    )

    return derivative, certificate


def integrate_dark_sector_fourier_mode(
    *,
    conformal_time_start: float,
    conformal_time_end: float,
    steps: int,
    initial_state: State4,
    scale_factor: float,
    conformal_hubble: float,
    wave_number: float,
    gravitational_constant: float,
    phi_background: float,
    phi_prime_background: float,
    theta_prime_background: float,
    alpha: float,
    beta: float,
    rho_star: float,
    m_phi_squared: float,
    lambda_phi: float,
    visible_delta_energy_density: float = 0.0,
    visible_momentum_divergence_source: float = 0.0,
    denominator_tolerance: float = 1.0e-14,
) -> FourierModeIntegrationCertificate:
    """Integrate one bounded fixed-background Fourier mode with RK4."""

    for name, value in (
        ("conformal_time_start", conformal_time_start),
        ("conformal_time_end", conformal_time_end),
        ("scale_factor", scale_factor),
        ("conformal_hubble", conformal_hubble),
        ("wave_number", wave_number),
        ("gravitational_constant", gravitational_constant),
        ("phi_background", phi_background),
        ("phi_prime_background", phi_prime_background),
        ("theta_prime_background", theta_prime_background),
        ("alpha", alpha),
        ("beta", beta),
        ("rho_star", rho_star),
        ("m_phi_squared", m_phi_squared),
        ("lambda_phi", lambda_phi),
        (
            "visible_delta_energy_density",
            visible_delta_energy_density,
        ),
        (
            "visible_momentum_divergence_source",
            visible_momentum_divergence_source,
        ),
        ("denominator_tolerance", denominator_tolerance),
    ):
        _require_finite(name, value)

    for index, value in enumerate(initial_state):
        _require_finite(f"initial_state[{index}]", value)

    if conformal_time_end <= conformal_time_start:
        raise ValueError(
            "conformal_time_end must exceed conformal_time_start"
        )
    if isinstance(steps, bool) or not isinstance(steps, int):
        raise TypeError("steps must be an integer")
    if steps <= 0:
        raise ValueError("steps must be positive")
    if scale_factor <= 0.0:
        raise ValueError("scale_factor must be positive")
    if wave_number <= 0.0:
        raise ValueError("wave_number must be positive")
    if gravitational_constant <= 0.0:
        raise ValueError(
            "gravitational_constant must be positive"
        )
    if phi_background == 0.0:
        raise ValueError("phi_background must be nonzero")
    if alpha <= 0.0:
        raise ValueError("alpha must be positive")
    if beta <= 0.0:
        raise ValueError("beta must be positive")
    if lambda_phi < 0.0:
        raise ValueError("lambda_phi must be nonnegative")
    if denominator_tolerance <= 0.0:
        raise ValueError(
            "denominator_tolerance must be positive"
        )

    step_size = (
        conformal_time_end - conformal_time_start
    ) / steps

    state = initial_state
    time = conformal_time_start

    times = [time]
    states = [state]

    _, initial_certificate = _evaluate_state(
        state,
        scale_factor=scale_factor,
        conformal_hubble=conformal_hubble,
        wave_number=wave_number,
        gravitational_constant=gravitational_constant,
        phi_background=phi_background,
        phi_prime_background=phi_prime_background,
        theta_prime_background=theta_prime_background,
        alpha=alpha,
        beta=beta,
        rho_star=rho_star,
        m_phi_squared=m_phi_squared,
        lambda_phi=lambda_phi,
        visible_delta_energy_density=(
            visible_delta_energy_density
        ),
        visible_momentum_divergence_source=(
            visible_momentum_divergence_source
        ),
        denominator_tolerance=denominator_tolerance,
    )

    max_component_residual = (
        _certificate_component_residual(initial_certificate)
    )
    max_metric_potential_abs = abs(
        initial_certificate.metric_potential
    )
    minimum_abs_constraint_denominator = abs(
        initial_certificate.constraint_denominator
    )
    all_closed = (
        initial_certificate
        .instantaneous_dark_sector_rhs_closed
    )

    for _ in range(steps):
        k1, _ = _evaluate_state(
            state,
            scale_factor=scale_factor,
            conformal_hubble=conformal_hubble,
            wave_number=wave_number,
            gravitational_constant=gravitational_constant,
            phi_background=phi_background,
            phi_prime_background=phi_prime_background,
            theta_prime_background=theta_prime_background,
            alpha=alpha,
            beta=beta,
            rho_star=rho_star,
            m_phi_squared=m_phi_squared,
            lambda_phi=lambda_phi,
            visible_delta_energy_density=(
                visible_delta_energy_density
            ),
            visible_momentum_divergence_source=(
                visible_momentum_divergence_source
            ),
            denominator_tolerance=denominator_tolerance,
        )

        stage_two = _state_add_scaled(
            state,
            k1,
            0.5 * step_size,
        )

        k2, _ = _evaluate_state(
            stage_two,
            scale_factor=scale_factor,
            conformal_hubble=conformal_hubble,
            wave_number=wave_number,
            gravitational_constant=gravitational_constant,
            phi_background=phi_background,
            phi_prime_background=phi_prime_background,
            theta_prime_background=theta_prime_background,
            alpha=alpha,
            beta=beta,
            rho_star=rho_star,
            m_phi_squared=m_phi_squared,
            lambda_phi=lambda_phi,
            visible_delta_energy_density=(
                visible_delta_energy_density
            ),
            visible_momentum_divergence_source=(
                visible_momentum_divergence_source
            ),
            denominator_tolerance=denominator_tolerance,
        )

        stage_three = _state_add_scaled(
            state,
            k2,
            0.5 * step_size,
        )

        k3, _ = _evaluate_state(
            stage_three,
            scale_factor=scale_factor,
            conformal_hubble=conformal_hubble,
            wave_number=wave_number,
            gravitational_constant=gravitational_constant,
            phi_background=phi_background,
            phi_prime_background=phi_prime_background,
            theta_prime_background=theta_prime_background,
            alpha=alpha,
            beta=beta,
            rho_star=rho_star,
            m_phi_squared=m_phi_squared,
            lambda_phi=lambda_phi,
            visible_delta_energy_density=(
                visible_delta_energy_density
            ),
            visible_momentum_divergence_source=(
                visible_momentum_divergence_source
            ),
            denominator_tolerance=denominator_tolerance,
        )

        stage_four = _state_add_scaled(
            state,
            k3,
            step_size,
        )

        k4, _ = _evaluate_state(
            stage_four,
            scale_factor=scale_factor,
            conformal_hubble=conformal_hubble,
            wave_number=wave_number,
            gravitational_constant=gravitational_constant,
            phi_background=phi_background,
            phi_prime_background=phi_prime_background,
            theta_prime_background=theta_prime_background,
            alpha=alpha,
            beta=beta,
            rho_star=rho_star,
            m_phi_squared=m_phi_squared,
            lambda_phi=lambda_phi,
            visible_delta_energy_density=(
                visible_delta_energy_density
            ),
            visible_momentum_divergence_source=(
                visible_momentum_divergence_source
            ),
            denominator_tolerance=denominator_tolerance,
        )

        state = _state_rk4_update(
            state,
            step_size,
            k1,
            k2,
            k3,
            k4,
        )

        for index, value in enumerate(state):
            _require_finite(f"state[{index}]", value)

        time += step_size

        _, accepted_certificate = _evaluate_state(
            state,
            scale_factor=scale_factor,
            conformal_hubble=conformal_hubble,
            wave_number=wave_number,
            gravitational_constant=gravitational_constant,
            phi_background=phi_background,
            phi_prime_background=phi_prime_background,
            theta_prime_background=theta_prime_background,
            alpha=alpha,
            beta=beta,
            rho_star=rho_star,
            m_phi_squared=m_phi_squared,
            lambda_phi=lambda_phi,
            visible_delta_energy_density=(
                visible_delta_energy_density
            ),
            visible_momentum_divergence_source=(
                visible_momentum_divergence_source
            ),
            denominator_tolerance=denominator_tolerance,
        )

        max_component_residual = max(
            max_component_residual,
            _certificate_component_residual(
                accepted_certificate
            ),
        )
        max_metric_potential_abs = max(
            max_metric_potential_abs,
            abs(accepted_certificate.metric_potential),
        )
        minimum_abs_constraint_denominator = min(
            minimum_abs_constraint_denominator,
            abs(accepted_certificate.constraint_denominator),
        )
        all_closed = (
            all_closed
            and accepted_certificate
            .instantaneous_dark_sector_rhs_closed
        )

        times.append(time)
        states.append(state)

    return FourierModeIntegrationCertificate(
        conformal_time_start=conformal_time_start,
        conformal_time_end=conformal_time_end,
        steps=steps,
        step_size=step_size,
        initial_state=initial_state,
        final_state=state,
        times=tuple(times),
        states=tuple(states),
        max_component_residual=max_component_residual,
        max_metric_potential_abs=max_metric_potential_abs,
        minimum_abs_constraint_denominator=(
            minimum_abs_constraint_denominator
        ),
        all_instantaneous_rhs_certificates_closed=all_closed,
        fixed_background_integration_completed=True,
        cosmological_background_evolved=False,
        visible_sector_evolved=False,
        observable_computed=False,
    )


def dark_sector_fourier_mode_step_doubling(
    *,
    base_steps: int,
    conformal_time_start: float,
    conformal_time_end: float,
    initial_state: State4,
    scale_factor: float,
    conformal_hubble: float,
    wave_number: float,
    gravitational_constant: float,
    phi_background: float,
    phi_prime_background: float,
    theta_prime_background: float,
    alpha: float,
    beta: float,
    rho_star: float,
    m_phi_squared: float,
    lambda_phi: float,
    visible_delta_energy_density: float = 0.0,
    visible_momentum_divergence_source: float = 0.0,
    denominator_tolerance: float = 1.0e-14,
) -> FourierModeStepDoublingCertificate:
    """Compare N, 2N, and 4N-step bounded RK4 integrations."""

    if isinstance(base_steps, bool) or not isinstance(
        base_steps,
        int,
    ):
        raise TypeError("base_steps must be an integer")
    if base_steps <= 0:
        raise ValueError("base_steps must be positive")

    shared = dict(
        conformal_time_start=conformal_time_start,
        conformal_time_end=conformal_time_end,
        initial_state=initial_state,
        scale_factor=scale_factor,
        conformal_hubble=conformal_hubble,
        wave_number=wave_number,
        gravitational_constant=gravitational_constant,
        phi_background=phi_background,
        phi_prime_background=phi_prime_background,
        theta_prime_background=theta_prime_background,
        alpha=alpha,
        beta=beta,
        rho_star=rho_star,
        m_phi_squared=m_phi_squared,
        lambda_phi=lambda_phi,
        visible_delta_energy_density=(
            visible_delta_energy_density
        ),
        visible_momentum_divergence_source=(
            visible_momentum_divergence_source
        ),
        denominator_tolerance=denominator_tolerance,
    )

    coarse = integrate_dark_sector_fourier_mode(
        steps=base_steps,
        **shared,
    )
    medium = integrate_dark_sector_fourier_mode(
        steps=2 * base_steps,
        **shared,
    )
    fine = integrate_dark_sector_fourier_mode(
        steps=4 * base_steps,
        **shared,
    )

    coarse_medium_difference = _state_distance(
        coarse.final_state,
        medium.final_state,
    )
    medium_fine_difference = _state_distance(
        medium.final_state,
        fine.final_state,
    )

    if (
        coarse_medium_difference > 0.0
        and medium_fine_difference > 0.0
    ):
        observed_order: Optional[float] = math.log2(
            coarse_medium_difference
            / medium_fine_difference
        )
    elif (
        coarse_medium_difference == 0.0
        and medium_fine_difference == 0.0
    ):
        observed_order = math.inf
    else:
        observed_order = None

    convergence_improved = (
        medium_fine_difference
        < coarse_medium_difference
        or (
            medium_fine_difference == 0.0
            and coarse_medium_difference == 0.0
        )
    )

    bounded_mode_convergence_certified = (
        convergence_improved
        and coarse.all_instantaneous_rhs_certificates_closed
        and medium.all_instantaneous_rhs_certificates_closed
        and fine.all_instantaneous_rhs_certificates_closed
    )

    return FourierModeStepDoublingCertificate(
        coarse_steps=base_steps,
        medium_steps=2 * base_steps,
        fine_steps=4 * base_steps,
        coarse_medium_difference=coarse_medium_difference,
        medium_fine_difference=medium_fine_difference,
        observed_order=observed_order,
        convergence_improved=convergence_improved,
        coarse=coarse,
        medium=medium,
        fine=fine,
        bounded_mode_convergence_certified=(
            bounded_mode_convergence_certified
        ),
    )
