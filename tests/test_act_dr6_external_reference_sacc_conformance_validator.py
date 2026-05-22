import importlib.util
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
VERIFY = ROOT / "tools/verify_act_dr6_external_reference_sacc_conformance_validator.py"
ARTIFACT = ROOT / "artifacts/cosmology/act_dr6_external_reference_sacc_conformance_validator_2026_05_22.json"

spec = importlib.util.spec_from_file_location("verify_act_dr6_external_reference_sacc_conformance_validator", VERIFY)
module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(module)

def test_verifier_passes():
    module.main()

def test_official_references_bound():
    data = json.loads(ARTIFACT.read_text())
    assert "act_dr6_data_products" in data["official_external_references"]
    assert "act_dr6_lite_repository" in data["official_external_references"]

def test_external_digest_not_overclaimed():
    data = json.loads(ARTIFACT.read_text())
    assert data["external_digest"] is None
    assert data["external_digest_supplied"] is False
    assert data["external_digest_matches_local_payload"] is False

def test_partial_validator_not_certification():
    data = json.loads(ARTIFACT.read_text())
    checks = data["sacc_conformance_validator"]["checks"]
    assert checks["fits_payload_opens"] is True
    assert checks["required_hdus_present"] is True
    assert data["sacc_conformance_validator"]["full_sacc_schema_conformance_established"] is False
    assert data["certified_for_profiled_likelihood_execution"] is False

def test_no_overclaim_boundaries:
    data = json.loads(ARTIFACT.read_text())
    assert "ACT DR6 public release digest certification" in data["does_not_prove"]
    assert "ACT DR6 full SACC schema certification" in data["does_not_prove"]
    assert "Lambda-CDM rejection" in data["does_not_prove"]
    assert "DFM-MKC validation" in data["does_not_prove"]
    assert "any Clay problem" in data["does_not_prove"]
