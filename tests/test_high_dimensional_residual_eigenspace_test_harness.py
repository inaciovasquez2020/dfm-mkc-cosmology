import json
import subprocess
from pathlib import Path

ART = Path("artifacts/dfm_mkc/high_dimensional_residual_eigenspace_test_harness_2026_05_25.json")
DOC = Path("docs/status/HIGH_DIMENSIONAL_RESIDUAL_EIGENSPACE_TEST_HARNESS_2026_05_25.md")
TOOL = Path("tools/run_high_dimensional_residual_eigenspace_test.py")

def test_high_dimensional_residual_eigenspace_harness_verifier_passes():
    result = subprocess.run(
        ["python3", "tools/verify_high_dimensional_residual_eigenspace_test_harness.py"],
        check=True,
        text=True,
        capture_output=True,
    )
    assert "HIGH_DIMENSIONAL_RESIDUAL_EIGENSPACE_TEST_HARNESS_OK" in result.stdout

def test_synthetic_eigenspace_harness_outputs_required_diagnostics():
    result = subprocess.run(
        ["python3", str(TOOL), "--seed", "145", "--top-k", "3"],
        check=True,
        text=True,
        capture_output=True,
    )
    payload = json.loads(result.stdout)

    for key in [
        "baseline_rank",
        "candidate_rank",
        "baseline_min_eigenvalue",
        "candidate_min_eigenvalue",
        "baseline_condition_number",
        "candidate_condition_number",
        "top_eigenspace_projection_distance",
        "boundary_guard_passed",
    ]:
        assert key in payload

    assert payload["baseline_rank"] == payload["dimension"]
    assert payload["candidate_rank"] == payload["dimension"]
    assert payload["boundary_guard_passed"] is True

def test_synthetic_boundary_covariance_failure_case_is_detected():
    result = subprocess.run(
        ["python3", str(TOOL), "--seed", "145", "--top-k", "3"],
        check=True,
        text=True,
        capture_output=True,
    )
    payload = json.loads(result.stdout)

    assert payload["singular_failure_rank"] < payload["dimension"]
    assert payload["synthetic_singular_boundary_guard_passed"] is False

def test_harness_artifact_preserves_boundaries():
    data = json.loads(ART.read_text())
    doc = DOC.read_text()

    assert data["status"] == "SYNTHETIC_HARNESS_ONLY_NO_EMPIRICAL_EVIDENCE"
    assert data["physical_dark_matter_phase_claim_status"] == "HYPOTHESIS_ONLY"
    assert "DFM-MKC empirical validation" in data["does_not_prove"]
    assert "Lambda-CDM failure" in data["does_not_prove"]
    assert "dark matter resolution" in data["does_not_prove"]
    assert "dark matter is liquid" in data["does_not_prove"]
    assert "dark matter is solid" in data["does_not_prove"]

    assert "This is a synthetic harness only." in doc
    assert "HYPOTHESIS_ONLY" in doc
