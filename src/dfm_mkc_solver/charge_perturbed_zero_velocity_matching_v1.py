"""Charge-perturbed matching on the zero-radial-velocity circular slice."""

from __future__ import annotations

from dataclasses import dataclass
import math
import numpy as np
from scipy.optimize import least_squares

from .dark_sector_fourier_rhs_v1 import (
    dark_sector_fourier_right_hand_side,
)
from .dark_sector_stress_energy_perturbations_v1 import (
    dark_sector_stress_energy_perturbations,
)


State4 = tuple[float, float, float, float]
Vector3 = tuple[float, float, float]
Vector4 = tuple[float, float, float, float]


@dataclass(frozen=True)
class ChargePerturbedZeroVelocityMatchingCertificate:
    initial_state: State4
    target_density_contrast: float
    selected_density_contrast_n: float
    selected_growth_rate: float
    phi_metric: float
    phi_metric_n: float
    psi_metric: float
    delta_phi: float
    delta_phi_prime: float
    delta_theta: float
    delta_theta_prime: float
    metric_residuals: Vector3
    matching_residuals: Vector4
    maximum_metric_residual: float
    maximum_matching_residual: float
    jacobian_singular_values: Vector3
    jacobian_rank: int
    jacobian_condition_number: float
    constraint_denominator: float
    background_pressure_residual: float
    circular_force_residual: float
    charge_perturbed_circular_tangent_imposed: bool
    zero_radial_velocity_branch_imposed: bool
    metric_constraints_solved: bool
    matching_surface_closed: bool
    instantaneous_rhs_closed: bool


def _require_finite(name: str, value: float) -> None:
    if not math.isfinite(value):
        raise ValueError(f"{name} must be finite")


