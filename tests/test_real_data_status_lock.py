from pathlib import Path

def test_real_data_status_lock():
    t = Path("docs/REAL_DATA_INTEGRATION_READINESS.md").read_text(encoding="utf-8")
    assert "Closed." in t
    assert "DESI DR2, DES Y6, and Planck 2018 are integrated as authentic public data artifacts." in t
    assert "- none" in t
