import json
import subprocess
from pathlib import Path

ART = Path("artifacts/dfm_mkc/act_dr6_baseline_lcdm_prediction_vector_source_authenticity_validation_2026_05_25.json")

def test_source_authenticity_validation_verifier_passes():
    result = subprocess.run(
        ["python3", "tools/verify_act_dr6_baseline_lcdm_prediction_vector_source_authenticity_validation.py"],
        check=True,
        text=True,
        capture_output=True,
    )
    assert "ACT_DR6_BASELINE_LCDM_PREDICTION_VECTOR_SOURCE_AUTHENTICITY_VALIDATION_OK" in result.stdout

def test_validation_does_not_promote_baseline_vector():
    data = json.loads(ART.read_text())
    assert data["promotion_decision"] == "DO_NOT_PROMOTE_TO_ACT_DR6_BASELINE_LCDM_PREDICTION_VECTOR"
    assert data["target_missing_object"] == "ACT_DR6_BASELINE_LCDM_PREDICTION_VECTOR"
    assert "ACT_DR6_BASELINE_LCDM_PREDICTION_VECTOR" in data["still_missing_objects_after_this_validation"]

def test_official_theory_provenance_remains_missing():
    data = json.loads(ART.read_text())
    checks = {item["id"]: item["status"] for item in data["source_authenticity_checks"]}
    assert checks["official_baseline_lcdm_theory_provenance"] == "MISSING"
    assert checks["official_act_cobaya_camb_digest_binding"] == "MISSING"
    assert data["minimal_next_object"]["id"] == "OFFICIAL_ACT_DR6_BASELINE_LCDM_THEORY_VECTOR_PROVENANCE_CERTIFICATE"

def test_source_authenticity_status_is_guarded():
    data = json.loads(ART.read_text())
    assert data["status"] in {
        "SOURCE_AUTHENTICITY_REJECTED_DATA_VECTOR_NOT_BASELINE_THEORY",
        "SOURCE_AUTHENTICITY_UNVALIDATED_NO_BASELINE_THEORY_PROVENANCE",
        "SOURCE_AUTHENTICITY_REQUIRES_MANUAL_OFFICIAL_PROVENANCE_REVIEW",
    }
    assert data["authenticity_result"] in {"REJECTED", "UNVALIDATED", "MANUAL_REVIEW_REQUIRED"}

def test_no_empirical_or_physical_claim_is_promoted():
    data = json.loads(ART.read_text())
    assert "baseline LCDM prediction vector exists" in data["does_not_prove"]
    assert "bound candidate is source-authenticated" in data["does_not_prove"]
    assert "DFM-MKC empirical validation" in data["does_not_prove"]
    assert "Lambda-CDM failure" in data["does_not_prove"]
    assert "any Clay problem" in data["does_not_prove"]
