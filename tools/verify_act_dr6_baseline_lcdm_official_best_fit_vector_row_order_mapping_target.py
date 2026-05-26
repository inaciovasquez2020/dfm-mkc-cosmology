#!/usr/bin/env python3
import json
from pathlib import Path

ART = Path("artifacts/dfm_mkc/act_dr6_baseline_lcdm_official_best_fit_vector_row_order_mapping_target_2026_05_25.json")
DOC = Path("docs/status/ACT_DR6_BASELINE_LCDM_OFFICIAL_BEST_FIT_VECTOR_ROW_ORDER_MAPPING_TARGET_2026_05_25.md")
HARNESS_ART = Path("artifacts/dfm_mkc/act_dr6_baseline_lcdm_official_best_fit_vector_extraction_harness_2026_05_25.json")
READINESS = Path("artifacts/dfm_mkc/act_dr6_baseline_lcdm_official_source_provenance_readiness_2026_05_25.json")
ORDER = Path("artifacts/dfm_mkc/act_dr6_prediction_vector_ordering_certificate_2026_05_25.json")

REQUIRED_SCHEMA_FIELDS = {
    "target_index",
    "source_row",
    "source_col",
    "observable_label",
    "frequency_or_spectrum_label",
}

REQUIRED_BOUNDARIES = {
    "official best-fit row-order mapping exists",
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
    for p in [ART, DOC, HARNESS_ART, READINESS, ORDER]:
        assert p.exists(), p

    data = json.loads(ART.read_text())
    doc = DOC.read_text()
    order = json.loads(ORDER.read_text())

    assert data["id"] == "ACT_DR6_BASELINE_LCDM_OFFICIAL_BEST_FIT_VECTOR_ROW_ORDER_MAPPING_TARGET_2026_05_25"
    assert data["status"] == "ROW_ORDER_MAPPING_TARGET_ONLY_NO_MAPPING_SUPPLIED"
    assert data["object_added"]["id"] == "ACT_DR6_BASELINE_LCDM_OFFICIAL_BEST_FIT_VECTOR_ROW_ORDER_MAPPING_TARGET"
    assert data["object_added"]["status"] == "OPEN_TARGET"
    assert data["target_missing_object"] == "ACT_DR6_BASELINE_LCDM_OFFICIAL_BEST_FIT_VECTOR_ROW_ORDER_MAPPING"
    assert data["ultimate_target_missing_object"] == "ACT_DR6_BASELINE_LCDM_PREDICTION_VECTOR"
    assert data["ordering_certificate_id"] == order["id"]
    assert data["required_prediction_vector_shape"] == order["ordering_rule"]["required_prediction_vector_shape"]
    assert data["required_mapping_schema"]["format"] == "JSON"
    assert data["required_mapping_schema"]["top_level_key"] == "row_mapping"
    fields = {item["id"] for item in data["required_mapping_schema"]["row_mapping_item_fields"]}
    assert REQUIRED_SCHEMA_FIELDS <= fields
    assert data["allowed_next_status_after_mapping_exists"] == "BASELINE_LCDM_OFFICIAL_BEST_FIT_MAPPING_READY_FOR_EXTRACTION_TRIAL"
    assert data["still_missing_objects_after_this_target"] == [
        "ACT_DR6_BASELINE_LCDM_OFFICIAL_BEST_FIT_VECTOR_ROW_ORDER_MAPPING",
        "ACT_DR6_BASELINE_LCDM_PREDICTION_VECTOR",
        "ACT_DR6_DFM_MKC_PREDICTION_VECTOR",
    ]
    assert data["physical_dark_matter_phase_claim_status"] == "HYPOTHESIS_ONLY"
    assert REQUIRED_BOUNDARIES <= set(data["does_not_prove"])

    for token in (
        REQUIRED_SCHEMA_FIELDS
        | REQUIRED_BOUNDARIES
        | {
            "ACT_DR6_BASELINE_LCDM_OFFICIAL_BEST_FIT_VECTOR_ROW_ORDER_MAPPING_TARGET",
            "ROW_ORDER_MAPPING_TARGET_ONLY_NO_MAPPING_SUPPLIED",
            "ACT_DR6_BASELINE_LCDM_OFFICIAL_BEST_FIT_VECTOR_ROW_ORDER_MAPPING",
            "ACT_DR6_BASELINE_LCDM_PREDICTION_VECTOR",
            "BASELINE_LCDM_OFFICIAL_BEST_FIT_MAPPING_READY_FOR_EXTRACTION_TRIAL",
            "ACT_DR6_DFM_MKC_PREDICTION_VECTOR",
            "HYPOTHESIS_ONLY",
        }
    ):
        assert token in doc, token

    print("ACT_DR6_BASELINE_LCDM_OFFICIAL_BEST_FIT_VECTOR_ROW_ORDER_MAPPING_TARGET_OK")

if __name__ == "__main__":
    main()
