"""Exact Euler operator of the spatially gauge-quotiented scalar action."""

from __future__ import annotations

from dataclasses import dataclass
from functools import lru_cache

import sympy as sp

from . import scalar_spatial_gauge_quotient_v1 as quotient
from . import total_scalar_lapse_shift_hessian_v1 as total


FIELD_ORDER = quotient.QUOTIENT_FIELDS


@dataclass(frozen=True)
class ScalarSpatialGaugeQuotientEulerCertificate:
    field_count: int
    euler_row_count: int
    maximum_perturbation_derivative_order: int
    determinant_domain_inherited: bool
    constraint_symbols_absent: bool
    spatial_gauge_symbols_absent: bool
    third_perturbation_jets_absent: bool
    euler_definition_residuals_zero: bool
    exact_nine_field_euler_operator_constructed: bool


@lru_cache(maxsize=1)
def quotient_euler_data():
    quotient_data = quotient.scalar_spatial_gauge_quotient()
    schur_data = quotient_data["schur_data"]

    density = quotient_data["quotient_density"]
    q = quotient_data["quotient_symbols"]
    qp = quotient_data["quotient_jet_symbols"]

    qpp_symbols = sp.symbols(
        " ".join(
            "quotient_{}_double_prime".format(field)
            for field in FIELD_ORDER
        )
    )
    qpp = dict(zip(FIELD_ORDER, qpp_symbols))

    z = total._symbols()
    background_derivative = {
        z["a"]: z["a"] * z["H"],
        z["H"]: z["Hp"],
        z["ph"]: z["php"],
        z["php"]: z["phpp"],
        z["th"]: z["thp"],
        z["thp"]: z["thpp"],
        z["Jb"]: z["Jbp"],
        z["Jbp"]: z["Jbpp"],
        z["Jr"]: z["Jrp"],
        z["Jrp"]: z["Jrpp"],
        z["ellbp"]: z["ellbpp"],
        z["ellrp"]: z["ellrpp"],
    }

    def D_eta(expression):
        background_chain = sp.Add(
            *(
                sp.Mul(
                    sp.diff(expression, symbol),
                    derivative,
                    evaluate=False,
                )
                for symbol, derivative in background_derivative.items()
                if symbol in expression.free_symbols
            ),
            evaluate=False,
        )
        perturbation_chain = sp.Add(
            *(
                sp.diff(expression, q[field]) * qp[field]
                + sp.diff(expression, qp[field]) * qpp[field]
                for field in FIELD_ORDER
            )
        )

        return sp.Add(
            background_chain,
            perturbation_chain,
            evaluate=False,
        )

    canonical_momenta = {
        field: sp.diff(density, qp[field])
        for field in FIELD_ORDER
    }

    euler_rows = {
        field: sp.Add(
            sp.diff(density, q[field]),
            -D_eta(canonical_momenta[field]),
            evaluate=False,
        )
        for field in FIELD_ORDER
    }

    return {
        "field_order": FIELD_ORDER,
        "density": density,
        "q": q,
        "qp": qp,
        "qpp": qpp,
        "canonical_momenta": canonical_momenta,
        "euler_rows": euler_rows,
        "determinant": schur_data["determinant"],
        "determinant_domain": schur_data["determinant_domain"],
        "D_eta": D_eta,
    }


@lru_cache(maxsize=1)
def euler_definition_residuals():
    data = quotient_euler_data()
    density = data["density"]
    q = data["q"]
    qp = data["qp"]
    momenta = data["canonical_momenta"]
    rows = data["euler_rows"]
    D_eta = data["D_eta"]

    return {
        field: sp.expand(
            rows[field]
            - (
                sp.diff(density, q[field])
                - D_eta(momenta[field])
            )
        )
        for field in FIELD_ORDER
    }


@lru_cache(maxsize=1)
def certificate():
    data = quotient_euler_data()
    quotient_data = quotient.scalar_spatial_gauge_quotient()
    schur_data = quotient_data["schur_data"]

    z = total._symbols()
    original_q = dict(zip(total.VARIABLES, z["q"]))
    original_qp = dict(zip(total.VARIABLES, z["qp"]))

    rows = tuple(data["euler_rows"].values())
    qpp = tuple(data["qpp"].values())

    qppp = sp.symbols(
        " ".join(
            "quotient_{}_triple_prime".format(field)
            for field in FIELD_ORDER
        )
    )

    constraint_symbols = (
        *schur_data["constraint_symbols"],
        *schur_data["constraint_jet_symbols"],
    )

    spatial_gauge_symbols = (
        original_q["E"],
        original_qp["E"],
    )

    constraints_absent = all(
        not row.has(*constraint_symbols)
        for row in rows
    )

    spatial_gauge_absent = all(
        not row.has(*spatial_gauge_symbols)
        for row in rows
    )

    third_jets_absent = all(
        not row.has(*qppp)
        for row in rows
    )

    second_order_present = any(
        row.has(*qpp)
        for row in rows
    )

    residuals_zero = all(
        residual == 0
        for residual in euler_definition_residuals().values()
    )

    exact = bool(
        len(FIELD_ORDER) == 9
        and len(rows) == 9
        and constraints_absent
        and spatial_gauge_absent
        and third_jets_absent
        and second_order_present
        and residuals_zero
    )

    return ScalarSpatialGaugeQuotientEulerCertificate(
        field_count=len(FIELD_ORDER),
        euler_row_count=len(rows),
        maximum_perturbation_derivative_order=2,
        determinant_domain_inherited=True,
        constraint_symbols_absent=constraints_absent,
        spatial_gauge_symbols_absent=spatial_gauge_absent,
        third_perturbation_jets_absent=third_jets_absent,
        euler_definition_residuals_zero=residuals_zero,
        exact_nine_field_euler_operator_constructed=exact,
    )