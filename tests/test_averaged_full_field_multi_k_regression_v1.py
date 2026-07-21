"""Deterministic multi-k averaged-versus-full-field regression."""

from __future__ import annotations

import math

from dfm_mkc_solver.averaged_full_field_time_dependent_comparison_v1 import (
    compare_averaged_and_time_dependent_full_field_growth,
)
from dfm_mkc_solver.charge_reduced_background_v1 import (
    ChargeReducedInitialData,
    ChargeReducedParameters,
    ChargeReducedSolverConfig,
)


EXPECTED = {
    0.005: {
        "full_field_growth_factor": 15.0171262499332,
        "averaged_growth_factor": 3.279556409787583,
        "full_to_averaged_growth_ratio": 4.579011419079649,
        "relative_growth_difference": 3.579011419079649,
    },
    0.01: {
        "full_field_growth_factor": 7.519441381217063,
        "averaged_growth_factor": -0.09609440250175318,
        "full_to_averaged_growth_ratio": -78.25056595861425,
        "relative_growth_difference": -79.25056595861425,
    },
    0.02: {
        "full_field_growth_factor": -1.026415841412059,
        "averaged_growth_factor": -0.9270459895254429,
        "full_to_averaged_growth_ratio": 1.107189775921994,
        "relative_growth_difference": 0.1071897759219944,
    },
}


def _run(wave_number: float):
    return compare_averaged_and_time_dependent_full_field_growth(
        parameters=ChargeReducedParameters(
            G=1.0e-4,
            Lambda=0.0,
            alpha=1.0,
            beta=1.0,
            rho_star=0.0,
            m_phi_squared=1.0e-2,
            lambda_phi=0.0,
            Q_theta=1.5625e-3,
        ),
        initial_data=ChargeReducedInitialData(
            phi=1.0,
            v=1.0e-4,
            theta=0.0,
            rho_m=0.0,
            rho_r=0.0,
        ),
        config=ChargeReducedSolverConfig(
            N_initial=math.log(0.25),
            N_final=0.0,
            samples=1201,
            rtol=1.0e-9,
            atol=1.0e-11,
        ),
        wave_number=wave_number,
        target_density_contrast=1.0e-6,
        target_density_contrast_n=1.0e-6,
        cycle_count=1,
        perturbation_rtol=1.0e-8,
        perturbation_atol=1.0e-10,
    )


def test_deterministic_multi_k_comparison_values() -> None:
    for wave_number, expected in EXPECTED.items():
        certificate = _run(wave_number)

        assert certificate.initial_matching_surface_closed
        assert certificate.initial_metric_fixed_point_solved
        assert certificate.time_dependent_background_evolved
        assert certificate.time_dependent_full_field_evolved
        assert certificate.metric_constraints_solved_at_each_sample
        assert certificate.phase_cycle_averaging_computed
        assert certificate.averaged_full_field_comparison_computed

        actual = {
            "full_field_growth_factor": (
                certificate.full_field_growth_factor
            ),
            "averaged_growth_factor": (
                certificate.averaged_growth_factor
            ),
            "full_to_averaged_growth_ratio": (
                certificate.full_to_averaged_growth_ratio
            ),
            "relative_growth_difference": (
                certificate.relative_growth_difference
            ),
        }

        for key, expected_value in expected.items():
            assert math.isclose(
                actual[key],
                expected_value,
                rel_tol=2.0e-5,
                abs_tol=1.0e-11,
            ), (
                wave_number,
                key,
                actual[key],
                expected_value,
            )

        assert certificate.maximum_rhs_residual < 1.0e-7
        assert certificate.minimum_abs_constraint_denominator > 0.0
