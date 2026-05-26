import json
import subprocess
from pathlib import Path

ART = Path("artifacts/dfm_mkc/act_dr6_baseline_lcdm_official_best_fit_mapping_extraction_trial_2026_05_25.json")

def test_mapping_extraction_trial_verifier_passes():
    result = subprocess.run(
        ["python3", "tools/verify_act_dr6_baseline_lcdm_official_best_fit_mapping_extraction_trial.py"],
        check=True,
        text=True,
        capture_output=True,
    )
    assert "ACT_DR6_BASELINE_LCDM_OFFICIAL_BEST_FIT_MAPPING_EXTRACTION_TRIAL_OK" in result.stdout

def test_official_best_fit_tarball_is_supplied_and_digest_bound():
    data = json.loads(ART.read_text())
    official = data["official_best_fit_spectra_file"]
    assert official["bytes"] > 0
    assert len(official["sha256"]) == 64
    assert official["url"].endswith("act_dr6.02_best_fits_dr6_lcdm.tar.gz")

def test_row_metadata_mapping_and_audit_artifacts_exist():
    data = json.loads(ART.read_text())
    manifest = Path(data["payload_manifest"])
    assert manifest.exists()
    payload = json.loads(manifest.read_text())
    assert payload["status"] == "PAYLOAD_MANIFEST_ONLY_LARGE_FILES_NOT_COMMITTED"
    assert payload["file_count"] > 0

def test_prediction_vector_is_not_promoted():
    data = json.loads(ART.read_text())
    assert data["promotion_decision"] == "DO_NOT_PROMOTE_TO_ACT_DR6_BASELINE_LCDM_PREDICTION_VECTOR"
    assert data["still_missing_objects_after_this_trial"] == [
        "ACT_DR6_BASELINE_LCDM_PREDICTION_VECTOR",
        "ACT_DR6_DFM_MKC_PREDICTION_VECTOR",
    ]

def test_status_is_guarded():
    data = json.loads(ART.read_text())
    assert data["status"] in {
        "OFFICIAL_BEST_FIT_MAPPING_EXTRACTION_TRIAL_BLOCKED_NO_CERTIFIED_ROW_MAPPING",
        "OFFICIAL_BEST_FIT_MAPPING_EXTRACTION_TRIAL_RAN_VECTOR_CANDIDATE_NOT_PROMOTED",
        "OFFICIAL_BEST_FIT_MAPPING_EXTRACTION_TRIAL_MANIFEST_ONLY_BLOCKED_NO_CERTIFIED_ROW_MAPPING",
    }

def test_no_empirical_or_physical_claim_is_promoted():
    data = json.loads(ART.read_text())
    assert "baseline LCDM prediction vector exists" in data["does_not_prove"]
    assert "baseline LCDM prediction vector is fully row-audited" in data["does_not_prove"]
    assert "DFM-MKC empirical validation" in data["does_not_prove"]
    assert "Lambda-CDM failure" in data["does_not_prove"]
    assert "any Clay problem" in data["does_not_prove"]
