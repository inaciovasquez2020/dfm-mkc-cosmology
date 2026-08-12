import importlib.util
import sys
from pathlib import Path

import numpy as np
import pytest
import sympy as sp


CODE = Path(
    "src/dfm_mkc_solver/charge_reduced_background_v1.py"
)

spec = importlib.util.spec_from_file_location(
    "charge_reduced_background_v1",
    CODE,
)
module = importlib.util.module_from_spec(spec)
assert spec.loader is not None
sys.modules[spec.name] = module
spec.loader.exec_module(module)


def test_flat_potential_zero_charge_solution():
    parameters = module.ChargeReducedParameters(
        rho_star=1.0,
        m_phi_squared=0.0,
        lambda_phi=0.0,
        Q_theta=0.0,
    )
    initial = module.ChargeReducedInitialData(
        phi=1.25,
        v=0.0,
        rho_m=0.9,
        rho_r=3.0e-4,
    )
    config = module.ChargeReducedSolverConfig(
        N_initial=-1.0,
        N_final=0.0,
        samples=201,
        rtol=1.0e-10,
        atol=1.0e-12,
    )

    solution = module.solve_charge_reduced_background(
        parameters,
        initial,
        config,
    )

    delta_N = solution.N - config.N_initial
    expected_rho_m = initial.rho_m * np.exp(-3.0 * delta_N)
    expected_rho_r = initial.rho_r * np.exp(-4.0 * delta_N)

    assert solution.success is True
    np.testing.assert_allclose(
        solution.phi,
        initial.phi,
        rtol=0.0,
        atol=1.0e-12,
    )
    np.testing.assert_allclose(
        solution.v,
        0.0,
        rtol=0.0,
        atol=1.0e-12,
    )
    np.testing.assert_allclose(
        solution.theta,
        initial.theta,
        rtol=0.0,
        atol=1.0e-12,
    )
    np.testing.assert_allclose(
        solution.rho_m,
        expected_rho_m,
        rtol=2.0e-9,
        atol=1.0e-12,
    )
    np.testing.assert_allclose(
        solution.rho_r,
        expected_rho_r,
        rtol=2.0e-9,
        atol=1.0e-12,
    )
    assert np.all(solution.H > 0.0)
    assert np.max(
        np.abs(solution.friedmann_constraint_residual)
    ) < 1.0e-12


def test_nonzero_charge_makes_beta_dynamical():
    state = (1.0, 0.0, 0.0, 0.3, 1.0e-4)

    beta_one = module.ChargeReducedParameters(
        beta=1.0,
        Q_theta=0.4,
    )
    beta_two = module.ChargeReducedParameters(
        beta=2.0,
        Q_theta=0.4,
    )

    H_beta_one = module.friedmann_hubble(
        0.0,
        state,
        beta_one,
    )
    H_beta_two = module.friedmann_hubble(
        0.0,
        state,
        beta_two,
    )

    assert H_beta_one > H_beta_two


def test_quartic_potential_and_derivative():
    parameters = module.ChargeReducedParameters(
        rho_star=0.7,
        m_phi_squared=-0.2,
        lambda_phi=0.3,
    )
    phi = 1.4

    expected_potential = (
        0.7
        + 0.5 * (-0.2) * phi**2
        + 0.25 * 0.3 * phi**4
    )
    expected_derivative = -0.2 * phi + 0.3 * phi**3

    assert module.potential(phi, parameters) == pytest.approx(
        expected_potential
    )
    assert module.potential_derivative(
        phi,
        parameters,
    ) == pytest.approx(expected_derivative)


def test_charge_reduction_rejects_zero_phi():
    parameters = module.ChargeReducedParameters(
        Q_theta=0.1,
    )
    initial = module.ChargeReducedInitialData(
        phi=0.0,
    )

    with pytest.raises(
        ValueError,
        match="phi must remain nonzero",
    ):
        module.solve_charge_reduced_background(
            parameters,
            initial,
        )



def test_phase_reconstruction_preserves_conserved_charge():
    parameters = module.ChargeReducedParameters(
        beta=1.3,
        rho_star=1.0,
        m_phi_squared=0.0,
        lambda_phi=0.0,
        Q_theta=0.05,
    )
    initial = module.ChargeReducedInitialData(
        phi=1.5,
        v=0.0,
        theta=0.7,
        rho_m=0.3,
        rho_r=1.0e-4,
    )
    config = module.ChargeReducedSolverConfig(
        N_initial=-0.2,
        N_final=0.0,
        samples=201,
        rtol=1.0e-10,
        atol=1.0e-12,
    )

    solution = module.solve_charge_reduced_background(
        parameters,
        initial,
        config,
    )

    assert solution.theta[0] == pytest.approx(initial.theta)
    assert np.all(np.diff(solution.theta) > 0.0)
    assert np.max(
        np.abs(solution.phase_charge_residual)
    ) < 1.0e-12
    assert np.all(np.isfinite(solution.theta))


def test_exact_charge_reduced_constraint_certificate():
    certificate = module.exact_charge_reduced_constraint_certificate()

    assert set(certificate) == {
        "dfm_continuity",
        "friedmann_constraint",
    }
    assert certificate["dfm_continuity"] == 0
    assert certificate["friedmann_constraint"] == 0


def test_antlia_eq12_tf_hierarchy_ratio_is_dimensionless():
    assert module.antlia_eq12_tf_hierarchy_ratio(
        particle_mass_eV=1.0e-21,
        minimum_halo_mass_solar=1.0e9,
        r_tf_kpc=1.0,
    ) == pytest.approx(
        1.0,
        rel=2.0e-15,
    )

    ratio = module.antlia_eq12_tf_hierarchy_ratio(
        particle_mass_eV=4.8e-21,
        minimum_halo_mass_solar=1.66e9,
        r_tf_kpc=0.18,
    )

    assert ratio == pytest.approx(
        1.023017599477064,
        rel=2.0e-14,
    )

    with pytest.raises(
        ValueError,
        match="particle_mass_eV must be positive",
    ):
        module.antlia_eq12_tf_hierarchy_ratio(
            particle_mass_eV=0.0,
            minimum_halo_mass_solar=1.0e9,
            r_tf_kpc=1.0,
        )


def test_positive_lambda_charge_normalization_obstruction_certificate():
    certificate = (
        module
        .exact_positive_lambda_charge_normalization_obstruction_certificate()
    )

    assert set(certificate) == {
        "density_gap_factorization",
        "phase_mass_am_gm_identity",
        "quartic_positive_floor_identity",
    }

    assert all(
        expression == 0
        for expression in certificate.values()
    )


def test_zero_alpha_dust_boundary_certificate():
    certificate = module.exact_zero_alpha_dust_boundary_certificate()

    assert set(certificate) == {
        "phase_energy",
        "mass_potential",
        "rho_dfm",
        "p_dfm",
        "algebraic_radial_force",
        "continuity",
        "dust_density_equivalence",
    }
    assert all(expression == 0 for expression in certificate.values())


