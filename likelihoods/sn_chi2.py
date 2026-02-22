import numpy as np
import pandas as pd

def mu_from_dL(dL):
    return 5.0 * np.log10(dL) 

def chi2_sn(csv_path, z_col="z", mu_col="mu", sigma_col="sigma", dL_fn=None, theta=None, M=0.0):
    df = pd.read_csv(csv_path)
    z = df[z_col].to_numpy(dtype=float)
    mu_obs = df[mu_col].to_numpy(dtype=float)
    sig = df[sigma_col].to_numpy(dtype=float)
    if dL_fn is None:
        raise ValueError("dL_fn is required")
    dL = dL_fn(z, theta)
    mu_model = mu_from_dL(dL) + M
    r = (mu_obs - mu_model) / sig
    return float(np.sum(r*r))

def bestfit_M(csv_path, z_col="z", mu_col="mu", sigma_col="sigma", dL_fn=None, theta=None):
    df = pd.read_csv(csv_path)
    z = df[z_col].to_numpy(dtype=float)
    mu_obs = df[mu_col].to_numpy(dtype=float)
    sig = df[sigma_col].to_numpy(dtype=float)
    dL = dL_fn(z, theta)
    base = mu_from_dL(dL)
    w = 1.0 / (sig*sig)
    M = np.sum(w * (mu_obs - base)) / np.sum(w)
    return float(M)
