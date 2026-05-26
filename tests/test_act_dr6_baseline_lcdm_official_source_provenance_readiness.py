import json
import subprocess
from pathlib import Path

ART = Path("artifacts/dfm_mkc/act_dr6_baseline_lcdm_official_source_provenance_readiness_2026_05_25.json")

def test_official_source_provenance_readiness_verifier_passes():
    result = subprocess.run(
        ["python3", "tools/verify_act_dr6_baseline_lcdm_official_source_provenance_readiness.py"],
        check=True,
        text=True,
        capture_output=True,
    )
    assert "ACT_DR6_BASELINE_LCDM_OFFICIAL_SOURCE_PROVENANCE_READINESS_OK" in result.stdout

def test_official_sources_are_digest_bound():
    data = json.loads(ART.read_text())
    sources = data["official_sources"]
    for key in [
        "NASA_LAMBDA_ACT_DR6_02_PSPIPE_BEST_FITS_INFO",
        "NASA_LAMBDA_ACT_DR6_02_PSPIPE_BEST_FITS_DOWNLOADS",
        "NASA_LAMBDA_ACT_DR6_02_CHAINS_INFO",
    ]:
        assert sources[key]["bytes"] > 0
        assert len(sources[key]["sha256"]) == 64
    assert sources["ACT_DR6_PARAMETERS_REPOSITORY"]["head_commit"]

def test_promotes_only_to_extraction_readiness():
    data = json.loads(ART.read_text())
    assert data["status"] == "BASELINE_LCDM_PROVENANCE_CERTIFIED_VECTOR_EXTRACTION_READY_NO_VECTOR_PROMOTION"
    assert data["promotion"]["to"] == "BASELINE_LCDM_PROVENANCE_CERTIFIED_VECTOR_EXTRACTION_READY"
    assert data["promotion"]["explicitly_not_promoted_to"] == "ACT_DR6_BASELINE_LCDM_PREDICTION_VECTOR"

def test_row_order_binding_is_ready_not_applied_to_vector():
    data = json.loads(ART.read_text())
    assert data["row_order_binding_against_act_dr6_ordering"]["status"] == "EXTRACTION_RULE_READY_BINDING_NOT_YET_APPLIED_TO_VECTOR"
    assert "ACT_DR6_BASELINE_LCDM_PREDICTION_VECTOR" in data["still_missing_objects_after_this_record"]

def test_not_observed_data_vector_source_class_is_certified():
    data = json.loads(ART.read_text())
    assert data["not_observed_data_vector_certificate"]["status"] == "SOURCE_CLASS_SEPARATION_CERTIFIED_FOR_OFFICIAL_SOURCE"
    assert data["digest_bound_execution_record"]["boltzmann_code"] == "CAMB"
    assert data["digest_bound_execution_record"]["camb_version_from_official_source"] == "1.5.9"

def test_no_empirical_or_physical_claim_is_promoted():
    data = json.loads(ART.read_text())
    assert "baseline LCDM prediction vector exists" in data["does_not_prove"]
    assert "baseline LCDM prediction vector is row-aligned" in data["does_not_prove"]
    assert "DFM-MKC empirical validation" in data["does_not_prove"]
    assert "Lambda-CDM failure" in data["does_not_prove"]
    assert "any Clay problem" in data["does_not_prove"]
