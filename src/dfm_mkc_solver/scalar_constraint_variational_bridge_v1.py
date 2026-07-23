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

from .metric_constraint_elimination_v1 import (
    eliminate_newtonian_metric_constraints,
)
from .scalar_bardeen_weyl_observable_v1 import (
    ScalarMetricGaugeState,
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
