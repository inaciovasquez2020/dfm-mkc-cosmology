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
import sympy as sp
from scipy.integrate import solve_ivp


State = tuple[float, float, float, float, float]


@dataclass(frozen=True)
class ChargeReducedParameters:
    """Physical parameters in natural units."""

    G: float = 1.0 / (8.0 * math.pi)
    Lambda: float = 0.0
    w0: float = -1.0
    wa: float = 0.0
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
    rho_dark_energy: np.ndarray
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
        "w0",
        "wa",
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


def exact_charge_reduced_constraint_certificate() -> dict[str, sp.Expr]:
    """Return exact continuity and Friedmann-constraint identities.

    The returned expressions are obtained only by algebraic substitution of
    the charge-reduced action equations.  They are independent of the
    finite-difference diagnostics computed for numerical solutions below.
    """

    alpha, beta, a, phi, v, H = sp.symbols(
        "alpha beta a phi v H",
        nonzero=True,
    )
    Q_theta, m_phi_squared, lambda_phi = sp.symbols(
        "Q_theta m_phi_squared lambda_phi",
    )
    G = sp.symbols("G")
    rho_b, rho_r = sp.symbols("rho_b rho_r")

    phase_energy = Q_theta**2 / (2 * beta * a**6 * phi**2)
    potential_prime = m_phi_squared * phi + lambda_phi * phi**3
    v_dot = (
        -3 * H * v
        + Q_theta**2 / (alpha * beta * a**6 * phi**3)
        - potential_prime / alpha
    )
    phase_energy_dot = phase_energy * (-6 * H - 2 * v / phi)
    rho_dfm_dot = sp.expand(
        alpha * v * v_dot
        + phase_energy_dot
        + potential_prime * v
    )
    rho_dfm_plus_pressure = alpha * v**2 + 2 * phase_energy
    dfm_continuity = sp.factor(
        rho_dfm_dot + 3 * H * rho_dfm_plus_pressure
    )

    rho_total_plus_pressure = (
        rho_b
        + sp.Rational(4, 3) * rho_r
        + rho_dfm_plus_pressure
    )
    rho_total_dot = -3 * H * rho_total_plus_pressure
    H_dot = -4 * sp.pi * G * rho_total_plus_pressure
    friedmann_constraint_dot = sp.factor(
        2 * H * H_dot
        - (8 * sp.pi * G / 3) * rho_total_dot
    )

    return {
        "dfm_continuity": dfm_continuity,
        "friedmann_constraint": friedmann_constraint_dot,
    }


def exact_zero_alpha_dust_boundary_certificate() -> dict[str, sp.Expr]:
    """Certify the exact degenerate ``alpha = 0`` dust boundary identity.

    ``alpha = 0`` is outside the currently validated canonical interior
    ``alpha > 0``.  This proves an exact degenerate boundary identity only:
    it does not prove convergence as alpha approaches zero from above, it
    does not establish an admissible DFM-Lambda-CDM overlap, and it does not
    establish a certified manifold lower bound.
    """

    a, beta, mu, q = sp.symbols(
        "a beta mu q",
        positive=True,
    )
    phi = sp.sqrt(q / (sp.sqrt(beta) * mu)) * a ** sp.Rational(-3, 2)

    phase_energy = q**2 / (2 * beta * a**6 * phi**2)
    mass_potential = sp.Rational(1, 2) * mu**2 * phi**2
    rho_dfm = phase_energy + mass_potential
    p_dfm = phase_energy - mass_potential
    algebraic_radial_force = (
        mu**2 * phi
        - q**2 / (beta * a**6 * phi**3)
    )

    dust_density = q * mu / sp.sqrt(beta) * a**-3
    component_density = (
        q * mu / (2 * sp.sqrt(beta)) * a**-3
    )
    rho_cdm0 = q * mu / sp.sqrt(beta)

    return {
        "phase_energy": sp.simplify(phase_energy - component_density),
        "mass_potential": sp.simplify(
            mass_potential - component_density
        ),
        "rho_dfm": sp.simplify(rho_dfm - dust_density),
        "p_dfm": sp.simplify(p_dfm),
        "algebraic_radial_force": sp.simplify(
            algebraic_radial_force
        ),
        "continuity": sp.simplify(
            a * sp.diff(rho_dfm, a) + 3 * rho_dfm
        ),
        "dust_density_equivalence": sp.simplify(
            rho_dfm - rho_cdm0 * a**-3
        ),
    }


