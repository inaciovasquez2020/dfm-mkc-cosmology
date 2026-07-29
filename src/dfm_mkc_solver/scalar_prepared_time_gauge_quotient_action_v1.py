"""Positive-density prepared H-chart quotient action and principal system.

The canonical orientation in this module is a result of differentiating the
H-chart Euler rows.  In particular, no preferred sign is supplied to either
visible-sector symplectic block.
"""

from __future__ import annotations

from functools import lru_cache
from types import MappingProxyType

import sympy as sp

from . import prepared_alpha_family_existence_v1 as alpha_family
from . import prepared_positive_visible_density_subfamily_v1 as positive
from . import scalar_bardeen_weyl_observable_v1 as bardeen
from . import scalar_prepared_auxiliary_elimination_v1 as auxiliary
from . import scalar_prepared_lapse_shift_determinant_v1 as prepared
from . import scalar_reduced_time_gauge_atlas_v1 as atlas
from . import scalar_reduced_time_gauge_direction_v1 as direction
from . import scalar_spatial_gauge_quotient_euler_v1 as quotient_euler
from . import scalar_spatial_gauge_quotient_v1 as quotient
from . import total_scalar_lapse_shift_hessian_v1 as total


CERTIFICATE_KEYS = (
    "h_chart_configuration_condition",
    "h_chart_jet_condition",
    "h_chart_retraction_identity",
    "h_chart_projection_idempotence",
    "h_chart_orbit_annihilation",
    "quadratic_projection_reconstruction",
    "linear_projection_reconstruction",
    "quotient_density_pullback",
    "quotient_euler_reconstruction",
    "baryon_canonical_block",
    "radiation_canonical_block",
    "auxiliary_solution_reconstruction",
    "physical_principal_determinant",
    "weyl_reconstruction",
)