def test_exact_finite_alpha_circular_dust_obstruction_certificate():
    certificate = (
        module.exact_finite_alpha_circular_dust_obstruction_certificate()
    )

    assert set(certificate) == {
        "inertial_identity",
        "radial_equation_identity",
        "force_balance",
        "pressure_identity",
        "density_excess_identity",
    }
    assert all(expression == 0 for expression in certificate.values())


def test_exact_finite_alpha_circular_tracking_coercivity_certificate():
    certificate = (
        module.exact_finite_alpha_circular_tracking_coercivity_certificate()
    )

    assert set(certificate) == {
        "force_factorization",
        "tracking_equation_decomposition",
        "linear_restoring_coefficient",
        "coercive_work_identity",
        "restoring_coefficient_monotonicity",
    }
    assert all(expression == 0 for expression in certificate.values())


def test_exact_finite_alpha_relative_tracking_energy_certificate():
    certificate = (
        module.exact_finite_alpha_relative_tracking_energy_certificate()
    )

    assert set(certificate) == {
        "relative_equation_decomposition",
        "energy_identity",
        "potential_coercivity_identity",
        "field_size_control_identity",
        "young_square_identity",
        "energy_majorant_remainder",
        "forcing_bound_remainder",
        "gronwall_ode_identity",
        "gronwall_initial_identity",
    }
    assert all(expression == 0 for expression in certificate.values())



def test_exact_coupled_friedmann_forcing_bound_certificate():
    certificate = (
        module.exact_coupled_friedmann_forcing_bound_certificate()
    )

    assert set(certificate) == {
        "acceleration_pressure_identity",
        "forcing_pressure_identity",
        "rho_plus_pressure_decomposition",
        "rho_minus_pressure_decomposition",
        "dominant_energy_product_identity",
        "hubble_monotonicity_identity",
        "local_forcing_square_identity",
        "interval_forcing_majorant_identity",
    }
    assert all(expression == 0 for expression in certificate.values())


def test_exact_relative_energy_density_hubble_propagation_certificate():
    certificate = (
        module.exact_relative_energy_density_hubble_propagation_certificate()
    )

    assert set(certificate) == {
        "density_excess_decomposition",
        "density_energy_majorant_remainder",
        "energy_bound_substitution",
        "relative_density_majorant",
        "friedmann_squared_difference",
        "hubble_square_root_identity",
        "hubble_majorant_remainder",
    }
    assert all(expression == 0 for expression in certificate.values())


def test_exact_dfm_cdm_shooting_degeneracy_certificate():
    certificate = (
        module.exact_dfm_cdm_shooting_degeneracy_certificate()
    )
    assert set(certificate) == {
        "present_constraint_factorization",
        "linearized_constraint_factorization",
        "jacobian_row_dependency",
    }
    assert all(expression == 0 for expression in certificate.values())


def test_independent_total_continuity_residual():
    parameters = module.ChargeReducedParameters(
        rho_star=1.0,
        m_phi_squared=0.0,
        lambda_phi=0.0,
        Q_theta=0.0,
    )
    initial = module.ChargeReducedInitialData(
        phi=1.25,
        v=0.0,
        theta=0.4,
        rho_m=0.9,
        rho_r=3.0e-4,
    )
    config = module.ChargeReducedSolverConfig(
        N_initial=-1.0,
        N_final=0.0,
        samples=401,
        rtol=1.0e-11,
        atol=1.0e-13,
    )

    solution = module.solve_charge_reduced_background(
        parameters,
        initial,
        config,
    )

    interior_residual = solution.total_continuity_residual[2:-2]

    assert interior_residual.size > 0
    assert np.max(np.abs(interior_residual)) < 1.0e-4
    assert np.all(
        np.isfinite(solution.total_continuity_residual)
    )



def test_nontrivial_expansion_satisfies_raychaudhuri_residual():
    parameters = module.ChargeReducedParameters(
        rho_star=1.0,
        m_phi_squared=0.0,
        lambda_phi=0.0,
        Q_theta=0.0,
    )
    initial = module.ChargeReducedInitialData(
        phi=1.25,
        v=0.0,
        theta=0.4,
        rho_m=0.9,
        rho_r=3.0e-4,
    )
    config = module.ChargeReducedSolverConfig(
        N_initial=-1.0,
        N_final=0.0,
        samples=401,
        rtol=1.0e-11,
        atol=1.0e-13,
    )

    solution = module.solve_charge_reduced_background(
        parameters,
        initial,
        config,
    )

    interior_residual = solution.raychaudhuri_residual[2:-2]

    assert interior_residual.size > 0
    assert solution.H[-1] < solution.H[0]
    assert np.all(np.isfinite(solution.raychaudhuri_residual))
    assert np.max(np.abs(interior_residual)) < 1.0e-4


def test_derivative_residuals_converge_under_grid_refinement():
    parameters = module.ChargeReducedParameters(
        rho_star=1.0,
        m_phi_squared=0.0,
        lambda_phi=0.0,
        Q_theta=0.0,
    )
    initial = module.ChargeReducedInitialData(
        phi=1.25,
        v=0.0,
        theta=0.4,
        rho_m=0.9,
        rho_r=3.0e-4,
    )

    residual_maxima = []

    for samples in (101, 201, 401):
        solution = module.solve_charge_reduced_background(
            parameters,
            initial,
            module.ChargeReducedSolverConfig(
                N_initial=-1.0,
                N_final=0.0,
                samples=samples,
                rtol=1.0e-12,
                atol=1.0e-14,
            ),
        )

        residual_maxima.append(
            (
                np.max(
                    np.abs(
                        solution.total_continuity_residual[2:-2]
                    )
                ),
                np.max(
                    np.abs(
                        solution.raychaudhuri_residual[2:-2]
                    )
                ),
            )
        )

    continuity_maxima = np.asarray(
        [entry[0] for entry in residual_maxima]
    )
    raychaudhuri_maxima = np.asarray(
        [entry[1] for entry in residual_maxima]
    )

    assert np.all(np.isfinite(continuity_maxima))
    assert np.all(np.isfinite(raychaudhuri_maxima))

    assert continuity_maxima[1] < 0.5 * continuity_maxima[0]
    assert continuity_maxima[2] < 0.5 * continuity_maxima[1]

    assert raychaudhuri_maxima[1] < 0.5 * raychaudhuri_maxima[0]
    assert raychaudhuri_maxima[2] < 0.5 * raychaudhuri_maxima[1]



def _dfm_cdm_unit_map():
    return module.build_dfm_cdm_unit_map(
        H0_km_s_Mpc=67.4,
        omega_b0=0.0224 / 0.674**2,
        omega_cdm0=0.120 / 0.674**2,
        omega_r0=9.2e-5,
    )


