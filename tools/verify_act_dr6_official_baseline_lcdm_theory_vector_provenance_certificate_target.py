#!/usr/bin/env python3
import json
from pathlib import Path

ART = Path("artifacts/dfm_mkc/act_dr6_official_baseline_lcdm_theory_vector_provenance_certificate_target_2026_05_25.json")
DOC = Path("docs/status/ACT_DR6_OFFICIAL_BASELINE_LCDM_THEORY_VECTOR_PROVENANCE_CERTIFICATE_TARGET_2026_05_25.md")
VALIDATION = Path("artifacts/dfm_mkc/act_dr6_baseline_lcdm_prediction_vector_source_authenticity_validation_2026_05_25.json")
SOURCE_MAP = Path("artifacts/dfm_mkc/act_dr6_baseline_lcdm_theory_vector_source_map_2026_05_25.json")
ORDER = Path("artifacts/dfm_mkc/act_dr6_prediction_vector_ordering_certificate_2026_05_25.json")

REQUIRED_FIELDS = {
    "official_likelihood_source",
    "official_parameter_or_bestfit_source",
    "camb_or_cobaya_execution_record",
    "theory_vector_extraction_rule",
    "row_order_binding",
    "shape_digest_certificate",
    "not_observed_data_vector_certificate",
}

REQUIRED_BOUNDARIES = {
    "official ACT DR6 baseline LCDM theory-vector provenance certificate exists",
    "baseline LCDM prediction vector exists",
    "baseline LCDM prediction vector is official",
    "baseline LCDM prediction vector is physically correct",
    "bound candidate is a baseline LCDM theory vector",
    "bound candidate is source-authenticated",
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
    for p in [ART, DOC, VALIDATION, SOURCE_MAP, ORDER]:
        assert p.exists(), p

    data = json.loads(ART.read_text())
    validation = json.loads(VALIDATION.read_text())
    order = json.loads(ORDER.read_text())
    doc = DOC.read_text()

    assert data["id"] == "ACT_DR6_OFFICIAL_BASELINE_LCDM_THEORY_VECTOR_PROVENANCE_CERTIFICATE_TARGET_2026_05_25"
    assert data["status"] == "PROVENANCE_CERTIFICATE_TARGET_ONLY_OFFICIAL_THEORY_VECTOR_SOURCE_MISSING"
    assert data["target_missing_object"] == "OFFICIAL_ACT_DR6_BASELINE_LCDM_THEORY_VECTOR_PROVENANCE_CERTIFICATE"
    assert data["ultimate_target_missing_object"] == "ACT_DR6_BASELINE_LCDM_PREDICTION_VECTOR"
    assert data["object_added"]["id"] == "OFFICIAL_ACT_DR6_BASELINE_LCDM_THEORY_VECTOR_PROVENANCE_CERTIFICATE_TARGET"
    assert data["object_added"]["status"] == "OPEN_TARGET"
    assert data["source_authenticity_validation_status"] == validation["status"]
    assert data["source_authenticity_promotion_decision"] == validation["promotion_decision"]
    assert data["required_prediction_vector_shape"] == order["ordering_rule"]["required_prediction_vector_shape"]
    assert data["allowed_next_status_after_certificate_exists"] == "BASELINE_LCDM_PROVENANCE_CERTIFIED_VECTOR_EXTRACTION_READY"
    assert data["still_missing_objects_after_this_target"] == [
        "OFFICIAL_ACT_DR6_BASELINE_LCDM_THEORY_VECTOR_PROVENANCE_CERTIFICATE",
        "ACT_DR6_BASELINE_LCDM_PREDICTION_VECTOR",
        "ACT_DR6_DFM_MKC_PREDICTION_VECTOR",
    ]
    assert data["physical_dark_matter_phase_claim_status"] == "HYPOTHESIS_ONLY"

    fields = {item["id"]: item["status"] for item in data["required_certificate_fields"]}
    assert REQUIRED_FIELDS <= set(fields)
    assert all(fields[field] == "REQUIRED" for field in REQUIRED_FIELDS)
    assert REQUIRED_BOUNDARIES <= set(data["does_not_prove"])

    for token in (
        REQUIRED_FIELDS
        | REQUIRED_BOUNDARIES
        | {
            "OFFICIAL_ACT_DR6_BASELINE_LCDM_THEORY_VECTOR_PROVENANCE_CERTIFICATE_TARGET",
            "PROVENANCE_CERTIFICATE_TARGET_ONLY_OFFICIAL_THEORY_VECTOR_SOURCE_MISSING",
            "OFFICIAL_ACT_DR6_BASELINE_LCDM_THEORY_VECTOR_PROVENANCE_CERTIFICATE",
            "ACT_DR6_BASELINE_LCDM_PREDICTION_VECTOR",
            "BASELINE_LCDM_PROVENANCE_CERTIFIED_VECTOR_EXTRACTION_READY",
            "ACT_DR6_DFM_MKC_PREDICTION_VECTOR",
            "HYPOTHESIS_ONLY",
        }
    ):
        assert token in doc, token

    print("ACT_DR6_OFFICIAL_BASELINE_LCDM_THEORY_VECTOR_PROVENANCE_CERTIFICATE_TARGET_OK")

if __name__ == "__main__":
    main()
