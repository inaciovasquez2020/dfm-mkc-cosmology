from src.models.lcdm import LCDMModel
from src.likelihood.hubble_likelihood import HubbleLikelihood

def fit_lcdm(z, Hobs, err, H0=70, Om=0.3):
    model = LCDMModel(H0=H0, Omega_m=Om, Omega_L=1-Om)
    lik = HubbleLikelihood(Hobs, err)
    theory = lik.theory_prediction(model, z)
    chi2 = lik.chi2(theory)
    return chi2
