"""Locally selected regular-growing-mode initial data.

The construction freezes the action-derived, metric-eliminated Fourier
system at one background point.  It is therefore a local numerical mode
certificate, not a proof of global uniqueness or early-time regularity.
"""

from __future__ import annotations

import math
from dataclasses import dataclass

import mpmath
import numpy as np

from .dark_sector_fourier_rhs_v1 import (
    dark_sector_fourier_right_hand_side,
)

State4 = tuple[float, float, float, float]
Matrix4 = tuple[State4, State4, State4, State4]
Matrix3x4 = tuple[State4, State4, State4]
VARIABLE_ORDER = (
    "delta_phi",
    "delta_phi_prime",
    "delta_theta",
    "delta_theta_prime",
)


@dataclass(frozen=True)
class RegularGrowingModeInitialStateCertificate:
    source_log_scale_factor: float
    variable_order: tuple[str, str, str, str]
    linear_operator: Matrix4
    eigenvalues: tuple[complex, complex, complex, complex]
    selected_eigenvalue: float
    selected_eigenvector: State4
    eigenpair_residual: float
    spectral_gap: float
    pivot_index: int
    pivot_absolute_value: float
    boundary_matrix: Matrix3x4
    rank_minor: float
    certified_rank: int
    nullity: int
    maximum_boundary_residual: float
    local_regular_growing_mode_selected: bool
    exact_rank_proved: bool
    local_numerical_rank_certified: bool
    gauge_status: str
    observational_calibration_completed: bool
    exact_global_uniqueness_proved: bool
    global_early_time_regularity_proved: bool
    initial_state: State4
    derived_density_contrast: float
    derived_density_contrast_n: float
    background_density_n: float
    perturbed_density_n: float
    density_contrast_chain_rule_residual: float
    density_contrast_finite_difference_check: float
    density_contrast_finite_difference_error: float
    density_contrast_finite_difference_coarse_error: float
    density_contrast_finite_difference_converged: bool
    frozen_background_shortcut_error: float
    total_density_derivative_certified: bool
    poisson_residual: float
    momentum_constraint_residual: float
    anisotropy_constraint_residual: float
    metric_closure_residual: float
    density_reconstruction_residual: float
    amplitude_equation_residual: float
    phase_equation_residual: float
    minimum_abs_constraint_denominator: float
    maximum_initial_constraint_residual: float
    metric_constraints_solved: bool
    initial_matching_surface_closed: bool
    maximum_linearity_residual: float
    arithmetic_precision_decimal_digits: int


