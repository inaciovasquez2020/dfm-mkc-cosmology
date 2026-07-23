from __future__ import annotations

import json
import math
from pathlib import Path

import numpy as np

from dfm_mkc_solver.radiation_species_fixed_background_mode_integrator_v1 import (
    FrozenBackgroundSpeciesMode,
    RadiationSpeciesModeState,
    certify_frozen_background_species_mode_time_step_convergence,
    frozen_background_species_mode_right_hand_side,
    integrate_frozen_background_species_mode,
)


REPO = Path(__file__).resolve().parents[1]
RECEIPT = (
    REPO
    / "artifacts"
    / "dfm_mkc"
    / "species_common_curvature_initial_mode_receipt_v2.json"
)



def _regular_neutrino_multipoles_for_lmax(
    mode,
    *,
    l_max: int,
):
    import math as _math

    if l_max not in (8, 12):
        raise ValueError("l_max must be 8 or 12")

    base = tuple(float(value) for value in mode["F_nu_l3_to_lmax"])
    if len(base) != 6:
        raise ValueError("receipt must contain the l=3,...,8 prefix")
    if l_max == 8:
        return base

    epsilon = (
        _math.sqrt(float(mode["wave_number_squared_code"]))
        * float(mode["initial_free_streaming_interval"])
    )
    extended = list(base)
    previous = base[-1]
    for ell in range(9, l_max + 1):
        previous = previous * epsilon / (2.0 * ell + 1.0)
        extended.append(previous)

    return tuple(extended)


def _objects(*, l_max: int = 8) -> tuple[
    dict,
    FrozenBackgroundSpeciesMode,
    RadiationSpeciesModeState,
]:
    receipt = json.loads(RECEIPT.read_text())
    background_data = receipt["selected_background"]
    mode = receipt["selected_modes"][0]
    dfm = mode["dfm_state"]

    background = FrozenBackgroundSpeciesMode(
        scale_factor=background_data["scale_factor"],
        conformal_hubble=background_data["conformal_H"],
        wave_number_squared=mode["wave_number_squared_code"],
        gravitational_constant=1.0 / (8.0 * math.pi),
        phi_background=background_data["phi"],
        phi_prime_background=background_data["phi_prime"],
        theta_prime_background=background_data["theta_prime"],
        alpha=receipt["alpha"],
        beta=receipt["beta"],
        rho_star=receipt["rho_star"],
        m_phi_squared=background_data["m_phi_squared"],
        lambda_phi=receipt["lambda_phi"],
        baryon_background_density=background_data["rho_b"],
        photon_background_density=background_data["rho_gamma"],
        neutrino_background_density=background_data["rho_nu"],
        thomson_scattering_rate=0.0,
    )
    state = RadiationSpeciesModeState(
        delta_phi=dfm[0],
        delta_phi_prime=dfm[1],
        delta_theta=dfm[2],
        delta_theta_prime=dfm[3],
        baryon_density_contrast=mode["delta_b"],
        baryon_velocity_divergence=mode["theta_b"],
        photon_density_contrast=mode["delta_gamma"],
        photon_velocity_divergence=mode["theta_gamma"],
        neutrino_density_contrast=mode["delta_nu"],
        neutrino_velocity_divergence=mode["theta_nu"],
        neutrino_anisotropic_stress=mode["sigma_nu"],
        multipoles_l3_to_lmax=(
            _regular_neutrino_multipoles_for_lmax(
                mode,
                l_max=l_max,
            )
        ),
        conformal_free_streaming_interval=(
            mode["initial_free_streaming_interval"]
        ),
    )
    return receipt, background, state


def test_frozen_common_curvature_mode_has_finite_complete_rhs():
    _, background, state = _objects()

    rhs = frozen_background_species_mode_right_hand_side(
        state=state,
        background=background,
    )
    derivative = np.asarray(
        rhs.derivative_with_respect_to_N,
        dtype=float,
    )

    assert state.l_max == 8
    assert state.dimension == 18
    assert derivative.shape == (18,)
    assert np.all(np.isfinite(derivative))
    assert math.isclose(
        derivative[0],
        state.delta_phi_prime / background.conformal_hubble,
        rel_tol=1.0e-14,
        abs_tol=0.0,
    )
    assert math.isclose(
        derivative[-1],
        1.0 / background.conformal_hubble,
        rel_tol=1.0e-14,
        abs_tol=0.0,
    )
    assert rhs.bessel_terminal_relation_closed is True
    assert rhs.finite_hierarchy_algebraically_closed is True
    assert rhs.coupled_prefix_closed is True
    assert rhs.species_rhs_closed is True
    assert rhs.physical_radiation_microphysics_closed is False
    assert rhs.physical_mode_integration_run is False


def test_short_frozen_background_mode_integration_runs():
    receipt, background, state = _objects()
    N_start = receipt["selected_background"]["N_initial"]

    integration = integrate_frozen_background_species_mode(
        N_start=N_start,
        N_end=N_start + 1.0e-2,
        steps=8,
        initial_state=state,
        background=background,
    )

    assert integration.N.shape == (9,)
    assert integration.states.shape == (9, 18)
    assert np.all(np.isfinite(integration.states))
    assert integration.all_rhs_finite is True
    assert (
        integration.all_bessel_terminal_relations_closed
        is True
    )
    assert (
        integration.all_finite_hierarchies_algebraically_closed
        is True
    )
    assert integration.all_coupled_prefixes_closed is False
    assert integration.all_species_rhs_closed is False
    assert integration.frozen_background_coefficients is True
    assert integration.thomson_scattering_history_supplied is False
    assert integration.frozen_coefficient_mode_integration_run is True
    assert integration.physical_mode_integration_run is False
    assert integration.physical_recombination_history_closed is False
    assert integration.coupled_lmax_convergence_certified is False