def _solve_charge_perturbed_zero_velocity_matching_k_squared_impl(
    *,
    scale_factor: float,
    conformal_hubble: float,
    wave_number_squared: float,
    gravitational_constant: float,
    phi_background: float,
    phi_prime_background: float,
    theta_prime_background: float,
    target_density_contrast: float,
    alpha: float,
    beta: float,
    rho_star: float,
    m_phi_squared: float,
    lambda_phi: float,
    branch_tolerance: float = 1.0e-10,
    residual_tolerance: float = 1.0e-9,
    rank_tolerance: float | None = None,
) -> ChargePerturbedZeroVelocityMatchingCertificate:
    """Solve the rank-three circular-tangent initial matching system."""

    from dfm_mkc_solver.dark_sector_fourier_rhs_v1 import (
        dark_sector_fourier_right_hand_side_k_squared,
    )
    from dfm_mkc_solver.dark_sector_stress_energy_perturbations_v1 import (
        dark_sector_stress_energy_perturbations_k_squared,
    )

    for name, value in (
        ("scale_factor", scale_factor),
        ("conformal_hubble", conformal_hubble),
        ("wave_number_squared", wave_number_squared),
        ("gravitational_constant", gravitational_constant),
        ("phi_background", phi_background),
        ("phi_prime_background", phi_prime_background),
        ("theta_prime_background", theta_prime_background),
        ("target_density_contrast", target_density_contrast),
        ("alpha", alpha),
        ("beta", beta),
        ("rho_star", rho_star),
        ("m_phi_squared", m_phi_squared),
        ("lambda_phi", lambda_phi),
        ("branch_tolerance", branch_tolerance),
        ("residual_tolerance", residual_tolerance),
    ):
        _require_finite(name, value)

    if scale_factor <= 0.0:
        raise ValueError("scale_factor must be positive")
    if conformal_hubble <= 0.0:
        raise ValueError("conformal_hubble must be positive")
    if wave_number_squared < 0.0:
        raise ValueError(
            "wave_number_squared must be nonnegative"
        )
    if gravitational_constant <= 0.0:
        raise ValueError("gravitational_constant must be positive")
    if alpha <= 0.0:
        raise ValueError("alpha must be positive")
    if beta <= 0.0:
        raise ValueError("beta must be positive")
    if branch_tolerance <= 0.0:
        raise ValueError("branch_tolerance must be positive")
    if residual_tolerance <= 0.0:
        raise ValueError("residual_tolerance must be positive")
    if abs(phi_background) <= branch_tolerance:
        raise ValueError("phi_background must be nonzero")
    if abs(theta_prime_background) <= branch_tolerance:
        raise ValueError("theta_prime_background must be nonzero")
    if abs(phi_prime_background) > branch_tolerance:
        raise ValueError(
            "phi_prime_background must vanish on the selected branch"
        )
    if abs(target_density_contrast) <= branch_tolerance:
        raise ValueError("target_density_contrast must be nonzero")

    background = dark_sector_stress_energy_perturbations_k_squared(
        scale_factor=scale_factor,
        wave_number_squared=wave_number_squared,
        phi_background=phi_background,
        phi_prime_background=phi_prime_background,
        theta_prime_background=theta_prime_background,
        delta_phi=0.0,
        delta_phi_prime=0.0,
        delta_theta=0.0,
        delta_theta_prime=0.0,
        psi_metric=0.0,
        alpha=alpha,
        beta=beta,
        rho_star=rho_star,
        m_phi_squared=m_phi_squared,
        lambda_phi=lambda_phi,
    )

    if background.background_energy_density <= 0.0:
        raise ValueError("background energy density must be positive")
    if abs(background.potential_slope) <= branch_tolerance:
        raise ValueError("potential slope must be nonzero")

    circular_force_residual = (
        background.potential_slope
        - beta
        * phi_background
        * theta_prime_background**2
        / scale_factor**2
    )
    background_pressure_residual = background.background_pressure

    if abs(circular_force_residual) > branch_tolerance:
        raise ValueError("background is not on the circular-force surface")
    if abs(background_pressure_residual) > branch_tolerance:
        raise ValueError("background is not pressureless")

    target_delta_rho = (
        background.background_energy_density
        * target_density_contrast
    )
    delta_phi = (
        target_delta_rho
        / (2.0 * background.potential_slope)
    )
    phi_metric = 0.0

    def evaluate(
        normalized_coordinates: np.ndarray,
    ) -> tuple[
        object,
        float,
        float,
        float,
        State4,
        np.ndarray,
        np.ndarray,
    ]:
        phi_metric_n = (
            float(normalized_coordinates[0])
            * target_density_contrast
        )
        psi_metric = (
            float(normalized_coordinates[1])
            * target_density_contrast
        )
        normalized_momentum_potential = float(
            normalized_coordinates[2]
        )
        momentum_potential_scale = (
            background.background_energy_density
            * target_density_contrast
            / conformal_hubble
        )
        target_momentum_potential = (
            normalized_momentum_potential
            * momentum_potential_scale
        )
        target_density_contrast_n = (
            3.0 * phi_metric_n
            - wave_number_squared
            * target_momentum_potential
            / (
                conformal_hubble
                * background.background_energy_density
            )
        )

        delta_phi_prime = (
            0.5
            * phi_prime_background
            * target_density_contrast
            + 0.5
            * phi_background
            * conformal_hubble
            * target_density_contrast_n
        )

        delta_theta = (
            scale_factor**2 * target_momentum_potential
            - alpha * phi_prime_background * delta_phi
        ) / (
            beta
            * phi_background**2
            * theta_prime_background
        )

        delta_theta_prime = (
            theta_prime_background * psi_metric
        )

        state: State4 = (
            delta_phi,
            delta_phi_prime,
            delta_theta,
            delta_theta_prime,
        )

        rhs = dark_sector_fourier_right_hand_side_k_squared(
            scale_factor=scale_factor,
            conformal_hubble=conformal_hubble,
            wave_number_squared=wave_number_squared,
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
        )

        source = rhs.stress_energy

        reconstructed_density_contrast = (
            source.delta_energy_density
            / source.background_energy_density
        )
        reconstructed_density_contrast_n = (
            -wave_number_squared
            * source.momentum_potential
            / (
                conformal_hubble
                * source.background_energy_density
            )
            + 3.0 * phi_metric_n
        )

        normalized_current_fraction = (
            (
                delta_theta_prime
                + 2.0
                * theta_prime_background
                * delta_phi
                / phi_background
                - theta_prime_background
                * (psi_metric + 3.0 * phi_metric)
            )
            / theta_prime_background
        )

        metric_residuals = np.asarray(
            [
                rhs.metric_constraints.phi - phi_metric,
                (
                    rhs.metric_constraints.phi_prime
                    / conformal_hubble
                    - phi_metric_n
                ),
                rhs.metric_constraints.psi - psi_metric,
            ],
            dtype=float,
        )

        matching_residuals = np.asarray(
            [
                (
                    reconstructed_density_contrast
                    - target_density_contrast
                ),
                (
                    reconstructed_density_contrast_n
                    - target_density_contrast_n
                ),
                (
                    source.delta_pressure
                    / source.background_energy_density
                ),
                (
                    normalized_current_fraction
                    - target_density_contrast
                ),
            ],
            dtype=float,
        )

        return (
            rhs,
            phi_metric_n,
            psi_metric,
            target_density_contrast_n,
            state,
            metric_residuals,
            matching_residuals,
        )

    def normalized_metric_residual(
        coordinates: np.ndarray,
    ) -> np.ndarray:
        return (
            evaluate(coordinates)[5]
            / target_density_contrast
        )

    solution = least_squares(
        normalized_metric_residual,
        x0=np.asarray([-1.0 / 6.0, 0.0, 0.0], dtype=float),
        x_scale="jac",
        xtol=1.0e-14,
        ftol=1.0e-14,
        gtol=1.0e-14,
        max_nfev=10000,
    )

    (
        rhs,
        phi_metric_n,
        psi_metric,
        target_density_contrast_n,
        state,
        metric_residual_array,
        matching_residual_array,
    ) = evaluate(solution.x)

    singular_values_array = np.linalg.svd(
        np.asarray(solution.jac, dtype=float),
        compute_uv=False,
    )

    if rank_tolerance is None:
        rank_tolerance = (
            max(solution.jac.shape)
            * np.finfo(float).eps
            * singular_values_array[0]
        )

    _require_finite("rank_tolerance", rank_tolerance)

    if rank_tolerance < 0.0:
        raise ValueError("rank_tolerance must be nonnegative")

    jacobian_rank = int(
        np.sum(singular_values_array > rank_tolerance)
    )
    jacobian_condition_number = float(
        singular_values_array[0]
        / singular_values_array[-1]
    )

    maximum_metric_residual = float(
        np.max(np.abs(metric_residual_array))
    )
    maximum_matching_residual = float(
        np.max(np.abs(matching_residual_array))
    )

    if jacobian_rank != 3:
        raise ValueError(
            "matching Jacobian must have rank three"
        )
    if maximum_metric_residual > residual_tolerance:
        raise ValueError("metric constraints failed closure")
    if maximum_matching_residual > residual_tolerance:
        raise ValueError("matching equations failed closure")
    if not rhs.instantaneous_dark_sector_rhs_closed:
        raise ValueError("instantaneous Fourier RHS failed closure")

    selected_growth_rate = (
        target_density_contrast_n
        / target_density_contrast
    )

    return ChargePerturbedZeroVelocityMatchingCertificate(
        initial_state=state,
        target_density_contrast=target_density_contrast,
        selected_density_contrast_n=(
            target_density_contrast_n
        ),
        selected_growth_rate=selected_growth_rate,
        phi_metric=phi_metric,
        phi_metric_n=phi_metric_n,
        psi_metric=psi_metric,
        delta_phi=state[0],
        delta_phi_prime=state[1],
        delta_theta=state[2],
        delta_theta_prime=state[3],
        metric_residuals=tuple(
            float(value) for value in metric_residual_array
        ),
        matching_residuals=tuple(
            float(value) for value in matching_residual_array
        ),
        maximum_metric_residual=maximum_metric_residual,
        maximum_matching_residual=maximum_matching_residual,
        jacobian_singular_values=tuple(
            float(value) for value in singular_values_array
        ),
        jacobian_rank=jacobian_rank,
        jacobian_condition_number=(
            jacobian_condition_number
        ),
        constraint_denominator=float(
            rhs.constraint_denominator
        ),
        background_pressure_residual=(
            background_pressure_residual
        ),
        circular_force_residual=circular_force_residual,
        charge_perturbed_circular_tangent_imposed=True,
        zero_radial_velocity_branch_imposed=True,
        metric_constraints_solved=True,
        matching_surface_closed=True,
        instantaneous_rhs_closed=True,
    )


