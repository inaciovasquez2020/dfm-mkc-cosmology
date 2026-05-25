import json
import subprocess
from pathlib import Path

ART = Path("artifacts/dfm_mkc/residual_eigenspace_empirical_payload_intake_target_2026_05_25.json")
DOC = Path("docs/status/RESIDUAL_EIGENSPACE_EMPIRICAL_PAYLOAD_INTAKE_TARGET_2026_05_25.md")

def test_residual_eigenspace_empirical_payload_intake_target_verifier_passes():
    result = subprocess.run(
        ["python3", "tools/verify_residual_eigenspace_empirical_payload_intake_target.py"],
        check=True,
        text=True,
        capture_output=True,
    )
    assert "RESIDUAL_EIGENSPACE_EMPIRICAL_PAYLOAD_INTAKE_TARGET_OK" in result.stdout

def test_payload_target_requires_authentic_data_and_covariance_slots():
    data = json.loads(ART.read_text())
    fields = set(data["required_payload_fields"])
    assert "data_vector_path" in fields
    assert "covariance_matrix_path" in fields
    assert "baseline_prediction_vector_path" in fields
    assert "candidate_prediction_vector_path" in fields
    assert "schema_validation_report_path" in fields

def test_payload_target_blocks_validation_promotion():
    data = json.loads(ART.read_text())
    assert data["status"] == "EMPIRICAL_PAYLOAD_TARGET_ONLY_NO_DATA_BOUND"
    assert data["allowed_empirical_promotion_status_after_success"] == "EMPIRICAL_TEST_READY_NOT_VALIDATED"
    assert "DFM-MKC empirical validation" in data["does_not_prove"]
    assert "Lambda-CDM failure" in data["does_not_prove"]
    assert "dark matter resolution" in data["does_not_prove"]

def test_phase_claim_boundary_remains_hypothesis_only():
    data = json.loads(ART.read_text())
    doc = DOC.read_text()
    assert data["physical_dark_matter_phase_claim_status"] == "HYPOTHESIS_ONLY"
    assert "dark matter is liquid" in data["does_not_prove"]
    assert "dark matter is solid" in data["does_not_prove"]
    assert "HYPOTHESIS_ONLY" in doc
