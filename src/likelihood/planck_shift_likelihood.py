import numpy as np
from src.likelihood.base_likelihood import BaseLikelihood
from src.cosmology.observables.distances import comoving_distance

class PlanckShiftLikelihood(BaseLikelihood):

    def __init__(self,R_obs=1.7499,sigma=0.0088):
        self.R_obs = R_obs
        self.sigma = sigma

    def theory_prediction(self,model,z_star=1089):
        dc = comoving_distance(model,z_star)
        return np.sqrt(model.Om) * dc

    def chi2(self,model):
        R = self.theory_prediction(model)
        return ((R-self.R_obs)/self.sigma)**2