def solve_charge_perturbed_zero_velocity_matching(
    *,
    scale_factor: float,
    conformal_hubble: float,
    wave_number: float,
    gravitational_constant: float,
    phi_background: float,
    phi_prime_background: float,
    theta_prime_background: float,
    target_density_contrast: float,
    alpha: float,
    beta: float,
    rho_star: float,
    m_phi_squared: float,
    lambda_phi: float,
    branch_tolerance: float = 1.0e-10,
    residual_tolerance: float = 1.0e-9,
    rank_tolerance: float | None = None,
) -> ChargePerturbedZeroVelocityMatchingCertificate:
    """Solve the matching system using the legacy k surface."""

    _require_finite("wave_number", wave_number)
    if wave_number < 0.0:
        raise ValueError("wave_number must be nonnegative")

    return _solve_charge_perturbed_zero_velocity_matching_k_squared_impl(
        scale_factor=scale_factor,
        conformal_hubble=conformal_hubble,
        wave_number_squared=wave_number**2,
        gravitational_constant=gravitational_constant,
        phi_background=phi_background,
        phi_prime_background=phi_prime_background,
        theta_prime_background=theta_prime_background,
        target_density_contrast=target_density_contrast,
        alpha=alpha,
        beta=beta,
        rho_star=rho_star,
        m_phi_squared=m_phi_squared,
        lambda_phi=lambda_phi,
        branch_tolerance=branch_tolerance,
        residual_tolerance=residual_tolerance,
        rank_tolerance=rank_tolerance,
    )


