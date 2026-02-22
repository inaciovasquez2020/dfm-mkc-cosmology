import numpy as np

def comoving_distance(z_grid, H_grid):
    z = np.asarray(z_grid)
    H = np.asarray(H_grid)
    dz = np.diff(z)
    invH_mid = 0.5*(1.0/H[:-1] + 1.0/H[1:])
    chi = np.zeros_like(z)
    chi[1:] = np.cumsum(dz * invH_mid)
    return chi

def luminosity_distance(z_grid, chi_grid):
    z = np.asarray(z_grid)
    chi = np.asarray(chi_grid)
    return (1.0 + z) * chi

def angular_diameter_distance(z_grid, chi_grid):
    z = np.asarray(z_grid)
    chi = np.asarray(chi_grid)
    return chi / (1.0 + z)
