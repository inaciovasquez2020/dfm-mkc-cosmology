"""Regression for the merged circular complete-cycle growth observable."""

from __future__ import annotations

from pathlib import Path
import json
import math

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

    assert comparison.phase_span > 2.0 * math.pi
    assert comparison.maximum_rhs_residual < 1.0e-14
    assert comparison.minimum_abs_constraint_denominator > 0.25

    assert math.isclose(
        comparison.full_field_growth_factor,
        0.99386114336848497,
        rel_tol=1.0e-8,
        abs_tol=1.0e-10,
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
