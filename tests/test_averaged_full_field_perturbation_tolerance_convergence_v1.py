"""Perturbation-tolerance convergence for the full-field comparison."""

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


PERTURBATION_TOLERANCES = (
    (1.0e-6, 1.0e-8),
    (1.0e-8, 1.0e-10),
    (1.0e-9, 1.0e-11),
)

WAVE_NUMBER = 0.005


def _run(
    perturbation_rtol: float,
    perturbation_atol: float,
):
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
        wave_number=WAVE_NUMBER,
        target_density_contrast=1.0e-6,
        target_density_contrast_n=1.0e-6,
        cycle_count=1,
        perturbation_rtol=perturbation_rtol,
        perturbation_atol=perturbation_atol,
    )


def _relative_difference(left: float, right: float) -> float:
    scale = max(abs(left), abs(right), 1.0e-14)
    return abs(right - left) / scale


def test_perturbation_tolerance_cauchy_convergence() -> None:
    certificates = [
        _run(perturbation_rtol, perturbation_atol)
        for perturbation_rtol, perturbation_atol
        in PERTURBATION_TOLERANCES
    ]

    for certificate in certificates:
        assert certificate.initial_metric_fixed_point_solved
        assert certificate.time_dependent_full_field_evolved
        assert certificate.metric_constraints_solved_at_each_sample
        assert certificate.phase_cycle_averaging_computed
        assert certificate.averaged_full_field_comparison_computed
        assert certificate.maximum_rhs_residual < 1.0e-7

    metrics = (
        "initial_cycle_average",
        "final_cycle_average",
        "full_field_growth_factor",
        "full_to_averaged_growth_ratio",
        "relative_growth_difference",
    )

    for metric in metrics:
        coarse, medium, fine = (
            float(getattr(certificate, metric))
            for certificate in certificates
        )

        coarse_to_medium = _relative_difference(coarse, medium)
        medium_to_fine = _relative_difference(medium, fine)

        assert medium_to_fine <= 1.0e-2, (
            metric,
            medium,
            fine,
            medium_to_fine,
        )

        assert medium_to_fine <= (
            2.0 * coarse_to_medium + 1.0e-7
        ), (
            metric,
            coarse,
            medium,
            fine,
            coarse_to_medium,
            medium_to_fine,
        )
