"""Local frozen-coefficient evolution for the split radiation-species mode.

This module supplies the first numerical bridge joining the frozen
common-curvature state to the action-derived DFM RHS, the baryon/photon/
neutrino RHS, and the spherical-Bessel neutrino terminal relation.

The background coefficients and Thomson rate are held fixed. Therefore this
is a local interface and numerical-consistency integrator, not a physical
recombination-era or late-time Boltzmann evolution.
"""

from __future__ import annotations

from dataclasses import dataclass
import math
from typing import Sequence

import numpy as np

from .massless_neutrino_bessel_terminal_closure_v1 import (
    massless_neutrino_hierarchy_prefix_with_bessel_terminal_closure,
)
from .massless_neutrino_hierarchy_prefix_v1 import (
    radiation_species_with_neutrino_hierarchy_prefix_k_squared,
)


_STATE_COMPONENT_NAMES = (
    "delta_phi",
    "delta_phi_prime",
    "delta_theta",
    "delta_theta_prime",
    "delta_b",
    "theta_b",
    "delta_gamma",
    "theta_gamma",
    "delta_nu",
    "theta_nu",
    "sigma_nu",
    "F_nu_3",
    "F_nu_4",
    "F_nu_5",
    "F_nu_6",
    "F_nu_7",
    "F_nu_8",
    "chi",
)


def _require_finite(name: str, value: float) -> None:
    if not math.isfinite(value):
        raise ValueError(f"{name} must be finite")


def _finite_tuple(
    name: str,
    values: Sequence[float],
    *,
    minimum_length: int = 1,
) -> tuple[float, ...]:
    result = tuple(float(value) for value in values)
    if len(result) < minimum_length:
        raise ValueError(
            f"{name} must have length at least {minimum_length}"
        )
    for index, value in enumerate(result):
        _require_finite(f"{name}[{index}]", value)
    return result


@dataclass(frozen=True)
class FrozenBackgroundSpeciesMode:
    """One immutable set of coefficients for a local mode evolution."""

    scale_factor: float
    conformal_hubble: float
    wave_number_squared: float
    gravitational_constant: float
    phi_background: float
    phi_prime_background: float
    theta_prime_background: float
    alpha: float
    beta: float
    rho_star: float
    m_phi_squared: float
    lambda_phi: float
    baryon_background_density: float
    photon_background_density: float
    neutrino_background_density: float
    thomson_scattering_rate: float = 0.0
    denominator_tolerance: float = 1.0e-14
    closure_tolerance: float = 1.0e-10

    def __post_init__(self) -> None:
        for name, value in (
            ("scale_factor", self.scale_factor),
            ("conformal_hubble", self.conformal_hubble),
            ("wave_number_squared", self.wave_number_squared),
            ("gravitational_constant", self.gravitational_constant),
            ("phi_background", self.phi_background),
            ("phi_prime_background", self.phi_prime_background),
            ("theta_prime_background", self.theta_prime_background),
            ("alpha", self.alpha),
            ("beta", self.beta),
            ("rho_star", self.rho_star),
            ("m_phi_squared", self.m_phi_squared),
            ("lambda_phi", self.lambda_phi),
            (
                "baryon_background_density",
                self.baryon_background_density,
            ),
            (
                "photon_background_density",
                self.photon_background_density,
            ),
            (
                "neutrino_background_density",
                self.neutrino_background_density,
            ),
            (
                "thomson_scattering_rate",
                self.thomson_scattering_rate,
            ),
            ("denominator_tolerance", self.denominator_tolerance),
            ("closure_tolerance", self.closure_tolerance),
        ):
            _require_finite(name, value)

        if self.scale_factor <= 0.0:
            raise ValueError("scale_factor must be positive")
        if self.conformal_hubble <= 0.0:
            raise ValueError("conformal_hubble must be positive")
        if self.wave_number_squared <= 0.0:
            raise ValueError("wave_number_squared must be positive")
        if self.gravitational_constant <= 0.0:
            raise ValueError("gravitational_constant must be positive")
        if min(
            self.baryon_background_density,
            self.photon_background_density,
            self.neutrino_background_density,
        ) < 0.0:
            raise ValueError("background densities must be nonnegative")
        if self.thomson_scattering_rate < 0.0:
            raise ValueError(
                "thomson_scattering_rate must be nonnegative"
            )
        if self.denominator_tolerance <= 0.0:
            raise ValueError(
                "denominator_tolerance must be positive"
            )
        if self.closure_tolerance < 0.0:
            raise ValueError(
                "closure_tolerance must be nonnegative"
            )


