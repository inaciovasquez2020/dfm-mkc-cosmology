from src.cosmology.background import BackgroundCosmology
import numpy as np

class wCDMModel(BackgroundCosmology):

    def __init__(self,H0=70,Omega_m=0.3,Omega_L=0.7,w=-1):
        super().__init__(H0,Omega_m,Omega_L)
        self.w = w

    def E(self,z):
        return np.sqrt(
            self.Om*(1+z)**3 +
            self.OL*(1+z)**(3*(1+self.w))
        )
