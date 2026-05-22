import importlib.util
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
VERIFY = ROOT / "tools/verify_act_dr6_full_sacc_schema_validation.py"
ARTIFACT = ROOT / "artifacts/cosmology/act_dr6_full_sacc_schema_validation_2026_05_22.json"

spec = importlib.util.spec_from_file_location("verify_act_dr6_full_sacc_schema_validation", VERIFY)
module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(module)

def test_verifier_passes():
    module.main()

def test_required_checks_present():
    data = json.loads(ARTIFACT.read_text())
    assert set(data["checks"]) == module.REQUIRED_CHECKS

def test_reproducible_payload_preconditions_hold:
    data = json.loads(ARTIFACT.read_text())
    assert data["checks"]["local_payload_exists"] is True
    assert data["checks"]["reproducible_download_sha256_matched"] is True
    assert data["local_sha256"]

def test_certification_equals_full_sacc_pass():
    data = json.loads(ARTIFACT.read_text())
    assert data["certified_for_profiled_likelihood_execution"] == data["full_sacc_schema_validation_passed"]

def test_no_overclaim_boundaries():
    data = json.loads(ARTIFACT.read_text())
    assert "executed multiprobe likelihood run" in data["does_not_prove"]
    assert "Lambda-CDM rejection" in data["does_not_prove"]
    assert "DFM-MKC validation" in data["does_not_prove"]
    assert "any Clay problem" in data["does_not_prove"]
