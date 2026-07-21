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
from dataclasses import dataclass, replace

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


MPC_IN_METERS = 3.085677581491367e22
SHOOTING_PARAMETER_NAMES = (
    "phi_initial",
    "v_initial",
    "rho_star",
    "m_phi_squared",
    "lambda_phi",
    "Q_theta",
)
SHOOTING_RESIDUAL_NAMES = ("F_rho", "F_w", "F_H")


@dataclass(frozen=True)
class DFMCDMUnitMap:
    """Dimensionless H0-normalized map for the DFM-as-CDM branch."""

    H0_km_s_Mpc: float
    H0_si: float
    H0_code: float
    G_code: float
    omega_b0: float
    omega_cdm0: float
    omega_r0: float
    omega_lambda0: float
    rho_b0_code: float
    rho_cdm0_code: float
    rho_r0_code: float
    Lambda_code: float

    def fluid_initial_data(self, N_initial: float) -> tuple[float, float]:
        """Return baryon and radiation densities at the shooting surface."""

        _require_finite("N_initial", N_initial)
        return (
            self.rho_b0_code * math.exp(-3.0 * N_initial),
            self.rho_r0_code * math.exp(-4.0 * N_initial),
        )


@dataclass(frozen=True)
class DFMCDMShootingResiduals:
    """Terminal calibration residuals for the DFM-as-CDM branch."""

    F_rho: float
    F_w: float
    F_H: float
    rho_dfm0: float
    pressure_dfm0: float
    H0_code: float

    def as_array(self) -> np.ndarray:
        return np.asarray((self.F_rho, self.F_w, self.F_H), dtype=float)


@dataclass(frozen=True)
class ShootingJacobianAnalysis:
    """Local rank and null-space certificate for the shooting map."""

    parameter_names: tuple[str, ...]
    residual_names: tuple[str, ...]
    parameter_vector: np.ndarray
    residual_vector: np.ndarray
    jacobian: np.ndarray
    singular_values: np.ndarray
    rank_tolerance: float
    rank: int
    nullity: int
    null_space_basis: np.ndarray
    friedmann_row_dependency_error: float
    locally_identifiable: bool


def _validated_dfm_cdm_shooting_vector(vector: np.ndarray) -> np.ndarray:
    """Return a copied shooting vector after enforcing its physical domain."""

    candidate = np.asarray(vector, dtype=float)
    if candidate.shape != (len(SHOOTING_PARAMETER_NAMES),):
        raise ValueError("shooting parameter vector has the wrong shape")
    if not np.all(np.isfinite(candidate)):
        raise ValueError("shooting parameter vector must be finite")

    phi_initial, _v_initial, rho_star, m2, lambda_phi, _Q_theta = (
        float(value) for value in candidate
    )
    if phi_initial <= 0.0:
        raise ValueError("phi_initial must be positive on the radial-field branch")
    if rho_star < 0.0:
        raise ValueError("rho_star must be nonnegative")
    if m2 < 0.0:
        raise ValueError("m_phi_squared must be nonnegative")
    if lambda_phi < 0.0:
        raise ValueError("lambda_phi must be nonnegative")
    return candidate.copy()