@dataclass(frozen=True)
class RadiationSpeciesModeState:
    """Full DFM+baryon+photon+neutrino state for one Fourier mode."""

    delta_phi: float
    delta_phi_prime: float
    delta_theta: float
    delta_theta_prime: float
    baryon_density_contrast: float
    baryon_velocity_divergence: float
    photon_density_contrast: float
    photon_velocity_divergence: float
    neutrino_density_contrast: float
    neutrino_velocity_divergence: float
    neutrino_anisotropic_stress: float
    multipoles_l3_to_lmax: tuple[float, ...]
    conformal_free_streaming_interval: float

    def __post_init__(self) -> None:
        for name, value in (
            ("delta_phi", self.delta_phi),
            ("delta_phi_prime", self.delta_phi_prime),
            ("delta_theta", self.delta_theta),
            ("delta_theta_prime", self.delta_theta_prime),
            (
                "baryon_density_contrast",
                self.baryon_density_contrast,
            ),
            (
                "baryon_velocity_divergence",
                self.baryon_velocity_divergence,
            ),
            (
                "photon_density_contrast",
                self.photon_density_contrast,
            ),
            (
                "photon_velocity_divergence",
                self.photon_velocity_divergence,
            ),
            (
                "neutrino_density_contrast",
                self.neutrino_density_contrast,
            ),
            (
                "neutrino_velocity_divergence",
                self.neutrino_velocity_divergence,
            ),
            (
                "neutrino_anisotropic_stress",
                self.neutrino_anisotropic_stress,
            ),
            (
                "conformal_free_streaming_interval",
                self.conformal_free_streaming_interval,
            ),
        ):
            _require_finite(name, value)

        multipoles = _finite_tuple(
            "multipoles_l3_to_lmax",
            self.multipoles_l3_to_lmax,
            minimum_length=1,
        )
        object.__setattr__(
            self,
            "multipoles_l3_to_lmax",
            multipoles,
        )

        if self.conformal_free_streaming_interval <= 0.0:
            raise ValueError(
                "conformal_free_streaming_interval must be positive"
            )

    @property
    def l_max(self) -> int:
        return len(self.multipoles_l3_to_lmax) + 2

    @property
    def dimension(self) -> int:
        return 12 + len(self.multipoles_l3_to_lmax)

    def as_array(self) -> np.ndarray:
        return np.asarray(
            (
                self.delta_phi,
                self.delta_phi_prime,
                self.delta_theta,
                self.delta_theta_prime,
                self.baryon_density_contrast,
                self.baryon_velocity_divergence,
                self.photon_density_contrast,
                self.photon_velocity_divergence,
                self.neutrino_density_contrast,
                self.neutrino_velocity_divergence,
                self.neutrino_anisotropic_stress,
                *self.multipoles_l3_to_lmax,
                self.conformal_free_streaming_interval,
            ),
            dtype=float,
        )

    @classmethod
    def from_array(
        cls,
        values: Sequence[float],
        *,
        l_max: int,
    ) -> "RadiationSpeciesModeState":
        vector = np.asarray(values, dtype=float)
        expected = l_max + 10
        if l_max < 3:
            raise ValueError("l_max must be at least 3")
        if vector.shape != (expected,):
            raise ValueError(
                f"state vector must have shape ({expected},)"
            )
        if not np.all(np.isfinite(vector)):
            raise ValueError("state vector must be finite")
        return cls(
            delta_phi=float(vector[0]),
            delta_phi_prime=float(vector[1]),
            delta_theta=float(vector[2]),
            delta_theta_prime=float(vector[3]),
            baryon_density_contrast=float(vector[4]),
            baryon_velocity_divergence=float(vector[5]),
            photon_density_contrast=float(vector[6]),
            photon_velocity_divergence=float(vector[7]),
            neutrino_density_contrast=float(vector[8]),
            neutrino_velocity_divergence=float(vector[9]),
            neutrino_anisotropic_stress=float(vector[10]),
            multipoles_l3_to_lmax=tuple(
                float(value)
                for value in vector[11:-1]
            ),
            conformal_free_streaming_interval=float(vector[-1]),
        )


