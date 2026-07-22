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

def test_zero_wave_number_matching_is_regular():
    receipt = json.loads(RECEIPT.read_text())
    (phi_initial, v_initial, rho_star, m_phi_squared, lambda_phi, q_theta) = map(float, receipt['candidate_vector'])
    unit_inputs = receipt['unit_map_inputs']
    unit_map = build_dfm_cdm_unit_map(H0_km_s_Mpc=float(unit_inputs['H0_km_s_Mpc']), omega_b0=float(unit_inputs['omega_b0']), omega_cdm0=float(unit_inputs['omega_cdm0']), omega_r0=float(unit_inputs['omega_r0']))
    config_inputs = receipt['solver_config']
    config = ChargeReducedSolverConfig(N_initial=float(config_inputs['N_initial']), N_final=float(config_inputs['N_final']), samples=int(config_inputs['samples']), rtol=float(config_inputs['rtol']), atol=float(config_inputs['atol']))
    (rho_m_initial, rho_r_initial) = unit_map.fluid_initial_data(config.N_initial)
    parameters = ChargeReducedParameters(G=unit_map.G_code, Lambda=unit_map.Lambda_code, alpha=float(receipt['alpha']), beta=float(receipt['beta']), rho_star=rho_star, m_phi_squared=m_phi_squared, lambda_phi=lambda_phi, Q_theta=q_theta)
    background = solve_charge_reduced_background(parameters=parameters, initial_data=ChargeReducedInitialData(phi=phi_initial, v=v_initial, theta=0.0, rho_m=rho_m_initial, rho_r=rho_r_initial), config=config)
    scale_factor = float(background.a[0])
    certificate = solve_charge_perturbed_zero_velocity_matching(scale_factor=scale_factor, conformal_hubble=scale_factor * float(background.H[0]), wave_number=0.0, gravitational_constant=parameters.G, phi_background=float(background.phi[0]), phi_prime_background=scale_factor * float(background.v[0]), theta_prime_background=scale_factor * float(background.theta_dot[0]), target_density_contrast=1e-06, alpha=parameters.alpha, beta=parameters.beta, rho_star=parameters.rho_star, m_phi_squared=parameters.m_phi_squared, lambda_phi=parameters.lambda_phi)
    assert certificate.zero_radial_velocity_branch_imposed
    assert certificate.metric_constraints_solved
    assert certificate.matching_surface_closed
    assert certificate.instantaneous_rhs_closed
    assert __import__('math').isfinite(certificate.constraint_denominator)
    assert __import__('math').isfinite(certificate.selected_growth_rate)
    assert all((__import__('math').isfinite(value) for value in certificate.initial_state))
    assert max((abs(value) for value in certificate.metric_residuals)) <= 1e-09
    assert max((abs(value) for value in certificate.matching_residuals)) <= 1e-09

