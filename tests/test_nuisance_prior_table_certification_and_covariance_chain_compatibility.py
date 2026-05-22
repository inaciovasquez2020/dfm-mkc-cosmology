import importlib.util
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
VERIFY = ROOT / "tools/verify_nuisance_prior_table_certification_and_covariance_chain_compatibility.py"
ARTIFACT = ROOT / "artifacts/cosmology/nuisance_prior_table_certification_and_covariance_chain_compatibility_2026_05_22.json"

spec = importlib.util.spec_from_file_location("verify_nuisance_prior_table_certification_and_covariance_chain_compatibility", VERIFY)
module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(module)

def test_verifier_passes():
    module.main()

def test_combined_gate_logic():
    data = json.loads(ARTIFACT.read_text())
    assert data["combined_certification_closed"] == (
        data["nuisance_prior_table_certified"] and data["covariance_chain_compatibility_certified"]
    )

def test_missing_certifications_explicit():
    data = json.loads(ARTIFACT.read_text())
    assert "per-probe nuisance prior table values" in data["missing_certifications"]
    assert "cross-probe covariance compatibility rule" in data["missing_certifications"]

def test_no_overclaim_boundaries():
    data = json.loads(ARTIFACT.read_text())
    assert "executed multiprobe likelihood run" in data["does_not_prove"]
    assert "Lambda-CDM rejection" in data["does_not_prove"]
    assert "DFM-MKC validation" in data["does_not_prove"]
    assert "any Clay problem" in data["does_not_prove"]
