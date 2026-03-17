from src.models.wcdm import wCDMModel
from src.models.curved_lcdm import CurvedLCDM

def test_wcdm():
    m = wCDMModel()
    assert m.E(0) > 0

def test_curved():
    m = CurvedLCDM()
    assert m.E(0) > 0
