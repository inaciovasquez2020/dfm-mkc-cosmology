import numpy as np

class BackgroundCosmology:
    """
    Basic cosmological background expansion model.
    """

    def __init__(self, H0=70.0, Omega_m=0.3, Omega_L=0.7):
        self.H0 = H0
        self.Om = Omega_m
        self.OL = Omega_L

    def E(self, z):
        """
        Dimensionless Hubble parameter.
        """
        return np.sqrt(self.Om*(1+z)**3 + self.OL)

    def H(self, z):
        return self.H0 * self.E(z)