def construct_regular_growing_mode_initial_state(
    *,
    source_log_scale_factor: float,
    scale_factor: float,
    conformal_hubble: float,
    wave_number: float,
    gravitational_constant: float,
    phi_background: float,
    phi_prime_background: float,
    theta_prime_background: float,
    cosmic_hubble_n: float,
    alpha: float,
    beta: float,
    rho_star: float,
    m_phi_squared: float,
    lambda_phi: float,
    amplitude: float = 1.0e-6,
    denominator_tolerance: float = 1.0e-14,
    reality_tolerance: float = 1.0e-10,
    spectral_gap_tolerance: float = 1.0e-10,
    eigenpair_residual_tolerance: float = 1.0e-10,
    linearity_tolerance: float = 2.0e-12,
    rank_tolerance: float = 1.0e-12,
    constraint_tolerance: float = 1.0e-10,
    density_derivative_tolerance: float = 2.0e-8,
    finite_difference_step: float = 2.0e-5,
    precision_decimal_digits: int = 80,
) -> RegularGrowingModeInitialStateCertificate:
    """Construct the dominant local mode ray and its three constraints."""
    if conformal_hubble <= 0.0:
        raise ValueError("conformal_hubble must be positive")
    if not math.isfinite(amplitude) or amplitude == 0.0:
        raise ValueError("amplitude must be finite and nonzero")
    if precision_decimal_digits < 30:
        raise ValueError("precision_decimal_digits must be at least 30")
    if not math.isfinite(cosmic_hubble_n):
        raise ValueError("cosmic_hubble_n must be finite")
    if finite_difference_step <= 0.0:
        raise ValueError("finite_difference_step must be positive")

    def rhs(state: np.ndarray) -> np.ndarray:
        certificate = dark_sector_fourier_right_hand_side(
            scale_factor=scale_factor,
            conformal_hubble=conformal_hubble,
            wave_number=wave_number,
            gravitational_constant=gravitational_constant,
            phi_background=phi_background,
            phi_prime_background=phi_prime_background,
            theta_prime_background=theta_prime_background,
            delta_phi=float(state[0]),
            delta_phi_prime=float(state[1]),
            delta_theta=float(state[2]),
            delta_theta_prime=float(state[3]),
            alpha=alpha,
            beta=beta,
            rho_star=rho_star,
            m_phi_squared=m_phi_squared,
            lambda_phi=lambda_phi,
            denominator_tolerance=denominator_tolerance,
        )
        return np.asarray(
            (
                state[1] / conformal_hubble,
                certificate.delta_phi_double_prime / conformal_hubble,
                state[3] / conformal_hubble,
                certificate.delta_theta_double_prime / conformal_hubble,
            ),
            dtype=float,
        )

    basis = np.eye(4, dtype=float)
    operator = np.column_stack([rhs(vector) for vector in basis])
    zero_residual = float(np.linalg.norm(rhs(np.zeros(4)), ord=np.inf))
    y = np.asarray((0.37, -0.23, 0.41, 0.19))
    z = np.asarray((-0.11, 0.29, 0.07, -0.31))
    c = -1.7
    scale_residual = float(
        np.linalg.norm(rhs(c * y) - c * rhs(y), ord=np.inf)
    )
    add_residual = float(
        np.linalg.norm(rhs(y + z) - rhs(y) - rhs(z), ord=np.inf)
    )
    maximum_linearity_residual = max(
        zero_residual, scale_residual, add_residual
    )
    linearity_scale = max(
        1.0,
        float(np.linalg.norm(rhs(y), ord=np.inf)),
        float(np.linalg.norm(rhs(z), ord=np.inf)),
    )
    if maximum_linearity_residual > linearity_tolerance * linearity_scale:
        raise RuntimeError("metric-eliminated RHS failed linearity checks")

    with mpmath.workdps(precision_decimal_digits):
        mp_operator = mpmath.matrix(
            [[mpmath.mpf(repr(value)) for value in row] for row in operator]
        )
        mp_values, mp_vectors = mpmath.eig(mp_operator)
        values = np.asarray([complex(value) for value in mp_values])
        selected_index = int(np.argmax(values.real))
        selected_value = values[selected_index]
        vector_complex = np.asarray(
            [complex(mp_vectors[row, selected_index]) for row in range(4)]
        )
        phase_pivot = int(np.argmax(np.abs(vector_complex)))
        vector_complex *= np.exp(
            -1j * np.angle(vector_complex[phase_pivot])
        )

    other_indices = [index for index in range(4) if index != selected_index]
    spectral_gap = float(
        min(
            selected_value.real - values[index].real
            for index in other_indices
        )
    )
    eigenvalue_separation = float(
        min(abs(selected_value - values[index]) for index in other_indices)
    )
    scale = max(1.0, abs(selected_value), float(np.linalg.norm(operator, 2)))
    if abs(selected_value.imag) > reality_tolerance * scale:
        raise RuntimeError("dominant local eigenvalue is not real")
    if spectral_gap <= spectral_gap_tolerance * scale:
        raise RuntimeError("dominant local eigenvalue is not strictly largest")
    if eigenvalue_separation <= spectral_gap_tolerance * scale:
        raise RuntimeError("dominant local eigenvalue is not numerically simple")
    if float(np.linalg.norm(vector_complex)) == 0.0:
        raise RuntimeError("selected eigenvector is zero")
    if np.linalg.norm(vector_complex.imag) > reality_tolerance * max(
        1.0, float(np.linalg.norm(vector_complex.real))
    ):
        raise RuntimeError("selected eigenvector is not numerically real")

    vector = vector_complex.real
    pivot_index = int(np.argmax(np.abs(vector)))
    vector = vector / vector[pivot_index]
    selected_eigenvalue = float(selected_value.real)
    residual_vector = operator @ vector - selected_eigenvalue * vector
    eigenpair_residual = float(
        np.linalg.norm(residual_vector, 2)
        / (
            max(1.0, float(np.linalg.norm(operator, 2)))
            * float(np.linalg.norm(vector, 2))
        )
    )
    if eigenpair_residual > eigenpair_residual_tolerance:
        raise RuntimeError("selected eigenpair residual is too large")

    rows: list[np.ndarray] = []
    nonpivot_indices = [index for index in range(4) if index != pivot_index]
    for index in nonpivot_indices:
        row = np.zeros(4)
        row[index] = vector[pivot_index]
        row[pivot_index] = -vector[index]
        rows.append(row)
    boundary = np.asarray(rows)
    maximum_boundary_residual = float(
        np.linalg.norm(boundary @ vector, ord=np.inf)
    )
    rank_minor = float(
        np.linalg.det(boundary[:, nonpivot_indices])
    )
    expected_minor = float(vector[pivot_index] ** 3)
    certified_rank = int(np.linalg.matrix_rank(boundary, tol=rank_tolerance))
    nullity = 4 - certified_rank
    local_rank_certified = (
        vector[pivot_index] != 0.0
        and math.isclose(
            rank_minor,
            expected_minor,
            rel_tol=rank_tolerance,
            abs_tol=rank_tolerance,
        )
        and certified_rank == 3
        and nullity == 1
        and maximum_boundary_residual <= rank_tolerance
    )
    if not local_rank_certified:
        raise RuntimeError("boundary matrix rank certificate failed")

    initial = amplitude * vector
    initial_rhs = operator @ initial

    def density_contrast(state: np.ndarray) -> float:
        certificate = dark_sector_fourier_right_hand_side(
            scale_factor=scale_factor,
            conformal_hubble=conformal_hubble,
            wave_number=wave_number,
            gravitational_constant=gravitational_constant,
            phi_background=phi_background,
            phi_prime_background=phi_prime_background,
            theta_prime_background=theta_prime_background,
            delta_phi=float(state[0]),
            delta_phi_prime=float(state[1]),
            delta_theta=float(state[2]),
            delta_theta_prime=float(state[3]),
            alpha=alpha,
            beta=beta,
            rho_star=rho_star,
            m_phi_squared=m_phi_squared,
            lambda_phi=lambda_phi,
            denominator_tolerance=denominator_tolerance,
        )
        return float(
            certificate.stress_energy.delta_energy_density
            / certificate.stress_energy.background_energy_density
        )

    initial_certificate = dark_sector_fourier_right_hand_side(
        scale_factor=scale_factor,
        conformal_hubble=conformal_hubble,
        wave_number=wave_number,
        gravitational_constant=gravitational_constant,
        phi_background=phi_background,
        phi_prime_background=phi_prime_background,
        theta_prime_background=theta_prime_background,
        delta_phi=float(initial[0]),
        delta_phi_prime=float(initial[1]),
        delta_theta=float(initial[2]),
        delta_theta_prime=float(initial[3]),
        alpha=alpha,
        beta=beta,
        rho_star=rho_star,
        m_phi_squared=m_phi_squared,
        lambda_phi=lambda_phi,
        denominator_tolerance=denominator_tolerance,
    )

    # Cosmic time, conformal time and e-fold time obey
    # d/deta = a d/dt = Hc d/dN.  The homogeneous conformal equations below
    # are the charge-reduced amplitude equation and conserved phase current.
    potential_slope = (
        m_phi_squared * phi_background
        + lambda_phi * phi_background**3
    )
    phi_background_n = phi_prime_background / conformal_hubble
    phi_prime_background_n = (
        -2.0 * conformal_hubble * phi_prime_background
        + (beta / alpha)
        * phi_background
        * theta_prime_background**2
        - scale_factor**2 * potential_slope / alpha
    ) / conformal_hubble
    theta_prime_background_n = (
        -2.0
        * (
            conformal_hubble
            + phi_prime_background / phi_background
        )
        * theta_prime_background
        / conformal_hubble
    )
    conformal_hubble_n = (
        conformal_hubble
        + scale_factor * cosmic_hubble_n
    )

    class _Dual:
        """Scalar with an explicit analytic N tangent."""

        def __init__(self, value: float, tangent: float = 0.0):
            self.value = float(value)
            self.tangent = float(tangent)

        def __add__(self, other: object) -> _Dual:
            rhs = other if isinstance(other, _Dual) else _Dual(float(other))
            return _Dual(self.value + rhs.value, self.tangent + rhs.tangent)

        __radd__ = __add__

        def __neg__(self) -> _Dual:
            return _Dual(-self.value, -self.tangent)

        def __sub__(self, other: object) -> _Dual:
            return self + (-other if isinstance(other, _Dual) else -float(other))

        def __rsub__(self, other: object) -> _Dual:
            return (-self) + other

        def __mul__(self, other: object) -> _Dual:
            rhs = other if isinstance(other, _Dual) else _Dual(float(other))
            return _Dual(
                self.value * rhs.value,
                self.tangent * rhs.value + self.value * rhs.tangent,
            )

        __rmul__ = __mul__

        def __truediv__(self, other: object) -> _Dual:
            rhs = other if isinstance(other, _Dual) else _Dual(float(other))
            return _Dual(
                self.value / rhs.value,
                (
                    self.tangent * rhs.value
                    - self.value * rhs.tangent
                )
                / rhs.value**2,
            )

        def __rtruediv__(self, other: object) -> _Dual:
            return _Dual(float(other)) / self

        def __pow__(self, exponent: int) -> _Dual:
            return _Dual(
                self.value**exponent,
                exponent * self.value ** (exponent - 1) * self.tangent,
            )

    def density_pair_with_tangent(
        *,
        a: _Dual,
        hc: _Dual,
        phi: _Dual,
        phi_prime: _Dual,
        theta_prime: _Dual,
        perturbation: tuple[_Dual, _Dual, _Dual, _Dual],
    ) -> tuple[_Dual, _Dual, _Dual]:
        dphi, dphi_prime, dtheta, dtheta_prime = perturbation
        inverse_a_squared = 1.0 / a**2
        potential = (
            rho_star
            + 0.5 * m_phi_squared * phi**2
            + 0.25 * lambda_phi * phi**4
        )
        slope = m_phi_squared * phi + lambda_phi * phi**3
        rho = (
            0.5 * alpha * inverse_a_squared * phi_prime**2
            + 0.5
            * beta
            * inverse_a_squared
            * phi**2
            * theta_prime**2
            + potential
        )
        enthalpy = inverse_a_squared * (
            alpha * phi_prime**2
            + beta * phi**2 * theta_prime**2
        )
        delta_rho_zero_metric = inverse_a_squared * (
            alpha * phi_prime * dphi_prime
            + beta
            * (
                phi**2 * theta_prime * dtheta_prime
                + phi * theta_prime**2 * dphi
            )
        ) + slope * dphi
        momentum_potential = inverse_a_squared * (
            alpha * phi_prime * dphi
            + beta * phi**2 * theta_prime * dtheta
        )
        gravitational_prefactor = (
            4.0 * math.pi * gravitational_constant * a**2
        )
        denominator = wave_number**2 - gravitational_prefactor * enthalpy
        psi = (
            -gravitational_prefactor * delta_rho_zero_metric
            - 3.0
            * hc
            * gravitational_prefactor
            * momentum_potential
        ) / denominator
        delta_rho = delta_rho_zero_metric - enthalpy * psi
        return rho, delta_rho, psi

    perturbation_dual = tuple(
        _Dual(value, derivative)
        for value, derivative in zip(initial, initial_rhs)
    )
    rho_dual, delta_rho_dual, _psi_dual = density_pair_with_tangent(
        a=_Dual(scale_factor, scale_factor),
        hc=_Dual(conformal_hubble, conformal_hubble_n),
        phi=_Dual(phi_background, phi_background_n),
        phi_prime=_Dual(phi_prime_background, phi_prime_background_n),
        theta_prime=_Dual(
            theta_prime_background, theta_prime_background_n
        ),
        perturbation=perturbation_dual,  # type: ignore[arg-type]
    )
    background_density_n = rho_dual.tangent
    perturbed_density_n = delta_rho_dual.tangent
    derived_density_contrast = delta_rho_dual.value / rho_dual.value
    derived_density_contrast_n = (
        perturbed_density_n / rho_dual.value
        - delta_rho_dual.value
        * background_density_n
        / rho_dual.value**2
    )
    quotient_dual = delta_rho_dual / rho_dual
    density_contrast_chain_rule_residual = (
        quotient_dual.tangent - derived_density_contrast_n
    )
    frozen_background_shortcut = density_contrast(initial_rhs)
    frozen_background_shortcut_error = (
        frozen_background_shortcut - derived_density_contrast_n
    )

    def coupled_density_at(offset: float) -> float:
        perturbed = initial + offset * initial_rhs
        certificate = dark_sector_fourier_right_hand_side(
            scale_factor=scale_factor * (1.0 + offset),
            conformal_hubble=(
                conformal_hubble + offset * conformal_hubble_n
            ),
            wave_number=wave_number,
            gravitational_constant=gravitational_constant,
            phi_background=phi_background + offset * phi_background_n,
            phi_prime_background=(
                phi_prime_background
                + offset * phi_prime_background_n
            ),
            theta_prime_background=(
                theta_prime_background
                + offset * theta_prime_background_n
            ),
            delta_phi=float(perturbed[0]),
            delta_phi_prime=float(perturbed[1]),
            delta_theta=float(perturbed[2]),
            delta_theta_prime=float(perturbed[3]),
            alpha=alpha,
            beta=beta,
            rho_star=rho_star,
            m_phi_squared=m_phi_squared,
            lambda_phi=lambda_phi,
            denominator_tolerance=denominator_tolerance,
        )
        return float(
            certificate.stress_energy.delta_energy_density
            / certificate.stress_energy.background_energy_density
        )

    coarse_check = (
        coupled_density_at(finite_difference_step)
        - coupled_density_at(-finite_difference_step)
    ) / (2.0 * finite_difference_step)
    half_step = 0.5 * finite_difference_step
    half_step_check = (
        coupled_density_at(half_step) - coupled_density_at(-half_step)
    ) / (2.0 * half_step)
    density_contrast_finite_difference_check = (
        4.0 * half_step_check - coarse_check
    ) / 3.0
    density_contrast_finite_difference_error = abs(
        density_contrast_finite_difference_check
        - derived_density_contrast_n
    )
    density_contrast_finite_difference_coarse_error = abs(
        coarse_check - derived_density_contrast_n
    )
    density_contrast_finite_difference_converged = (
        abs(half_step_check - derived_density_contrast_n)
        < density_contrast_finite_difference_coarse_error
    )
    derivative_scale = max(1.0e-30, abs(derived_density_contrast_n))
    total_density_derivative_certified = (
        abs(density_contrast_chain_rule_residual)
        <= density_derivative_tolerance * derivative_scale
        and density_contrast_finite_difference_error
        <= density_derivative_tolerance * derivative_scale
        and density_contrast_finite_difference_converged
    )

    poisson_residual = initial_certificate.metric_constraints.poisson_residual
    momentum_constraint_residual = (
        initial_certificate.metric_constraints.momentum_residual
    )
    anisotropy_constraint_residual = (
        initial_certificate.metric_constraints.anisotropy_residual
    )
    metric_closure_residual = initial_certificate.metric_closure_residual
    density_reconstruction_residual = (
        initial_certificate.density_reconstruction_residual
    )
    amplitude_equation_residual = (
        initial_certificate.amplitude_equation.amplitude_equation_residual
    )
    phase_equation_residual = (
        initial_certificate.phase_equation.normalized_equation_residual
    )
    residuals = (
        poisson_residual,
        momentum_constraint_residual,
        anisotropy_constraint_residual,
        metric_closure_residual,
        density_reconstruction_residual,
        amplitude_equation_residual,
        phase_equation_residual,
    )
    maximum_initial_constraint_residual = max(abs(x) for x in residuals)
    minimum_abs_constraint_denominator = abs(
        initial_certificate.constraint_denominator
    )
    metric_constraints_solved = (
        minimum_abs_constraint_denominator > denominator_tolerance
        and maximum_initial_constraint_residual <= constraint_tolerance
        and all(math.isfinite(value) for value in residuals)
    )
    all_values_finite = all(
        math.isfinite(value)
        for value in (
            *initial,
            derived_density_contrast,
            derived_density_contrast_n,
            background_density_n,
            perturbed_density_n,
            density_contrast_finite_difference_check,
            density_contrast_finite_difference_error,
            minimum_abs_constraint_denominator,
        )
    )
    initial_matching_surface_closed = (
        local_rank_certified
        and eigenpair_residual <= eigenpair_residual_tolerance
        and spectral_gap > spectral_gap_tolerance * scale
        and maximum_boundary_residual <= rank_tolerance
        and metric_constraints_solved
        and total_density_derivative_certified
        and all_values_finite
    )

    return RegularGrowingModeInitialStateCertificate(
        source_log_scale_factor=float(source_log_scale_factor),
        variable_order=VARIABLE_ORDER,
        linear_operator=tuple(tuple(float(x) for x in row) for row in operator),
        eigenvalues=tuple(complex(value) for value in values),
        selected_eigenvalue=selected_eigenvalue,
        selected_eigenvector=tuple(float(x) for x in vector),
        eigenpair_residual=eigenpair_residual,
        spectral_gap=spectral_gap,
        pivot_index=pivot_index,
        pivot_absolute_value=abs(float(vector[pivot_index])),
        boundary_matrix=tuple(tuple(float(x) for x in row) for row in boundary),
        rank_minor=rank_minor,
        certified_rank=certified_rank,
        nullity=nullity,
        maximum_boundary_residual=maximum_boundary_residual,
        local_regular_growing_mode_selected=True,
        exact_rank_proved=False,
        local_numerical_rank_certified=True,
        gauge_status="Newtonian gauge",
        observational_calibration_completed=False,
        exact_global_uniqueness_proved=False,
        global_early_time_regularity_proved=False,
        initial_state=tuple(float(x) for x in initial),
        derived_density_contrast=derived_density_contrast,
        derived_density_contrast_n=derived_density_contrast_n,
        background_density_n=background_density_n,
        perturbed_density_n=perturbed_density_n,
        density_contrast_chain_rule_residual=(
            density_contrast_chain_rule_residual
        ),
        density_contrast_finite_difference_check=(
            density_contrast_finite_difference_check
        ),
        density_contrast_finite_difference_error=(
            density_contrast_finite_difference_error
        ),
        density_contrast_finite_difference_coarse_error=(
            density_contrast_finite_difference_coarse_error
        ),
        density_contrast_finite_difference_converged=(
            density_contrast_finite_difference_converged
        ),
        frozen_background_shortcut_error=frozen_background_shortcut_error,
        total_density_derivative_certified=total_density_derivative_certified,
        poisson_residual=poisson_residual,
        momentum_constraint_residual=momentum_constraint_residual,
        anisotropy_constraint_residual=anisotropy_constraint_residual,
        metric_closure_residual=metric_closure_residual,
        density_reconstruction_residual=density_reconstruction_residual,
        amplitude_equation_residual=amplitude_equation_residual,
        phase_equation_residual=phase_equation_residual,
        minimum_abs_constraint_denominator=(
            minimum_abs_constraint_denominator
        ),
        maximum_initial_constraint_residual=(
            maximum_initial_constraint_residual
        ),
        metric_constraints_solved=metric_constraints_solved,
        initial_matching_surface_closed=initial_matching_surface_closed,
        maximum_linearity_residual=maximum_linearity_residual,
        arithmetic_precision_decimal_digits=precision_decimal_digits,
    )
