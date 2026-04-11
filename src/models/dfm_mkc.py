import numpy as np
from src.cosmology.background import BackgroundCosmology

class DFMMKCModel(BackgroundCosmology):
    def __init__(self, H0=70.0, Omega_m=0.3, Omega_L=0.7, xi=0.0):
        super().__init__(H0, Omega_m, Omega_L)
        self.xi = xi

    def E(self, z):
        return np.sqrt(self.Om*(1+z)**3 + self.OL + self.xi*z*(1+z))
