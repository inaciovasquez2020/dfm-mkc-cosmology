import numpy as np
from solver.background_solver import solve_background
from solver.distances import comoving_distance, luminosity_distance

def lcdm_H(z, H0, Om_m0, Om_r0, Om_L0):
    return H0 * np.sqrt(Om_m0*(1+z)**3 + Om_r0*(1+z)**4 + Om_L0)

def score_against_lcdm(z, H, H_lcdm):
    rel = (H - H_lcdm) / H_lcdm
    return float(np.max(np.abs(rel)))

def run_scan(zmax, base_params, alpha_grid, beta_grid, nz=1200):
    H0, Om_m0, Om_r0, Om_L0, _, _ = base_params
    results = []
    for a in alpha_grid:
        for b in beta_grid:
            params = (H0, Om_m0, Om_r0, Om_L0, float(a), float(b))
            z, H, Phi = solve_background(zmax, params, nz=nz)
            H_lcdm = lcdm_H(z, H0, Om_m0, Om_r0, Om_L0)
            s = score_against_lcdm(z, H, H_lcdm)
            results.append((float(a), float(b), s))
    return results

if __name__ == "__main__":
    base = (70.0, 0.3, 8.4e-5, 0.699916, 0.0, 0.0)
    grid = np.linspace(-0.2, 0.2, 9)
    res = run_scan(3.0, base, grid, grid, nz=1200)
    res.sort(key=lambda t: t[2])
    print("best 10 by max relative H deviation")
    for a, b, s in res[:10]:
        print(a, b, s)