def test_zero_k_squared_matching_jacobian_is_regular():
    from dfm_mkc_solver.charge_perturbed_zero_velocity_matching_v1 import solve_charge_perturbed_zero_velocity_matching_k_squared
    receipt = json.loads(RECEIPT.read_text())
    (phi_initial, v_initial, rho_star, m_phi_squared, lambda_phi, q_theta) = map(float, receipt['candidate_vector'])
    unit_inputs = receipt['unit_map_inputs']
    unit_map = build_dfm_cdm_unit_map(H0_km_s_Mpc=float(unit_inputs['H0_km_s_Mpc']), omega_b0=float(unit_inputs['omega_b0']), omega_cdm0=float(unit_inputs['omega_cdm0']), omega_r0=float(unit_inputs['omega_r0']))
    config_inputs = receipt['solver_config']
    config = ChargeReducedSolverConfig(N_initial=float(config_inputs['N_initial']), N_final=float(config_inputs['N_final']), samples=int(config_inputs['samples']), rtol=float(config_inputs['rtol']), atol=float(config_inputs['atol']))
    (rho_m_initial, rho_r_initial) = unit_map.fluid_initial_data(config.N_initial)
    parameters = ChargeReducedParameters(G=unit_map.G_code, Lambda=unit_map.Lambda_code, alpha=float(receipt['alpha']), beta=float(receipt['beta']), rho_star=rho_star, m_phi_squared=m_phi_squared, lambda_phi=lambda_phi, Q_theta=q_theta)
    background = solve_charge_reduced_background(parameters=parameters, initial_data=ChargeReducedInitialData(phi=phi_initial, v=v_initial, theta=0.0, rho_m=rho_m_initial, rho_r=rho_r_initial), config=config)
    scale_factor = float(background.a[0])
    certificate = solve_charge_perturbed_zero_velocity_matching_k_squared(scale_factor=scale_factor, conformal_hubble=scale_factor * float(background.H[0]), wave_number_squared=0.0, gravitational_constant=parameters.G, phi_background=float(background.phi[0]), phi_prime_background=scale_factor * float(background.v[0]), theta_prime_background=scale_factor * float(background.theta_dot[0]), target_density_contrast=1e-06, alpha=parameters.alpha, beta=parameters.beta, rho_star=parameters.rho_star, m_phi_squared=parameters.m_phi_squared, lambda_phi=parameters.lambda_phi)
    assert certificate.zero_radial_velocity_branch_imposed
    assert certificate.metric_constraints_solved
    assert certificate.matching_surface_closed
    assert certificate.instantaneous_rhs_closed
    assert __import__('math').isfinite(certificate.constraint_denominator)
    assert __import__('math').isfinite(certificate.selected_growth_rate)
    assert all((__import__('math').isfinite(value) for value in certificate.initial_state))
    assert max((abs(value) for value in certificate.metric_residuals)) <= 1e-09
    assert max((abs(value) for value in certificate.matching_residuals)) <= 1e-09
    assert certificate.jacobian_rank == 3
    assert len(certificate.jacobian_singular_values) == 3
    assert all((__import__('math').isfinite(value) and value > 0.0 for value in certificate.jacobian_singular_values))
    assert __import__('math').isfinite(certificate.jacobian_condition_number)

