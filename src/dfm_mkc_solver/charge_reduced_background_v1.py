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
from scipy.integrate import quad, solve_ivp


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

    if phi == 0.0:
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


def exact_dfm_antlia_tf_reduction_certificate(
) -> dict[str, sp.Expr]:
    """Exact DFM -> LRS/SFDM -> Gross-Pitaevskii/TF coefficient map.

    Natural units hbar=c=1 are used for the symbolic coefficient map.
    This certifies the algebraic reduction only; actual halo membership
    in the Thomas-Fermi regime is a separate inequality gate.
    """

    alpha, beta = sp.symbols(
        "alpha beta",
        positive=True,
    )
    m_phi_squared, lambda_phi = sp.symbols(
        "m_phi_squared lambda_phi",
        positive=True,
    )
    phi, dphi, dtheta = sp.symbols(
        "phi dphi dtheta",
        real=True,
    )
    rho, G = sp.symbols(
        "rho G",
        positive=True,
    )

    # Canonically normalized polar field:
    #
    # R = sqrt(alpha) phi
    # Theta = sqrt(beta/alpha) theta.
    R = sp.sqrt(alpha) * phi
    dR = sp.sqrt(alpha) * dphi
    dTheta = sp.sqrt(beta / alpha) * dtheta

    polar_kinetic_gap = sp.simplify(
        sp.Rational(1, 2)
        * (
            dR**2
            + R**2 * dTheta**2
        )
        - (
            sp.Rational(1, 2) * alpha * dphi**2
            + sp.Rational(1, 2)
            * beta
            * phi**2
            * dtheta**2
        )
    )

    # Canonical relativistic potential:
    #
    # V = 1/2 m^2 R^2 + 1/4 lambda_rel R^4.
    m_squared = sp.simplify(
        m_phi_squared / alpha
    )
    lambda_rel = sp.simplify(
        lambda_phi / alpha**2
    )

    potential_gap = sp.simplify(
        sp.Rational(1, 2)
        * m_squared
        * R**2
        + sp.Rational(1, 4)
        * lambda_rel
        * R**4
        - (
            sp.Rational(1, 2)
            * m_phi_squared
            * phi**2
            + sp.Rational(1, 4)
            * lambda_phi
            * phi**4
        )
    )

    # LRS normalization:
    #
    # psi_LRS = sqrt(m) Phi_DFM
    #
    # L_LRS =
    #   (1/(2m)) |d psi|^2
    #   - (m/2) |psi|^2
    #   - (g/2) |psi|^4.
    #
    # Matching the quartic term gives
    #
    #   g = lambda_rel/(2 m^2).
    g = sp.simplify(
        lambda_rel
        / (2 * m_squared)
    )

    expected_g = sp.simplify(
        lambda_phi
        / (
            2
            * alpha
            * m_phi_squared
        )
    )

    g_gap = sp.simplify(
        g - expected_g
    )

    # Antlia B uses g/m^2 as the self-interaction strength.
    g_over_m_squared = sp.simplify(
        g / m_squared
    )

    expected_g_over_m_squared = sp.simplify(
        lambda_phi
        / (
            2
            * m_phi_squared**2
        )
    )

    g_over_m_squared_gap = sp.simplify(
        g_over_m_squared
        - expected_g_over_m_squared
    )

    alpha_independence = sp.simplify(
        sp.diff(
            g_over_m_squared,
            alpha,
        )
    )

    beta_independence = sp.simplify(
        sp.diff(
            g_over_m_squared,
            beta,
        )
    )

    # Gross-Pitaevskii/Madelung self-interaction pressure:
    #
    # V_SI = (g/m^2) rho
    # P_SI = (g/(2m^2)) rho^2.
    V_si = sp.simplify(
        g * rho / m_squared
    )

    P_si = sp.simplify(
        g * rho**2
        / (2 * m_squared)
    )

    madelung_pressure_gap = sp.simplify(
        sp.diff(P_si, rho) / rho
        - sp.diff(V_si, rho)
    )

    # n=1 Thomas-Fermi polytrope:
    #
    # R_TF = pi sqrt(g/(4 pi G m^2)).
    r_tf_squared = sp.simplify(
        sp.pi
        * g
        / (
            4
            * G
            * m_squared
        )
    )

    expected_dfm_r_tf_squared = sp.simplify(
        sp.pi
        * lambda_phi
        / (
            8
            * G
            * m_phi_squared**2
        )
    )

    tf_radius_gap = sp.simplify(
        r_tf_squared
        - expected_dfm_r_tf_squared
    )

    # Antlia B reports R_TF < 0.18 kpc (68%) and
    # R_TF < 0.72 kpc (95%).  Equation (5) gives
    #
    #   g/m^2 proportional to R_TF^2.
    #
    # Therefore the 95% coupling corresponding to the reported
    # radius must be derived quadratically from the 68% pair.
    #
    # Source: arXiv:2307.13035, Eq. (5), Sect. 5.1.
    antlia_68_r_tf_kpc = sp.Rational(18, 100)
    antlia_95_r_tf_kpc = sp.Rational(72, 100)

    antlia_68_g_over_m2 = (
        sp.Rational(52, 10) * sp.Integer(10) ** -20
    )

    antlia_95_g_over_m2_reported = (
        sp.Rational(83, 10) * sp.Integer(10) ** -20
    )

    antlia_95_g_over_m2_from_radius = sp.simplify(
        antlia_68_g_over_m2
        * (
            antlia_95_r_tf_kpc
            / antlia_68_r_tf_kpc
        ) ** 2
    )

    antlia_95_reported_consistency_gap = sp.simplify(
        antlia_95_g_over_m2_from_radius
        - antlia_95_g_over_m2_reported
    )

    lrs_lower = (
        sp.Rational(95, 10) * sp.Integer(10) ** -19
    )

    interval_separation = sp.simplify(
        lrs_lower
        - antlia_95_g_over_m2_from_radius
    )

    return {
        "polar_kinetic_gap": polar_kinetic_gap,
        "potential_gap": potential_gap,
        "g_gap": g_gap,
        "g_over_m_squared_gap": g_over_m_squared_gap,
        "alpha_independence": alpha_independence,
        "beta_independence": beta_independence,
        "madelung_pressure_gap": madelung_pressure_gap,
        "tf_radius_gap": tf_radius_gap,
        "m_squared": m_squared,
        "lambda_rel": lambda_rel,
        "g": g,
        "g_over_m_squared": g_over_m_squared,
        "r_tf_squared": r_tf_squared,
        "antlia_95_g_over_m2_reported": (
            antlia_95_g_over_m2_reported
        ),
        "antlia_95_g_over_m2_from_radius": (
            antlia_95_g_over_m2_from_radius
        ),
        "antlia_95_reported_consistency_gap": (
            antlia_95_reported_consistency_gap
        ),
        "interval_separation": interval_separation,
    }


def antlia_eq12_tf_hierarchy_ratio(
    *,
    particle_mass_eV: float,
    minimum_halo_mass_solar: float,
    r_tf_kpc: float,
) -> float:
    """Dimensionless Thomas-Fermi hierarchy ratio from Antlia-B Eq. (12).

    Eq. (12) is equivalent to requiring

        H_TF =
            (m c^2 / 1e-21 eV)
            * (M_200,min / 1e9 M_sun)^(1/3)
            * (R_TF / 1 kpc)

        >> 1.

    This function returns H_TF only.  It deliberately does not choose
    a numerical meaning for the asymptotic symbol ">>".
    """

    for name, value in (
        ("particle_mass_eV", particle_mass_eV),
        ("minimum_halo_mass_solar", minimum_halo_mass_solar),
        ("r_tf_kpc", r_tf_kpc),
    ):
        _require_finite(name, value)

        if value <= 0.0:
            raise ValueError(
                f"{name} must be positive"
            )

    hierarchy_ratio = (
        particle_mass_eV / 1.0e-21
        * (
            minimum_halo_mass_solar / 1.0e9
        ) ** (1.0 / 3.0)
        * r_tf_kpc
    )

    _require_finite(
        "hierarchy_ratio",
        hierarchy_ratio,
    )

    return hierarchy_ratio


