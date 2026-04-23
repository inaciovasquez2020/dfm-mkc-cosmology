from pathlib import Path

def test_real_data_readiness_mentions_export_contract():
    t = Path("docs/REAL_DATA_INTEGRATION_READINESS.md").read_text(encoding="utf-8")
    assert "Closed." in t
    assert "docs/data/DES_Y6_EXPORT_RECIPE.md" in t
    assert "artifacts/data/des_y6_fingerprints.json" in t
