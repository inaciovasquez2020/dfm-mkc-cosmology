import json
import subprocess
from pathlib import Path

ART = Path("artifacts/dfm_mkc/act_dr6_baseline_lcdm_row_mapping_failure_analysis_2026_05_25.json")

def test_row_mapping_failure_analysis_verifier_passes():
    result = subprocess.run(
        ["python3", "tools/verify_act_dr6_baseline_lcdm_row_mapping_failure_analysis.py"],
        check=True,
        text=True,
        capture_output=True,
    )
    assert "ACT_DR6_BASELINE_LCDM_ROW_MAPPING_FAILURE_ANALYSIS_OK" in result.stdout

def test_failure_analysis_status_is_guarded():
    data = json.loads(ART.read_text())
    assert data["status"] in {
        "ROW_MAPPING_FAILURE_ANALYSIS_BLOCKED_SACC_METADATA_UNAVAILABLE",
        "ROW_MAPPING_FAILURE_ANALYSIS_BLOCKED_ROW_COUNT_MISMATCH",
        "ROW_MAPPING_FAILURE_ANALYSIS_BLOCKED_INCOMPLETE_SACC_ROW_METADATA",
        "ROW_MAPPING_FAILURE_ANALYSIS_LOCAL_SACC_METADATA_SUFFICIENT_MAPPING_ALGORITHM_STILL_OPEN",
    }

def test_minimal_next_object_is_binding_rule():
    data = json.loads(ART.read_text())
    assert data["minimal_next_object"]["id"] == "ACT_DR6_BASELINE_LCDM_SACC_TO_BEST_FIT_LABEL_BINDING_RULE"
    assert data["minimal_next_object"]["status"] == "MISSING"
    assert data["allowed_next_status_after_binding_rule"] == "ROW_MAPPING_BINDING_RULE_READY_FOR_MAPPING_CONSTRUCTION"

def test_mapping_and_baseline_vector_remain_missing():
    data = json.loads(ART.read_text())
    assert data["still_missing_objects_after_this_analysis"] == [
        "ACT_DR6_BASELINE_LCDM_OFFICIAL_BEST_FIT_VECTOR_ROW_ORDER_MAPPING",
        "ACT_DR6_BASELINE_LCDM_PREDICTION_VECTOR",
        "ACT_DR6_DFM_MKC_PREDICTION_VECTOR",
    ]
    assert "official best-fit row-order mapping exists" in data["does_not_prove"]
    assert "baseline LCDM prediction vector exists" in data["does_not_prove"]

def test_no_empirical_or_physical_claim_is_promoted():
    data = json.loads(ART.read_text())
    assert "DFM-MKC empirical validation" in data["does_not_prove"]
    assert "Lambda-CDM failure" in data["does_not_prove"]
    assert "dark matter is liquid" in data["does_not_prove"]
    assert "dark matter is solid" in data["does_not_prove"]
    assert "any Clay problem" in data["does_not_prove"]
