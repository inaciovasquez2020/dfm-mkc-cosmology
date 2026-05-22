import importlib.util
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
VERIFY = ROOT / "tools/verify_act_dr6_sacc_reader_and_independent_release_hash_validation.py"
ARTIFACT = ROOT / "artifacts/cosmology/act_dr6_sacc_reader_and_independent_release_hash_validation_2026_05_22.json"

spec = importlib.util.spec_from_file_location("verify_act_dr6_sacc_reader_and_independent_release_hash_validation", VERIFY)
module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(module)

def test_verifier_passes():
    module.main()

def test_local_fits_header_probe_runs():
    data = json.loads(ARTIFACT.read_text())
    assert data["reader"]["executes_on_local_payload"] is True
    assert data["reader"]["fits_header_observed"] is True
    assert data["local_payload"]["local_sha256"]

def test_independent_release_hash_is_not_claimed():
    data = json.loads(ARTIFACT.read_text())
    assert data["independent_release_validation"]["external_release_digest"] is None
    assert data["independent_release_validation"]["independent_hash_match_verified"] is False
    assert data["independent_release_validation"]["release_provenance_certified"] is False

def test_not_certified_for_likelihood_execution():
    data = json.loads(ARTIFACT.read_text())
    assert data["reader"]["full_sacc_schema_validation_passed"] is False
    assert data["certified_for_profiled_likelihood_execution"] is False

def test_no_overclaim_boundaries():
    data = json.loads(ARTIFACT.read_text())
    assert "ACT DR6 independent source certification" in data["does_not_prove"]
    assert "Lambda-CDM rejection" in data["does_not_prove"]
    assert "DFM-MKC validation" in data["does_not_prove"]
    assert "any Clay problem" in data["does_not_prove"]
