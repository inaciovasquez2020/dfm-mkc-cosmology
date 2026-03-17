import numpy as np
from src.likelihood.base_likelihood import BaseLikelihood

class HubbleLikelihood(BaseLikelihood):

    def theory_prediction(self, model, z):
        return np.array([model.H(zi) for zi in z])
