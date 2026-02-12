import numpy as np

def chi2(data, model, cov):
    r = data - model
    return r.T @ np.linalg.inv(cov) @ r

def loglike(data, model, cov):
    return -0.5 * chi2(data, model, cov)
