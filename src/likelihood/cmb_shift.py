import numpy as np
from src.likelihood.base_likelihood import BaseLikelihood
from src.cosmology.observables.distances import comoving_distance

class CMBShiftLikelihood(BaseLikelihood):

    def theory_prediction(self,model,z_star):
        dc = comoving_distance(model,z_star)
        return np.sqrt(model.Om) * dc
