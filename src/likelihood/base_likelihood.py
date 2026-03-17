import numpy as np

class BaseLikelihood:
    """
    Generic likelihood object.
    """

    def __init__(self, data, errors):
        self.data = data
        self.errors = errors

    def chi2(self, theory):
        return np.sum((self.data - theory)**2 / self.errors**2)

    def loglikelihood(self, theory):
        return -0.5 * self.chi2(theory)
