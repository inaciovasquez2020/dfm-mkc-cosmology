"""Self-consistent initial metric fixed-point matching.

For a supplied averaged density mode, the existing matching surface maps a
metric triple

    (Phi, dPhi/dN, Psi)

to a four-component full-field perturbation state. The action-derived
Fourier constraint solver maps that state back to a metric triple.

Because the linear perturbation system makes this map affine, this module
constructs the affine map explicitly and solves

    m = T(m)

as a three-dimensional linear system. The returned certificate verifies the
affine reduction, uniqueness, the matching identities, and the metric
constraint fixed-point residual.
"""

from __future__ import annotations

import math
from collections.abc import Mapping
from dataclasses import asdict, dataclass, is_dataclass
from typing import Any

import numpy as np

from .averaged_full_field_matching_surface_v1 import (
    AveragedFullFieldInitialMatchingCertificate,
    match_averaged_mode_on_pressureless_phase_locked_slice,
)
from .dark_sector_fourier_rhs_v1 import (
    DarkSectorFourierRightHandSideCertificate,
    dark_sector_fourier_right_hand_side,
)

State4 = tuple[float, float, float, float]
Metric3 = tuple[float, float, float]
Matrix3 = tuple[
    tuple[float, float, float],
    tuple[float, float, float],
    tuple[float, float, float],
]


@dataclass(frozen=True)
class InitialMetricFixedPointCertificate:
    initial_state: State4
    phi_metric: float
    phi_metric_n: float
    psi_metric: float
    reconstructed_phi_metric: float
    reconstructed_phi_metric_n: float
    reconstructed_psi_metric: float
    fixed_point_residual: Metric3
    maximum_fixed_point_residual: float
    affine_offset: Metric3
    affine_matrix: Matrix3
    affine_probe_residual: Metric3
    maximum_affine_probe_residual: float
    fixed_point_matrix: Matrix3
    fixed_point_matrix_determinant: float
    fixed_point_matrix_condition_number: float
    matching_surface_closed: bool
    instantaneous_rhs_closed: bool
    affine_metric_map_verified: bool
    unique_fixed_point_verified: bool
    initial_metric_fixed_point_solved: bool
    time_dependent_full_field_evolution_solved: bool
    observational_calibration_completed: bool


def _require_finite(name: str, value: float) -> None:
    if not math.isfinite(value):
        raise ValueError(f"{name} must be finite")


def _mapping(value: Any) -> dict[str, Any]:
    if is_dataclass(value):
        converted = asdict(value)
        if isinstance(converted, dict):
            return converted
    if isinstance(value, Mapping):
        return dict(value)
    if hasattr(value, "__dict__"):
        return dict(vars(value))
    raise ValueError(
        "MISSING_OBJECT := inspectable metric-constraint certificate"
    )


def _normalized_mapping(value: Any) -> dict[str, float]:
    result: dict[str, float] = {}
    for key, item in _mapping(value).items():
        if isinstance(item, bool):
            continue
        if isinstance(item, (int, float, np.floating)):
            result[str(key).lower()] = float(item)
    return result


def _extract_from_schema(
    payload: dict[str, float],
    schema: tuple[str, str, str],
    *,
    conformal_hubble: float,
    derivative_is_conformal: bool,
) -> Metric3 | None:
    keys = tuple(key.lower() for key in schema)
    if not all(key in payload for key in keys):
        return None

    phi_metric = payload[keys[0]]
    phi_derivative = payload[keys[1]]
    psi_metric = payload[keys[2]]

    if derivative_is_conformal:
        phi_metric_n = phi_derivative / conformal_hubble
    else:
        phi_metric_n = phi_derivative

    return (
        float(phi_metric),
        float(phi_metric_n),
        float(psi_metric),
    )


def _extract_metric_solution(
    certificate: DarkSectorFourierRightHandSideCertificate,
    *,
    conformal_hubble: float,
) -> Metric3:
    direct_n_schemas = (
        ("phi_metric", "phi_metric_n", "psi_metric"),
        ("metric_phi", "metric_phi_n", "metric_psi"),
        ("phi", "phi_n", "psi"),
        ("newtonian_phi", "newtonian_phi_n", "newtonian_psi"),
    )
    conformal_schemas = (
        ("phi_metric", "phi_metric_prime", "psi_metric"),
        ("metric_phi", "metric_phi_prime", "metric_psi"),
        ("phi", "phi_prime", "psi"),
        (
            "newtonian_phi",
            "newtonian_phi_prime",
            "newtonian_psi",
        ),
    )

    sources = (
        certificate.metric_constraints,
        certificate,
    )

    for source in sources:
        payload = _normalized_mapping(source)

        for schema in direct_n_schemas:
            result = _extract_from_schema(
                payload,
                schema,
                conformal_hubble=conformal_hubble,
                derivative_is_conformal=False,
            )
            if result is not None:
                return result

        for schema in conformal_schemas:
            result = _extract_from_schema(
                payload,
                schema,
                conformal_hubble=conformal_hubble,
                derivative_is_conformal=True,
            )
            if result is not None:
                return result

    available = sorted(
        {
            key
            for source in sources
            for key in _normalized_mapping(source)
        }
    )
    raise ValueError(
        "MISSING_OBJECT := metric solution fields; "
        f"available={available}"
    )