@dataclass(frozen=True)
class FrozenBackgroundSpeciesModeRightHandSide:
    """One full RHS evaluation with algebraic closure diagnostics."""

    derivative_with_respect_to_N: tuple[float, ...]
    estimated_tail_multipole_lmax_plus_one: float
    maximum_hierarchy_recurrence_residual: float
    bessel_terminal_relation_closed: bool
    finite_hierarchy_algebraically_closed: bool
    coupled_prefix_closed: bool
    species_rhs_closed: bool
    physical_radiation_microphysics_closed: bool
    physical_mode_integration_run: bool

    def __post_init__(self) -> None:
        derivative = _finite_tuple(
            "derivative_with_respect_to_N",
            self.derivative_with_respect_to_N,
        )
        object.__setattr__(
            self,
            "derivative_with_respect_to_N",
            derivative,
        )
        _require_finite(
            "estimated_tail_multipole_lmax_plus_one",
            self.estimated_tail_multipole_lmax_plus_one,
        )
        _require_finite(
            "maximum_hierarchy_recurrence_residual",
            self.maximum_hierarchy_recurrence_residual,
        )


@dataclass(frozen=True)
class FrozenBackgroundSpeciesModeIntegration:
    """A fixed-step RK4 local evolution receipt."""

    N: np.ndarray
    states: np.ndarray
    l_max: int
    steps: int
    all_rhs_finite: bool
    all_bessel_terminal_relations_closed: bool
    all_finite_hierarchies_algebraically_closed: bool
    all_coupled_prefixes_closed: bool
    all_species_rhs_closed: bool
    frozen_background_coefficients: bool
    thomson_scattering_history_supplied: bool
    frozen_coefficient_mode_integration_run: bool
    physical_mode_integration_run: bool
    physical_recombination_history_closed: bool
    coupled_lmax_convergence_certified: bool

    def __post_init__(self) -> None:
        N = np.asarray(self.N, dtype=float)
        states = np.asarray(self.states, dtype=float)
        expected_dimension = self.l_max + 10
        if N.shape != (self.steps + 1,):
            raise ValueError("N has the wrong shape")
        if states.shape != (
            self.steps + 1,
            expected_dimension,
        ):
            raise ValueError("states has the wrong shape")
        if not np.all(np.isfinite(N)):
            raise ValueError("N must be finite")
        if not np.all(np.isfinite(states)):
            raise ValueError("states must be finite")
        N = N.copy()
        states = states.copy()
        N.setflags(write=False)
        states.setflags(write=False)
        object.__setattr__(self, "N", N)
        object.__setattr__(self, "states", states)



@dataclass(frozen=True)
class FrozenBackgroundSpeciesModeTimeStepConvergence:
    "Asymptotic RK4 refinement certificate at fixed background and l_max."

    finest: FrozenBackgroundSpeciesModeIntegration
    step_counts: tuple[int, ...]
    adjacent_absolute_inf_differences: tuple[float, ...]
    observed_orders: tuple[float, ...]
    minimum_required_order: float
    conservative_richardson_order: float
    last_adjacent_seed_scaled_difference: float
    richardson_absolute_final_error_bound: float
    richardson_seed_scaled_final_error_bound: float
    dominant_final_difference_component: str
    all_refinements_finite: bool
    all_bessel_terminal_relations_closed: bool
    all_finite_hierarchies_algebraically_closed: bool
    adjacent_differences_strictly_decrease: bool
    asymptotic_order_gate: bool
    fixed_background_time_step_convergence_certified: bool
    physical_mode_integration_run: bool
    physical_recombination_history_closed: bool
    coupled_lmax_convergence_certified: bool

    def __post_init__(self) -> None:
        if len(self.step_counts) < 4:
            raise ValueError("at least four refinement levels are required")
        if any(step < 1 for step in self.step_counts):
            raise ValueError("step counts must be positive")
        if any(
            right != 2 * left
            for left, right in zip(
                self.step_counts[:-1],
                self.step_counts[1:],
            )
        ):
            raise ValueError("step counts must double at each refinement")
        if len(self.adjacent_absolute_inf_differences) != (
            len(self.step_counts) - 1
        ):
            raise ValueError("adjacent difference count is inconsistent")
        if len(self.observed_orders) != len(self.step_counts) - 2:
            raise ValueError("observed order count is inconsistent")

        for name, values in (
            (
                "adjacent_absolute_inf_differences",
                self.adjacent_absolute_inf_differences,
            ),
            ("observed_orders", self.observed_orders),
        ):
            _finite_tuple(name, values)

        for name, value in (
            ("minimum_required_order", self.minimum_required_order),
            (
                "conservative_richardson_order",
                self.conservative_richardson_order,
            ),
            (
                "last_adjacent_seed_scaled_difference",
                self.last_adjacent_seed_scaled_difference,
            ),
            (
                "richardson_absolute_final_error_bound",
                self.richardson_absolute_final_error_bound,
            ),
            (
                "richardson_seed_scaled_final_error_bound",
                self.richardson_seed_scaled_final_error_bound,
            ),
        ):
            _require_finite(name, value)

        if self.minimum_required_order <= 0.0:
            raise ValueError("minimum_required_order must be positive")
        if self.conservative_richardson_order <= 0.0:
            raise ValueError(
                "conservative_richardson_order must be positive"
            )
        if not self.dominant_final_difference_component:
            raise ValueError(
                "dominant_final_difference_component must be nonempty"
            )


