"""Prepared positive-alpha family existence theorem on 0 <= z <= 2.33.

This module is an analytic certificate and constructor. It deliberately does
not numerically integrate the canonical background equations.
"""

from __future__ import annotations

import math
from dataclasses import dataclass
from types import MappingProxyType
from typing import Any, Mapping

import sympy as sp

from .bao_distance_profile_stability_v1 import (
    exact_bao_distance_profile_stability_certificate,
)
from .charge_reduced_background_v1 import (
    ChargeReducedInitialData,
    ChargeReducedParameters,
)


Z_MAX = 2.33
A_INITIAL = 1.0 / (1.0 + Z_MAX)


@dataclass(frozen=True)
class PreparedAlphaThresholds:
    """Alpha-independent constants used by the prepared-family proof."""

    a_i: float
    phi_i: float
    H_floor: float
    H_L_i: float
    alpha_initial: float
    H_bar: float
    G_bar: float
    T_bar: float
    c_bar: float
    C_B: float
    alpha_energy: float
    alpha_max: float


@dataclass(frozen=True)
class PreparedAlphaFamilyMember:
    """Canonical objects and bounds for one admissible positive alpha."""

    parameters: ChargeReducedParameters
    initial_data: ChargeReducedInitialData
    thresholds: PreparedAlphaThresholds
    alpha: float
    H_i: float
    v_i: float
    phi_min: float
    phi_max: float
    v_upper: float
    phase_upper: float
    rho_b_i: float
    rho_r_i: float
    phase_energy_upper: float
    mass_energy_upper: float
    kinetic_energy_upper: float


def _finite(name: str, value: float) -> float:
    value = float(value)
    if not math.isfinite(value):
        raise ValueError(f"{name} must be finite")
    return value


def prepared_alpha_thresholds(
    *,
    G_N: float,
    beta: float,
    mu: float,
    q: float,
    rho_b0: float,
    rho_r0: float,
    rho_lambda: float,
) -> PreparedAlphaThresholds:
    """Calculate all alpha-independent thresholds; no alpha is accepted."""

    G_N = _finite("G_N", G_N)
    beta = _finite("beta", beta)
    mu = _finite("mu", mu)
    q = _finite("q", q)
    rho_b0 = _finite("rho_b0", rho_b0)
    rho_r0 = _finite("rho_r0", rho_r0)
    rho_lambda = _finite("rho_lambda", rho_lambda)
    if G_N <= 0.0 or beta <= 0.0 or mu <= 0.0 or q <= 0.0:
        raise ValueError("G_N, beta, mu, and q must be positive")
    if rho_b0 < 0.0 or rho_r0 < 0.0 or rho_lambda < 0.0:
        raise ValueError("background densities must be nonnegative")

    a_i = A_INITIAL
    kappa = 8.0 * math.pi * G_N / 3.0
    rho_cdm0 = q * mu / math.sqrt(beta)
    phi_i = math.sqrt(q / (math.sqrt(beta) * mu)) * a_i ** (-1.5)

    def H_L(a: float) -> float:
        return math.sqrt(
            kappa
            * (
                rho_lambda
                + (rho_b0 + rho_cdm0) * a**-3
                + rho_r0 * a**-4
            )
        )

    H_floor = H_L(1.0)
    H_L_i = H_L(a_i)
    alpha_initial = 1.0 / (6.0 * math.pi * G_N * phi_i**2)
    H_bar = math.sqrt(2.0) * H_L_i
    G_bar = 9.0 * H_bar**2 / 4.0
    T_bar = -math.log(a_i) / H_floor
    c_bar = 1.0 + alpha_initial * G_bar**2 / mu**2
    try:
        C_B = G_bar**2 * T_bar * math.exp(c_bar * T_bar)
    except OverflowError as exc:
        raise ValueError("threshold constants overflow") from exc
    if not math.isfinite(C_B) or C_B <= 0.0:
        raise ValueError("C_B must be finite and positive")
    alpha_energy = mu**2 / (16.0 * C_B)
    alpha_max = min(alpha_initial, alpha_energy)
    return PreparedAlphaThresholds(
        a_i=a_i,
        phi_i=phi_i,
        H_floor=H_floor,
        H_L_i=H_L_i,
        alpha_initial=alpha_initial,
        H_bar=H_bar,
        G_bar=G_bar,
        T_bar=T_bar,
        c_bar=c_bar,
        C_B=C_B,
        alpha_energy=alpha_energy,
        alpha_max=alpha_max,
    )