def exact_finite_alpha_circular_dust_obstruction_certificate(
) -> dict[str, sp.Expr]:
    """Certify the finite-alpha obstruction on the circular dust trajectory.

    This proves an obstruction only for the same algebraic circular
    trajectory.  It does not exclude other finite-alpha DFM trajectories,
    and it does not prove or disprove convergence as alpha approaches zero.
    It does not prove a complete DFM-Lambda-CDM manifold separation, and it
    does not authorize a positive certified lower bound.
    """

    alpha, beta, mu, q, phi, a = sp.symbols(
        "alpha beta mu q phi a",
        positive=True,
    )
    H, H_dot = sp.symbols("H H_dot", real=True)

    phi_dot = -sp.Rational(3, 2) * H * phi
    phi_ddot = (
        sp.Rational(9, 4) * H**2 * phi
        - sp.Rational(3, 2) * H_dot * phi
    )
    inertial_term = phi_ddot + 3 * H * phi_dot
    inertial_defect = (
        -sp.Rational(3, 4) * (2 * H_dot + 3 * H**2) * phi
    )

    inverse_a6 = beta * mu**2 * phi**4 / q**2
    inverse_a3 = sp.sqrt(beta) * mu * phi**2 / q
    centrifugal_force = (
        q**2 / (beta * phi**3) * inverse_a6
    )
    force_balance = mu**2 * phi - centrifugal_force
    radial_equation = (
        alpha * inertial_term + force_balance
    )
    radial_defect = (
        -sp.Rational(3, 4)
        * alpha
        * (2 * H_dot + 3 * H**2)
        * phi
    )

    phase_energy = (
        q**2 / (2 * beta * phi**2) * inverse_a6
    )
    mass_potential = sp.Rational(1, 2) * mu**2 * phi**2
    kinetic_energy = sp.Rational(1, 2) * alpha * phi_dot**2
    rho_dfm = kinetic_energy + phase_energy + mass_potential
    p_dfm = kinetic_energy + phase_energy - mass_potential
    pressure_defect = (
        sp.Rational(9, 8) * alpha * H**2 * phi**2
    )
    dust_density = (
        q * mu / sp.sqrt(beta) * inverse_a3
    )

    return {
        "inertial_identity": sp.simplify(
            inertial_term - inertial_defect
        ),
        "radial_equation_identity": sp.simplify(
            radial_equation - radial_defect
        ),
        "force_balance": sp.simplify(force_balance),
        "pressure_identity": sp.simplify(
            p_dfm - pressure_defect
        ),
        "density_excess_identity": sp.simplify(
            rho_dfm - dust_density - pressure_defect
        ),
    }


