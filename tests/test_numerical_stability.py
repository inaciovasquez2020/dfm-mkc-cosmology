import numpy as np
from dfm_mkc.model import init_params, evolve_background

def test_numerical_stability_positive_scale():
    params = init_params(H0=70.0, Omega_m=0.3, Omega_L=0.7)
    a = np.logspace(-6, 0, 50)
    H = evolve_background(params, a)
    assert np.all(np.isfinite(H))
    assert np.all(H > 0.0)