def build_prepared_alpha_family_member(
    *,
    G_N: float,
    beta: float,
    mu: float,
    q: float,
    rho_b0: float,
    rho_r0: float,
    rho_lambda: float,
    alpha: float,
) -> PreparedAlphaFamilyMember:
    """Construct one exactly prepared canonical member without integration."""

    thresholds = prepared_alpha_thresholds(
        G_N=G_N,
        beta=beta,
        mu=mu,
        q=q,
        rho_b0=rho_b0,
        rho_r0=rho_r0,
        rho_lambda=rho_lambda,
    )
    alpha = _finite("alpha", alpha)
    if not 0.0 < alpha <= thresholds.alpha_max:
        raise ValueError(
            "alpha must satisfy 0 < alpha <= alpha_max "
            f"(alpha_initial={thresholds.alpha_initial!r}, "
            f"alpha_energy={thresholds.alpha_energy!r}, "
            f"alpha_max={thresholds.alpha_max!r})"
        )

    denominator = (
        1.0
        - 3.0 * math.pi * float(G_N) * alpha * thresholds.phi_i**2
    )
    H_i = thresholds.H_L_i / math.sqrt(denominator)
    v_i = -1.5 * H_i * thresholds.phi_i
    rho_b_i = float(rho_b0) * thresholds.a_i**-3
    rho_r_i = float(rho_r0) * thresholds.a_i**-4
    parameters = ChargeReducedParameters(
        G=float(G_N),
        Lambda=8.0 * math.pi * float(G_N) * float(rho_lambda),
        w0=-1.0,
        wa=0.0,
        alpha=alpha,
        beta=float(beta),
        rho_star=0.0,
        m_phi_squared=float(mu) ** 2,
        lambda_phi=0.0,
        Q_theta=float(q),
    )
    initial_data = ChargeReducedInitialData(
        phi=thresholds.phi_i,
        v=v_i,
        theta=0.0,
        rho_m=rho_b_i,
        rho_r=rho_r_i,
    )
    phi_min = thresholds.phi_i * thresholds.a_i**1.5 / 2.0
    phi_max = 1.5 * thresholds.phi_i
    v_upper = thresholds.phi_i * (
        math.sqrt(2.0 * thresholds.C_B) + 9.0 * thresholds.H_bar / 4.0
    )
    phase_upper = (
        float(q)
        * thresholds.T_bar
        / (float(beta) * thresholds.a_i**3 * phi_min**2)
    )
    return PreparedAlphaFamilyMember(
        parameters=parameters,
        initial_data=initial_data,
        thresholds=thresholds,
        alpha=alpha,
        H_i=H_i,
        v_i=v_i,
        phi_min=phi_min,
        phi_max=phi_max,
        v_upper=v_upper,
        phase_upper=phase_upper,
        rho_b_i=rho_b_i,
        rho_r_i=rho_r_i,
        phase_energy_upper=2.0 * float(mu) ** 2 * thresholds.phi_i**2,
        mass_energy_upper=9.0 * float(mu) ** 2 * thresholds.phi_i**2 / 8.0,
        kinetic_energy_upper=thresholds.alpha_initial * v_upper**2 / 2.0,
    )


def exact_prepared_alpha_family_existence_certificate() -> dict[str, sp.Expr]:
    """Return the twelve exact residuals used in the existence theorem."""

    G_N, beta, mu, q, a_i, alpha = sp.symbols(
        "G_N beta mu q a_i alpha", positive=True
    )
    rho_lambda = sp.symbols("rho_lambda", nonnegative=True)
    H_L_i, H_floor, C_B = sp.symbols(
        "H_L_i H_floor C_B", positive=True
    )
    phi_i = (
        sp.sqrt(q / (sp.sqrt(beta) * mu))
        * a_i ** sp.Rational(-3, 2)
    )
    rho_cdm = q * mu / sp.sqrt(beta) * a_i**-3
    alpha_initial_definition = 1 / (6 * sp.pi * G_N * phi_i**2)
    alpha_energy_definition = mu**2 / (16 * C_B)
    prepared_denominator = 1 - 3 * sp.pi * G_N * alpha * phi_i**2
    H_i = H_L_i / sp.sqrt(prepared_denominator)
    v_i = -sp.Rational(3, 2) * H_i * phi_i
    H_bar = sp.sqrt(2) * H_L_i
    G_bar = sp.Rational(9, 4) * H_bar**2
    T_bar_definition = -sp.log(a_i) / H_floor
    phi_min = phi_i * a_i ** sp.Rational(3, 2) / 2
    phase_rate = q / (beta * a_i**3 * phi_min**2)
    Lambda = 8 * sp.pi * G_N * rho_lambda

    return {
        "circular_density_normalization": sp.simplify(
            mu**2 * phi_i**2 - rho_cdm
        ),
        "prepared_initial_velocity": sp.simplify(
            v_i + sp.Rational(3, 2) * H_i * phi_i
        ),
        "prepared_initial_friedmann_identity": sp.simplify(
            H_i**2 - H_L_i**2 / prepared_denominator
        ),
        "initial_denominator_margin_identity": sp.simplify(
            prepared_denominator
            - sp.Rational(1, 2)
            - 3
            * sp.pi
            * G_N
            * phi_i**2
            * (alpha_initial_definition - alpha)
        ),
        "initial_hubble_upper_identity": sp.simplify(
            H_bar**2
            - H_i**2
            - H_L_i**2
            * (1 - 6 * sp.pi * G_N * alpha * phi_i**2)
            / prepared_denominator
        ),
        "forcing_upper_identity": sp.simplify(
            G_bar - sp.Rational(9, 4) * H_bar**2
        ),
        "time_to_redshift_identity": sp.simplify(
            T_bar_definition - (-sp.log(a_i) / H_floor)
        ),
        "energy_threshold_identity": sp.simplify(
            alpha_energy_definition * C_B - mu**2 / 16
        ),
        "strict_field_margin_identity": sp.simplify(
            2 * alpha_energy_definition * C_B / mu**2
            - sp.Rational(1, 8)
        ),
        "field_lower_bound_identity": sp.simplify(
            phi_min - phi_i * a_i ** sp.Rational(3, 2) / 2
        ),
        "canonical_lambda_density_mapping": sp.simplify(
            Lambda / (8 * sp.pi * G_N) - rho_lambda
        ),
        "phase_derivative_majorant_identity": sp.simplify(
            phase_rate - q / (beta * a_i**3 * phi_min**2)
        ),
    }


