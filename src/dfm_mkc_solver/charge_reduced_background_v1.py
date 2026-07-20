"""Conditional charge-reduced DFM-MKC FLRW background integrator.

This module numerically integrates the action-consistent homogeneous system

    x = (phi, v, rho_m, rho_r)

with independent variable N = ln(a), conserved phase charge Q_theta, the
quartic potential, separately conserved dust and radiation, and the expanding
Friedmann branch.

It is a conditional background integrator only. It does not implement
perturbations, observable projection, likelihood evaluation, or empirical
validation.
"""

from __future__ import annotations

import math
from dataclasses import dataclass

import numpy as np
from scipy.integrate import solve_ivp


State = tuple[float, float, float, float, float]


@dataclass(frozen=True)
class ChargeReducedParameters:
    """Physical parameters in natural units."""

    G: float = 1.0 / (8.0 * math.pi)
    Lambda: float = 0.0
    alpha: float = 1.0
    beta: float = 1.0
    rho_star: float = 1.0
    m_phi_squared: float = 0.0
    lambda_phi: float = 0.0
    Q_theta: float = 0.0


@dataclass(frozen=True)
class ChargeReducedInitialData:
    """Initial data at N_initial; H is fixed by the constraint."""

    phi: float = 1.0
    v: float = 0.0
    theta: float = 0.0
    rho_m: float = 0.9
    rho_r: float = 3.0e-4


@dataclass(frozen=True)
class ChargeReducedSolverConfig:
    N_initial: float = -1.0
    N_final: float = 0.0
    samples: int = 201
    rtol: float = 1.0e-9
    atol: float = 1.0e-11


@dataclass(frozen=True)
class ChargeReducedBackgroundSolution:
    N: np.ndarray
    a: np.ndarray
    phi: np.ndarray
    v: np.ndarray
    rho_m: np.ndarray
    rho_r: np.ndarray
    H: np.ndarray
    rho_dfm_mkc: np.ndarray
    theta: np.ndarray
    theta_dot: np.ndarray
    phase_charge_residual: np.ndarray
    total_continuity_residual: np.ndarray
    raychaudhuri_residual: np.ndarray
    friedmann_constraint_residual: np.ndarray
    success: bool
    message: str


def _require_finite(name: str, value: float) -> None:
    if not math.isfinite(value):
        raise ValueError(f"{name} must be finite")


def validate_parameters(parameters: ChargeReducedParameters) -> None:
    for name in (
        "G",
        "Lambda",
        "alpha",
        "beta",
        "rho_star",
        "m_phi_squared",
        "lambda_phi",
        "Q_theta",
    ):
        _require_finite(name, float(getattr(parameters, name)))

    if parameters.G <= 0.0:
        raise ValueError("G must be positive")
    if parameters.alpha <= 0.0:
        raise ValueError("alpha must be positive")
    if parameters.beta <= 0.0:
        raise ValueError("beta must be positive")
    if parameters.lambda_phi < 0.0:
        raise ValueError("lambda_phi must be nonnegative")


def validate_solver_config(config: ChargeReducedSolverConfig) -> None:
    _require_finite("N_initial", config.N_initial)
    _require_finite("N_final", config.N_final)
    _require_finite("rtol", config.rtol)
    _require_finite("atol", config.atol)

    if config.N_final <= config.N_initial:
        raise ValueError("N_final must be greater than N_initial")
    if config.samples < 2:
        raise ValueError("samples must be at least 2")
    if config.rtol <= 0.0:
        raise ValueError("rtol must be positive")
    if config.atol <= 0.0:
        raise ValueError("atol must be positive")


def validate_state(state: State) -> None:
    phi, v, theta, rho_m, rho_r = state

    for name, value in (
        ("phi", phi),
        ("v", v),
        ("theta", theta),
        ("rho_m", rho_m),
        ("rho_r", rho_r),
    ):
        _require_finite(name, value)

    if abs(phi) <= 1.0e-12:
        raise ValueError("phi must remain nonzero in the charge-reduced system")
    if rho_m < 0.0:
        raise ValueError("rho_m must be nonnegative")
    if rho_r < 0.0:
        raise ValueError("rho_r must be nonnegative")


