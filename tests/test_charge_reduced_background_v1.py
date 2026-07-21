import importlib.util
import sys
from pathlib import Path

import numpy as np
import pytest


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
