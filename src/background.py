import numpy as np

def Hubble(z, theta):
    H0, Om, Or, Ol, alpha, beta = theta
    Op = 1.0 - (Om + Or + Ol)
    return H0 * np.sqrt(
        Om*(1+z)**3 + Or*(1+z)**4 + Ol + Op*(1+z)**alpha
    )
