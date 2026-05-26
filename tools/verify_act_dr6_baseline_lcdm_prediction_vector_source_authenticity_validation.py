#!/usr/bin/env python3
import json
from pathlib import Path

ART = Path("artifacts/dfm_mkc/act_dr6_baseline_lcdm_prediction_vector_source_authenticity_validation_2026_05_25.json")
DOC = Path("docs/status/ACT_DR6_BASELINE_LCDM_PREDICTION_VECTOR_SOURCE_AUTHENTICITY_VALIDATION_2026_05_25.md")
CANDIDATE = Path("artifacts/dfm_mkc/act_dr6_baseline_lcdm_prediction_vector_binding_candidate_from_probe.json")
PROBE_ART = Path("artifacts/dfm_mkc/act_dr6_baseline_lcdm_prediction_vector_candidate_probe_2026_05_25.json")
PROBE_RESULT = Path("artifacts/dfm_mkc/act_dr6_baseline_lcdm_prediction_vector_candidate_probe_result.json")
SOURCE_MAP = Path("artifacts/dfm_mkc/act_dr6_baseline_lcdm_theory_vector_source_map_2026_05_25.json")
ORDER = Path("artifacts/dfm_mkc/act_dr6_prediction_vector_ordering_certificate_2026_05_25.json")

REQUIRED_BOUNDARIES = {
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

VALID_STATUSES = {
    "SOURCE_AUTHENTICITY_REJECTED_DATA_VECTOR_NOT_BASELINE_THEORY",
    "SOURCE_AUTHENTICITY_UNVALIDATED_NO_BASELINE_THEORY_PROVENANCE",
    "SOURCE_AUTHENTICITY_REQUIRES_MANUAL_OFFICIAL_PROVENANCE_REVIEW",
}

def main() -> None:
    for p in [ART, DOC, CANDIDATE, PROBE_ART, PROBE_RESULT, SOURCE_MAP, ORDER]:
        assert p.exists(), p

    data = json.loads(ART.read_text())
    candidate = json.loads(CANDIDATE.read_text())
    order = json.loads(ORDER.read_text())
    doc = DOC.read_text()

    assert data["id"] == "ACT_DR6_BASELINE_LCDM_PREDICTION_VECTOR_SOURCE_AUTHENTICITY_VALIDATION_2026_05_25"
    assert data["status"] in VALID_STATUSES
    assert data["target_missing_object"] == "ACT_DR6_BASELINE_LCDM_PREDICTION_VECTOR"
    assert data["object_added"]["id"] == "ACT_DR6_BASELINE_LCDM_PREDICTION_VECTOR_SOURCE_AUTHENTICITY_VALIDATION"
    assert data["object_added"]["status"] == "VALIDATION_RECORD_NO_PROMOTION"
    assert data["candidate_binding_status"] == candidate["status"]
    assert data["candidate_shape"] == order["ordering_rule"]["required_prediction_vector_shape"]
    assert data["required_prediction_vector_shape"] == order["ordering_rule"]["required_prediction_vector_shape"]
    assert data["promotion_decision"] == "DO_NOT_PROMOTE_TO_ACT_DR6_BASELINE_LCDM_PREDICTION_VECTOR"
    assert data["minimal_next_object"]["id"] == "OFFICIAL_ACT_DR6_BASELINE_LCDM_THEORY_VECTOR_PROVENANCE_CERTIFICATE"
    assert data["minimal_next_object"]["status"] == "MISSING"
    assert data["still_missing_objects_after_this_validation"] == [
        "ACT_DR6_BASELINE_LCDM_PREDICTION_VECTOR",
        "ACT_DR6_DFM_MKC_PREDICTION_VECTOR",
    ]
    assert data["physical_dark_matter_phase_claim_status"] == "HYPOTHESIS_ONLY"
    assert REQUIRED_BOUNDARIES <= set(data["does_not_prove"])

    checks = {item["id"]: item["status"] for item in data["source_authenticity_checks"]}
    assert checks["shape_binding_candidate_exists"] == "PASSED"
    assert checks["shape_matches_order_certificate"] == "PASSED"
    assert checks["official_baseline_lcdm_theory_provenance"] == "MISSING"
    assert checks["official_act_cobaya_camb_digest_binding"] == "MISSING"

    for token in (
        REQUIRED_BOUNDARIES
        | {
            "ACT_DR6_BASELINE_LCDM_PREDICTION_VECTOR_SOURCE_AUTHENTICITY_VALIDATION",
            "ACT_DR6_BASELINE_LCDM_PREDICTION_VECTOR",
            "OFFICIAL_ACT_DR6_BASELINE_LCDM_THEORY_VECTOR_PROVENANCE_CERTIFICATE",
            "DO_NOT_PROMOTE_TO_ACT_DR6_BASELINE_LCDM_PREDICTION_VECTOR",
            "ACT_DR6_DFM_MKC_PREDICTION_VECTOR",
            "HYPOTHESIS_ONLY",
        }
    ):
        assert token in doc, token

    print("ACT_DR6_BASELINE_LCDM_PREDICTION_VECTOR_SOURCE_AUTHENTICITY_VALIDATION_OK")

if __name__ == "__main__":
    main()