def _dfm_cdm_config():
    return module.ChargeReducedSolverConfig(
        N_initial=-0.1,
        N_final=0.0,
        samples=101,
        rtol=1.0e-10,
        atol=1.0e-12,
    )


def test_bbn_thermodynamic_reference_round_trip_and_species_split():
    unit_map = _dfm_cdm_unit_map()

    reference = module.build_bbn_thermodynamic_reference(
        unit_map,
        T_gamma_MeV=1.0,
    )

    assert reference.T_gamma_MeV == pytest.approx(1.0)

    assert module.bbn_temperature_from_efold(
        reference.N
    ) == pytest.approx(
        reference.T_gamma_MeV,
        rel=0.0,
        abs=2.0e-14,
    )

    assert reference.a == pytest.approx(
        np.exp(reference.N),
        rel=2.0e-15,
    )

    assert 5.0 < reference.g_s_em < 5.5
    assert 0.0 < reference.T_nu_MeV <= 1.0

    assert reference.rho_gamma_code > 0.0
    assert reference.rho_e_pm_code > 0.0
    assert reference.rho_nu_code > 0.0

    assert reference.rho_radiation_code == pytest.approx(
        reference.rho_gamma_code
        + reference.rho_e_pm_code
        + reference.rho_nu_code,
        rel=2.0e-15,
    )

    assert reference.rho_cdm_reference_code == pytest.approx(
        unit_map.rho_cdm0_code * reference.a**-3,
        rel=2.0e-15,
    )

    assert module.bbn_em_entropy_degrees(
        10.0
    ) == pytest.approx(
        5.5,
        rel=2.0e-4,
    )


def test_bbn_dfm_density_excess_is_stable_against_large_reference_density():
    unit_map = _dfm_cdm_unit_map()

    reference = module.build_bbn_thermodynamic_reference(
        unit_map,
        T_gamma_MeV=1.0,
    )

    mass_shift = 0.2

    parameters = module.ChargeReducedParameters(
        alpha=1.0,
        beta=1.0,
        rho_star=reference.rho_cdm_reference_code,
        m_phi_squared=mass_shift,
        lambda_phi=0.0,
        Q_theta=0.0,
    )

    excess = module.bbn_dfm_density_excess(
        reference=reference,
        phi=1.0,
        v=0.0,
        parameters=parameters,
    )

    assert excess == pytest.approx(
        0.5 * mass_shift,
        rel=2.0e-15,
        abs=1.0e-15,
    )


def test_bbn_dfm_effective_neutrino_number_uses_one_species_energy():
    unit_map = _dfm_cdm_unit_map()

    reference = module.build_bbn_thermodynamic_reference(
        unit_map,
        T_gamma_MeV=1.0,
    )

    rho_one_neutrino_species = (
        reference.rho_gamma_code
        * (7.0 / 8.0)
        * (
            reference.T_nu_MeV
            / reference.T_gamma_MeV
        ) ** 4
    )

    baseline_parameters = module.ChargeReducedParameters(
        alpha=1.0,
        beta=1.0,
        rho_star=reference.rho_cdm_reference_code,
        m_phi_squared=0.0,
        lambda_phi=0.0,
        Q_theta=0.0,
    )

    baseline_n_eff = module.bbn_dfm_effective_neutrino_number(
        reference=reference,
        phi=1.0,
        v=0.0,
        parameters=baseline_parameters,
    )

    assert baseline_n_eff == pytest.approx(
        module.STANDARD_BBN_N_NU,
        rel=0.0,
        abs=1.0e-14,
    )

    target_delta_n_eff = 0.25

    shifted_parameters = module.ChargeReducedParameters(
        alpha=1.0,
        beta=1.0,
        rho_star=reference.rho_cdm_reference_code,
        m_phi_squared=(
            2.0
            * target_delta_n_eff
            * rho_one_neutrino_species
        ),
        lambda_phi=0.0,
        Q_theta=0.0,
    )

    shifted_n_eff = module.bbn_dfm_effective_neutrino_number(
        reference=reference,
        phi=1.0,
        v=0.0,
        parameters=shifted_parameters,
    )

    assert shifted_n_eff == pytest.approx(
        module.STANDARD_BBN_N_NU
        + target_delta_n_eff,
        rel=2.0e-15,
        abs=1.0e-14,
    )


def test_bbn_neff_likelihood_is_statistical_not_exact_closure():
    unit_map = _dfm_cdm_unit_map()

    reference = module.build_bbn_thermodynamic_reference(
        unit_map,
        T_gamma_MeV=1.0,
    )

    rho_one_neutrino_species = (
        reference.rho_gamma_code
        * (7.0 / 8.0)
        * (
            reference.T_nu_MeV
            / reference.T_gamma_MeV
        ) ** 4
    )

    target_excess = (
        module.BBN_N_EFF_TARGET
        - module.STANDARD_BBN_N_NU
    ) * rho_one_neutrino_species

    target_parameters = module.ChargeReducedParameters(
        alpha=1.0,
        beta=1.0,
        rho_star=(
            reference.rho_cdm_reference_code
            + target_excess
        ),
        m_phi_squared=0.0,
        lambda_phi=0.0,
        Q_theta=0.0,
    )

    likelihood = module.evaluate_bbn_neff_likelihood(
        reference=reference,
        phi=1.0,
        v=0.0,
        parameters=target_parameters,
    )

    assert likelihood.n_eff_dfm == pytest.approx(
        module.BBN_N_EFF_TARGET,
        rel=0.0,
        abs=2.0e-14,
    )
    assert likelihood.residual == pytest.approx(
        0.0,
        rel=0.0,
        abs=2.0e-14,
    )
    assert likelihood.z_score == pytest.approx(
        0.0,
        rel=0.0,
        abs=2.0e-13,
    )
    assert likelihood.chi_squared == pytest.approx(
        0.0,
        rel=0.0,
        abs=1.0e-24,
    )
    assert likelihood.admissible_1sigma is True

    two_sigma_excess = (
        module.BBN_N_EFF_TARGET
        + 2.0 * module.BBN_N_EFF_SIGMA
        - module.STANDARD_BBN_N_NU
    ) * rho_one_neutrino_species

    two_sigma_parameters = module.ChargeReducedParameters(
        alpha=1.0,
        beta=1.0,
        rho_star=(
            reference.rho_cdm_reference_code
            + two_sigma_excess
        ),
        m_phi_squared=0.0,
        lambda_phi=0.0,
        Q_theta=0.0,
    )

    two_sigma_likelihood = module.evaluate_bbn_neff_likelihood(
        reference=reference,
        phi=1.0,
        v=0.0,
        parameters=two_sigma_parameters,
    )

    assert two_sigma_likelihood.z_score == pytest.approx(
        2.0,
        rel=2.0e-13,
        abs=2.0e-13,
    )
    assert two_sigma_likelihood.chi_squared == pytest.approx(
        4.0,
        rel=4.0e-13,
        abs=4.0e-13,
    )
    assert two_sigma_likelihood.admissible_1sigma is False