def frozen_background_species_mode_right_hand_side(
    *,
    state: RadiationSpeciesModeState,
    background: FrozenBackgroundSpeciesMode,
) -> FrozenBackgroundSpeciesModeRightHandSide:
    """Evaluate the complete local RHS and convert d/deta into d/dN."""

    closure = (
        massless_neutrino_hierarchy_prefix_with_bessel_terminal_closure(
            wave_number_squared=background.wave_number_squared,
            conformal_free_streaming_interval=(
                state.conformal_free_streaming_interval
            ),
            neutrino_anisotropic_stress=(
                state.neutrino_anisotropic_stress
            ),
            multipoles_l3_to_lmax=(
                state.multipoles_l3_to_lmax
            ),
            closure_tolerance=background.closure_tolerance,
        )
    )
    tail = float(
        closure.terminal_closure
        .estimated_tail_multipole_lmax_plus_one
    )

    certificate = (
        radiation_species_with_neutrino_hierarchy_prefix_k_squared(
            multipoles_l3_to_lmax=(
                state.multipoles_l3_to_lmax
            ),
            tail_multipole_lmax_plus_one=tail,
            closure_tolerance=background.closure_tolerance,
            scale_factor=background.scale_factor,
            conformal_hubble=background.conformal_hubble,
            wave_number_squared=background.wave_number_squared,
            gravitational_constant=background.gravitational_constant,
            phi_background=background.phi_background,
            phi_prime_background=(
                background.phi_prime_background
            ),
            theta_prime_background=(
                background.theta_prime_background
            ),
            delta_phi=state.delta_phi,
            delta_phi_prime=state.delta_phi_prime,
            delta_theta=state.delta_theta,
            delta_theta_prime=state.delta_theta_prime,
            alpha=background.alpha,
            beta=background.beta,
            rho_star=background.rho_star,
            m_phi_squared=background.m_phi_squared,
            lambda_phi=background.lambda_phi,
            baryon_background_density=(
                background.baryon_background_density
            ),
            photon_background_density=(
                background.photon_background_density
            ),
            neutrino_background_density=(
                background.neutrino_background_density
            ),
            baryon_density_contrast=(
                state.baryon_density_contrast
            ),
            baryon_velocity_divergence=(
                state.baryon_velocity_divergence
            ),
            photon_density_contrast=(
                state.photon_density_contrast
            ),
            photon_velocity_divergence=(
                state.photon_velocity_divergence
            ),
            neutrino_density_contrast=(
                state.neutrino_density_contrast
            ),
            neutrino_velocity_divergence=(
                state.neutrino_velocity_divergence
            ),
            neutrino_anisotropic_stress=(
                state.neutrino_anisotropic_stress
            ),
            thomson_scattering_rate=(
                background.thomson_scattering_rate
            ),
            denominator_tolerance=(
                background.denominator_tolerance
            ),
        )
    )

    species_rhs = certificate.species_rhs
    dark_rhs = species_rhs.dark_sector_rhs
    hierarchy = certificate.neutrino_hierarchy
    inverse_conformal_hubble = (
        1.0 / background.conformal_hubble
    )

    conformal_derivative = (
        state.delta_phi_prime,
        float(dark_rhs.delta_phi_double_prime),
        state.delta_theta_prime,
        float(dark_rhs.delta_theta_double_prime),
        float(species_rhs.baryon_density_contrast_prime),
        float(species_rhs.baryon_velocity_divergence_prime),
        float(species_rhs.photon_density_contrast_prime),
        float(species_rhs.photon_velocity_divergence_prime),
        float(species_rhs.neutrino_density_contrast_prime),
        float(species_rhs.neutrino_velocity_divergence_prime),
        float(species_rhs.neutrino_anisotropic_stress_prime),
        *tuple(
            float(value)
            for value in hierarchy.derivatives_l3_to_lmax
        ),
    )
    derivative = tuple(
        value * inverse_conformal_hubble
        for value in conformal_derivative
    ) + (inverse_conformal_hubble,)

    return FrozenBackgroundSpeciesModeRightHandSide(
        derivative_with_respect_to_N=derivative,
        estimated_tail_multipole_lmax_plus_one=tail,
        maximum_hierarchy_recurrence_residual=float(
            hierarchy.maximum_recurrence_residual
        ),
        bessel_terminal_relation_closed=bool(
            closure.terminal_closure
            .bessel_terminal_relation_closed
        ),
        finite_hierarchy_algebraically_closed=bool(
            closure.finite_hierarchy_algebraically_closed
        ),
        coupled_prefix_closed=bool(
            certificate.coupled_prefix_closed
        ),
        species_rhs_closed=bool(
            species_rhs.species_rhs_closed
        ),
        physical_radiation_microphysics_closed=False,
        physical_mode_integration_run=False,
    )


