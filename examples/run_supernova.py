import numpy as np
from src.models.lcdm import LCDMModel
from src.likelihood.supernova_likelihood import SupernovaLikelihood

z = np.array([0.1,0.2,0.3])
mu_obs = np.array([38.2,39.5,40.6])
err = np.array([0.2,0.2,0.3])

model = LCDMModel()

lik = SupernovaLikelihood(mu_obs, err)
theory = lik.theory_prediction(model, z)

print("logL:", lik.loglikelihood(theory))
