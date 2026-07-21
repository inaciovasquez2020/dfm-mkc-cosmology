"""Regression for the merged circular zero-velocity matching branch."""

from __future__ import annotations

from pathlib import Path
import json
import math

from dfm_mkc_solver.charge_perturbed_zero_velocity_matching_v1 import (
    solve_charge_perturbed_zero_velocity_matching,
)
from dfm_mkc_solver.charge_reduced_background_v1 import (
    ChargeReducedInitialData,
    ChargeReducedParameters,
    ChargeReducedSolverConfig,
    build_dfm_cdm_unit_map,
    solve_charge_reduced_background,
)


RECEIPT = Path(
    "artifacts/dfm_mkc/"
    "dfm_cdm_minimal_circular_solution_receipt_2026_07_21.json"
)


def test_merged_candidate_zero_velocity_matching_closes() -> None:
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
        N_final=float(config_inputs["N_final"]),
        samples=int(config_inputs["samples"]),
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

    background = solve_charge_reduced_background(
        parameters=parameters,
        initial_data=ChargeReducedInitialData(
            phi=phi_initial,
            v=v_initial,
            theta=0.0,
            rho_m=rho_m_initial,
            rho_r=rho_r_initial,
        ),
        config=config,
    )

    scale_factor = float(background.a[0])

    certificate = (
        solve_charge_perturbed_zero_velocity_matching(
            scale_factor=scale_factor,
            conformal_hubble=(
                scale_factor * float(background.H[0])
            ),
            wave_number=0.005,
            gravitational_constant=parameters.G,
            phi_background=float(background.phi[0]),
            phi_prime_background=(
                scale_factor * float(background.v[0])
            ),
            theta_prime_background=(
                scale_factor * float(background.theta_dot[0])
            ),
            target_density_contrast=1.0e-6,
            alpha=parameters.alpha,
            beta=parameters.beta,
            rho_star=parameters.rho_star,
            m_phi_squared=parameters.m_phi_squared,
            lambda_phi=parameters.lambda_phi,
        )
    )

    assert certificate.jacobian_rank == 3
    assert certificate.maximum_metric_residual < 1.0e-12
    assert certificate.maximum_matching_residual < 1.0e-12
    assert certificate.constraint_denominator != 0.0
    assert certificate.instantaneous_rhs_closed
    assert certificate.metric_constraints_solved
    assert certificate.matching_surface_closed

    assert math.isclose(
        certificate.selected_growth_rate,
        -0.4759665082080208,
        rel_tol=1.0e-8,
        abs_tol=1.0e-10,
    )
    assert math.isclose(
        certificate.phi_metric_n,
        -1.5865857812258096e-7,
        rel_tol=1.0e-8,
        abs_tol=1.0e-12,
    )
    assert abs(certificate.psi_metric) < 1.0e-12
    assert certificate.delta_phi_prime < 0.0
