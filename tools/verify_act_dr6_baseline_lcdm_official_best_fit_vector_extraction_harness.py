#!/usr/bin/env python3
import json
from pathlib import Path

ART = Path("artifacts/dfm_mkc/act_dr6_baseline_lcdm_official_best_fit_vector_extraction_harness_2026_05_25.json")
DOC = Path("docs/status/ACT_DR6_BASELINE_LCDM_OFFICIAL_BEST_FIT_VECTOR_EXTRACTION_HARNESS_2026_05_25.md")
HARNESS = Path("tools/extract_act_dr6_baseline_lcdm_official_best_fit_vector.py")
READINESS = Path("artifacts/dfm_mkc/act_dr6_baseline_lcdm_official_source_provenance_readiness_2026_05_25.json")
ORDER = Path("artifacts/dfm_mkc/act_dr6_prediction_vector_ordering_certificate_2026_05_25.json")

REQUIRED_BOUNDARIES = {
    "baseline LCDM prediction vector exists",
    "baseline LCDM prediction vector has been extracted",
    "baseline LCDM prediction vector is row-aligned",
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
    for p in [ART, DOC, HARNESS, READINESS, ORDER]:
        assert p.exists(), p

    data = json.loads(ART.read_text())
    doc = DOC.read_text()
    order = json.loads(ORDER.read_text())
    harness = HARNESS.read_text()

    assert data["id"] == "ACT_DR6_BASELINE_LCDM_OFFICIAL_BEST_FIT_VECTOR_EXTRACTION_HARNESS_2026_05_25"
    assert data["status"] == "EXTRACTION_HARNESS_ONLY_NO_BASELINE_VECTOR_EXTRACTED"
    assert data["object_added"]["id"] == "ACT_DR6_BASELINE_LCDM_OFFICIAL_BEST_FIT_VECTOR_EXTRACTION_HARNESS"
    assert data["object_added"]["status"] == "HARNESS_AVAILABLE_NO_VECTOR_EXTRACTED"
    assert data["object_added"]["script"] == str(HARNESS)
    assert data["target_missing_object"] == "ACT_DR6_BASELINE_LCDM_PREDICTION_VECTOR"
    assert data["required_prediction_vector_shape"] == order["ordering_rule"]["required_prediction_vector_shape"]
    assert data["row_order_binding_status"] == "HARNESS_CAN_BIND_BY_EXPLICIT_MAPPING_ROW_AUDIT_STILL_REQUIRED"
    assert data["not_observed_data_vector_certificate_status"] == "HARNESS_SOURCE_CLASS_SEPARATION_READY"
    assert data["allowed_next_status_after_successful_extraction"] == "BASELINE_LCDM_EXTRACTED_VECTOR_CANDIDATE_READY_FOR_ROW_ORDER_AUDIT"
    assert data["still_missing_objects_after_this_harness"] == [
        "ACT_DR6_BASELINE_LCDM_PREDICTION_VECTOR",
        "ACT_DR6_DFM_MKC_PREDICTION_VECTOR",
    ]
    assert data["physical_dark_matter_phase_claim_status"] == "HYPOTHESIS_ONLY"
    assert REQUIRED_BOUNDARIES <= set(data["does_not_prove"])

    for token in [
        "parse_mapping",
        "build_vector",
        "mapping covers",
        "best_fit_sha256",
        "mapping_sha256",
        "vector_sha256",
        "DO_NOT_PROMOTE_TO_ACT_DR6_BASELINE_LCDM_PREDICTION_VECTOR",
    ]:
        assert token in harness, token

    for token in (
        REQUIRED_BOUNDARIES
        | {
            "ACT_DR6_BASELINE_LCDM_OFFICIAL_BEST_FIT_VECTOR_EXTRACTION_HARNESS",
            "EXTRACTION_HARNESS_ONLY_NO_BASELINE_VECTOR_EXTRACTED",
            "ACT_DR6_BASELINE_LCDM_PREDICTION_VECTOR",
            "BASELINE_LCDM_EXTRACTED_VECTOR_CANDIDATE_READY_FOR_ROW_ORDER_AUDIT",
            "HARNESS_CAN_BIND_BY_EXPLICIT_MAPPING_ROW_AUDIT_STILL_REQUIRED",
            "ACT_DR6_DFM_MKC_PREDICTION_VECTOR",
            "HYPOTHESIS_ONLY",
        }
    ):
        assert token in doc, token

    print("ACT_DR6_BASELINE_LCDM_OFFICIAL_BEST_FIT_VECTOR_EXTRACTION_HARNESS_OK")

if __name__ == "__main__":
    main()
