import numpy as np
from src.analysis.fit import fit_lcdm

def test_fit_runs():
    z = np.array([0.1,0.2])
    H = np.array([70,72])
    err = np.array([3,3])
    chi2 = fit_lcdm(z,H,err)
    assert chi2 >= 0
