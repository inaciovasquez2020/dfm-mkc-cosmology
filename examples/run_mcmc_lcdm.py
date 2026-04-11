import numpy as np
from dfm_mkc.models.lcdm import LCDMModel
from dfm_mkc.likelihood.hubble_likelihood import HubbleLikelihood
from dfm_mkc.inference.mcmc import SimpleMCMC

z = np.array([0.1,0.2,0.3])
Hobs = np.array([69,72,78])
err = np.array([3,3,4])

def loglike(params):
    H0, Om = params
    model = LCDMModel(H0=H0, Omega_m=Om, Omega_L=1-Om)
    lik = HubbleLikelihood(Hobs, err)
    theory = lik.theory_prediction(model, z)
    return lik.loglikelihood(theory)

sampler = SimpleMCMC(loglike, [70,0.3], [1.0,0.02])

chain = sampler.sample(500)

print("Mean parameters:", chain.mean(axis=0))
