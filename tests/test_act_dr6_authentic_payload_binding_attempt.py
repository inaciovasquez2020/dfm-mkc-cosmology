import json
import subprocess
from pathlib import Path

ART = Path("artifacts/dfm_mkc/act_dr6_authentic_payload_binding_attempt_2026_05_25.json")
DATA = Path("data/act_dr6_cmbonly/dr6_data_cmbonly.fits")
SHA = Path("data/act_dr6_cmbonly/dr6_data_cmbonly.fits.sha256")
SCHEMA = Path("artifacts/dfm_mkc/act_dr6_cmbonly_fits_schema_summary_2026_05_25.json")

def test_act_dr6_authentic_payload_binding_verifier_passes():
    result = subprocess.run(
        ["python3", "tools/verify_act_dr6_authentic_payload_binding_attempt.py"],
        check=True,
        text=True,
        capture_output=True,
    )
    assert "ACT_DR6_AUTHENTIC_PAYLOAD_BINDING_ATTEMPT_OK" in result.stdout

def test_act_dr6_payload_file_and_sha_exist():
    assert DATA.exists()
    assert SHA.exists()
    assert DATA.stat().st_size > 0
    assert len(SHA.read_text().split()[0]) == 64

def test_act_dr6_schema_summary_exists():
    schema = json.loads(SCHEMA.read_text())
    assert schema["status"] == "ACT_DR6_CMBONLY_FITS_SCHEMA_SUMMARY"
    assert schema["hdu_count"] >= 1

def test_act_dr6_binding_preserves_no_overclaim_boundaries():
    data = json.loads(ART.read_text())
    assert data["actual_data_file_bound"] is True
    assert data["actual_sha256_verified_payload"] is True
    assert data["dfm_mkc_prediction_vector_status"] == "NOT_AVAILABLE_NO_DFM_MKC_ACT_SOLVER_BOUND"
    assert data["residual_eigenspace_empirical_run_status"] == "NOT_RUN_REQUIRES_BASELINE_AND_DFM_MKC_PREDICTION_VECTORS"
    assert data["physical_dark_matter_phase_claim_status"] == "HYPOTHESIS_ONLY"
    assert "DFM-MKC empirical validation" in data["does_not_prove"]
    assert "Lambda-CDM failure" in data["does_not_prove"]
    assert "dark matter resolution" in data["does_not_prove"]
