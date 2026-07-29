"""Exact first-jet elimination of the longitudinal visible currents.

The two algebraic auxiliary Euler equations are differentiated implicitly.
In particular, the already-expanded auxiliary solution is never passed to
``total._D_eta``.
"""

from __future__ import annotations

from functools import lru_cache
from types import MappingProxyType

import sympy as sp

from . import prepared_positive_visible_density_subfamily_v1 as positive
from . import scalar_prepared_auxiliary_elimination_v1 as auxiliary
from . import scalar_prepared_lapse_shift_determinant_v1 as determinant
from . import scalar_prepared_time_gauge_quotient_action_v1 as time_quotient
from . import scalar_spatial_gauge_quotient_v1 as spatial_quotient
from . import total_scalar_lapse_shift_hessian_v1 as total


CERTIFICATE_KEYS = (
    "imported_auxiliary_solution",
    "background_generator_derivative_equivalence",
    "h_chart_generator_derivative_equivalence",
    "auxiliary_derivative_jet_stratification",
    "implicit_auxiliary_derivative_identity",
    "structured_auxiliary_first_jet_solution",
    "differentiated_auxiliary_reconstruction",
)

SECOND_ORDER_FIELDS = ("delta_phi", "delta_theta")
AUXILIARY_FIELDS = ("delta_J_b_L", "delta_J_r_L")
CANONICAL_FIELDS = (
    "delta_J_b_0",
    "delta_ell_b",
    "delta_J_r_0",
    "delta_ell_r",
)


def _zero_scalar(expression):
    """Apply the prescribed numerator-only check to one scalar residual."""
    numerator = sp.together(expression).as_numer_denom()[0]
    return sp.expand(numerator)


def _first_scalar_residual(expressions):
    for expression in expressions:
        residual = _zero_scalar(expression)
        if residual != 0:
            return residual
    return sp.Integer(0)


def _immutable(mapping):
    return MappingProxyType(dict(mapping))


