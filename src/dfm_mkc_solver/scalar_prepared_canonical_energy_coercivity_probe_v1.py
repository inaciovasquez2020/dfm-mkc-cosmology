"""Exact first coercivity probe for the prepared canonical scalar energy.

This module does not assume positivity of the full reduced Hamiltonian.  It
applies Sylvester's criterion to the quadratic energy on the canonical reduced
state

    (delta_phi', delta_theta',
     delta_phi, delta_theta,
     delta_J_b_0, delta_ell_b,
     delta_J_r_0, delta_ell_r)

on the prepared quadratic positive-charge branch.  The first leading minor
whose strict sign is not certified is returned as the authoritative boundary.
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


def _strict_sign(expression):
    """Return a conservative exact sign classification."""
    expression = sp.factor(sp.cancel(expression))
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
    # existence theorem.  The replacement symbols encode only strict signs
    # already present in that branch; no sign is assigned to background time
    # derivatives.
    mu_squared = sp.symbols("prepared_mu_squared", positive=True)
    phi_positive = sp.symbols("prepared_phi_bar", positive=True)
    prepared_substitution = {
        z["lam"]: sp.Integer(0),
        z["rho_star"]: sp.Integer(0),
        z["m2"]: mu_squared,
        z["ph"]: phi_positive,
    }

    energy_density = sp.cancel(
        energy["canonical_energy_density"].subs(
            prepared_substitution, simultaneous=True
        )
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
        [sp.cancel(sp.diff(energy_density, left, right)) for right in state_atoms]
        for left in state_atoms
    ])
    symmetric = all(
        sp.cancel(hessian[i, j] - hessian[j, i]) == 0
        for i in range(len(state_atoms))
        for j in range(len(state_atoms))
    )
    if not symmetric:
        raise AssertionError("canonical energy Hessian is not symmetric")

    leading_minors = []
    statuses = []
    first_obstruction = None
    for size in range(1, len(state_atoms) + 1):
        minor = sp.factor(sp.cancel(hessian[:size, :size].det(method="berkowitz")))
        status = _strict_sign(minor)
        leading_minors.append(minor)
        statuses.append(status)
        if status != "positive":
            first_obstruction = (size, status, minor)
            break

    all_positive = first_obstruction is None and len(leading_minors) == len(state_atoms)
    return _immutable({
        "state_order": tuple(str(atom) for atom in state_atoms),
        "hessian_symmetric": symmetric,
        "leading_minors": tuple(leading_minors),
        "leading_minor_statuses": tuple(statuses),
        "first_obstruction": first_obstruction,
        "all_leading_minors_strictly_positive": all_positive,
        "sylvester_coercivity_established": all_positive,
        "prepared_branch_substitution": _immutable(prepared_substitution),
    })