def test_dfm_particle_mass_eV_uses_H0_normalized_mass_scale():
    unit_map = _dfm_cdm_unit_map()

    mass_eV = module.dfm_particle_mass_eV(
        unit_map=unit_map,
        alpha=1.0,
        m_phi_squared=1.0,
    )

    expected = (
        6.582119569e-16
        * unit_map.H0_si
    )

    assert mass_eV == pytest.approx(
        expected,
        rel=2.0e-15,
    )

    assert mass_eV == pytest.approx(
        1.4377226629626768e-33,
        rel=2.0e-12,
    )


def test_minimum_m_phi_squared_from_LRS_mass_lower_bound():
    unit_map = _dfm_cdm_unit_map()

    minimum = module.minimum_m_phi_squared_from_particle_mass(
        unit_map=unit_map,
        alpha=1.0,
    )

    assert minimum == pytest.approx(
        2.786584686766427e24,
        rel=2.0e-12,
    )

    recovered_mass = module.dfm_particle_mass_eV(
        unit_map=unit_map,
        alpha=1.0,
        m_phi_squared=minimum,
    )

    assert recovered_mass == pytest.approx(
        module.LRS_PARTICLE_MASS_LOWER_EV,
        rel=2.0e-15,
    )


def test_dfm_lrs_self_interaction_interval_round_trips():
    unit_map = _dfm_cdm_unit_map()

    minimum_m2 = (
        module.minimum_m_phi_squared_from_particle_mass(
            unit_map=unit_map,
            alpha=1.0,
        )
    )

    lower, upper = module.dfm_lambda_phi_interval_from_lrs(
        unit_map=unit_map,
        m_phi_squared=minimum_m2,
    )

    assert lower == pytest.approx(
        2.353977053406619e34,
        rel=3.0e-10,
    )

    assert upper == pytest.approx(
        9.911482330133133e35,
        rel=3.0e-10,
    )

    recovered_lower = (
        module.dfm_lrs_self_interaction_strength_eV_inv_cm3(
            unit_map=unit_map,
            m_phi_squared=minimum_m2,
            lambda_phi=lower,
        )
    )

    recovered_upper = (
        module.dfm_lrs_self_interaction_strength_eV_inv_cm3(
            unit_map=unit_map,
            m_phi_squared=minimum_m2,
            lambda_phi=upper,
        )
    )

    assert recovered_lower == pytest.approx(
        module.LRS_SELF_INTERACTION_LOWER_EV_INV_CM3,
        rel=3.0e-15,
    )

    assert recovered_upper == pytest.approx(
        module.LRS_SELF_INTERACTION_UPPER_EV_INV_CM3,
        rel=3.0e-15,
    )

    assert lower > 0.0
    assert upper > lower


def test_positive_lambda_family_round_trips_through_scattering_length():
    unit_map = _dfm_cdm_unit_map()

    alpha = 1.0

    m_phi_squared = (
        module.minimum_m_phi_squared_from_particle_mass(
            unit_map=unit_map,
            alpha=alpha,
        )
    )

    lambda_lower, _ = (
        module.dfm_lambda_phi_interval_from_lrs(
            unit_map=unit_map,
            m_phi_squared=m_phi_squared,
        )
    )

    scattering_length_cm = module.dfm_scattering_length_cm(
        unit_map=unit_map,
        alpha=alpha,
        m_phi_squared=m_phi_squared,
        lambda_phi=lambda_lower,
    )

    assert scattering_length_cm > 0.0

    mass_eV = module.dfm_particle_mass_eV(
        unit_map=unit_map,
        alpha=alpha,
        m_phi_squared=m_phi_squared,
    )

    recovered_strength = (
        4.0
        * np.pi
        * module.HBAR_C_EV_CM**2
        * scattering_length_cm
        / mass_eV**3
    )

    assert recovered_strength == pytest.approx(
        module.LRS_SELF_INTERACTION_LOWER_EV_INV_CM3,
        rel=4.0e-15,
    )

    recovered_lambda = (
        module.dfm_lambda_phi_from_scattering_length_cm(
            unit_map=unit_map,
            alpha=alpha,
            m_phi_squared=m_phi_squared,
            scattering_length_cm=scattering_length_cm,
        )
    )

    assert recovered_lambda == pytest.approx(
        lambda_lower,
        rel=4.0e-15,
    )


def test_lrs_antlia_scattering_length_intersection_is_fail_closed():
    intersection = (
        module.dfm_lrs_antlia_scattering_length_intersection(
            particle_mass_eV=2.4e-21,
            minimum_halo_mass_solar=1.66e9,
        )
    )

    assert intersection[
        "antlia_strength_95_eq5"
    ] == pytest.approx(
        8.32e-19,
        rel=2.0e-15,
    )

    assert intersection[
        "antlia_95_internal_gap"
    ] > 0.0

    assert (
        intersection[
            "antlia_95_printed_equals_eq5"
        ]
        is False
    )

    assert (
        intersection[
            "overlap_with_printed_95"
        ]
        is False
    )

    assert (
        intersection[
            "overlap_with_eq5_95"
        ]
        is False
    )

    assert (
        intersection["lrs_a_s_lower_cm"]
        > intersection["antlia_a_s_95_printed_cm"]
    )

    assert (
        intersection["lrs_a_s_lower_cm"]
        > intersection["antlia_a_s_95_eq5_cm"]
    )

    assert intersection["tf_hierarchy_68"] > 0.0
    assert intersection["tf_hierarchy_95"] > 0.0


def test_dfm_cdm_unit_map_locks_h0_g_and_density_budget():
    unit_map = _dfm_cdm_unit_map()
    assert unit_map.H0_code == 1.0
    assert unit_map.G_code == pytest.approx(1.0 / (8.0 * np.pi))
    assert unit_map.rho_b0_code == pytest.approx(3.0 * unit_map.omega_b0)
    assert unit_map.rho_cdm0_code == pytest.approx(3.0 * unit_map.omega_cdm0)
    assert unit_map.rho_r0_code == pytest.approx(3.0 * unit_map.omega_r0)
    assert unit_map.Lambda_code == pytest.approx(3.0 * unit_map.omega_lambda0)
    assert (
        unit_map.omega_b0
        + unit_map.omega_cdm0
        + unit_map.omega_r0
        + unit_map.omega_lambda0
    ) == pytest.approx(1.0)


