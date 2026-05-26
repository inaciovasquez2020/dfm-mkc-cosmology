#!/usr/bin/env python3
import json
from pathlib import Path

ART = Path("artifacts/dfm_mkc/act_dr6_prediction_vector_missing_object_target_2026_05_25.json")
DOC = Path("docs/status/ACT_DR6_PREDICTION_VECTOR_MISSING_OBJECT_TARGET_2026_05_25.md")
NPZ = Path("artifacts/dfm_mkc/act_dr6_cmbonly_official_data_covariance_2026_05_25.npz")

REQUIRED_MISSING = {
    "ACT_DR6_BASELINE_LCDM_PREDICTION_VECTOR",
    "ACT_DR6_DFM_MKC_PREDICTION_VECTOR",
    "ACT_DR6_PREDICTION_VECTOR_ORDERING_CERTIFICATE",
}

REQUIRED_BOUNDARIES = {
    "baseline LCDM prediction vector exists",
    "DFM-MKC prediction vector exists",
    "prediction vector ordering has been certified",
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

    assert data["id"] == "ACT_DR6_PREDICTION_VECTOR_MISSING_OBJECT_TARGET_2026_05_25"
    assert data["status"] == "MISSING_PREDICTION_VECTOR_TARGET_ONLY_NO_MODEL_COMPARISON"
    assert data["object_added"]["id"] == "ACT_DR6_PREDICTION_VECTOR_MISSING_OBJECT_TARGET"
    assert data["object_added"]["status"] == "OPEN_TARGET"
    assert data["allowed_next_status_after_all_objects_exist"] == "RESIDUAL_EIGENSPACE_COMPARISON_READY_NOT_VALIDATED"
    assert data["physical_dark_matter_phase_claim_status"] == "HYPOTHESIS_ONLY"

    missing_ids = {item["id"] for item in data["required_missing_objects"]}
    assert REQUIRED_MISSING <= missing_ids
    assert REQUIRED_BOUNDARIES <= set(data["does_not_prove"])

    for token in (
        REQUIRED_MISSING
        | REQUIRED_BOUNDARIES
        | {
            "ACT_DR6_PREDICTION_VECTOR_MISSING_OBJECT_TARGET",
            "MISSING_PREDICTION_VECTOR_TARGET_ONLY_NO_MODEL_COMPARISON",
            "RESIDUAL_EIGENSPACE_COMPARISON_READY_NOT_VALIDATED",
            "HYPOTHESIS_ONLY",
        }
    ):
        assert token in doc, token

    print("ACT_DR6_PREDICTION_VECTOR_MISSING_OBJECT_TARGET_OK")

if __name__ == "__main__":
    main()
