"""Background-sampling convergence for the full-field comparison."""

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


SAMPLE_COUNTS = (601, 1201, 2401)
WAVE_NUMBER = 0.005


def _run(samples: int):
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
            samples=samples,
            rtol=1.0e-9,
            atol=1.0e-11,
        ),
        wave_number=WAVE_NUMBER,
        target_density_contrast=1.0e-6,
        target_density_contrast_n=1.0e-6,
        cycle_count=1,
        perturbation_rtol=1.0e-8,
        perturbation_atol=1.0e-10,
    )


def _relative_change(left: float, right: float) -> float:
    scale = max(abs(left), abs(right), 1.0e-14)
    return abs(right - left) / scale


def test_background_sampling_convergence() -> None:
    certificates = [_run(samples) for samples in SAMPLE_COUNTS]

    for certificate in certificates:
        assert certificate.initial_metric_fixed_point_solved
        assert certificate.time_dependent_full_field_evolved
        assert certificate.phase_cycle_averaging_computed
        assert certificate.averaged_full_field_comparison_computed
        assert certificate.maximum_rhs_residual < 1.0e-7

    metrics = (
        "initial_cycle_average",
        "final_cycle_average",
        "full_field_growth_factor",
        "averaged_growth_factor",
        "full_to_averaged_growth_ratio",
        "relative_growth_difference",
    )

    for metric in metrics:
        coarse, medium, fine = (
            float(getattr(certificate, metric))
            for certificate in certificates
        )

        coarse_to_medium = abs(medium - coarse)
        medium_to_fine = abs(fine - medium)
        fine_relative_change = _relative_change(medium, fine)

        assert medium_to_fine <= coarse_to_medium, (
            metric,
            coarse,
            medium,
            fine,
            coarse_to_medium,
            medium_to_fine,
        )

        assert fine_relative_change <= 1.0e-2, (
            metric,
            medium,
            fine,
            fine_relative_change,
        )
