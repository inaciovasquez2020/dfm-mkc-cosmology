from src.models.lcdm import LCDMModel
from src.cosmology.observables.distances import luminosity_distance

def test_distance():
    m = LCDMModel()
    assert luminosity_distance(m, 0.1) > 0
