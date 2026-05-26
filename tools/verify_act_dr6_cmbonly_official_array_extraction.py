#!/usr/bin/env python3
import json
import subprocess
from pathlib import Path

import numpy as np

ART = Path("artifacts/dfm_mkc/act_dr6_cmbonly_official_array_extraction_2026_05_25.json")
NPZ = Path("artifacts/dfm_mkc/act_dr6_cmbonly_official_data_covariance_2026_05_25.npz")
DOC = Path("docs/status/ACT_DR6_CMBONLY_OFFICIAL_ARRAY_EXTRACTION_2026_05_25.md")
TOOL = Path("tools/extract_act_dr6_cmbonly_official_arrays.py")

REQUIRED_BOUNDARIES = {
    "baseline LCDM prediction vector exists",
    "DFM-MKC prediction vector exists",
    "residual eigenspace empirical comparison has been run",
    "DFM-MKC empirical validation",
    "Lambda-CDM failure",
    "dark matter resolution",
    "dark energy resolution",
    "dark matter is liquid",
    "dark matter is solid",
    "dark matter phase transition is physically real",
    "ACT validation of DFM-MKC",
    "CMB validation of DFM-MKC",
    "independent empirical replication",
    "gravity closure",
    "Chronos-RR",
    "H4.1/FGL",
    "P vs NP",
    "any Clay problem",
}

def main() -> None:
    subprocess.run(["python3", str(TOOL)], check=True)

    assert ART.exists(), ART
    assert NPZ.exists(), NPZ
    assert DOC.exists(), DOC

    data = json.loads(ART.read_text())
    doc = DOC.read_text()

    assert data["id"] == "ACT_DR6_CMBONLY_OFFICIAL_ARRAY_EXTRACTION_2026_05_25"
    assert data["status"] == "OFFICIAL_DATA_VECTOR_COVARIANCE_EXTRACTED_NO_MODEL_COMPARISON"
    assert data["extraction_backend"] == "sacc.Sacc.load_fits"
    assert data["baseline_lcdm_prediction_vector_status"] == "NOT_AVAILABLE"
    assert data["dfm_mkc_prediction_vector_status"] == "NOT_AVAILABLE_NO_DFM_MKC_ACT_SOLVER_BOUND"
    assert data["residual_eigenspace_empirical_run_status"] == "NOT_RUN_REQUIRES_BASELINE_AND_DFM_MKC_PREDICTION_VECTORS"
    assert data["physical_dark_matter_phase_claim_status"] == "HYPOTHESIS_ONLY"
    assert REQUIRED_BOUNDARIES <= set(data["does_not_prove"])

    arrays = np.load(NPZ)
    data_vector = arrays["data_vector"]
    covariance = arrays["covariance_matrix"]
    eigvals = arrays["covariance_eigenvalues"]

    assert data_vector.ndim == 1
    assert covariance.ndim == 2
    assert covariance.shape[0] == covariance.shape[1]
    assert covariance.shape[0] == data_vector.shape[0]
    assert eigvals.shape[0] == data_vector.shape[0]
    assert np.isfinite(data_vector).all()
    assert np.isfinite(covariance).all()
    assert data["data_vector_shape"] == list(data_vector.shape)
    assert data["covariance_matrix_shape"] == list(covariance.shape)

    for token in REQUIRED_BOUNDARIES | {
        "OFFICIAL_DATA_VECTOR_COVARIANCE_EXTRACTED_NO_MODEL_COMPARISON",
        "HYPOTHESIS_ONLY",
    }:
        assert token in doc, token

    print("ACT_DR6_CMBONLY_OFFICIAL_ARRAY_EXTRACTION_VERIFIED")


if __name__ == "__main__":
    main()
