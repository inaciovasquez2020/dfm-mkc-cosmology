"""Regression for the merged circular complete-cycle growth observable."""

from __future__ import annotations

from pathlib import Path
import json
import math

import pytest

from dfm_mkc_solver.averaged_full_field_time_dependent_comparison_v1 import (
    compare_averaged_and_time_dependent_full_field_growth,
)
from dfm_mkc_solver.charge_reduced_background_v1 import (
    ChargeReducedInitialData,
    ChargeReducedParameters,
    ChargeReducedSolverConfig,
    build_dfm_cdm_unit_map,
)


RECEIPT = Path(
    "artifacts/dfm_mkc/"
    "dfm_cdm_minimal_circular_solution_receipt_2026_07_21.json"
)


def test_merged_circular_complete_cycle_observable() -> None:
    receipt = json.loads(RECEIPT.read_text())

    (
        phi_initial,
        v_initial,
        rho_star,
        m_phi_squared,
        lambda_phi,
        q_theta,
    ) = map(float, receipt["candidate_vector"])

    unit_inputs = receipt["unit_map_inputs"]
    unit_map = build_dfm_cdm_unit_map(
        H0_km_s_Mpc=float(unit_inputs["H0_km_s_Mpc"]),
        omega_b0=float(unit_inputs["omega_b0"]),
        omega_cdm0=float(unit_inputs["omega_cdm0"]),
        omega_r0=float(unit_inputs["omega_r0"]),
    )

    config_inputs = receipt["solver_config"]

    config = ChargeReducedSolverConfig(
        N_initial=float(config_inputs["N_initial"]),
        N_final=0.3,
        samples=401,
        rtol=float(config_inputs["rtol"]),
        atol=float(config_inputs["atol"]),
    )

    rho_m_initial, rho_r_initial = (
        unit_map.fluid_initial_data(config.N_initial)
    )

    parameters = ChargeReducedParameters(
        G=unit_map.G_code,
        Lambda=unit_map.Lambda_code,
        alpha=float(receipt["alpha"]),
        beta=float(receipt["beta"]),
        rho_star=rho_star,
        m_phi_squared=m_phi_squared,
        lambda_phi=lambda_phi,
        Q_theta=q_theta,
    )

    comparison = compare_averaged_and_time_dependent_full_field_growth(
        parameters=parameters,
        initial_data=ChargeReducedInitialData(
            phi=phi_initial,
            v=v_initial,
            theta=0.0,
            rho_m=rho_m_initial,
            rho_r=rho_r_initial,
        ),
        config=config,
        wave_number=0.005,
        target_density_contrast=1.0e-6,
        cycle_count=1,
    )

    assert comparison.initial_matching_surface_closed
    assert comparison.initial_metric_fixed_point_solved
    assert comparison.metric_constraints_solved_at_each_sample
    assert comparison.time_dependent_full_field_evolved
    assert comparison.phase_cycle_averaging_computed
    assert comparison.averaged_full_field_comparison_computed
    assert (
        comparison
        .gauge_invariant_regular_mode_normalization_certificate
        is None
    )

    assert comparison.phase_span > 2.0 * math.pi
    assert comparison.maximum_rhs_residual < 1.0e-14
    assert comparison.minimum_abs_constraint_denominator > 0.25

    assert math.isclose(
        comparison.full_field_growth_factor,
        0.99386114336848497,
        rel_tol=1.0e-8,
        abs_tol=1.0e-10,
    )
    expected_cdm_growth = (
        comparison.final_cycle_midpoint_scale_factor
        / comparison.initial_cycle_midpoint_scale_factor
    )
    assert expected_cdm_growth > 0.0
    assert math.isclose(
        comparison.cdm_growth_factor,
        expected_cdm_growth,
        rel_tol=1.0e-10,
        abs_tol=1.0e-12,
    )
    assert math.isclose(
        comparison.full_field_growth_suppression,
        comparison.full_field_growth_factor
        / comparison.cdm_growth_factor,
        rel_tol=1.0e-12,
        abs_tol=1.0e-14,
    )
    assert math.isclose(
        comparison.averaged_growth_factor,
        1.0211620958708991,
        rel_tol=1.0e-8,
        abs_tol=1.0e-10,
    )
    assert math.isclose(
        comparison.full_to_averaged_growth_ratio,
        0.97326481994111769,
        rel_tol=1.0e-8,
        abs_tol=1.0e-10,
    )
    assert math.isclose(
        comparison.relative_growth_difference,
        -0.026735180058882313,
        rel_tol=1.0e-8,
        abs_tol=1.0e-10,
    )


