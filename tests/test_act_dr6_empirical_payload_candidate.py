import json
import subprocess
from pathlib import Path

ART = Path("artifacts/dfm_mkc/act_dr6_empirical_payload_candidate_2026_05_25.json")
DOC = Path("docs/status/ACT_DR6_EMPIRICAL_PAYLOAD_CANDIDATE_2026_05_25.md")

def test_act_dr6_empirical_payload_candidate_verifier_passes():
    result = subprocess.run(
        ["python3", "tools/verify_act_dr6_empirical_payload_candidate.py"],
        check=True,
        text=True,
        capture_output=True,
    )
    assert "ACT_DR6_EMPIRICAL_PAYLOAD_CANDIDATE_OK" in result.stdout

def test_act_dr6_candidate_contains_required_source_pointers():
    data = json.loads(ART.read_text())
    pointers = data["source_pointers"]
    assert "https://act.princeton.edu/act-dr6-data-products" in pointers["act_dr6_data_products"]
    assert "lambda.gsfc.nasa.gov" in pointers["nasa_lambda_act_dr6_02"]
    assert "act_dr6_mflike" in pointers["act_dr6_full_likelihood_code"]
    assert "DR6-ACT-lite" in pointers["act_dr6_cmb_only_likelihood_code"]

def test_act_dr6_candidate_has_payload_slots_but_no_data_claim():
    data = json.loads(ART.read_text())
    assert data["status"] == "EMPIRICAL_PAYLOAD_CANDIDATE_ONLY_NO_DATA_IMPORTED"
    assert "data_vector_path" in data["payload_slots_to_fill_later"]
    assert "covariance_matrix_path" in data["payload_slots_to_fill_later"]
    assert "payload_sha256" in data["payload_slots_to_fill_later"]
    assert "ACT DR6 data has been downloaded" in data["does_not_prove"]
    assert "ACT DR6 payload has been verified" in data["does_not_prove"]

def test_act_dr6_candidate_preserves_no_overclaim_boundaries():
    data = json.loads(ART.read_text())
    doc = DOC.read_text()
    assert data["physical_dark_matter_phase_claim_status"] == "HYPOTHESIS_ONLY"
    assert "DFM-MKC empirical validation" in data["does_not_prove"]
    assert "Lambda-CDM failure" in data["does_not_prove"]
    assert "dark matter resolution" in data["does_not_prove"]
    assert "HYPOTHESIS_ONLY" in doc