EXPECTED_FIELD_ORDER = (
    "psi",
    "delta_phi",
    "delta_theta",
    "delta_J_b_0",
    "delta_J_b_L",
    "delta_ell_b",
    "delta_J_r_0",
    "delta_J_r_L",
    "delta_ell_r",
)
H_CHART_FIELDS = EXPECTED_FIELD_ORDER[1:]
PHYSICAL_STATE_ORDER = (
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


def _first_nonzero(expressions):
    for expression in expressions:
        residual = _zero_scalar(expression)
        if residual != 0:
            return residual
    return sp.Integer(0)


def _matrix_residual(left, right):
    if left.shape != right.shape:
        return sp.Integer(1)
    return _first_nonzero(
        left[i, j] - right[i, j]
        for i in range(left.rows)
        for j in range(left.cols)
    )


def _immutable_mapping(mapping):
    return MappingProxyType(dict(mapping))


@lru_cache(maxsize=1)
def _construction():
    # Read-only audit.  This is the sole direct quotient call in this module.
    source = quotient.scalar_spatial_gauge_quotient()
    fields = tuple(source["quotient_fields"])
    if fields != EXPECTED_FIELD_ORDER or len(fields) != 9:
        raise AssertionError(("spatial_quotient_field_order", fields))

    generator = direction.reduced_time_gauge_first_jet_prolongation_data()
    z = total._symbols()
    H = z["H"]
    R = generator["configuration_coefficients"]
    if _zero_scalar(R["psi"] - H) != 0:
        raise AssertionError(("time_generator_psi_coefficient", R["psi"] - H))

    atlas_data = atlas.reduced_time_gauge_atlas()
    if _zero_scalar(atlas_data["chart_shifts"]["psi"] + source[
        "quotient_symbols"
    ]["psi"] / H) != 0:
        raise AssertionError(("psi_chart_shift", atlas_data["chart_shifts"]["psi"]))

    family_claim = alpha_family.prepared_alpha_family_existence_theorem()[
        "nonnegative_decomposition_inequalities"
    ]
    if "H_L>=H_floor>0" not in family_claim:
        raise AssertionError(("prepared_H_floor", family_claim))
    positive_data = positive.prepared_positive_visible_density_subfamily_data()
    strict = positive_data["strict_claims"]
    if not strict["rho_b0_positive"] or not strict["rho_r0_positive"]:
        raise AssertionError(("positive_visible_density", strict))

    imported_solution = auxiliary.scalar_prepared_auxiliary_solution()
    if not isinstance(imported_solution, MappingProxyType):
        raise AssertionError(("immutable_auxiliary_solution", type(imported_solution)))
    auxiliary_data = auxiliary.scalar_prepared_auxiliary_elimination_data()
    expected_det = z["a"]**4 * z["alpha"] * z["beta"] * z["ph"]**2
    actual_det = auxiliary_data["prepared_scalar_factors"][
        "det_K_effective"
    ]
    if _zero_scalar(actual_det - expected_det) != 0:
        raise AssertionError(("effective_kinetic_determinant", actual_det))
    if dict(auxiliary_data["unresolved_factors"]):
        raise AssertionError(("unresolved_factor", auxiliary_data["unresolved_factors"]))
    if not callable(bardeen.bardeen_weyl_definitions):
        raise AssertionError(("bardeen_weyl_definitions", None))

    q = source["quotient_symbols"]
    qp = source["quotient_jet_symbols"]
    chart_q_symbols = sp.symbols(
        " ".join(f"h_{field}" for field in H_CHART_FIELDS)
    )
    chart_qp_symbols = sp.symbols(
        " ".join(f"h_{field}_prime" for field in H_CHART_FIELDS)
    )
    hq = dict(zip(H_CHART_FIELDS, chart_q_symbols))
    hqp = dict(zip(H_CHART_FIELDS, chart_qp_symbols))
    embedding = {q["psi"]: sp.Integer(0), qp["psi"]: sp.Integer(0)}
    embedding.update({q[field]: hq[field] for field in H_CHART_FIELDS})
    embedding.update({qp[field]: hqp[field] for field in H_CHART_FIELDS})
    density = source["quotient_density"]
    L_H = density.subs(embedding, simultaneous=True)

    original_atoms = tuple(q.values()) + tuple(qp.values())
    constraint_atoms = (
        *source["schur_data"]["constraint_symbols"],
        *source["schur_data"]["constraint_jet_symbols"],
    )
    structural_checks = {
        "original_psi_absent": not L_H.has(q["psi"]),
        "original_psi_prime_absent": not L_H.has(qp["psi"]),
        "original_quotient_atoms_absent": not L_H.has(*original_atoms),
        "constraint_atoms_absent": not L_H.has(*constraint_atoms),
        "retained_chart_fields_represented": all(
            L_H.has(hq[field]) for field in H_CHART_FIELDS
        ),
    }
    if not all(structural_checks.values()):
        raise AssertionError(("quotient_density_structure", structural_checks))

    T_H = -q["psi"] / H
    D_T_H = -qp["psi"] / H + q["psi"] * z["Hp"] / H**2
    projected_q = {
        field: q[field] + R[field] * T_H for field in fields
    }
    projected_qp = {
        field: (
            qp[field]
            + generator["coefficient_time_derivatives"][field] * T_H
            + R[field] * D_T_H
        )
        for field in fields
    }

    x = tuple(q[field] for field in fields) + tuple(
        qp[field] for field in fields
    )
    y = chart_q_symbols + chart_qp_symbols
    projected_retained = tuple(projected_q[field] for field in H_CHART_FIELDS)
    projected_retained += tuple(projected_qp[field] for field in H_CHART_FIELDS)
    C_H = sp.Matrix(len(y), len(x), lambda i, j: sp.diff(
        projected_retained[i], x[j]
    ))
    E_H = sp.zeros(len(x), len(y))
    for i in range(len(H_CHART_FIELDS)):
        E_H[i + 1, i] = 1
        E_H[len(fields) + i + 1, len(H_CHART_FIELDS) + i] = 1
    P_H = E_H * C_H

    zero_configuration = {atom: sp.Integer(0) for atom in x}
    constant = density.subs(zero_configuration, simultaneous=True)
    linear = sp.Matrix([
        sp.diff(density, atom).subs(zero_configuration, simultaneous=True)
        for atom in x
    ])
    quadratic = sp.Matrix(len(x), len(x), lambda i, j: sp.diff(
        density, x[i], x[j]
    ).subs(zero_configuration, simultaneous=True))
    M_H = E_H.T * quadratic * E_H
    l_H = E_H.T * linear

    hqpp_symbols = sp.symbols(
        " ".join(f"h_{field}_double_prime" for field in H_CHART_FIELDS)
    )
    hqpp = dict(zip(H_CHART_FIELDS, hqpp_symbols))

    def D_eta_H(expression):
        chain = sp.Add(*(
            sp.diff(expression, hq[field]) * hqp[field]
            + sp.diff(expression, hqp[field]) * hqpp[field]
            for field in H_CHART_FIELDS
        ))
        return sp.Add(total._D_eta(expression), chain, evaluate=False)

    momenta = {
        field: sp.diff(L_H, hqp[field]) for field in H_CHART_FIELDS
    }
    euler_rows = {
        field: sp.Add(
            sp.diff(L_H, hq[field]),
            -D_eta_H(momenta[field]),
            evaluate=False,
        )
        for field in H_CHART_FIELDS
    }
    second_order = tuple(
        field for field in H_CHART_FIELDS
        if any(euler_rows[field].has(symbol) for symbol in hqpp_symbols)
    )
    auxiliary_fields = tuple(
        field for field in H_CHART_FIELDS
        if not L_H.has(hqp[field])
        and field in ("delta_J_b_L", "delta_J_r_L")
    )
    if second_order != ("delta_phi", "delta_theta"):
        raise AssertionError(("second_order_fields", second_order))
    if auxiliary_fields != ("delta_J_b_L", "delta_J_r_L"):
        raise AssertionError(("auxiliary_fields", auxiliary_fields))

    def canonical_block(order):
        return sp.Matrix(2, 2, lambda i, j: sp.diff(
            euler_rows[order[i]], hqp[order[j]]
        ))

    baryon_order = ("delta_J_b_0", "delta_ell_b")
    radiation_order = ("delta_J_r_0", "delta_ell_r")
    J_b = canonical_block(baryon_order)
    J_r = canonical_block(radiation_order)
    c_b, c_r = J_b[0, 1], J_r[0, 1]
    expected_b = sp.Matrix(((0, c_b), (-c_b, 0)))
    expected_r = sp.Matrix(((0, c_r), (-c_r, 0)))
    canonical_checks = (
        _matrix_residual(J_b.T, -J_b),
        _matrix_residual(J_b, expected_b),
        _zero_scalar(c_b**2 - 1),
        _zero_scalar(J_b.det() - 1),
        _matrix_residual(J_r.T, -J_r),
        _matrix_residual(J_r, expected_r),
        _zero_scalar(c_r**2 - 1),
        _zero_scalar(J_r.det() - 1),
    )
    if any(value != 0 for value in canonical_checks):
        raise AssertionError(("canonical_block", canonical_checks))
    if c_b != -1 or c_r != -1:
        raise AssertionError(("canonical_orientation", (c_b, c_r)))

    K_effective = auxiliary_data["structured_effective_kinetic"]
    P_phys = sp.diag(1, 1, 1, 1, 1, 1)
    for block, offset in ((K_effective, 0), (J_b, 2), (J_r, 4)):
        for i in range(2):
            for j in range(2):
                P_phys[offset + i, offset + j] = block[i, j]
    physical_det = actual_det * J_b.det() * J_r.det()

    schur = source["schur_data"]
    A_solution, B_solution = tuple(schur["solution"])
    A_H = A_solution.subs(embedding, simultaneous=True)
    B_H = B_solution.subs(embedding, simultaneous=True)
    B_H_prime = D_eta_H(B_H)
    definitions_H = bardeen.bardeen_weyl_definitions(
        lapse_potential=A_H,
        curvature_potential=sp.Integer(0),
        scalar_shift=B_H,
        spatial_shear_prime=sp.Integer(0),
        scalar_shear_prime=B_H_prime,
        conformal_hubble=H,
    )
    bardeen_potentials = (
        definitions_H.bardeen_lapse_potential,
        definitions_H.bardeen_curvature_potential,
    )
    W_H = definitions_H.weyl_potential_sum

    # Project the original E=0 expressions, then retract to the H chart.
    projection_sub = {}
    projection_sub.update({q[field]: projected_q[field] for field in fields})
    projection_sub.update({qp[field]: projected_qp[field] for field in fields})
    projected_A = A_solution.subs(projection_sub, simultaneous=True)
    projected_B = B_solution.subs(projection_sub, simultaneous=True)
    projected_B_prime = (
        quotient_euler.quotient_euler_data()["D_eta"](projected_B)
    )
    projected_defs = bardeen.bardeen_weyl_definitions(
        lapse_potential=projected_A,
        curvature_potential=projected_q["psi"],
        scalar_shift=projected_B,
        spatial_shear_prime=sp.Integer(0),
        scalar_shear_prime=projected_B_prime,
        conformal_hubble=H,
    )
    retract = dict(embedding)

    imported_rows = auxiliary_data["auxiliary_euler_rows"]
    imported_aux_order = tuple(imported_solution["order"])
    auxiliary_reconstruction = (
        imported_aux_order == auxiliary_fields
        and imported_solution["source"] == auxiliary_data["auxiliary_source"]
        and imported_solution["inverse"]
        == auxiliary_data["structured_auxiliary_inverse"]
        and imported_solution["solution"]
        == auxiliary_data["structured_auxiliary_solution"]
        and all(value == 0 for value in imported_solution[
            "solution_reconstruction_residuals"
        ])
        and len(imported_rows) == 2
        and _zero_scalar(imported_solution["determinant"]) != 0
        and not dict(auxiliary_data["unresolved_factors"])
    )

    original_euler = quotient_euler.quotient_euler_data()["euler_rows"]
    euler_pullback_residuals = (
        euler_rows[field]
        - original_euler[field].subs({
            **embedding,
            **{
                quotient_euler.quotient_euler_data()["qpp"][name]:
                    (sp.Integer(0) if name == "psi" else hqpp[name])
                for name in fields
            },
        }, simultaneous=True)
        for field in H_CHART_FIELDS
    )

    configuration_condition = _zero_scalar(projected_q["psi"])
    jet_condition = _zero_scalar(projected_qp["psi"])
    retraction_residual = _first_nonzero(
        projected_retained[i].subs(embedding, simultaneous=True) - y[i]
        for i in range(len(y))
    )
    orbit_parameter = generator["time_parameter"]
    orbit_parameter_prime = generator["time_parameter_prime"]
    orbit_sub = {
        q[field]: q[field] + R[field] * orbit_parameter for field in fields
    }
    orbit_sub.update({
        qp[field]: (
            qp[field]
            + generator["coefficient_time_derivatives"][field] * orbit_parameter
            + R[field] * orbit_parameter_prime
        )
        for field in fields
    })
    orbit_residual = _first_nonzero(
        projected_retained[i].subs(orbit_sub, simultaneous=True)
        - projected_retained[i]
        for i in range(len(y))
    )

    residuals = {
        "h_chart_configuration_condition": configuration_condition,
        "h_chart_jet_condition": jet_condition,
        "h_chart_retraction_identity": retraction_residual,
        "h_chart_projection_idempotence": _matrix_residual(P_H * P_H, P_H),
        "h_chart_orbit_annihilation": orbit_residual,
        "quadratic_projection_reconstruction": _matrix_residual(
            P_H.T * quadratic * P_H, C_H.T * M_H * C_H
        ),
        "linear_projection_reconstruction": _matrix_residual(
            P_H.T * linear, C_H.T * l_H
        ),
        "quotient_density_pullback": _zero_scalar(
            L_H - density.subs(embedding, simultaneous=True)
        ),
        "quotient_euler_reconstruction": _first_nonzero(
            euler_pullback_residuals
        ),
        "baryon_canonical_block": _first_nonzero(canonical_checks[:4]),
        "radiation_canonical_block": _first_nonzero(canonical_checks[4:]),
        "auxiliary_solution_reconstruction": (
            sp.Integer(0) if auxiliary_reconstruction else sp.Integer(1)
        ),
        "physical_principal_determinant": _zero_scalar(
            physical_det - expected_det
        ),
        "weyl_reconstruction": _first_nonzero((
            projected_defs.bardeen_lapse_potential.subs(
                retract, simultaneous=True
            ) - bardeen_potentials[0],
            projected_defs.bardeen_curvature_potential.subs(
                retract, simultaneous=True
            ) - bardeen_potentials[1],
            projected_defs.weyl_potential_sum.subs(
                retract, simultaneous=True
            ) - W_H,
        )),
    }

    canonical_pairings = (
        ("delta_J_b_0", "delta_ell_b", c_b),
        ("delta_J_r_0", "delta_ell_r", c_r),
    )
    data = {
        "spatial_quotient_field_order": fields,
        "h_chart_field_order": H_CHART_FIELDS,
        "independent_chart_symbols": _immutable_mapping(hq),
        "independent_chart_jet_symbols": _immutable_mapping(hqp),
        "embedding_substitution": _immutable_mapping(embedding),
        "chart_projection": _immutable_mapping({
            "configuration": _immutable_mapping(projected_q),
            "first_jets": _immutable_mapping(projected_qp),
            "shift": T_H,
            "embedding_matrix": E_H,
            "projection_matrix": C_H,
            "projector": P_H,
        }),
        "quotient_density": L_H,
        "quotient_euler_rows": _immutable_mapping(euler_rows),
        "second_order_fields": second_order,
        "canonical_pairings": canonical_pairings,
        "canonical_orientation_coefficients": _immutable_mapping({
            "baryon": c_b, "radiation": c_r,
        }),
        "baryon_canonical_block": J_b,
        "radiation_canonical_block": J_r,
        "auxiliary_fields": auxiliary_fields,
        "imported_auxiliary_solution": imported_solution,
        "physical_state_order": PHYSICAL_STATE_ORDER,
        "physical_principal_matrix": P_phys,
        "physical_principal_determinant": physical_det,
        "bardeen_potentials": bardeen_potentials,
        "weyl_observable": W_H,
        "prepared_domain": _immutable_mapping({
            "global_chart": "psi=0",
            "chart_denominator": H,
            "H_floor": "H>=H_floor>0",
            "rho_b0": "rho_b0>0",
            "rho_r0": "rho_r0>0",
            "strict_principal_factors": ("a>0", "alpha>0", "beta>0", "phi_bar>0"),
        }),
        "structural_checks": _immutable_mapping(structural_checks),
        "unresolved_factors": auxiliary_data["unresolved_factors"],
        "_constant_coefficient": constant,
        "_linear_vector": linear,
        "_quadratic_matrix": quadratic,
        "_certificate": _immutable_mapping(residuals),
    }
    return _immutable_mapping(data)


def exact_scalar_prepared_time_gauge_quotient_certificate():
    """Return exactly the fourteen scalar, fraction-free residuals."""
    residuals = _construction()["_certificate"]
    return _immutable_mapping({key: residuals[key] for key in CERTIFICATE_KEYS})


def scalar_prepared_time_gauge_quotient_action():
    """Return the immutable H-chart action construction."""
    data = _construction()
    return _immutable_mapping({
        key: value for key, value in data.items() if not key.startswith("_")
    })


def scalar_prepared_physical_principal_system():
    """Return the immutable six-state physical principal system."""
    data = _construction()
    return _immutable_mapping({
        "physical_state_order": data["physical_state_order"],
        "physical_principal_matrix": data["physical_principal_matrix"],
        "physical_principal_determinant":
            data["physical_principal_determinant"],
        "strictly_positive": True,
        "strict_positive_factors":
            data["prepared_domain"]["strict_principal_factors"],
        "independent_determinant_assumption": False,
    })


def scalar_prepared_time_gauge_quotient_theorem():
    """Return the immutable theorem statement and its explicit limitations."""
    residuals = exact_scalar_prepared_time_gauge_quotient_certificate()
    if tuple(residuals) != CERTIFICATE_KEYS:
        raise AssertionError("time-gauge quotient certificate keys changed")
    if not all(value == 0 for value in residuals.values()):
        first = next((key, value) for key, value in residuals.items() if value != 0)
        raise AssertionError(("time-gauge quotient certificate", first))
    data = _construction()
    return _immutable_mapping({
        "global_prepared_chart": "psi=0",
        "chart_denominator": total._symbols()["H"],
        "positive_visible_density_restriction":
            ("rho_b0>0", "rho_r0>0"),
        "longitudinal_currents_exactly_eliminable": True,
        "canonical_blocks_nonsingular": True,
        "canonical_orientation_derived_from_action": True,
        "canonical_pairings": data["canonical_pairings"],
        "physical_principal_determinant":
            data["physical_principal_determinant"],
        "physical_principal_determinant_strictly_positive": True,
        "independent_determinant_assumption": False,
        "limitations": (
            "Zero-density boundary charts are not constructed.",
            "The alpha->0 Weyl limit is not classified.",
            "No nonzero Weyl defect is proved.",
            "No full Lambda-CDM-manifold separation is proved.",
            "No perturbation evolution was integrated.",
            "This is reduction infrastructure, not yet a measurable prediction.",
        ),
    })
