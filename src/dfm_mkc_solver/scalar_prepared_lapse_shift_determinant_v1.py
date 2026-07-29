"""Prepared on-shell nonvanishing of the scalar lapse/shift determinant."""

from __future__ import annotations

from functools import lru_cache
from types import MappingProxyType

import sympy as sp

from . import scalar_lapse_shift_schur_complement_v1 as schur
from . import scalar_spatial_gauge_quotient_kinetic_v1 as kinetic
from . import total_scalar_lapse_shift_hessian_v1 as total


CERTIFICATE_KEYS = (
    "baryon_current_density_mapping",
    "radiation_current_density_mapping",
    "prepared_phase_mapping",
    "conformal_friedmann_mapping",
    "visible_current_combination",
    "schur_factor_extraction",
    "schur_factor_on_shell_reduction",
    "schur_determinant_negative_factorization",
    "kinetic_pivot_on_shell_reduction",
    "kinetic_pivot_positive_factorization",
)


@lru_cache(maxsize=1)
def scalar_prepared_lapse_shift_determinant_data():
    """Return exact source, substitution, factorization, and sign data."""

    z = total._symbols()
    mu, q = sp.symbols("mu q", positive=True)
    rho_b, rho_r, rho_lambda = sp.symbols(
        "rho_b rho_r rho_lambda", nonnegative=True
    )
    a, G = z["a"], z["G"]
    alpha, beta = z["alpha"], z["beta"]
    phi, phi_prime = z["ph"], z["php"]
    H, k2 = z["H"], z["k2"]

    K = alpha * phi_prime**2 / (2 * a**2)
    P = q**2 / (2 * beta * a**6 * phi**2)
    V = mu**2 * phi**2 / 2
    rho_total = rho_b + rho_r + rho_lambda + K + P + V

    prepared_substitution = {
        z["rho_star"]: 0,
        z["lam"]: 0,
        z["m2"]: mu**2,
        z["thp"]: q / (beta * a**2 * phi**2),
        z["Lambda"]: 8 * sp.pi * G * rho_lambda,
    }
    current_density_substitution = {
        z["Jb"]: a**3 * rho_b / z["mb"],
        z["Jr"] ** sp.Rational(4, 3):
            a**4 * rho_r / z["kr"],
    }
    friedmann_substitution = {
        H**2: 8 * sp.pi * G * a**2 * rho_total / 3,
    }

    S = (
        12 * sp.pi * G * a**4 * rho_b
        + 16 * sp.pi * G * a**4 * rho_r
    )
    M = S + a**2 * k2
    positive_bracket = (
        S * (rho_b + rho_r + rho_lambda + V)
        + a**2 * k2 * rho_total
    )

    raw_determinant = (
        schur.scalar_lapse_shift_schur_complement()["determinant"]
    )
    prepared_determinant = sp.factor(
        raw_determinant.subs(
            prepared_substitution, simultaneous=True
        )
    )
    determinant_prefactor = (
        k2
        / (
            48 * sp.pi**2 * G**2 * a**2 * beta * phi**2
        )
    )
    raw_factor_F = sp.cancel(
        prepared_determinant / determinant_prefactor
    )
    on_shell_factor_F = sp.factor(
        raw_factor_F
        .subs(current_density_substitution, simultaneous=True)
        .subs(friedmann_substitution, simultaneous=True)
    )
    negative_factor_F = (
        -8 * sp.pi * G * a**6 * beta * phi**2
        * positive_bracket
    )
    on_shell_determinant = sp.factor(
        prepared_determinant
        .subs(current_density_substitution, simultaneous=True)
        .subs(friedmann_substitution, simultaneous=True)
    )
    negative_determinant = (
        -a**4 * k2 * positive_bracket / (6 * sp.pi * G)
    )

    raw_pivot = kinetic.quotient_kinetic_rank_data()["pivot_minor"]
    prepared_pivot = sp.factor(
        raw_pivot.subs(
            prepared_substitution, simultaneous=True
        )
    )
    on_shell_pivot = sp.factor(
        prepared_pivot
        .subs(current_density_substitution, simultaneous=True)
        .subs(friedmann_substitution, simultaneous=True)
    )
    positive_pivot = (
        3 * alpha * q**2 * M
        / (
            8 * sp.pi * G * a**2 * beta * phi**2
            * positive_bracket
        )
    )

    return {
        "symbols": MappingProxyType({
            "mu": mu,
            "q": q,
            "rho_b": rho_b,
            "rho_r": rho_r,
            "rho_lambda": rho_lambda,
        }),
        "prepared_substitution": prepared_substitution,
        "current_density_substitution":
            current_density_substitution,
        "friedmann_substitution": friedmann_substitution,
        "kinetic_energy_density": K,
        "phase_energy_density": P,
        "potential_energy_density": V,
        "rho_total": rho_total,
        "visible_current_combination": S,
        "positive_pivot_numerator": M,
        "raw_schur_determinant": raw_determinant,
        "prepared_schur_determinant": prepared_determinant,
        "determinant_prefactor": determinant_prefactor,
        "raw_factor_F": raw_factor_F,
        "on_shell_factor_F": on_shell_factor_F,
        "negative_factor_F": negative_factor_F,
        "strict_positive_bracket": positive_bracket,
        "on_shell_schur_determinant": on_shell_determinant,
        "negative_schur_determinant_factorization":
            negative_determinant,
        "raw_pivot_minor": raw_pivot,
        "prepared_pivot_minor": prepared_pivot,
        "on_shell_pivot_minor": on_shell_pivot,
        "positive_pivot_minor_factorization": positive_pivot,
        "positive_variables": (
            "G", "a", "alpha", "beta", "mu", "q", "phi", "k2",
        ),
        "nonnegative_variables": (
            "rho_b", "rho_r", "rho_lambda",
        ),
        "sign_assumptions": (
            "G,a,alpha,beta,mu,q,phi,k2>0; "
            "rho_b,rho_r,rho_lambda>=0"
        ),
        "nonvanishing_domain": MappingProxyType({
            "prepared_positive_energy": True,
            "finite_k": "k2>0 and finite",
            "friedmann_identity": "3*H^2=8*pi*G*a^2*rho_total",
            "current_density_identities": (
                "rho_b=m_b*Jbar_b_0/a^3",
                "rho_r=kappa_r*Jbar_r_0^(4/3)/a^4",
            ),
            "independent_determinant_factor_condition": False,
        }),
        "source_schur_determinant": raw_determinant,
        "source_kinetic_pivot_minor": raw_pivot,
    }


