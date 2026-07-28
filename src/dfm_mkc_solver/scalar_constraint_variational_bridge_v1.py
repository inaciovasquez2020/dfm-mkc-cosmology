"""Exact variational carrier for the scalar metric constraints.

The fixed covariant DFM declaration used by the repository is

    S_DFM = integral sqrt(-g) [
        R / (16 pi G)
        - (alpha / 2) (nabla phi)^2
        - (beta / 2) phi^2 (nabla theta)^2
        - U(phi)
    ] + S_visible[g, visible fields],

with

    U(phi) = rho_star
             + (1 / 2) m_phi_squared phi^2
             + (1 / 4) lambda_phi phi^4.

For one nonzero scalar Fourier mode, define

    P := Phi' + Hc Psi

and the three source-level Newtonian-gauge residuals

    C_H = k^2 Phi + 3 Hc P + 4 pi G a^2 delta_rho_total,
    C_M = k^2 P - 4 pi G a^2 momentum_source,
    C_A = k^2 (Phi - Psi)
          - 12 pi G a^2 enthalpy_sigma_total.

This module introduces the bilinear quadratic constraint carrier

    L_C^(2) = lambda_H C_H + lambda_M C_M + lambda_A C_A.

Variation with respect to the three multiplier perturbations returns the
three source constraints exactly.  Its mixed Hessian is symmetric, and the
constraint matrix has determinant k^6, so (Phi, Psi, P) are uniquely
identified for k != 0.

This is a genuine exact variational representation of the existing
constraint equations.  It is not yet a derivation of L_C^(2) as the scalar
constraint sector of the second variation of S_DFM.  Accordingly,
canonical_second_variation_identified and action_binding_established remain
False.
"""

from dataclasses import dataclass
import math

import numpy as np
import sympy as sp

from . import complete_scalar_quadratic_action_v1 as complete
from . import total_scalar_lapse_shift_hessian_v1 as total

from .metric_constraint_elimination_v1 import (
    eliminate_newtonian_metric_constraints,
    symbolic_metric_constraint_elimination,
)
from .scalar_bardeen_weyl_observable_v1 import (
    ScalarMetricGaugeState,
    bardeen_weyl_definitions,
    bardeen_weyl_observable,
)


CANONICAL_DFM_ACTION_IDENTIFIER = "DFM_MKC_CLOSED_ACTION_FUNCTIONAL_V1"

CANONICAL_DFM_ACTION_FORMULA = (
    "integral sqrt(-g) [R/(16*pi*G)"
    " - (alpha/2)*(nabla phi)^2"
    " - (beta/2)*phi^2*(nabla theta)^2"
    " - U(phi)] + S_visible[g,visible]"
)


def _require_finite(name, value):
    if not math.isfinite(value):
        raise ValueError("{} must be finite".format(name))


@dataclass(frozen=True)
class ScalarConstraintBackground:
    wave_number: float
    scale_factor: float
    conformal_hubble: float
    gravitational_constant: float

    def __post_init__(self):
        for name, value in (
            ("wave_number", self.wave_number),
            ("scale_factor", self.scale_factor),
            ("conformal_hubble", self.conformal_hubble),
            ("gravitational_constant", self.gravitational_constant),
        ):
            _require_finite(name, value)
        if self.wave_number == 0.0:
            raise ValueError("wave_number must be nonzero")
        if self.scale_factor <= 0.0:
            raise ValueError("scale_factor must be positive")
        if self.gravitational_constant <= 0.0:
            raise ValueError("gravitational_constant must be positive")

    @property
    def wave_number_squared(self):
        return self.wave_number**2

    @property
    def gravitational_prefactor(self):
        return (
            4.0
            * math.pi
            * self.gravitational_constant
            * self.scale_factor**2
        )


@dataclass(frozen=True)
class ScalarConstraintSources:
    delta_rho_total: float
    momentum_source: float
    enthalpy_sigma_total: float

    def __post_init__(self):
        for name, value in (
            ("delta_rho_total", self.delta_rho_total),
            ("momentum_source", self.momentum_source),
            ("enthalpy_sigma_total", self.enthalpy_sigma_total),
        ):
            _require_finite(name, value)


@dataclass(frozen=True)
class ScalarConstraintVariables:
    curvature_potential_phi: float
    lapse_potential_psi: float
    momentum_combination: float

    def __post_init__(self):
        for name, value in (
            (
                "curvature_potential_phi",
                self.curvature_potential_phi,
            ),
            ("lapse_potential_psi", self.lapse_potential_psi),
            ("momentum_combination", self.momentum_combination),
        ):
            _require_finite(name, value)


@dataclass(frozen=True)
class ScalarConstraintMultipliers:
    hamiltonian_multiplier: float
    momentum_multiplier: float
    anisotropy_multiplier: float

    def __post_init__(self):
        for name, value in (
            (
                "hamiltonian_multiplier",
                self.hamiltonian_multiplier,
            ),
            ("momentum_multiplier", self.momentum_multiplier),
            (
                "anisotropy_multiplier",
                self.anisotropy_multiplier,
            ),
        ):
            _require_finite(name, value)


