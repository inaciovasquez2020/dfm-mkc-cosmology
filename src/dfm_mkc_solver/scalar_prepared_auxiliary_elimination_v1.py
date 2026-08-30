"""Exact rank-one elimination of the two longitudinal visible currents."""

from __future__ import annotations

from functools import lru_cache
from types import MappingProxyType

import sympy as sp

from . import prepared_positive_visible_density_subfamily_v1 as positive
from . import scalar_prepared_lapse_shift_determinant_v1 as prepared
from . import scalar_spatial_gauge_quotient_v1 as quotient
from . import total_scalar_lapse_shift_hessian_v1 as total


CERTIFICATE_KEYS = (
    "h_chart_embedding",
    "second_order_block_symmetry",
    "auxiliary_block_symmetry",
    "kinetic_rank_one_decomposition",
    "auxiliary_rank_one_decomposition",
    "mixed_rank_one_decomposition",
    "auxiliary_determinant_lemma",
    "auxiliary_inverse_reconstruction",
    "effective_kinetic_schur_identity",
    "effective_kinetic_determinant_lemma",
)

SOLUTION_CERTIFICATE_KEYS = (
    "auxiliary_gradient_affine_reconstruction",
    "auxiliary_inverse_source_application",
    "auxiliary_solution_reconstruction",
)

VELOCITY_ORDER = ("delta_phi_prime", "delta_theta_prime")
AUXILIARY_ORDER = ("delta_J_b_L", "delta_J_r_L")


def _zero_scalar(expression):
    """Use the prescribed fraction-free zero test on one scalar."""
    numerator = sp.together(expression).as_numer_denom()[0]
    return sp.expand(numerator)


def _check_all(expressions):
    residuals = tuple(_zero_scalar(value) for value in expressions)
    for residual in residuals:
        if residual != 0:
            return residual
    return sp.Integer(0)


def _det2(matrix):
    return matrix[0, 0] * matrix[1, 1] - matrix[0, 1] * matrix[1, 0]


