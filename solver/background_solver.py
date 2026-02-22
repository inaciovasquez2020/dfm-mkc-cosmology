import numpy as np
from scipy.integrate import solve_ivp

def background_odes(z, y, params):
    H, Phi = y
    H0, Om_m0, Om_r0, Om_L0, alpha, beta = params

    Om_Phi0 = 1.0 - (Om_m0 + Om_r0 + Om_L0)

    rho_m = Om_m0 * H0**2 * (1 + z)**3
    rho_r = Om_r0 * H0**2 * (1 + z)**4
    rho_L = Om_L0 * H0**2

    rho = rho_m + rho_r + rho_L
    p = (1/3) * rho_r - rho_L

    dH_dz = (1/(1+z)) * (4*np.pi*(rho + p)/H - (Phi + alpha*H**2)/(2*H))
    dPhi_dz = (1/(1+z)) * (3*Phi - alpha*H**2)

    return [dH_dz, dPhi_dz]

def solve_background(zmax, params, nz=1000):
    H0, Om_m0, Om_r0, Om_L0, alpha, beta = params
    Om_Phi0 = 1.0 - (Om_m0 + Om_r0 + Om_L0)

    y0 = [H0, H0**2 * Om_Phi0]
    z_span = (0.0, zmax)
    z_eval = np.linspace(0.0, zmax, nz)

    sol = solve_ivp(
        lambda z, y: background_odes(z, y, params),
        z_span,
        y0,
        t_eval=z_eval,
        rtol=1e-8,
        atol=1e-10
    )

    return sol.t, sol.y[0], sol.y[1]
