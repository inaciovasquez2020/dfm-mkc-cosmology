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