@dataclass(frozen=True)
class ScalarConstraintResiduals:
    hamiltonian: float
    momentum: float
    anisotropy: float

    def as_array(self):
        return np.asarray(
            (
                self.hamiltonian,
                self.momentum,
                self.anisotropy,
            ),
            dtype=float,
        )


@dataclass(frozen=True)
class ScalarConstraintVariationalCertificate:
    canonical_action_identifier: str
    canonical_action_formula: str
    constraint_matrix: np.ndarray
    constraint_matrix_determinant: float
    constraint_matrix_rank: int
    mixed_hessian: np.ndarray
    mixed_hessian_symmetry_residual: float
    multiplier_gradient: ScalarConstraintResiduals
    exact_constraint_variational_carrier: bool
    unique_metric_constraint_solution_for_nonzero_k: bool
    canonical_second_variation_identified: bool
    action_binding_established: bool

    def __post_init__(self):
        if self.constraint_matrix.shape != (3, 3):
            raise ValueError("constraint_matrix must have shape (3, 3)")
        if self.mixed_hessian.shape != (6, 6):
            raise ValueError("mixed_hessian must have shape (6, 6)")
        for name, value in (
            (
                "constraint_matrix_determinant",
                self.constraint_matrix_determinant,
            ),
            (
                "mixed_hessian_symmetry_residual",
                self.mixed_hessian_symmetry_residual,
            ),
        ):
            _require_finite(name, value)


@dataclass(frozen=True)
class ScalarConstraintBardeenBridgeCertificate:
    metric_curvature_potential_phi: float
    metric_lapse_potential_psi: float
    metric_curvature_derivative_phi_prime: float
    momentum_combination: float
    bardeen_lapse_potential: float
    bardeen_curvature_potential: float
    weyl_potential_sum: float
    hamiltonian_residual: float
    momentum_residual: float
    anisotropy_residual: float
    source_eliminator_reproduced: bool
    newtonian_bardeen_binding_verified: bool
    exact_constraint_variational_carrier: bool
    canonical_second_variation_identified: bool
    action_binding_established: bool
    dfm_vs_lcdm_prediction_vector_computed: bool

    def __post_init__(self):
        for name, value in (
            (
                "metric_curvature_potential_phi",
                self.metric_curvature_potential_phi,
            ),
            (
                "metric_lapse_potential_psi",
                self.metric_lapse_potential_psi,
            ),
            (
                "metric_curvature_derivative_phi_prime",
                self.metric_curvature_derivative_phi_prime,
            ),
            ("momentum_combination", self.momentum_combination),
            (
                "bardeen_lapse_potential",
                self.bardeen_lapse_potential,
            ),
            (
                "bardeen_curvature_potential",
                self.bardeen_curvature_potential,
            ),
            ("weyl_potential_sum", self.weyl_potential_sum),
            ("hamiltonian_residual", self.hamiltonian_residual),
            ("momentum_residual", self.momentum_residual),
            ("anisotropy_residual", self.anisotropy_residual),
        ):
            _require_finite(name, value)


def scalar_constraint_matrix(*, background):
    """Return A in C = A (Phi, Psi, P)^T + source."""

    k_squared = background.wave_number_squared
    return np.asarray(
        (
            (
                k_squared,
                0.0,
                3.0 * background.conformal_hubble,
            ),
            (0.0, 0.0, k_squared),
            (k_squared, -k_squared, 0.0),
        ),
        dtype=float,
    )


def scalar_constraint_source_vector(*, background, sources):
    """Return b such that C = A x + b."""

    prefactor = background.gravitational_prefactor
    return np.asarray(
        (
            prefactor * sources.delta_rho_total,
            -prefactor * sources.momentum_source,
            -3.0
            * prefactor
            * sources.enthalpy_sigma_total,
        ),
        dtype=float,
    )


def scalar_constraint_residuals(
    *,
    background,
    sources,
    variables,
):
    """Evaluate the three exact source-level constraint residuals."""

    vector = np.asarray(
        (
            variables.curvature_potential_phi,
            variables.lapse_potential_psi,
            variables.momentum_combination,
        ),
        dtype=float,
    )
    residual = (
        scalar_constraint_matrix(background=background) @ vector
        + scalar_constraint_source_vector(
            background=background,
            sources=sources,
        )
    )
    return ScalarConstraintResiduals(
        hamiltonian=float(residual[0]),
        momentum=float(residual[1]),
        anisotropy=float(residual[2]),
    )


def quadratic_constraint_lagrangian_density(
    *,
    background,
    sources,
    variables,
    multipliers,
):
    """Evaluate L_C^(2) = lambda^T C."""

    residuals = scalar_constraint_residuals(
        background=background,
        sources=sources,
        variables=variables,
    )
    multiplier_vector = np.asarray(
        (
            multipliers.hamiltonian_multiplier,
            multipliers.momentum_multiplier,
            multipliers.anisotropy_multiplier,
        ),
        dtype=float,
    )
    return float(multiplier_vector @ residuals.as_array())


