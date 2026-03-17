import numpy as np
from src.likelihood.base_likelihood import BaseLikelihood
from src.cosmology.observables.distances import luminosity_distance

class SupernovaLikelihood(BaseLikelihood):

    def theory_prediction(self, model, z):
        dL = np.array([luminosity_distance(model, zi) for zi in z])
        return 5 * np.log10(dL) + 25
