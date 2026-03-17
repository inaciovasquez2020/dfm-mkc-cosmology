import numpy as np
from src.analysis.fisher_matrix import fisher_matrix

def forecast(loglike,params):

    F = fisher_matrix(loglike,params)

    cov = np.linalg.inv(F)

    sigma = np.sqrt(np.diag(cov))

    return cov,sigma
