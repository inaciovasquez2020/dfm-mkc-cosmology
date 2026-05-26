import json
import subprocess
from pathlib import Path

ART = Path("artifacts/dfm_mkc/act_dr6_baseline_lcdm_prediction_vector_candidate_probe_2026_05_25.json")
RESULT = Path("artifacts/dfm_mkc/act_dr6_baseline_lcdm_prediction_vector_candidate_probe_result.json")

def test_baseline_lcdm_prediction_vector_candidate_probe_verifier_passes():
    result = subprocess.run(
        ["python3", "tools/verify_act_dr6_baseline_lcdm_prediction_vector_candidate_probe.py"],
        check=True,
        text=True,
        capture_output=True,
    )
    assert "ACT_DR6_BASELINE_LCDM_PREDICTION_VECTOR_CANDIDATE_PROBE_OK" in result.stdout

def test_probe_result_is_recorded_without_promotion():
    data = json.loads(ART.read_text())
    result = json.loads(RESULT.read_text())
    assert data["status"] == "CANDIDATE_PROBE_ONLY_BASELINE_VECTOR_NOT_PROMOTED"
    assert data["probe_result_status"] == result["status"]
    assert data["matching_candidate_count"] == result["matching_candidate_count"]

def test_probe_keeps_baseline_vector_missing():
    data = json.loads(ART.read_text())
    assert data["still_missing_objects_after_this_probe"] == [
        "ACT_DR6_BASELINE_LCDM_PREDICTION_VECTOR",
        "ACT_DR6_DFM_MKC_PREDICTION_VECTOR",
    ]
    assert "baseline LCDM prediction vector exists" in data["does_not_prove"]

def test_probe_script_can_execute():
    result = subprocess.run(
        ["python3", "tools/probe_act_dr6_baseline_lcdm_prediction_vector_candidates.py"],
        check=True,
        text=True,
        capture_output=True,
    )
    assert "WROTE artifacts/dfm_mkc/act_dr6_baseline_lcdm_prediction_vector_candidate_probe_result.json" in result.stdout

def test_no_empirical_or_physical_claim_is_promoted():
    data = json.loads(ART.read_text())
    assert "DFM-MKC empirical validation" in data["does_not_prove"]
    assert "Lambda-CDM failure" in data["does_not_prove"]
    assert "dark matter is liquid" in data["does_not_prove"]
    assert "dark matter is solid" in data["does_not_prove"]
    assert "any Clay problem" in data["does_not_prove"]