def _background_at_n(
    background: FrozenBackgroundSpeciesMode,
    N: float,
) -> FrozenBackgroundSpeciesMode:
    """Resolve and validate the background at one RK4 stage."""

    _require_finite("N", N)

    evaluator = getattr(background, "at_N", None)
    if evaluator is None:
        evaluator = getattr(background, "evaluate", None)

    if callable(evaluator):
        candidate = evaluator(float(N))
    elif callable(background):
        candidate = background(float(N))
    else:
        candidate = background

    if candidate is None:
        raise ValueError("background evaluator returned None")

    values = vars(candidate) if hasattr(candidate, "__dict__") else {}
    for name, value in values.items():
        if isinstance(
            value,
            (int, float, np.integer, np.floating),
        ):
            if not np.isfinite(float(value)):
                raise ValueError(
                    f"background stage field {name} is nonfinite at N={N}"
                )
        elif isinstance(value, np.ndarray):
            if not np.all(np.isfinite(value)):
                raise ValueError(
                    f"background stage field {name} is nonfinite at N={N}"
                )

    normalized_residual = getattr(
        candidate,
        "normalized_friedmann_residual",
        None,
    )
    if normalized_residual is not None:
        normalized_residual = float(normalized_residual)
        if not np.isfinite(normalized_residual):
            raise ValueError(
                "normalized Friedmann residual is nonfinite"
            )
        if abs(normalized_residual) > 1.0e-10:
            raise ValueError(
                "normalized Friedmann residual exceeds 1e-10"
            )

    return candidate


def _rk4_step(
    *,
    N_start: float,
    vector: np.ndarray,
    step_size: float,
    l_max: int,
    background: FrozenBackgroundSpeciesMode,
) -> tuple[
    np.ndarray,
    tuple[FrozenBackgroundSpeciesModeRightHandSide, ...],
]:
    def evaluate(
        N_value: float,
        values: np.ndarray,
    ) -> FrozenBackgroundSpeciesModeRightHandSide:
        state = RadiationSpeciesModeState.from_array(
            values,
            l_max=l_max,
        )
        return frozen_background_species_mode_right_hand_side(
            state=state,
            background=_background_at_n(background, N_value),
        )

    first = evaluate(N_start, vector)
    k1 = np.asarray(
        first.derivative_with_respect_to_N,
        dtype=float,
    )

    N_half = N_start + 0.5 * step_size
    second = evaluate(
        N_half,
        vector + 0.5 * step_size * k1,
    )
    k2 = np.asarray(
        second.derivative_with_respect_to_N,
        dtype=float,
    )

    third = evaluate(
        N_half,
        vector + 0.5 * step_size * k2,
    )
    k3 = np.asarray(
        third.derivative_with_respect_to_N,
        dtype=float,
    )

    fourth = evaluate(
        N_start + step_size,
        vector + step_size * k3,
    )
    k4 = np.asarray(
        fourth.derivative_with_respect_to_N,
        dtype=float,
    )

    updated = vector + (
        step_size / 6.0
    ) * (k1 + 2.0 * k2 + 2.0 * k3 + k4)

    if not np.all(np.isfinite(updated)):
        raise FloatingPointError(
            "species-mode RK4 step is nonfinite"
        )

    return updated, (first, second, third, fourth)