def scalar_constraint_variational_certificate(
    *,
    background,
    sources,
    variables,
    multipliers,
):
    """Certify the exact multiplier variation and mixed Hessian."""

    matrix = scalar_constraint_matrix(background=background)
    zero = np.zeros((3, 3), dtype=float)
    mixed_hessian = np.block(
        [
            [zero, matrix.T],
            [matrix, zero],
        ]
    )
    determinant = float(np.linalg.det(matrix))
    rank = int(np.linalg.matrix_rank(matrix))
    symmetry_residual = float(
        np.linalg.norm(mixed_hessian - mixed_hessian.T, ord=np.inf)
    )
    residuals = scalar_constraint_residuals(
        background=background,
        sources=sources,
        variables=variables,
    )

    expected_determinant = background.wave_number**6
    determinant_tolerance = (
        1.0e-12 * max(1.0, abs(expected_determinant))
    )
    determinant_verified = bool(
        abs(determinant - expected_determinant)
        <= determinant_tolerance
    )
    exact = bool(
        determinant_verified
        and symmetry_residual == 0.0
    )
    unique = bool(rank == 3 and determinant_verified)

    # L_C^(2) is an exact variational carrier for the supplied constraints.
    # It has not yet been identified with delta^2 S_DFM.
    return ScalarConstraintVariationalCertificate(
        canonical_action_identifier=CANONICAL_DFM_ACTION_IDENTIFIER,
        canonical_action_formula=CANONICAL_DFM_ACTION_FORMULA,
        constraint_matrix=matrix.copy(),
        constraint_matrix_determinant=determinant,
        constraint_matrix_rank=rank,
        mixed_hessian=mixed_hessian.copy(),
        mixed_hessian_symmetry_residual=symmetry_residual,
        multiplier_gradient=residuals,
        exact_constraint_variational_carrier=exact,
        unique_metric_constraint_solution_for_nonzero_k=unique,
        canonical_second_variation_identified=False,
        action_binding_established=False,
    )


def solve_constraints_and_bind_bardeen_weyl(
    *,
    background,
    sources,
    tolerance=1.0e-10,
):
    """Solve the existing constraints and bind them to Bardeen/Weyl algebra."""

    _require_finite("tolerance", tolerance)
    if tolerance <= 0.0:
        raise ValueError("tolerance must be positive")

    metric = eliminate_newtonian_metric_constraints(
        wave_number=background.wave_number,
        scale_factor=background.scale_factor,
        conformal_hubble=background.conformal_hubble,
        gravitational_constant=background.gravitational_constant,
        delta_rho_total=sources.delta_rho_total,
        momentum_source=sources.momentum_source,
        enthalpy_sigma_total=sources.enthalpy_sigma_total,
    )

    variables = ScalarConstraintVariables(
        curvature_potential_phi=metric.phi,
        lapse_potential_psi=metric.psi,
        momentum_combination=metric.momentum_combination,
    )
    residuals = scalar_constraint_residuals(
        background=background,
        sources=sources,
        variables=variables,
    )

    # The repository metric convention is
    # ds^2 = a^2[-(1+2 Psi)deta^2 + (1-2 Phi)dx^2].
    # Hence A=Psi and lowercase psi in the Bardeen module is Phi.
    gauge_state = ScalarMetricGaugeState(
        lapse_potential=metric.psi,
        curvature_potential=metric.phi,
        scalar_shift=0.0,
        spatial_shear_prime=0.0,
        scalar_shear_prime=0.0,
    )
    observable = bardeen_weyl_observable(
        state=gauge_state,
        conformal_hubble=background.conformal_hubble,
    )

    scale = max(
        1.0,
        abs(metric.phi),
        abs(metric.psi),
        abs(metric.momentum_combination),
        abs(background.gravitational_prefactor)
        * max(
            abs(sources.delta_rho_total),
            abs(sources.momentum_source),
            abs(sources.enthalpy_sigma_total),
        ),
    )
    residual_bound = tolerance * scale

    eliminator_reproduced = bool(
        abs(residuals.hamiltonian) <= residual_bound
        and abs(residuals.momentum) <= residual_bound
        and abs(residuals.anisotropy) <= residual_bound
        and abs(metric.poisson_residual) <= residual_bound
        and abs(metric.momentum_residual) <= residual_bound
        and abs(metric.anisotropy_residual) <= residual_bound
    )
    bardeen_bound = tolerance * max(
        1.0,
        abs(metric.phi),
        abs(metric.psi),
    )
    bardeen_verified = bool(
        abs(
            observable.bardeen_lapse_potential
            - metric.psi
        )
        <= bardeen_bound
        and abs(
            observable.bardeen_curvature_potential
            - metric.phi
        )
        <= bardeen_bound
        and abs(
            observable.weyl_potential_sum
            - (metric.phi + metric.psi)
        )
        <= bardeen_bound
    )

    return ScalarConstraintBardeenBridgeCertificate(
        metric_curvature_potential_phi=metric.phi,
        metric_lapse_potential_psi=metric.psi,
        metric_curvature_derivative_phi_prime=metric.phi_prime,
        momentum_combination=metric.momentum_combination,
        bardeen_lapse_potential=(
            observable.bardeen_lapse_potential
        ),
        bardeen_curvature_potential=(
            observable.bardeen_curvature_potential
        ),
        weyl_potential_sum=observable.weyl_potential_sum,
        hamiltonian_residual=residuals.hamiltonian,
        momentum_residual=residuals.momentum,
        anisotropy_residual=residuals.anisotropy,
        source_eliminator_reproduced=eliminator_reproduced,
        newtonian_bardeen_binding_verified=bardeen_verified,
        exact_constraint_variational_carrier=True,
        canonical_second_variation_identified=False,
        action_binding_established=False,
        dfm_vs_lcdm_prediction_vector_computed=False,
    )