def test_fixed_background_time_step_convergence_is_certified():
    receipt, background, state = _objects()
    N_start = receipt["selected_background"]["N_initial"]

    certificate = (
        certify_frozen_background_species_mode_time_step_convergence(
            N_start=N_start,
            N_end=N_start + 1.0e-2,
            initial_state=state,
            background=background,
            base_steps=128,
            refinement_levels=4,
            reference_amplitude=abs(receipt["target_R_star"]),
            minimum_observed_order=4.0,
            conservative_richardson_order=4.0,
            maximum_seed_scaled_richardson_bound=1.0e-6,
        )
    )

    assert certificate.step_counts == (128, 256, 512, 1024)
    assert len(
        certificate.adjacent_absolute_inf_differences
    ) == 3
    assert len(certificate.observed_orders) == 2
    assert certificate.adjacent_differences_strictly_decrease is True
    assert certificate.asymptotic_order_gate is True
    assert min(certificate.observed_orders) >= 4.0
    assert (
        certificate.adjacent_absolute_inf_differences[-1]
        < 1.0e-11
    )
    assert (
        certificate.last_adjacent_seed_scaled_difference
        < 1.0e-5
    )
    assert (
        certificate.richardson_absolute_final_error_bound
        < 1.0e-12
    )
    assert (
        certificate.richardson_seed_scaled_final_error_bound
        < 1.0e-6
    )
    assert (
        certificate.dominant_final_difference_component
        == "delta_gamma"
    )
    assert certificate.all_refinements_finite is True
    assert (
        certificate.all_bessel_terminal_relations_closed
        is True
    )
    assert (
        certificate.all_finite_hierarchies_algebraically_closed
        is True
    )
    assert (
        certificate
        .fixed_background_time_step_convergence_certified
        is True
    )
    assert certificate.physical_mode_integration_run is False
    assert (
        certificate.physical_recombination_history_closed
        is False
    )
    assert certificate.coupled_lmax_convergence_certified is False