@dataclass(frozen=True)
class DFMCDMNullChart:
    """Bounded local chart along four shooting-Jacobian null directions."""

    base_vector: np.ndarray
    null_basis: np.ndarray
    eta_lower: np.ndarray
    eta_upper: np.ndarray

    def __post_init__(self) -> None:
        parameter_count = len(SHOOTING_PARAMETER_NAMES)
        nullity = parameter_count - 2
        base_vector = _validated_dfm_cdm_shooting_vector(self.base_vector)
        null_basis = np.asarray(self.null_basis, dtype=float)
        eta_lower = np.asarray(self.eta_lower, dtype=float)
        eta_upper = np.asarray(self.eta_upper, dtype=float)

        if null_basis.shape != (parameter_count, nullity):
            raise ValueError("null_basis must have shape (6, 4)")
        if eta_lower.shape != (nullity,) or eta_upper.shape != (nullity,):
            raise ValueError("eta bounds must each have shape (4,)")
        if not np.all(np.isfinite(null_basis)):
            raise ValueError("null_basis must be finite")
        if not np.all(np.isfinite(eta_lower)) or not np.all(np.isfinite(eta_upper)):
            raise ValueError("eta bounds must be finite")
        if np.any(eta_lower > eta_upper):
            raise ValueError("eta_lower must not exceed eta_upper")
        if np.linalg.matrix_rank(null_basis) != nullity:
            raise ValueError("null_basis must have four independent columns")

        base_vector.setflags(write=False)
        null_basis = null_basis.copy()
        eta_lower = eta_lower.copy()
        eta_upper = eta_upper.copy()
        null_basis.setflags(write=False)
        eta_lower.setflags(write=False)
        eta_upper.setflags(write=False)
        object.__setattr__(self, "base_vector", base_vector)
        object.__setattr__(self, "null_basis", null_basis)
        object.__setattr__(self, "eta_lower", eta_lower)
        object.__setattr__(self, "eta_upper", eta_upper)

    def candidate_vector(self, eta: np.ndarray) -> np.ndarray:
        """Construct one bounded candidate and enforce the static domain."""

        coordinates = np.asarray(eta, dtype=float)
        if coordinates.shape != self.eta_lower.shape:
            raise ValueError("eta must have shape (4,)")
        if not np.all(np.isfinite(coordinates)):
            raise ValueError("eta must be finite")
        if np.any(coordinates < self.eta_lower) or np.any(coordinates > self.eta_upper):
            raise ValueError("eta lies outside the null-chart bounds")
        return _validated_dfm_cdm_shooting_vector(
            self.base_vector + self.null_basis @ coordinates
        )


def build_dfm_cdm_unit_map(
    *,
    H0_km_s_Mpc: float,
    omega_b0: float,
    omega_cdm0: float,
    omega_r0: float,
    omega_lambda0: float | None = None,
) -> DFMCDMUnitMap:
    """Map measured density fractions into H0-normalized solver units.

    The branch convention is H0_code = 1, G_code = 1/(8*pi), visible
    pressureless matter = baryons, and DFM replaces cold dark matter.
    """

    for name, value in (
        ("H0_km_s_Mpc", H0_km_s_Mpc),
        ("omega_b0", omega_b0),
        ("omega_cdm0", omega_cdm0),
        ("omega_r0", omega_r0),
    ):
        _require_finite(name, value)
    if H0_km_s_Mpc <= 0.0:
        raise ValueError("H0_km_s_Mpc must be positive")
    if min(omega_b0, omega_cdm0, omega_r0) < 0.0:
        raise ValueError("density fractions must be nonnegative")

    if omega_lambda0 is None:
        omega_lambda0 = 1.0 - omega_b0 - omega_cdm0 - omega_r0
    _require_finite("omega_lambda0", omega_lambda0)
    if omega_lambda0 < 0.0:
        raise ValueError("omega_lambda0 must be nonnegative")

    closure = omega_b0 + omega_cdm0 + omega_r0 + omega_lambda0
    if not math.isclose(closure, 1.0, rel_tol=0.0, abs_tol=1.0e-12):
        raise ValueError("flat DFM-as-CDM branch requires density fractions to sum to one")

    H0_si = H0_km_s_Mpc * 1000.0 / MPC_IN_METERS
    return DFMCDMUnitMap(
        H0_km_s_Mpc=H0_km_s_Mpc,
        H0_si=H0_si,
        H0_code=1.0,
        G_code=1.0 / (8.0 * math.pi),
        omega_b0=omega_b0,
        omega_cdm0=omega_cdm0,
        omega_r0=omega_r0,
        omega_lambda0=omega_lambda0,
        rho_b0_code=3.0 * omega_b0,
        rho_cdm0_code=3.0 * omega_cdm0,
        rho_r0_code=3.0 * omega_r0,
        Lambda_code=3.0 * omega_lambda0,
    )


def dfm_pressure(
    N: float,
    phi: float,
    v: float,
    parameters: ChargeReducedParameters,
) -> float:
    """Return the homogeneous DFM pressure."""

    return (
        0.5 * parameters.alpha * v**2
        + phase_energy_density(N, phi, parameters)
        - potential(phi, parameters)
    )