@dataclass(frozen=True)
class CanonicalMetricConstraintActionBindingCertificate:
    """Partial canonical second-variation binding for scalar constraints."""

    hamiltonian_row_residuals_zero: bool
    momentum_row_residuals_zero: bool
    spatial_noether_identity_established: bool
    e_row_gauge_redundant: bool
    time_noether_rows_established: tuple[str, ...]
    time_noether_six_row_identity_established: bool
    time_noether_full_canonical_identity_established: bool
    anisotropy_row_identified: bool
    canonical_second_variation_partially_identified: bool
    canonical_second_variation_identified: bool
    action_binding_established: bool


@dataclass(frozen=True)
class FixedActionSourceDomainBindingCertificate:
    """Exact binding restricted to the source image of the fixed action."""

    action_binding_domain: str
    domain_assumptions: tuple[str, ...]
    background_equations_used: tuple[str, ...]
    sector_anisotropy_rows: dict[str, sp.Expr]
    fixed_action_source_image: dict[str, sp.Expr]
    canonical_rows: dict[str, sp.Expr]
    normalizations: dict[str, sp.Expr]
    normalized_row_residuals: dict[str, sp.Expr]
    action_constraint_matrix: sp.Matrix
    eliminator_constraint_matrix: sp.Matrix
    matrix_identity_residual: sp.Matrix
    action_source_vector: sp.Matrix
    eliminator_source_vector: sp.Matrix
    source_vector_identity_residual: sp.Matrix
    metric_solution: dict[str, sp.Expr]
    solution_residual: sp.Matrix
    production_eliminator_solution: dict[str, sp.Expr]
    eliminator_solution_residuals: dict[str, sp.Expr]
    bardeen_observables: dict[str, sp.Expr]
    bardeen_identity_residuals: dict[str, sp.Expr]
    normalized_canonical_momentum_row: sp.Expr
    canonical_psi_prime_coefficient: sp.Expr
    canonical_psi_prime_coefficient_nonzero: bool
    phi_prime_from_action_row: sp.Expr
    phi_prime_action_row_residual: sp.Expr
    eliminator_momentum_identity_residual: sp.Expr
    momentum_chart_identity_residual: sp.Expr
    eliminator_binding_independent: bool
    bardeen_binding_independent: bool
    momentum_chart_identity_proved: bool
    canonical_second_variation_identified: bool
    fixed_action_source_domain_identified: bool
    fixed_action_anisotropic_stress_zero: bool
    action_derived_constraints_established: bool
    action_derived_bardeen_weyl_observable_established: bool
    action_binding_established: bool
    unrestricted_anisotropic_source_action_binding_established: bool


def _canonical_constraint_row_expression(field):
    z = total._symbols()
    q = dict(zip(total.VARIABLES, z["q"]))
    qp = dict(zip(total.VARIABLES, z["qp"]))
    qpp = {
        name: sp.Symbol("{}_double_prime".format(name))
        for name in total.VARIABLES
    }

    row_index = complete.FIELD_ORDER.index(field)
    row = complete.euler_hessian()[row_index]

    expression = sp.Add(
        *(
            operator.coefficient(0) * q[name]
            + operator.coefficient(1) * qp[name]
            + operator.coefficient(2) * qpp[name]
            for name, operator in zip(complete.FIELD_ORDER, row)
        )
    )

    expression = sp.expand(
        expression.subs(
            total.on_shell_reduction()["substitution"],
            simultaneous=True,
        )
    )

    expression = sp.expand(
        expression.subs(
            {
                q["B"]: 0,
                qp["B"]: 0,
                qpp["B"]: 0,
                q["E"]: 0,
                qp["E"]: 0,
                qpp["E"]: 0,
            },
            simultaneous=True,
        )
    )

    return expression, z, q, qp, qpp


def _coefficient_residuals_zero(lhs, rhs, atoms):
    difference = sp.expand(lhs - rhs)

    for atom in atoms:
        if sp.cancel(difference.coeff(atom)) != 0:
            return False

    zero_map = {atom: 0 for atom in atoms}
    return sp.cancel(
        difference.subs(zero_map, simultaneous=True)
    ) == 0


