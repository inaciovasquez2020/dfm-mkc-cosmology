#!/usr/bin/env python3
import json
from pathlib import Path

ART = Path("artifacts/dfm_mkc/act_dr6_baseline_lcdm_prediction_vector_execution_gate_2026_05_25.json")
DOC = Path("docs/status/ACT_DR6_BASELINE_LCDM_PREDICTION_VECTOR_EXECUTION_GATE_2026_05_25.md")
ORDER = Path("artifacts/dfm_mkc/act_dr6_prediction_vector_ordering_certificate_2026_05_25.json")
NPZ = Path("artifacts/dfm_mkc/act_dr6_cmbonly_official_data_covariance_2026_05_25.npz")

REQUIRED_BOUNDARIES = {
    "baseline LCDM prediction vector exists",
    "trusted baseline LCDM theory source exists",
    "baseline LCDM prediction vector is correct",
    "DFM-MKC prediction vector exists",
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
    assert ORDER.exists(), ORDER
    assert NPZ.exists(), NPZ

    data = json.loads(ART.read_text())
    order = json.loads(ORDER.read_text())
    doc = DOC.read_text()

    assert data["id"] == "ACT_DR6_BASELINE_LCDM_PREDICTION_VECTOR_EXECUTION_GATE_2026_05_25"
    assert data["status"] == "BASELINE_LCDM_PREDICTION_VECTOR_EXECUTION_BLOCKED_SOURCE_MISSING"
    assert data["target_missing_object"] == "ACT_DR6_BASELINE_LCDM_PREDICTION_VECTOR"
    assert data["execution_result"] == "NOT_EXECUTED"
    assert data["minimal_missing_input"]["id"] == "TRUSTED_ACT_DR6_BASELINE_LCDM_THEORY_VECTOR_SOURCE"
    assert data["minimal_missing_input"]["status"] == "MISSING"
    assert data["required_prediction_vector_shape"] == order["ordering_rule"]["required_prediction_vector_shape"]
    assert data["allowed_next_status_after_missing_input_exists"] == "BASELINE_LCDM_PREDICTION_VECTOR_READY_FOR_SHAPE_AND_ORDER_VALIDATION"
    assert data["still_missing_objects_after_this_gate"] == [
        "ACT_DR6_BASELINE_LCDM_PREDICTION_VECTOR",
        "ACT_DR6_DFM_MKC_PREDICTION_VECTOR",
    ]
    assert data["physical_dark_matter_phase_claim_status"] == "HYPOTHESIS_ONLY"
    assert REQUIRED_BOUNDARIES <= set(data["does_not_prove"])

    for token in (
        REQUIRED_BOUNDARIES
        | {
            "ACT_DR6_BASELINE_LCDM_PREDICTION_VECTOR",
            "TRUSTED_ACT_DR6_BASELINE_LCDM_THEORY_VECTOR_SOURCE",
            "BASELINE_LCDM_PREDICTION_VECTOR_EXECUTION_BLOCKED_SOURCE_MISSING",
            "BASELINE_LCDM_PREDICTION_VECTOR_READY_FOR_SHAPE_AND_ORDER_VALIDATION",
            "ACT_DR6_DFM_MKC_PREDICTION_VECTOR",
            "HYPOTHESIS_ONLY",
        }
    ):
        assert token in doc, token

    print("ACT_DR6_BASELINE_LCDM_PREDICTION_VECTOR_EXECUTION_GATE_OK")

if __name__ == "__main__":
    main()
