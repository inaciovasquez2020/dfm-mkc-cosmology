import numpy as np
from src.analysis.fisher_matrix import fisher_matrix

def loglike(p):
    return -0.5*(p[0]**2 + p[1]**2)

def test_fisher():
    F = fisher_matrix(loglike,[0.1,0.2])
    assert F.shape == (2,2)
