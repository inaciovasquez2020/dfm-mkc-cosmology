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