def shoot_dfm_cdm_background(
    *,
    unit_map: DFMCDMUnitMap,
    parameters: ChargeReducedParameters,
    phi_initial: float,
    v_initial: float,
    config: ChargeReducedSolverConfig,
) -> ChargeReducedBackgroundSolution:
    """Integrate the canonical DFM-as-CDM branch to N=0."""

    if not math.isclose(config.N_final, 0.0, rel_tol=0.0, abs_tol=1.0e-15):
        raise ValueError("DFM-CDM shooting requires N_final = 0")
    rho_b_initial, rho_r_initial = unit_map.fluid_initial_data(
        config.N_initial
    )
    locked_parameters = replace(
        parameters,
        G=unit_map.G_code,
        Lambda=unit_map.Lambda_code,
    )
    initial_data = ChargeReducedInitialData(
        phi=phi_initial,
        v=v_initial,
        theta=0.0,
        rho_m=rho_b_initial,
        rho_r=rho_r_initial,
    )
    return solve_charge_reduced_background(
        locked_parameters,
        initial_data,
        config,
    )


def dfm_cdm_shooting_residuals(
    *,
    unit_map: DFMCDMUnitMap,
    parameters: ChargeReducedParameters,
    phi_initial: float,
    v_initial: float,
    config: ChargeReducedSolverConfig,
    target_w_dfm0: float = 0.0,
) -> DFMCDMShootingResiduals:
    """Compute F_rho, F_w, and F_H at the present surface."""

    _require_finite("target_w_dfm0", target_w_dfm0)
    locked_parameters = replace(
        parameters,
        G=unit_map.G_code,
        Lambda=unit_map.Lambda_code,
    )
    solution = shoot_dfm_cdm_background(
        unit_map=unit_map,
        parameters=locked_parameters,
        phi_initial=phi_initial,
        v_initial=v_initial,
        config=config,
    )
    rho_dfm0 = float(solution.rho_dfm_mkc[-1])
    pressure_dfm0 = dfm_pressure(
        float(solution.N[-1]),
        float(solution.phi[-1]),
        float(solution.v[-1]),
        locked_parameters,
    )
    H0_code = float(solution.H[-1])
    return DFMCDMShootingResiduals(
        F_rho=rho_dfm0 - unit_map.rho_cdm0_code,
        F_w=pressure_dfm0 - target_w_dfm0 * rho_dfm0,
        F_H=H0_code - unit_map.H0_code,
        rho_dfm0=rho_dfm0,
        pressure_dfm0=pressure_dfm0,
        H0_code=H0_code,
    )


def _shooting_vector_to_inputs(
    vector: np.ndarray,
    *,
    alpha: float,
    beta: float,
    unit_map: DFMCDMUnitMap,
) -> tuple[float, float, ChargeReducedParameters]:
    if vector.shape != (len(SHOOTING_PARAMETER_NAMES),):
        raise ValueError("shooting parameter vector has the wrong shape")
    if not np.all(np.isfinite(vector)):
        raise ValueError("shooting parameter vector must be finite")
    phi_initial, v_initial, rho_star, m2, lambda_phi, Q_theta = (
        float(value) for value in vector
    )
    return (
        phi_initial,
        v_initial,
        ChargeReducedParameters(
            G=unit_map.G_code,
            Lambda=unit_map.Lambda_code,
            alpha=alpha,
            beta=beta,
            rho_star=rho_star,
            m_phi_squared=m2,
            lambda_phi=lambda_phi,
            Q_theta=Q_theta,
        ),
    )


def dfm_cdm_shooting_residual_vector(
    vector: np.ndarray,
    *,
    alpha: float,
    beta: float,
    unit_map: DFMCDMUnitMap,
    config: ChargeReducedSolverConfig,
    target_w_dfm0: float = 0.0,
) -> np.ndarray:
    """Evaluate the three-component shooting residual map."""

    phi_initial, v_initial, parameters = _shooting_vector_to_inputs(
        np.asarray(vector, dtype=float),
        alpha=alpha,
        beta=beta,
        unit_map=unit_map,
    )
    return dfm_cdm_shooting_residuals(
        unit_map=unit_map,
        parameters=parameters,
        phi_initial=phi_initial,
        v_initial=v_initial,
        config=config,
        target_w_dfm0=target_w_dfm0,
    ).as_array()