def solve_charge_perturbed_zero_velocity_matching_k_squared(
    *,
    scale_factor: float,
    conformal_hubble: float,
    wave_number_squared: float,
    gravitational_constant: float,
    phi_background: float,
    phi_prime_background: float,
    theta_prime_background: float,
    target_density_contrast: float,
    alpha: float,
    beta: float,
    rho_star: float,
    m_phi_squared: float,
    lambda_phi: float,
    branch_tolerance: float = 1.0e-10,
    residual_tolerance: float = 1.0e-9,
    rank_tolerance: float | None = None,
) -> ChargePerturbedZeroVelocityMatchingCertificate:
    """Solve the matching system directly in x = k^2."""

    return _solve_charge_perturbed_zero_velocity_matching_k_squared_impl(
        scale_factor=scale_factor,
        conformal_hubble=conformal_hubble,
        wave_number_squared=wave_number_squared,
        gravitational_constant=gravitational_constant,
        phi_background=phi_background,
        phi_prime_background=phi_prime_background,
        theta_prime_background=theta_prime_background,
        target_density_contrast=target_density_contrast,
        alpha=alpha,
        beta=beta,
        rho_star=rho_star,
        m_phi_squared=m_phi_squared,
        lambda_phi=lambda_phi,
        branch_tolerance=branch_tolerance,
        residual_tolerance=residual_tolerance,
        rank_tolerance=rank_tolerance,
    )

from typing import NamedTuple as _NamedTuple


class ChargePerturbedZeroVelocityImplicitTangentCertificate(
    _NamedTuple
):
    normalized_coordinates_at_zero: tuple[float, float, float]
    normalized_metric_residuals_at_zero: tuple[
        float,
        float,
        float,
    ]
    jacobian_z: tuple[
        tuple[float, float, float],
        tuple[float, float, float],
        tuple[float, float, float],
    ]
    forcing_x: tuple[float, float, float]
    normalized_coordinate_tangent: tuple[
        float,
        float,
        float,
    ]
    implicit_residual: tuple[float, float, float]
    growth_tangent: float
    direct_growth_tangent: float
    growth_tangent_difference: float
    forcing_refinement_difference: float
    coordinate_affine_defect: float
    jacobian_rank: int
    jacobian_condition_number: float
    wave_number_squared_step: float