def test_dfm_cdm_shooting_overrides_free_g_and_lambda_background_inputs():
    unit_map = _dfm_cdm_unit_map()
    config = _dfm_cdm_config()
    common = dict(
        alpha=1.0,
        beta=1.0,
        rho_star=0.2,
        m_phi_squared=1.0,
        lambda_phi=0.1,
        Q_theta=0.6,
    )
    first = module.shoot_dfm_cdm_background(
        unit_map=unit_map,
        parameters=module.ChargeReducedParameters(
            G=0.2,
            Lambda=0.3,
            **common,
        ),
        phi_initial=1.0,
        v_initial=0.1,
        config=config,
    )
    second = module.shoot_dfm_cdm_background(
        unit_map=unit_map,
        parameters=module.ChargeReducedParameters(
            G=0.7,
            Lambda=1.4,
            **common,
        ),
        phi_initial=1.0,
        v_initial=0.1,
        config=config,
    )
    np.testing.assert_allclose(first.H, second.H, rtol=0.0, atol=0.0)
    np.testing.assert_allclose(
        first.rho_dfm_mkc,
        second.rho_dfm_mkc,
        rtol=0.0,
        atol=0.0,
    )


def test_dfm_cdm_shooting_jacobian_has_rank_two_and_four_null_directions():
    vector = np.asarray((1.0, 0.1, 0.2, 1.0, 0.1, 0.6), dtype=float)
    analysis = module.analyze_dfm_cdm_shooting_jacobian(
        vector,
        alpha=1.0,
        beta=1.0,
        unit_map=_dfm_cdm_unit_map(),
        config=_dfm_cdm_config(),
    )
    assert analysis.rank == 2
    assert analysis.nullity == 4
    assert analysis.locally_identifiable is False
    assert analysis.null_space_basis.shape == (6, 4)
    assert analysis.friedmann_row_dependency_error < 1.0e-8
    np.testing.assert_allclose(
        analysis.jacobian @ analysis.null_space_basis,
        0.0,
        rtol=0.0,
        atol=2.0e-8,
    )


def _dfm_cdm_null_chart():
    vector = np.asarray((1.0, 0.1, 0.2, 1.0, 0.1, 0.6), dtype=float)
    analysis = module.analyze_dfm_cdm_shooting_jacobian(
        vector,
        alpha=1.0,
        beta=1.0,
        unit_map=_dfm_cdm_unit_map(),
        config=_dfm_cdm_config(),
    )
    return module.DFMCDMNullChart(
        base_vector=vector,
        null_basis=analysis.null_space_basis,
        eta_lower=-1.0e-4 * np.ones(4),
        eta_upper=1.0e-4 * np.ones(4),
    )


def test_dfm_cdm_null_chart_rejects_non_null_basis():
    vector = np.asarray((1.0, 0.1, 0.2, 1.0, 0.1, 0.6), dtype=float)
    base_analysis = module.analyze_dfm_cdm_shooting_jacobian(
        vector,
        alpha=1.0,
        beta=1.0,
        unit_map=_dfm_cdm_unit_map(),
        config=_dfm_cdm_config(),
    )
    bad_basis = base_analysis.null_space_basis.copy()
    bad_basis[:, 0] = base_analysis.jacobian[0, :]
    chart = module.DFMCDMNullChart(
        base_vector=vector,
        null_basis=bad_basis,
        eta_lower=-1.0e-4 * np.ones(4),
        eta_upper=1.0e-4 * np.ones(4),
    )
    with pytest.raises(ValueError, match="does not lie in the base Jacobian null space"):
        module.evaluate_dfm_cdm_null_chart_candidate(
            chart,
            np.zeros(4),
            alpha=1.0,
            beta=1.0,
            unit_map=_dfm_cdm_unit_map(),
            config=_dfm_cdm_config(),
        )


def test_dfm_cdm_null_chart_accepts_bounded_rank_two_candidate():
    analysis = module.evaluate_dfm_cdm_null_chart_candidate(
        _dfm_cdm_null_chart(),
        np.zeros(4),
        alpha=1.0,
        beta=1.0,
        unit_map=_dfm_cdm_unit_map(),
        config=_dfm_cdm_config(),
    )
    assert analysis.rank == 2
    assert analysis.nullity == 4


def test_dfm_cdm_null_chart_rejects_eta_outside_bounds():
    with pytest.raises(ValueError, match="outside the null-chart bounds"):
        _dfm_cdm_null_chart().candidate_vector(
            np.asarray((2.0e-4, 0.0, 0.0, 0.0))
        )


def test_dfm_cdm_null_chart_rejects_static_physical_domain_failure():
    chart = module.DFMCDMNullChart(
        base_vector=np.asarray((1.0, 0.1, 0.2, 1.0, 0.1, 0.6)),
        null_basis=np.asarray(
            (
                (1.0, 0.0, 0.0, 0.0),
                (0.0, 0.0, 0.0, 0.0),
                (0.0, 1.0, 0.0, 0.0),
                (0.0, 0.0, 1.0, 0.0),
                (0.0, 0.0, 0.0, 1.0),
                (0.0, 0.0, 0.0, 0.0),
            )
        ),
        eta_lower=-2.0 * np.ones(4),
        eta_upper=2.0 * np.ones(4),
    )
    with pytest.raises(ValueError, match="phi_initial must be positive"):
        chart.candidate_vector(np.asarray((-2.0, 0.0, 0.0, 0.0)))


def test_dfm_cdm_null_chart_rejects_rank_change(monkeypatch):
    chart = _dfm_cdm_null_chart()

    class RankOneAnalysis:
        rank = 1

    monkeypatch.setattr(
        module,
        "analyze_dfm_cdm_shooting_jacobian",
        lambda *args, **kwargs: RankOneAnalysis(),
    )
    with pytest.raises(ValueError, match="rank must equal 2; got 1"):
        module.evaluate_dfm_cdm_null_chart_candidate(
            chart,
            np.zeros(4),
            alpha=1.0,
            beta=1.0,
            unit_map=_dfm_cdm_unit_map(),
            config=_dfm_cdm_config(),
        )


def test_canonical_action_supersedes_legacy_phi_and_locks_cdm_branch():
    theory = Path("theory/deformation_field.md").read_text()
    assert "supersedes the" in theory
    assert "legacy `Phi` equations" in theory
    assert "DFM–MKC is locked as a cold-dark-matter replacement" in theory
    assert "rank at most two" in theory
    assert "nullity" in theory


def test_minimal_circular_closure_residual_formula():
    vector = np.asarray(
        (1.0, 0.1, 0.2, 1.0, 0.1, 0.6),
        dtype=float,
    )

    closures = (
        module.dfm_cdm_minimal_circular_closure_residuals(
            vector,
            beta=1.0,
            N_initial=-0.1,
        )
    )

    expected_force = (
        1.0
        + 0.1
        - 0.6**2 * np.exp(0.6)
    )

    np.testing.assert_allclose(
        closures.as_array(),
        np.asarray(
            (
                0.1,
                0.2,
                0.1,
                expected_force,
            )
        ),
        rtol=0.0,
        atol=1.0e-14,
    )