def integrate_frozen_background_species_mode(
    *,
    N_start: float,
    N_end: float,
    steps: int,
    initial_state: RadiationSpeciesModeState,
    background: FrozenBackgroundSpeciesMode,
) -> FrozenBackgroundSpeciesModeIntegration:
    """Integrate one local mode with frozen coefficients using RK4."""

    _require_finite("N_start", N_start)
    _require_finite("N_end", N_end)
    if N_end <= N_start:
        raise ValueError("N_end must exceed N_start")
    if steps < 1:
        raise ValueError("steps must be positive")

    N = np.linspace(N_start, N_end, steps + 1)
    states = np.empty(
        (steps + 1, initial_state.dimension),
        dtype=float,
    )
    states[0] = initial_state.as_array()
    step_size = (N_end - N_start) / steps

    all_rhs_finite = True
    all_bessel_closed = True
    all_hierarchy_closed = True
    all_prefixes_closed = True
    all_species_closed = True

    for index in range(steps):
        updated, evaluations = _rk4_step(
            N_start=float(N[index]),
            vector=states[index],
            step_size=step_size,
            l_max=initial_state.l_max,
            background=background,
        )
        states[index + 1] = updated

        for evaluation in evaluations:
            derivative = np.asarray(
                evaluation.derivative_with_respect_to_N,
                dtype=float,
            )
            all_rhs_finite = (
                all_rhs_finite
                and bool(np.all(np.isfinite(derivative)))
            )
            all_bessel_closed = (
                all_bessel_closed
                and evaluation.bessel_terminal_relation_closed
            )
            all_hierarchy_closed = (
                all_hierarchy_closed
                and evaluation.finite_hierarchy_algebraically_closed
            )
            all_prefixes_closed = (
                all_prefixes_closed
                and evaluation.coupled_prefix_closed
            )
            all_species_closed = (
                all_species_closed
                and evaluation.species_rhs_closed
            )

    return FrozenBackgroundSpeciesModeIntegration(
        N=N,
        states=states,
        l_max=initial_state.l_max,
        steps=steps,
        all_rhs_finite=all_rhs_finite,
        all_bessel_terminal_relations_closed=(
            all_bessel_closed
        ),
        all_finite_hierarchies_algebraically_closed=(
            all_hierarchy_closed
        ),
        all_coupled_prefixes_closed=all_prefixes_closed,
        all_species_rhs_closed=all_species_closed,
        frozen_background_coefficients=True,
        thomson_scattering_history_supplied=False,
        frozen_coefficient_mode_integration_run=True,
        physical_mode_integration_run=False,
        physical_recombination_history_closed=False,
        coupled_lmax_convergence_certified=False,
    )

