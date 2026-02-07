import numpy as np
from .model import Parameters, observables

def gaussian_likelihood(model_values: np.ndarray,
                        data: np.ndarray,
                        sigma: np.ndarray) -> float:
    """
    Standard Gaussian log-likelihood.
    """
    residual = data - model_values
    return -0.5 * np.sum((residual / sigma) ** 2)

def background_likelihood(params: Parameters,
                          a: np.ndarray,
                          data_H: np.ndarray,
                          sigma_H: np.ndarray) -> float:
    """
    Likelihood for background expansion data H(a).
    """
    obs = observables(params, a)
    H_model = obs["H"]
    return gaussian_likelihood(H_model, data_H, sigma_H)

