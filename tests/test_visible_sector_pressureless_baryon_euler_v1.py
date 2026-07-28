import sympy as sp

from dfm_mkc_solver import visible_sector_action_v1 as visible


def test_pressureless_baryon_euler_force_and_evolution_are_action_bound():
    k2, H, psi, theta = sp.symbols("k2 H Psi_B theta_b")
    row = visible.pressureless_baryon_euler_equation(
        wave_number_squared=k2,
        conformal_hubble=H,
        bardeen_lapse_potential=psi,
        velocity_divergence=theta,
    )
    assert sp.cancel(row.gravitational_force - k2 * psi) == 0
    assert sp.cancel(row.velocity_divergence_prime + H*theta - k2*psi) == 0
    assert row.force_coefficient_residual == 0
    assert row.hubble_drag_coefficient_residual == 0
    assert row.fourier_sign_and_normalization_proved
    assert "Schutz-Sorkin J_b^mu Euler row" in row.action_origin
    assert "collision" not in row.action_origin
