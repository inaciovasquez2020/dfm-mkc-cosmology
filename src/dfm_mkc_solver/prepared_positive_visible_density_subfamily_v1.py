"""Positive-visible-density restriction of the prepared alpha family."""

from __future__ import annotations

from functools import lru_cache
from types import MappingProxyType

import sympy as sp

from . import prepared_alpha_family_existence_v1 as prepared
from . import scalar_prepared_lapse_shift_determinant_v1 as determinant
from . import total_scalar_lapse_shift_hessian_v1 as total


CERTIFICATE_KEYS = (
    "baryon_scale_factor_solution",
    "radiation_scale_factor_solution",
    "baryon_conservation_equation",
    "radiation_conservation_equation",
    "baryon_initial_value",
    "radiation_initial_value",
    "baryon_current_reconstruction",
    "radiation_current_reconstruction",
    "baryon_density_reconstruction",
    "radiation_density_reconstruction",
)


@lru_cache(maxsize=1)
def prepared_positive_visible_density_subfamily_data():
    """Return exact scaling, current reconstruction, and domain data."""

    N = sp.symbols("N", real=True)
    a = sp.symbols("a", positive=True)
    rho_b0, rho_r0 = sp.symbols(
        "rho_b0 rho_r0", positive=True
    )
    m_b, kappa_r = sp.symbols(
        "m_b kappa_r", positive=True
    )

    rho_b_N = rho_b0 * sp.exp(-3 * N)
    rho_r_N = rho_r0 * sp.exp(-4 * N)
    rho_b_a = rho_b0 / a**3
    rho_r_a = rho_r0 / a**4
    Jbar_b_0 = rho_b0 / m_b
    Jbar_r_0 = (rho_r0 / kappa_r) ** sp.Rational(3, 4)

    a_i = sp.Rational(100, 333)
    z_max = sp.Rational(233, 100)

    return {
        "N": N,
        "a": a,
        "rho_b0": rho_b0,
        "rho_r0": rho_r0,
        "m_b": m_b,
        "kappa_r": kappa_r,
        "rho_b_N": rho_b_N,
        "rho_r_N": rho_r_N,
        "rho_b_a": rho_b_a,
        "rho_r_a": rho_r_a,
        "Jbar_b_0": Jbar_b_0,
        "Jbar_r_0": Jbar_r_0,
        "z_max": z_max,
        "a_i": a_i,
        "repository_a_i": prepared.A_INITIAL,
        "positive_variables": (
            "rho_b0",
            "rho_r0",
            "a",
            "m_b",
            "kappa_r",
        ),
        "strict_claims": MappingProxyType({
            "rho_b0_positive": True,
            "rho_r0_positive": True,
            "scale_factor_positive": True,
            "rho_b_positive": True,
            "rho_r_positive": True,
            "Jbar_b_0_positive": True,
            "Jbar_r_0_positive": True,
            "complete_prepared_interval_covered": True,
        }),
        "prepared_interval": sp.And(
            sp.Le(a_i, a, evaluate=False),
            sp.Le(a, 1, evaluate=False),
            evaluate=False,
        ),
        "determinant_density_mappings":
            determinant
            .scalar_prepared_lapse_shift_determinant_data()[
                "current_density_substitution"
            ],
    }


@lru_cache(maxsize=1)
def exact_prepared_positive_visible_density_subfamily_certificate():
    """Return ten exact identities for the positive-density subfamily."""

    data = prepared_positive_visible_density_subfamily_data()
    N, a = data["N"], data["a"]
    rho_b0, rho_r0 = data["rho_b0"], data["rho_r0"]
    m_b, kappa_r = data["m_b"], data["kappa_r"]
    rho_b_N, rho_r_N = data["rho_b_N"], data["rho_r_N"]
    rho_b_a, rho_r_a = data["rho_b_a"], data["rho_r_a"]
    Jb, Jr = data["Jbar_b_0"], data["Jbar_r_0"]

    return {
        "baryon_scale_factor_solution": sp.simplify(
            rho_b_N.subs(N, sp.log(a)) - rho_b_a
        ),
        "radiation_scale_factor_solution": sp.simplify(
            rho_r_N.subs(N, sp.log(a)) - rho_r_a
        ),
        "baryon_conservation_equation": sp.simplify(
            sp.diff(rho_b_N, N) + 3 * rho_b_N
        ),
        "radiation_conservation_equation": sp.simplify(
            sp.diff(rho_r_N, N) + 4 * rho_r_N
        ),
        "baryon_initial_value": sp.simplify(
            rho_b_N.subs(N, 0) - rho_b0
        ),
        "radiation_initial_value": sp.simplify(
            rho_r_N.subs(N, 0) - rho_r0
        ),
        "baryon_current_reconstruction": sp.simplify(
            m_b * Jb - rho_b0
        ),
        "radiation_current_reconstruction": sp.simplify(
            kappa_r * Jr ** sp.Rational(4, 3) - rho_r0
        ),
        "baryon_density_reconstruction": sp.simplify(
            m_b * Jb / a**3 - rho_b_a
        ),
        "radiation_density_reconstruction": sp.simplify(
            kappa_r * Jr ** sp.Rational(4, 3) / a**4
            - rho_r_a
        ),
    }


def prepared_positive_visible_density_subfamily_theorem():
    """Return the immutable positive-visible prepared-subfamily theorem."""

    data = prepared_positive_visible_density_subfamily_data()
    residuals = (
        exact_prepared_positive_visible_density_subfamily_certificate()
    )
    if tuple(residuals) != CERTIFICATE_KEYS:
        raise AssertionError("positive-density certificate keys changed")
    if not all(value == 0 for value in residuals.values()):
        raise AssertionError("positive-density certificate is not exact")

    return MappingProxyType({
        "relation_to_generic_family": (
            "Subfamily of the generic prepared-alpha family obtained by "
            "restricting rho_b0>0 and rho_r0>0."
        ),
        "subfamily_assumptions": (
            "rho_b0>0",
            "rho_r0>0",
        ),
        "scaling": (
            "rho_b=rho_b0/a^3",
            "rho_r=rho_r0/a^4",
        ),
        "current_reconstruction": (
            "Jbar_b_0=rho_b0/m_b",
            "Jbar_r_0=(rho_r0/kappa_r)^(3/4)",
        ),
        "strict_claims": data["strict_claims"],
        "prepared_interval": (
            "0<=z<=2.33; 100/333<=a<=1"
        ),
        "independent_determinant_nonvanishing_assumed": False,
        "limitations": (
            "The generic prepared theorem still permits zero visible "
            "densities.",
            "This theorem applies only when rho_b0>0 and rho_r0>0.",
            "Zero-species boundary models require separate visible-sector "
            "charts.",
            "No separate zero-species chart is constructed here.",
        ),
    })