def exact_positive_lambda_charge_normalization_obstruction_certificate(
) -> dict[str, sp.Expr]:
    """Certify the obstruction to exact CDM rest-mass charge normalization.

    Consider the candidate sixth equality

        Q_theta * sqrt(m_phi_squared / beta) = rho_cdm0.

    If F_rho simultaneously requires the full DFM density to equal the same
    rho_cdm0 and rho_star = 0, then the exact density difference is a sum of
    nonnegative terms.  For lambda_phi > 0 and phi != 0 the quartic term is
    strictly positive, so the two equalities cannot hold simultaneously.

    This certificate does not modify the shooting closure.
    """

    alpha, beta, mu, q, phi, lambda_phi = sp.symbols(
        "alpha beta mu q phi lambda_phi",
        positive=True,
    )
    v = sp.symbols("v", real=True)

    kinetic = sp.Rational(1, 2) * alpha * v**2
    phase = q**2 / (2 * beta * phi**2)
    mass = sp.Rational(1, 2) * mu**2 * phi**2
    quartic = sp.Rational(1, 4) * lambda_phi * phi**4

    rho_dfm = kinetic + phase + mass + quartic

    rho_charge_rest_mass = q * mu / sp.sqrt(beta)

    am_gm_square = sp.Rational(1, 2) * (
        mu * phi
        - q / (sp.sqrt(beta) * phi)
    ) ** 2

    density_gap = sp.expand(
        rho_dfm - rho_charge_rest_mass
    )

    decomposed_gap = (
        kinetic
        + am_gm_square
        + quartic
    )

    return {
        "density_gap_factorization": sp.simplify(
            density_gap - decomposed_gap
        ),
        "phase_mass_am_gm_identity": sp.simplify(
            phase
            + mass
            - rho_charge_rest_mass
            - am_gm_square
        ),
        "quartic_positive_floor_identity": sp.simplify(
            decomposed_gap
            - kinetic
            - am_gm_square
            - quartic
        ),
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


def positive_lambda_lrs_bbn_nonrealization_certificate(
    unit_map: "DFMCDMUnitMap",
    *,
    alpha: float = 1.0,
    beta: float = 1.0,
    N_initial: float = -0.1,
    T_gamma_MeV: float = 1.0,
) -> dict[str, object]:
    """Certify non-realization of the prepared positive-lambda LRS family.

    Assumptions fixed by this theorem surface:

        rho_star = 0,
        alpha = beta = 1,
        late-time DFM density calibrated to the CDM target,
        v_initial = 0,
        initial point on the algebraic circular manifold,
        m_eV >= LRS_PARTICLE_MASS_LOWER_EV,
        LRS_SELF_INTERACTION_LOWER_EV_INV_CM3
            <= g/(m*c^2)^2
            <= LRS_SELF_INTERACTION_UPPER_EV_INV_CM3,
        repository BBN convention at T_gamma = 1 MeV.

    Prior exact certificates establish

        rho_exact(a) >= rho_circ(a),

    particle-mass independence after the z=m_phi_squared*phi_c^2
    reduction, and strict increase of rho_circ(BBN) with the LRS
    self-interaction strength.

    Therefore the global BBN minimum over the prepared LRS family
    occurs at the lower LRS coupling endpoint.  This function
    recomputes that minimum and fails closed unless it lies above
    the repository two-sigma BBN upper bound.
    """

    for name, value in (
        ("alpha", alpha),
        ("beta", beta),
        ("N_initial", N_initial),
        ("T_gamma_MeV", T_gamma_MeV),
    ):
        _require_finite(name, value)

    if alpha != 1.0:
        raise ValueError(
            "non-realization certificate currently requires alpha = 1"
        )

    if beta != 1.0:
        raise ValueError(
            "non-realization certificate currently requires beta = 1"
        )

    if N_initial >= 0.0:
        raise ValueError(
            "non-realization certificate requires N_initial < 0"
        )

    monotonicity = (
        exact_positive_lambda_bbn_lrs_monotonicity_certificate()
    )

    failed_monotonicity = {
        name: sp.simplify(residual)
        for name, residual in monotonicity.items()
        if sp.simplify(residual) != 0
    }

    if failed_monotonicity:
        raise RuntimeError(
            "BBN-LRS monotonicity certificate is not closed"
        )

    m2_floor = minimum_m_phi_squared_from_particle_mass(
        unit_map=unit_map,
        alpha=alpha,
        particle_mass_lower_eV=LRS_PARTICLE_MASS_LOWER_EV,
    )

    lambda_lower, lambda_same = (
        dfm_lambda_phi_interval_from_lrs(
            unit_map=unit_map,
            m_phi_squared=m2_floor,
            lower_eV_inv_cm3=(
                LRS_SELF_INTERACTION_LOWER_EV_INV_CM3
            ),
            upper_eV_inv_cm3=(
                LRS_SELF_INTERACTION_LOWER_EV_INV_CM3
            ),
        )
    )

    if not math.isclose(
        lambda_lower,
        lambda_same,
        rel_tol=2.0e-15,
        abs_tol=0.0,
    ):
        raise RuntimeError(
            "lower LRS coupling did not map to a unique lambda_phi"
        )

    a_initial = math.exp(N_initial)

    rho_initial = (
        unit_map.rho_cdm0_code
        * math.exp(-3.0 * N_initial)
    )

    kappa = (
        lambda_lower
        / m2_floor**2
    )

    z_initial = (
        2.0
        * rho_initial
        / (
            1.0
            + math.sqrt(
                1.0
                + 3.0
                * kappa
                * rho_initial
            )
        )
    )

    x_initial = (
        z_initial
        / m2_floor
    )

    Q_theta = math.sqrt(
        beta
        * a_initial**6
        / m2_floor
        * z_initial**2
        * (
            1.0
            + kappa
            * z_initial
        )
    )

    reference = build_bbn_thermodynamic_reference(
        unit_map,
        T_gamma_MeV=T_gamma_MeV,
    )

    if reference.a >= a_initial:
        raise ValueError(
            "BBN surface must precede the prepared initial surface"
        )

    x_bbn = circular_phi_squared_positive_root(
        a=reference.a,
        beta=beta,
        m_phi_squared=m2_floor,
        lambda_phi=lambda_lower,
        Q_theta=Q_theta,
    )

    rho_circ_bbn, _ = circular_energy_density_pressure(
        a=reference.a,
        beta=beta,
        rho_star=0.0,
        m_phi_squared=m2_floor,
        lambda_phi=lambda_lower,
        Q_theta=Q_theta,
    )

    rho_one_neutrino_species = (
        reference.rho_gamma_code
        * (7.0 / 8.0)
        * (
            reference.T_nu_MeV
            / reference.T_gamma_MeV
        ) ** 4
    )

    if rho_one_neutrino_species <= 0.0:
        raise RuntimeError(
            "one-neutrino-species BBN density must be positive"
        )

    delta_rho_lower = (
        rho_circ_bbn
        - reference.rho_cdm_reference_code
    )

    n_eff_global_lower = (
        STANDARD_BBN_N_NU
        + delta_rho_lower
        / rho_one_neutrino_species
    )

    bbn_upper_2sigma = (
        BBN_N_EFF_TARGET
        + 2.0 * BBN_N_EFF_SIGMA
    )

    exclusion_margin = (
        n_eff_global_lower
        - bbn_upper_2sigma
    )

    if exclusion_margin <= 0.0:
        raise RuntimeError(
            "positive-lambda LRS family is not excluded by the "
            "repository two-sigma BBN criterion"
        )

    return {
        "theorem": (
            "prepared positive-lambda LRS-family BBN non-realization"
        ),
        "rho_star": 0.0,
        "alpha": alpha,
        "beta": beta,
        "N_initial": N_initial,
        "T_gamma_MeV": T_gamma_MeV,
        "a_bbn": reference.a,
        "N_bbn": reference.N,
        "particle_mass_lower_eV": (
            LRS_PARTICLE_MASS_LOWER_EV
        ),
        "lrs_strength_lower_eV_inv_cm3": (
            LRS_SELF_INTERACTION_LOWER_EV_INV_CM3
        ),
        "lrs_strength_upper_eV_inv_cm3": (
            LRS_SELF_INTERACTION_UPPER_EV_INV_CM3
        ),
        "m_phi_squared_floor": m2_floor,
        "lambda_phi_at_global_minimum": lambda_lower,
        "kappa_at_global_minimum": kappa,
        "x_initial_at_global_minimum": x_initial,
        "Q_theta_at_global_minimum": Q_theta,
        "x_bbn_at_global_minimum": x_bbn,
        "rho_circ_bbn_global_minimum": rho_circ_bbn,
        "rho_cdm_reference_bbn": (
            reference.rho_cdm_reference_code
        ),
        "n_eff_global_lower": n_eff_global_lower,
        "bbn_upper_2sigma": bbn_upper_2sigma,
        "exclusion_margin": exclusion_margin,
        "mass_independent": True,
        "global_minimum_at_lrs_lower_coupling": True,
        "rho_exact_gte_rho_circ": True,
        "excluded_2sigma": True,
    }


def exact_positive_lambda_bbn_lrs_monotonicity_certificate(
) -> dict[str, sp.Expr]:
    """Certify mass-independence and coupling monotonicity of rho_circ.

    Define

        kappa = lambda_phi / m_phi_squared^2,
        z     = m_phi_squared * phi_c^2,
        t     = kappa*z.

    Then

        rho_circ = z + 3*kappa*z^2/4
                 = f(t)/kappa,

        f(t) = t + 3*t^2/4,

    while the circular charge relation is proportional to

        z^2*(1+kappa*z)
          = h(t)/kappa^2,

        h(t) = t^2*(1+t).

    Between two scale factors the common mass and kappa factors
    cancel, giving

        h(t_f) = A*h(t_i),

        A = (a_i/a_f)^6.

    The density ratio is therefore

        rho_f/rho_i = f(t_f)/f(t_i).

    Its logarithmic elasticity with respect to h is

        E(t) = d ln(f) / d ln(h)
             = 2*(1+t)/(4+3*t),

    and

        E'(t) = 2/(4+3*t)^2 > 0.

    For A>1, h strictly increasing implies t_f>t_i, hence

        E(t_f)-E(t_i)
          = 2*(t_f-t_i)
            /[(4+3*t_f)*(4+3*t_i)] > 0.

    Thus rho_f/rho_i increases with kappa. Since the physical
    LRS strength is proportional to kappa, the smallest BBN
    circular density occurs at the lower LRS coupling endpoint.

    All explicit m_phi_squared dependence cancels.
    """

    t, t_i, t_f = sp.symbols(
        "t t_i t_f",
        positive=True,
    )

    kappa, z, m2 = sp.symbols(
        "kappa z m2",
        positive=True,
    )

    f = (
        t
        + sp.Rational(3, 4) * t**2
    )

    h = (
        t**2 * (1 + t)
    )

    rho_z = (
        z
        + sp.Rational(3, 4)
        * kappa
        * z**2
    )

    charge_z = (
        z**2
        * (1 + kappa * z)
        / m2
    )

    f_from_z = (
        f.subs(t, kappa * z)
        / kappa
    )

    h_from_z = (
        h.subs(t, kappa * z)
        / (
            m2 * kappa**2
        )
    )

    elasticity = sp.simplify(
        (sp.diff(f, t) / f)
        / (sp.diff(h, t) / h)
    )

    expected_elasticity = (
        2 * (1 + t)
        / (4 + 3 * t)
    )

    elasticity_derivative = sp.diff(
        expected_elasticity,
        t,
    )

    expected_elasticity_derivative = (
        2
        / (4 + 3 * t)**2
    )

    endpoint_elasticity_gap = sp.factor(
        expected_elasticity.subs(t, t_f)
        - expected_elasticity.subs(t, t_i)
    )

    expected_endpoint_gap = (
        2
        * (t_f - t_i)
        / (
            (4 + 3 * t_f)
            * (4 + 3 * t_i)
        )
    )

    return {
        "density_scale_reduction": sp.factor(
            rho_z - f_from_z
        ),
        "charge_scale_reduction": sp.factor(
            charge_z - h_from_z
        ),
        "h_derivative_identity": sp.factor(
            sp.diff(h, t)
            - t * (2 + 3 * t)
        ),
        "f_derivative_identity": sp.factor(
            sp.diff(f, t)
            - (
                1
                + sp.Rational(3, 2) * t
            )
        ),
        "elasticity_identity": sp.factor(
            elasticity
            - expected_elasticity
        ),
        "elasticity_derivative_identity": sp.factor(
            elasticity_derivative
            - expected_elasticity_derivative
        ),
        "endpoint_elasticity_gap_identity": sp.factor(
            endpoint_elasticity_gap
            - expected_endpoint_gap
        ),
    }


def exact_positive_lambda_circular_density_lower_bound_certificate(
) -> dict[str, sp.Expr]:
    """Certify rho_exact >= rho_circ at every fixed scale factor.

    For x = phi^2 > 0 define

        U_eff(x)
          = C/(2*x)
            + m2*x/2
            + lambda*x^2/4
            + rho_star,

        C = Q_theta^2/(beta*a^6) > 0.

    The circular root x_c satisfies

        C = m2*x_c^2 + lambda*x_c^3.

    Since

        U_eff''(x) = C/x^3 + lambda/2 > 0,

    x_c is the unique global minimum on x>0.

    The full finite-alpha density is

        rho_exact
          = alpha*phi_dot^2/2 + U_eff(phi^2),

    so

        rho_exact >= rho_circ

    without any tracking or averaging assumption.
    """

    x, x_c = sp.symbols(
        "x x_c",
        positive=True,
    )

    alpha, m2, lambda_phi, C = sp.symbols(
        "alpha m2 lambda_phi C",
        positive=True,
    )

    rho_star, phi_dot = sp.symbols(
        "rho_star phi_dot",
        real=True,
    )

    U_eff = (
        C / (2 * x)
        + m2 * x / 2
        + lambda_phi * x**2 / 4
        + rho_star
    )

    dU = sp.diff(U_eff, x)
    ddU = sp.diff(U_eff, x, 2)

    circular_relation = (
        C
        - m2 * x_c**2
        - lambda_phi * x_c**3
    )

    stationary_at_circular = sp.factor(
        dU.subs(
            {
                x: x_c,
                C: (
                    m2 * x_c**2
                    + lambda_phi * x_c**3
                ),
            }
        )
    )

    rho_circ_from_minimum = sp.factor(
        U_eff.subs(
            {
                x: x_c,
                C: (
                    m2 * x_c**2
                    + lambda_phi * x_c**3
                ),
            }
        )
    )

    expected_rho_circ = (
        rho_star
        + m2 * x_c
        + sp.Rational(3, 4)
        * lambda_phi
        * x_c**2
    )

    exact_density = (
        alpha * phi_dot**2 / 2
        + U_eff
    )

    kinetic_gap = sp.factor(
        exact_density - U_eff
    )

    return {
        "circular_relation_identity": sp.factor(
            circular_relation.subs(
                C,
                m2 * x_c**2
                + lambda_phi * x_c**3,
            )
        ),
        "stationary_at_circular": stationary_at_circular,
        "strict_convexity_identity": sp.factor(
            ddU
            - (
                C / x**3
                + lambda_phi / 2
            )
        ),
        "circular_minimum_density_identity": sp.factor(
            rho_circ_from_minimum
            - expected_rho_circ
        ),
        "nonnegative_kinetic_identity": sp.factor(
            kinetic_gap
            - alpha * phi_dot**2 / 2
        ),
    }


def exact_positive_lambda_quartic_density_pressure_bridge_certificate(
) -> dict[str, sp.Expr]:
    """Certify exact finite-alpha rho/p deviations from the circular layer.

    Put

        x = phi_c^2,
        L = lambda_phi*x,
        s = phi_c_dot/phi_c,
        phi = phi_c*y.

    Then

        phi_dot = phi_c*(y_dot + s*y).

    Relative to the algebraic circular density and pressure,

        Delta rho
          = x*E_rel
            + alpha*x*s*y*y_dot
            + alpha*x*s^2*y^2/2,

    where

        E_rel = alpha*y_dot^2/2 + V_rel.

    The pressure satisfies the exact relation

        Delta p
          = Delta rho
            - x*(y^2-1)
              *(L*y^2 + L + 2*m2)/2.

    Thus density inherits the quadratic relative-energy control,
    while pressure contains one additional term linear in the
    displacement from the circular manifold.
    """

    alpha, x, m2, L, y = sp.symbols(
        "alpha x m2 L y",
        positive=True,
    )

    rho_star = sp.symbols(
        "rho_star",
        real=True,
    )

    s, y_dot = sp.symbols(
        "s y_dot",
        real=True,
    )

    kinetic = (
        sp.Rational(1, 2)
        * alpha
        * x
        * (y_dot + s * y)**2
    )

    phase = (
        sp.Rational(1, 2)
        * x
        * (m2 + L)
        * y**-2
    )

    potential = (
        rho_star
        + sp.Rational(1, 2)
        * m2
        * x
        * y**2
        + sp.Rational(1, 4)
        * L
        * x
        * y**4
    )

    rho_exact = (
        kinetic
        + phase
        + potential
    )

    p_exact = (
        kinetic
        + phase
        - potential
    )

    rho_circ = (
        rho_star
        + m2 * x
        + sp.Rational(3, 4) * L * x
    )

    p_circ = (
        -rho_star
        + sp.Rational(1, 4) * L * x
    )

    quadratic_shape = (
        sp.Rational(1, 2)
        * (
            y**2
            + y**-2
            - 2
        )
    )

    quartic_shape = (
        sp.Rational(1, 4) * y**4
        + sp.Rational(1, 2) * y**-2
        - sp.Rational(3, 4)
    )

    V_rel = (
        m2 * quadratic_shape
        + L * quartic_shape
    )

    E_rel = (
        sp.Rational(1, 2)
        * alpha
        * y_dot**2
        + V_rel
    )

    delta_rho = sp.expand(
        rho_exact - rho_circ
    )

    delta_p = sp.expand(
        p_exact - p_circ
    )

    reduced_delta_rho = (
        x * E_rel
        + alpha * x * s * y * y_dot
        + sp.Rational(1, 2)
        * alpha
        * x
        * s**2
        * y**2
    )

    pressure_correction = (
        sp.Rational(1, 2)
        * x
        * (y**2 - 1)
        * (
            L * y**2
            + L
            + 2 * m2
        )
    )

    return {
        "density_decomposition_identity": sp.factor(
            delta_rho
            - reduced_delta_rho
        ),
        "pressure_from_density_identity": sp.factor(
            delta_p
            - (
                delta_rho
                - pressure_correction
            )
        ),
        "circular_density_identity": sp.factor(
            rho_exact.subs(
                {
                    y: 1,
                    y_dot: -s,
                }
            )
            - rho_circ
        ),
        "circular_pressure_identity": sp.factor(
            p_exact.subs(
                {
                    y: 1,
                    y_dot: -s,
                }
            )
            - p_circ
        ),
    }


def exact_positive_lambda_quartic_initial_energy_gronwall_certificate(
) -> dict[str, sp.Expr]:
    """Certify the prepared-seed initial energy and Gronwall solution.

    On the circular manifold let

        L = lambda_phi*phi_c^2,

        u = d(log(phi_c))/dN
          = -3*(m2+L)/(2*m2+3*L).

    At the prepared shooting seed

        y_i = 1,
        phi_dot_i = 0,

    so

        y_dot_i = -phi_c_dot/phi_c
                = -H_i*u_i
                = 3*H_i*(m2+L_i)/(2*m2+3*L_i).

    Since V_rel(1)=0,

        E_i
          = alpha*y_dot_i^2/2,

        e_i
          = E_i/m2
          = 9*alpha*H_i^2*(m2+L_i)^2
            /[2*m2*(2*m2+3*L_i)^2].

    If

        de/dN <= K*(e+1),
        K <= K_max,

    then the comparison majorant is

        e_bar(N)
          = (1+e_i)*exp(K_max*(N-N_i)) - 1.
    """

    alpha, H_i, m2, L_i = sp.symbols(
        "alpha H_i m2 L_i",
        positive=True,
    )

    K_max = sp.symbols(
        "K_max",
        nonnegative=True,
    )

    N, N_i = sp.symbols(
        "N N_i",
        real=True,
    )

    u_i = (
        -3
        * (m2 + L_i)
        / (2 * m2 + 3 * L_i)
    )

    y_dot_i = -H_i * u_i

    expected_y_dot_i = (
        3
        * H_i
        * (m2 + L_i)
        / (2 * m2 + 3 * L_i)
    )

    E_i = (
        sp.Rational(1, 2)
        * alpha
        * y_dot_i**2
    )

    e_i = sp.simplify(
        E_i / m2
    )

    expected_e_i = (
        9
        * alpha
        * H_i**2
        * (m2 + L_i)**2
        / (
            2
            * m2
            * (2 * m2 + 3 * L_i)**2
        )
    )

    e_bar = (
        (1 + e_i)
        * sp.exp(
            K_max
            * (N - N_i)
        )
        - 1
    )

    comparison_ode_residual = (
        sp.diff(e_bar, N)
        - K_max * (e_bar + 1)
    )

    comparison_initial_residual = (
        e_bar.subs(N, N_i)
        - e_i
    )

    return {
        "prepared_seed_y_dot_identity": sp.factor(
            y_dot_i
            - expected_y_dot_i
        ),
        "prepared_seed_energy_identity": sp.factor(
            e_i
            - expected_e_i
        ),
        "comparison_ode_identity": sp.factor(
            comparison_ode_residual
        ),
        "comparison_initial_identity": sp.factor(
            comparison_initial_residual
        ),
    }


def exact_positive_lambda_quartic_uniform_young_envelope_certificate(
) -> dict[str, sp.Expr]:
    """Certify the analytic envelope used for uniform A/H control.

    Put

        r = lambda_phi*phi_c^2/m_phi_squared > 0,
        q_H = -H_dot/H^2.

    Then

        gamma/H = 3*r/(2 + 3*r),

    and

        g_q/H^2
          = -3*(1+r)/(2+3*r)*q_H
            + 9*(1+r)*(2+9*r+6*r^2)/(2+3*r)^3.

    For a nonnegative cosmological constant and matter/radiation/
    circular components with w <= 1/3,

        0 <= q_H <= 2.

    The two coefficient estimates

        (1+r)/(2+3*r) <= 1/2,

        (2+9*r+6*r^2)/(2+3*r)^2 <= 1

    give the conservative exact envelope

        abs(g_q/H^2) <= 15/2.

    Also r_N < 0, so

        (2+3*r)/(3*r)

    increases with N.  Since H decreases on the expanding branch,
    a uniform interval bound is therefore

        A/H
          <= alpha*H_i^2/m2
             *(15/2)^2
             *(2+3*r_f)/(3*r_f),

    where H_i is the initial Hubble value and r_f is the final
    circular r value.
    """

    r, q_H = sp.symbols(
        "r q_H",
        nonnegative=True,
    )

    m2 = sp.symbols(
        "m2",
        positive=True,
    )

    first_ratio = (
        (1 + r)
        / (2 + 3 * r)
    )

    second_ratio = (
        (2 + 9 * r + 6 * r**2)
        / (2 + 3 * r)**2
    )

    first_gap = (
        sp.Rational(1, 2)
        - first_ratio
    )

    expected_first_gap = (
        r
        / (
            2
            * (2 + 3 * r)
        )
    )

    second_gap = (
        1
        - second_ratio
    )

    expected_second_gap = (
        2 + 3 * r + 3 * r**2
    ) / (
        2 + 3 * r
    )**2

    circular_w = (
        r
        / (4 + 3 * r)
    )

    circular_w_gap = (
        sp.Rational(1, 3)
        - circular_w
    )

    expected_circular_w_gap = (
        4
        / (
            3
            * (4 + 3 * r)
        )
    )

    r_N = (
        -6
        * r
        * (1 + r)
        / (2 + 3 * r)
    )

    inverse_damping_factor = (
        (2 + 3 * r)
        / (3 * r)
    )

    inverse_damping_r_derivative = sp.diff(
        inverse_damping_factor,
        r,
    )

    expected_inverse_damping_r_derivative = (
        -sp.Rational(2, 3)
        / r**2
    )

    forcing_second_term = (
        9
        * first_ratio
        * second_ratio
    )

    forcing_coarse_bound = (
        sp.Rational(9, 2)
    )

    total_forcing_bound = (
        sp.Rational(3, 2) * 2
        + forcing_coarse_bound
    )

    return {
        "first_ratio_gap_identity": sp.factor(
            first_gap
            - expected_first_gap
        ),
        "second_ratio_gap_identity": sp.factor(
            second_gap
            - expected_second_gap
        ),
        "circular_w_le_one_third_identity": sp.factor(
            circular_w_gap
            - expected_circular_w_gap
        ),
        "r_N_identity": sp.factor(
            r_N
            + 6
            * r
            * (1 + r)
            / (2 + 3 * r)
        ),
        "inverse_damping_derivative_identity": sp.factor(
            inverse_damping_r_derivative
            - expected_inverse_damping_r_derivative
        ),
        "forcing_second_term_factorization": sp.factor(
            forcing_second_term
            - 9
            * first_ratio
            * second_ratio
        ),
        "total_forcing_bound_identity": sp.factor(
            total_forcing_bound
            - sp.Rational(15, 2)
        ),
    }


def exact_positive_lambda_quartic_relative_energy_young_majorant_certificate(
) -> dict[str, sp.Expr]:
    """Certify a coercive Young majorant for quartic tracking energy.

    Starting from

        E_dot
          = -alpha*gamma*y_dot^2
            + alpha*g_q*y*y_dot
            + L_dot*W(y),

    with gamma > 0 and L_dot*W(y) <= 0, Young's inequality gives

        alpha*g_q*y*y_dot
          <= alpha*gamma*y_dot^2/2
             + alpha*g_q^2*y^2/(2*gamma).

    The positive relative potential also gives

        y^2 <= 2 + 2*V_rel/m2
             <= 2 + 2*E_rel/m2.

    Therefore

        E_dot
          <= -alpha*gamma*y_dot^2/2
             + alpha*g_q^2/gamma
               * (1 + E_rel/m2),

    and hence

        E_dot <= A*E_rel + B,

        A = alpha*g_q^2/(gamma*m2),
        B = alpha*g_q^2/gamma.

    This is an exact differential majorant.  It does not assert
    that A or B are small on the physical branch.
    """

    alpha, H, m2, ell, y = sp.symbols(
        "alpha H m2 ell y",
        positive=True,
    )

    y_dot, g_q = sp.symbols(
        "y_dot g_q",
        real=True,
    )

    denominator = 2 * m2 + 3 * ell

    gamma = (
        3 * H * ell
        / denominator
    )

    ell_dot = (
        -6
        * H
        * ell
        * (m2 + ell)
        / denominator
    )

    quartic_shape = (
        sp.Rational(1, 4) * y**4
        + sp.Rational(1, 2) * y**-2
        - sp.Rational(3, 4)
    )

    quartic_shape_factored = (
        (y**2 - 1)**2
        * (y**2 + 2)
        / (4 * y**2)
    )

    quadratic_shape = (
        sp.Rational(1, 2)
        * (
            y**2
            + y**-2
            - 2
        )
    )

    potential = (
        m2 * quadratic_shape
        + ell * quartic_shape
    )

    energy = (
        sp.Rational(1, 2)
        * alpha
        * y_dot**2
        + potential
    )

    energy_dot = (
        -alpha * gamma * y_dot**2
        + alpha * g_q * y * y_dot
        + ell_dot * quartic_shape
    )

    young_upper = (
        sp.Rational(1, 2)
        * alpha
        * gamma
        * y_dot**2
        + alpha
        * g_q**2
        * y**2
        / (2 * gamma)
    )

    young_gap = (
        young_upper
        - alpha * g_q * y * y_dot
    )

    expected_young_gap = (
        alpha
        * (
            gamma * y_dot
            - g_q * y
        )**2
        / (2 * gamma)
    )

    y_coercive_gap = (
        2
        + 2 * potential / m2
        - y**2
    )

    expected_y_coercive_gap = (
        y**-2
        + 2 * ell * quartic_shape / m2
    )

    energy_coercive_gap = (
        2
        + 2 * energy / m2
        - y**2
    )

    expected_energy_coercive_gap = (
        y**-2
        + alpha * y_dot**2 / m2
        + 2 * ell * quartic_shape / m2
    )

    majorant = (
        -sp.Rational(1, 2)
        * alpha
        * gamma
        * y_dot**2
        + alpha
        * g_q**2
        / gamma
        * (
            1
            + energy / m2
        )
    )

    gronwall_A = (
        alpha
        * g_q**2
        / (gamma * m2)
    )

    gronwall_B = (
        alpha
        * g_q**2
        / gamma
    )

    expected_majorant = (
        -sp.Rational(1, 2)
        * alpha
        * gamma
        * y_dot**2
        + gronwall_A * energy
        + gronwall_B
    )

    majorant_gap = sp.simplify(
        majorant - energy_dot
    )

    expected_majorant_gap = (
        expected_young_gap
        + alpha
        * g_q**2
        / (2 * gamma)
        * energy_coercive_gap
        - ell_dot * quartic_shape
    )

    return {
        "quartic_shape_factorization": sp.factor(
            quartic_shape
            - quartic_shape_factored
        ),
        "young_square_identity": sp.factor(
            young_gap
            - expected_young_gap
        ),
        "potential_y2_coercivity_identity": sp.factor(
            y_coercive_gap
            - expected_y_coercive_gap
        ),
        "energy_y2_coercivity_identity": sp.factor(
            energy_coercive_gap
            - expected_energy_coercive_gap
        ),
        "majorant_decomposition_identity": sp.factor(
            majorant
            - expected_majorant
        ),
        "majorant_gap_positive_decomposition": sp.factor(
            majorant_gap
            - expected_majorant_gap
        ),
        "gronwall_A_identity": sp.factor(
            gronwall_A
            - alpha
            * g_q**2
            * denominator
            / (
                3
                * H
                * ell
                * m2
            )
        ),
        "gronwall_B_identity": sp.factor(
            gronwall_B
            - alpha
            * g_q**2
            * denominator
            / (
                3
                * H
                * ell
            )
        ),
    }


def exact_positive_lambda_quartic_relative_energy_derivative_certificate(
) -> dict[str, sp.Expr]:
    """Certify the exact positive-lambda relative-energy derivative.

    For the quartic relative equation

        alpha*(y_ddot + gamma*y_dot)
        + dV_rel/dy
        - alpha*g_q*y
        = 0,

    define

        E_rel = alpha*y_dot^2/2 + V_rel(y, L),

        L = lambda_phi*phi_c^2,

        gamma = 3*H*L/(2*m2 + 3*L).

    Since

        dL/dt
          = -6*H*L*(m2 + L)/(2*m2 + 3*L),

    the exact energy identity is

        dE_rel/dt
          = -alpha*gamma*y_dot^2
            + alpha*g_q*y*y_dot
            + L_dot*W(y),

    where

        W(y)
          = y^4/4 + y^-2/2 - 3/4
          = (y^2 - 1)^2*(y^2 + 2)/(4*y^2)
          >= 0.

    Thus for H>0, m2>0, L>0, y>0, the explicit
    time-dependent quartic-potential contribution satisfies

        L_dot*W(y) <= 0.

    The new quartic time-dependence is therefore dissipative.
    Only the moving-manifold forcing alpha*g_q*y*y_dot can
    inject relative energy.

    This certificate does not yet bound that forcing term.
    """

    alpha, H, m2, ell, y = sp.symbols(
        "alpha H m2 ell y",
        positive=True,
    )

    y_dot, y_ddot, g_q = sp.symbols(
        "y_dot y_ddot g_q",
        real=True,
    )

    denominator = (
        2 * m2
        + 3 * ell
    )

    gamma = (
        3 * H * ell
        / denominator
    )

    ell_dot = (
        -6
        * H
        * ell
        * (m2 + ell)
        / denominator
    )

    quadratic_shape = (
        sp.Rational(1, 2)
        * (
            y**2
            + y**-2
            - 2
        )
    )

    quartic_shape = (
        sp.Rational(1, 4) * y**4
        + sp.Rational(1, 2) * y**-2
        - sp.Rational(3, 4)
    )

    relative_potential = (
        m2 * quadratic_shape
        + ell * quartic_shape
    )

    restoring_force = sp.diff(
        relative_potential,
        y,
    )

    relative_equation = (
        alpha
        * (
            y_ddot
            + gamma * y_dot
        )
        + restoring_force
        - alpha * g_q * y
    )

    y_ddot_on_shell = (
        -gamma * y_dot
        - restoring_force / alpha
        + g_q * y
    )

    energy_dot = (
        alpha * y_dot * y_ddot
        + restoring_force * y_dot
        + ell_dot * quartic_shape
    )

    energy_dot_on_shell = sp.simplify(
        energy_dot.subs(
            y_ddot,
            y_ddot_on_shell,
        )
    )

    expected_energy_dot = (
        -alpha * gamma * y_dot**2
        + alpha * g_q * y * y_dot
        + ell_dot * quartic_shape
    )

    quartic_shape_factored = (
        (y**2 - 1)**2
        * (y**2 + 2)
        / (4 * y**2)
    )

    quadratic_shape_factored = (
        sp.Rational(1, 2)
        * (y - y**-1)**2
    )

    explicit_quartic_dissipation = (
        ell_dot * quartic_shape
    )

    expected_explicit_quartic_dissipation = (
        -sp.Rational(3, 2)
        * H
        * ell
        * (m2 + ell)
        / denominator
        * (
            (y**2 - 1)**2
            * (y**2 + 2)
            / y**2
        )
    )

    return {
        "relative_equation_on_shell": sp.factor(
            relative_equation.subs(
                y_ddot,
                y_ddot_on_shell,
            )
        ),
        "energy_derivative_identity": sp.factor(
            energy_dot_on_shell
            - expected_energy_dot
        ),
        "quartic_shape_nonnegative_factorization": sp.factor(
            quartic_shape
            - quartic_shape_factored
        ),
        "quadratic_shape_nonnegative_factorization": sp.factor(
            quadratic_shape
            - quadratic_shape_factored
        ),
        "explicit_quartic_dissipation_factorization": sp.factor(
            explicit_quartic_dissipation
            - expected_explicit_quartic_dissipation
        ),
        "energy_at_circular_manifold": sp.factor(
            relative_potential.subs(y, 1)
        ),
        "quartic_shape_at_circular_manifold": sp.factor(
            quartic_shape.subs(y, 1)
        ),
        "restoring_force_at_circular_manifold": sp.factor(
            restoring_force.subs(y, 1)
        ),
    }


def exact_positive_lambda_quartic_relative_tracking_certificate(
) -> dict[str, sp.Expr]:
    """Certify the exact positive-lambda relative tracking equation.

    The algebraic circular manifold is

        m2*phi_c^4 + lambda*phi_c^6
            = Q_theta^2/(beta*a^6).

    With

        y = phi/phi_c,
        L = lambda*phi_c^2,

    implicit differentiation gives

        d(log(phi_c))/dN
          = -3*(m2 + L)/(2*m2 + 3*L).

    The exact finite-alpha relative radial equation is

        alpha*(y_ddot + gamma*y_dot)
        + dV_rel/dy
        - alpha*g_q*y
        = 0,

    where

        gamma
          = 3*H*L/(2*m2 + 3*L),

        dV_rel/dy
          = m2*(y - y^-3)
            + L*(y^3 - y^-3),

    and g_q contains the exact acceleration of the moving
    quartic circular manifold.

    This certificate proves identities only.  It does not yet
    provide an energy majorant or a bound on F_rho or F_w.
    """

    alpha, beta, m2, lambda_phi = sp.symbols(
        "alpha beta m2 lambda_phi",
        positive=True,
    )
    q, a, phi_c, y = sp.symbols(
        "q a phi_c y",
        positive=True,
    )
    H = sp.symbols(
        "H",
        positive=True,
    )
    H_dot, y_dot, y_ddot = sp.symbols(
        "H_dot y_dot y_ddot",
        real=True,
    )

    ell_symbol = sp.symbols(
        "ell_symbol",
        positive=True,
    )

    u_symbol = (
        -3
        * (m2 + ell_symbol)
        / (2 * m2 + 3 * ell_symbol)
    )

    ell_N_symbol = (
        2 * u_symbol * ell_symbol
    )

    u_N_symbol = sp.simplify(
        sp.diff(
            u_symbol,
            ell_symbol,
        )
        * ell_N_symbol
    )

    ell = lambda_phi * phi_c**2

    u = sp.simplify(
        u_symbol.subs(
            ell_symbol,
            ell,
        )
    )

    ell_N = sp.simplify(
        ell_N_symbol.subs(
            ell_symbol,
            ell,
        )
    )

    u_N = sp.simplify(
        u_N_symbol.subs(
            ell_symbol,
            ell,
        )
    )

    denominator = (
        2 * m2
        + 3 * ell
    )

    expected_ell_N = (
        -6
        * ell
        * (m2 + ell)
        / denominator
    )

    expected_u_N = (
        -18
        * m2
        * ell
        * (m2 + ell)
        / denominator**3
    )

    phi_c_N = u * phi_c

    circular_manifold_N_derivative = (
        (
            4 * m2 * phi_c**3
            + 6 * lambda_phi * phi_c**5
        )
        * phi_c_N
        + 6 * q**2 / (beta * a**6)
    )

    circular_manifold_N_derivative = (
        circular_manifold_N_derivative.subs(
            q**2 / (beta * a**6),
            m2 * phi_c**4
            + lambda_phi * phi_c**6,
        )
    )

    phi_c_dot_over_phi_c = (
        H * u
    )

    phi_c_ddot_over_phi_c = sp.simplify(
        u * H_dot
        + H**2 * u_N
        + H**2 * u**2
    )

    gamma = sp.simplify(
        H * (3 + 2 * u)
    )

    expected_gamma = (
        3
        * H
        * ell
        / denominator
    )

    g_quartic = sp.simplify(
        -(
            u * H_dot
            + H**2
            * (
                u_N
                + u**2
                + 3 * u
            )
        )
    )

    expected_g_quartic = (
        3
        * (m2 + ell)
        * H_dot
        / denominator
        + 9
        * (m2 + ell)
        * (
            2 * m2**2
            + 9 * m2 * ell
            + 6 * ell**2
        )
        * H**2
        / denominator**3
    )

    restoring_force = (
        m2 * (y - y**-3)
        + ell * (y**3 - y**-3)
    )

    relative_potential = (
        sp.Rational(1, 2)
        * m2
        * (
            y**2
            + y**-2
            - 2
        )
        + ell
        * (
            sp.Rational(1, 4) * y**4
            + sp.Rational(1, 2) * y**-2
            - sp.Rational(3, 4)
        )
    )

    complete_relative_equation = (
        alpha
        * (
            y_ddot
            + (
                2 * phi_c_dot_over_phi_c
                + 3 * H
            )
            * y_dot
            + (
                phi_c_ddot_over_phi_c
                + 3 * H * phi_c_dot_over_phi_c
            )
            * y
        )
        + restoring_force
    )

    reduced_relative_equation = (
        alpha
        * (
            y_ddot
            + gamma * y_dot
        )
        + restoring_force
        - alpha * g_quartic * y
    )

    linear_restoring = sp.diff(
        restoring_force,
        y,
    ).subs(
        y,
        1,
    )

    return {
        "circular_manifold_N_derivative": sp.factor(
            circular_manifold_N_derivative
        ),
        "quartic_coefficient_N_identity": sp.factor(
            ell_N
            - expected_ell_N
        ),
        "log_circular_field_N_derivative_identity": sp.factor(
            u
            + 3
            * (m2 + ell)
            / denominator
        ),
        "log_circular_field_second_N_identity": sp.factor(
            u_N
            - expected_u_N
        ),
        "relative_damping_identity": sp.factor(
            gamma
            - expected_gamma
        ),
        "quartic_forcing_identity": sp.factor(
            g_quartic
            - expected_g_quartic
        ),
        "relative_equation_decomposition": sp.factor(
            complete_relative_equation
            - reduced_relative_equation
        ),
        "relative_potential_derivative": sp.factor(
            sp.diff(
                relative_potential,
                y,
            )
            - restoring_force
        ),
        "linear_restoring_coefficient": sp.factor(
            linear_restoring
            - (
                4 * m2
                + 6 * ell
            )
        ),
        "quadratic_limit_log_field": sp.simplify(
            sp.limit(
                u,
                lambda_phi,
                0,
            )
            + sp.Rational(3, 2)
        ),
        "quadratic_limit_damping": sp.simplify(
            sp.limit(
                gamma,
                lambda_phi,
                0,
            )
        ),
        "quadratic_limit_forcing": sp.simplify(
            sp.limit(
                g_quartic,
                lambda_phi,
                0,
            )
            - sp.Rational(3, 4)
            * (
                2 * H_dot
                + 3 * H**2
            )
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

BOLTZMANN_MEV_PER_K = 8.617333262e-11
T_CMB0_K = 2.7255
T_CMB0_MEV = T_CMB0_K * BOLTZMANN_MEV_PER_K
ELECTRON_MASS_MEV = 0.51099895069

STANDARD_N_EFF_TODAY = 3.044
STANDARD_BBN_N_NU = 3.0
STANDARD_NEUTRINO_DECOUPLING_MEV = 3.0


@dataclass(frozen=True)
class BBNThermodynamicReference:
    """Gamma/e+-/nu/CDM comparator on a photon-temperature surface."""

    T_gamma_MeV: float
    T_nu_MeV: float
    a: float
    N: float
    g_s_em: float
    rho_gamma_code: float
    rho_e_pm_code: float
    rho_nu_code: float
    rho_radiation_code: float
    rho_cdm_reference_code: float


def _electron_equilibrium_thermodynamics(
    T_gamma_MeV: float,
) -> tuple[float, float, float]:
    """Return rho_e/T^4, p_e/T^4, and e+- entropy degrees of freedom."""

    _require_finite("T_gamma_MeV", T_gamma_MeV)
    if T_gamma_MeV <= 0.0:
        raise ValueError("T_gamma_MeV must be positive")

    y = ELECTRON_MASS_MEV / T_gamma_MeV

    if y >= 50.0:
        return 0.0, 0.0, 0.0

    def fermi_factor(energy: float) -> float:
        weight = math.exp(-energy)
        return weight / (1.0 + weight)

    def rho_integrand(x: float) -> float:
        energy = math.sqrt(x * x + y * y)
        return x * x * energy * fermi_factor(energy)

    def pressure_integrand(x: float) -> float:
        energy = math.sqrt(x * x + y * y)
        return x**4 / energy * fermi_factor(energy)

    rho_integral = quad(
        rho_integrand,
        0.0,
        math.inf,
        epsabs=1.0e-12,
        epsrel=1.0e-11,
        limit=200,
    )[0]

    pressure_integral = quad(
        pressure_integrand,
        0.0,
        math.inf,
        epsabs=1.0e-12,
        epsrel=1.0e-11,
        limit=200,
    )[0]

    rho_over_T4 = 2.0 * rho_integral / math.pi**2
    pressure_over_T4 = (
        2.0 * pressure_integral / (3.0 * math.pi**2)
    )

    g_s_e_pm = (
        45.0
        * (rho_over_T4 + pressure_over_T4)
        / (2.0 * math.pi**2)
    )

    return rho_over_T4, pressure_over_T4, g_s_e_pm


def bbn_em_entropy_degrees(T_gamma_MeV: float) -> float:
    """Electromagnetic entropy g_*s for gamma plus e+-."""

    _, _, g_s_e_pm = _electron_equilibrium_thermodynamics(
        T_gamma_MeV
    )
    return 2.0 + g_s_e_pm


def bbn_scale_factor_from_temperature(
    T_gamma_MeV: float,
) -> float:
    """Map photon temperature to a via electromagnetic entropy conservation."""

    _require_finite("T_gamma_MeV", T_gamma_MeV)
    if T_gamma_MeV <= 0.0:
        raise ValueError("T_gamma_MeV must be positive")

    g_s_em = bbn_em_entropy_degrees(T_gamma_MeV)

    return (
        T_CMB0_MEV
        / T_gamma_MeV
        * (2.0 / g_s_em) ** (1.0 / 3.0)
    )


def bbn_efold_from_temperature(T_gamma_MeV: float) -> float:
    """Return solver N=ln(a) for a photon-temperature surface."""

    return math.log(
        bbn_scale_factor_from_temperature(T_gamma_MeV)
    )


def bbn_temperature_from_efold(N: float) -> float:
    """Invert the monotone BBN N <-> T_gamma entropy map."""

    _require_finite("N", N)

    if N >= 0.0:
        return T_CMB0_MEV * math.exp(-N)

    naive_temperature = T_CMB0_MEV * math.exp(-N)

    lower = (
        naive_temperature
        * (2.0 / 5.5) ** (1.0 / 3.0)
        * 0.98
    )
    upper = naive_temperature * 1.02

    def residual(temperature: float) -> float:
        return bbn_efold_from_temperature(temperature) - N

    lower_residual = residual(lower)
    upper_residual = residual(upper)

    if lower_residual < 0.0 or upper_residual > 0.0:
        raise RuntimeError(
            "failed to bracket the N-to-T_gamma inversion"
        )

    for _ in range(96):
        midpoint = 0.5 * (lower + upper)
        midpoint_residual = residual(midpoint)

        if midpoint_residual > 0.0:
            lower = midpoint
        else:
            upper = midpoint

    return 0.5 * (lower + upper)


def bbn_neutrino_temperature(
    T_gamma_MeV: float,
    *,
    decoupling_temperature_MeV: float = (
        STANDARD_NEUTRINO_DECOUPLING_MEV
    ),
) -> float:
    """Instantaneous-decoupling neutrino reference temperature."""

    _require_finite("T_gamma_MeV", T_gamma_MeV)
    _require_finite(
        "decoupling_temperature_MeV",
        decoupling_temperature_MeV,
    )

    if T_gamma_MeV <= 0.0:
        raise ValueError("T_gamma_MeV must be positive")

    if decoupling_temperature_MeV <= 0.0:
        raise ValueError(
            "decoupling_temperature_MeV must be positive"
        )

    if T_gamma_MeV >= decoupling_temperature_MeV:
        return T_gamma_MeV

    g_s_em = bbn_em_entropy_degrees(T_gamma_MeV)
    g_s_decoupling = bbn_em_entropy_degrees(
        decoupling_temperature_MeV
    )

    return (
        T_gamma_MeV
        * (g_s_em / g_s_decoupling) ** (1.0 / 3.0)
    )


def build_bbn_thermodynamic_reference(
    unit_map: "DFMCDMUnitMap",
    *,
    T_gamma_MeV: float = 1.0,
    N_nu: float = STANDARD_BBN_N_NU,
    N_eff_today: float = STANDARD_N_EFF_TODAY,
    decoupling_temperature_MeV: float = (
        STANDARD_NEUTRINO_DECOUPLING_MEV
    ),
) -> BBNThermodynamicReference:
    """Construct gamma/e+-/nu/CDM reference densities at BBN."""

    _require_finite("N_nu", N_nu)
    _require_finite("N_eff_today", N_eff_today)

    if N_nu < 0.0:
        raise ValueError("N_nu must be nonnegative")
    if N_eff_today < 0.0:
        raise ValueError("N_eff_today must be nonnegative")

    a = bbn_scale_factor_from_temperature(T_gamma_MeV)
    N = math.log(a)

    T_nu_MeV = bbn_neutrino_temperature(
        T_gamma_MeV,
        decoupling_temperature_MeV=(
            decoupling_temperature_MeV
        ),
    )

    (
        electron_rho_over_T4,
        _electron_pressure_over_T4,
        electron_g_s,
    ) = _electron_equilibrium_thermodynamics(
        T_gamma_MeV
    )

    present_radiation_to_photon_ratio = (
        1.0
        + (7.0 / 8.0)
        * N_eff_today
        * (4.0 / 11.0) ** (4.0 / 3.0)
    )

    rho_gamma0_code = (
        unit_map.rho_r0_code
        / present_radiation_to_photon_ratio
    )

    temperature_ratio = T_gamma_MeV / T_CMB0_MEV

    rho_gamma_code = (
        rho_gamma0_code * temperature_ratio**4
    )

    photon_rho_over_T4 = math.pi**2 / 15.0

    rho_e_pm_code = (
        rho_gamma_code
        * electron_rho_over_T4
        / photon_rho_over_T4
    )

    rho_nu_code = (
        rho_gamma_code
        * (7.0 / 8.0)
        * N_nu
        * (T_nu_MeV / T_gamma_MeV) ** 4
    )

    rho_radiation_code = (
        rho_gamma_code
        + rho_e_pm_code
        + rho_nu_code
    )

    rho_cdm_reference_code = (
        unit_map.rho_cdm0_code * a**-3
    )

    return BBNThermodynamicReference(
        T_gamma_MeV=T_gamma_MeV,
        T_nu_MeV=T_nu_MeV,
        a=a,
        N=N,
        g_s_em=2.0 + electron_g_s,
        rho_gamma_code=rho_gamma_code,
        rho_e_pm_code=rho_e_pm_code,
        rho_nu_code=rho_nu_code,
        rho_radiation_code=rho_radiation_code,
        rho_cdm_reference_code=rho_cdm_reference_code,
    )
def bbn_dfm_density_excess(
    *,
    reference: BBNThermodynamicReference,
    phi: float,
    v: float,
    parameters: ChargeReducedParameters,
) -> float:
    """Return rho_DFM - rho_CDM_ref without catastrophic cancellation."""

    _require_finite("phi", phi)
    _require_finite("v", v)

    if phi == 0.0:
        raise ValueError(
            "phi must remain nonzero in the charge-reduced system"
        )

    delta_rho_dfm_code = (
        0.5 * parameters.alpha * v**2
        + phase_energy_density(
            reference.N,
            phi,
            parameters,
        )
        + (
            parameters.rho_star
            - reference.rho_cdm_reference_code
        )
        + 0.5 * parameters.m_phi_squared * phi**2
        + 0.25 * parameters.lambda_phi * phi**4
    )

    _require_finite(
        "delta_rho_dfm_code",
        delta_rho_dfm_code,
    )

    return delta_rho_dfm_code


def bbn_dfm_effective_neutrino_number(
    *,
    reference: BBNThermodynamicReference,
    phi: float,
    v: float,
    parameters: ChargeReducedParameters,
    standard_bbn_n_nu: float = STANDARD_BBN_N_NU,
) -> float:
    """Convert DFM excess energy to the BBN effective neutrino number."""

    _require_finite(
        "standard_bbn_n_nu",
        standard_bbn_n_nu,
    )

    if standard_bbn_n_nu < 0.0:
        raise ValueError(
            "standard_bbn_n_nu must be nonnegative"
        )

    rho_one_neutrino_species_code = (
        reference.rho_gamma_code
        * (7.0 / 8.0)
        * (
            reference.T_nu_MeV
            / reference.T_gamma_MeV
        ) ** 4
    )

    if rho_one_neutrino_species_code <= 0.0:
        raise ValueError(
            "one-neutrino-species BBN energy density must be positive"
        )

    delta_rho_dfm_code = bbn_dfm_density_excess(
        reference=reference,
        phi=phi,
        v=v,
        parameters=parameters,
    )

    n_eff_dfm = (
        standard_bbn_n_nu
        + delta_rho_dfm_code
        / rho_one_neutrino_species_code
    )

    _require_finite(
        "n_eff_dfm",
        n_eff_dfm,
    )

    return n_eff_dfm


BBN_N_EFF_TARGET = 2.898
BBN_N_EFF_SIGMA = 0.141


@dataclass(frozen=True)
class BBNNeffLikelihood:
    """Gaussian BBN N_eff likelihood/admissibility diagnostic."""

    n_eff_dfm: float
    target: float
    sigma: float
    residual: float
    z_score: float
    chi_squared: float
    admissible_1sigma: bool


def evaluate_bbn_neff_likelihood(
    *,
    reference: BBNThermodynamicReference,
    phi: float,
    v: float,
    parameters: ChargeReducedParameters,
    target: float = BBN_N_EFF_TARGET,
    sigma: float = BBN_N_EFF_SIGMA,
) -> BBNNeffLikelihood:
    """Evaluate 2.898 +/- 0.141 without imposing an exact closure."""

    _require_finite("target", target)
    _require_finite("sigma", sigma)

    if sigma <= 0.0:
        raise ValueError("sigma must be positive")

    n_eff_dfm = bbn_dfm_effective_neutrino_number(
        reference=reference,
        phi=phi,
        v=v,
        parameters=parameters,
    )

    residual = n_eff_dfm - target
    z_score = residual / sigma
    chi_squared = z_score**2

    return BBNNeffLikelihood(
        n_eff_dfm=n_eff_dfm,
        target=target,
        sigma=sigma,
        residual=residual,
        z_score=z_score,
        chi_squared=chi_squared,
        admissible_1sigma=(abs(z_score) <= 1.0),
    )


SHOOTING_PARAMETER_NAMES = (
    "phi_initial",
    "v_initial",
    "rho_star",
    "m_phi_squared",
    "lambda_phi",
    "Q_theta",
)
SHOOTING_RESIDUAL_NAMES = ("F_rho", "F_w", "F_H")


def exact_dfm_cdm_shooting_degeneracy_certificate() -> dict[str, sp.Expr]:
    """Certify the exact Friedmann dependency of the shooting map.

    On the flat H0-normalized branch, the visible and dark-energy sectors
    are fixed while DFM replaces CDM.  The present Friedmann constraint
    therefore gives

        F_rho = 3 * F_H * (H_DFM + H_target).

    Linearizing on the positive expanding branch gives

        dF_H = dF_rho / (6 * H_DFM).

    Hence the F_H Jacobian row is dependent on the F_rho row.  The
    three-residual, six-parameter unaugmented shooting map has structural
    rank at most two and nullity at least four wherever H_DFM is positive.
    """

    H_dfm, H_target = sp.symbols(
        "H_dfm H_target",
        positive=True,
    )
    rho_dfm, rho_cdm = sp.symbols(
        "rho_dfm rho_cdm",
        real=True,
    )
    dH, dF_rho = sp.symbols(
        "dH dF_rho",
        real=True,
    )

    F_rho = rho_dfm - rho_cdm
    F_H = H_dfm - H_target
    friedmann_constraint = (
        H_dfm**2
        - (3 * H_target**2 - rho_cdm + rho_dfm) / 3
    )
    linearized_friedmann_constraint = (
        2 * H_dfm * dH - dF_rho / 3
    )
    dF_rho_on_shell = 6 * H_dfm * dH

    return {
        "present_constraint_factorization": sp.expand(
            F_rho
            - 3 * F_H * (H_dfm + H_target)
            + 3 * friedmann_constraint
        ),
        "linearized_constraint_factorization": sp.simplify(
            dH
            - dF_rho / (6 * H_dfm)
            - linearized_friedmann_constraint / (2 * H_dfm)
        ),
        "jacobian_row_dependency": sp.simplify(
            dH - dF_rho_on_shell / (6 * H_dfm)
        ),
    }


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


def dfm_particle_mass_eV(
    *,
    unit_map: DFMCDMUnitMap,
    alpha: float,
    m_phi_squared: float,
) -> float:
    """Convert the H0-normalized canonical DFM mass to physical eV."""

    _require_finite("alpha", alpha)
    _require_finite("m_phi_squared", m_phi_squared)

    if alpha <= 0.0:
        raise ValueError("alpha must be positive")
    if m_phi_squared < 0.0:
        raise ValueError("m_phi_squared must be nonnegative")

    # Canonical mass:
    #
    #     m_code^2 = m_phi_squared / alpha.
    #
    # The DFM-CDM unit map fixes H0_code = 1, so one code inverse-time
    # unit is H0_si.  In natural units E = hbar * omega.
    hbar_eV_s = 6.582119569e-16

    mass_eV = (
        hbar_eV_s
        * unit_map.H0_si
        * math.sqrt(m_phi_squared / alpha)
    )

    _require_finite("mass_eV", mass_eV)
    return mass_eV


LRS_PARTICLE_MASS_LOWER_EV = 2.4e-21


def minimum_m_phi_squared_from_particle_mass(
    *,
    unit_map: DFMCDMUnitMap,
    alpha: float,
    particle_mass_lower_eV: float = LRS_PARTICLE_MASS_LOWER_EV,
) -> float:
    """Invert the exact H0-normalized DFM mass map."""

    _require_finite("alpha", alpha)
    _require_finite(
        "particle_mass_lower_eV",
        particle_mass_lower_eV,
    )

    if alpha <= 0.0:
        raise ValueError("alpha must be positive")

    if particle_mass_lower_eV <= 0.0:
        raise ValueError(
            "particle_mass_lower_eV must be positive"
        )

    hbar_eV_s = 6.582119569e-16
    one_code_mass_eV = hbar_eV_s * unit_map.H0_si

    minimum_m_phi_squared = (
        alpha
        * (
            particle_mass_lower_eV
            / one_code_mass_eV
        ) ** 2
    )

    _require_finite(
        "minimum_m_phi_squared",
        minimum_m_phi_squared,
    )

    return minimum_m_phi_squared


LRS_SELF_INTERACTION_LOWER_EV_INV_CM3 = 9.5e-19
LRS_SELF_INTERACTION_UPPER_EV_INV_CM3 = 4.0e-17

HBAR_EV_S = 6.582119569e-16
HBAR_C_EV_CM = 1.973269804e-5
REDUCED_PLANCK_ENERGY_EV = 2.435323460e27


def dfm_lrs_self_interaction_strength_eV_inv_cm3(
    *,
    unit_map: DFMCDMUnitMap,
    m_phi_squared: float,
    lambda_phi: float,
) -> float:
    """Map H0-normalized DFM parameters to LRS g/(mc^2)^2.

    The DFM-CDM convention H0_code=1 and G_code=1/(8*pi)
    implies the physical density unit

        rho_unit = Mbar_Pl^2 H0^2.

    Hence

        lambda_rel
          = lambda_phi H0^2 / (alpha^2 Mbar_Pl^2),

        m^2
          = H0^2 m_phi_squared / alpha,

    so alpha cancels from

        g/m^2 = lambda_rel / (2 m^4).

    Conversion from natural eV^-4 units to eV^-1 cm^3
    contributes (hbar c)^3.
    """

    _require_finite("m_phi_squared", m_phi_squared)
    _require_finite("lambda_phi", lambda_phi)

    if m_phi_squared <= 0.0:
        raise ValueError(
            "m_phi_squared must be positive"
        )

    if lambda_phi < 0.0:
        raise ValueError(
            "lambda_phi must be nonnegative"
        )

    expected_G_code = 1.0 / (8.0 * math.pi)

    if not math.isclose(
        unit_map.G_code,
        expected_G_code,
        rel_tol=0.0,
        abs_tol=1.0e-15,
    ):
        raise ValueError(
            "DFM-LRS map requires G_code = 1/(8*pi)"
        )

    H0_eV = HBAR_EV_S * unit_map.H0_si

    strength = (
        lambda_phi
        * HBAR_C_EV_CM**3
        / (
            2.0
            * m_phi_squared**2
            * REDUCED_PLANCK_ENERGY_EV**2
            * H0_eV**2
        )
    )

    _require_finite(
        "lrs_self_interaction_strength",
        strength,
    )

    return strength


def dfm_lambda_phi_interval_from_lrs(
    *,
    unit_map: DFMCDMUnitMap,
    m_phi_squared: float,
    lower_eV_inv_cm3: float = (
        LRS_SELF_INTERACTION_LOWER_EV_INV_CM3
    ),
    upper_eV_inv_cm3: float = (
        LRS_SELF_INTERACTION_UPPER_EV_INV_CM3
    ),
) -> tuple[float, float]:
    """Return the DFM-code lambda_phi interval implied by LRS."""

    _require_finite("m_phi_squared", m_phi_squared)
    _require_finite(
        "lower_eV_inv_cm3",
        lower_eV_inv_cm3,
    )
    _require_finite(
        "upper_eV_inv_cm3",
        upper_eV_inv_cm3,
    )

    if m_phi_squared <= 0.0:
        raise ValueError(
            "m_phi_squared must be positive"
        )

    if lower_eV_inv_cm3 <= 0.0:
        raise ValueError(
            "lower_eV_inv_cm3 must be positive"
        )

    if upper_eV_inv_cm3 < lower_eV_inv_cm3:
        raise ValueError(
            "upper_eV_inv_cm3 must be >= lower_eV_inv_cm3"
        )

    H0_eV = HBAR_EV_S * unit_map.H0_si

    conversion = (
        2.0
        * m_phi_squared**2
        * REDUCED_PLANCK_ENERGY_EV**2
        * H0_eV**2
        / HBAR_C_EV_CM**3
    )

    lower = conversion * lower_eV_inv_cm3
    upper = conversion * upper_eV_inv_cm3

    _require_finite("lambda_phi_lower", lower)
    _require_finite("lambda_phi_upper", upper)

    return lower, upper


def dfm_scattering_length_cm(
    *,
    unit_map: DFMCDMUnitMap,
    alpha: float,
    m_phi_squared: float,
    lambda_phi: float,
) -> float:
    """Map a positive-lambda DFM point to the LRS s-wave scattering length.

    LRS convention:
        lambda_LRS = 4*pi*hbar^2*a_s/m

    Equivalently, with
        S = lambda_LRS/(m*c^2)^2,

        a_s = S*(m*c^2)^3 / [4*pi*(hbar*c)^2].

    Source:
    https://arxiv.org/pdf/1310.6061
    """

    mass_eV = dfm_particle_mass_eV(
        unit_map=unit_map,
        alpha=alpha,
        m_phi_squared=m_phi_squared,
    )

    strength = (
        dfm_lrs_self_interaction_strength_eV_inv_cm3(
            unit_map=unit_map,
            m_phi_squared=m_phi_squared,
            lambda_phi=lambda_phi,
        )
    )

    scattering_length_cm = (
        strength
        * mass_eV**3
        / (
            4.0
            * math.pi
            * HBAR_C_EV_CM**2
        )
    )

    _require_finite(
        "scattering_length_cm",
        scattering_length_cm,
    )

    if lambda_phi > 0.0 and scattering_length_cm <= 0.0:
        raise RuntimeError(
            "positive lambda_phi must map to positive scattering length"
        )

    return scattering_length_cm


def dfm_lambda_phi_from_scattering_length_cm(
    *,
    unit_map: DFMCDMUnitMap,
    alpha: float,
    m_phi_squared: float,
    scattering_length_cm: float,
) -> float:
    """Parameterize the surviving positive-lambda family by a_s > 0."""

    _require_finite(
        "scattering_length_cm",
        scattering_length_cm,
    )

    if scattering_length_cm <= 0.0:
        raise ValueError(
            "scattering_length_cm must be positive"
        )

    mass_eV = dfm_particle_mass_eV(
        unit_map=unit_map,
        alpha=alpha,
        m_phi_squared=m_phi_squared,
    )

    strength = (
        4.0
        * math.pi
        * HBAR_C_EV_CM**2
        * scattering_length_cm
        / mass_eV**3
    )

    lower, upper = dfm_lambda_phi_interval_from_lrs(
        unit_map=unit_map,
        m_phi_squared=m_phi_squared,
        lower_eV_inv_cm3=strength,
        upper_eV_inv_cm3=strength,
    )

    if not math.isclose(
        lower,
        upper,
        rel_tol=2.0e-15,
        abs_tol=0.0,
    ):
        raise RuntimeError(
            "single-strength lambda_phi inversion did not close"
        )

    if lower <= 0.0:
        raise RuntimeError(
            "positive scattering length must map to lambda_phi > 0"
        )

    return lower


def dfm_lrs_antlia_scattering_length_intersection(
    *,
    particle_mass_eV: float,
    minimum_halo_mass_solar: float = 1.66e9,
) -> dict[str, object]:
    """Compare the LRS and Antlia-B regions in (m, a_s).

    The Antlia-B paper reports:
      R_TF < 0.18 kpc at 68 percent,
      R_TF < 0.72 kpc at 95 percent,
      S < 5.2e-20 eV^-1 cm^3 at 68 percent,
      S < 8.3e-20 eV^-1 cm^3 at 95 percent,

    where S = g/(m*c^2)^2.

    Its Eq. (5) has S proportional to R_TF^2, so this function
    also derives the 95-percent strength from the published
    68-percent pair and the published 95-percent radius.

    No numerical replacement for the Eq. (12) condition ">> 1"
    is introduced.
    """

    _require_finite(
        "particle_mass_eV",
        particle_mass_eV,
    )
    _require_finite(
        "minimum_halo_mass_solar",
        minimum_halo_mass_solar,
    )

    if particle_mass_eV <= 0.0:
        raise ValueError(
            "particle_mass_eV must be positive"
        )

    if minimum_halo_mass_solar <= 0.0:
        raise ValueError(
            "minimum_halo_mass_solar must be positive"
        )

    antlia_r_tf_68_kpc = 0.18
    antlia_r_tf_95_kpc = 0.72

    antlia_strength_68 = 5.2e-20
    antlia_strength_95_printed = 8.3e-20

    antlia_strength_95_eq5 = (
        antlia_strength_68
        * (
            antlia_r_tf_95_kpc
            / antlia_r_tf_68_kpc
        ) ** 2
    )

    strength_to_scattering_length = (
        particle_mass_eV**3
        / (
            4.0
            * math.pi
            * HBAR_C_EV_CM**2
        )
    )

    lrs_a_s_lower_cm = (
        LRS_SELF_INTERACTION_LOWER_EV_INV_CM3
        * strength_to_scattering_length
    )

    lrs_a_s_upper_cm = (
        LRS_SELF_INTERACTION_UPPER_EV_INV_CM3
        * strength_to_scattering_length
    )

    antlia_a_s_95_printed_cm = (
        antlia_strength_95_printed
        * strength_to_scattering_length
    )

    antlia_a_s_95_eq5_cm = (
        antlia_strength_95_eq5
        * strength_to_scattering_length
    )

    overlap_with_printed_95 = (
        lrs_a_s_lower_cm
        <= min(
            lrs_a_s_upper_cm,
            antlia_a_s_95_printed_cm,
        )
    )

    overlap_with_eq5_95 = (
        lrs_a_s_lower_cm
        <= min(
            lrs_a_s_upper_cm,
            antlia_a_s_95_eq5_cm,
        )
    )

    tf_hierarchy_68 = antlia_eq12_tf_hierarchy_ratio(
        particle_mass_eV=particle_mass_eV,
        minimum_halo_mass_solar=minimum_halo_mass_solar,
        r_tf_kpc=antlia_r_tf_68_kpc,
    )

    tf_hierarchy_95 = antlia_eq12_tf_hierarchy_ratio(
        particle_mass_eV=particle_mass_eV,
        minimum_halo_mass_solar=minimum_halo_mass_solar,
        r_tf_kpc=antlia_r_tf_95_kpc,
    )

    return {
        "particle_mass_eV": particle_mass_eV,
        "lrs_a_s_lower_cm": lrs_a_s_lower_cm,
        "lrs_a_s_upper_cm": lrs_a_s_upper_cm,
        "antlia_a_s_95_printed_cm": (
            antlia_a_s_95_printed_cm
        ),
        "antlia_a_s_95_eq5_cm": (
            antlia_a_s_95_eq5_cm
        ),
        "antlia_strength_95_printed": (
            antlia_strength_95_printed
        ),
        "antlia_strength_95_eq5": (
            antlia_strength_95_eq5
        ),
        "antlia_95_internal_gap": (
            antlia_strength_95_eq5
            - antlia_strength_95_printed
        ),
        "antlia_95_printed_equals_eq5": (
            antlia_strength_95_printed
            == antlia_strength_95_eq5
        ),
        "overlap_with_printed_95": (
            overlap_with_printed_95
        ),
        "overlap_with_eq5_95": (
            overlap_with_eq5_95
        ),
        "tf_hierarchy_68": tf_hierarchy_68,
        "tf_hierarchy_95": tf_hierarchy_95,
    }


def normalized_circular_force_residual(
    *,
    N: float,
    phi: float,
    beta: float,
    m_phi_squared: float,
    lambda_phi: float,
    Q_theta: float,
) -> float:
    """Scale-free residual for the circular-force equation.

    The zero set is exactly

        m_phi_squared*phi
        + lambda_phi*phi^3
        - Q_theta^2*exp(-6N)/(beta*phi^3)
        = 0,

    but the returned residual is divided by the sum of the
    magnitudes of the three force terms.  This avoids treating
    floating-point cancellation between O(1e12) terms as an
    O(1e-4) physical failure.
    """

    for name, value in (
        ("N", N),
        ("phi", phi),
        ("beta", beta),
        ("m_phi_squared", m_phi_squared),
        ("lambda_phi", lambda_phi),
        ("Q_theta", Q_theta),
    ):
        _require_finite(name, value)

    if phi == 0.0:
        raise ValueError(
            "phi must be nonzero in the charge-reduced system"
        )

    if beta <= 0.0:
        raise ValueError("beta must be positive")

    mass_force = m_phi_squared * phi
    quartic_force = lambda_phi * phi**3
    charge_force = (
        Q_theta**2
        * math.exp(-6.0 * N)
        / (beta * phi**3)
    )

    numerator = (
        mass_force
        + quartic_force
        - charge_force
    )

    denominator = (
        abs(mass_force)
        + abs(quartic_force)
        + abs(charge_force)
    )

    if denominator == 0.0:
        raise ValueError(
            "circular-force normalization scale must be nonzero"
        )

    residual = numerator / denominator

    _require_finite(
        "normalized_circular_force_residual",
        residual,
    )

    return residual


def circular_phi_squared_positive_root(
    *,
    a: float,
    beta: float,
    m_phi_squared: float,
    lambda_phi: float,
    Q_theta: float,
) -> float:
    """Return the unique positive x = phi^2 on the circular-force manifold.

    Solves

        lambda_phi*x^3
        + m_phi_squared*x^2
        - Q_theta^2/(beta*a^6)
        = 0

    for x > 0.

    For beta > 0, m_phi_squared > 0, lambda_phi > 0,
    a > 0, and Q_theta != 0, the polynomial is strictly
    increasing for x > 0 and therefore has exactly one
    positive root.

    The numerical solve is performed on a dimensionless
    monotone residual.  The upper bracket is the smaller of
    the pure-mass and pure-quartic roots, so both normalized
    positive terms remain <= 1 throughout the bracket.
    """

    for name, value in (
        ("a", a),
        ("beta", beta),
        ("m_phi_squared", m_phi_squared),
        ("lambda_phi", lambda_phi),
        ("Q_theta", Q_theta),
    ):
        _require_finite(name, value)

    if a <= 0.0:
        raise ValueError("a must be positive")

    if beta <= 0.0:
        raise ValueError("beta must be positive")

    if m_phi_squared <= 0.0:
        raise ValueError(
            "m_phi_squared must be positive"
        )

    if lambda_phi <= 0.0:
        raise ValueError(
            "lambda_phi must be positive"
        )

    if Q_theta == 0.0:
        raise ValueError(
            "Q_theta must be nonzero for a positive circular root"
        )

    # Compute C = Q^2/(beta*a^6) through logarithms so the
    # physical mass-floor branch does not inherit unnecessary
    # overflow/underflow from direct powers.
    log_c = (
        2.0 * math.log(abs(Q_theta))
        - math.log(beta)
        - 6.0 * math.log(a)
    )

    log_x_mass = 0.5 * (
        log_c - math.log(m_phi_squared)
    )

    log_x_quartic = (
        log_c - math.log(lambda_phi)
    ) / 3.0

    log_x_hi = min(
        log_x_mass,
        log_x_quartic,
    )

    x_hi = math.exp(log_x_hi)

    if not math.isfinite(x_hi) or x_hi <= 0.0:
        raise RuntimeError(
            "positive circular-root bracket is not representable"
        )

    # Evaluate
    #
    #   m2*x^2/C + lambda*x^3/C - 1
    #
    # through ratios to the two one-term roots.  On
    # [0, x_hi], neither positive contribution exceeds 1.
    def scaled_residual(x: float) -> float:
        if x == 0.0:
            return -1.0

        mass_ratio = math.exp(
            2.0 * math.log(x)
            - 2.0 * log_x_mass
        )

        quartic_ratio = math.exp(
            3.0 * math.log(x)
            - 3.0 * log_x_quartic
        )

        return mass_ratio + quartic_ratio - 1.0

    f_hi = scaled_residual(x_hi)

    if f_hi < 0.0:
        raise RuntimeError(
            "failed to bracket the unique positive circular root"
        )

    lo = 0.0
    hi = x_hi

    # Monotone bisection to the floating-point adjacency limit.
    for _ in range(256):
        mid = 0.5 * (lo + hi)

        if mid == lo or mid == hi:
            break

        if scaled_residual(mid) < 0.0:
            lo = mid
        else:
            hi = mid

    root = 0.5 * (lo + hi)

    if root == lo:
        root = hi

    if not math.isfinite(root) or root <= 0.0:
        raise RuntimeError(
            "unique positive circular root is not representable"
        )

    residual = scaled_residual(root)

    if abs(residual) > 5.0e-14:
        # Either adjacent endpoint can be the closer floating-point
        # representation of the mathematical root.
        candidates = (lo, root, hi)
        root = min(
            (
                value
                for value in candidates
                if value > 0.0
            ),
            key=lambda value: abs(
                scaled_residual(value)
            ),
        )
        residual = scaled_residual(root)

    if abs(residual) > 5.0e-14:
        raise RuntimeError(
            "positive circular root failed normalized identity check"
        )

    return root


def circular_energy_density_pressure(
    *,
    a: float,
    beta: float,
    rho_star: float,
    m_phi_squared: float,
    lambda_phi: float,
    Q_theta: float,
) -> tuple[float, float]:
    """Leading algebraic circular-manifold density and pressure.

    For x = phi_c^2 satisfying

        lambda_phi*x^3
        + m_phi_squared*x^2
        = Q_theta^2/(beta*a^6),

    the circular-force identity gives

        rho_circ
          = rho_star
            + m_phi_squared*x
            + 3/4*lambda_phi*x^2,

        p_circ
          = -rho_star
            + 1/4*lambda_phi*x^2.

    Radial tracking kinetic energy is outside this algebraic layer.
    """

    _require_finite("rho_star", rho_star)

    x = circular_phi_squared_positive_root(
        a=a,
        beta=beta,
        m_phi_squared=m_phi_squared,
        lambda_phi=lambda_phi,
        Q_theta=Q_theta,
    )

    rho_circ = (
        rho_star
        + m_phi_squared * x
        + 0.75 * lambda_phi * x**2
    )

    p_circ = (
        -rho_star
        + 0.25 * lambda_phi * x**2
    )

    _require_finite("rho_circ", rho_circ)
    _require_finite("p_circ", p_circ)

    return rho_circ, p_circ


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


DFM_CDM_POSITIVE_LAMBDA_FAMILY_RESIDUAL_NAMES = (
    "F_rho",
    "F_w",
    "C_v_initial",
    "C_rho_star",
    "C_circular_force",
)


def dfm_cdm_positive_lambda_family_residual_vector(
    vector: np.ndarray,
    *,
    alpha: float,
    beta: float,
    unit_map: DFMCDMUnitMap,
    config: ChargeReducedSolverConfig,
    target_w_dfm0: float = 0.0,
) -> np.ndarray:
    """Return the five equations defining the positive-lambda family.

    This does not alter the existing six-row augmented residual.
    C_lambda_phi is omitted only from this family evaluator.
    """

    candidate = _validated_dfm_cdm_shooting_vector(
        np.asarray(vector, dtype=float)
    )

    if float(candidate[4]) <= 0.0:
        raise ValueError(
            "positive-lambda family requires lambda_phi > 0"
        )

    validate_solver_config(config)
    _require_finite("target_w_dfm0", target_w_dfm0)

    if not math.isclose(
        config.N_final,
        0.0,
        rel_tol=0.0,
        abs_tol=1.0e-15,
    ):
        raise ValueError(
            "DFM-CDM positive-lambda family requires N_final = 0"
        )

    (
        phi_initial,
        _v_initial,
        rho_star,
        m_phi_squared,
        lambda_phi,
        Q_theta,
    ) = (float(value) for value in candidate)

    rho_circ0, p_circ0 = circular_energy_density_pressure(
        a=1.0,
        beta=beta,
        rho_star=rho_star,
        m_phi_squared=m_phi_squared,
        lambda_phi=lambda_phi,
        Q_theta=Q_theta,
    )

    F_rho_circ = (
        rho_circ0
        - unit_map.rho_cdm0_code
    )

    F_w_circ = (
        p_circ0
        - target_w_dfm0 * rho_circ0
    )

    closures = dfm_cdm_minimal_circular_closure_residuals(
        candidate,
        beta=beta,
        N_initial=config.N_initial,
    ).as_array()

    circular_normalized = normalized_circular_force_residual(
        N=config.N_initial,
        phi=phi_initial,
        beta=beta,
        m_phi_squared=m_phi_squared,
        lambda_phi=lambda_phi,
        Q_theta=Q_theta,
    )

    return np.asarray(
        (
            F_rho_circ,
            F_w_circ,
            closures[0],
            closures[1],
            circular_normalized,
        ),
        dtype=float,
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
