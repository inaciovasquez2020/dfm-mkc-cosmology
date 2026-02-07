import numpy as np
from dfm_mkc.model import init_params, evolve_background

def test_lcdm_reduction():
    params = init_params(H0=70.0, Omega_m=0.3, Omega_L=0.7)
    a = np.linspace(0.1, 1.0, 5)
    H = evolve_background(params, a)
    expected = 70.0 * np.sqrt(0.3 * a**(-3) + 0.7)
    assert np.allclose(H, expected, rtol=1e-8)

