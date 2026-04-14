from pathlib import Path

def test_des_y6_terminal_lock():
    t = Path("docs/DES_Y6_TERMINAL_LOCK.md").read_text(encoding="utf-8")
    assert "Conditional." in t
    assert "DESI DR2 real chains are imported and locked." in t
    assert "Planck 2018 baseline parameters are imported and locked." in t
    assert "The repository main branch is synchronized after PR #43." in t
    assert "- public_data/des_y6/y6_3x2pt_summary.csv" in t
    assert "- public_data/des_y6/y6_covariance.csv" in t
    assert "The repository cannot truthfully claim three-anchor real-data closure until the two DES Y6 placeholder files are replaced by authentic public data files." in t
    assert "- direct public URL for y6_3x2pt_summary.csv" in t
    assert "- direct public URL for y6_covariance.csv" in t