def evaluate_charge_perturbed_zero_velocity_matching_residuals_k_squared(
    *,
    normalized_coordinates: tuple[float, float, float],
    scale_factor: float,
    conformal_hubble: float,
    wave_number_squared: float,
    gravitational_constant: float,
    phi_background: float,
    phi_prime_background: float,
    theta_prime_background: float,
    target_density_contrast: float,
    alpha: float,
    beta: float,
    rho_star: float,
    m_phi_squared: float,
    lambda_phi: float,
    branch_tolerance: float = 1.0e-10,
) -> tuple[float, float, float]:
    """Evaluate F(z, x), the three normalized metric residuals."""

    from dfm_mkc_solver.dark_sector_fourier_rhs_v1 import (
        dark_sector_fourier_right_hand_side_k_squared,
    )
    from dfm_mkc_solver.dark_sector_stress_energy_perturbations_v1 import (
        dark_sector_stress_energy_perturbations_k_squared,
    )

    if len(normalized_coordinates) != 3:
        raise ValueError(
            "normalized_coordinates must contain three values"
        )

    (
        normalized_phi_metric_n,
        normalized_psi_metric,
        normalized_momentum_potential,
    ) = (
        float(normalized_coordinates[0]),
        float(normalized_coordinates[1]),
        float(normalized_coordinates[2]),
    )

    for name, value in (
        ("normalized_phi_metric_n", normalized_phi_metric_n),
        ("normalized_psi_metric", normalized_psi_metric),
        (
            "normalized_momentum_potential",
            normalized_momentum_potential,
        ),
        ("scale_factor", scale_factor),
        ("conformal_hubble", conformal_hubble),
        ("wave_number_squared", wave_number_squared),
        ("gravitational_constant", gravitational_constant),
        ("phi_background", phi_background),
        ("phi_prime_background", phi_prime_background),
        ("theta_prime_background", theta_prime_background),
        ("target_density_contrast", target_density_contrast),
        ("alpha", alpha),
        ("beta", beta),
        ("rho_star", rho_star),
        ("m_phi_squared", m_phi_squared),
        ("lambda_phi", lambda_phi),
        ("branch_tolerance", branch_tolerance),
    ):
        _require_finite(name, value)

    if scale_factor <= 0.0:
        raise ValueError("scale_factor must be positive")
    if conformal_hubble <= 0.0:
        raise ValueError("conformal_hubble must be positive")
    if wave_number_squared < 0.0:
        raise ValueError(
            "wave_number_squared must be nonnegative"
        )
    if gravitational_constant <= 0.0:
        raise ValueError(
            "gravitational_constant must be positive"
        )
    if alpha <= 0.0:
        raise ValueError("alpha must be positive")
    if beta <= 0.0:
        raise ValueError("beta must be positive")
    if branch_tolerance <= 0.0:
        raise ValueError("branch_tolerance must be positive")
    if abs(phi_background) <= branch_tolerance:
        raise ValueError("phi_background must be nonzero")
    if abs(theta_prime_background) <= branch_tolerance:
        raise ValueError(
            "theta_prime_background must be nonzero"
        )
    if abs(phi_prime_background) > branch_tolerance:
        raise ValueError(
            "phi_prime_background must vanish on the selected branch"
        )
    if abs(target_density_contrast) <= branch_tolerance:
        raise ValueError(
            "target_density_contrast must be nonzero"
        )

    background = (
        dark_sector_stress_energy_perturbations_k_squared(
            scale_factor=scale_factor,
            wave_number_squared=wave_number_squared,
            phi_background=phi_background,
            phi_prime_background=phi_prime_background,
            theta_prime_background=theta_prime_background,
            delta_phi=0.0,
            delta_phi_prime=0.0,
            delta_theta=0.0,
            delta_theta_prime=0.0,
            psi_metric=0.0,
            alpha=alpha,
            beta=beta,
            rho_star=rho_star,
            m_phi_squared=m_phi_squared,
            lambda_phi=lambda_phi,
        )
    )

    if background.background_energy_density <= 0.0:
        raise ValueError(
            "background energy density must be positive"
        )
    if abs(background.potential_slope) <= branch_tolerance:
        raise ValueError("potential slope must be nonzero")

    circular_force_residual = (
        background.potential_slope
        - beta
        * phi_background
        * theta_prime_background**2
        / scale_factor**2
    )

    if abs(circular_force_residual) > branch_tolerance:
        raise ValueError(
            "background is not on the circular-force surface"
        )
    if abs(background.background_pressure) > branch_tolerance:
        raise ValueError("background is not pressureless")

    target_delta_rho = (
        background.background_energy_density
        * target_density_contrast
    )

    delta_phi = (
        target_delta_rho
        / (2.0 * background.potential_slope)
    )

    phi_metric = 0.0

    phi_metric_n = (
        normalized_phi_metric_n
        * target_density_contrast
    )

    psi_metric = (
        normalized_psi_metric
        * target_density_contrast
    )

    momentum_potential_scale = (
        background.background_energy_density
        * target_density_contrast
        / conformal_hubble
    )

    target_momentum_potential = (
        normalized_momentum_potential
        * momentum_potential_scale
    )

    target_density_contrast_n = (
        3.0 * phi_metric_n
        - wave_number_squared
        * target_momentum_potential
        / (
            conformal_hubble
            * background.background_energy_density
        )
    )

    delta_phi_prime = (
        0.5
        * phi_prime_background
        * target_density_contrast
        + 0.5
        * phi_background
        * conformal_hubble
        * target_density_contrast_n
    )

    delta_theta = (
        scale_factor**2 * target_momentum_potential
        - alpha * phi_prime_background * delta_phi
    ) / (
        beta
        * phi_background**2
        * theta_prime_background
    )

    delta_theta_prime = (
        theta_prime_background * psi_metric
    )

    rhs = dark_sector_fourier_right_hand_side_k_squared(
        scale_factor=scale_factor,
        conformal_hubble=conformal_hubble,
        wave_number_squared=wave_number_squared,
        gravitational_constant=gravitational_constant,
        phi_background=phi_background,
        phi_prime_background=phi_prime_background,
        theta_prime_background=theta_prime_background,
        delta_phi=delta_phi,
        delta_phi_prime=delta_phi_prime,
        delta_theta=delta_theta,
        delta_theta_prime=delta_theta_prime,
        alpha=alpha,
        beta=beta,
        rho_star=rho_star,
        m_phi_squared=m_phi_squared,
        lambda_phi=lambda_phi,
    )

    residuals = (
        (
            rhs.metric_constraints.phi
            - phi_metric
        ) / target_density_contrast,
        (
            rhs.metric_constraints.phi_prime
            / conformal_hubble
            - phi_metric_n
        ) / target_density_contrast,
        (
            rhs.metric_constraints.psi
            - psi_metric
        ) / target_density_contrast,
    )

    for index, value in enumerate(residuals):
        _require_finite(
            f"normalized_metric_residual_{index}",
            value,
        )

    return tuple(float(value) for value in residuals)