def test_minimal_circular_closure_requires_positive_beta_and_charge():
    vector = np.asarray(
        (1.0, 0.1, 0.2, 1.0, 0.1, 0.6),
        dtype=float,
    )

    with pytest.raises(
        ValueError,
        match="beta to be positive",
    ):
        module.dfm_cdm_minimal_circular_closure_residuals(
            vector,
            beta=0.0,
            N_initial=-0.1,
        )

    zero_charge = vector.copy()
    zero_charge[5] = 0.0

    with pytest.raises(
        ValueError,
        match="positive-charge branch",
    ):
        module.dfm_cdm_minimal_circular_closure_residuals(
            zero_charge,
            beta=1.0,
            N_initial=-0.1,
        )


def test_dfm_cdm_augmented_residual_uses_six_independent_rows():
    vector = np.asarray(
        (1.0, 0.1, 0.2, 1.0, 0.1, 0.6),
        dtype=float,
    )

    residual = module.dfm_cdm_augmented_residual_vector(
        vector,
        alpha=1.0,
        beta=1.0,
        unit_map=_dfm_cdm_unit_map(),
        config=_dfm_cdm_config(),
    )

    assert residual.shape == (6,)
    assert module.DFM_CDM_AUGMENTED_RESIDUAL_NAMES == (
        "F_rho",
        "F_w",
        "C_v_initial",
        "C_rho_star",
        "C_lambda_phi",
        "C_circular_force",
    )


def test_minimal_circular_closure_augmented_jacobian_has_rank_six():
    vector = np.asarray(
        (1.0, 0.1, 0.2, 1.0, 0.1, 0.6),
        dtype=float,
    )

    analysis = module.analyze_dfm_cdm_augmented_jacobian(
        vector,
        alpha=1.0,
        beta=1.0,
        unit_map=_dfm_cdm_unit_map(),
        config=_dfm_cdm_config(),
    )

    assert analysis.jacobian.shape == (6, 6)
    assert analysis.rank == 6
    assert analysis.locally_identifiable is True
    assert np.isfinite(analysis.condition_number)
    assert analysis.condition_number < 1.0e4
    assert analysis.singular_values[-1] > analysis.rank_tolerance


def test_minimal_circular_closure_is_documented_as_conditional():
    theory = Path("theory/deformation_field.md").read_text()

    assert "Minimal circular physical closure" in theory
    assert r"C_{v_i}=v_i=0" in theory
    assert r"C_{\rho_\star}=\rho_\star=0" in theory
    assert r"C_{\lambda_\phi}=\lambda_\phi=0" in theory
    assert "positive-charge branch" in theory
    assert "Growth likelihood remains blocked" in theory


def test_constant_w_dark_energy_preserves_lambda_baseline():
    import numpy as np
    import pytest

    from dfm_mkc_solver.charge_reduced_background_v1 import (
        ChargeReducedParameters,
        dark_energy_density,
        dark_energy_equation_of_state,
        dark_energy_pressure,
        dfm_energy_density,
        friedmann_radicand,
    )

    parameters = ChargeReducedParameters(
        G=1.0 / (8.0 * np.pi),
        Lambda=2.1,
        w0=-1.0,
        wa=0.0,
        alpha=1.0,
        beta=1.0,
        rho_star=0.2,
        m_phi_squared=0.1,
        lambda_phi=0.0,
        Q_theta=0.0,
    )
    state = (1.0, 0.0, 0.0, 0.7, 2.0e-4)
    expected_density = (
        parameters.Lambda
        / (8.0 * np.pi * parameters.G)
    )

    for N in (-4.0, -1.0, 0.0):
        assert dark_energy_equation_of_state(
            N,
            parameters,
        ) == pytest.approx(-1.0)
        assert dark_energy_density(
            N,
            parameters,
        ) == pytest.approx(expected_density)
        assert dark_energy_pressure(
            N,
            parameters,
        ) == pytest.approx(-expected_density)

        old_radicand = (
            parameters.Lambda / 3.0
            + (
                8.0 * np.pi * parameters.G / 3.0
            )
            * (
                state[3]
                + state[4]
                + dfm_energy_density(
                    N,
                    state[0],
                    state[1],
                    parameters,
                )
            )
        )
        assert friedmann_radicand(
            N,
            state,
            parameters,
        ) == pytest.approx(
            old_radicand,
            rel=2.0e-15,
            abs=2.0e-15,
        )

    constant_w = ChargeReducedParameters(
        G=parameters.G,
        Lambda=parameters.Lambda,
        w0=-0.9,
        wa=0.0,
        alpha=parameters.alpha,
        beta=parameters.beta,
        rho_star=parameters.rho_star,
        m_phi_squared=parameters.m_phi_squared,
        lambda_phi=parameters.lambda_phi,
        Q_theta=parameters.Q_theta,
    )
    N = -2.0
    assert dark_energy_density(
        N,
        constant_w,
    ) == pytest.approx(
        expected_density
        * np.exp(-3.0 * (1.0 + constant_w.w0) * N)
    )

    cpl = ChargeReducedParameters(
        G=parameters.G,
        Lambda=parameters.Lambda,
        w0=-0.95,
        wa=0.2,
        alpha=parameters.alpha,
        beta=parameters.beta,
        rho_star=parameters.rho_star,
        m_phi_squared=parameters.m_phi_squared,
        lambda_phi=parameters.lambda_phi,
        Q_theta=parameters.Q_theta,
    )
    a = np.exp(N)
    expected_w = cpl.w0 + cpl.wa * (1.0 - a)
    expected_cpl_density = expected_density * np.exp(
        -3.0 * (1.0 + cpl.w0 + cpl.wa) * N
        + 3.0 * cpl.wa * (a - 1.0)
    )
    assert dark_energy_equation_of_state(
        N,
        cpl,
    ) == pytest.approx(expected_w)
    assert dark_energy_density(
        N,
        cpl,
    ) == pytest.approx(expected_cpl_density)
    assert dark_energy_pressure(
        N,
        cpl,
    ) == pytest.approx(expected_w * expected_cpl_density)


