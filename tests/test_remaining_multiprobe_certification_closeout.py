import importlib.util
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
VERIFY = ROOT / "tools/verify_remaining_multiprobe_certification_closeout.py"
ACT = ROOT / "artifacts/cosmology/act_dr6_external_digest_or_reproducible_download_lock_2026_05_22.json"
ALL = ROOT / "artifacts/cosmology/remaining_multiprobe_certification_closeout_2026_05_22.json"

spec = importlib.util.spec_from_file_location("verify_remaining_multiprobe_certification_closeout", VERIFY)
module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(module)

def test_verifier_passes():
    module.main()

def test_act_digest_lock_does_not_certify():
    data = json.loads(ACT.read_text())
    assert data["external_digest_supplied"] is False
    assert data["reproducible_download_command_supplied"] is False
    assert data["download_reproduces_local_sha256"] is False
    assert data["act_dr6_certified_for_profiled_likelihood_execution"] is False

def test_remaining_objects_are_complete_for_closeout():
    data = json.loads(ALL.read_text())
    assert set(data["remaining_objects"]) == module.REQUIRED_REMAINING
    assert data["terminal_for_today"] is True

def test_no_empirical_or_mathematical_claim():
    data = json.loads(ALL.read_text())
    assert data["proof_status"]["mathematical_proof"] is False
    assert data["proof_status"]["mathematical_disproof"] is False
    assert data["proof_status"]["empirical_validation"] is False
    assert data["proof_status"]["lambda_cdm_rejection"] is False
    assert data["proof_status"]["dfm_mkc_validation"] is False

def test_no_overclaim_boundaries():
    data = json.loads(ALL.read_text())
    assert "Lambda-CDM rejection" in data["does_not_prove"]
    assert "DFM-MKC validation" in data["does_not_prove"]
    assert "any Clay problem" in data["does_not_prove"]