def analyze_dfm_cdm_shooting_jacobian(
    vector: np.ndarray,
    *,
    alpha: float,
    beta: float,
    unit_map: DFMCDMUnitMap,
    config: ChargeReducedSolverConfig,
    target_w_dfm0: float = 0.0,
    relative_step: float = 1.0e-5,
    rank_tolerance: float | None = None,
) -> ShootingJacobianAnalysis:
    """Compute the local Jacobian rank and an explicit null-space basis."""

    if relative_step <= 0.0 or not math.isfinite(relative_step):
        raise ValueError("relative_step must be positive and finite")
    vector = np.asarray(vector, dtype=float)
    residual = dfm_cdm_shooting_residual_vector(
        vector,
        alpha=alpha,
        beta=beta,
        unit_map=unit_map,
        config=config,
        target_w_dfm0=target_w_dfm0,
    )
    jacobian = np.empty(
        (len(SHOOTING_RESIDUAL_NAMES), len(SHOOTING_PARAMETER_NAMES)),
        dtype=float,
    )
    for column in range(vector.size):
        step = relative_step * max(1.0, abs(float(vector[column])))
        plus = vector.copy()
        minus = vector.copy()
        plus[column] += step
        minus[column] -= step
        if column == 4 and minus[column] < 0.0:
            plus_residual = dfm_cdm_shooting_residual_vector(
                plus,
                alpha=alpha,
                beta=beta,
                unit_map=unit_map,
                config=config,
                target_w_dfm0=target_w_dfm0,
            )
            jacobian[:, column] = (plus_residual - residual) / step
        else:
            plus_residual = dfm_cdm_shooting_residual_vector(
                plus,
                alpha=alpha,
                beta=beta,
                unit_map=unit_map,
                config=config,
                target_w_dfm0=target_w_dfm0,
            )
            minus_residual = dfm_cdm_shooting_residual_vector(
                minus,
                alpha=alpha,
                beta=beta,
                unit_map=unit_map,
                config=config,
                target_w_dfm0=target_w_dfm0,
            )
            jacobian[:, column] = (
                plus_residual - minus_residual
            ) / (2.0 * step)

    _u, singular_values, vh = np.linalg.svd(jacobian, full_matrices=True)
    if rank_tolerance is None:
        largest = float(singular_values[0]) if singular_values.size else 0.0
        rank_tolerance = (
            max(jacobian.shape)
            * math.sqrt(np.finfo(float).eps)
            * largest
        )
    if rank_tolerance < 0.0 or not math.isfinite(rank_tolerance):
        raise ValueError("rank_tolerance must be nonnegative and finite")
    rank = int(np.sum(singular_values > rank_tolerance))
    null_space_basis = vh[rank:, :].T.copy()
    nullity = int(null_space_basis.shape[1])

    H0_code = residual[2] + unit_map.H0_code
    expected_H_row = jacobian[0, :] / (6.0 * H0_code)
    dependency_error = float(
        np.linalg.norm(jacobian[2, :] - expected_H_row, ord=np.inf)
    )
    return ShootingJacobianAnalysis(
        parameter_names=SHOOTING_PARAMETER_NAMES,
        residual_names=SHOOTING_RESIDUAL_NAMES,
        parameter_vector=vector.copy(),
        residual_vector=residual,
        jacobian=jacobian,
        singular_values=singular_values,
        rank_tolerance=float(rank_tolerance),
        rank=rank,
        nullity=nullity,
        null_space_basis=null_space_basis,
        friedmann_row_dependency_error=dependency_error,
        locally_identifiable=rank == len(SHOOTING_PARAMETER_NAMES),
    )