def test_regular_mode_common_amplitude_rescaling_invariance() -> None:
    receipt = json.loads(RECEIPT.read_text())
    phi_initial, v_initial, rho_star, m2, coupling, charge = map(
        float, receipt["candidate_vector"]
    )
    inputs = receipt["unit_map_inputs"]
    unit_map = build_dfm_cdm_unit_map(
        H0_km_s_Mpc=float(inputs["H0_km_s_Mpc"]),
        omega_b0=float(inputs["omega_b0"]),
        omega_cdm0=float(inputs["omega_cdm0"]),
        omega_r0=float(inputs["omega_r0"]),
    )
    config_inputs = receipt["solver_config"]
    config = ChargeReducedSolverConfig(
        N_initial=float(config_inputs["N_initial"]),
        N_final=0.3,
        samples=401,
        rtol=float(config_inputs["rtol"]),
        atol=float(config_inputs["atol"]),
    )
    rho_m, rho_r = unit_map.fluid_initial_data(config.N_initial)
    parameters = ChargeReducedParameters(
        G=unit_map.G_code,
        Lambda=unit_map.Lambda_code,
        alpha=float(receipt["alpha"]),
        beta=float(receipt["beta"]),
        rho_star=rho_star,
        m_phi_squared=m2,
        lambda_phi=coupling,
        Q_theta=charge,
    )
    data = ChargeReducedInitialData(
        phi=phi_initial,
        v=v_initial,
        theta=0.0,
        rho_m=rho_m,
        rho_r=rho_r,
    )

    results = []
    for amplitude in (1.0e-6, 2.0e-6, -1.0e-6):
        results.append(
            compare_averaged_and_time_dependent_full_field_growth(
                parameters=parameters,
                initial_data=data,
                config=config,
                wave_number=0.005,
                cycle_count=1,
                derive_regular_growing_mode_initial_state=True,
                initial_mode_amplitude=amplitude,
            )
        )

    base, doubled, negative = results
    assert base.regular_growing_mode_certificate is not None
    assert doubled.regular_growing_mode_certificate is not None
    assert negative.regular_growing_mode_certificate is not None
    assert math.isclose(
        doubled.derived_initial_density_contrast,
        2.0 * base.derived_initial_density_contrast,
        rel_tol=1.0e-12,
    )
    assert math.isclose(
        negative.derived_initial_density_contrast,
        -base.derived_initial_density_contrast,
        rel_tol=1.0e-12,
    )
    assert math.isclose(
        doubled.derived_initial_density_contrast_n,
        2.0 * base.derived_initial_density_contrast_n,
        rel_tol=1.0e-12,
    )
    assert math.isclose(
        negative.derived_initial_density_contrast_n,
        -base.derived_initial_density_contrast_n,
        rel_tol=1.0e-12,
    )
    for result in results:
        certificate = result.regular_growing_mode_certificate
        assert certificate is not None
        assert result.initial_metric_fixed_point_solved
        assert result.initial_matching_surface_closed
        assert certificate.metric_constraints_solved
        assert certificate.initial_matching_surface_closed
        assert certificate.total_density_derivative_certified
        normalization = (
            result
            .gauge_invariant_regular_mode_normalization_certificate
        )
        assert normalization is not None
        assert normalization.background_density_derivative_separated
        assert (
            normalization
            .initial_uniform_density_curvature_gauge_invariant
        )
        assert normalization.gauge_invariant_normalization_closed
        assert not normalization.global_gauge_invariant_observable_completed
        assert not normalization.lcdm_tangent_separation_completed
        assert not normalization.observational_calibration_completed
        assert math.isclose(
            result.derived_initial_density_contrast_n,
            certificate.derived_density_contrast_n,
            rel_tol=0.0,
            abs_tol=0.0,
        )
        assert not result.observational_calibration_completed
        assert not certificate.observational_calibration_completed
    assert results[0].gauge_invariant_regular_mode_normalization_certificate
    base_normalized = (
        results[0]
        .gauge_invariant_regular_mode_normalization_certificate
        .normalized_initial_state
    )
    for result in results[1:]:
        assert (
            result
            .gauge_invariant_regular_mode_normalization_certificate
            .normalized_initial_state
            == pytest.approx(base_normalized, rel=2.0e-10, abs=2.0e-12)
        )
    for field in (
        "full_field_growth_factor",
        "cdm_growth_factor",
        "full_field_growth_suppression",
    ):
        assert math.isclose(
            getattr(doubled, field),
            getattr(base, field),
            rel_tol=2.0e-9,
            abs_tol=2.0e-11,
        )
        assert math.isclose(
            getattr(negative, field),
            getattr(base, field),
            rel_tol=2.0e-9,
            abs_tol=2.0e-11,
        )

def test_non_lambda_dark_energy_enthalpy_enters_hubble_derivative() -> None:
    from dfm_mkc_solver.averaged_full_field_time_dependent_comparison_v1 import (
        _cosmic_hubble_n_from_background_fields,
    )

    log_scale_factor = math.log(0.5)
    parameters = ChargeReducedParameters(
        G=1.0 / (8.0 * math.pi),
        w0=-0.9,
        wa=0.2,
    )
    dark_energy_density = 3.0
    hubble = 2.0

    actual = _cosmic_hubble_n_from_background_fields(
        parameters=parameters,
        log_scale_factor=log_scale_factor,
        hubble=hubble,
        phi=1.0,
        velocity=0.0,
        theta_dot=0.0,
        matter_density=0.0,
        radiation_density=0.0,
        dark_energy_density=dark_energy_density,
    )

    scale_factor = math.exp(log_scale_factor)
    equation_of_state = (
        parameters.w0
        + parameters.wa * (1.0 - scale_factor)
    )
    expected = (
        -4.0
        * math.pi
        * parameters.G
        * (1.0 + equation_of_state)
        * dark_energy_density
        / hubble
    )

    assert equation_of_state != -1.0
    assert math.isclose(
        actual,
        expected,
        rel_tol=1.0e-15,
        abs_tol=1.0e-15,
    )