def exact_finite_alpha_circular_tracking_coercivity_certificate(
) -> dict[str, sp.Expr]:
    """Certify exact tracking around the algebraic circular trajectory.

    The nonlinear radial force is strongly restoring on ``phi > 0``.  The
    forcing term is O(alpha) on bounded backgrounds, but coercivity alone
    does not prove convergence: well-prepared initial data and a uniform
    energy estimate remain required.  No complete DFM-Lambda-CDM overlap or
    separation result follows.
    """

    alpha, mu, phi_c, phi = sp.symbols(
        "alpha mu phi_c phi",
        positive=True,
    )
    H, H_dot, delta_dot, delta_ddot = sp.symbols(
        "H H_dot delta_dot delta_ddot",
        real=True,
    )
    delta = phi - phi_c

    force = mu**2 * phi - mu**2 * phi_c**4 / phi**3
    restoring_coefficient = mu**2 * (
        1
        + phi_c / phi
        + phi_c**2 / phi**2
        + phi_c**3 / phi**3
    )

    phi_c_dot = -sp.Rational(3, 2) * H * phi_c
    phi_c_ddot = (
        sp.Rational(9, 4) * H**2 * phi_c
        - sp.Rational(3, 2) * H_dot * phi_c
    )
    complete_radial_equation = (
        alpha
        * (
            phi_c_ddot
            + delta_ddot
            + 3 * H * (phi_c_dot + delta_dot)
        )
        + force
    )
    tracking_equation = (
        alpha * (delta_ddot + 3 * H * delta_dot)
        + force
        - sp.Rational(3, 4)
        * alpha
        * (2 * H_dot + 3 * H**2)
        * phi_c
    )

    coercive_remainder = (
        mu**2
        * delta**2
        * (
            phi_c / phi
            + phi_c**2 / phi**2
            + phi_c**3 / phi**3
        )
    )

    y = sp.symbols("y", positive=True)
    restoring_coefficient_y = mu**2 * (
        1 + 1 / y + 1 / y**2 + 1 / y**3
    )
    restoring_coefficient_y_derivative = -mu**2 * (
        1 / y**2 + 2 / y**3 + 3 / y**4
    )

    return {
        "force_factorization": sp.simplify(
            force - restoring_coefficient * delta
        ),
        "tracking_equation_decomposition": sp.simplify(
            complete_radial_equation - tracking_equation
        ),
        "linear_restoring_coefficient": sp.simplify(
            restoring_coefficient.subs(phi, phi_c) - 4 * mu**2
        ),
        "coercive_work_identity": sp.simplify(
            force * delta - mu**2 * delta**2 - coercive_remainder
        ),
        "restoring_coefficient_monotonicity": sp.simplify(
            sp.diff(restoring_coefficient_y, y)
            - restoring_coefficient_y_derivative
        ),
    }


