import numpy as np
from scipy.integrate import quad

c = 299792.458

def comoving_distance(model, z):
    """
    Line-of-sight comoving distance
    """
    integrand = lambda zp: 1.0 / model.H(zp)
    integral, _ = quad(integrand, 0, z)
    return c * integral

def luminosity_distance(model, z):
    """
    Luminosity distance
    """
    return (1 + z) * comoving_distance(model, z)

def angular_diameter_distance(model, z):
    """
    Angular diameter distance
    """
    return comoving_distance(model, z) / (1 + z)
