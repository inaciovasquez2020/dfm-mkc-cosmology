"""Exact algebraic A/B Schur complement of the scalar quadratic action."""

from __future__ import annotations

from dataclasses import dataclass
from functools import lru_cache

import sympy as sp

from . import complete_scalar_quadratic_action_v1 as complete
from . import total_scalar_lapse_shift_hessian_v1 as total


CONSTRAINT_FIELDS = ("A", "B")
REDUCED_FIELDS = tuple(
    field
    for field in complete.FIELD_ORDER
    if field not in CONSTRAINT_FIELDS
)


@dataclass(frozen=True)
class ScalarLapseShiftSchurComplementCertificate:
    constraint_fields: tuple[str, str]
    reduced_fields: tuple[str, ...]
    constraint_time_jets_absent: bool
    constraint_block_symmetric: bool
    constraint_gradient_affine: bool
    adjugate_identity_exact: bool
    constraint_solution_exact: bool
    reduced_density_constraint_free: bool
    determinant_domain_required: bool
    exact_schur_complement_constructed: bool
    spatial_gauge_quotient_applied: bool


@lru_cache(maxsize=1)
def scalar_lapse_shift_schur_complement():
    """Return the exact density-level A/B Schur-complement data."""

    if complete.FIELD_ORDER != total.VARIABLES:
        raise ValueError("canonical field orders disagree")

    density = complete.quadratic_action()["density"]
    z = total._symbols()
    q = dict(zip(total.VARIABLES, z["q"]))
    qp = dict(zip(total.VARIABLES, z["qp"]))

    A = q["A"]
    B = q["B"]
    zero_constraints = {A: 0, B: 0}

    constraint_block = sp.Matrix(
        [
            [
                sp.diff(density, q[left], q[right])
                for right in CONSTRAINT_FIELDS
            ]
            for left in CONSTRAINT_FIELDS
        ]
    )

    source_vector = sp.Matrix(
        [
            sp.diff(density, q[field]).subs(
                zero_constraints,
                simultaneous=True,
            )
            for field in CONSTRAINT_FIELDS
        ]
    )

    determinant = sp.expand(
        constraint_block[0, 0] * constraint_block[1, 1]
        - constraint_block[0, 1] * constraint_block[1, 0]
    )

    adjugate = sp.Matrix(
        [
            [constraint_block[1, 1], -constraint_block[0, 1]],
            [-constraint_block[1, 0], constraint_block[0, 0]],
        ]
    )

    solution_numerator = -adjugate * source_vector
    solution = sp.Matrix(
        [
            solution_numerator[index] / determinant
            for index in range(2)
        ]
    )

    unconstrained_density = density.subs(
        zero_constraints,
        simultaneous=True,
    )

    correction = (
        source_vector.T * adjugate * source_vector
    )[0] / (2 * determinant)

    reduced_density = sp.Add(
        unconstrained_density,
        -correction,
        evaluate=False,
    )

    return {
        "density": density,
        "constraint_fields": CONSTRAINT_FIELDS,
        "reduced_fields": REDUCED_FIELDS,
        "constraint_symbols": (A, B),
        "constraint_jet_symbols": (qp["A"], qp["B"]),
        "constraint_block": constraint_block,
        "source_vector": source_vector,
        "determinant": determinant,
        "determinant_domain": sp.Ne(
            determinant,
            0,
            evaluate=False,
        ),
        "adjugate": adjugate,
        "solution_numerator": solution_numerator,
        "solution": solution,
        "reduced_density": reduced_density,
    }


@lru_cache(maxsize=1)
def certificate():
    data = scalar_lapse_shift_schur_complement()

    density = data["density"]
    A, B = data["constraint_symbols"]
    A_prime, B_prime = data["constraint_jet_symbols"]
    block = data["constraint_block"]
    source = data["source_vector"]
    determinant = data["determinant"]
    adjugate = data["adjugate"]
    solution_numerator = data["solution_numerator"]
    reduced_density = data["reduced_density"]

    constraints = sp.Matrix([A, B])
    gradient = sp.Matrix(
        [
            sp.diff(density, A),
            sp.diff(density, B),
        ]
    )

    affine_residual = gradient - block * constraints - source
    adjugate_residual = (
        block * adjugate - determinant * sp.eye(2)
    )
    solution_residual = (
        block * solution_numerator
        + determinant * source
    )

    no_constraint_jets = all(
        sp.expand(sp.diff(density, jet)) == 0
        for jet in (A_prime, B_prime)
    )

    block_symmetric = all(
        sp.expand(
            block[left, right] - block[right, left]
        ) == 0
        for left in range(2)
        for right in range(2)
    )

    affine_exact = all(
        sp.expand(value) == 0
        for value in affine_residual
    )

    adjugate_exact = all(
        sp.expand(value) == 0
        for value in adjugate_residual
    )

    solution_exact = all(
        sp.expand(value) == 0
        for value in solution_residual
    )

    reduced_constraint_free = not reduced_density.has(
        A,
        B,
        A_prime,
        B_prime,
    )

    exact = bool(
        no_constraint_jets
        and block_symmetric
        and affine_exact
        and adjugate_exact
        and solution_exact
        and reduced_constraint_free
    )

    return ScalarLapseShiftSchurComplementCertificate(
        constraint_fields=CONSTRAINT_FIELDS,
        reduced_fields=REDUCED_FIELDS,
        constraint_time_jets_absent=no_constraint_jets,
        constraint_block_symmetric=block_symmetric,
        constraint_gradient_affine=affine_exact,
        adjugate_identity_exact=adjugate_exact,
        constraint_solution_exact=solution_exact,
        reduced_density_constraint_free=reduced_constraint_free,
        determinant_domain_required=True,
        exact_schur_complement_constructed=exact,
        spatial_gauge_quotient_applied=False,
    )
