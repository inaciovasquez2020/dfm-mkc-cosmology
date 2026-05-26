import json
import subprocess
from pathlib import Path

ART = Path("artifacts/dfm_mkc/act_dr6_prediction_vector_missing_object_target_2026_05_25.json")

def test_act_dr6_prediction_vector_missing_object_target_verifier_passes():
    result = subprocess.run(
        ["python3", "tools/verify_act_dr6_prediction_vector_missing_object_target.py"],
        check=True,
        text=True,
        capture_output=True,
    )
    assert "ACT_DR6_PREDICTION_VECTOR_MISSING_OBJECT_TARGET_OK" in result.stdout

def test_prediction_vector_missing_objects_are_explicit():
    data = json.loads(ART.read_text())
    missing = {item["id"]: item["status"] for item in data["required_missing_objects"]}
    assert missing["ACT_DR6_BASELINE_LCDM_PREDICTION_VECTOR"] == "MISSING"
    assert missing["ACT_DR6_DFM_MKC_PREDICTION_VECTOR"] == "MISSING"
    assert missing["ACT_DR6_PREDICTION_VECTOR_ORDERING_CERTIFICATE"] == "MISSING"

def test_residual_comparison_remains_blocked():
    data = json.loads(ART.read_text())
    assert data["status"] == "MISSING_PREDICTION_VECTOR_TARGET_ONLY_NO_MODEL_COMPARISON"
    assert "ACT DR6 residual eigenspace empirical comparison" in data["blocked_until_missing_objects_exist"]
    assert "DFM-MKC empirical validation" in data["does_not_prove"]
    assert "Lambda-CDM failure" in data["does_not_prove"]

def test_phase_claim_boundary_remains_hypothesis_only():
    data = json.loads(ART.read_text())
    assert data["physical_dark_matter_phase_claim_status"] == "HYPOTHESIS_ONLY"
    assert "dark matter is liquid" in data["does_not_prove"]
    assert "dark matter is solid" in data["does_not_prove"]