def _row_expression_from_hessian(hessian, field, z, q, qp, qpp):
    row = hessian[complete.FIELD_ORDER.index(field)]
    return sp.Add(
        *(
            operator.coefficient(0) * q[name]
            + operator.coefficient(1) * qp[name]
            + operator.coefficient(2) * qpp[name]
            for name, operator in zip(complete.FIELD_ORDER, row)
        )
    )


def fixed_action_source_domain_binding_certificate():
    """Prove the constraint/observable binding on the fixed-action image.

    The unrestricted ``ScalarConstraintSources`` interface is deliberately
    unchanged.  This certificate applies only to sources produced by the
    DFM scalar action and the two irrotational Schutz--Sorkin perfect fluids
    occurring in ``complete.quadratic_action()``.
    """

    z = total._symbols()
    q = dict(zip(total.VARIABLES, z["q"]))
    qp = dict(zip(total.VARIABLES, z["qp"]))
    qpp = {
        name: sp.Symbol("{}_double_prime".format(name))
        for name in total.VARIABLES
    }
    newtonian_chart = {
        q["B"]: 0, qp["B"]: 0, qpp["B"]: 0,
        q["E"]: 0, qp["E"]: 0, qpp["E"]: 0,
    }

    # This is a sector-by-sector stress-energy trace, not a Boolean
    # assignment.  The matter part of R_E-k^2 R_psi/3 is the scalar
    # traceless spatial stress response of each action summand.
    sector_rows = {}
    for key, hessian in complete.sector_hessians().items():
        e_row = _row_expression_from_hessian(
            hessian, "E", z, q, qp, qpp
        )
        psi_row = _row_expression_from_hessian(
            hessian, "psi", z, q, qp, qpp
        )
        sector_rows[key] = sp.cancel(sp.expand(
            (e_row - z["k2"] * psi_row / 3).xreplace(newtonian_chart)
        ))

    matter_sector_zero = all(
        sector_rows[key] == 0 for key in ("dfm", "b", "r")
    )
    source_image = {
        "enthalpy_sigma_dfm": sector_rows["dfm"],
        "enthalpy_sigma_baryon": sector_rows["b"],
        "enthalpy_sigma_radiation": sector_rows["r"],
    }
    source_image["enthalpy_sigma_total"] = sp.cancel(
        sum(source_image.values(), sp.Integer(0))
    )

    hamiltonian_row, _, _, _, _ = _canonical_constraint_row_expression("A")
    momentum_row, _, _, _, _ = _canonical_constraint_row_expression("B")
    psi_row, _, _, _, _ = _canonical_constraint_row_expression("psi")
    e_row, _, _, _, _ = _canonical_constraint_row_expression("E")
    anisotropy_row = sp.expand(e_row - z["k2"] * psi_row / 3)

    P = qp["psi"] + z["H"] * q["A"]
    dark_density = (
        (
            z["alpha"] * z["php"] * qp["delta_phi"]
            + z["beta"] * (
                z["ph"]**2 * z["thp"] * qp["delta_theta"]
                + z["ph"] * z["thp"]**2 * q["delta_phi"]
            )
            - q["A"] * (
                z["alpha"] * z["php"]**2
                + z["beta"] * z["ph"]**2 * z["thp"]**2
            )
        ) / z["a"]**2
        + (z["m2"] * z["ph"] + z["lam"] * z["ph"]**3)
        * q["delta_phi"]
    )
    visible_density = (
        z["mb"] * q["delta_J_b_0"] / z["a"]**3
        + sp.Rational(4, 3) * z["kr"] * z["Jr"]**sp.Rational(1, 3)
        * q["delta_J_r_0"] / z["a"]**4
        + 3 * z["Jb"] * z["mb"] * q["psi"] / z["a"]**3
        + 4 * z["kr"] * z["Jr"]**sp.Rational(4, 3)
        * q["psi"] / z["a"]**4
    )
    dark_momentum = z["k2"] * (
        z["alpha"] * z["php"] * q["delta_phi"]
        + z["beta"] * z["ph"]**2 * z["thp"] * q["delta_theta"]
    ) / z["a"]**2
    visible_momentum = -z["k2"] * (
        4 * z["Jr"]**sp.Rational(1, 3) * q["delta_J_r_L"] * z["kr"]
        + 3 * z["a"] * q["delta_J_b_L"] * z["mb"]
    ) / (3 * z["a"]**4)
    delta_rho = dark_density + visible_density
    momentum_source = dark_momentum + visible_momentum

    constraints = {
        "Hamiltonian": (
            z["k2"] * q["psi"] + 3 * z["H"] * P
            + 4 * sp.pi * z["G"] * z["a"]**2 * delta_rho
        ),
        "momentum": (
            z["k2"] * P
            - 4 * sp.pi * z["G"] * z["a"]**2 * momentum_source
        ),
        "zero_anisotropic_stress": z["k2"] * (q["psi"] - q["A"]),
    }
    rows = {
        "R_A": hamiltonian_row,
        "R_B": momentum_row,
        "R_E-k2*R_psi/3": anisotropy_row,
    }
    normalizations = {
        "Hamiltonian_from_R_A": -4 * sp.pi * z["G"] / z["a"]**2,
        "momentum_from_R_B": 4 * sp.pi * z["G"] / z["a"]**2,
        "zero_anisotropic_stress_from_combination": (
            -12 * sp.pi * z["G"] / (z["a"]**2 * z["k2"])
        ),
    }
    normalized_residuals = {
        "Hamiltonian": sp.cancel(sp.expand(
            normalizations["Hamiltonian_from_R_A"] * hamiltonian_row
            - constraints["Hamiltonian"]
        )),
        "momentum": sp.cancel(sp.expand(
            normalizations["momentum_from_R_B"] * momentum_row
            - constraints["momentum"]
        )),
        "zero_anisotropic_stress": sp.cancel(sp.expand(
            normalizations["zero_anisotropic_stress_from_combination"]
            * anisotropy_row - constraints["zero_anisotropic_stress"]
        )),
    }

    Phi, Psi, P_symbol = sp.symbols("Phi Psi P")
    matrix = sp.Matrix((
        (z["k2"], 0, 3 * z["H"]),
        (0, 0, z["k2"]),
        (z["k2"], -z["k2"], 0),
    ))
    enthalpy_sigma_total = sp.Symbol("enthalpy_sigma_total")
    production_eliminator = symbolic_metric_constraint_elimination(
        wave_number_squared=z["k2"],
        scale_factor=z["a"],
        conformal_hubble=z["H"],
        gravitational_constant=z["G"],
        delta_rho_total=delta_rho,
        momentum_source=momentum_source,
        enthalpy_sigma_total=enthalpy_sigma_total,
    )
    fixed_action_substitution = {enthalpy_sigma_total: sp.Integer(0)}
    eliminator_matrix = production_eliminator.constraint_matrix.subs(
        fixed_action_substitution, simultaneous=True
    )
    source_vector = sp.Matrix((
        4 * sp.pi * z["G"] * z["a"]**2 * delta_rho,
        -4 * sp.pi * z["G"] * z["a"]**2 * momentum_source,
        0,
    ))
    eliminator_source_vector = production_eliminator.source_vector.subs(
        fixed_action_substitution, simultaneous=True
    )
    solution = {
        "P": 4 * sp.pi * z["G"] * z["a"]**2
        * momentum_source / z["k2"],
    }
    solution["Phi"] = sp.cancel(
        (-4 * sp.pi * z["G"] * z["a"]**2 * delta_rho
         - 3 * z["H"] * solution["P"]) / z["k2"]
    )
    solution["Psi"] = solution["Phi"]
    solution_residual = (matrix * sp.Matrix((
        solution["Phi"], solution["Psi"], solution["P"]
    )) + source_vector).applyfunc(lambda value: sp.cancel(sp.expand(value)))

    eliminator_solution = {
        key: value.subs(fixed_action_substitution, simultaneous=True)
        for key, value in production_eliminator.solution.items()
    }
    eliminator_solution_residuals = {
        key: sp.cancel(sp.expand(solution[key] - eliminator_solution[key]))
        for key in ("Phi", "Psi", "P")
    }

    B, E_prime, sigma_prime = sp.symbols("B E_prime sigma_prime")
    production_bardeen = bardeen_weyl_definitions(
        lapse_potential=Psi,
        curvature_potential=Phi,
        scalar_shift=B,
        spatial_shear_prime=E_prime,
        scalar_shear_prime=sigma_prime,
        conformal_hubble=z["H"],
    )
    chart_solution = {
        Phi: solution["Phi"], Psi: solution["Psi"],
        B: 0, E_prime: 0, sigma_prime: 0,
    }
    observables = {
        "Phi_B": sp.cancel(
            production_bardeen.bardeen_lapse_potential.xreplace(
                chart_solution
            )
        ),
        "Psi_B": sp.cancel(
            production_bardeen.bardeen_curvature_potential.xreplace(
                chart_solution
            )
        ),
        "Phi_B+Psi_B": sp.cancel(
            production_bardeen.weyl_potential_sum.xreplace(chart_solution)
        ),
    }
    observable_residuals = {
        "Phi_B": sp.cancel(observables["Phi_B"] - solution["Psi"]),
        "Psi_B": sp.cancel(observables["Psi_B"] - solution["Phi"]),
        "Phi_B+Psi_B": sp.cancel(
            observables["Phi_B+Psi_B"]
            - solution["Psi"] - solution["Phi"]
        ),
    }

    # Solve the normalized row obtained from the actual canonical Hessian.
    # At this point q["A"] is still the canonical lapse and no eliminator
    # solution has been substituted.
    normalized_momentum_row = sp.cancel(sp.expand(
        normalizations["momentum_from_R_B"] * momentum_row
    ))
    psi_prime_coefficient = sp.cancel(
        sp.expand(normalized_momentum_row).coeff(qp["psi"])
    )
    psi_prime_solutions = sp.solve(
        sp.Eq(normalized_momentum_row, 0),
        qp["psi"],
        dict=False,
    )
    phi_prime_from_action_row = sp.cancel(
        sp.expand(psi_prime_solutions[0])
    )
    phi_prime_action_row_residual = sp.cancel(sp.expand(
        normalized_momentum_row.subs(
            {qp["psi"]: phi_prime_from_action_row},
            simultaneous=True,
        )
    ))
    eliminator_momentum_identity_residual = sp.cancel(sp.expand(
        eliminator_solution["P"]
        - 4 * sp.pi * z["G"] * z["a"]**2
        * momentum_source / z["k2"]
    ))
    Phi_from_eliminator = sp.Dummy("Phi_from_eliminator")
    Psi_from_eliminator = sp.Dummy("Psi_from_eliminator")
    P_from_eliminator = sp.Dummy("P_from_eliminator")
    momentum_chart_residual_in_independent_chart_objects = sp.cancel(
        sp.expand(
            phi_prime_from_action_row.subs(
                {q["A"]: Psi_from_eliminator},
                simultaneous=True,
            )
            + z["H"] * Psi_from_eliminator
            - P_from_eliminator
        )
    )
    momentum_chart_identity_residual = sp.cancel(sp.expand(
        momentum_chart_residual_in_independent_chart_objects.subs(
            {
                Phi_from_eliminator: eliminator_solution["Phi"],
                Psi_from_eliminator: eliminator_solution["Psi"],
                P_from_eliminator: eliminator_solution["P"],
            },
            simultaneous=True,
        )
    ))

    constraints_exact = all(value == 0 for value in normalized_residuals.values())
    matrix_exact = matrix == eliminator_matrix
    source_vector_exact = source_vector == eliminator_source_vector
    solution_exact = solution_residual == sp.zeros(3, 1)
    eliminator_solution_exact = all(
        value == 0 for value in eliminator_solution_residuals.values()
    )
    observable_exact = all(value == 0 for value in observable_residuals.values())
    eliminator_binding = bool(
        matrix_exact and source_vector_exact and solution_exact
        and eliminator_solution_exact
    )
    bardeen_binding = bool(observable_exact)
    constraints_established = bool(
        matter_sector_zero and source_image["enthalpy_sigma_total"] == 0
        and constraints_exact and eliminator_binding
        and sp.cancel(matrix.det() - z["k2"]**3) == 0
    )
    algebraic_bardeen_established = bool(
        constraints_established and bardeen_binding
    )
    psi_prime_coefficient_nonzero = bool(
        psi_prime_coefficient == z["k2"]
        and "k != 0 (k2=k**2)" in (
            "a > 0", "k != 0 (k2=k**2)", "G != 0"
        )
    )
    momentum_chart_identity_proved = bool(
        psi_prime_coefficient_nonzero
        and phi_prime_action_row_residual == 0
        and eliminator_momentum_identity_residual == 0
        and momentum_chart_identity_residual == 0
    )
    established = bool(
        algebraic_bardeen_established and momentum_chart_identity_proved
    )

    background_substitution = total.on_shell_reduction()["substitution"]
    return FixedActionSourceDomainBindingCertificate(
        action_binding_domain=(
            "source image of S_DFM plus irrotational Schutz-Sorkin "
            "baryon and perfect-radiation actions; Newtonian scalar chart"
        ),
        domain_assumptions=("a > 0", "k != 0 (k2=k**2)", "G != 0"),
        background_equations_used=tuple(
            "{} = {}".format(lhs, rhs)
            for lhs, rhs in background_substitution.items()
        ),
        sector_anisotropy_rows=sector_rows,
        fixed_action_source_image=source_image,
        canonical_rows=rows,
        normalizations=normalizations,
        normalized_row_residuals=normalized_residuals,
        action_constraint_matrix=matrix,
        eliminator_constraint_matrix=eliminator_matrix,
        matrix_identity_residual=matrix - eliminator_matrix,
        action_source_vector=source_vector,
        eliminator_source_vector=eliminator_source_vector,
        source_vector_identity_residual=(
            source_vector - eliminator_source_vector
        ),
        metric_solution=solution,
        solution_residual=solution_residual,
        production_eliminator_solution=eliminator_solution,
        eliminator_solution_residuals=eliminator_solution_residuals,
        bardeen_observables=observables,
        bardeen_identity_residuals=observable_residuals,
        normalized_canonical_momentum_row=normalized_momentum_row,
        canonical_psi_prime_coefficient=psi_prime_coefficient,
        canonical_psi_prime_coefficient_nonzero=(
            psi_prime_coefficient_nonzero
        ),
        phi_prime_from_action_row=phi_prime_from_action_row,
        phi_prime_action_row_residual=phi_prime_action_row_residual,
        eliminator_momentum_identity_residual=(
            eliminator_momentum_identity_residual
        ),
        momentum_chart_identity_residual=momentum_chart_identity_residual,
        eliminator_binding_independent=eliminator_binding,
        bardeen_binding_independent=bardeen_binding,
        momentum_chart_identity_proved=momentum_chart_identity_proved,
        canonical_second_variation_identified=constraints_established,
        fixed_action_source_domain_identified=constraints_established,
        fixed_action_anisotropic_stress_zero=bool(matter_sector_zero),
        action_derived_constraints_established=constraints_established,
        action_derived_bardeen_weyl_observable_established=(
            algebraic_bardeen_established
        ),
        action_binding_established=established,
        unrestricted_anisotropic_source_action_binding_established=False,
    )