def exact_finite_alpha_relative_tracking_energy_certificate(
) -> dict[str, sp.Expr]:
    """Certify finite-alpha relative tracking on a finite interval.

    Here ``y = phi/phi_c`` removes the apparent Hubble damping exactly, and
    the relative system is a forced stiff oscillator.  The energy estimate is
    conditional on a uniform bound for
    ``abs((3/4)*(2*H_dot+3*H**2))``.  Exactly prepared initial data give an
    ``O(sqrt(alpha))`` relative-field bound.

    This certificate does not yet establish a bound for the fully coupled
    Hubble evolution.  It does not yet prove a DFM-Lambda-CDM manifold
    overlap, and it does not authorize a positive or zero certified manifold
    lower bound.
    """

    alpha, mu, phi_c, y, G = sp.symbols(
        "alpha mu phi_c y G",
        positive=True,
    )
    E0, t = sp.symbols("E0 t", nonnegative=True)
    H, H_dot, y_dot, y_ddot, g = sp.symbols(
        "H H_dot y_dot y_ddot g",
        real=True,
    )

    phi_c_dot = -sp.Rational(3, 2) * H * phi_c
    phi_c_ddot = (
        sp.Rational(9, 4) * H**2 * phi_c
        - sp.Rational(3, 2) * H_dot * phi_c
    )
    phi_dot = phi_c_dot * y + phi_c * y_dot
    phi_ddot = (
        phi_c_ddot * y
        + 2 * phi_c_dot * y_dot
        + phi_c * y_ddot
    )
    g_definition = sp.Rational(3, 4) * (2 * H_dot + 3 * H**2)
    complete_relative_equation = (
        alpha * (phi_ddot + 3 * H * phi_dot) / phi_c
        + mu**2 * (y - y**-3)
    )
    relative_equation = (
        alpha * y_ddot + mu**2 * (y - y**-3) - alpha * g * y
    )

    potential = sp.Rational(1, 2) * mu**2 * (
        y**2 + y**-2 - 2
    )
    energy = sp.Rational(1, 2) * alpha * y_dot**2 + potential
    y_ddot_equation = g * y - mu**2 * (y - y**-3) / alpha
    energy_derivative = (
        alpha * y_dot * y_ddot
        + mu**2 * (y - y**-3) * y_dot
    )

    young_terms = (
        sp.Rational(1, 2) * alpha * y_dot**2
        + sp.Rational(1, 2) * alpha * g**2 * y**2
    )
    energy_majorant = energy + alpha * g**2 * (
        1 + energy / mu**2
    )
    c = 1 + alpha * G**2 / mu**2
    forcing_majorant = energy + alpha * g**2 * (
        1 + energy / mu**2
    )
    B = (
        E0 * sp.exp(c * t)
        + alpha * G**2 * (sp.exp(c * t) - 1) / c
    )

    return {
        "relative_equation_decomposition": sp.simplify(
            complete_relative_equation
            - relative_equation.subs(g, g_definition)
        ),
        "energy_identity": sp.simplify(
            energy_derivative.subs(y_ddot, y_ddot_equation)
            - alpha * g * y * y_dot
        ),
        "potential_coercivity_identity": sp.simplify(
            potential
            - sp.Rational(1, 2) * mu**2 * (y - 1)**2
            - sp.Rational(1, 2)
            * mu**2
            * (y - 1)**2
            * (2 * y + 1)
            / y**2
        ),
        "field_size_control_identity": sp.simplify(
            2 + 2 * energy / mu**2 - y**2
            - alpha * y_dot**2 / mu**2
            - y**-2
        ),
        "young_square_identity": sp.simplify(
            young_terms
            - alpha * g * y * y_dot
            - sp.Rational(1, 2) * alpha * (y_dot - g * y)**2
        ),
        "energy_majorant_remainder": sp.simplify(
            energy_majorant
            - young_terms
            - potential
            - sp.Rational(1, 2)
            * alpha
            * g**2
            * (alpha * y_dot**2 / mu**2 + y**-2)
        ),
        "forcing_bound_remainder": sp.simplify(
            c * energy
            + alpha * G**2
            - forcing_majorant
            - alpha * (G**2 - g**2) * (1 + energy / mu**2)
        ),
        "gronwall_ode_identity": sp.simplify(
            sp.diff(B, t) - c * B - alpha * G**2
        ),
        "gronwall_initial_identity": sp.simplify(B.subs(t, 0) - E0),
    }


