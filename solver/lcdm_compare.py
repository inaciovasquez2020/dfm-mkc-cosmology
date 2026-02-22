import numpy as np
from solver.background_solver import solve_background
from solver.distances import comoving_distance, luminosity_distance, angular_diameter_distance

def lcdm_H(z, H0, Om_m0, Om_r0, Om_L0):
    return H0 * np.sqrt(Om_m0*(1+z)**3 + Om_r0*(1+z)**4 + Om_L0)

def compare(zmax, params, nz=2000):
    z, H, Phi = solve_background(zmax, params, nz=nz)
    H0, Om_m0, Om_r0, Om_L0, alpha, beta = params
    H_lcdm = lcdm_H(z, H0, Om_m0, Om_r0, Om_L0)

    chi = comoving_distance(z, H)
    chi_lcdm = comoving_distance(z, H_lcdm)

    out = {
        "z": z,
        "H": H,
        "H_lcdm": H_lcdm,
        "Phi": Phi,
        "chi": chi,
        "chi_lcdm": chi_lcdm,
        "dL": luminosity_distance(z, chi),
        "dL_lcdm": luminosity_distance(z, chi_lcdm),
        "dA": angular_diameter_distance(z, chi),
        "dA_lcdm": angular_diameter_distance(z, chi_lcdm),
    }
    return out

if __name__ == "__main__":
    params = (70.0, 0.3, 8.4e-5, 0.699916, 0.0, 0.0)
    out = compare(3.0, params, nz=2000)
    z = out["z"]
    relH = (out["H"] - out["H_lcdm"]) / out["H_lcdm"]
    relDL = (out["dL"] - out["dL_lcdm"]) / out["dL_lcdm"]
    print("max rel H", np.max(np.abs(relH)))
    print("max rel dL", np.max(np.abs(relDL)))
