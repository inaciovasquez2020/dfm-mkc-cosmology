import json
import subprocess
from pathlib import Path

ART = Path("artifacts/dfm_mkc/act_dr6_official_baseline_lcdm_theory_vector_provenance_certificate_target_2026_05_25.json")

def test_official_baseline_lcdm_provenance_certificate_target_verifier_passes():
    result = subprocess.run(
        ["python3", "tools/verify_act_dr6_official_baseline_lcdm_theory_vector_provenance_certificate_target.py"],
        check=True,
        text=True,
        capture_output=True,
    )
    assert "ACT_DR6_OFFICIAL_BASELINE_LCDM_THEORY_VECTOR_PROVENANCE_CERTIFICATE_TARGET_OK" in result.stdout

def test_provenance_certificate_target_remains_open():
    data = json.loads(ART.read_text())
    assert data["status"] == "PROVENANCE_CERTIFICATE_TARGET_ONLY_OFFICIAL_THEORY_VECTOR_SOURCE_MISSING"
    assert data["object_added"]["status"] == "OPEN_TARGET"
    assert data["target_missing_object"] == "OFFICIAL_ACT_DR6_BASELINE_LCDM_THEORY_VECTOR_PROVENANCE_CERTIFICATE"

def test_required_certificate_fields_are_explicit():
    data = json.loads(ART.read_text())
    fields = {item["id"]: item["status"] for item in data["required_certificate_fields"]}
    for key in [
        "official_likelihood_source",
        "official_parameter_or_bestfit_source",
        "camb_or_cobaya_execution_record",
        "theory_vector_extraction_rule",
        "row_order_binding",
        "shape_digest_certificate",
        "not_observed_data_vector_certificate",
    ]:
        assert fields[key] == "REQUIRED"

def test_baseline_vector_is_not_promoted():
    data = json.loads(ART.read_text())
    assert data["still_missing_objects_after_this_target"] == [
        "OFFICIAL_ACT_DR6_BASELINE_LCDM_THEORY_VECTOR_PROVENANCE_CERTIFICATE",
        "ACT_DR6_BASELINE_LCDM_PREDICTION_VECTOR",
        "ACT_DR6_DFM_MKC_PREDICTION_VECTOR",
    ]
    assert "baseline LCDM prediction vector exists" in data["does_not_prove"]
    assert "official ACT DR6 baseline LCDM theory-vector provenance certificate exists" in data["does_not_prove"]

def test_no_empirical_or_physical_claim_is_promoted():
    data = json.loads(ART.read_text())
    assert "DFM-MKC empirical validation" in data["does_not_prove"]
    assert "Lambda-CDM failure" in data["does_not_prove"]
    assert "dark matter is liquid" in data["does_not_prove"]
    assert "dark matter is solid" in data["does_not_prove"]
    assert "any Clay problem" in data["does_not_prove"]