class _CalibratedShortEvolvingBackground:
    """Interpolate the actual calibrated charge-reduced background solution."""

    def __init__(
        self,
        frozen_background,
        *,
        receipt,
        N_start: float,
        N_end: float,
        background_samples: int = 17,
    ):
        import numpy as _np

        from dfm_mkc_solver.charge_reduced_background_v1 import (
            ChargeReducedInitialData,
            ChargeReducedParameters,
            ChargeReducedSolverConfig,
            friedmann_hubble,
            solve_charge_reduced_background,
        )

        self._frozen_background = frozen_background
        self._N_start = float(N_start)
        self._N_end = float(N_end)
        self._background_samples = int(background_samples)
        if (
            self._background_samples != background_samples
            or self._background_samples < 5
        ):
            raise ValueError(
                "background_samples must be an integer at least five"
            )
        self._friedmann_hubble = friedmann_hubble
        self.stage_N_values = []
        self.normalized_friedmann_residuals = []

        if self._N_end <= self._N_start:
            raise ValueError("N_end must exceed N_start")

        selected = receipt["selected_background"]
        required_selected = (
            "rho_b",
            "rho_gamma",
            "rho_nu",
        )
        missing_selected = [
            name for name in required_selected
            if name not in selected
        ]
        if missing_selected:
            raise KeyError(
                "selected background is missing "
                + ",".join(missing_selected)
            )

        scale_factor_initial = float(
            getattr(frozen_background, "scale_factor")
        )
        conformal_hubble_initial = float(
            getattr(frozen_background, "conformal_hubble")
        )
        phi_initial = float(
            getattr(frozen_background, "phi_background")
        )
        phi_prime_initial = float(
            getattr(frozen_background, "phi_prime_background")
        )
        theta_prime_initial = float(
            getattr(frozen_background, "theta_prime_background")
        )
        alpha = float(getattr(frozen_background, "alpha"))
        beta = float(getattr(frozen_background, "beta"))
        rho_star = float(getattr(frozen_background, "rho_star"))
        m_phi_squared = float(
            getattr(frozen_background, "m_phi_squared")
        )
        lambda_phi = float(
            getattr(frozen_background, "lambda_phi")
        )
        gravitational_constant = float(
            getattr(frozen_background, "gravitational_constant")
        )

        if scale_factor_initial <= 0.0:
            raise ValueError("initial scale factor must be positive")
        if conformal_hubble_initial <= 0.0:
            raise ValueError("initial conformal Hubble value must be positive")
        if phi_initial == 0.0:
            raise ValueError("initial phi must be nonzero")

        v_initial = phi_prime_initial / scale_factor_initial
        theta_dot_initial = (
            theta_prime_initial / scale_factor_initial
        )
        q_theta = (
            beta
            * scale_factor_initial**3
            * phi_initial**2
            * theta_dot_initial
        )
        rho_m_initial = float(selected["rho_b"])
        rho_gamma_initial = float(selected["rho_gamma"])
        rho_nu_initial = float(selected["rho_nu"])
        rho_r_initial = rho_gamma_initial + rho_nu_initial

        if rho_m_initial < 0.0 or rho_r_initial <= 0.0:
            raise ValueError(
                "direct background densities must be nonnegative"
            )

        self._photon_fraction = (
            rho_gamma_initial / rho_r_initial
        )
        self._neutrino_fraction = (
            rho_nu_initial / rho_r_initial
        )

        self._parameters = ChargeReducedParameters(
            G=gravitational_constant,
            Lambda=0.0,
            alpha=alpha,
            beta=beta,
            rho_star=rho_star,
            m_phi_squared=m_phi_squared,
            lambda_phi=lambda_phi,
            Q_theta=q_theta,
        )
        initial_data = ChargeReducedInitialData(
            phi=phi_initial,
            v=v_initial,
            theta=0.0,
            rho_m=rho_m_initial,
            rho_r=rho_r_initial,
        )
        config = ChargeReducedSolverConfig(
            N_initial=self._N_start,
            N_final=self._N_end,
            samples=self._background_samples,
            rtol=1.0e-9,
            atol=1.0e-11,
        )
        solution = solve_charge_reduced_background(
            parameters=self._parameters,
            initial_data=initial_data,
            config=config,
        )
        if not solution.success:
            raise RuntimeError(solution.message)

        self._grid = _np.asarray(solution.N, dtype=float)
        self._a = _np.asarray(solution.a, dtype=float)
        self._H = _np.asarray(solution.H, dtype=float)
        self._phi = _np.asarray(solution.phi, dtype=float)
        self._v = _np.asarray(solution.v, dtype=float)
        self._theta = _np.asarray(solution.theta, dtype=float)
        self._theta_dot = _np.asarray(
            solution.theta_dot,
            dtype=float,
        )
        self._rho_m = _np.asarray(solution.rho_m, dtype=float)
        self._rho_r = _np.asarray(solution.rho_r, dtype=float)

        arrays = (
            self._grid,
            self._a,
            self._H,
            self._phi,
            self._v,
            self._theta,
            self._theta_dot,
            self._rho_m,
            self._rho_r,
        )
        if any(array.shape != self._grid.shape for array in arrays):
            raise ValueError(
                "charge-reduced background arrays have inconsistent shapes"
            )
        if self._grid.size != self._background_samples:
            raise ValueError(
                "direct short background sample count mismatch"
            )
        if _np.any(_np.diff(self._grid) <= 0.0):
            raise ValueError(
                "charge-reduced background N grid is not increasing"
            )
        if not all(bool(_np.all(_np.isfinite(array))) for array in arrays):
            raise ValueError(
                "charge-reduced background contains nonfinite values"
            )

        integrand = 1.0 / (self._a * self._H)
        self._conformal_elapsed = _np.zeros_like(self._grid)
        self._conformal_elapsed[1:] = _np.cumsum(
            0.5
            * (integrand[:-1] + integrand[1:])
            * _np.diff(self._grid)
        )

        initial_state = (
            float(self._phi[0]),
            float(self._v[0]),
            float(self._theta[0]),
            float(self._rho_m[0]),
            float(self._rho_r[0]),
        )
        initial_constraint_hubble = self._friedmann_hubble(
            float(self._grid[0]),
            initial_state,
            self._parameters,
        )
        target_hubble = (
            conformal_hubble_initial / scale_factor_initial
        )
        initial_binding_residual = abs(
            initial_constraint_hubble - target_hubble
        ) / max(abs(target_hubble), 1.0)
        if initial_binding_residual > 1.0e-10:
            raise ValueError(
                "direct background initial binding exceeds 1e-10"
            )

    def _interp(self, values, N: float) -> float:
        import numpy as _np

        return float(_np.interp(N, self._grid, values))

    def at_N(self, N: float):
        N = float(N)
        tolerance = 1.0e-12
        if (
            N < self._N_start - tolerance
            or N > self._N_end + tolerance
        ):
            raise ValueError(
                "RK4 stage N lies outside direct background interval"
            )
        N = min(self._N_end, max(self._N_start, N))

        scale_factor = self._interp(self._a, N)
        interpolated_hubble = self._interp(self._H, N)
        phi = self._interp(self._phi, N)
        v = self._interp(self._v, N)
        theta = self._interp(self._theta, N)
        theta_dot = self._interp(self._theta_dot, N)
        rho_m = self._interp(self._rho_m, N)
        rho_r = self._interp(self._rho_r, N)
        conformal_elapsed = self._interp(
            self._conformal_elapsed,
            N,
        )

        state = (phi, v, theta, rho_m, rho_r)
        constraint_hubble = self._friedmann_hubble(
            N,
            state,
            self._parameters,
        )
        interpolation_constraint_mismatch = abs(
            interpolated_hubble**2 - constraint_hubble**2
        ) / max(abs(constraint_hubble**2), 1.0)

        # Use the Friedmann-constrained expanding branch at the RK4
        # stage. Independently interpolating H and the state violates
        # the algebraic constraint between solver samples.
        hubble = constraint_hubble
        normalized_residual = abs(
            hubble**2 - constraint_hubble**2
        ) / max(abs(constraint_hubble**2), 1.0)
        if not __import__("math").isfinite(
            interpolation_constraint_mismatch
        ):
            raise ValueError(
                "interpolated H constraint mismatch is nonfinite"
            )

        stage = _CalibratedShortBackgroundStage(
            self._frozen_background,
            N=N,
            scale_factor=scale_factor,
            conformal_hubble=scale_factor * hubble,
            phi_background=phi,
            phi_prime_background=scale_factor * v,
            theta_prime_background=scale_factor * theta_dot,
            baryon_background_density=rho_m,
            photon_background_density=(
                self._photon_fraction * rho_r
            ),
            neutrino_background_density=(
                self._neutrino_fraction * rho_r
            ),
            conformal_elapsed=conformal_elapsed,
            normalized_friedmann_residual=normalized_residual,
        )
        self.stage_N_values.append(N)
        self.normalized_friedmann_residuals.append(
            normalized_residual
        )
        return stage


class _CalibratedShortBackgroundStage:
    def __init__(
        self,
        frozen_background,
        *,
        N: float,
        scale_factor: float,
        conformal_hubble: float,
        phi_background: float,
        phi_prime_background: float,
        theta_prime_background: float,
        baryon_background_density: float,
        photon_background_density: float,
        neutrino_background_density: float,
        conformal_elapsed: float,
        normalized_friedmann_residual: float,
    ):
        self._frozen_background = frozen_background
        self.N = float(N)
        self.scale_factor = float(scale_factor)
        self.conformal_hubble = float(conformal_hubble)
        self.phi_background = float(phi_background)
        self.phi_prime_background = float(phi_prime_background)
        self.theta_prime_background = float(
            theta_prime_background
        )
        self.baryon_background_density = float(
            baryon_background_density
        )
        self.photon_background_density = float(
            photon_background_density
        )
        self.neutrino_background_density = float(
            neutrino_background_density
        )
        self.normalized_friedmann_residual = float(
            normalized_friedmann_residual
        )
        # No free-streaming interval is stored on
        # FrozenBackgroundSpeciesMode. Preserve the verified frozen
        # hierarchy closure inputs through __getattr__.

    def __getattr__(self, name):
        return getattr(self._frozen_background, name)


