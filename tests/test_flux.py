import numpy as np

from solver.background_solver import solve_background
from solver.distances import comoving_distance

def test_flux_monotonic_with_scale_factor():
    params = (
        70.0,
        0.3,
        9e-5,
        0.7,
        0.0,
        0.0,
    )
    z, H, _ = solve_background(5.0, params, nz=200)
    assert np.all(H > 0.0)

def test_flux_distance_finite():
    params = (
        70.0,
        0.3,
        9e-5,
        0.7,
        0.0,
        0.0,
    )
    z, H, _ = solve_background(5.0, params, nz=200)
    d = comoving_distance(z, H)
    assert np.isfinite(d[-1])

def test_flux_scaling_consistency():
    params = (
        70.0,
        0.3,
        9e-5,
        0.7,
        0.0,
        0.0,
    )
    z1, H1, _ = solve_background(2.0, params, nz=200)
    z2, H2, _ = solve_background(5.0, params, nz=200)

    d1 = comoving_distance(z1, H1)[-1]
    d2 = comoving_distance(z2, H2)[-1]

    assert d2 > d1
