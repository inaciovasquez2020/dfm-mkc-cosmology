import json
import subprocess
from pathlib import Path

ART = Path("artifacts/dfm_mkc/act_dr6_cmbonly_data_vector_covariance_extraction_2026_05_25.json")

def test_act_dr6_data_vector_covariance_extraction_verifier_passes():
    result = subprocess.run(
        ["python3", "tools/verify_act_dr6_cmbonly_data_vector_covariance_extraction.py"],
        check=True,
        text=True,
        capture_output=True,
    )
    assert "ACT_DR6_CMBONLY_DATA_VECTOR_COVARIANCE_EXTRACTION_VERIFIED" in result.stdout

def test_act_dr6_extraction_identifies_numeric_candidates_without_promotion():
    data = json.loads(ART.read_text())
    assert data["numeric_candidate_count"] >= 1
    assert data["data_vector_status"] == "CANDIDATE_ARRAYS_IDENTIFIED_NOT_PROMOTED"
    assert data["covariance_matrix_status"] == "CANDIDATE_ARRAYS_IDENTIFIED_NOT_PROMOTED"

def test_act_dr6_extraction_blocks_empirical_claims():
    data = json.loads(ART.read_text())
    assert data["status"] == "SCHEMA_LEVEL_EXTRACTION_ONLY_NO_EMPIRICAL_COMPARISON"
    assert data["residual_eigenspace_empirical_run_status"] == "NOT_RUN"
    assert "DFM-MKC empirical validation" in data["does_not_prove"]
    assert "Lambda-CDM failure" in data["does_not_prove"]

def test_phase_claim_boundary_remains_hypothesis_only():
    data = json.loads(ART.read_text())
    assert data["physical_dark_matter_phase_claim_status"] == "HYPOTHESIS_ONLY"
    assert "dark matter is liquid" in data["does_not_prove"]
    assert "dark matter is solid" in data["does_not_prove"]