def test_positive_lambda_family_residual_is_augmented_map_without_C_lambda_phi():
    unit_map = _dfm_cdm_unit_map()

    config = module.ChargeReducedSolverConfig(
        N_initial=-0.1,
        N_final=0.0,
        samples=101,
        rtol=1.0e-10,
        atol=1.0e-12,
    )

    alpha = 1.0
    beta = 1.0

    m_phi_squared = (
        module.minimum_m_phi_squared_from_particle_mass(
            unit_map=unit_map,
            alpha=alpha,
        )
    )

    lambda_lower, _ = (
        module.dfm_lambda_phi_interval_from_lrs(
            unit_map=unit_map,
            m_phi_squared=m_phi_squared,
        )
    )

    candidate = np.asarray(
        (
            1.0,
            0.1,
            0.2,
            m_phi_squared,
            lambda_lower,
            0.6,
        ),
        dtype=float,
    )

    family = (
        module.dfm_cdm_positive_lambda_family_residual_vector(
            candidate,
            alpha=alpha,
            beta=beta,
            unit_map=unit_map,
            config=config,
        )
    )

    augmented = module.dfm_cdm_augmented_residual_vector(
        candidate,
        alpha=alpha,
        beta=beta,
        unit_map=unit_map,
        config=config,
    )

    assert module.DFM_CDM_POSITIVE_LAMBDA_FAMILY_RESIDUAL_NAMES == (
        "F_rho",
        "F_w",
        "C_v_initial",
        "C_rho_star",
        "C_circular_force",
    )

    assert family.shape == (5,)
    assert np.all(np.isfinite(family))

    # Only the exact closure rows remain shared with the direct
    # augmented system. F_rho and F_w now belong to the algebraic
    # circular family evaluator and do not call solve_ivp.
    np.testing.assert_allclose(
        family[2:4],
        augmented[2:4],
        rtol=0.0,
        atol=0.0,
    )

    assert augmented[4] == pytest.approx(
        lambda_lower,
        rel=2.0e-15,
    )


def test_charge_reduced_state_nonzero_guard_is_scale_free():
    module.validate_state(
        (
            1.0e-30,
            0.0,
            0.0,
            1.0,
            1.0e-4,
        )
    )

    module.validate_state(
        (
            -1.0e-30,
            0.0,
            0.0,
            1.0,
            1.0e-4,
        )
    )

    with pytest.raises(
        ValueError,
        match="phi must remain nonzero",
    ):
        module.validate_state(
            (
                0.0,
                0.0,
                0.0,
                1.0,
                1.0e-4,
            )
        )


def test_circular_phi_squared_positive_root_closes_cubic():
    unit_map = _dfm_cdm_unit_map()

    alpha = 1.0
    beta = 1.0
    N_initial = -0.1
    a = np.exp(N_initial)

    m_phi_squared = (
        module.minimum_m_phi_squared_from_particle_mass(
            unit_map=unit_map,
            alpha=alpha,
        )
    )

    lambda_phi, _ = (
        module.dfm_lambda_phi_interval_from_lrs(
            unit_map=unit_map,
            m_phi_squared=m_phi_squared,
        )
    )

    Q_theta = 4.747298986616094e-13

    x = module.circular_phi_squared_positive_root(
        a=a,
        beta=beta,
        m_phi_squared=m_phi_squared,
        lambda_phi=lambda_phi,
        Q_theta=Q_theta,
    )

    assert x > 0.0

    c = (
        Q_theta**2
        / (beta * a**6)
    )

    normalized_residual = (
        m_phi_squared * x**2 / c
        + lambda_phi * x**3 / c
        - 1.0
    )

    assert normalized_residual == pytest.approx(
        0.0,
        abs=5.0e-14,
    )

    phi = np.sqrt(x)

    circular_force = (
        m_phi_squared * phi
        + lambda_phi * phi**3
        - Q_theta**2
        * np.exp(-6.0 * N_initial)
        / (beta * phi**3)
    )

    force_scale = (
        m_phi_squared * phi
        + lambda_phi * phi**3
        + Q_theta**2
        * np.exp(-6.0 * N_initial)
        / (beta * phi**3)
    )

    assert circular_force / force_scale == pytest.approx(
        0.0,
        abs=5.0e-14,
    )


def test_circular_energy_density_pressure_matches_stable_circular_identity():
    unit_map = _dfm_cdm_unit_map()

    alpha = 1.0
    beta = 1.0
    a = np.exp(-0.1)
    rho_star = 0.0

    m_phi_squared = (
        module.minimum_m_phi_squared_from_particle_mass(
            unit_map=unit_map,
            alpha=alpha,
        )
    )

    lambda_phi, _ = (
        module.dfm_lambda_phi_interval_from_lrs(
            unit_map=unit_map,
            m_phi_squared=m_phi_squared,
        )
    )

    Q_theta = 4.747298986616094e-13

    x = module.circular_phi_squared_positive_root(
        a=a,
        beta=beta,
        m_phi_squared=m_phi_squared,
        lambda_phi=lambda_phi,
        Q_theta=Q_theta,
    )

    rho_circ, p_circ = (
        module.circular_energy_density_pressure(
            a=a,
            beta=beta,
            rho_star=rho_star,
            m_phi_squared=m_phi_squared,
            lambda_phi=lambda_phi,
            Q_theta=Q_theta,
        )
    )

    phase = (
        Q_theta**2
        / (2.0 * beta * a**6 * x)
    )

    phase_from_circular_force = (
        0.5 * m_phi_squared * x
        + 0.5 * lambda_phi * x**2
    )

    phase_scale = max(
        abs(phase),
        abs(phase_from_circular_force),
    )

    assert (
        abs(phase - phase_from_circular_force)
        / phase_scale
    ) <= 5.0e-14

    expected_rho = (
        rho_star
        + m_phi_squared * x
        + 0.75 * lambda_phi * x**2
    )

    expected_p = (
        -rho_star
        + 0.25 * lambda_phi * x**2
    )

    assert rho_circ == pytest.approx(
        expected_rho,
        rel=5.0e-14,
    )

    assert p_circ == pytest.approx(
        expected_p,
        rel=5.0e-14,
        abs=1.0e-30,
    )

    assert (
        p_circ + rho_star
    ) == pytest.approx(
        0.25 * lambda_phi * x**2,
        rel=5.0e-14,
        abs=1.0e-30,
    )


def test_normalized_circular_force_residual_is_machine_small_at_certified_root():
    unit_map = _dfm_cdm_unit_map()

    alpha = 1.0
    beta = 1.0
    N = -0.1
    a = np.exp(N)

    m_phi_squared = (
        module.minimum_m_phi_squared_from_particle_mass(
            unit_map=unit_map,
            alpha=alpha,
        )
    )

    lambda_phi, _ = (
        module.dfm_lambda_phi_interval_from_lrs(
            unit_map=unit_map,
            m_phi_squared=m_phi_squared,
        )
    )

    Q_theta = 4.747298986616094e-13

    x = module.circular_phi_squared_positive_root(
        a=a,
        beta=beta,
        m_phi_squared=m_phi_squared,
        lambda_phi=lambda_phi,
        Q_theta=Q_theta,
    )

    phi = np.sqrt(x)

    normalized = module.normalized_circular_force_residual(
        N=N,
        phi=phi,
        beta=beta,
        m_phi_squared=m_phi_squared,
        lambda_phi=lambda_phi,
        Q_theta=Q_theta,
    )

    assert abs(normalized) <= 5.0e-14


