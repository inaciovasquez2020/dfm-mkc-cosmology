import numpy as np
from src.models.lcdm import LCDMModel
from src.likelihood.hubble_likelihood import HubbleLikelihood

z = np.array([0.1,0.2,0.3])
Hobs = np.array([69,72,78])
err = np.array([3,3,4])

model = LCDMModel()

lik = HubbleLikelihood(Hobs, err)

theory = lik.theory_prediction(model, z)

print("logL:", lik.loglikelihood(theory))