def evaluate_dfm_cdm_null_chart_candidate(
    chart: DFMCDMNullChart,
    eta: np.ndarray,
    *,
    alpha: float,
    beta: float,
    unit_map: DFMCDMUnitMap,
    config: ChargeReducedSolverConfig,
    target_w_dfm0: float = 0.0,
    relative_step: float = 1.0e-5,
    rank_tolerance: float | None = None,
) -> ShootingJacobianAnalysis:
    """Accept a chart point only when its basis and evolved rank remain valid."""

    candidate = chart.candidate_vector(eta)
    base_analysis = analyze_dfm_cdm_shooting_jacobian(
        chart.base_vector,
        alpha=alpha,
        beta=beta,
        unit_map=unit_map,
        config=config,
        target_w_dfm0=target_w_dfm0,
        relative_step=relative_step,
        rank_tolerance=rank_tolerance,
    )
    if base_analysis.rank != 2:
        raise ValueError(
            f"null-chart base Jacobian rank must equal 2; got {base_analysis.rank}"
        )

    null_residual = float(
        np.linalg.norm(base_analysis.jacobian @ chart.null_basis, ord=2)
    )
    jacobian_scale = float(np.linalg.norm(base_analysis.jacobian, ord=2))
    basis_scale = float(np.linalg.norm(chart.null_basis, ord=2))
    null_tolerance = (
        10.0
        * max(
            base_analysis.rank_tolerance,
            np.finfo(float).eps
            * max(base_analysis.jacobian.shape)
            * jacobian_scale,
        )
        * max(1.0, basis_scale)
    )
    if null_residual > null_tolerance:
        raise ValueError(
            "null_basis does not lie in the base Jacobian null space: "
            f"residual {null_residual:.12e} exceeds tolerance "
            f"{null_tolerance:.12e}"
        )

    analysis = analyze_dfm_cdm_shooting_jacobian(
        candidate,
        alpha=alpha,
        beta=beta,
        unit_map=unit_map,
        config=config,
        target_w_dfm0=target_w_dfm0,
        relative_step=relative_step,
        rank_tolerance=rank_tolerance,
    )
    if analysis.rank != 2:
        raise ValueError(
            f"null-chart candidate Jacobian rank must equal 2; got {analysis.rank}"
        )
    return analysis


DFM_CDM_PHYSICAL_CLOSURE_NAMES = (
    "C_v_initial",
    "C_rho_star",
    "C_lambda_phi",
    "C_circular_force",
)

DFM_CDM_AUGMENTED_RESIDUAL_NAMES = (
    "F_rho",
    "F_w",
    *DFM_CDM_PHYSICAL_CLOSURE_NAMES,
)


@dataclass(frozen=True)
class DFMCDMPhysicalClosureResiduals:
    """Residuals defining the minimal circular DFM-as-CDM branch."""

    C_v_initial: float
    C_rho_star: float
    C_lambda_phi: float
    C_circular_force: float

    def as_array(self) -> np.ndarray:
        return np.asarray(
            (
                self.C_v_initial,
                self.C_rho_star,
                self.C_lambda_phi,
                self.C_circular_force,
            ),
            dtype=float,
        )


@dataclass(frozen=True)
class DFMCDMAugmentedJacobianAnalysis:
    """Local rank certificate after imposing physical closures."""

    parameter_names: tuple[str, ...]
    residual_names: tuple[str, ...]
    parameter_vector: np.ndarray
    residual_vector: np.ndarray
    jacobian: np.ndarray
    singular_values: np.ndarray
    rank_tolerance: float
    rank: int
    condition_number: float
    locally_identifiable: bool


def dfm_cdm_minimal_circular_closure_residuals(
    vector: np.ndarray,
    *,
    beta: float,
    N_initial: float,
) -> DFMCDMPhysicalClosureResiduals:
    """Evaluate the four minimal circular-branch closure equations."""

    _require_finite("beta", beta)
    _require_finite("N_initial", N_initial)

    if beta <= 0.0:
        raise ValueError(
            "minimal circular closure requires beta to be positive"
        )

    candidate = _validated_dfm_cdm_shooting_vector(vector)

    (
        phi_initial,
        v_initial,
        rho_star,
        m_phi_squared,
        lambda_phi,
        Q_theta,
    ) = (float(value) for value in candidate)

    if Q_theta <= 0.0:
        raise ValueError(
            "minimal circular closure requires the positive-charge branch"
        )

    circular_force = (
        m_phi_squared * phi_initial
        + lambda_phi * phi_initial**3
        - (
            Q_theta**2
            * math.exp(-6.0 * N_initial)
            / (beta * phi_initial**3)
        )
    )

    return DFMCDMPhysicalClosureResiduals(
        C_v_initial=v_initial,
        C_rho_star=rho_star,
        C_lambda_phi=lambda_phi,
        C_circular_force=circular_force,
    )


