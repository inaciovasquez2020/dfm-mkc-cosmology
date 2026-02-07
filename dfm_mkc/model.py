from dataclasses import dataclass
import numpy as np

@dataclass(frozen=True)
class Parameters:
    H0: float
    Omega_m: float
    Omega_L: float

def init_params(H0: float, Omega_m: float, Omega_L: float) -> Parameters:
    return Parameters(H0=H0, Omega_m=Omega_m, Omega_L=Omega_L)

def evolve_background(params: Parameters, a: np.ndarray) -> np.ndarray:
    H0 = params.H0
    Om = params.Omega_m
    OL = params.Omega_L
    return H0 * np.sqrt(Om * a**(-3) + OL)

def observables(params: Parameters, a: np.ndarray) -> dict:
    H = evolve_background(params, a)
    return {
        "a": a,
        "H": H,
    }