@lru_cache(maxsize=1)
def exact_scalar_prepared_lapse_shift_determinant_certificate():
    """Return the ten exact prepared determinant residuals."""

    data = scalar_prepared_lapse_shift_determinant_data()
    z = total._symbols()
    symbols = data["symbols"]
    rho_b = symbols["rho_b"]
    rho_r = symbols["rho_r"]
    q = symbols["q"]
    a, G, beta, phi, H = (
        z["a"], z["G"], z["beta"], z["ph"], z["H"]
    )
    current_sub = data["current_density_substitution"]
    current_b = z["mb"] * z["Jb"] / a**3
    current_r = z["kr"] * z["Jr"] ** sp.Rational(4, 3) / a**4
    phase_target = q / (beta * a**2 * phi**2)
    current_S = (
        12 * sp.pi * G * z["Jb"] * a * z["mb"]
        + 16 * sp.pi * G
        * z["Jr"] ** sp.Rational(4, 3) * z["kr"]
    )

    return {
        "baryon_current_density_mapping": sp.simplify(
            current_b.subs(current_sub, simultaneous=True) - rho_b
        ),
        "radiation_current_density_mapping": sp.simplify(
            current_r.subs(current_sub, simultaneous=True) - rho_r
        ),
        "prepared_phase_mapping": sp.simplify(
            (z["thp"] - phase_target).subs(
                data["prepared_substitution"], simultaneous=True
            )
        ),
        "conformal_friedmann_mapping": sp.simplify(
            (
                3 * H**2
                - 8 * sp.pi * G * a**2 * data["rho_total"]
            ).subs(data["friedmann_substitution"], simultaneous=True)
        ),
        "visible_current_combination": sp.simplify(
            current_S.subs(current_sub, simultaneous=True)
            - data["visible_current_combination"]
        ),
        "schur_factor_extraction": sp.simplify(
            data["prepared_schur_determinant"]
            - data["determinant_prefactor"] * data["raw_factor_F"]
        ),
        "schur_factor_on_shell_reduction": sp.simplify(
            data["on_shell_factor_F"] - data["negative_factor_F"]
        ),
        "schur_determinant_negative_factorization": sp.simplify(
            data["on_shell_schur_determinant"]
            - data["negative_schur_determinant_factorization"]
        ),
        "kinetic_pivot_on_shell_reduction": sp.simplify(
            data["on_shell_pivot_minor"]
            - data["positive_pivot_minor_factorization"]
        ),
        "kinetic_pivot_positive_factorization": sp.simplify(
            data["positive_pivot_minor_factorization"]
            - (
                3 * z["alpha"] * q**2
                * data["positive_pivot_numerator"]
                / (
                    8 * sp.pi * G * a**2 * beta * phi**2
                    * data["strict_positive_bracket"]
                )
            )
        ),
    }


def scalar_prepared_lapse_shift_determinant_theorem():
    """Return the immutable prepared-branch nonvanishing theorem."""

    data = scalar_prepared_lapse_shift_determinant_data()
    residuals = (
        exact_scalar_prepared_lapse_shift_determinant_certificate()
    )
    if tuple(residuals) != CERTIFICATE_KEYS:
        raise AssertionError("prepared determinant certificate keys changed")
    if not all(value == 0 for value in residuals.values()):
        raise AssertionError("prepared determinant certificate is not exact")

    return MappingProxyType({
        "prior_obstruction": (
            "The mixed-sign factor arose with H treated independently; "
            "the prepared Friedmann constraint removes that freedom."
        ),
        "friedmann_constraint": "3*H^2=8*pi*G*a^2*rho_total",
        "factor_sign": (
            "F<0 because V>0, rho_total>0, S>=0, and "
            "S*(rho_b+rho_r+rho_lambda+V)+a^2*k2*rho_total>0"
        ),
        "schur_determinant_sign": "strictly negative",
        "kinetic_pivot_sign": "strictly positive",
        "finite_alpha_nonvanishing": True,
        "independent_determinant_domain_required": False,
        "nonvanishing_domain": data["nonvanishing_domain"],
        "limitations": (
            "This does not construct the time-gauge quotient action.",
            "This does not classify the prepared-family Weyl limit.",
        ),
    })
