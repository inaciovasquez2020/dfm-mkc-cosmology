#!/usr/bin/env python3
import json
from pathlib import Path

ART = Path("artifacts/dfm_mkc/act_dr6_baseline_lcdm_cobaya_run_output_binding_harness_2026_05_25.json")
DOC = Path("docs/status/ACT_DR6_BASELINE_LCDM_COBAYA_RUN_OUTPUT_BINDING_HARNESS_2026_05_25.md")
HARNESS = Path("tools/bind_act_dr6_baseline_lcdm_cobaya_run_output.py")
SOURCE_MAP = Path("artifacts/dfm_mkc/act_dr6_baseline_lcdm_theory_vector_source_map_2026_05_25.json")
ORDER = Path("artifacts/dfm_mkc/act_dr6_prediction_vector_ordering_certificate_2026_05_25.json")

REQUIRED_BOUNDARIES = {
    "baseline LCDM prediction vector exists",
    "baseline LCDM prediction vector is official",
    "baseline LCDM prediction vector is physically correct",
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
    assert HARNESS.exists(), HARNESS
    assert SOURCE_MAP.exists(), SOURCE_MAP
    assert ORDER.exists(), ORDER

    data = json.loads(ART.read_text())
    order = json.loads(ORDER.read_text())
    doc = DOC.read_text()
    harness = HARNESS.read_text()

    assert data["id"] == "ACT_DR6_BASELINE_LCDM_COBAYA_RUN_OUTPUT_BINDING_HARNESS_2026_05_25"
    assert data["status"] == "BINDING_HARNESS_ONLY_NO_BASELINE_VECTOR_IMPORTED"
    assert data["target_missing_object"] == "ACT_DR6_BASELINE_LCDM_PREDICTION_VECTOR"
    assert data["object_added"]["id"] == "ACT_DR6_BASELINE_LCDM_COBAYA_RUN_OUTPUT_BINDING_HARNESS"
    assert data["object_added"]["script"] == str(HARNESS)
    assert data["required_prediction_vector_shape"] == order["ordering_rule"]["required_prediction_vector_shape"]
    assert data["execution_result"] == "NOT_EXECUTED_NO_CANDIDATE_VECTOR_SUPPLIED"
    assert data["allowed_next_status_after_candidate_passes_harness"] == "BASELINE_LCDM_PREDICTION_VECTOR_READY_FOR_SOURCE_AUTHENTICITY_VALIDATION"
    assert data["still_missing_objects_after_this_harness"] == [
        "ACT_DR6_BASELINE_LCDM_PREDICTION_VECTOR",
        "ACT_DR6_DFM_MKC_PREDICTION_VECTOR",
    ]
    assert data["physical_dark_matter_phase_claim_status"] == "HYPOTHESIS_ONLY"
    assert REQUIRED_BOUNDARIES <= set(data["does_not_prove"])

    for token in [
        "argparse",
        "required_prediction_vector_shape",
        "candidate vector must be 1D",
        "candidate vector shape",
        "candidate_sha256",
        "SHAPE_AND_ORDER_BINDING_CANDIDATE_ONLY_NOT_VALIDATED",
    ]:
        assert token in harness, token

    for token in (
        REQUIRED_BOUNDARIES
        | {
            "ACT_DR6_BASELINE_LCDM_COBAYA_RUN_OUTPUT_BINDING_HARNESS",
            "BINDING_HARNESS_ONLY_NO_BASELINE_VECTOR_IMPORTED",
            "ACT_DR6_BASELINE_LCDM_PREDICTION_VECTOR",
            "BASELINE_LCDM_PREDICTION_VECTOR_READY_FOR_SOURCE_AUTHENTICITY_VALIDATION",
            "ACT_DR6_DFM_MKC_PREDICTION_VECTOR",
            "HYPOTHESIS_ONLY",
        }
    ):
        assert token in doc, token

    print("ACT_DR6_BASELINE_LCDM_COBAYA_RUN_OUTPUT_BINDING_HARNESS_OK")

if __name__ == "__main__":
    main()
