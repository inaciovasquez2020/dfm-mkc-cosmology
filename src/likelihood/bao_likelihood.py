import numpy as np
from src.likelihood.base_likelihood import BaseLikelihood
from src.cosmology.observables.distances import comoving_distance

class BAOLikelihood(BaseLikelihood):

    def theory_prediction(self,model,z):
        return np.array([comoving_distance(model,zi) for zi in z])
