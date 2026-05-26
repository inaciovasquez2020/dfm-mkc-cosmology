import json
import subprocess
from pathlib import Path

ART = Path("artifacts/dfm_mkc/act_dr6_prediction_vector_ordering_certificate_2026_05_25.json")

def test_act_dr6_prediction_vector_ordering_certificate_verifier_passes():
    result = subprocess.run(
        ["python3", "tools/verify_act_dr6_prediction_vector_ordering_certificate.py"],
        check=True,
        text=True,
        capture_output=True,
    )
    assert "ACT_DR6_PREDICTION_VECTOR_ORDERING_CERTIFICATE_OK" in result.stdout

def test_ordering_certificate_closes_only_ordering_object():
    data = json.loads(ART.read_text())
    assert data["closes_missing_object"] == "ACT_DR6_PREDICTION_VECTOR_ORDERING_CERTIFICATE"
    assert data["status"] == "ORDERING_CERTIFICATE_FOR_EXTRACTED_DATA_VECTOR_ONLY_PREDICTIONS_STILL_MISSING"
    assert data["still_missing_objects_after_this_certificate"] == [
        "ACT_DR6_BASELINE_LCDM_PREDICTION_VECTOR",
        "ACT_DR6_DFM_MKC_PREDICTION_VECTOR",
    ]

def test_ordering_rule_requires_same_prediction_shape():
    data = json.loads(ART.read_text())
    assert data["ordering_rule"]["type"] == "frozen_row_index_order"
    assert data["ordering_rule"]["required_prediction_vector_shape"] == data["data_vector"]["shape"]
    assert len(data["data_vector"]["shape"]) == 1
    assert data["covariance"]["shape"] == [
        data["data_vector"]["shape"][0],
        data["data_vector"]["shape"][0],
    ]

def test_no_empirical_or_physical_claim_is_promoted():
    data = json.loads(ART.read_text())
    assert data["physical_dark_matter_phase_claim_status"] == "HYPOTHESIS_ONLY"
    assert "DFM-MKC empirical validation" in data["does_not_prove"]
    assert "Lambda-CDM failure" in data["does_not_prove"]
    assert "dark matter is liquid" in data["does_not_prove"]
    assert "dark matter is solid" in data["does_not_prove"]
    assert "any Clay problem" in data["does_not_prove"]