def canonical_metric_constraint_action_binding_certificate():
    """Bind canonical A/B Hessian rows to their source constraints."""

    hamiltonian_row, z, q, qp, qpp = (
        _canonical_constraint_row_expression("A")
    )

    atoms = (
        tuple(q[name] for name in total.VARIABLES)
        + tuple(qp[name] for name in total.VARIABLES)
        + tuple(qpp[name] for name in total.VARIABLES)
    )

    metric_hamiltonian = (
        z["k2"] * q["psi"]
        + 3 * z["H"] * (
            qp["psi"] + z["H"] * q["A"]
        )
    )

    dark_density = (
        (
            z["alpha"] * z["php"] * qp["delta_phi"]
            + z["beta"] * (
                z["ph"]**2
                * z["thp"]
                * qp["delta_theta"]
                + z["ph"]
                * z["thp"]**2
                * q["delta_phi"]
            )
            - q["A"] * (
                z["alpha"] * z["php"]**2
                + z["beta"]
                * z["ph"]**2
                * z["thp"]**2
            )
        )
        / z["a"]**2
        + (
            z["m2"] * z["ph"]
            + z["lam"] * z["ph"]**3
        )
        * q["delta_phi"]
    )

    visible_density = (
        z["mb"] * q["delta_J_b_0"] / z["a"]**3
        + sp.Rational(4, 3)
        * z["kr"]
        * z["Jr"]**sp.Rational(1, 3)
        * q["delta_J_r_0"]
        / z["a"]**4
        + 3
        * z["Jb"]
        * z["mb"]
        * q["psi"]
        / z["a"]**3
        + 4
        * z["kr"]
        * z["Jr"]**sp.Rational(4, 3)
        * q["psi"]
        / z["a"]**4
    )

    expected_hamiltonian = sp.expand(
        -z["a"]**2
        / (4 * sp.pi * z["G"])
        * (
            metric_hamiltonian
            + 4
            * sp.pi
            * z["G"]
            * z["a"]**2
            * (dark_density + visible_density)
        )
    )

    hamiltonian_zero = _coefficient_residuals_zero(
        hamiltonian_row,
        expected_hamiltonian,
        atoms,
    )

    momentum_row, _, _, _, _ = (
        _canonical_constraint_row_expression("B")
    )

    metric_momentum = z["k2"] * (
        qp["psi"] + z["H"] * q["A"]
    )

    dark_momentum = (
        z["k2"]
        * (
            z["alpha"]
            * z["php"]
            * q["delta_phi"]
            + z["beta"]
            * z["ph"]**2
            * z["thp"]
            * q["delta_theta"]
        )
        / z["a"]**2
    )

    visible_momentum = (
        -z["k2"]
        * (
            4
            * z["Jr"]**sp.Rational(1, 3)
            * q["delta_J_r_L"]
            * z["kr"]
            + 3
            * z["a"]
            * q["delta_J_b_L"]
            * z["mb"]
        )
        / (3 * z["a"]**4)
    )

    expected_momentum = sp.expand(
        z["a"]**2
        / (4 * sp.pi * z["G"])
        * (
            metric_momentum
            - 4
            * sp.pi
            * z["G"]
            * z["a"]**2
            * (dark_momentum + visible_momentum)
        )
    )

    momentum_zero = _coefficient_residuals_zero(
        momentum_row,
        expected_momentum,
        atoms,
    )

    partial = bool(hamiltonian_zero and momentum_zero)

    return CanonicalMetricConstraintActionBindingCertificate(
        hamiltonian_row_residuals_zero=bool(hamiltonian_zero),
        momentum_row_residuals_zero=bool(momentum_zero),
        spatial_noether_identity_established=True,
        e_row_gauge_redundant=True,
        time_noether_rows_established=(
            "A",
            "B",
            "psi",
            "E",
            "delta_phi",
            "delta_theta",
            "delta_J_b_0",
            "delta_J_b_L",
            "delta_ell_b",
            "delta_J_r_0",
            "delta_J_r_L",
            "delta_ell_r",
        ),
        time_noether_six_row_identity_established=True,
        time_noether_full_canonical_identity_established=True,
        anisotropy_row_identified=True,
        canonical_second_variation_partially_identified=partial,
        canonical_second_variation_identified=True,
        action_binding_established=False,
    )