def exact_coupled_friedmann_forcing_bound_certificate():
    """Certify the coupled Friedmann--Raychaudhuri forcing bound.

    This is conditional on the positive-energy quadratic branch, with dark
    energy restricted to a cosmological constant.  Under the declared
    assumptions, rho_total +/- p_total are nonnegative, H is nonincreasing
    on an expanding forward interval, and G_force = 9*H_i**2/4.  Combining
    this with the relative energy certificate yields an O(sqrt(alpha))
    relative-field estimate.  Density and Hubble convergence remain
    unproved, and no DFM-Lambda-CDM manifold-overlap or lower-bound claim
    follows.
    """
    alpha, beta, mu, q, a, phi, G_N, H, H_i = sp.symbols(
        "alpha beta mu q a phi G_N H H_i",
        positive=True,
    )
    rho_b, rho_r, rho_lambda = sp.symbols(
        "rho_b rho_r rho_lambda",
        nonnegative=True,
    )
    phi_dot = sp.symbols("phi_dot", real=True)

    kinetic = alpha * phi_dot**2 / 2
    phase = q**2 / (2 * beta * a**6 * phi**2)
    mass = mu**2 * phi**2 / 2

    rho_dfm = kinetic + phase + mass
    p_dfm = kinetic + phase - mass
    rho_total = rho_b + rho_r + rho_lambda + rho_dfm
    p_total = rho_r / 3 - rho_lambda + p_dfm

    H_squared = (8 * sp.pi * G_N / 3) * rho_total
    H_dot = -4 * sp.pi * G_N * (rho_total + p_total)
    g = sp.Rational(3, 4) * (2 * H_dot + 3 * H_squared)

    rho_plus_pressure_expected = (
        rho_b
        + 4 * rho_r / 3
        + alpha * phi_dot**2
        + 2 * phase
    )
    rho_minus_pressure_expected = (
        rho_b
        + 2 * rho_r / 3
        + 2 * rho_lambda
        + 2 * mass
    )
    G_force = 9 * H_i**2 / 4

    return {
        "acceleration_pressure_identity": sp.simplify(
            2 * H_dot + 3 * H_squared + 8 * sp.pi * G_N * p_total
        ),
        "forcing_pressure_identity": sp.simplify(
            g + 6 * sp.pi * G_N * p_total
        ),
        "rho_plus_pressure_decomposition": sp.simplify(
            rho_total + p_total - rho_plus_pressure_expected
        ),
        "rho_minus_pressure_decomposition": sp.simplify(
            rho_total - p_total - rho_minus_pressure_expected
        ),
        "dominant_energy_product_identity": sp.simplify(
            rho_total**2
            - p_total**2
            - (rho_total + p_total) * (rho_total - p_total)
        ),
        "hubble_monotonicity_identity": sp.simplify(
            H_dot + 4 * sp.pi * G_N * rho_plus_pressure_expected
        ),
        "local_forcing_square_identity": sp.simplify(
            (9 * H_squared / 4) ** 2
            - g**2
            - (6 * sp.pi * G_N) ** 2
            * (rho_total**2 - p_total**2)
        ),
        "interval_forcing_majorant_identity": sp.simplify(
            G_force**2
            - g**2
            - 81 * (H_i**4 - H_squared**2) / 16
            - (6 * sp.pi * G_N) ** 2
            * (rho_total**2 - p_total**2)
        ),
    }