def test_zero_k_squared_matching_tangent_plateau_is_stable():
    from dfm_mkc_solver.charge_perturbed_zero_velocity_matching_v1 import solve_charge_perturbed_zero_velocity_matching_k_squared
    receipt = json.loads(RECEIPT.read_text())
    (phi_initial, v_initial, rho_star, m_phi_squared, lambda_phi, q_theta) = map(float, receipt['candidate_vector'])
    unit_inputs = receipt['unit_map_inputs']
    unit_map = build_dfm_cdm_unit_map(H0_km_s_Mpc=float(unit_inputs['H0_km_s_Mpc']), omega_b0=float(unit_inputs['omega_b0']), omega_cdm0=float(unit_inputs['omega_cdm0']), omega_r0=float(unit_inputs['omega_r0']))
    config_inputs = receipt['solver_config']
    config = ChargeReducedSolverConfig(N_initial=float(config_inputs['N_initial']), N_final=float(config_inputs['N_final']), samples=int(config_inputs['samples']), rtol=float(config_inputs['rtol']), atol=float(config_inputs['atol']))
    (rho_m_initial, rho_r_initial) = unit_map.fluid_initial_data(config.N_initial)
    parameters = ChargeReducedParameters(G=unit_map.G_code, Lambda=unit_map.Lambda_code, alpha=float(receipt['alpha']), beta=float(receipt['beta']), rho_star=rho_star, m_phi_squared=m_phi_squared, lambda_phi=lambda_phi, Q_theta=q_theta)
    background = solve_charge_reduced_background(parameters=parameters, initial_data=ChargeReducedInitialData(phi=phi_initial, v=v_initial, theta=0.0, rho_m=rho_m_initial, rho_r=rho_r_initial), config=config)
    scale_factor = float(background.a[0])
    certificate = solve_charge_perturbed_zero_velocity_matching_k_squared(scale_factor=scale_factor, conformal_hubble=scale_factor * float(background.H[0]), wave_number_squared=0.0, gravitational_constant=parameters.G, phi_background=float(background.phi[0]), phi_prime_background=scale_factor * float(background.v[0]), theta_prime_background=scale_factor * float(background.theta_dot[0]), target_density_contrast=1e-06, alpha=parameters.alpha, beta=parameters.beta, rho_star=parameters.rho_star, m_phi_squared=parameters.m_phi_squared, lambda_phi=parameters.lambda_phi)
    assert certificate.zero_radial_velocity_branch_imposed
    assert certificate.metric_constraints_solved
    assert certificate.matching_surface_closed
    assert certificate.instantaneous_rhs_closed
    assert __import__('math').isfinite(certificate.constraint_denominator)
    assert __import__('math').isfinite(certificate.selected_growth_rate)
    assert all((__import__('math').isfinite(value) for value in certificate.initial_state))
    assert max((abs(value) for value in certificate.metric_residuals)) <= 1e-09
    assert max((abs(value) for value in certificate.matching_residuals)) <= 1e-09
    assert certificate.jacobian_rank == 3
    assert len(certificate.jacobian_singular_values) == 3
    assert all((__import__('math').isfinite(value) and value > 0.0 for value in certificate.jacobian_singular_values))
    assert __import__('math').isfinite(certificate.jacobian_condition_number)
    conformal_hubble_for_tangent = scale_factor * float(background.H[0])
    coarse_step = 0.0001 * conformal_hubble_for_tangent ** 2
    fine_step = coarse_step / 2.0
    assert __import__('math').isfinite(coarse_step)
    assert coarse_step > 0.0
    assert fine_step > 0.0
    coarse_certificate = solve_charge_perturbed_zero_velocity_matching_k_squared(scale_factor=scale_factor, conformal_hubble=scale_factor * float(background.H[0]), wave_number_squared=coarse_step, gravitational_constant=parameters.G, phi_background=float(background.phi[0]), phi_prime_background=scale_factor * float(background.v[0]), theta_prime_background=scale_factor * float(background.theta_dot[0]), target_density_contrast=1e-06, alpha=parameters.alpha, beta=parameters.beta, rho_star=parameters.rho_star, m_phi_squared=parameters.m_phi_squared, lambda_phi=parameters.lambda_phi)
    fine_certificate = solve_charge_perturbed_zero_velocity_matching_k_squared(scale_factor=scale_factor, conformal_hubble=scale_factor * float(background.H[0]), wave_number_squared=fine_step, gravitational_constant=parameters.G, phi_background=float(background.phi[0]), phi_prime_background=scale_factor * float(background.v[0]), theta_prime_background=scale_factor * float(background.theta_dot[0]), target_density_contrast=1e-06, alpha=parameters.alpha, beta=parameters.beta, rho_star=parameters.rho_star, m_phi_squared=parameters.m_phi_squared, lambda_phi=parameters.lambda_phi)
    zero_observable = (*certificate.initial_state, certificate.selected_growth_rate)
    coarse_observable = (*coarse_certificate.initial_state, coarse_certificate.selected_growth_rate)
    fine_observable = (*fine_certificate.initial_state, fine_certificate.selected_growth_rate)
    coarse_tangent = tuple(((positive_value - zero_value) / coarse_step for (positive_value, zero_value) in zip(coarse_observable, zero_observable)))
    fine_tangent = tuple(((positive_value - zero_value) / fine_step for (positive_value, zero_value) in zip(fine_observable, zero_observable)))
    assert all((__import__('math').isfinite(value) for value in coarse_tangent))
    assert all((__import__('math').isfinite(value) for value in fine_tangent))
    tangent_difference = max((abs(fine_value - coarse_value) for (fine_value, coarse_value) in zip(fine_tangent, coarse_tangent)))
    assert tangent_difference <= 1e-10
    assert fine_tangent[-1] > 0.0
    assert coarse_certificate.instantaneous_rhs_closed
    assert fine_certificate.instantaneous_rhs_closed

