from src.cosmology.background import BackgroundCosmology
import numpy as np

class CurvedLCDM(BackgroundCosmology):

    def __init__(self,H0=70,Omega_m=0.3,Omega_L=0.65,Omega_k=0.05):
        super().__init__(H0,Omega_m,Omega_L)
        self.Ok = Omega_k

    def E(self,z):
        return np.sqrt(
            self.Om*(1+z)**3 +
            self.Ok*(1+z)**2 +
            self.OL
        )
