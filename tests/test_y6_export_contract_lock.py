from pathlib import Path

def test_y6_export_contract_lock():
    t = Path("docs/Y6_EXPORT_CONTRACT_LOCK.md").read_text(encoding="utf-8")
    assert "Conditional." in t
    assert "The repository no longer requires that the two remaining DES Y6 objects be obtained only via fixed direct-download CSV URLs." in t
    assert "- public_data/des_y6/y6_3x2pt_summary.csv" in t
    assert "- public_data/des_y6/y6_covariance.csv" in t
    assert "The source surface is official for DES Y6 public data access." in t
    assert "The export recipe is reproducible." in t
    assert "The resulting files contain no SYNTHETIC_PLACEHOLDER marker." in t

def test_real_data_readiness_mentions_export_contract():
    t = Path("docs/REAL_DATA_INTEGRATION_READINESS.md").read_text(encoding="utf-8")
    assert "Conditional." in t
    assert "Repository closure on the declared three-anchor real-data surface remains open until the two DES Y6 canonical files are replaced by authentic public data." in t
    assert "Direct fixed CSV URLs are not required; a reproducible official export recipe from an official DES Y6 public access surface is admissible." in t
