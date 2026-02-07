import numpy as np
from dfm_mkc.model import init_params, evolve_background

def test_matter_dominated_limit():
    params = init_params(H0=70.0, Omega_m=1.0, Omega_L=0.0)
    a = np.array([0.5, 1.0, 2.0])
    H = evolve_background(params, a)
    expected = 70.0 * a ** (-3/2)
    assert np.allclose(H, expected, rtol=1e-8)

