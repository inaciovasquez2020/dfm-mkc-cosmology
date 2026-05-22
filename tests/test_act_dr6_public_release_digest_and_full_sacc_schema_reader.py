import importlib.util
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
VERIFY = ROOT / "tools/verify_act_dr6_public_release_digest_and_full_sacc_schema_reader.py"
ARTIFACT = ROOT / "artifacts/cosmology/act_dr6_public_release_digest_and_full_sacc_schema_reader_2026_05_22.json"

spec = importlib.util.spec_from_file_location("verify_act_dr6_public_release_digest_and_full_sacc_schema_reader", VERIFY)
module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(module)

def test_verifier_passes():
    module.main()

def test_local_fits_header_enumerator_runs():
    data = json.loads(ARTIFACT.read_text())
    assert data["local_payload"]["exists"] is True
    assert data["local_payload"]["sha256"]
    assert data["local_payload"]["fits_hdu_headers_observed"] >= 1
    assert data["reader"]["executes_on_local_payload"] is True

def test_public_digest_not_claimed():
    data = json.loads(ARTIFACT.read_text())
    assert data["public_release_digest"]["external_release_digest"] is None
    assert data["public_release_digest"]["independent_hash_match_verified"] is False
    assert data["public_release_digest"]["release_provenance_certified"] is False

def test_full_sacc_schema_not_claimed():
    data = json.loads(ARTIFACT.read_text())
    assert data["reader"]["full_sacc_schema_reader_implemented"] is False
    assert data["reader"]["full_sacc_schema_validation_passed"] is False
    assert data["certified_for_profiled_likelihood_execution"] is False

def test_no_overclaim_boundaries():
    data = json.loads(ARTIFACT.read_text())
    assert "ACT DR6 public release digest certification" in data["does_not_prove"]
    assert "ACT DR6 full SACC schema certification" in data["does_not_prove"]
    assert "Lambda-CDM rejection" in data["does_not_prove"]
    assert "DFM-MKC validation" in data["does_not_prove"]
    assert "any Clay problem" in data["does_not_prove"]