def solve_charge_perturbed_zero_velocity_matching_implicit_tangent_k_squared(
    *,
    scale_factor: float,
    conformal_hubble: float,
    gravitational_constant: float,
    phi_background: float,
    phi_prime_background: float,
    theta_prime_background: float,
    target_density_contrast: float,
    alpha: float,
    beta: float,
    rho_star: float,
    m_phi_squared: float,
    lambda_phi: float,
    branch_tolerance: float = 1.0e-10,
    residual_tolerance: float = 1.0e-9,
    rank_tolerance: float | None = None,
    wave_number_squared_step: float | None = None,
) -> ChargePerturbedZeroVelocityImplicitTangentCertificate:
    """Solve J_z z_x = -F_x at x = k^2 = 0."""

    import numpy as np

    from dfm_mkc_solver.dark_sector_stress_energy_perturbations_v1 import (
        dark_sector_stress_energy_perturbations_k_squared,
    )

    if wave_number_squared_step is None:
        wave_number_squared_step = (
            1.0e-4 * conformal_hubble**2
        )

    _require_finite(
        "wave_number_squared_step",
        wave_number_squared_step,
    )

    if wave_number_squared_step <= 0.0:
        raise ValueError(
            "wave_number_squared_step must be positive"
        )

    common = dict(
        scale_factor=scale_factor,
        conformal_hubble=conformal_hubble,
        gravitational_constant=gravitational_constant,
        phi_background=phi_background,
        phi_prime_background=phi_prime_background,
        theta_prime_background=theta_prime_background,
        target_density_contrast=target_density_contrast,
        alpha=alpha,
        beta=beta,
        rho_star=rho_star,
        m_phi_squared=m_phi_squared,
        lambda_phi=lambda_phi,
        branch_tolerance=branch_tolerance,
        residual_tolerance=residual_tolerance,
        rank_tolerance=rank_tolerance,
    )

    zero_certificate = (
        solve_charge_perturbed_zero_velocity_matching_k_squared(
            wave_number_squared=0.0,
            **common,
        )
    )

    background = (
        dark_sector_stress_energy_perturbations_k_squared(
            scale_factor=scale_factor,
            wave_number_squared=0.0,
            phi_background=phi_background,
            phi_prime_background=phi_prime_background,
            theta_prime_background=theta_prime_background,
            delta_phi=0.0,
            delta_phi_prime=0.0,
            delta_theta=0.0,
            delta_theta_prime=0.0,
            psi_metric=0.0,
            alpha=alpha,
            beta=beta,
            rho_star=rho_star,
            m_phi_squared=m_phi_squared,
            lambda_phi=lambda_phi,
        )
    )

    momentum_potential_scale = (
        background.background_energy_density
        * target_density_contrast
        / conformal_hubble
    )

    selected_momentum_potential = (
        alpha
        * phi_prime_background
        * zero_certificate.delta_phi
        + beta
        * phi_background**2
        * theta_prime_background
        * zero_certificate.delta_theta
    ) / scale_factor**2

    normalized_coordinates = np.asarray(
        (
            zero_certificate.phi_metric_n
            / target_density_contrast,
            zero_certificate.psi_metric
            / target_density_contrast,
            selected_momentum_potential
            / momentum_potential_scale,
        ),
        dtype=float,
    )

    residual_common = dict(
        scale_factor=scale_factor,
        conformal_hubble=conformal_hubble,
        gravitational_constant=gravitational_constant,
        phi_background=phi_background,
        phi_prime_background=phi_prime_background,
        theta_prime_background=theta_prime_background,
        target_density_contrast=target_density_contrast,
        alpha=alpha,
        beta=beta,
        rho_star=rho_star,
        m_phi_squared=m_phi_squared,
        lambda_phi=lambda_phi,
        branch_tolerance=branch_tolerance,
    )

    def residual(
        coordinates: np.ndarray,
        wave_number_squared: float,
    ) -> np.ndarray:
        return np.asarray(
            evaluate_charge_perturbed_zero_velocity_matching_residuals_k_squared(
                normalized_coordinates=tuple(
                    float(value) for value in coordinates
                ),
                wave_number_squared=wave_number_squared,
                **residual_common,
            ),
            dtype=float,
        )

    residual_zero = residual(
        normalized_coordinates,
        0.0,
    )

    jacobian_columns = []
    coordinate_affine_defects = []

    for index in range(3):
        direction = np.zeros(3, dtype=float)
        direction[index] = 1.0

        plus = residual(
            normalized_coordinates + direction,
            0.0,
        )
        minus = residual(
            normalized_coordinates - direction,
            0.0,
        )

        jacobian_columns.append(
            0.5 * (plus - minus)
        )

        coordinate_affine_defects.append(
            float(
                np.linalg.norm(
                    plus + minus - 2.0 * residual_zero,
                    ord=np.inf,
                )
            )
        )

    jacobian_z = np.column_stack(
        jacobian_columns
    )

    def forward_five_point(step: float) -> np.ndarray:
        values = [
            residual(
                normalized_coordinates,
                multiplier * step,
            )
            for multiplier in range(5)
        ]

        return (
            -25.0 * values[0]
            + 48.0 * values[1]
            - 36.0 * values[2]
            + 16.0 * values[3]
            - 3.0 * values[4]
        ) / (12.0 * step)

    forcing_coarse = forward_five_point(
        wave_number_squared_step
    )
    forcing_fine = forward_five_point(
        wave_number_squared_step / 2.0
    )

    forcing_x = forcing_fine

    forcing_refinement_difference = float(
        np.linalg.norm(
            forcing_fine - forcing_coarse,
            ord=np.inf,
        )
    )

    normalized_coordinate_tangent = np.linalg.solve(
        jacobian_z,
        -forcing_x,
    )

    implicit_residual = (
        jacobian_z @ normalized_coordinate_tangent
        + forcing_x
    )

    growth_tangent = float(
        3.0 * normalized_coordinate_tangent[0]
        - normalized_coordinates[2]
        / conformal_hubble**2
    )

    coarse_certificate = (
        solve_charge_perturbed_zero_velocity_matching_k_squared(
            wave_number_squared=wave_number_squared_step,
            **common,
        )
    )

    fine_certificate = (
        solve_charge_perturbed_zero_velocity_matching_k_squared(
            wave_number_squared=(
                wave_number_squared_step / 2.0
            ),
            **common,
        )
    )

    coarse_growth_tangent = (
        coarse_certificate.selected_growth_rate
        - zero_certificate.selected_growth_rate
    ) / wave_number_squared_step

    fine_growth_tangent = (
        fine_certificate.selected_growth_rate
        - zero_certificate.selected_growth_rate
    ) / (
        wave_number_squared_step / 2.0
    )

    direct_growth_tangent = float(
        2.0 * fine_growth_tangent
        - coarse_growth_tangent
    )

    growth_tangent_difference = abs(
        growth_tangent - direct_growth_tangent
    )

    singular_values = np.linalg.svd(
        jacobian_z,
        compute_uv=False,
    )

    if rank_tolerance is None:
        effective_rank_tolerance = (
            max(jacobian_z.shape)
            * np.finfo(float).eps
            * singular_values[0]
        )
    else:
        effective_rank_tolerance = rank_tolerance

    jacobian_rank = int(
        np.sum(
            singular_values
            > effective_rank_tolerance
        )
    )

    jacobian_condition_number = float(
        singular_values[0] / singular_values[-1]
    )

    arrays = (
        residual_zero,
        jacobian_z,
        forcing_x,
        normalized_coordinate_tangent,
        implicit_residual,
    )

    if not all(
        np.all(np.isfinite(array))
        for array in arrays
    ):
        raise ValueError(
            "implicit tangent arrays must be finite"
        )

    for name, value in (
        ("growth_tangent", growth_tangent),
        (
            "direct_growth_tangent",
            direct_growth_tangent,
        ),
        (
            "growth_tangent_difference",
            growth_tangent_difference,
        ),
        (
            "forcing_refinement_difference",
            forcing_refinement_difference,
        ),
        (
            "jacobian_condition_number",
            jacobian_condition_number,
        ),
    ):
        _require_finite(name, value)

    return (
        ChargePerturbedZeroVelocityImplicitTangentCertificate(
            normalized_coordinates_at_zero=tuple(
                float(value)
                for value in normalized_coordinates
            ),
            normalized_metric_residuals_at_zero=tuple(
                float(value) for value in residual_zero
            ),
            jacobian_z=tuple(
                tuple(float(value) for value in row)
                for row in jacobian_z
            ),
            forcing_x=tuple(
                float(value) for value in forcing_x
            ),
            normalized_coordinate_tangent=tuple(
                float(value)
                for value in normalized_coordinate_tangent
            ),
            implicit_residual=tuple(
                float(value) for value in implicit_residual
            ),
            growth_tangent=growth_tangent,
            direct_growth_tangent=direct_growth_tangent,
            growth_tangent_difference=(
                growth_tangent_difference
            ),
            forcing_refinement_difference=(
                forcing_refinement_difference
            ),
            coordinate_affine_defect=max(
                coordinate_affine_defects
            ),
            jacobian_rank=jacobian_rank,
            jacobian_condition_number=(
                jacobian_condition_number
            ),
            wave_number_squared_step=(
                wave_number_squared_step
            ),
        )
    )