def potential(phi: float, parameters: ChargeReducedParameters) -> float:
    return (
        parameters.rho_star
        + 0.5 * parameters.m_phi_squared * phi**2
        + 0.25 * parameters.lambda_phi * phi**4
    )


def potential_derivative(
    phi: float,
    parameters: ChargeReducedParameters,
) -> float:
    return (
        parameters.m_phi_squared * phi
        + parameters.lambda_phi * phi**3
    )


def phase_energy_density(
    N: float,
    phi: float,
    parameters: ChargeReducedParameters,
) -> float:
    a = math.exp(N)
    return (
        parameters.Q_theta**2
        / (2.0 * parameters.beta * a**6 * phi**2)
    )


def dfm_energy_density(
    N: float,
    phi: float,
    v: float,
    parameters: ChargeReducedParameters,
) -> float:
    return (
        0.5 * parameters.alpha * v**2
        + phase_energy_density(N, phi, parameters)
        + potential(phi, parameters)
    )


def friedmann_radicand(
    N: float,
    state: State,
    parameters: ChargeReducedParameters,
) -> float:
    validate_state(state)
    phi, v, _theta, rho_m, rho_r = state

    rho_total = (
        rho_m
        + rho_r
        + dfm_energy_density(N, phi, v, parameters)
    )

    return (
        parameters.Lambda / 3.0
        + (8.0 * math.pi * parameters.G / 3.0) * rho_total
    )


def friedmann_hubble(
    N: float,
    state: State,
    parameters: ChargeReducedParameters,
) -> float:
    radicand = friedmann_radicand(N, state, parameters)

    if not math.isfinite(radicand) or radicand <= 0.0:
        raise ValueError(
            f"expanding Friedmann branch requires positive H^2, got {radicand}"
        )

    return math.sqrt(radicand)


def background_rhs(
    N: float,
    state_array: np.ndarray,
    parameters: ChargeReducedParameters,
) -> np.ndarray:
    state: State = tuple(float(value) for value in state_array)  # type: ignore[assignment]
    validate_state(state)

    phi, v, _theta, rho_m, rho_r = state
    a = math.exp(N)
    H = friedmann_hubble(N, state, parameters)

    charge_force = (
        parameters.Q_theta**2
        / (
            parameters.alpha
            * parameters.beta
            * a**6
            * phi**3
        )
    )

    dphi_dN = v / H
    dtheta_dN = (
        parameters.Q_theta
        / (
            parameters.beta
            * a**3
            * phi**2
            * H
        )
    )
    dv_dN = (
        -3.0 * v
        + charge_force / H
        - potential_derivative(phi, parameters)
        / (parameters.alpha * H)
    )
    drho_m_dN = -3.0 * rho_m
    drho_r_dN = -4.0 * rho_r

    return np.array(
        [
            dphi_dN,
            dv_dN,
            dtheta_dN,
            drho_m_dN,
            drho_r_dN,
        ],
        dtype=float,
    )


