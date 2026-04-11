import csv
import math
import numpy as np

from src.models.lcdm import LCDMModel
from src.models.wcdm import wCDMModel
from src.models.curved_lcdm import CurvedLCDM
from src.models.dfm_mkc import DFMMKCModel
from src.likelihood.hubble_likelihood import HubbleLikelihood

z = np.array([0.1, 0.2, 0.3])
Hobs = np.array([69.0, 72.0, 78.0])
err = np.array([3.0, 3.0, 4.0])

def score(name, model, k):
    lik = HubbleLikelihood(Hobs, err)
    theory = lik.theory_prediction(model, z)
    logL = float(lik.loglikelihood(theory))
    n = len(z)
    aic = 2*k - 2*logL
    bic = k*math.log(n) - 2*logL
    return {
        "model": name,
        "logL": f"{logL:.12f}",
        "AIC": f"{aic:.12f}",
        "BIC": f"{bic:.12f}",
        "H0_mean": f"{model.H0:.12f}",
        "Omega_m_mean": f"{model.Om:.12f}",
        "status": "example"
    }

rows = [
    score("LCDM", LCDMModel(), 2),
    score("wCDM", wCDMModel(), 3),
    score("curved_LCDM", CurvedLCDM(), 3),
    score("DFM_MKC", DFMMKCModel(), 3),
]

with open("artifacts/results/model_comparison.csv", "w", newline="") as f:
    w = csv.DictWriter(f, fieldnames=["model","logL","AIC","BIC","H0_mean","Omega_m_mean","status"])
    w.writeheader()
    w.writerows(rows)
