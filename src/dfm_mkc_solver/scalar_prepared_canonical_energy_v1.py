"""Canonical scalar second-variation energy on the prepared DFM-MKC branch.

This module takes the already action-derived scalar reduction literally:

1. start from the exact spatial-gauge quotient of the canonical quadratic
   action;
2. pull it to the prepared global H-chart ``psi = 0``;
3. substitute the exact longitudinal-current auxiliary solution; and
4. perform the Legendre construction on the six retained physical variables.

The resulting expression is the canonical quadratic energy density

    E_2 = sum_i q_i' * dL_phys/dq_i' - L_phys.

No positivity claim is built into the definition. The repository proves a
strictly nondegenerate principal system on the prepared positive-density
branch, but that fact alone does not imply positivity of the full reduced
Hamiltonian once lower-order gravitational and mass terms are included.
Accordingly ``full_coercivity_established`` remains False here unless a later
certificate proves the full quadratic form positive.
"""

from __future__ import annotations

from functools import lru_cache
from types import MappingProxyType

import sympy as sp

from . import scalar_prepared_auxiliary_elimination_v1 as auxiliary
from . import scalar_prepared_time_gauge_quotient_action_v1 as quotient_action


PHYSICAL_FIELDS = (
    "delta_phi",
    "delta_theta",
    "delta_J_b_0",
    "delta_ell_b",
    "delta_J_r_0",
    "delta_ell_r",
)


def _zero_scalar(expression):
    numerator = sp.together(expression).as_numer_denom()[0]
    return sp.expand(numerator)


def _immutable_mapping(mapping):
    return MappingProxyType(dict(mapping))


@lru_cache(maxsize=1)
def scalar_prepared_canonical_energy_data():
    """Return the exact reduced Lagrangian and its Legendre energy density."""

    action = quotient_action.scalar_prepared_time_gauge_quotient_action()
    h_fields = tuple(action["h_chart_field_order"])
    if h_fields != (
        "delta_phi",
        "delta_theta",
        "delta_J_b_0",
        "delta_J_b_L",
        "delta_ell_b",
        "delta_J_r_0",
        "delta_J_r_L",
        "delta_ell_r",
    ):
        raise AssertionError(("h_chart_field_order", h_fields))

    hq = dict(action["independent_chart_symbols"])
    hqp = dict(action["independent_chart_jet_symbols"])
    L_H = action["quotient_density"]

    aux = auxiliary.scalar_prepared_auxiliary_solution()
    if tuple(aux["order"]) != ("delta_J_b_L", "delta_J_r_L"):
        raise AssertionError(("auxiliary_order", tuple(aux["order"])))
    if any(value != 0 for value in aux["solution_reconstruction_residuals"]):
        raise AssertionError("auxiliary solution is not exact")

    # The imported solution is written in the spatial-quotient symbols. The
    # prepared action exports the exact embedding into H-chart symbols.
    embedding = dict(action["embedding_substitution"])
    imported_solution = tuple(aux["solution"])
    solution_H = tuple(
        expression.subs(embedding, simultaneous=True)
        for expression in imported_solution
    )
    auxiliary_substitution = {
        hq["delta_J_b_L"]: solution_H[0],
        hq["delta_J_r_L"]: solution_H[1],
    }

    L_phys = L_H.subs(auxiliary_substitution, simultaneous=True)
    if L_phys.has(hq["delta_J_b_L"], hq["delta_J_r_L"]):
        raise AssertionError("reduced Lagrangian still contains auxiliaries")

    canonical_momenta = {
        field: sp.diff(L_phys, hqp[field])
        for field in PHYSICAL_FIELDS
    }
    velocity_pairing = sp.Add(
        *(
            hqp[field] * canonical_momenta[field]
            for field in PHYSICAL_FIELDS
        ),
        evaluate=False,
    )
    energy_density = sp.Add(velocity_pairing, -L_phys, evaluate=False)

    # Expose the no-first-jet part separately. Its sign is deliberately not
    # asserted: this is where a later full coercivity theorem must work.
    zero_jets = {hqp[field]: sp.Integer(0) for field in PHYSICAL_FIELDS}
    lower_order_energy = energy_density.subs(zero_jets, simultaneous=True)
    kinetic_energy = sp.Add(
        energy_density,
        -lower_order_energy,
        evaluate=False,
    )

    all_state_atoms = tuple(hq[field] for field in PHYSICAL_FIELDS) + tuple(
        hqp[field] for field in PHYSICAL_FIELDS
    )
    zero_state = {atom: sp.Integer(0) for atom in all_state_atoms}
    energy_zero_residual = _zero_scalar(
        energy_density.xreplace(zero_state)
    )
    legendre_residual = _zero_scalar(
        energy_density - velocity_pairing + L_phys
    )
    split_residual = _zero_scalar(
        energy_density - kinetic_energy - lower_order_energy
    )

    return _immutable_mapping({
        "physical_fields": PHYSICAL_FIELDS,
        "reduced_lagrangian_density": L_phys,
        "canonical_momenta": _immutable_mapping(canonical_momenta),
        "velocity_pairing": velocity_pairing,
        "canonical_energy_density": energy_density,
        "kinetic_energy_part": kinetic_energy,
        "lower_order_energy_part": lower_order_energy,
        "auxiliary_substitution": _immutable_mapping(auxiliary_substitution),
        "legendre_identity_residual": legendre_residual,
        "energy_zero_state_residual": energy_zero_residual,
        "energy_split_residual": split_residual,
        "action_derived": True,
        "auxiliaries_exactly_eliminated": True,
        "prepared_principal_nondegenerate": True,
        "full_coercivity_established": False,
    })


def scalar_prepared_canonical_energy_theorem():
    """Return the exact derivation statement and its current boundary."""

    data = scalar_prepared_canonical_energy_data()
    exact = bool(
        data["legendre_identity_residual"] == 0
        and data["energy_zero_state_residual"] == 0
        and data["energy_split_residual"] == 0
        and data["action_derived"]
        and data["auxiliaries_exactly_eliminated"]
    )
    if not exact:
        raise AssertionError("canonical energy derivation is not exact")

    return _immutable_mapping({
        "canonical_scalar_second_variation_energy_derived": True,
        "physical_fields": data["physical_fields"],
        "prepared_principal_nondegenerate":
            data["prepared_principal_nondegenerate"],
        "full_coercivity_established": False,
        "limitations": (
            "The full lower-order reduced Hamiltonian has not been proved positive.",
            "No coercive constant for metric potentials is asserted.",
            "No Fourier-to-pointwise spherical derivative estimate is asserted.",
            "No comparison with the Chronos E_grav or boundary flux is asserted.",
        ),
    })
