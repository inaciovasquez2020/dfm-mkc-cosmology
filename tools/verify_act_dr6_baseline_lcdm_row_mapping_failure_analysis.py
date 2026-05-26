#!/usr/bin/env python3
import json
from pathlib import Path

ART = Path("artifacts/dfm_mkc/act_dr6_baseline_lcdm_row_mapping_failure_analysis_2026_05_25.json")
DOC = Path("docs/status/ACT_DR6_BASELINE_LCDM_ROW_MAPPING_FAILURE_ANALYSIS_2026_05_25.md")
ANALYZE = Path("tools/analyze_act_dr6_baseline_lcdm_row_mapping_failures.py")
TRIAL_ART = Path("artifacts/dfm_mkc/act_dr6_baseline_lcdm_official_best_fit_mapping_extraction_trial_2026_05_25.json")
MANIFEST = Path("artifacts/dfm_mkc/act_dr6_official_best_fits_dr6_lcdm_payload_manifest_2026_05_25.json")
ORDER = Path("artifacts/dfm_mkc/act_dr6_prediction_vector_ordering_certificate_2026_05_25.json")

VALID_STATUSES = {
    "ROW_MAPPING_FAILURE_ANALYSIS_BLOCKED_SACC_METADATA_UNAVAILABLE",
    "ROW_MAPPING_FAILURE_ANALYSIS_BLOCKED_ROW_COUNT_MISMATCH",
    "ROW_MAPPING_FAILURE_ANALYSIS_BLOCKED_INCOMPLETE_SACC_ROW_METADATA",
    "ROW_MAPPING_FAILURE_ANALYSIS_LOCAL_SACC_METADATA_SUFFICIENT_MAPPING_ALGORITHM_STILL_OPEN",
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
    for p in [ART, DOC, ANALYZE, TRIAL_ART, MANIFEST, ORDER]:
        assert p.exists(), p

    data = json.loads(ART.read_text())
    doc = DOC.read_text()
    order = json.loads(ORDER.read_text())
    analyze = ANALYZE.read_text()

    assert data["id"] == "ACT_DR6_BASELINE_LCDM_ROW_MAPPING_FAILURE_ANALYSIS_2026_05_25"
    assert data["status"] in VALID_STATUSES
    assert data["target_missing_object"] == "ACT_DR6_BASELINE_LCDM_OFFICIAL_BEST_FIT_VECTOR_ROW_ORDER_MAPPING"
    assert data["ultimate_target_missing_object"] == "ACT_DR6_BASELINE_LCDM_PREDICTION_VECTOR"
    assert data["required_prediction_vector_shape"] == order["ordering_rule"]["required_prediction_vector_shape"]
    assert data["minimal_next_object"]["id"] == "ACT_DR6_BASELINE_LCDM_SACC_TO_BEST_FIT_LABEL_BINDING_RULE"
    assert data["minimal_next_object"]["status"] == "MISSING"
    assert data["allowed_next_status_after_binding_rule"] == "ROW_MAPPING_BINDING_RULE_READY_FOR_MAPPING_CONSTRUCTION"
    assert data["promotion_decision"] == "DO_NOT_PROMOTE_TO_ACT_DR6_BASELINE_LCDM_PREDICTION_VECTOR"
    assert data["still_missing_objects_after_this_analysis"] == [
        "ACT_DR6_BASELINE_LCDM_OFFICIAL_BEST_FIT_VECTOR_ROW_ORDER_MAPPING",
        "ACT_DR6_BASELINE_LCDM_PREDICTION_VECTOR",
        "ACT_DR6_DFM_MKC_PREDICTION_VECTOR",
    ]
    assert data["physical_dark_matter_phase_claim_status"] == "HYPOTHESIS_ONLY"
    assert isinstance(data["root_causes"], list)
    assert data["root_causes"]
    assert REQUIRED_BOUNDARIES <= set(data["does_not_prove"])

    for token in [
        "load_sacc_rows",
        "infer_spectrum_label",
        "missing_spectrum_label",
        "missing_scalar_ell",
        "ACT_DR6_BASELINE_LCDM_SACC_TO_BEST_FIT_LABEL_BINDING_RULE",
        "DO_NOT_PROMOTE_TO_ACT_DR6_BASELINE_LCDM_PREDICTION_VECTOR",
    ]:
        assert token in analyze, token

    for token in (
        REQUIRED_BOUNDARIES
        | {
            "ACT_DR6_BASELINE_LCDM_ROW_MAPPING_FAILURE_ANALYSIS",
            "ACT_DR6_BASELINE_LCDM_OFFICIAL_BEST_FIT_VECTOR_ROW_ORDER_MAPPING",
            "ACT_DR6_BASELINE_LCDM_SACC_TO_BEST_FIT_LABEL_BINDING_RULE",
            "ROW_MAPPING_BINDING_RULE_READY_FOR_MAPPING_CONSTRUCTION",
            "ACT_DR6_BASELINE_LCDM_PREDICTION_VECTOR",
            "ACT_DR6_DFM_MKC_PREDICTION_VECTOR",
            "HYPOTHESIS_ONLY",
        }
    ):
        assert token in doc, token

    print("ACT_DR6_BASELINE_LCDM_ROW_MAPPING_FAILURE_ANALYSIS_OK")

if __name__ == "__main__":
    main()
