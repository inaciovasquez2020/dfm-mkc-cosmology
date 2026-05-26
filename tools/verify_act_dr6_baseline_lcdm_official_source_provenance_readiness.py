#!/usr/bin/env python3
import json
from pathlib import Path

ART = Path("artifacts/dfm_mkc/act_dr6_baseline_lcdm_official_source_provenance_readiness_2026_05_25.json")
DOC = Path("docs/status/ACT_DR6_BASELINE_LCDM_OFFICIAL_SOURCE_PROVENANCE_READINESS_2026_05_25.md")
TARGET = Path("artifacts/dfm_mkc/act_dr6_official_baseline_lcdm_theory_vector_provenance_certificate_target_2026_05_25.json")
VALIDATION = Path("artifacts/dfm_mkc/act_dr6_baseline_lcdm_prediction_vector_source_authenticity_validation_2026_05_25.json")
ORDER = Path("artifacts/dfm_mkc/act_dr6_prediction_vector_ordering_certificate_2026_05_25.json")

REQUIRED_SOURCES = {
    "NASA_LAMBDA_ACT_DR6_02_PSPIPE_BEST_FITS_INFO",
    "NASA_LAMBDA_ACT_DR6_02_PSPIPE_BEST_FITS_DOWNLOADS",
    "NASA_LAMBDA_ACT_DR6_02_CHAINS_INFO",
    "ACT_DR6_PARAMETERS_REPOSITORY",
}

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
    for p in [ART, DOC, TARGET, VALIDATION, ORDER]:
        assert p.exists(), p

    data = json.loads(ART.read_text())
    doc = DOC.read_text()
    order = json.loads(ORDER.read_text())

    assert data["id"] == "ACT_DR6_BASELINE_LCDM_OFFICIAL_SOURCE_PROVENANCE_READINESS_2026_05_25"
    assert data["status"] == "BASELINE_LCDM_PROVENANCE_CERTIFIED_VECTOR_EXTRACTION_READY_NO_VECTOR_PROMOTION"
    assert data["object_added"]["id"] == "OFFICIAL_ACT_DR6_BASELINE_LCDM_THEORY_VECTOR_PROVENANCE_CERTIFICATE"
    assert data["object_added"]["status"] == "SOURCE_PROVENANCE_CERTIFIED_EXTRACTION_READY"
    assert data["required_prediction_vector_shape"] == order["ordering_rule"]["required_prediction_vector_shape"]
    assert REQUIRED_SOURCES <= set(data["official_sources"])
    assert data["digest_bound_execution_record"]["status"] == "SOURCE_AND_CONFIGURATION_DIGEST_BOUND_EXECUTION_NOT_RUN_HERE"
    assert data["digest_bound_execution_record"]["boltzmann_code"] == "CAMB"
    assert data["digest_bound_execution_record"]["camb_version_from_official_source"] == "1.5.9"
    assert data["row_order_binding_against_act_dr6_ordering"]["status"] == "EXTRACTION_RULE_READY_BINDING_NOT_YET_APPLIED_TO_VECTOR"
    assert data["not_observed_data_vector_certificate"]["status"] == "SOURCE_CLASS_SEPARATION_CERTIFIED_FOR_OFFICIAL_SOURCE"
    assert data["promotion"]["to"] == "BASELINE_LCDM_PROVENANCE_CERTIFIED_VECTOR_EXTRACTION_READY"
    assert data["promotion"]["explicitly_not_promoted_to"] == "ACT_DR6_BASELINE_LCDM_PREDICTION_VECTOR"
    assert data["still_missing_objects_after_this_record"] == [
        "ACT_DR6_BASELINE_LCDM_PREDICTION_VECTOR",
        "ACT_DR6_DFM_MKC_PREDICTION_VECTOR",
    ]
    assert data["next_admissible_object"] == "ACT_DR6_BASELINE_LCDM_OFFICIAL_BEST_FIT_VECTOR_EXTRACTION_HARNESS"
    assert data["physical_dark_matter_phase_claim_status"] == "HYPOTHESIS_ONLY"
    assert REQUIRED_BOUNDARIES <= set(data["does_not_prove"])

    for source in REQUIRED_SOURCES:
        assert data["official_sources"][source].get("url")
        assert source in doc, source

    for token in (
        REQUIRED_SOURCES
        | REQUIRED_BOUNDARIES
        | {
            "OFFICIAL_ACT_DR6_BASELINE_LCDM_THEORY_VECTOR_PROVENANCE_CERTIFICATE",
            "BASELINE_LCDM_PROVENANCE_CERTIFIED_VECTOR_EXTRACTION_READY_NO_VECTOR_PROMOTION",
            "ACT_DR6_BASELINE_LCDM_PREDICTION_VECTOR",
            "ACT_DR6_BASELINE_LCDM_OFFICIAL_BEST_FIT_VECTOR_EXTRACTION_HARNESS",
            "SOURCE_CLASS_SEPARATION_CERTIFIED_FOR_OFFICIAL_SOURCE",
            "ACT_DR6_DFM_MKC_PREDICTION_VECTOR",
            "HYPOTHESIS_ONLY",
        }
    ):
        assert token in doc, token

    print("ACT_DR6_BASELINE_LCDM_OFFICIAL_SOURCE_PROVENANCE_READINESS_OK")

if __name__ == "__main__":
    main()
