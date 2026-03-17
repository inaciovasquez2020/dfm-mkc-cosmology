from src.cosmology.background import BackgroundCosmology

def test_hubble():
    c = BackgroundCosmology()
    assert c.H(0) > 0