def certify_frozen_background_species_mode_time_step_convergence(
    *,
    N_start: float,
    N_end: float,
    initial_state: RadiationSpeciesModeState,
    background: FrozenBackgroundSpeciesMode,
    base_steps: int = 128,
    refinement_levels: int = 4,
    reference_amplitude: float = 1.0e-6,
    minimum_observed_order: float = 4.0,
    conservative_richardson_order: float = 4.0,
    maximum_seed_scaled_richardson_bound: float = 1.0e-6,
) -> FrozenBackgroundSpeciesModeTimeStepConvergence:
    "Certify the asymptotic fixed-background RK4 refinement regime."

    _require_finite("reference_amplitude", reference_amplitude)
    _require_finite(
        "minimum_observed_order",
        minimum_observed_order,
    )
    _require_finite(
        "conservative_richardson_order",
        conservative_richardson_order,
    )
    _require_finite(
        "maximum_seed_scaled_richardson_bound",
        maximum_seed_scaled_richardson_bound,
    )

    if base_steps < 1:
        raise ValueError("base_steps must be positive")
    if refinement_levels < 4:
        raise ValueError(
            "refinement_levels must be at least four"
        )
    if reference_amplitude <= 0.0:
        raise ValueError("reference_amplitude must be positive")
    if minimum_observed_order <= 0.0:
        raise ValueError(
            "minimum_observed_order must be positive"
        )
    if conservative_richardson_order <= 0.0:
        raise ValueError(
            "conservative_richardson_order must be positive"
        )
    if maximum_seed_scaled_richardson_bound <= 0.0:
        raise ValueError(
            "maximum_seed_scaled_richardson_bound must be positive"
        )

    step_counts = tuple(
        base_steps * (2**level)
        for level in range(refinement_levels)
    )
    integrations = tuple(
        integrate_frozen_background_species_mode(
            N_start=N_start,
            N_end=N_end,
            steps=steps,
            initial_state=initial_state,
            background=background,
        )
        for steps in step_counts
    )

    adjacent_differences = tuple(
        float(
            np.linalg.norm(
                fine.states[-1] - coarse.states[-1],
                ord=np.inf,
            )
        )
        for coarse, fine in zip(
            integrations[:-1],
            integrations[1:],
        )
    )
    observed_orders = tuple(
        math.log2(left / right)
        for left, right in zip(
            adjacent_differences[:-1],
            adjacent_differences[1:],
        )
        if left > 0.0 and right > 0.0
    )
    if len(observed_orders) != refinement_levels - 2:
        raise FloatingPointError(
            "adjacent differences must be strictly positive"
        )

    adjacent_decrease = all(
        right < left
        for left, right in zip(
            adjacent_differences[:-1],
            adjacent_differences[1:],
        )
    )
    asymptotic_order_gate = all(
        order >= minimum_observed_order
        for order in observed_orders
    )

    initial = initial_state.as_array()
    penultimate = integrations[-2].states[-1]
    finest = integrations[-1].states[-1]
    last_component_difference = np.abs(finest - penultimate)

    component_scale = np.maximum.reduce(
        (
            np.abs(initial),
            np.abs(finest),
            np.full_like(initial, reference_amplitude),
        )
    )
    component_scale[-1] = max(
        abs(initial[-1]),
        abs(finest[-1]),
        reference_amplitude,
    )
    seed_scaled_difference = (
        last_component_difference / component_scale
    )
    dominant_index = int(np.argmax(seed_scaled_difference))
    last_seed_scaled = float(
        np.linalg.norm(seed_scaled_difference, ord=np.inf)
    )

    richardson_denominator = (
        2.0**conservative_richardson_order - 1.0
    )
    richardson_absolute_bound = (
        adjacent_differences[-1]
        / richardson_denominator
    )
    richardson_seed_scaled_bound = (
        last_seed_scaled
        / richardson_denominator
    )

    all_refinements_finite = all(
        integration.all_rhs_finite
        and bool(np.all(np.isfinite(integration.states)))
        for integration in integrations
    )
    all_bessel_closed = all(
        integration.all_bessel_terminal_relations_closed
        for integration in integrations
    )
    all_hierarchies_closed = all(
        integration
        .all_finite_hierarchies_algebraically_closed
        for integration in integrations
    )

    certified = (
        all_refinements_finite
        and all_bessel_closed
        and all_hierarchies_closed
        and adjacent_decrease
        and asymptotic_order_gate
        and richardson_seed_scaled_bound
        <= maximum_seed_scaled_richardson_bound
    )

    return FrozenBackgroundSpeciesModeTimeStepConvergence(
        finest=integrations[-1],
        step_counts=step_counts,
        adjacent_absolute_inf_differences=(
            adjacent_differences
        ),
        observed_orders=observed_orders,
        minimum_required_order=minimum_observed_order,
        conservative_richardson_order=(
            conservative_richardson_order
        ),
        last_adjacent_seed_scaled_difference=(
            last_seed_scaled
        ),
        richardson_absolute_final_error_bound=(
            richardson_absolute_bound
        ),
        richardson_seed_scaled_final_error_bound=(
            richardson_seed_scaled_bound
        ),
        dominant_final_difference_component=(
            _STATE_COMPONENT_NAMES[dominant_index]
        ),
        all_refinements_finite=all_refinements_finite,
        all_bessel_terminal_relations_closed=(
            all_bessel_closed
        ),
        all_finite_hierarchies_algebraically_closed=(
            all_hierarchies_closed
        ),
        adjacent_differences_strictly_decrease=(
            adjacent_decrease
        ),
        asymptotic_order_gate=asymptotic_order_gate,
        fixed_background_time_step_convergence_certified=(
            certified
        ),
        physical_mode_integration_run=False,
        physical_recombination_history_closed=False,
        coupled_lmax_convergence_certified=False,
    )

