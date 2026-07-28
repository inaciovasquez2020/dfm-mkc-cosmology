"""Exact spatial scalar-gauge quotient of the A/B Schur-reduced action."""

from __future__ import annotations

from dataclasses import dataclass
from functools import lru_cache

import sympy as sp

from . import scalar_lapse_shift_schur_complement_v1 as schur
from . import total_scalar_lapse_shift_hessian_v1 as total


SPATIAL_GAUGE_FIELD = "E"

QUOTIENT_FIELDS = tuple(
    field
    for field in schur.REDUCED_FIELDS
    if field != SPATIAL_GAUGE_FIELD
)

CURRENT_FIELDS = (
    "delta_J_b_0",
    "delta_J_b_L",
    "delta_J_r_0",
    "delta_J_r_L",
)


@dataclass(frozen=True)
class ScalarSpatialGaugeQuotientCertificate:
    schur_reduced_field_count: int
    quotient_field_count: int
    exact_E_zero_slice: bool
    invariant_current_combinations_exact: bool
    quotient_density_gauge_field_free: bool
    quotient_density_constraint_free: bool
    quotient_basis_complete: bool
    spatial_gauge_quotient_applied: bool


@lru_cache(maxsize=1)
def scalar_spatial_gauge_quotient():
    """Return the exact E=0 representative in invariant coordinates.

    The spatial scalar generator acts by

        E -> E - L,
        delta_J_s_0 -> delta_J_s_0 + J_s k^2 L,
        delta_J_s_L -> delta_J_s_L + J_s L'.

    Hence every orbit has the exact representative L=E, with invariant
    current coordinates

        delta_J_s_0^GI = delta_J_s_0 + J_s k^2 E,
        delta_J_s_L^GI = delta_J_s_L + J_s E'.
    """

    data = schur.scalar_lapse_shift_schur_complement()
    z = total._symbols()
    q = dict(zip(total.VARIABLES, z["q"]))
    qp = dict(zip(total.VARIABLES, z["qp"]))

    quotient_symbols = sp.symbols(
        " ".join(
            "quotient_{}".format(field)
            for field in QUOTIENT_FIELDS
        )
    )
    quotient_jet_symbols = sp.symbols(
        " ".join(
            "quotient_{}_prime".format(field)
            for field in QUOTIENT_FIELDS
        )
    )

    quotient_q = dict(zip(QUOTIENT_FIELDS, quotient_symbols))
    quotient_qp = dict(
        zip(QUOTIENT_FIELDS, quotient_jet_symbols)
    )

    gauge_slice_substitution = {
        q["E"]: sp.Integer(0),
        qp["E"]: sp.Integer(0),
    }

    for field in QUOTIENT_FIELDS:
        gauge_slice_substitution[q[field]] = quotient_q[field]
        gauge_slice_substitution[qp[field]] = quotient_qp[field]

    quotient_density = data["reduced_density"].subs(
        gauge_slice_substitution,
        simultaneous=True,
    )

    invariant_currents = {
        "delta_J_b_0": (
            q["delta_J_b_0"]
            + z["Jb"] * z["k2"] * q["E"]
        ),
        "delta_J_b_L": (
            q["delta_J_b_L"]
            + z["Jb"] * qp["E"]
        ),
        "delta_J_r_0": (
            q["delta_J_r_0"]
            + z["Jr"] * z["k2"] * q["E"]
        ),
        "delta_J_r_L": (
            q["delta_J_r_L"]
            + z["Jr"] * qp["E"]
        ),
    }

    return {
        "schur_data": data,
        "spatial_gauge_field": SPATIAL_GAUGE_FIELD,
        "quotient_fields": QUOTIENT_FIELDS,
        "quotient_symbols": quotient_q,
        "quotient_jet_symbols": quotient_qp,
        "gauge_slice_substitution": gauge_slice_substitution,
        "invariant_currents": invariant_currents,
        "quotient_density": quotient_density,
    }


@lru_cache(maxsize=1)
def certificate():
    data = scalar_spatial_gauge_quotient()
    z = total._symbols()
    q = dict(zip(total.VARIABLES, z["q"]))
    qp = dict(zip(total.VARIABLES, z["qp"]))

    L, Lp = sp.symbols(
        "spatial_gauge_parameter spatial_gauge_parameter_prime"
    )

    transformed = {
        "E": q["E"] - L,
        "E_prime": qp["E"] - Lp,
        "delta_J_b_0": (
            q["delta_J_b_0"] + z["Jb"] * z["k2"] * L
        ),
        "delta_J_b_L": (
            q["delta_J_b_L"] + z["Jb"] * Lp
        ),
        "delta_J_r_0": (
            q["delta_J_r_0"] + z["Jr"] * z["k2"] * L
        ),
        "delta_J_r_L": (
            q["delta_J_r_L"] + z["Jr"] * Lp
        ),
    }

    invariant_residuals = (
        sp.expand(
            transformed["delta_J_b_0"]
            + z["Jb"] * z["k2"] * transformed["E"]
            - data["invariant_currents"]["delta_J_b_0"]
        ),
        sp.expand(
            transformed["delta_J_b_L"]
            + z["Jb"] * transformed["E_prime"]
            - data["invariant_currents"]["delta_J_b_L"]
        ),
        sp.expand(
            transformed["delta_J_r_0"]
            + z["Jr"] * z["k2"] * transformed["E"]
            - data["invariant_currents"]["delta_J_r_0"]
        ),
        sp.expand(
            transformed["delta_J_r_L"]
            + z["Jr"] * transformed["E_prime"]
            - data["invariant_currents"]["delta_J_r_L"]
        ),
    )

    exact_slice = bool(
        sp.expand(
            transformed["E"].subs(L, q["E"])
        ) == 0
        and sp.expand(
            transformed["E_prime"].subs(Lp, qp["E"])
        ) == 0
    )

    invariants_exact = all(
        residual == 0
        for residual in invariant_residuals
    )

    quotient_density = data["quotient_density"]
    schur_data = data["schur_data"]

    gauge_free = not quotient_density.has(
        q["E"],
        qp["E"],
    )

    constraint_free = not quotient_density.has(
        *schur_data["constraint_symbols"],
        *schur_data["constraint_jet_symbols"],
    )

    quotient_atoms = (
        tuple(data["quotient_symbols"].values())
        + tuple(data["quotient_jet_symbols"].values())
    )

    original_reduced_atoms = (
        tuple(q[field] for field in schur.REDUCED_FIELDS)
        + tuple(qp[field] for field in schur.REDUCED_FIELDS)
    )

    basis_complete = bool(
        len(QUOTIENT_FIELDS) == 9
        and all(
            not quotient_density.has(atom)
            for atom in original_reduced_atoms
        )
        and all(
            atom in quotient_atoms
            for atom in quotient_atoms
        )
    )

    applied = bool(
        exact_slice
        and invariants_exact
        and gauge_free
        and constraint_free
        and basis_complete
    )

    return ScalarSpatialGaugeQuotientCertificate(
        schur_reduced_field_count=len(schur.REDUCED_FIELDS),
        quotient_field_count=len(QUOTIENT_FIELDS),
        exact_E_zero_slice=exact_slice,
        invariant_current_combinations_exact=invariants_exact,
        quotient_density_gauge_field_free=gauge_free,
        quotient_density_constraint_free=constraint_free,
        quotient_basis_complete=basis_complete,
        spatial_gauge_quotient_applied=applied,
    )