def dfm_cdm_augmented_residual_vector(
    vector: np.ndarray,
    *,
    alpha: float,
    beta: float,
    unit_map: DFMCDMUnitMap,
    config: ChargeReducedSolverConfig,
    target_w_dfm0: float = 0.0,
) -> np.ndarray:
    """Return two independent calibration residuals and four closures."""

    candidate = _validated_dfm_cdm_shooting_vector(vector)

    shooting = dfm_cdm_shooting_residual_vector(
        candidate,
        alpha=alpha,
        beta=beta,
        unit_map=unit_map,
        config=config,
        target_w_dfm0=target_w_dfm0,
    )

    closures = dfm_cdm_minimal_circular_closure_residuals(
        candidate,
        beta=beta,
        N_initial=config.N_initial,
    ).as_array()

    # F_H is excluded because its Jacobian row is dependent on F_rho.
    return np.concatenate((shooting[:2], closures))


def analyze_dfm_cdm_augmented_jacobian(
    vector: np.ndarray,
    *,
    alpha: float,
    beta: float,
    unit_map: DFMCDMUnitMap,
    config: ChargeReducedSolverConfig,
    target_w_dfm0: float = 0.0,
    relative_step: float = 1.0e-6,
    rank_tolerance: float | None = None,
) -> DFMCDMAugmentedJacobianAnalysis:
    """Analyze local identifiability of the physically closed system."""

    if relative_step <= 0.0 or not math.isfinite(relative_step):
        raise ValueError("relative_step must be positive and finite")

    candidate = _validated_dfm_cdm_shooting_vector(vector)

    residual = dfm_cdm_augmented_residual_vector(
        candidate,
        alpha=alpha,
        beta=beta,
        unit_map=unit_map,
        config=config,
        target_w_dfm0=target_w_dfm0,
    )

    parameter_count = len(SHOOTING_PARAMETER_NAMES)
    jacobian = np.empty(
        (
            len(DFM_CDM_AUGMENTED_RESIDUAL_NAMES),
            parameter_count,
        ),
        dtype=float,
    )

    for column in range(parameter_count):
        step = relative_step * max(
            1.0,
            abs(float(candidate[column])),
        )

        plus = candidate.copy()
        minus = candidate.copy()
        plus[column] += step
        minus[column] -= step

        forward_difference = (
            (column in (0, 5) and minus[column] <= 0.0)
            or (column in (2, 3, 4) and minus[column] < 0.0)
        )

        plus_residual = dfm_cdm_augmented_residual_vector(
            plus,
            alpha=alpha,
            beta=beta,
            unit_map=unit_map,
            config=config,
            target_w_dfm0=target_w_dfm0,
        )

        if forward_difference:
            jacobian[:, column] = (
                plus_residual - residual
            ) / step
        else:
            minus_residual = dfm_cdm_augmented_residual_vector(
                minus,
                alpha=alpha,
                beta=beta,
                unit_map=unit_map,
                config=config,
                target_w_dfm0=target_w_dfm0,
            )
            jacobian[:, column] = (
                plus_residual - minus_residual
            ) / (2.0 * step)

    singular_values = np.linalg.svd(
        jacobian,
        compute_uv=False,
    )

    if rank_tolerance is None:
        largest = (
            float(singular_values[0])
            if singular_values.size
            else 0.0
        )
        rank_tolerance = (
            max(jacobian.shape)
            * math.sqrt(np.finfo(float).eps)
            * largest
        )

    if rank_tolerance < 0.0 or not math.isfinite(rank_tolerance):
        raise ValueError(
            "rank_tolerance must be nonnegative and finite"
        )

    rank = int(
        np.sum(singular_values > rank_tolerance)
    )

    parameter_vector = candidate.copy()
    residual_vector = residual.copy()
    jacobian_copy = jacobian.copy()
    singular_values_copy = singular_values.copy()

    for array in (
        parameter_vector,
        residual_vector,
        jacobian_copy,
        singular_values_copy,
    ):
        array.setflags(write=False)

    return DFMCDMAugmentedJacobianAnalysis(
        parameter_names=SHOOTING_PARAMETER_NAMES,
        residual_names=DFM_CDM_AUGMENTED_RESIDUAL_NAMES,
        parameter_vector=parameter_vector,
        residual_vector=residual_vector,
        jacobian=jacobian_copy,
        singular_values=singular_values_copy,
        rank_tolerance=float(rank_tolerance),
        rank=rank,
        condition_number=float(np.linalg.cond(jacobian)),
        locally_identifiable=rank == parameter_count,
    )