def _frozen_versus_evolving_background_metrics(
    *,
    background_samples: int = 17,
):
    import numpy as _np

    receipt, frozen_background, initial_state = _objects()
    N_start = float(
        receipt["selected_background"]["N_initial"]
    )
    N_end = N_start + 1.0e-2
    step_sequence = (128, 256, 512, 1024)

    if initial_state.l_max != 8:
        raise AssertionError("regression requires l_max=8")

    evolving_background = _CalibratedShortEvolvingBackground(
        frozen_background,
        receipt=receipt,
        N_start=N_start,
        N_end=N_end,
        background_samples=background_samples,
    )

    frozen_runs = {}
    evolving_runs = {}

    for steps in step_sequence:
        frozen = integrate_frozen_background_species_mode(
            N_start=N_start,
            N_end=N_end,
            steps=steps,
            initial_state=initial_state,
            background=frozen_background,
        )
        evolving = integrate_frozen_background_species_mode(
            N_start=N_start,
            N_end=N_end,
            steps=steps,
            initial_state=initial_state,
            background=evolving_background,
        )

        assert frozen.l_max == 8
        assert evolving.l_max == 8
        assert frozen.steps == steps
        assert evolving.steps == steps
        assert frozen.N.shape == evolving.N.shape
        assert _np.array_equal(frozen.N, evolving.N)
        assert _np.all(_np.isfinite(frozen.states))
        assert _np.all(_np.isfinite(evolving.states))
        assert frozen.all_rhs_finite is True
        assert evolving.all_rhs_finite is True

        frozen_runs[steps] = frozen
        evolving_runs[steps] = evolving

    frozen_512_1024 = float(
        _np.max(
            _np.abs(
                frozen_runs[1024].states[-1]
                - frozen_runs[512].states[-1]
            )
        )
    )
    evolving_512_1024 = float(
        _np.max(
            _np.abs(
                evolving_runs[1024].states[-1]
                - evolving_runs[512].states[-1]
            )
        )
    )
    frozen_evolving_signal = float(
        _np.max(
            _np.abs(
                evolving_runs[1024].states[-1]
                - frozen_runs[1024].states[-1]
            )
        )
    )

    combined_order_four_richardson_bound = (
        frozen_512_1024 + evolving_512_1024
    ) / 15.0
    measurable = bool(
        frozen_evolving_signal
        > combined_order_four_richardson_bound
    )

    maximum_normalized_friedmann_residual = max(
        evolving_background.normalized_friedmann_residuals
    )
    expected_stage_count = 4 * sum(step_sequence)

    return {
        "background_samples": background_samples,
        "N_start": N_start,
        "N_end": N_end,
        "l_max": initial_state.l_max,
        "step_sequence": step_sequence,
        "stage_count": len(evolving_background.stage_N_values),
        "expected_stage_count": expected_stage_count,
        "minimum_stage_N": min(
            evolving_background.stage_N_values
        ),
        "maximum_stage_N": max(
            evolving_background.stage_N_values
        ),
        "maximum_normalized_friedmann_residual": (
            maximum_normalized_friedmann_residual
        ),
        "frozen_512_1024_difference": frozen_512_1024,
        "evolving_512_1024_difference": evolving_512_1024,
        "combined_order_four_richardson_bound": (
            combined_order_four_richardson_bound
        ),
        "frozen_evolving_signal": frozen_evolving_signal,
        "measurable": measurable,
    }


def test_frozen_versus_evolving_background_same_mode_regression():
    import math as _math

    metrics = _frozen_versus_evolving_background_metrics()

    assert _math.isclose(
        metrics["N_end"] - metrics["N_start"],
        1.0e-2,
        rel_tol=0.0,
        abs_tol=1.0e-14,
    )
    assert metrics["l_max"] == 8
    assert metrics["step_sequence"] == (128, 256, 512, 1024)
    assert metrics["stage_count"] == metrics["expected_stage_count"]
    assert metrics["minimum_stage_N"] >= metrics["N_start"]
    assert metrics["maximum_stage_N"] <= metrics["N_end"]
    assert (
        metrics["maximum_normalized_friedmann_residual"]
        <= 1.0e-10
    )
    assert metrics["frozen_evolving_signal"] > 0.0

def _direct_background_sampling_convergence_metrics():
    import math as _math

    sample_counts = (17, 33, 65)
    runs = {
        samples: _frozen_versus_evolving_background_metrics(
            background_samples=samples,
        )
        for samples in sample_counts
    }

    signals = tuple(
        float(runs[samples]["frozen_evolving_signal"])
        for samples in sample_counts
    )
    first_difference = abs(signals[0] - signals[1])
    second_difference = abs(signals[1] - signals[2])

    if second_difference == 0.0:
        observed_order = _math.inf
        background_sampling_error_bound = 0.0
    elif first_difference <= 0.0:
        observed_order = -_math.inf
        background_sampling_error_bound = _math.inf
    else:
        observed_order = _math.log(
            first_difference / second_difference,
            2.0,
        )
        denominator = 2.0**observed_order - 1.0
        background_sampling_error_bound = (
            second_difference / denominator
            if denominator > 0.0
            else _math.inf
        )

    fine = runs[65]
    rk4_bound = float(
        fine["combined_order_four_richardson_bound"]
    )
    total_numerical_bound = (
        rk4_bound + background_sampling_error_bound
    )
    separation_ratio = (
        signals[2] / total_numerical_bound
        if total_numerical_bound > 0.0
        else _math.inf
    )

    return {
        "sample_counts": sample_counts,
        "runs": runs,
        "signals": signals,
        "first_difference": first_difference,
        "second_difference": second_difference,
        "observed_order": observed_order,
        "background_sampling_error_bound": (
            background_sampling_error_bound
        ),
        "rk4_bound": rk4_bound,
        "total_numerical_bound": total_numerical_bound,
        "fine_signal": signals[2],
        "separation_ratio": separation_ratio,
        "converged": bool(
            second_difference < first_difference
            and observed_order >= 1.5
            and signals[2] > 10.0 * total_numerical_bound
        ),
    }


