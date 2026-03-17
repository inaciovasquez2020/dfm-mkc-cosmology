from src.cosmology.background import BackgroundCosmology

class LCDMModel(BackgroundCosmology):
    """
    Standard Lambda-CDM cosmology.
    """

    def parameters(self):
        return {
            "H0": self.H0,
            "Omega_m": self.Om,
            "Omega_L": self.OL
        }
