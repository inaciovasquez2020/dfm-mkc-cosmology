import numpy as np
from solver.distances import comoving_distance, luminosity_distance

def test_distances_monotonic():
    z = np.linspace(0.0, 2.0, 100)
    H = 70.0 * np.sqrt(0.3 * (1 + z)**3 + 0.7)

    chi = comoving_distance(z, H)
    dL = luminosity_distance(z, chi)

    assert np.all(np.diff(chi) >= 0.0)
    assert np.all(np.diff(dL) >= 0.0)