def solve_initial_metric_fixed_point(
    *,
    scale_factor: float,
    conformal_hubble: float,
    wave_number: float,
    gravitational_constant: float,
    phi_background: float,
    phi_prime_background: float,
    theta_prime_background: float,
    target_density_contrast: float,
    target_density_contrast_n: float,
    alpha: float,
    beta: float,
    rho_star: float,
    m_phi_squared: float,
    lambda_phi: float,
    denominator_tolerance: float = 1.0e-14,
    residual_tolerance: float = 1.0e-9,
    affine_tolerance: float = 1.0e-9,
    maximum_condition_number: float = 1.0e12,
) -> InitialMetricFixedPointCertificate:
    """Solve and verify the affine metric matching fixed point."""
    for name, value in (
        ("scale_factor", scale_factor),
        ("conformal_hubble", conformal_hubble),
        ("wave_number", wave_number),
        ("gravitational_constant", gravitational_constant),
        ("phi_background", phi_background),
        ("phi_prime_background", phi_prime_background),
        ("theta_prime_background", theta_prime_background),
        ("target_density_contrast", target_density_contrast),
        ("target_density_contrast_n", target_density_contrast_n),
        ("alpha", alpha),
        ("beta", beta),
        ("rho_star", rho_star),
        ("m_phi_squared", m_phi_squared),
        ("lambda_phi", lambda_phi),
        ("denominator_tolerance", denominator_tolerance),
        ("residual_tolerance", residual_tolerance),
        ("affine_tolerance", affine_tolerance),
        ("maximum_condition_number", maximum_condition_number),
    ):
        _require_finite(name, value)

    if scale_factor <= 0.0:
        raise ValueError("scale_factor must be positive")
    if conformal_hubble <= 0.0:
        raise ValueError("conformal_hubble must be positive")
    if wave_number <= 0.0:
        raise ValueError("wave_number must be positive")
    if gravitational_constant <= 0.0:
        raise ValueError("gravitational_constant must be positive")
    if denominator_tolerance <= 0.0:
        raise ValueError("denominator_tolerance must be positive")
    if residual_tolerance <= 0.0:
        raise ValueError("residual_tolerance must be positive")
    if affine_tolerance <= 0.0:
        raise ValueError("affine_tolerance must be positive")
    if maximum_condition_number <= 1.0:
        raise ValueError(
            "maximum_condition_number must exceed one"
        )

    def metric_map(
        metric: np.ndarray,
    ) -> tuple[
        np.ndarray,
        AveragedFullFieldInitialMatchingCertificate,
        DarkSectorFourierRightHandSideCertificate,
    ]:
        matching = (
            match_averaged_mode_on_pressureless_phase_locked_slice(
                scale_factor=scale_factor,
                conformal_hubble=conformal_hubble,
                wave_number=wave_number,
                phi_background=phi_background,
                phi_prime_background=phi_prime_background,
                theta_prime_background=theta_prime_background,
                phi_metric=float(metric[0]),
                phi_metric_n=float(metric[1]),
                psi_metric=float(metric[2]),
                target_density_contrast=target_density_contrast,
                target_density_contrast_n=(
                    target_density_contrast_n
                ),
                alpha=alpha,
                beta=beta,
                rho_star=rho_star,
                m_phi_squared=m_phi_squared,
                lambda_phi=lambda_phi,
                nonzero_tolerance=denominator_tolerance,
                residual_tolerance=residual_tolerance,
            )
        )

        state = matching.initial_state
        rhs = dark_sector_fourier_right_hand_side(
            scale_factor=scale_factor,
            conformal_hubble=conformal_hubble,
            wave_number=wave_number,
            gravitational_constant=gravitational_constant,
            phi_background=phi_background,
            phi_prime_background=phi_prime_background,
            theta_prime_background=theta_prime_background,
            delta_phi=state[0],
            delta_phi_prime=state[1],
            delta_theta=state[2],
            delta_theta_prime=state[3],
            alpha=alpha,
            beta=beta,
            rho_star=rho_star,
            m_phi_squared=m_phi_squared,
            lambda_phi=lambda_phi,
            denominator_tolerance=denominator_tolerance,
        )

        solved = np.asarray(
            _extract_metric_solution(
                rhs,
                conformal_hubble=conformal_hubble,
            ),
            dtype=float,
        )
        if solved.shape != (3,) or not np.all(np.isfinite(solved)):
            raise ValueError(
                "metric constraint solution must be a finite triple"
            )
        return solved, matching, rhs

    zero = np.zeros(3, dtype=float)
    affine_offset_array, _, _ = metric_map(zero)

    affine_matrix_array = np.empty((3, 3), dtype=float)
    for column in range(3):
        basis = np.zeros(3, dtype=float)
        basis[column] = 1.0
        image, _, _ = metric_map(basis)
        affine_matrix_array[:, column] = (
            image - affine_offset_array
        )

    probe = np.asarray([0.173, -0.119, 0.071], dtype=float)
    direct_probe, _, _ = metric_map(probe)
    predicted_probe = (
        affine_offset_array + affine_matrix_array @ probe
    )
    affine_probe_residual_array = (
        direct_probe - predicted_probe
    )
    maximum_affine_probe_residual = float(
        np.max(np.abs(affine_probe_residual_array))
    )
    affine_metric_map_verified = (
        maximum_affine_probe_residual <= affine_tolerance
    )
    if not affine_metric_map_verified:
        raise ValueError(
            "metric matching map failed the affine verification"
        )

    fixed_point_matrix_array = (
        np.eye(3, dtype=float) - affine_matrix_array
    )
    determinant = float(np.linalg.det(fixed_point_matrix_array))
    condition_number = float(
        np.linalg.cond(fixed_point_matrix_array)
    )
    rank = int(np.linalg.matrix_rank(fixed_point_matrix_array))

    _require_finite("fixed_point_matrix_determinant", determinant)
    _require_finite(
        "fixed_point_matrix_condition_number",
        condition_number,
    )

    unique_fixed_point_verified = (
        rank == 3
        and abs(determinant) > denominator_tolerance
        and condition_number <= maximum_condition_number
    )
    if not unique_fixed_point_verified:
        raise ValueError(
            "initial metric fixed-point matrix is singular or "
            "insufficiently conditioned"
        )

    metric_solution = np.linalg.solve(
        fixed_point_matrix_array,
        affine_offset_array,
    )
    reconstructed_metric, matching, rhs = metric_map(
        metric_solution
    )
    fixed_point_residual_array = (
        reconstructed_metric - metric_solution
    )
    maximum_fixed_point_residual = float(
        np.max(np.abs(fixed_point_residual_array))
    )
    initial_metric_fixed_point_solved = (
        maximum_fixed_point_residual <= residual_tolerance
        and matching.matching_surface_closed
        and rhs.instantaneous_dark_sector_rhs_closed
    )
    if not initial_metric_fixed_point_solved:
        raise ValueError(
            "initial metric fixed point failed verification"
        )

    def vector3(array: np.ndarray) -> Metric3:
        return (
            float(array[0]),
            float(array[1]),
            float(array[2]),
        )

    def matrix3(array: np.ndarray) -> Matrix3:
        return (
            (
                float(array[0, 0]),
                float(array[0, 1]),
                float(array[0, 2]),
            ),
            (
                float(array[1, 0]),
                float(array[1, 1]),
                float(array[1, 2]),
            ),
            (
                float(array[2, 0]),
                float(array[2, 1]),
                float(array[2, 2]),
            ),
        )

    return InitialMetricFixedPointCertificate(
        initial_state=matching.initial_state,
        phi_metric=float(metric_solution[0]),
        phi_metric_n=float(metric_solution[1]),
        psi_metric=float(metric_solution[2]),
        reconstructed_phi_metric=float(reconstructed_metric[0]),
        reconstructed_phi_metric_n=float(
            reconstructed_metric[1]
        ),
        reconstructed_psi_metric=float(
            reconstructed_metric[2]
        ),
        fixed_point_residual=vector3(
            fixed_point_residual_array
        ),
        maximum_fixed_point_residual=(
            maximum_fixed_point_residual
        ),
        affine_offset=vector3(affine_offset_array),
        affine_matrix=matrix3(affine_matrix_array),
        affine_probe_residual=vector3(
            affine_probe_residual_array
        ),
        maximum_affine_probe_residual=(
            maximum_affine_probe_residual
        ),
        fixed_point_matrix=matrix3(
            fixed_point_matrix_array
        ),
        fixed_point_matrix_determinant=determinant,
        fixed_point_matrix_condition_number=condition_number,
        matching_surface_closed=matching.matching_surface_closed,
        instantaneous_rhs_closed=(
            rhs.instantaneous_dark_sector_rhs_closed
        ),
        affine_metric_map_verified=affine_metric_map_verified,
        unique_fixed_point_verified=unique_fixed_point_verified,
        initial_metric_fixed_point_solved=(
            initial_metric_fixed_point_solved
        ),
        time_dependent_full_field_evolution_solved=False,
        observational_calibration_completed=False,
    )