@lru_cache(maxsize=1)
def _construction():
    # Authoritative imported audits.
    quotient_certificate = (
        time_quotient.exact_scalar_prepared_time_gauge_quotient_certificate()
    )
    if len(quotient_certificate) != 14:
        raise AssertionError(("quotient_certificate_count", len(quotient_certificate)))
    for key, residual in quotient_certificate.items():
        if residual != 0:
            raise AssertionError((key, residual))

    chart = time_quotient.scalar_prepared_time_gauge_quotient_action()
    auxiliary_data = auxiliary.scalar_prepared_auxiliary_elimination_data()
    auxiliary_solution = auxiliary.scalar_prepared_auxiliary_solution()
    solution_certificate = (
        auxiliary.exact_scalar_prepared_auxiliary_solution_certificate()
    )
    # These imports are part of the validated public dependency surface.
    determinant.scalar_prepared_lapse_shift_determinant_data()
    positive.prepared_positive_visible_density_subfamily_data()

    if tuple(chart["second_order_fields"]) != SECOND_ORDER_FIELDS:
        raise AssertionError(
            ("second_order_fields", tuple(chart["second_order_fields"]))
        )
    if tuple(chart["auxiliary_fields"]) != AUXILIARY_FIELDS:
        raise AssertionError(("auxiliary_fields", tuple(chart["auxiliary_fields"])))
    if tuple(auxiliary_data["auxiliary_order"]) != AUXILIARY_FIELDS:
        raise AssertionError(
            ("auxiliary_order", tuple(auxiliary_data["auxiliary_order"]))
        )
    if tuple(auxiliary_solution["order"]) != AUXILIARY_FIELDS:
        raise AssertionError(
            ("solution_auxiliary_order", tuple(auxiliary_solution["order"]))
        )
    if solution_certificate["auxiliary_gradient_affine_reconstruction"] != 0:
        raise AssertionError(
            (
                "auxiliary_gradient_affine_reconstruction",
                solution_certificate["auxiliary_gradient_affine_reconstruction"],
            )
        )
    for key, residual in solution_certificate.items():
        if residual != 0:
            raise AssertionError((key, residual))

    z = total._symbols()
    expected_determinant = (
        z["a"] ** 4 * z["alpha"] * z["beta"] * z["ph"] ** 2
    )
    effective_determinant = auxiliary_data["prepared_scalar_factors"][
        "det_K_effective"
    ]
    determinant_residual = _zero_scalar(
        effective_determinant - expected_determinant
    )
    if determinant_residual != 0:
        raise AssertionError(("effective_kinetic_determinant", determinant_residual))
    if auxiliary_data["_checks"]["auxiliary_inverse_reconstruction"] != 0:
        raise AssertionError(
            (
                "auxiliary_inverse_reconstruction",
                auxiliary_data["_checks"]["auxiliary_inverse_reconstruction"],
            )
        )
    if dict(auxiliary_data["unresolved_factors"]):
        raise AssertionError(
            ("unresolved_factors", auxiliary_data["unresolved_factors"])
        )

    spatial = spatial_quotient.scalar_spatial_gauge_quotient()
    q = spatial["quotient_symbols"]
    qp = spatial["quotient_jet_symbols"]
    hq = chart["independent_chart_symbols"]
    hqp = chart["independent_chart_jet_symbols"]
    h_chart_field_order = tuple(chart["h_chart_field_order"])
    translation = {
        q["psi"]: sp.Integer(0),
        qp["psi"]: sp.Integer(0),
    }
    translation.update({q[field]: hq[field] for field in h_chart_field_order})
    translation.update({qp[field]: hqp[field] for field in h_chart_field_order})

    A_H = auxiliary_data["A"].subs(translation, simultaneous=True)
    A_inverse_H = auxiliary_data["structured_auxiliary_inverse"].subs(
        translation, simultaneous=True
    )
    j_H = auxiliary_data["auxiliary_source"].subs(
        translation, simultaneous=True
    )
    x_solution_H = auxiliary_data["structured_auxiliary_solution"].subs(
        translation, simultaneous=True
    )
    delta_A_H = auxiliary_data["delta_A"].subs(
        translation, simultaneous=True
    )

    imported_inverse_source = _first_scalar_residual(
        delta_A_H
        * (x_solution_H + A_inverse_H * j_H)[i, 0]
        for i in range(2)
    )
    if imported_inverse_source != 0:
        raise AssertionError(
            ("imported_auxiliary_solution", imported_inverse_source)
        )
    imported_reconstruction = _first_scalar_residual(
        delta_A_H * (A_H * x_solution_H + j_H)[i, 0]
        for i in range(2)
    )
    if imported_reconstruction != 0:
        raise AssertionError(
            ("imported_auxiliary_reconstruction", imported_reconstruction)
        )

    # Recover only the two perturbation acceleration symbols already present
    # in the quotient Euler rows.
    hqpp = {}
    for field in SECOND_ORDER_FIELDS:
        name = f"h_{field}_double_prime"
        matches = tuple(
            symbol
            for symbol in chart["quotient_euler_rows"][field].free_symbols
            if symbol.name == name
        )
        if len(matches) != 1:
            raise AssertionError(("scalar_double_prime_symbol", field, matches))
        hqpp[field] = matches[0]
    scalar_double_primes = tuple(hqpp[field] for field in SECOND_ORDER_FIELDS)

    forbidden_input_jets = tuple(hqp[field] for field in (
        *AUXILIARY_FIELDS,
        *CANONICAL_FIELDS,
    ))
    if A_H.has(*scalar_double_primes) or j_H.has(*scalar_double_primes):
        raise AssertionError(("input_double_prime_dependence",))
    if A_H.has(*forbidden_input_jets) or j_H.has(*forbidden_input_jets):
        raise AssertionError(("input_forbidden_first_jet_dependence",))
    allowed_source_jets = tuple(hqp[field] for field in SECOND_ORDER_FIELDS)
    chart_jets = tuple(hqp[field] for field in h_chart_field_order)
    unexpected_source_jets = tuple(
        jet for jet in chart_jets
        if j_H.has(jet) and jet not in allowed_source_jets
    )
    if unexpected_source_jets:
        raise AssertionError(
            ("auxiliary_source_jet_stratification", unexpected_source_jets)
        )

    background_symbols = tuple(dict.fromkeys(
        value for value in z.values() if isinstance(value, sp.Symbol)
    ))
    background_generator_derivatives = _immutable({
        symbol: total._D_eta(symbol) for symbol in background_symbols
    })

    def D_background_sparse(expression):
        terms = tuple(
            sp.Mul(
                sp.diff(expression, symbol),
                background_generator_derivatives[symbol],
                evaluate=False,
            )
            for symbol in background_symbols
            if symbol in expression.free_symbols
        )
        return (
            sp.Add(*terms, evaluate=False)
            if terms else sp.Integer(0)
        )

    generator_residual = _first_scalar_residual(
        D_background_sparse(symbol) - total._D_eta(symbol)
        for symbol in background_symbols
    )
    if generator_residual != 0:
        raise AssertionError(
            ("background_generator_derivative_equivalence", generator_residual)
        )

    def D_eta_H_sparse(expression):
        configuration_terms = tuple(
            sp.Mul(
                sp.diff(expression, hq[field]),
                hqp[field],
                evaluate=False,
            )
            for field in h_chart_field_order
            if hq[field] in expression.free_symbols
        )
        second_order_terms = tuple(
            sp.Mul(
                sp.diff(expression, hqp[field]),
                hqpp[field],
                evaluate=False,
            )
            for field in SECOND_ORDER_FIELDS
            if hqp[field] in expression.free_symbols
        )
        return sp.Add(
            D_background_sparse(expression),
            *configuration_terms,
            *second_order_terms,
            evaluate=False,
        )

    chart_generator_residual = _first_scalar_residual((
        *(
            D_eta_H_sparse(hq[field]) - hqp[field]
            for field in h_chart_field_order
        ),
        *(
            D_eta_H_sparse(hqp[field]) - hqpp[field]
            for field in SECOND_ORDER_FIELDS
        ),
    ))
    if chart_generator_residual != 0:
        raise AssertionError(
            ("h_chart_generator_derivative_equivalence", chart_generator_residual)
        )

    D_A = sp.Matrix(2, 2, lambda i, j: D_eta_H_sparse(A_H[i, j]))
    D_j = sp.Matrix(2, 1, lambda i, _: D_eta_H_sparse(j_H[i, 0]))
    implicit_rhs = D_A * x_solution_H + D_j
    x_aux_prime_solution = -A_inverse_H * implicit_rhs

    inverse_residual = sp.Matrix(2, 2, lambda i, j:
        _zero_scalar(
            delta_A_H * (A_H * A_inverse_H - sp.eye(2))[i, j]
        )
    )
    for i in range(2):
        for j in range(2):
            if inverse_residual[i, j] != 0:
                raise AssertionError(
                    ("auxiliary_inverse_identity", (i, j), inverse_residual[i, j])
                )

    # Composition uses the proven zero inverse residual, without expanding the
    # full differentiated solution.
    reconstruction_rows = tuple(
        -sum(
            inverse_residual[i, j] * implicit_rhs[j, 0]
            for j in range(2)
        )
        for i in range(2)
    )
    differentiated_reconstruction = _first_scalar_residual(
        reconstruction_rows
    )
    if differentiated_reconstruction != 0:
        raise AssertionError(
            ("differentiated_auxiliary_reconstruction",
             differentiated_reconstruction)
        )

    canonical_prime_symbols = tuple(hqp[field] for field in CANONICAL_FIELDS)
    all_symbols = x_aux_prime_solution.free_symbols
    perturbation_double_primes = tuple(
        symbol for symbol in all_symbols
        if symbol.name.startswith("h_")
        and symbol.name.endswith("_double_prime")
    )
    unexpected_double_primes = tuple(
        symbol for symbol in perturbation_double_primes
        if symbol not in scalar_double_primes
    )
    auxiliary_prime_symbols = tuple(hqp[field] for field in AUXILIARY_FIELDS)
    unexpected_canonical_primes = tuple(
        symbol for symbol in canonical_prime_symbols
        if symbol not in all_symbols
    )
    if unexpected_double_primes:
        raise AssertionError(
            ("unexpected_perturbation_double_prime", unexpected_double_primes)
        )
    if x_aux_prime_solution.has(*auxiliary_prime_symbols):
        raise AssertionError(
            ("unexpected_auxiliary_first_jet", auxiliary_prime_symbols)
        )
    if unexpected_canonical_primes:
        raise AssertionError(
            ("missing_canonical_first_jet", unexpected_canonical_primes)
        )

    Q_double_prime = sp.Matrix(scalar_double_primes)
    U_canonical_prime = sp.Matrix(canonical_prime_symbols)
    state_fields = tuple(chart["physical_state_order"])
    state_symbols = tuple(hq[field] for field in state_fields) + tuple(
        hqp[field] for field in SECOND_ORDER_FIELDS
    )
    X_H = sp.Matrix(state_symbols)
    C_acceleration = x_aux_prime_solution.jacobian(Q_double_prime)
    C_canonical = x_aux_prime_solution.jacobian(U_canonical_prime)
    C_state = x_aux_prime_solution.jacobian(X_H)
    affine_offset = x_aux_prime_solution.subs(
        {
            symbol: sp.Integer(0)
            for symbol in (
                *scalar_double_primes,
                *canonical_prime_symbols,
                *state_symbols,
            )
        },
        simultaneous=True,
    )
    if not affine_offset.is_zero_matrix:
        raise AssertionError(("affine_offset", affine_offset))
    coefficient_reconstruction = (
        C_acceleration * Q_double_prime
        + C_canonical * U_canonical_prime
        + C_state * X_H
        + affine_offset
    )
    structured_solution_residual = _first_scalar_residual(
        x_aux_prime_solution[i, 0] - coefficient_reconstruction[i, 0]
        for i in range(2)
    )
    if structured_solution_residual != 0:
        raise AssertionError(
            ("structured_auxiliary_first_jet_solution",
             structured_solution_residual)
        )

    structural_checks = _immutable({
        "fourteen_quotient_residuals": len(quotient_certificate) == 14,
        "auxiliary_order_agrees": tuple(auxiliary_solution["order"])
            == AUXILIARY_FIELDS,
        "raw_inverse_identity": inverse_residual.is_zero_matrix,
        "input_jet_stratification": not unexpected_source_jets,
        "only_scalar_accelerations": not unexpected_double_primes,
        "all_canonical_first_jets_present": not unexpected_canonical_primes,
        "no_auxiliary_first_jets": not x_aux_prime_solution.has(
            *auxiliary_prime_symbols
        ),
        "zero_affine_offset": affine_offset.is_zero_matrix,
    })
    certificates = _immutable({
        "imported_auxiliary_solution": sp.Integer(0),
        "background_generator_derivative_equivalence": generator_residual,
        "h_chart_generator_derivative_equivalence": chart_generator_residual,
        "auxiliary_derivative_jet_stratification": sp.Integer(0),
        "implicit_auxiliary_derivative_identity": sp.Integer(0),
        "structured_auxiliary_first_jet_solution":
            structured_solution_residual,
        "differentiated_auxiliary_reconstruction":
            differentiated_reconstruction,
    })
    data = _immutable({
        "auxiliary_order": AUXILIARY_FIELDS,
        "second_order_fields": SECOND_ORDER_FIELDS,
        "canonical_fields": CANONICAL_FIELDS,
        "scalar_double_prime_symbols": scalar_double_primes,
        "canonical_prime_symbols": canonical_prime_symbols,
        "background_generator_derivatives":
            background_generator_derivatives,
        "auxiliary_matrix": A_H,
        "auxiliary_inverse": A_inverse_H,
        "auxiliary_source": j_H,
        "auxiliary_solution": x_solution_H,
        "auxiliary_matrix_derivative": D_A,
        "auxiliary_source_derivative": D_j,
        "implicit_derivative_rhs": implicit_rhs,
        "auxiliary_first_jet_solution": x_aux_prime_solution,
        "acceleration_coefficient_matrix": C_acceleration,
        "canonical_prime_coefficient_matrix": C_canonical,
        "state_coefficient_matrix": C_state,
        "state_symbols": state_symbols,
        "affine_offset": affine_offset,
        "structural_checks": structural_checks,
        "unresolved_factors": auxiliary_data["unresolved_factors"],
        "_certificate": certificates,
    })
    return data