def solve_charge_reduced_background(
    parameters: ChargeReducedParameters | None = None,
    initial_data: ChargeReducedInitialData | None = None,
    config: ChargeReducedSolverConfig | None = None,
) -> ChargeReducedBackgroundSolution:
    """Integrate the conditional charge-reduced expanding FLRW background."""

    parameters = parameters or ChargeReducedParameters()
    initial_data = initial_data or ChargeReducedInitialData()
    config = config or ChargeReducedSolverConfig()

    validate_parameters(parameters)
    validate_solver_config(config)
    _require_finite("theta", initial_data.theta)

    initial_state: State = (
        initial_data.phi,
        initial_data.v,
        initial_data.theta,
        initial_data.rho_m,
        initial_data.rho_r,
    )
    validate_state(initial_state)
    friedmann_hubble(config.N_initial, initial_state, parameters)

    N_grid = np.linspace(
        config.N_initial,
        config.N_final,
        config.samples,
    )

    integration = solve_ivp(
        lambda N, y: background_rhs(N, y, parameters),
        (config.N_initial, config.N_final),
        np.asarray(initial_state, dtype=float),
        t_eval=N_grid,
        rtol=config.rtol,
        atol=config.atol,
    )

    if not integration.success:
        raise RuntimeError(
            f"charge-reduced background integration failed: "
            f"{integration.message}"
        )

    N = integration.t
    phi, v, theta, rho_m, rho_r = integration.y
    a = np.exp(N)

    H = np.empty_like(N)
    rho_dfm_mkc = np.empty_like(N)
    theta_dot = np.empty_like(N)
    constraint_residual = np.empty_like(N)

    for index, N_value in enumerate(N):
        state: State = (
            float(phi[index]),
            float(v[index]),
            float(theta[index]),
            float(rho_m[index]),
            float(rho_r[index]),
        )
        validate_state(state)

        H[index] = friedmann_hubble(
            float(N_value),
            state,
            parameters,
        )
        rho_dfm_mkc[index] = dfm_energy_density(
            float(N_value),
            state[0],
            state[1],
            parameters,
        )
        theta_dot[index] = (
            parameters.Q_theta
            / (
                parameters.beta
                * a[index] ** 3
                * state[0] ** 2
            )
        )

        constraint_residual[index] = (
            H[index] ** 2
            - friedmann_radicand(
                float(N_value),
                state,
                parameters,
            )
        )

    phase_charge_residual = (
        a**3
        * parameters.beta
        * phi**2
        * theta_dot
        - parameters.Q_theta
    )

    phase_energy = (
        parameters.Q_theta**2
        / (
            2.0
            * parameters.beta
            * a**6
            * phi**2
        )
    )
    potential_values = (
        parameters.rho_star
        + 0.5 * parameters.m_phi_squared * phi**2
        + 0.25 * parameters.lambda_phi * phi**4
    )
    pressure_total = (
        rho_r / 3.0
        + 0.5 * parameters.alpha * v**2
        + phase_energy
        - potential_values
    )
    rho_total = rho_m + rho_r + rho_dfm_mkc
    gradient_edge_order = 2 if len(N) >= 3 else 1
    rho_total_derivative = np.gradient(
        rho_total,
        N,
        edge_order=gradient_edge_order,
    )
    total_continuity_residual = (
        rho_total_derivative
        + 3.0 * (rho_total + pressure_total)
    )

    hubble_derivative = np.gradient(
        H,
        N,
        edge_order=gradient_edge_order,
    )
    raychaudhuri_residual = (
        H * hubble_derivative
        + 0.5 * (rho_total + pressure_total)
    )

    arrays = (
        N,
        a,
        phi,
        v,
        rho_m,
        rho_r,
        H,
        rho_dfm_mkc,
        theta,
        theta_dot,
        phase_charge_residual,
        total_continuity_residual,
        raychaudhuri_residual,
        constraint_residual,
    )
    if not all(np.all(np.isfinite(array)) for array in arrays):
        raise RuntimeError("background integration produced nonfinite output")

    return ChargeReducedBackgroundSolution(
        N=N,
        a=a,
        phi=phi,
        v=v,
        rho_m=rho_m,
        rho_r=rho_r,
        H=H,
        rho_dfm_mkc=rho_dfm_mkc,
        theta=theta,
        theta_dot=theta_dot,
        phase_charge_residual=phase_charge_residual,
        total_continuity_residual=total_continuity_residual,
        raychaudhuri_residual=raychaudhuri_residual,
        friedmann_constraint_residual=constraint_residual,
        success=True,
        message=integration.message,
    )
