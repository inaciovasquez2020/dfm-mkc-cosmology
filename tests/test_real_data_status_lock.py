from pathlib import Path

def test_real_data_status_lock():
    t = Path("docs/REAL_DATA_INTEGRATION_READINESS.md").read_text(encoding="utf-8")
    assert "Conditional." in t
    assert "DESI DR2 and Planck 2018 are integrated as authentic public data artifacts." in t
    assert "Repository closure on the declared three-anchor real-data surface remains open until the two DES Y6 placeholder files are replaced by authentic public data." in t
    assert "- y6_3x2pt_summary.csv" in t
    assert "- y6_covariance.csv" in t
