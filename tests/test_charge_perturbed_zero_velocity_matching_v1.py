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
import numpy as np


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


def test_regularized_k_squared_tangent_evolution_matches_two_forward_trajectory_derivatives():
    from dfm_mkc_solver.averaged_full_field_time_dependent_comparison_v1 import (
        integrate_regularized_k_squared_tangent_evolution,
    )
    from dfm_mkc_solver.charge_perturbed_zero_velocity_matching_v1 import (
        solve_charge_perturbed_zero_velocity_matching_k_squared,
    )
    from dfm_mkc_solver.charge_reduced_background_v1 import (
        ChargeReducedInitialData,
        ChargeReducedParameters,
        ChargeReducedSolverConfig,
        build_dfm_cdm_unit_map,
        solve_charge_reduced_background,
    )

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
    rho_m_initial, rho_r_initial = unit_map.fluid_initial_data(
        config.N_initial
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
    initial_data = ChargeReducedInitialData(
        phi=phi_initial,
        v=v_initial,
        theta=0.0,
        rho_m=rho_m_initial,
        rho_r=rho_r_initial,
    )
    background = solve_charge_reduced_background(
        parameters=parameters,
        initial_data=initial_data,
        config=config,
    )
    assert background.success

    scale_factor = float(background.a[0])
    common = dict(
        scale_factor=scale_factor,
        conformal_hubble=scale_factor * float(background.H[0]),
        gravitational_constant=parameters.G,
        phi_background=float(background.phi[0]),
        phi_prime_background=scale_factor * float(background.v[0]),
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
    x_step = 1.0e-5
    base = solve_charge_perturbed_zero_velocity_matching_k_squared(
        wave_number_squared=0.0,
        **common,
    )
    first = solve_charge_perturbed_zero_velocity_matching_k_squared(
        wave_number_squared=x_step,
        **common,
    )
    second = solve_charge_perturbed_zero_velocity_matching_k_squared(
        wave_number_squared=2.0 * x_step,
        **common,
    )
    base_state = np.asarray(base.initial_state, dtype=float)
    initial_state_tangent = (
        -3.0 * base_state
        + 4.0 * np.asarray(first.initial_state, dtype=float)
        - np.asarray(second.initial_state, dtype=float)
    ) / (2.0 * x_step)

    certificate = integrate_regularized_k_squared_tangent_evolution(
        parameters=parameters,
        initial_data=initial_data,
        config=config,
        initial_state=tuple(float(value) for value in base_state),
        initial_state_tangent=tuple(
            float(value) for value in initial_state_tangent
        ),
        sigma8_0=1.0,
        wave_number_squared=0.0,
        wave_number_squared_difference_step=x_step,
        validation_tolerance=1.0e-1,
    )

    assert certificate.native_k_squared_rhs_used is True
    assert certificate.variational_equation_integrated is True
    assert certificate.two_noninitial_trajectory_checks_passed is True
    assert certificate.validation_indices[0] > 0
    assert certificate.validation_indices[1] > certificate.validation_indices[0]
    assert certificate.maximum_validation_relative_error < 1.0e-1
    assert np.all(np.isfinite(certificate.fsigma8_values))
    assert np.all(np.isfinite(certificate.fsigma8_tangents))
    assert np.max(np.abs(certificate.fsigma8_tangents)) > 0.0

def test_regularized_fsigma8_projection_computes_orthogonal_residual():
    import pytest

    from dfm_mkc_solver.averaged_full_field_time_dependent_comparison_v1 import (
        integrate_regularized_k_squared_tangent_evolution,
    )
    from dfm_mkc_solver.charge_perturbed_zero_velocity_matching_v1 import (
        solve_charge_perturbed_zero_velocity_matching_k_squared,
    )
    from dfm_mkc_solver.charge_reduced_background_v1 import (
        ChargeReducedInitialData,
        ChargeReducedParameters,
        ChargeReducedSolverConfig,
        build_dfm_cdm_unit_map,
        solve_charge_reduced_background,
    )

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
    config_inputs = receipt["solver_config"]
    base_h0 = float(unit_inputs["H0_km_s_Mpc"])
    base_omega_b0 = float(unit_inputs["omega_b0"])
    base_omega_cdm0 = float(unit_inputs["omega_cdm0"])
    base_omega_r0 = float(unit_inputs["omega_r0"])
    base_w0 = -1.0
    base_wa = 0.0
    h0_step = 5.0e-5
    coarse_parameter_step = 1.0e-4
    fine_parameter_step = 5.0e-5
    coarse_x_step = 1.0e-5
    fine_x_step = 5.0e-6
    residual_tolerance = 1.0e-10

    config = ChargeReducedSolverConfig(
        N_initial=float(config_inputs["N_initial"]),
        N_final=float(config_inputs["N_final"]),
        samples=int(config_inputs["samples"]),
        rtol=float(config_inputs["rtol"]),
        atol=float(config_inputs["atol"]),
    )

    def build_evolution(
        *,
        h0_km_s_mpc=base_h0,
        omega_b0=base_omega_b0,
        omega_cdm0=base_omega_cdm0,
        w0=base_w0,
        wa=base_wa,
        x_step=fine_x_step,
    ):
        unit_map = build_dfm_cdm_unit_map(
            H0_km_s_Mpc=h0_km_s_mpc,
            omega_b0=omega_b0,
            omega_cdm0=omega_cdm0,
            omega_r0=base_omega_r0,
        )
        assert unit_map.omega_b0 == pytest.approx(omega_b0)
        assert unit_map.omega_cdm0 == pytest.approx(omega_cdm0)
        assert unit_map.omega_r0 == pytest.approx(base_omega_r0)
        assert (
            unit_map.omega_b0
            + unit_map.omega_cdm0
            + unit_map.omega_r0
            + unit_map.omega_lambda0
        ) == pytest.approx(1.0)

        rho_m_initial, rho_r_initial = unit_map.fluid_initial_data(
            config.N_initial
        )
        parameters = ChargeReducedParameters(
            G=unit_map.G_code,
            Lambda=unit_map.Lambda_code,
            w0=w0,
            wa=wa,
            alpha=float(receipt["alpha"]),
            beta=float(receipt["beta"]),
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
        background = solve_charge_reduced_background(
            parameters=parameters,
            initial_data=initial_data,
            config=config,
        )
        assert background.success

        scale_factor = float(background.a[0])
        matching_inputs = dict(
            scale_factor=scale_factor,
            conformal_hubble=scale_factor * float(background.H[0]),
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
        base_matching = (
            solve_charge_perturbed_zero_velocity_matching_k_squared(
                wave_number_squared=0.0,
                **matching_inputs,
            )
        )
        first_matching = (
            solve_charge_perturbed_zero_velocity_matching_k_squared(
                wave_number_squared=x_step,
                **matching_inputs,
            )
        )
        second_matching = (
            solve_charge_perturbed_zero_velocity_matching_k_squared(
                wave_number_squared=2.0 * x_step,
                **matching_inputs,
            )
        )
        base_state = np.asarray(
            base_matching.initial_state,
            dtype=float,
        )
        initial_state_tangent = (
            -3.0 * base_state
            + 4.0
            * np.asarray(first_matching.initial_state, dtype=float)
            - np.asarray(second_matching.initial_state, dtype=float)
        ) / (2.0 * x_step)

        return integrate_regularized_k_squared_tangent_evolution(
            parameters=parameters,
            initial_data=initial_data,
            config=config,
            initial_state=tuple(
                float(value) for value in base_state
            ),
            initial_state_tangent=tuple(
                float(value) for value in initial_state_tangent
            ),
            sigma8_0=1.0,
            wave_number_squared=0.0,
            wave_number_squared_difference_step=x_step,
            validation_tolerance=1.0e-1,
        )

    base_fine = build_evolution(x_step=fine_x_step)
    base_coarse = build_evolution(x_step=coarse_x_step)

    plus_h0 = build_evolution(
        h0_km_s_mpc=base_h0 * float(np.exp(h0_step))
    )
    minus_h0 = build_evolution(
        h0_km_s_mpc=base_h0 * float(np.exp(-h0_step))
    )

    def centered_pair(parameter_name, step):
        if parameter_name == "ln_omega_b0":
            return (
                build_evolution(
                    omega_b0=base_omega_b0 * float(np.exp(step))
                ),
                build_evolution(
                    omega_b0=base_omega_b0 * float(np.exp(-step))
                ),
            )
        if parameter_name == "ln_omega_cdm0":
            return (
                build_evolution(
                    omega_cdm0=(
                        base_omega_cdm0 * float(np.exp(step))
                    )
                ),
                build_evolution(
                    omega_cdm0=(
                        base_omega_cdm0 * float(np.exp(-step))
                    )
                ),
            )
        if parameter_name == "w0":
            return (
                build_evolution(w0=base_w0 + step),
                build_evolution(w0=base_w0 - step),
            )
        if parameter_name == "wa":
            return (
                build_evolution(wa=base_wa + step),
                build_evolution(wa=base_wa - step),
            )
        raise AssertionError(parameter_name)

    parameter_names = (
        "ln_omega_b0",
        "ln_omega_cdm0",
        "w0",
        "wa",
    )
    coarse_pairs = {
        name: centered_pair(name, coarse_parameter_step)
        for name in parameter_names
    }
    fine_pairs = {
        name: centered_pair(name, fine_parameter_step)
        for name in parameter_names
    }

    grid = np.asarray(base_fine.log_scale_factors, dtype=float)

    def sample_points(count):
        indices = np.unique(
            np.linspace(1, grid.size - 2, num=count, dtype=int)
        )
        assert indices.size == count
        assert np.all(np.diff(indices) > 0)
        return tuple(float(grid[index]) for index in indices)

    def sampled_values(evolution, points):
        return np.interp(
            points,
            evolution.log_scale_factors,
            evolution.fsigma8_values,
        )

    def sampled_k2_tangent(evolution, points):
        return np.interp(
            points,
            evolution.log_scale_factors,
            evolution.fsigma8_tangents,
        )

    def trapezoid_weights(points):
        points_array = np.asarray(points, dtype=float)
        widths = np.diff(points_array)
        weights = np.empty_like(points_array)
        weights[0] = 0.5 * widths[0]
        weights[-1] = 0.5 * widths[-1]
        weights[1:-1] = 0.5 * (widths[:-1] + widths[1:])
        weights /= float(np.sum(weights))
        return weights

    def tangent_from_pair(pair, step, points):
        plus, minus = pair
        return (
            sampled_values(plus, points)
            - sampled_values(minus, points)
        ) / (2.0 * step)

    def weighted_projection(
        *,
        points,
        base_evolution,
        pairs,
        parameter_step,
    ):
        observable = sampled_values(base_evolution, points)
        k2_tangent = sampled_k2_tangent(base_evolution, points)
        h0_tangent = (
            sampled_values(plus_h0, points)
            - sampled_values(minus_h0, points)
        ) / (2.0 * h0_step)
        parameter_tangents = {
            name: tangent_from_pair(
                pairs[name],
                parameter_step,
                points,
            )
            for name in parameter_names
        }
        matrix = np.column_stack(
            [
                observable,
                h0_tangent,
                parameter_tangents["ln_omega_b0"],
                parameter_tangents["ln_omega_cdm0"],
                parameter_tangents["w0"],
                parameter_tangents["wa"],
            ]
        )
        weights = trapezoid_weights(points)
        root_weights = np.sqrt(weights)
        weighted_matrix = root_weights[:, None] * matrix
        weighted_tangent = root_weights * k2_tangent
        u, singular_values, _vh = np.linalg.svd(
            weighted_matrix,
            full_matrices=False,
        )
        largest = float(singular_values[0])
        rank_tolerance = (
            max(weighted_matrix.shape)
            * np.finfo(float).eps
            * largest
        )
        rank = int(np.sum(singular_values > rank_tolerance))
        if rank:
            active_u = u[:, :rank]
            projected = active_u @ (active_u.T @ weighted_tangent)
        else:
            projected = np.zeros_like(weighted_tangent)
        residual = weighted_tangent - projected
        tangent_norm = float(np.linalg.norm(weighted_tangent, ord=2))
        residual_norm = float(np.linalg.norm(residual, ord=2))
        relative_residual = (
            residual_norm / tangent_norm
            if tangent_norm > 0.0
            else 0.0
        )
        tangent_norms = {
            "ln_H0": float(np.linalg.norm(h0_tangent, ord=2)),
            **{
                name: float(np.linalg.norm(values, ord=2))
                for name, values in parameter_tangents.items()
            },
        }
        return {
            "rank": rank,
            "relative_residual": relative_residual,
            "residual_norm": residual_norm,
            "k2_tangent_norm": tangent_norm,
            "tangent_norms": tangent_norms,
            "parameter_tangents": parameter_tangents,
        }

    grid_counts = (7, 11, 15)
    fine_grid_results = {
        count: weighted_projection(
            points=sample_points(count),
            base_evolution=base_fine,
            pairs=fine_pairs,
            parameter_step=fine_parameter_step,
        )
        for count in grid_counts
    }
    finest_points = sample_points(grid_counts[-1])
    coarse_parameter_result = weighted_projection(
        points=finest_points,
        base_evolution=base_fine,
        pairs=coarse_pairs,
        parameter_step=coarse_parameter_step,
    )
    fine_parameter_result = fine_grid_results[grid_counts[-1]]
    coarse_x_result = weighted_projection(
        points=finest_points,
        base_evolution=base_coarse,
        pairs=fine_pairs,
        parameter_step=fine_parameter_step,
    )

    fine_residuals = tuple(
        fine_grid_results[count]["relative_residual"]
        for count in grid_counts
    )
    grid_error = max(
        abs(fine_residuals[2] - fine_residuals[1]),
        abs(fine_residuals[1] - fine_residuals[0]),
    )
    parameter_step_error = abs(
        fine_parameter_result["relative_residual"]
        - coarse_parameter_result["relative_residual"]
    )
    x_step_error = abs(
        fine_parameter_result["relative_residual"]
        - coarse_x_result["relative_residual"]
    )
    empirical_error = (
        grid_error + parameter_step_error + x_step_error
    )
    empirical_lower_bound = max(
        0.0,
        fine_parameter_result["relative_residual"]
        - 2.0 * empirical_error,
    )

    tangent_step_changes = []
    for name in parameter_names:
        fine_tangent = fine_parameter_result[
            "parameter_tangents"
        ][name]
        coarse_tangent = coarse_parameter_result[
            "parameter_tangents"
        ][name]
        denominator = max(
            float(np.linalg.norm(fine_tangent, ord=2)),
            np.finfo(float).tiny,
        )
        tangent_step_changes.append(
            float(
                np.linalg.norm(
                    fine_tangent - coarse_tangent,
                    ord=2,
                )
            )
            / denominator
        )
    maximum_tangent_step_change = max(tangent_step_changes)

    finest_rank = int(fine_parameter_result["rank"])
    finest_residual = float(
        fine_parameter_result["relative_residual"]
    )
    discovery_rejected = finest_residual <= residual_tolerance
    basis_complete = finest_rank == 5
    refinement_resolved = (
        maximum_tangent_step_change <= 1.0e-2
        and x_step_error <= 1.0e-3
    )
    if discovery_rejected:
        status = "rejected_residual_below_tolerance"
    elif not basis_complete:
        status = "conditional_rank_deficient"
    elif empirical_lower_bound <= 0.0:
        status = "conditional_refinement_unresolved"
    elif not refinement_resolved:
        status = "conditional_derivative_refinement_unresolved"
    else:
        status = "conditional_positive_empirical_lower_bound"

    assert base_fine.two_noninitial_trajectory_checks_passed is True
    assert base_coarse.two_noninitial_trajectory_checks_passed is True
    assert fine_parameter_result["tangent_norms"]["ln_H0"] <= 1.0e-10
    for name in parameter_names:
        assert fine_parameter_result["tangent_norms"][name] > 0.0
    assert 1 <= finest_rank <= 5
    assert np.all(np.isfinite(fine_residuals))
    assert np.isfinite(parameter_step_error)
    assert np.isfinite(x_step_error)
    assert np.isfinite(maximum_tangent_step_change)
    assert np.isfinite(empirical_lower_bound)
    assert empirical_lower_bound > 0.0
    assert finest_rank == 5
    assert refinement_resolved is True
    assert status == "conditional_positive_empirical_lower_bound"

    for count, residual in zip(grid_counts, fine_residuals):
        print(
            f"DISCOVERY_FSIGMA8_RELATIVE_RESIDUAL_GRID_{count} := "
            f"{residual:.12e}"
        )
    print(
        "DISCOVERY_FSIGMA8_STANDARD_TANGENT_RANK := "
        f"{finest_rank}"
    )
    print(
        "DISCOVERY_FSIGMA8_LN_OMEGA_B0_TANGENT_NORM := "
        f"{fine_parameter_result['tangent_norms']['ln_omega_b0']:.12e}"
    )
    print(
        "DISCOVERY_FSIGMA8_LN_OMEGA_CDM0_TANGENT_NORM := "
        f"{fine_parameter_result['tangent_norms']['ln_omega_cdm0']:.12e}"
    )
    print(
        "DISCOVERY_FSIGMA8_W0_TANGENT_NORM := "
        f"{fine_parameter_result['tangent_norms']['w0']:.12e}"
    )
    print(
        "DISCOVERY_FSIGMA8_WA_TANGENT_NORM := "
        f"{fine_parameter_result['tangent_norms']['wa']:.12e}"
    )
    print(
        "DISCOVERY_FSIGMA8_PARAMETER_STEP_ERROR := "
        f"{parameter_step_error:.12e}"
    )
    print(
        "DISCOVERY_FSIGMA8_K2_STEP_ERROR := "
        f"{x_step_error:.12e}"
    )
    print(
        "DISCOVERY_FSIGMA8_MAX_TANGENT_STEP_CHANGE := "
        f"{maximum_tangent_step_change:.12e}"
    )
    print(
        "DISCOVERY_FSIGMA8_EMPIRICAL_RELATIVE_LOWER_BOUND := "
        f"{empirical_lower_bound:.12e}"
    )
    print(
        "DISCOVERY_FSIGMA8_REJECTED := "
        f"{str(discovery_rejected).lower()}"
    )
    print(
        "DISCOVERY_FSIGMA8_STATUS := "
        f"{status}"
    )