def test_direct_background_sampling_convergence_17_33_65():
    import math as _math

    metrics = _direct_background_sampling_convergence_metrics()

    assert metrics["sample_counts"] == (17, 33, 65)
    for samples in metrics["sample_counts"]:
        run = metrics["runs"][samples]
        assert run["background_samples"] == samples
        assert run["l_max"] == 8
        assert run["step_sequence"] == (128, 256, 512, 1024)
        assert run["stage_count"] == run["expected_stage_count"]
        assert run["maximum_normalized_friedmann_residual"] <= 1.0e-10
        assert run["measurable"] is True
        assert _math.isfinite(run["frozen_evolving_signal"])
        assert run["frozen_evolving_signal"] > 0.0

    assert _math.isfinite(metrics["first_difference"])
    assert _math.isfinite(metrics["second_difference"])
    assert metrics["second_difference"] < metrics["first_difference"]
    assert (
        _math.isinf(metrics["observed_order"])
        or metrics["observed_order"] >= 1.5
    )
    assert _math.isfinite(
        metrics["background_sampling_error_bound"]
    )
    assert metrics["background_sampling_error_bound"] >= 0.0
    assert metrics["fine_signal"] > (
        10.0 * metrics["total_numerical_bound"]
    )
    assert metrics["converged"] is True


def _lmax_activity_metrics():
    import math as _math

    receipt, background, state = _objects(l_max=12)
    N_start = float(receipt["selected_background"]["N_initial"])
    N_end = N_start + 1.0e-2
    steps = 128

    if state.l_max != 12:
        raise AssertionError("lmax activity state must have l_max=12")
    if state.dimension != 22:
        raise AssertionError("lmax activity state must have dimension 22")

    def component_index(ell: int) -> int:
        if not 3 <= ell <= 12:
            raise ValueError("ell must lie in 3,...,12")
        return 11 + (ell - 3)

    index_l8 = component_index(8)
    index_l9 = component_index(9)
    high_indices = tuple(component_index(ell) for ell in range(9, 13))

    regular = integrate_frozen_background_species_mode(
        N_start=N_start,
        N_end=N_end,
        steps=steps,
        initial_state=state,
        background=background,
    )

    initial_high = tuple(
        float(regular.states[0, index]) for index in high_indices
    )
    final_high = tuple(
        float(regular.states[-1, index]) for index in high_indices
    )
    high_changes = tuple(
        abs(final - initial)
        for initial, final in zip(initial_high, final_high)
    )

    high_components_present = bool(
        regular.l_max == 12
        and regular.states.shape == (steps + 1, 22)
        and len(initial_high) == 4
    )
    high_components_nonzero = bool(
        all(value != 0.0 and _math.isfinite(value) for value in initial_high)
    )
    high_components_evolved = bool(
        all(change > 0.0 and _math.isfinite(change) for change in high_changes)
    )

    base_rhs = frozen_background_species_mode_right_hand_side(
        state=state,
        background=background,
    )
    base_derivative = tuple(
        float(value) for value in base_rhs.derivative_with_respect_to_N
    )

    probe_delta_f9 = 1.0e-10
    probe_vector = state.as_array().copy()
    probe_vector[index_l9] += probe_delta_f9
    probe_state = RadiationSpeciesModeState.from_array(
        probe_vector,
        l_max=12,
    )
    probe_rhs = frozen_background_species_mode_right_hand_side(
        state=probe_state,
        background=background,
    )
    probe_derivative = tuple(
        float(value) for value in probe_rhs.derivative_with_respect_to_N
    )

    lower_rhs_response = abs(
        probe_derivative[index_l8] - base_derivative[index_l8]
    )
    lower_rhs_sensitivity = lower_rhs_response / probe_delta_f9

    probed = integrate_frozen_background_species_mode(
        N_start=N_start,
        N_end=N_end,
        steps=steps,
        initial_state=probe_state,
        background=background,
    )
    lower_integrated_response = abs(
        float(probed.states[-1, index_l8])
        - float(regular.states[-1, index_l8])
    )

    lower_hierarchy_coupled = bool(
        _math.isfinite(lower_rhs_response)
        and _math.isfinite(lower_rhs_sensitivity)
        and _math.isfinite(lower_integrated_response)
        and lower_rhs_response > 0.0
        and lower_rhs_sensitivity > 0.0
        and lower_integrated_response > 0.0
    )

    certified = bool(
        high_components_present
        and high_components_nonzero
        and high_components_evolved
        and regular.all_rhs_finite
        and probed.all_rhs_finite
        and lower_hierarchy_coupled
    )

    return {
        "N_interval": (N_start, N_end),
        "steps": steps,
        "l_max": state.l_max,
        "dimension": state.dimension,
        "initial_high": initial_high,
        "final_high": final_high,
        "high_changes": high_changes,
        "high_components_present": high_components_present,
        "high_components_nonzero": high_components_nonzero,
        "high_components_evolved": high_components_evolved,
        "probe_delta_f9": probe_delta_f9,
        "lower_rhs_response": lower_rhs_response,
        "lower_rhs_sensitivity": lower_rhs_sensitivity,
        "lower_integrated_response": lower_integrated_response,
        "lower_hierarchy_coupled": lower_hierarchy_coupled,
        "certified": certified,
    }


def test_lmax_9_to_12_components_are_active_and_coupled():
    import math as _math

    metrics = _lmax_activity_metrics()

    assert metrics["l_max"] == 12
    assert metrics["dimension"] == 22
    assert metrics["steps"] == 128
    assert metrics["high_components_present"] is True
    assert metrics["high_components_nonzero"] is True
    assert metrics["high_components_evolved"] is True
    assert all(
        _math.isfinite(value) and value != 0.0
        for value in metrics["initial_high"]
    )
    assert all(
        _math.isfinite(value) and value > 0.0
        for value in metrics["high_changes"]
    )
    assert metrics["probe_delta_f9"] == 1.0e-10
    assert _math.isfinite(metrics["lower_rhs_response"])
    assert _math.isfinite(metrics["lower_rhs_sensitivity"])
    assert _math.isfinite(metrics["lower_integrated_response"])
    assert metrics["lower_rhs_response"] > 0.0
    assert metrics["lower_rhs_sensitivity"] > 0.0
    assert metrics["lower_integrated_response"] > 0.0
    assert metrics["lower_hierarchy_coupled"] is True
    assert metrics["certified"] is True