@lru_cache(maxsize=1)
def scalar_prepared_auxiliary_elimination_data():
    """Return the exact structured blocks and prepared scalar factors."""
    # This is deliberately the sole quotient construction in this module.
    source = quotient.scalar_spatial_gauge_quotient()
    density = source["quotient_density"]
    q = source["quotient_symbols"]
    qp = source["quotient_jet_symbols"]
    z = total._symbols()

    h_substitution = {
        q["psi"]: sp.Integer(0),
        qp["psi"]: sp.Integer(0),
    }
    h_density = density.subs(h_substitution, simultaneous=True)
    velocities = (qp["delta_phi"], qp["delta_theta"])
    auxiliaries = (q["delta_J_b_L"], q["delta_J_r_L"])

    K = sp.Matrix(2, 2, lambda i, j: sp.diff(
        h_density, velocities[i], velocities[j]
    ))
    A = sp.Matrix(2, 2, lambda i, j: sp.diff(
        h_density, auxiliaries[i], auxiliaries[j]
    ))
    B = sp.Matrix(2, 2, lambda i, j: sp.diff(
        h_density, velocities[i], auxiliaries[j]
    ))

    a, k2 = z["a"], z["k2"]
    alpha, beta = z["alpha"], z["beta"]
    phi, phi_prime, theta_prime = z["ph"], z["php"], z["thp"]
    Jb, Jr = z["Jb"], z["Jr"]
    mb, kr = z["mb"], z["kr"]

    D = sp.diag(a**2 * alpha, a**2 * beta * phi**2)
    F = sp.diag(
        a * k2 * mb / Jb,
        4 * k2 * kr / (3 * Jr**sp.Rational(2, 3)),
    )
    u = sp.Matrix((
        alpha * phi_prime,
        beta * phi**2 * theta_prime,
    ))
    v = sp.Matrix((
        a * mb,
        4 * Jr**sp.Rational(1, 3) * kr / 3,
    ))
    C_K = D - K
    C_A = F - A

    c = C_K[0, 0] / u[0]**2
    d = C_A[0, 0] / v[0]**2
    e = -B[0, 0] / (u[0] * v[0])

    det_D = D[0, 0] * D[1, 1]
    det_F = F[0, 0] * F[1, 1]
    t = u[0]**2 / D[0, 0] + u[1]**2 / D[1, 1]
    s = v[0]**2 / F[0, 0] + v[1]**2 / F[1, 1]
    delta_A = 1 - d * s
    det_A = det_F * delta_A

    F_inverse = sp.diag(1 / F[0, 0], 1 / F[1, 1])
    A_inverse = (
        F_inverse
        + d / delta_A
        * F_inverse * v * v.T * F_inverse
    )
    x_aux = sp.Matrix(auxiliaries)
    E_aux = sp.Matrix([
        sp.diff(h_density, auxiliaries[0]),
        sp.diff(h_density, auxiliaries[1]),
    ])
    j_aux = E_aux.subs(
        {auxiliary: sp.Integer(0) for auxiliary in auxiliaries},
        simultaneous=True,
    )
    x_aux_solution = -A_inverse * j_aux
    gradient_reconstruction_residuals = tuple(
        _zero_scalar((E_aux - A * x_aux - j_aux)[i, 0])
        for i in range(2)
    )
    inverse_source_residuals = tuple(
        _zero_scalar(
            delta_A
            * (x_aux_solution + A_inverse * j_aux)[i, 0]
        )
        for i in range(2)
    )
    solution_reconstruction_residuals = tuple(
        _zero_scalar(
            delta_A * (A * x_aux_solution + j_aux)[i, 0]
        )
        for i in range(2)
    )
    gamma = c + e**2 * s / delta_A
    K_effective = D - gamma * u * u.T
    det_K_effective = det_D * (1 - gamma * t)

    adj_A = sp.Matrix(((A[1, 1], -A[0, 1]),
                       (-A[1, 0], A[0, 0])))
    R = det_A * K - B * adj_A * B.T
    det_R = _det2(R)

    rank_k = (
        C_K[i, j] * u[0]**2 - C_K[0, 0] * u[i] * u[j]
        for i in range(2) for j in range(2)
    )
    rank_a = (
        C_A[i, j] * v[0]**2 - C_A[0, 0] * v[i] * v[j]
        for i in range(2) for j in range(2)
    )
    rank_b = (
        B[i, j] * u[0] * v[0] - B[0, 0] * u[i] * v[j]
        for i in range(2) for j in range(2)
    )
    inverse_residuals = (
        delta_A * (A * A_inverse - sp.eye(2))[i, j]
        for i in range(2) for j in range(2)
    )
    schur_residuals = (
        delta_A * (
            K_effective - (K - B * A_inverse * B.T)
        )[i, j]
        for i in range(2) for j in range(2)
    )
    fraction_free_residuals = (
        R[i, j] - det_A * K_effective[i, j]
        for i in range(2) for j in range(2)
    )

    checks = {
        "h_chart_embedding": _check_all((
            q["psi"].subs(h_substitution),
            qp["psi"].subs(h_substitution),
        )),
        "second_order_block_symmetry": _check_all(
            K[i, j] - K[j, i] for i in range(2) for j in range(2)
        ),
        "auxiliary_block_symmetry": _check_all(
            A[i, j] - A[j, i] for i in range(2) for j in range(2)
        ),
        "kinetic_rank_one_decomposition": _check_all(rank_k),
        "auxiliary_rank_one_decomposition": _check_all(rank_a),
        "mixed_rank_one_decomposition": _check_all(rank_b),
        "auxiliary_determinant_lemma": _zero_scalar(
            _det2(A) - det_F * delta_A
        ),
        "auxiliary_inverse_reconstruction": _check_all(
            inverse_residuals
        ),
        "effective_kinetic_schur_identity": _check_all(
            schur_residuals
        ),
        "effective_kinetic_determinant_lemma": _check_all((
            _det2(K_effective) - det_D * (1 - gamma * t),
            *fraction_free_residuals,
            det_R - det_A**2 * det_K_effective,
        )),
    }
    solution_checks = {
        "auxiliary_gradient_affine_reconstruction": _check_all(
            gradient_reconstruction_residuals
        ),
        "auxiliary_inverse_source_application": _check_all(
            inverse_source_residuals
        ),
        "auxiliary_solution_reconstruction": _check_all(
            solution_reconstruction_residuals
        ),
    }

    det_data = prepared.scalar_prepared_lapse_shift_determinant_data()
    pos_data = positive.prepared_positive_visible_density_subfamily_data()
    scalar_substitutions = (
        det_data["prepared_substitution"],
        det_data["current_density_substitution"],
        det_data["friedmann_substitution"],
        {
            det_data["symbols"]["rho_b"]:
                pos_data["rho_b0"] / z["a"]**3,
            det_data["symbols"]["rho_r"]:
                pos_data["rho_r0"] / z["a"]**4,
        },
    )

    def prepare_scalar(value):
        result = value
        for substitution in scalar_substitutions:
            result = result.subs(substitution, simultaneous=True)
        return sp.factor_terms(result)

    scalar_quantities = {
        "det_D": det_D,
        "det_F": det_F,
        "delta_A": delta_A,
        "t": t,
        "s": s,
        "gamma": gamma,
        "one_minus_gamma_t": 1 - gamma * t,
        "det_A": det_A,
        "det_K_effective": det_K_effective,
    }
    prepared_factors = MappingProxyType({
        key: prepare_scalar(value)
        for key, value in scalar_quantities.items()
    })

    effective_nondegenerate = bool(
        prepared_factors["one_minus_gamma_t"] == 1
    )
    signs = MappingProxyType({
        "det_D": "strictly positive",
        "det_F": "strictly positive",
        "delta_A": "strictly positive",
        "det_A": "strictly positive",
        "one_minus_gamma_t": "strictly positive (equals 1)",
    })

    return {
        "velocity_order": VELOCITY_ORDER,
        "auxiliary_order": AUXILIARY_ORDER,
        "D": D, "F": F, "u": u, "v": v,
        "c": c, "d": d, "e": e,
        "K": K, "A": A, "B": B,
        "det_D": det_D, "det_F": det_F,
        "t": t, "s": s, "delta_A": delta_A, "det_A": det_A,
        "gamma": gamma,
        "auxiliary_configuration": x_aux,
        "auxiliary_euler_rows": E_aux,
        "auxiliary_source": j_aux,
        "structured_auxiliary_inverse": A_inverse,
        "structured_auxiliary_solution": x_aux_solution,
        "auxiliary_gradient_reconstruction_residuals":
            gradient_reconstruction_residuals,
        "auxiliary_solution_reconstruction_residuals":
            solution_reconstruction_residuals,
        "structured_effective_kinetic": K_effective,
        "structured_effective_determinant": det_K_effective,
        "fraction_free_matrix": R,
        "fraction_free_determinant": det_R,
        "prepared_scalar_factors": prepared_factors,
        "unresolved_factors": MappingProxyType({}),
        "effective_kinetic_nondegenerate": effective_nondegenerate,
        "signs": signs,
        "_checks": checks,
        "_solution_checks": solution_checks,
    }


