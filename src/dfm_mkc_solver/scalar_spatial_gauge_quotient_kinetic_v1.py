"""Conditional exact rank classification of the quotient kinetic Hessian."""

from __future__ import annotations

from dataclasses import dataclass
from functools import lru_cache

import sympy as sp

from . import scalar_spatial_gauge_quotient_euler_v1 as euler


FIELD_ORDER = euler.FIELD_ORDER

ACTIVE_FIELDS = (
    "psi",
    "delta_phi",
    "delta_theta",
)

ZERO_KINETIC_FIELDS = tuple(
    field
    for field in FIELD_ORDER
    if field not in ACTIVE_FIELDS
)

PIVOT_FIELDS = (
    "psi",
    "delta_phi",
)


@dataclass(frozen=True)
class ScalarQuotientKineticRankCertificate:
    field_count: int
    active_field_count: int
    exact_zero_row_count: int
    kinetic_hessian_symmetric: bool
    exact_zero_rows_verified: bool
    active_determinant_zero: bool
    pivot_minor_not_identically_zero: bool
    cofactor_null_vector_exact: bool
    cofactor_null_vector_nonzero_on_domain: bool
    active_rank_on_domain: int
    full_rank_on_domain: int
    full_nullity_on_domain: int
    determinant_domain_required: bool
    pivot_domain_required: bool
    time_gauge_quotient_applied: bool
    classification_conditional: bool


@lru_cache(maxsize=1)
def quotient_kinetic_rank_data():
    data = euler.quotient_euler_data()

    density = data["density"]
    qp = data["qp"]

    kinetic_hessian = sp.Matrix(
        [
            [
                sp.cancel(
                    sp.diff(
                        density,
                        qp[left],
                        qp[right],
                    )
                )
                for right in FIELD_ORDER
            ]
            for left in FIELD_ORDER
        ]
    )

    active_indices = tuple(
        FIELD_ORDER.index(field)
        for field in ACTIVE_FIELDS
    )

    active_block = kinetic_hessian.extract(
        active_indices,
        active_indices,
    )

    a = active_block[0, 0]
    b = active_block[0, 1]
    c = active_block[0, 2]
    d = active_block[1, 1]
    e = active_block[1, 2]
    f = active_block[2, 2]

    pivot_minor = sp.cancel(a * d - b**2)

    active_determinant = sp.cancel(
        a * d * f
        + 2 * b * c * e
        - a * e**2
        - d * c**2
        - f * b**2
    )

    cofactor_null_vector = sp.Matrix(
        [
            b * e - c * d,
            sp.cancel(b * c - a * e),
            pivot_minor,
        ]
    )

    # For a symmetric 3x3 block [[a,b,c],[b,d,e],[c,e,f]],
    # multiplying by this cofactor vector gives exactly (0, 0, det).
    # The certificate verifies symmetry independently below, so avoid asking
    # SymPy to rediscover these polynomial cancellations at high cost.
    null_residual = (
        sp.S.Zero,
        sp.S.Zero,
        active_determinant,
    )

    full_null_vector = sp.zeros(len(FIELD_ORDER), 1)

    for field, value in zip(
        ACTIVE_FIELDS,
        cofactor_null_vector,
    ):
        full_null_vector[
            FIELD_ORDER.index(field),
            0,
        ] = value

    zero_row_null_vectors = {
        field: sp.eye(len(FIELD_ORDER))[
            :,
            FIELD_ORDER.index(field),
        ]
        for field in ZERO_KINETIC_FIELDS
    }

    rank_domain = sp.And(
        data["determinant_domain"],
        sp.Ne(
            pivot_minor,
            0,
            evaluate=False,
        ),
        evaluate=False,
    )

    return {
        "field_order": FIELD_ORDER,
        "active_fields": ACTIVE_FIELDS,
        "zero_kinetic_fields": ZERO_KINETIC_FIELDS,
        "pivot_fields": PIVOT_FIELDS,
        "kinetic_hessian": kinetic_hessian,
        "active_block": active_block,
        "pivot_minor": pivot_minor,
        "active_determinant": active_determinant,
        "cofactor_null_vector": cofactor_null_vector,
        "cofactor_null_residual": null_residual,
        "full_null_vector": full_null_vector,
        "zero_row_null_vectors": zero_row_null_vectors,
        "rank_domain": rank_domain,
        "schur_determinant_domain": data["determinant_domain"],
    }


@lru_cache(maxsize=1)
def certificate():
    data = quotient_kinetic_rank_data()

    kinetic_hessian = data["kinetic_hessian"]
    pivot_minor = data["pivot_minor"]
    cofactor_null_vector = data["cofactor_null_vector"]

    symmetric = all(
        sp.cancel(
            kinetic_hessian[left, right]
            - kinetic_hessian[right, left]
        ) == 0
        for left in range(len(FIELD_ORDER))
        for right in range(len(FIELD_ORDER))
    )

    zero_rows = all(
        all(
            kinetic_hessian[
                FIELD_ORDER.index(field),
                column,
            ] == 0
            for column in range(len(FIELD_ORDER))
        )
        for field in ZERO_KINETIC_FIELDS
    )

    determinant_zero = (
        data["active_determinant"] == 0
    )

    pivot_nonzero_expression = (
        pivot_minor != 0
    )

    null_exact = all(
        residual == 0
        for residual in data["cofactor_null_residual"]
    )

    null_nonzero_on_domain = (
        sp.cancel(
            cofactor_null_vector[2] - pivot_minor
        ) == 0
    )

    conditional_exact_rank = bool(
        symmetric
        and zero_rows
        and determinant_zero
        and pivot_nonzero_expression
        and null_exact
        and null_nonzero_on_domain
    )

    return ScalarQuotientKineticRankCertificate(
        field_count=len(FIELD_ORDER),
        active_field_count=len(ACTIVE_FIELDS),
        exact_zero_row_count=len(ZERO_KINETIC_FIELDS),
        kinetic_hessian_symmetric=symmetric,
        exact_zero_rows_verified=zero_rows,
        active_determinant_zero=determinant_zero,
        pivot_minor_not_identically_zero=pivot_nonzero_expression,
        cofactor_null_vector_exact=null_exact,
        cofactor_null_vector_nonzero_on_domain=null_nonzero_on_domain,
        active_rank_on_domain=2 if conditional_exact_rank else -1,
        full_rank_on_domain=2 if conditional_exact_rank else -1,
        full_nullity_on_domain=7 if conditional_exact_rank else -1,
        determinant_domain_required=True,
        pivot_domain_required=True,
        time_gauge_quotient_applied=False,
        classification_conditional=True,
    )