def test_zero_k_squared_implicit_tangent_matches_direct_tangent():
    from dfm_mkc_solver.charge_perturbed_zero_velocity_matching_v1 import solve_charge_perturbed_zero_velocity_matching_k_squared
    receipt = json.loads(RECEIPT.read_text())
    (phi_initial, v_initial, rho_star, m_phi_squared, lambda_phi, q_theta) = map(float, receipt['candidate_vector'])
    unit_inputs = receipt['unit_map_inputs']
    unit_map = build_dfm_cdm_unit_map(H0_km_s_Mpc=float(unit_inputs['H0_km_s_Mpc']), omega_b0=float(unit_inputs['omega_b0']), omega_cdm0=float(unit_inputs['omega_cdm0']), omega_r0=float(unit_inputs['omega_r0']))
    config_inputs = receipt['solver_config']
    config = ChargeReducedSolverConfig(N_initial=float(config_inputs['N_initial']), N_final=float(config_inputs['N_final']), samples=int(config_inputs['samples']), rtol=float(config_inputs['rtol']), atol=float(config_inputs['atol']))
    (rho_m_initial, rho_r_initial) = unit_map.fluid_initial_data(config.N_initial)
    parameters = ChargeReducedParameters(G=unit_map.G_code, Lambda=unit_map.Lambda_code, alpha=float(receipt['alpha']), beta=float(receipt['beta']), rho_star=rho_star, m_phi_squared=m_phi_squared, lambda_phi=lambda_phi, Q_theta=q_theta)
    background = solve_charge_reduced_background(parameters=parameters, initial_data=ChargeReducedInitialData(phi=phi_initial, v=v_initial, theta=0.0, rho_m=rho_m_initial, rho_r=rho_r_initial), config=config)
    scale_factor = float(background.a[0])
    certificate = solve_charge_perturbed_zero_velocity_matching_k_squared(scale_factor=scale_factor, conformal_hubble=scale_factor * float(background.H[0]), wave_number_squared=0.0, gravitational_constant=parameters.G, phi_background=float(background.phi[0]), phi_prime_background=scale_factor * float(background.v[0]), theta_prime_background=scale_factor * float(background.theta_dot[0]), target_density_contrast=1e-06, alpha=parameters.alpha, beta=parameters.beta, rho_star=parameters.rho_star, m_phi_squared=parameters.m_phi_squared, lambda_phi=parameters.lambda_phi)
    assert certificate.zero_radial_velocity_branch_imposed
    assert certificate.metric_constraints_solved
    assert certificate.matching_surface_closed
    assert certificate.instantaneous_rhs_closed
    assert __import__('math').isfinite(certificate.constraint_denominator)
    assert __import__('math').isfinite(certificate.selected_growth_rate)
    assert all((__import__('math').isfinite(value) for value in certificate.initial_state))
    assert max((abs(value) for value in certificate.metric_residuals)) <= 1e-09
    assert max((abs(value) for value in certificate.matching_residuals)) <= 1e-09
    assert certificate.jacobian_rank == 3
    assert len(certificate.jacobian_singular_values) == 3
    assert all((__import__('math').isfinite(value) and value > 0.0 for value in certificate.jacobian_singular_values))
    assert __import__('math').isfinite(certificate.jacobian_condition_number)
    from dfm_mkc_solver.charge_perturbed_zero_velocity_matching_v1 import solve_charge_perturbed_zero_velocity_matching_implicit_tangent_k_squared
    conformal_hubble_for_implicit_tangent = scale_factor * float(background.H[0])
    implicit_tangent = solve_charge_perturbed_zero_velocity_matching_implicit_tangent_k_squared(scale_factor=scale_factor, conformal_hubble=conformal_hubble_for_implicit_tangent, gravitational_constant=parameters.G, phi_background=float(background.phi[0]), phi_prime_background=scale_factor * float(background.v[0]), theta_prime_background=scale_factor * float(background.theta_dot[0]), target_density_contrast=1e-06, alpha=parameters.alpha, beta=parameters.beta, rho_star=parameters.rho_star, m_phi_squared=parameters.m_phi_squared, lambda_phi=parameters.lambda_phi, wave_number_squared_step=0.0001 * conformal_hubble_for_implicit_tangent ** 2)
    assert implicit_tangent.jacobian_rank == 3
    assert __import__('math').isfinite(implicit_tangent.jacobian_condition_number)
    assert implicit_tangent.coordinate_affine_defect <= 1e-08
    assert implicit_tangent.forcing_refinement_difference <= 1e-05
    assert max((abs(value) for value in implicit_tangent.implicit_residual)) <= 1e-09
    assert all((__import__('math').isfinite(value) for value in implicit_tangent.normalized_coordinate_tangent))
    assert abs(implicit_tangent.growth_tangent - implicit_tangent.direct_growth_tangent) <= 2e-05
    assert abs(implicit_tangent.growth_tangent - 0.3690463889) <= 2e-05
