#!/usr/bin/env python3
import json
from pathlib import Path

import numpy as np

ART = Path("artifacts/dfm_mkc/act_dr6_prediction_vector_ordering_certificate_2026_05_25.json")
DOC = Path("docs/status/ACT_DR6_PREDICTION_VECTOR_ORDERING_CERTIFICATE_2026_05_25.md")
NPZ = Path("artifacts/dfm_mkc/act_dr6_cmbonly_official_data_covariance_2026_05_25.npz")

REQUIRED_BOUNDARIES = {
    "baseline LCDM prediction vector exists",
    "DFM-MKC prediction vector exists",
    "baseline LCDM prediction vector is correct",
    "DFM-MKC prediction vector is correct",
    "ACT DR6 residual eigenspace empirical comparison has been run",
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
    assert ART.exists(), ART
    assert DOC.exists(), DOC
    assert NPZ.exists(), NPZ

    data = json.loads(ART.read_text())
    doc = DOC.read_text()
    npz = np.load(NPZ)

    assert data["id"] == "ACT_DR6_PREDICTION_VECTOR_ORDERING_CERTIFICATE_2026_05_25"
    assert data["status"] == "ORDERING_CERTIFICATE_FOR_EXTRACTED_DATA_VECTOR_ONLY_PREDICTIONS_STILL_MISSING"
    assert data["closes_missing_object"] == "ACT_DR6_PREDICTION_VECTOR_ORDERING_CERTIFICATE"
    assert data["physical_dark_matter_phase_claim_status"] == "HYPOTHESIS_ONLY"
    assert data["allowed_next_status_after_prediction_vectors_exist"] == "RESIDUAL_EIGENSPACE_COMPARISON_READY_NOT_VALIDATED"

    data_key = data["data_vector"]["key"]
    cov_key = data["covariance"]["key"]
    arr = np.asarray(npz[data_key])
    cov = np.asarray(npz[cov_key])

    assert list(arr.shape) == data["data_vector"]["shape"]
    assert list(cov.shape) == data["covariance"]["shape"]
    assert cov.shape == (arr.shape[0], arr.shape[0])
    assert data["ordering_rule"]["required_prediction_vector_shape"] == list(arr.shape)
    assert data["still_missing_objects_after_this_certificate"] == [
        "ACT_DR6_BASELINE_LCDM_PREDICTION_VECTOR",
        "ACT_DR6_DFM_MKC_PREDICTION_VECTOR",
    ]

    assert REQUIRED_BOUNDARIES <= set(data["does_not_prove"])

    for token in (
        REQUIRED_BOUNDARIES
        | {
            "ACT_DR6_PREDICTION_VECTOR_ORDERING_CERTIFICATE",
            "ORDERING_CERTIFICATE_FOR_EXTRACTED_DATA_VECTOR_ONLY_PREDICTIONS_STILL_MISSING",
            "ACT_DR6_BASELINE_LCDM_PREDICTION_VECTOR",
            "ACT_DR6_DFM_MKC_PREDICTION_VECTOR",
            "RESIDUAL_EIGENSPACE_COMPARISON_READY_NOT_VALIDATED",
            "HYPOTHESIS_ONLY",
        }
    ):
        assert token in doc, token

    print("ACT_DR6_PREDICTION_VECTOR_ORDERING_CERTIFICATE_OK")

if __name__ == "__main__":
    main()
