import numpy as np
import pandas as pd

def chi2_bao(csv_path, model_fn=None, theta=None, z_col="z", obs_col="obs", sigma_col="sigma"):
    df = pd.read_csv(csv_path)
    z = df[z_col].to_numpy(dtype=float)
    obs = df[obs_col].to_numpy(dtype=float)
    sig = df[sigma_col].to_numpy(dtype=float)
    if model_fn is None:
        raise ValueError("model_fn is required")
    pred = model_fn(z, theta)
    r = (obs - pred) / sig
    return float(np.sum(r*r))
