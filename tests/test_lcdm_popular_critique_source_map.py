import importlib.util
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
VERIFY = ROOT / "tools/verify_lcdm_popular_critique_source_map.py"
ARTIFACT = ROOT / "artifacts/cosmology/lcdm_popular_critique_source_map_2026_05_22.json"

spec = importlib.util.spec_from_file_location("verify_lcdm_popular_critique_source_map", VERIFY)
module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(module)

def test_verifier_passes():
    module.main()

def test_medium_source_registered_as_popular_critique_only():
    data = json.loads(ARTIFACT.read_text())
    source = data["sources"][0]
    assert source["id"] == "KRIGER_2026_BANKRUPT_COSMOLOGY_MEDIUM"
    assert source["claim_class"] == "POPULAR_POLEMICAL_CRITIQUE_ONLY"
    assert "peer-reviewed empirical evidence" in source["not_usable_for"]

def test_no_lcdm_rejection_claim():
    data = json.loads(ARTIFACT.read_text())
    assert data["status"] == "POPULAR_CRITIQUE_SOURCE_ONLY_NO_LCDM_REJECTION"
    assert "Lambda-CDM failure" in data["does_not_prove"]
    assert "six-parameter flat Lambda-CDM rejection" in data["does_not_prove"]
    assert "DFM-MKC validation" in data["does_not_prove"]
    assert "any Clay problem" in data["does_not_prove"]