def test_positive_lambda_family_algebraic_rows_close_without_direct_shooting(
    monkeypatch,
):
    unit_map = _dfm_cdm_unit_map()

    alpha = 1.0
    beta = 1.0
    N_initial = -0.1

    config = module.ChargeReducedSolverConfig(
        N_initial=N_initial,
        N_final=0.0,
        samples=101,
        rtol=1.0e-10,
        atol=1.0e-12,
    )

    m_phi_squared = (
        module.minimum_m_phi_squared_from_particle_mass(
            unit_map=unit_map,
            alpha=alpha,
        )
    )

    lambda_phi, _ = (
        module.dfm_lambda_phi_interval_from_lrs(
            unit_map=unit_map,
            m_phi_squared=m_phi_squared,
        )
    )

    rho_cdm_initial = (
        unit_map.rho_cdm0_code
        * np.exp(-3.0 * N_initial)
    )

    discriminant = np.sqrt(
        m_phi_squared**2
        + 3.0 * lambda_phi * rho_cdm_initial
    )

    x_initial = (
        2.0 * rho_cdm_initial
        / (
            m_phi_squared
            + discriminant
        )
    )

    phi_initial = np.sqrt(x_initial)

    Q_theta = np.sqrt(
        beta
        * np.exp(6.0 * N_initial)
        * (
            m_phi_squared * x_initial**2
            + lambda_phi * x_initial**3
        )
    )

    candidate = np.asarray(
        (
            phi_initial,
            0.0,
            0.0,
            m_phi_squared,
            lambda_phi,
            Q_theta,
        ),
        dtype=float,
    )

    def forbidden_direct_shooting(*args, **kwargs):
        raise AssertionError(
            "positive-lambda algebraic family must not call direct shooting"
        )

    monkeypatch.setattr(
        module,
        "dfm_cdm_shooting_residual_vector",
        forbidden_direct_shooting,
    )

    family = (
        module.dfm_cdm_positive_lambda_family_residual_vector(
            candidate,
            alpha=alpha,
            beta=beta,
            unit_map=unit_map,
            config=config,
        )
    )

    assert family.shape == (5,)
    assert np.all(np.isfinite(family))

    rho_scale = max(
        abs(unit_map.rho_cdm0_code),
        1.0,
    )

    assert abs(family[0]) / rho_scale <= 1.0e-12
    assert abs(family[1]) <= 1.0e-12
    assert family[2] == 0.0
    assert family[3] == 0.0
    assert abs(family[4]) <= 5.0e-14


def test_exact_positive_lambda_quartic_relative_tracking_certificate():
    certificate = (
        module.exact_positive_lambda_quartic_relative_tracking_certificate()
    )

    assert certificate

    for name, residual in certificate.items():
        assert sp.simplify(residual) == 0, (
            name,
            residual,
        )


def test_exact_positive_lambda_quartic_relative_energy_derivative_certificate():
    certificate = (
        module
        .exact_positive_lambda_quartic_relative_energy_derivative_certificate()
    )

    assert certificate

    for name, residual in certificate.items():
        assert sp.simplify(residual) == 0, (
            name,
            residual,
        )


def test_exact_positive_lambda_quartic_relative_energy_young_majorant_certificate():
    certificate = (
        module
        .exact_positive_lambda_quartic_relative_energy_young_majorant_certificate()
    )

    assert certificate

    for name, residual in certificate.items():
        assert sp.simplify(residual) == 0, (
            name,
            residual,
        )


def test_exact_positive_lambda_quartic_uniform_young_envelope_certificate():
    certificate = (
        module
        .exact_positive_lambda_quartic_uniform_young_envelope_certificate()
    )

    assert certificate

    for name, residual in certificate.items():
        assert sp.simplify(residual) == 0, (
            name,
            residual,
        )


def test_exact_positive_lambda_quartic_initial_energy_gronwall_certificate():
    certificate = (
        module
        .exact_positive_lambda_quartic_initial_energy_gronwall_certificate()
    )

    assert certificate

    for name, residual in certificate.items():
        assert sp.simplify(residual) == 0, (
            name,
            residual,
        )


def test_exact_positive_lambda_quartic_density_pressure_bridge_certificate():
    certificate = (
        module
        .exact_positive_lambda_quartic_density_pressure_bridge_certificate()
    )

    assert certificate

    for name, residual in certificate.items():
        assert sp.simplify(residual) == 0, (
            name,
            residual,
        )


def test_exact_positive_lambda_circular_density_lower_bound_certificate():
    certificate = (
        module
        .exact_positive_lambda_circular_density_lower_bound_certificate()
    )

    assert certificate

    for name, residual in certificate.items():
        assert sp.simplify(residual) == 0, (
            name,
            residual,
        )


def test_bbn_density_excess_uses_exact_nonzero_phi_domain():
    unit_map = _dfm_cdm_unit_map()

    reference = module.build_bbn_thermodynamic_reference(
        unit_map,
        T_gamma_MeV=1.0,
    )

    parameters = module.ChargeReducedParameters(
        alpha=1.0,
        beta=1.0,
        rho_star=0.0,
        m_phi_squared=1.0,
        lambda_phi=1.0,
        Q_theta=1.0e-60,
    )

    value = module.bbn_dfm_density_excess(
        reference=reference,
        phi=1.0e-30,
        v=0.0,
        parameters=parameters,
    )

    assert np.isfinite(value)

    with pytest.raises(
        ValueError,
        match="phi must remain nonzero",
    ):
        module.bbn_dfm_density_excess(
            reference=reference,
            phi=0.0,
            v=0.0,
            parameters=parameters,
        )


def test_exact_positive_lambda_bbn_lrs_monotonicity_certificate():
    certificate = (
        module
        .exact_positive_lambda_bbn_lrs_monotonicity_certificate()
    )

    assert certificate

    for name, residual in certificate.items():
        assert sp.simplify(residual) == 0, (
            name,
            residual,
        )


def test_positive_lambda_lrs_bbn_nonrealization_certificate():
    unit_map = _dfm_cdm_unit_map()

    certificate = (
        module.positive_lambda_lrs_bbn_nonrealization_certificate(
            unit_map,
        )
    )

    assert certificate["excluded_2sigma"] is True
    assert certificate["mass_independent"] is True
    assert (
        certificate[
            "global_minimum_at_lrs_lower_coupling"
        ]
        is True
    )
    assert certificate["rho_exact_gte_rho_circ"] is True

    assert certificate[
        "n_eff_global_lower"
    ] == pytest.approx(
        3.214211020193349,
        rel=5.0e-14,
    )

    assert certificate[
        "bbn_upper_2sigma"
    ] == pytest.approx(
        3.18,
        rel=0.0,
        abs=1.0e-15,
    )

    assert certificate["exclusion_margin"] > 0.0

    assert certificate[
        "exclusion_margin"
    ] == pytest.approx(
        0.034211020193349,
        rel=5.0e-13,
        abs=1.0e-15,
    )