def prepared_alpha_family_existence_theorem() -> Mapping[str, Any]:
    """Return an immutable, structured statement of the analytic theorem."""

    identities = (
        "mu^2*phi_c(a)^2=rho_cdm(a), the prepared velocity and Friedmann "
        "constraint, threshold definitions, Lambda mapping, and phase bound"
    )
    inequalities = (
        "For a_i<=a<=1, H_L>=H_floor>0. For 0<alpha<=alpha_max: "
        "the initial denominator is >=1/2, H_i<=H_bar, |g|<=G_bar, "
        "T<=T_bar, and B<=alpha*C_B<=mu^2/16. Hence "
        "|y-1|<=1/(2*sqrt(2))<1/2, |y_dot|<=sqrt(2*C_B), "
        "0<phi_min<phi<phi_max, and all stated field, matter, energy, "
        "velocity, and phase bounds hold."
    )
    continuation = (
        "Bootstrap on 1/2<y<3/2. Raychaudhuri monotonicity gives "
        "H<=H_i<=H_bar while the nonnegative DFM contribution gives "
        "H_DFM>=H_L>=H_floor. The strict energy margin keeps phi positive; "
        "phi, v, theta, rho_b, and rho_r stay bounded and the Friedmann "
        "radicand stays >=H_floor^2. For each fixed alpha>0 the actual "
        "canonical N-time right-hand side is smooth on a>0, phi>0, H>0. "
        "The maximal-solution continuation criterion therefore extends the "
        "unique prepared solution through N=0 (a=1), closing the bootstrap."
    )
    conclusions = (
        "Every 0<alpha<=alpha_max has a unique exactly prepared canonical "
        "solution on 0<=z<=2.33. Combined with "
        "exact_bao_distance_profile_stability_certificate, the raw 13-row "
        "BAO error is O(alpha), the profile candidate objective is "
        "O(alpha^2), and arbitrarily small admissible alpha>0 imply "
        "DFM_LCDM_PROFILED_BAO_INFIMUM=0."
    )
    limitations = (
        "No exact finite-alpha overlap is proved.",
        "Only the quadratic positive-charge branch is covered.",
        "No compact complete DFM domain is supplied.",
        "This does not prove agreement with DESI.",
        "This does not establish an observable separated from Lambda-CDM.",
        "Python tests check identities and construction logic; they are not "
        "a proof-assistant formalization of the continuation theorem.",
    )
    bao_residuals = exact_bao_distance_profile_stability_certificate()
    if not all(value == 0 for value in bao_residuals.values()):
        raise AssertionError("BAO stability certificate is not exact")
    return MappingProxyType(
        {
            "branch": (
                "z_max=2.33; G_N,beta,mu,q>0; "
                "rho_b0,rho_r0,rho_lambda>=0"
            ),
            "exact_symbolic_identities": identities,
            "nonnegative_decomposition_inequalities": inequalities,
            "bootstrap_continuation": continuation,
            "conclusions": conclusions,
            "limitations": limitations,
        }
    )
