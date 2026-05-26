import json
import subprocess
from pathlib import Path

ART = Path("artifacts/dfm_mkc/act_dr6_baseline_lcdm_prediction_vector_execution_gate_2026_05_25.json")
ORDER = Path("artifacts/dfm_mkc/act_dr6_prediction_vector_ordering_certificate_2026_05_25.json")

def test_baseline_lcdm_prediction_vector_execution_gate_verifier_passes():
    result = subprocess.run(
        ["python3", "tools/verify_act_dr6_baseline_lcdm_prediction_vector_execution_gate.py"],
        check=True,
        text=True,
        capture_output=True,
    )
    assert "ACT_DR6_BASELINE_LCDM_PREDICTION_VECTOR_EXECUTION_GATE_OK" in result.stdout

def test_gate_blocks_without_trusted_baseline_source():
    data = json.loads(ART.read_text())
    assert data["status"] == "BASELINE_LCDM_PREDICTION_VECTOR_EXECUTION_BLOCKED_SOURCE_MISSING"
    assert data["execution_result"] == "NOT_EXECUTED"
    assert data["minimal_missing_input"]["id"] == "TRUSTED_ACT_DR6_BASELINE_LCDM_THEORY_VECTOR_SOURCE"
    assert data["minimal_missing_input"]["status"] == "MISSING"

def test_required_prediction_shape_matches_ordering_certificate():
    data = json.loads(ART.read_text())
    order = json.loads(ORDER.read_text())
    assert data["required_prediction_vector_shape"] == order["ordering_rule"]["required_prediction_vector_shape"]

def test_no_prediction_or_empirical_claim_is_promoted():
    data = json.loads(ART.read_text())
    assert data["still_missing_objects_after_this_gate"] == [
        "ACT_DR6_BASELINE_LCDM_PREDICTION_VECTOR",
        "ACT_DR6_DFM_MKC_PREDICTION_VECTOR",
    ]
    assert "baseline LCDM prediction vector exists" in data["does_not_prove"]
    assert "trusted baseline LCDM theory source exists" in data["does_not_prove"]
    assert "DFM-MKC empirical validation" in data["does_not_prove"]
    assert "Lambda-CDM failure" in data["does_not_prove"]
    assert "any Clay problem" in data["does_not_prove"]
