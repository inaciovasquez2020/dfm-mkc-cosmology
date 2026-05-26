import json
import subprocess
from pathlib import Path

import numpy as np

ART = Path("artifacts/dfm_mkc/act_dr6_cmbonly_official_array_extraction_2026_05_25.json")
NPZ = Path("artifacts/dfm_mkc/act_dr6_cmbonly_official_data_covariance_2026_05_25.npz")

def test_act_dr6_official_array_extraction_verifier_passes():
    result = subprocess.run(
        ["python3", "tools/verify_act_dr6_cmbonly_official_array_extraction.py"],
        check=True,
        text=True,
        capture_output=True,
    )
    assert "ACT_DR6_CMBONLY_OFFICIAL_ARRAY_EXTRACTION_VERIFIED" in result.stdout

def test_act_dr6_official_arrays_have_matching_dimensions():
    arrays = np.load(NPZ)
    data_vector = arrays["data_vector"]
    covariance = arrays["covariance_matrix"]
    assert data_vector.ndim == 1
    assert covariance.ndim == 2
    assert covariance.shape[0] == covariance.shape[1] == data_vector.shape[0]

def test_act_dr6_official_array_artifact_preserves_no_model_comparison_boundary():
    data = json.loads(ART.read_text())
    assert data["status"] == "OFFICIAL_DATA_VECTOR_COVARIANCE_EXTRACTED_NO_MODEL_COMPARISON"
    assert data["baseline_lcdm_prediction_vector_status"] == "NOT_AVAILABLE"
    assert data["dfm_mkc_prediction_vector_status"] == "NOT_AVAILABLE_NO_DFM_MKC_ACT_SOLVER_BOUND"
    assert data["residual_eigenspace_empirical_run_status"] == "NOT_RUN_REQUIRES_BASELINE_AND_DFM_MKC_PREDICTION_VECTORS"
    assert "DFM-MKC empirical validation" in data["does_not_prove"]
    assert "Lambda-CDM failure" in data["does_not_prove"]

def test_phase_claim_boundary_remains_hypothesis_only():
    data = json.loads(ART.read_text())
    assert data["physical_dark_matter_phase_claim_status"] == "HYPOTHESIS_ONLY"
    assert "dark matter is liquid" in data["does_not_prove"]
    assert "dark matter is solid" in data["does_not_prove"]
