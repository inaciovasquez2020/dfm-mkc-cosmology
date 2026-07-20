import numpy as np
from solver.background_solver import solve_background

def test_background_solver_basic():
    params = (
        70.0,
        0.3,
        9e-5,
        0.7,
        0.0,
        0.0,
    )
    z, H, Phi = solve_background(5.0, params, nz=200)

    assert np.all(np.isfinite(H))
    assert np.all(H > 0.0)
    assert np.all(np.isfinite(Phi))
    assert np.max(np.abs(Phi / H**2)) < 10.0


def test_background_solver_beta_degeneracy():
    """Changing beta alone cannot change the current background IVP."""
    common_parameters = (
        70.0,
        0.3,
        9e-5,
        0.69991,
        0.17,
    )

    params_beta_1 = (*common_parameters, -3.0)
    params_beta_2 = (*common_parameters, 8.5)

    z_1, H_1, Phi_1 = solve_background(5.0, params_beta_1, nz=200)
    z_2, H_2, Phi_2 = solve_background(5.0, params_beta_2, nz=200)

    np.testing.assert_array_equal(z_1, z_2)
    np.testing.assert_array_equal(H_1, H_2)
    np.testing.assert_array_equal(Phi_1, Phi_2)