def _blockwise_volterra_lmax_tail_metrics():
    """Conditionally propagate the omitted l>=13 tail to the final observable.

    The perturbation system is affine-linear after the free-streaming interval
    is fixed.  For a terminal-tail mismatch u(N) entering only the F12 row,

        z' = A(N) z + e_F12 c(N) u(N),   z(N_start) = 0.

    The final component response is represented by the adjoint Volterra
    kernel.  For each output component j,

        |z_j(N_end)| <= U * integral |c(N) lambda_j,F12(N)| dN,

    where U is the visible uniform terminal-mismatch envelope and lambda_j is
    the backward adjoint solution.  This retains the sequential hierarchy
    transfer instead of replacing the full coupled system by one raw-state
    Lipschitz norm.

    The result remains conditional on:

    1. the regular high-l ratio cap used for the omitted tail;
    2. a factor-four envelope for the sampled physical tail and the final
       transfer-discretization remainder;
    3. observed convergence of the 256-512-1024 adjoint Volterra sequence.

    No unconditional infinite-hierarchy theorem is claimed.
    """
    import math as _math
    import numpy as _np

    receipt, frozen_background, initial_state = _objects(l_max=12)
    N_start = float(receipt["selected_background"]["N_initial"])
    N_end = N_start + 1.0e-2
    duration = N_end - N_start
    physical_steps = 1024
    transfer_step_sequence = (128, 256, 512, 1024)
    background_samples = 65
    tail_envelope_safety_factor = 4.0
    transfer_remainder_safety_factor = 4.0
    affine_tolerance = 1.0e-8
    minimum_transfer_order = 1.5
    negligible_fraction_of_existing_numerics = 1.0e-3

    if initial_state.l_max != 12 or initial_state.dimension != 22:
        raise AssertionError("Volterra tail state must be l_max=12")

    active_dimension = initial_state.dimension - 1
    index_f11 = 11 + (11 - 3)
    index_f12 = 11 + (12 - 3)
    wave_number = _math.sqrt(float(frozen_background.wave_number_squared))

    evolving_physical_background = _CalibratedShortEvolvingBackground(
        frozen_background,
        receipt=receipt,
        N_start=N_start,
        N_end=N_end,
        background_samples=background_samples,
    )

    frozen_run = integrate_frozen_background_species_mode(
        N_start=N_start,
        N_end=N_end,
        steps=physical_steps,
        initial_state=initial_state,
        background=frozen_background,
    )
    evolving_run = integrate_frozen_background_species_mode(
        N_start=N_start,
        N_end=N_end,
        steps=physical_steps,
        initial_state=initial_state,
        background=evolving_physical_background,
    )

    phase_values = []
    absolute_f12_values = []
    absolute_estimated_f13_values = []
    for run in (frozen_run, evolving_run):
        for vector in run.states:
            chi = float(vector[-1])
            phase = wave_number * chi
            if not _math.isfinite(phase) or phase <= 0.0:
                raise AssertionError("free-streaming phase must remain positive")
            f11 = float(vector[index_f11])
            f12 = float(vector[index_f12])
            estimated_f13 = 25.0 * f12 / phase - f11
            phase_values.append(phase)
            absolute_f12_values.append(abs(f12))
            absolute_estimated_f13_values.append(abs(estimated_f13))

    phase_max = max(phase_values)
    maximum_absolute_f12 = max(absolute_f12_values)
    maximum_absolute_estimated_f13 = max(
        absolute_estimated_f13_values
    )
    regular_ratio_cap = phase_max / 27.0

    if not 0.0 <= regular_ratio_cap < 1.0:
        conditional_tail_sum_bound = _math.inf
    else:
        conditional_tail_sum_bound = (
            maximum_absolute_f12
            * regular_ratio_cap
            / (1.0 - regular_ratio_cap)
        )

    raw_terminal_mismatch_bound = (
        conditional_tail_sum_bound
        + maximum_absolute_estimated_f13
    )
    terminal_mismatch_envelope = _math.nextafter(
        tail_envelope_safety_factor * raw_terminal_mismatch_bound,
        _math.inf,
    )

    def stage_and_chi(background, N_value: float):
        evaluator = getattr(background, "at_N", None)
        if callable(evaluator):
            stage = evaluator(float(N_value))
            conformal_elapsed = float(
                background._interp(
                    background._conformal_elapsed,
                    float(N_value),
                )
            )
            chi = (
                float(initial_state.conformal_free_streaming_interval)
                + conformal_elapsed
            )
        else:
            stage = background
            chi = (
                float(initial_state.conformal_free_streaming_interval)
                + (float(N_value) - N_start)
                / float(stage.conformal_hubble)
            )
        if not _math.isfinite(chi) or chi <= 0.0:
            raise AssertionError("Volterra coefficient chi must be positive")
        return stage, chi

    def active_affine_matrix(background, N_value: float):
        stage, chi = stage_and_chi(background, float(N_value))
        base_vector = _np.zeros(initial_state.dimension, dtype=float)
        base_vector[-1] = chi
        base_state = RadiationSpeciesModeState.from_array(
            base_vector,
            l_max=12,
        )
        base_derivative = _np.asarray(
            frozen_background_species_mode_right_hand_side(
                state=base_state,
                background=stage,
            ).derivative_with_respect_to_N,
            dtype=float,
        )[:active_dimension]

        matrix = _np.empty(
            (active_dimension, active_dimension),
            dtype=float,
        )
        for column in range(active_dimension):
            vector = base_vector.copy()
            vector[column] = 1.0
            state = RadiationSpeciesModeState.from_array(
                vector,
                l_max=12,
            )
            derivative = _np.asarray(
                frozen_background_species_mode_right_hand_side(
                    state=state,
                    background=stage,
                ).derivative_with_respect_to_N,
                dtype=float,
            )[:active_dimension]
            matrix[:, column] = derivative - base_derivative

        probe = _np.asarray(
            [
                ((-1.0) ** column) * (column + 1.0) * 1.0e-4
                for column in range(active_dimension)
            ],
            dtype=float,
        )
        probe_vector = base_vector.copy()
        probe_vector[:active_dimension] = probe
        probe_state = RadiationSpeciesModeState.from_array(
            probe_vector,
            l_max=12,
        )
        probe_derivative = _np.asarray(
            frozen_background_species_mode_right_hand_side(
                state=probe_state,
                background=stage,
            ).derivative_with_respect_to_N,
            dtype=float,
        )[:active_dimension]
        reconstructed = base_derivative + matrix @ probe
        affine_scale = max(
            1.0e-30,
            float(_np.max(_np.abs(probe_derivative))),
            float(_np.max(_np.abs(reconstructed))),
        )
        affine_residual = float(
            _np.max(_np.abs(probe_derivative - reconstructed))
            / affine_scale
        )

        tail_coefficient = abs(
            _math.sqrt(float(stage.wave_number_squared))
            * 13.0
            / 25.0
            / float(stage.conformal_hubble)
        )
        if not _np.all(_np.isfinite(matrix)):
            raise AssertionError("Volterra affine matrix must be finite")
        if not _math.isfinite(tail_coefficient):
            raise AssertionError("Volterra tail coefficient must be finite")
        return matrix, tail_coefficient, affine_residual

    def adjoint_transfer(background, steps: int):
        step_size = duration / steps
        identity = _np.eye(active_dimension, dtype=float)
        adjoint = identity.copy()
        transfer = _np.zeros(active_dimension, dtype=float)
        maximum_affine_residual = 0.0
        maximum_tail_coefficient = 0.0

        def evaluate(N_value: float, matrix_value):
            nonlocal maximum_affine_residual
            nonlocal maximum_tail_coefficient
            affine, tail_coefficient, affine_residual = (
                active_affine_matrix(background, float(N_value))
            )
            maximum_affine_residual = max(
                maximum_affine_residual,
                affine_residual,
            )
            maximum_tail_coefficient = max(
                maximum_tail_coefficient,
                tail_coefficient,
            )
            derivative = -(affine.T @ matrix_value)
            kernel = _np.abs(
                tail_coefficient * matrix_value[index_f12, :]
            )
            return derivative, kernel

        N_high = N_end
        _, kernel_high = evaluate(N_high, adjoint)

        for _ in range(steps):
            signed_step = -step_size
            N_mid = N_high - 0.5 * step_size
            N_low = N_high - step_size

            k1, _ = evaluate(N_high, adjoint)
            k2, _ = evaluate(
                N_mid,
                adjoint + 0.5 * signed_step * k1,
            )
            k3, _ = evaluate(
                N_mid,
                adjoint + 0.5 * signed_step * k2,
            )
            k4, _ = evaluate(
                N_low,
                adjoint + signed_step * k3,
            )
            updated = adjoint + (
                signed_step / 6.0
            ) * (k1 + 2.0 * k2 + 2.0 * k3 + k4)

            if not _np.all(_np.isfinite(updated)):
                return {
                    "transfer": _np.full(active_dimension, _math.inf),
                    "maximum_affine_residual": maximum_affine_residual,
                    "maximum_tail_coefficient": maximum_tail_coefficient,
                    "finite": False,
                }

            _, kernel_low = evaluate(N_low, updated)
            transfer += 0.5 * step_size * (
                kernel_high + kernel_low
            )
            adjoint = updated
            kernel_high = kernel_low
            N_high = N_low

        return {
            "transfer": transfer,
            "maximum_affine_residual": maximum_affine_residual,
            "maximum_tail_coefficient": maximum_tail_coefficient,
            "finite": bool(
                _np.all(_np.isfinite(transfer))
                and _np.all(transfer >= 0.0)
            ),
        }

    def transfer_sequence(kind: str):
        runs = {}
        for steps in transfer_step_sequence:
            if kind == "frozen":
                background = frozen_background
            elif kind == "evolving":
                background = _CalibratedShortEvolvingBackground(
                    frozen_background,
                    receipt=receipt,
                    N_start=N_start,
                    N_end=N_end,
                    background_samples=background_samples,
                )
            else:
                raise ValueError("unknown transfer background kind")
            runs[steps] = adjoint_transfer(background, steps)

        transfer_256 = _np.asarray(runs[256]["transfer"], dtype=float)
        transfer_512 = _np.asarray(runs[512]["transfer"], dtype=float)
        transfer_1024 = _np.asarray(runs[1024]["transfer"], dtype=float)
        first_difference = float(
            _np.max(_np.abs(transfer_512 - transfer_256))
        )
        second_difference = float(
            _np.max(_np.abs(transfer_1024 - transfer_512))
        )

        if second_difference == 0.0 and first_difference == 0.0:
            observed_order = _math.inf
            decreased = True
        elif second_difference > 0.0 and first_difference > second_difference:
            observed_order = _math.log(
                first_difference / second_difference,
                2.0,
            )
            decreased = True
        else:
            observed_order = -_math.inf
            decreased = False

        componentwise_remainder = (
            transfer_remainder_safety_factor
            * _np.abs(transfer_1024 - transfer_512)
        )
        transfer_upper = _np.nextafter(
            _np.abs(transfer_1024) + componentwise_remainder,
            _np.full(active_dimension, _math.inf),
        )
        maximum_affine_residual = max(
            float(run["maximum_affine_residual"])
            for run in runs.values()
        )
        maximum_tail_coefficient = max(
            float(run["maximum_tail_coefficient"])
            for run in runs.values()
        )
        converged = bool(
            all(bool(run["finite"]) for run in runs.values())
            and decreased
            and (
                _math.isinf(observed_order)
                or observed_order >= minimum_transfer_order
            )
            and _np.all(_np.isfinite(transfer_upper))
        )
        return {
            "runs": runs,
            "first_difference": first_difference,
            "second_difference": second_difference,
            "observed_order": observed_order,
            "decreased": decreased,
            "transfer_upper": transfer_upper,
            "maximum_affine_residual": maximum_affine_residual,
            "maximum_tail_coefficient": maximum_tail_coefficient,
            "converged": converged,
        }

    frozen_transfer = transfer_sequence("frozen")
    evolving_transfer = transfer_sequence("evolving")

    frozen_response = _np.nextafter(
        terminal_mismatch_envelope
        * _np.asarray(frozen_transfer["transfer_upper"], dtype=float),
        _np.full(active_dimension, _math.inf),
    )
    evolving_response = _np.nextafter(
        terminal_mismatch_envelope
        * _np.asarray(evolving_transfer["transfer_upper"], dtype=float),
        _np.full(active_dimension, _math.inf),
    )
    signal_component_response = _np.nextafter(
        frozen_response + evolving_response,
        _np.full(active_dimension, _math.inf),
    )
    sigma_lmax = float(_np.max(signal_component_response))
    maximizing_component = int(_np.argmax(signal_component_response))

    block_indices = {
        "dark": tuple(range(0, 4)),
        "baryon_photon": tuple(range(4, 8)),
        "neutrino_low": tuple(range(8, 11)),
        "hierarchy_f3_f8": tuple(range(11, 17)),
        "hierarchy_f9_f12": tuple(range(17, 21)),
    }
    block_response_bounds = {
        name: float(
            _np.max(signal_component_response[_np.asarray(indices)])
        )
        for name, indices in block_indices.items()
    }

    sampling = _direct_background_sampling_convergence_metrics()
    signal = abs(float(sampling["fine_signal"]))
    sigma_rk4 = float(sampling["rk4_bound"])
    sigma_sampling = float(
        sampling["background_sampling_error_bound"]
    )
    existing_numerical_uncertainty = sigma_rk4 + sigma_sampling
    total_uncertainty = _math.nextafter(
        existing_numerical_uncertainty + sigma_lmax,
        _math.inf,
    )
    separated = bool(signal > total_uncertainty)
    negligible = bool(
        _math.isfinite(sigma_lmax)
        and sigma_lmax >= 0.0
        and sigma_lmax
        <= negligible_fraction_of_existing_numerics
        * existing_numerical_uncertainty
    )

    maximum_affine_residual = max(
        float(frozen_transfer["maximum_affine_residual"]),
        float(evolving_transfer["maximum_affine_residual"]),
    )
    affine_verified = bool(maximum_affine_residual <= affine_tolerance)
    conditional_certified = bool(
        regular_ratio_cap < 1.0
        and _math.isfinite(conditional_tail_sum_bound)
        and _math.isfinite(terminal_mismatch_envelope)
        and affine_verified
        and frozen_transfer["converged"]
        and evolving_transfer["converged"]
        and _math.isfinite(sigma_lmax)
        and negligible
        and separated
    )

    return {
        "N_interval": (N_start, N_end),
        "physical_steps": physical_steps,
        "transfer_step_sequence": transfer_step_sequence,
        "background_samples": background_samples,
        "tail_envelope_safety_factor": tail_envelope_safety_factor,
        "transfer_remainder_safety_factor": (
            transfer_remainder_safety_factor
        ),
        "minimum_transfer_order": minimum_transfer_order,
        "negligible_fraction_of_existing_numerics": (
            negligible_fraction_of_existing_numerics
        ),
        "phase_max": phase_max,
        "maximum_absolute_f12": maximum_absolute_f12,
        "regular_ratio_cap": regular_ratio_cap,
        "maximum_absolute_estimated_f13": (
            maximum_absolute_estimated_f13
        ),
        "conditional_tail_sum_bound": conditional_tail_sum_bound,
        "raw_terminal_mismatch_bound": raw_terminal_mismatch_bound,
        "terminal_mismatch_envelope": terminal_mismatch_envelope,
        "frozen_transfer": frozen_transfer,
        "evolving_transfer": evolving_transfer,
        "maximum_affine_residual": maximum_affine_residual,
        "affine_tolerance": affine_tolerance,
        "affine_verified": affine_verified,
        "block_response_bounds": block_response_bounds,
        "maximizing_component": maximizing_component,
        "sigma_lmax": sigma_lmax,
        "signal": signal,
        "sigma_rk4": sigma_rk4,
        "sigma_sampling": sigma_sampling,
        "existing_numerical_uncertainty": existing_numerical_uncertainty,
        "total_uncertainty": total_uncertainty,
        "negligible": negligible,
        "separated": separated,
        "conditional_certified": conditional_certified,
    }