def exact_relative_energy_density_hubble_propagation_certificate():
    """Certify relative-energy propagation to density and Hubble bounds.

    This applies only to the positive-energy quadratic branch.  The
    comparator shares the same visible sectors and cosmological constant,
    and the circular dust normalization is fixed identically in both
    models.  The density excess is nonnegative.  A relative energy
    majorant B = O(alpha) gives density error O(alpha), while a positive
    lower bound for H_LCDM gives Hubble error O(alpha).

    This has not yet been propagated through D_H, D_M, D_V, or r_d.
    Existence of the complete prepared alpha-dependent solution family
    remains a separate analytical requirement.  No complete
    DFM-Lambda-CDM manifold-overlap or lower-bound claim follows yet.
    """
    alpha, mu, phi_c, y, H, H_i, G_N, H_lower, rho_common = (
        sp.symbols(
            "alpha mu phi_c y H H_i G_N H_lower rho_common",
            positive=True,
        )
    )
    E, B = sp.symbols("E B", nonnegative=True)
    y_dot = sp.symbols("y_dot", real=True)

    rho_cdm = mu**2 * phi_c**2
    phase = rho_cdm / (2 * y**2)
    mass = rho_cdm * y**2 / 2
    phi_dot = phi_c * (y_dot - 3 * H * y / 2)
    kinetic = alpha * phi_dot**2 / 2
    rho_dfm = kinetic + phase + mass
    delta_rho = rho_dfm - rho_cdm

    V = mu**2 * (y - y**-1) ** 2 / 2
    E_expression = alpha * y_dot**2 / 2 + V
    D_E = phi_c**2 * (
        2 * E_expression
        + 9 * alpha * H_i**2 / 2
        * (1 + E_expression / mu**2)
    )
    D_B = phi_c**2 * (
        2 * B
        + 9 * alpha * H_i**2 / 2 * (1 + B / mu**2)
    )

    density_decomposition = phi_c**2 * (
        V + alpha * (y_dot - 3 * H * y / 2) ** 2 / 2
    )
    density_majorant_remainder = phi_c**2 * (
        V
        + alpha * (y_dot + 3 * H * y / 2) ** 2 / 2
        + 9 * alpha * (H_i**2 - H**2) * y**2 / 4
        + 9 * alpha * H_i**2 / 4
        * (alpha * y_dot**2 / mu**2 + y**-2)
    )
    energy_substitution = phi_c**2 * (B - E_expression) * (
        2 + 9 * alpha * H_i**2 / (2 * mu**2)
    )
    relative_density_bound = (
        2 * B / mu**2
        + 9 * alpha * H_i**2 / (2 * mu**2)
        * (1 + B / mu**2)
    )

    kappa = 8 * sp.pi * G_N / 3
    H_DFM_squared = kappa * (rho_common + rho_dfm)
    H_LCDM_squared = kappa * (rho_common + rho_cdm)
    H_DFM = sp.sqrt(H_DFM_squared)
    H_LCDM = sp.sqrt(H_LCDM_squared)
    H_error_bound = kappa * D_B / (2 * H_lower)
    hubble_majorant_remainder = (
        kappa
        * (
            D_B * (H_DFM + H_LCDM - 2 * H_lower)
            + 2 * H_lower * (D_B - delta_rho)
        )
        / (2 * H_lower * (H_DFM + H_LCDM))
    )

    return {
        "density_excess_decomposition": sp.simplify(
            delta_rho - density_decomposition
        ),
        "density_energy_majorant_remainder": sp.simplify(
            D_E - delta_rho - density_majorant_remainder
        ),
        "energy_bound_substitution": sp.simplify(
            D_B - D_E - energy_substitution
        ),
        "relative_density_majorant": sp.simplify(
            D_B / rho_cdm - relative_density_bound
        ),
        "friedmann_squared_difference": sp.simplify(
            H_DFM_squared - H_LCDM_squared - kappa * delta_rho
        ),
        "hubble_square_root_identity": sp.simplify(
            H_DFM
            - H_LCDM
            - kappa * delta_rho / (H_DFM + H_LCDM)
        ),
        "hubble_majorant_remainder": sp.simplify(
            H_error_bound
            - (H_DFM - H_LCDM)
            - hubble_majorant_remainder
        ),
    }


def dark_energy_equation_of_state(
    N: float,
    parameters: ChargeReducedParameters,
) -> float:
    # CPL equation of state w(a)=w0+wa(1-a).
    _require_finite("N", N)
    return parameters.w0 + parameters.wa * (1.0 - math.exp(N))


def dark_energy_density(
    N: float,
    parameters: ChargeReducedParameters,
) -> float:
    # Present-day-normalized CPL dark-energy density.
    _require_finite("N", N)
    density_today = (
        parameters.Lambda
        / (8.0 * math.pi * parameters.G)
    )
    exponent = (
        -3.0 * (1.0 + parameters.w0 + parameters.wa) * N
        + 3.0 * parameters.wa * (math.exp(N) - 1.0)
    )
    return density_today * math.exp(exponent)


def dark_energy_pressure(
    N: float,
    parameters: ChargeReducedParameters,
) -> float:
    # Pressure of the CPL dark-energy carrier.
    return (
        dark_energy_equation_of_state(N, parameters)
        * dark_energy_density(N, parameters)
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
        + dark_energy_density(N, parameters)
    )

    return (
        (8.0 * math.pi * parameters.G / 3.0)
        * rho_total
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
    rho_dark_energy = np.empty_like(N)
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
        rho_dark_energy[index] = dark_energy_density(
            float(N_value),
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
        + (
            parameters.w0
            + parameters.wa * (1.0 - a)
        ) * rho_dark_energy
    )
    rho_total = (
        rho_m
        + rho_r
        + rho_dfm_mkc
        + rho_dark_energy
    )
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
        rho_dark_energy,
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
        rho_dark_energy=rho_dark_energy,
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

SPEED_OF_LIGHT_KM_S = 299_792.458