@lru_cache(maxsize=1)
def exact_scalar_prepared_auxiliary_first_jet_certificate():
    """Return exactly the seven exact first-jet residuals."""
    certificate = _construction()["_certificate"]
    return _immutable({key: certificate[key] for key in CERTIFICATE_KEYS})


@lru_cache(maxsize=1)
def scalar_prepared_auxiliary_first_jet_data():
    """Return the immutable implicit first-jet elimination data."""
    return _immutable({
        key: value for key, value in _construction().items()
        if not key.startswith("_")
    })


def scalar_prepared_auxiliary_first_jet_theorem():
    """Return the exact result and the deliberately narrow boundary."""
    certificate = exact_scalar_prepared_auxiliary_first_jet_certificate()
    if tuple(certificate) != CERTIFICATE_KEYS:
        raise AssertionError("auxiliary first-jet certificate keys changed")
    if not all(value == 0 for value in certificate.values()):
        first = next(
            (key, value) for key, value in certificate.items() if value != 0
        )
        raise AssertionError(("auxiliary first-jet certificate", first))
    return _immutable({
        "claims": (
            "The two algebraic longitudinal-current equations possess an "
            "exact differentiated first-jet solution on the positive-density "
            "prepared domain.",
            "The result is obtained by implicit differentiation.",
            "No differentiation of the expanded inverse-source solution is "
            "required.",
            "The result uses the existing exact auxiliary inverse.",
            "The first-jet solution contains no auxiliary or canonical "
            "double-primes.",
            "No numerical integration is used.",
        ),
        "limitations": (
            "The complete fixed-k evolution operator is not yet constructed.",
            "The alpha->0 limit is not classified.",
            "No state rescaling is constructed.",
            "No nonzero Weyl defect is proved.",
            "No Lambda-CDM-manifold separation is proved.",
        ),
    })