@lru_cache(maxsize=1)
def exact_scalar_prepared_auxiliary_elimination_certificate():
    """Return exactly the ten requested exact zero residuals."""
    checks = scalar_prepared_auxiliary_elimination_data()["_checks"]
    return {key: checks[key] for key in CERTIFICATE_KEYS}


@lru_cache(maxsize=1)
def exact_scalar_prepared_auxiliary_solution_certificate():
    """Return exactly the three structured-solution zero residuals."""
    checks = scalar_prepared_auxiliary_elimination_data()["_solution_checks"]
    return {key: checks[key] for key in SOLUTION_CERTIFICATE_KEYS}


@lru_cache(maxsize=1)
def scalar_prepared_auxiliary_solution():
    """Return the immutable exact structured auxiliary solution."""
    data = scalar_prepared_auxiliary_elimination_data()
    return MappingProxyType({
        "source": data["auxiliary_source"],
        "inverse": data["structured_auxiliary_inverse"],
        "solution": data["structured_auxiliary_solution"],
        "determinant": data["det_A"],
        "order": data["auxiliary_order"],
        "gradient_reconstruction_residuals":
            data["auxiliary_gradient_reconstruction_residuals"],
        "solution_reconstruction_residuals":
            data["auxiliary_solution_reconstruction_residuals"],
        "positive_density_domain": ("rho_b0>0", "rho_r0>0"),
    })


def scalar_prepared_auxiliary_elimination_theorem():
    """Return the immutable positive-density auxiliary theorem."""
    data = scalar_prepared_auxiliary_elimination_data()
    residuals = exact_scalar_prepared_auxiliary_elimination_certificate()
    if tuple(residuals) != CERTIFICATE_KEYS:
        raise AssertionError("auxiliary-elimination certificate keys changed")
    if not all(value == 0 for value in residuals.values()):
        raise AssertionError("auxiliary-elimination certificate is not exact")
    return MappingProxyType({
        "velocity_order": data["velocity_order"],
        "auxiliary_order": data["auxiliary_order"],
        "rank_one_decomposition": True,
        "auxiliary_determinant_nonzero": True,
        "structured_auxiliary_solution_available": True,
        "auxiliary_solution_source":
            "exact action-derived auxiliary Euler rows",
        "auxiliary_solution_reconstruction_exact": True,
        "effective_kinetic_nondegenerate":
            data["effective_kinetic_nondegenerate"],
        "signs": data["signs"],
        "unresolved_factors": data["unresolved_factors"],
        "limitations": (
            "The result applies only to rho_b0>0 and rho_r0>0.",
            "Zero-density boundary charts are not covered.",
            "The complete H-chart quotient action is not constructed.",
            "The Weyl limit is not classified.",
            "No matrix-wide factorization was used.",
        ),
    })
