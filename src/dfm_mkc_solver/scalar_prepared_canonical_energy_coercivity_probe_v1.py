"""Exact first coercivity probe for the prepared canonical scalar energy.

This module does not assume positivity of the full reduced Hamiltonian. It
applies Sylvester's criterion to the quadratic energy on the canonical reduced
state

    (delta_phi', delta_theta',
     delta_phi, delta_theta,
     delta_J_b_0, delta_ell_b,
     delta_J_r_0, delta_ell_r)

on the prepared quadratic positive-charge branch. The first leading principal
pivot whose strict sign is not certified is returned as the authoritative
boundary.

The implementation uses an exact incremental LDL^T factorization rather than
recomputing every leading determinant by Berkowitz. For a symmetric matrix,
strict positivity of every LDL^T pivot is equivalent to strict positivity of
all leading principal minors, so the mathematical target is unchanged while
avoiding the previous CI timeout.
"""

from __future__ import annotations

from functools import lru_cache
from types import MappingProxyType

import sympy as sp

from . import scalar_prepared_canonical_energy_v1 as canonical
from . import scalar_prepared_time_gauge_quotient_action_v1 as quotient
from . import total_scalar_lapse_shift_hessian_v1 as total


CONFIGURATION_FIELDS = canonical.PHYSICAL_FIELDS
SECOND_ORDER_FIELDS = ("delta_phi", "delta_theta")


def _immutable(mapping):
    return MappingProxyType(dict(mapping))


def _normalize(expression):
    return sp.factor_terms(expression)


def _strict_sign(expression):
    """Return a conservative exact sign classification."""
    expression = _normalize(expression)
    if expression == 0:
        return "zero"
    if expression.is_positive is True:
        return "positive"
    if expression.is_negative is True:
        return "negative"
    return "unresolved"


@lru_cache(maxsize=1)
def scalar_prepared_canonical_energy_coercivity_probe():
    energy = canonical.scalar_prepared_canonical_energy_data()
    action = quotient.scalar_prepared_time_gauge_quotient_action()
    hq = dict(action["independent_chart_symbols"])
    hqp = dict(action["independent_chart_jet_symbols"])
    z = total._symbols()

    # Exact prepared quadratic positive-charge branch used by the repository's
    # existence theorem. The positive-charge phase relation, current-density
    # identities, and Friedmann identity are already established background
    # identities on this branch; encoding them here removes independent
    # background variables without adding a sign assumption.
    mu_squared = sp.symbols("prepared_mu_squared", positive=True)
    phi_positive = sp.symbols("prepared_phi_bar", positive=True)
    charge_positive = sp.symbols("prepared_q", positive=True)
    rho_b, rho_r, rho_lambda = sp.symbols(
        "prepared_rho_b prepared_rho_r prepared_rho_lambda",
        nonnegative=True,
    )

    rho_total = (
        rho_b
        + rho_r
        + rho_lambda
        + z["alpha"] * z["php"]**2 / (2 * z["a"]**2)
        + charge_positive**2
        / (2 * z["beta"] * z["a"]**6 * phi_positive**2)
        + mu_squared * phi_positive**2 / 2
    )
    prepared_substitution = {
        z["lam"]: sp.Integer(0),
        z["rho_star"]: sp.Integer(0),
        z["m2"]: mu_squared,
        z["ph"]: phi_positive,
        z["thp"]: (
            charge_positive
            / (z["beta"] * z["a"]**2 * phi_positive**2)
        ),
        z["Jb"]: z["a"]**3 * rho_b / z["mb"],
        z["Jr"]: (
            z["a"]**4 * rho_r / z["kr"]
        ) ** sp.Rational(3, 4),
        z["Lambda"]: 8 * sp.pi * z["G"] * rho_lambda,
        z["H"]**2: (
            8 * sp.pi * z["G"] * z["a"]**2 * rho_total / 3
        ),
    }

    energy_density = energy["canonical_energy_density"].subs(
        prepared_substitution, simultaneous=True
    )

    state_atoms = (
        hqp["delta_phi"],
        hqp["delta_theta"],
        hq["delta_phi"],
        hq["delta_theta"],
        hq["delta_J_b_0"],
        hq["delta_ell_b"],
        hq["delta_J_r_0"],
        hq["delta_ell_r"],
    )

    hessian = sp.Matrix([
        [sp.diff(energy_density, left, right) for right in state_atoms]
        for left in state_atoms
    ])
    symmetric = all(
        sp.cancel(hessian[i, j] - hessian[j, i]) == 0
        for i in range(len(state_atoms))
        for j in range(len(state_atoms))
    )
    if not symmetric:
        raise AssertionError("canonical energy Hessian is not symmetric")

    n = len(state_atoms)
    L = [[sp.Integer(0) for _ in range(n)] for _ in range(n)]
    pivots = []
    pivot_statuses = []
    leading_minors = []
    leading_minor_statuses = []
    first_obstruction = None
    cumulative_minor = sp.Integer(1)

    for k in range(n):
        diagonal_correction = sum(
            L[k][j] ** 2 * pivots[j]
            for j in range(k)
        )
        pivot = _normalize(hessian[k, k] - diagonal_correction)
        pivot_status = _strict_sign(pivot)
        pivots.append(pivot)
        pivot_statuses.append(pivot_status)

        cumulative_minor = _normalize(cumulative_minor * pivot)
        leading_minors.append(cumulative_minor)
        leading_minor_statuses.append(_strict_sign(cumulative_minor))

        if pivot_status != "positive":
            first_obstruction = (k + 1, pivot_status, pivot)
            break

        L[k][k] = sp.Integer(1)
        for i in range(k + 1, n):
            off_diagonal_correction = sum(
                L[i][j] * L[k][j] * pivots[j]
                for j in range(k)
            )
            L[i][k] = _normalize(
                (hessian[i, k] - off_diagonal_correction) / pivot
            )

    all_positive = first_obstruction is None and len(pivots) == n
    return _immutable({
        "state_order": tuple(str(atom) for atom in state_atoms),
        "hessian_symmetric": symmetric,
        "ldlt_pivots": tuple(pivots),
        "ldlt_pivot_statuses": tuple(pivot_statuses),
        "leading_minors": tuple(leading_minors),
        "leading_minor_statuses": tuple(leading_minor_statuses),
        "first_obstruction": first_obstruction,
        "all_leading_minors_strictly_positive": all_positive,
        "sylvester_coercivity_established": all_positive,
        "prepared_branch_substitution": _immutable(prepared_substitution),
        "algorithm": "exact incremental LDL^T pivots",
    })