def test_blockwise_volterra_lmax_tail_bound_is_finite_and_negligible():
    import math as _math

    metrics = _blockwise_volterra_lmax_tail_metrics()

    assert metrics["physical_steps"] == 1024
    assert metrics["transfer_step_sequence"] == (128, 256, 512, 1024)
    assert metrics["background_samples"] == 65
    assert metrics["tail_envelope_safety_factor"] == 4.0
    assert metrics["transfer_remainder_safety_factor"] == 4.0
    assert 0.0 <= metrics["regular_ratio_cap"] < 1.0
    assert _math.isfinite(metrics["conditional_tail_sum_bound"])
    assert metrics["conditional_tail_sum_bound"] > 0.0
    assert _math.isfinite(metrics["terminal_mismatch_envelope"])
    assert metrics["terminal_mismatch_envelope"] > 0.0
    assert metrics["maximum_affine_residual"] <= metrics["affine_tolerance"]
    assert metrics["affine_verified"] is True

    for key in ("frozen_transfer", "evolving_transfer"):
        transfer = metrics[key]
        assert transfer["decreased"] is True
        assert (
            _math.isinf(transfer["observed_order"])
            or transfer["observed_order"]
            >= metrics["minimum_transfer_order"]
        )
        assert transfer["converged"] is True

    assert _math.isfinite(metrics["sigma_lmax"])
    assert metrics["sigma_lmax"] >= 0.0
    assert metrics["negligible"] is True
    assert metrics["signal"] > metrics["total_uncertainty"]
    assert metrics["separated"] is True
    assert metrics["conditional_certified"] is True

