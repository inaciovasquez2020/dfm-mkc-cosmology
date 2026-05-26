#!/usr/bin/env python3
import json
from pathlib import Path

ART = Path("artifacts/dfm_mkc/act_dr6_empirical_payload_candidate_2026_05_25.json")
DOC = Path("docs/status/ACT_DR6_EMPIRICAL_PAYLOAD_CANDIDATE_2026_05_25.md")

REQUIRED_POINTERS = {
    "act_dr6_data_products",
    "nasa_lambda_act_dr6_02",
    "nasa_lambda_act_dr6_02_chains_info",
    "act_dr6_full_likelihood_code",
    "act_dr6_cmb_only_likelihood_code",
    "act_dr6_notebooks",
    "act_dr6_nersc_chains",
}

REQUIRED_SLOTS = {
    "dataset_id",
    "dataset_release",
    "source_url_or_release_doi",
    "payload_sha256",
    "data_vector_path",
    "covariance_matrix_path",
    "baseline_prediction_vector_path",
    "candidate_prediction_vector_path",
    "nuisance_parameter_table_path",
    "likelihood_configuration_path",
    "reproduction_command",
    "schema_validation_report_path",
}

REQUIRED_BOUNDARIES = {
    "ACT DR6 data has been downloaded",
    "ACT DR6 payload has been verified",
    "ACT DR6 likelihood has been executed",
    "DFM-MKC empirical validation",
    "Lambda-CDM failure",
    "dark matter is liquid",
    "dark matter is solid",
    "dark matter phase transition is physically real",
    "dark matter resolution",
    "dark energy resolution",
    "CMB validation",
    "ACT validation",
    "independent empirical replication",
    "gravity closure",
    "Chronos proof input",
    "Chronos-RR",
    "H4.1/FGL",
    "P vs NP",
    "any Clay problem",
}

def main() -> None:
    assert ART.exists(), ART
    assert DOC.exists(), DOC

    data = json.loads(ART.read_text())
    doc = DOC.read_text()

    assert data["id"] == "ACT_DR6_EMPIRICAL_PAYLOAD_CANDIDATE_2026_05_25"
    assert data["status"] == "EMPIRICAL_PAYLOAD_CANDIDATE_ONLY_NO_DATA_IMPORTED"
    assert data["object_added"]["id"] == "ACT_DR6_EMPIRICAL_PAYLOAD_CANDIDATE"
    assert data["object_added"]["status"] == "SOURCE_POINTER_CANDIDATE"
    assert data["allowed_next_status_after_payload_binding"] == "EMPIRICAL_TEST_READY_NOT_VALIDATED"
    assert data["physical_dark_matter_phase_claim_status"] == "HYPOTHESIS_ONLY"

    assert REQUIRED_POINTERS <= set(data["source_pointers"])
    assert REQUIRED_SLOTS <= set(data["payload_slots_to_fill_later"])
    assert REQUIRED_BOUNDARIES <= set(data["does_not_prove"])

    for token in (
        REQUIRED_SLOTS
        | REQUIRED_BOUNDARIES
        | {
            "ACT_DR6_EMPIRICAL_PAYLOAD_CANDIDATE",
            "EMPIRICAL_PAYLOAD_CANDIDATE_ONLY_NO_DATA_IMPORTED",
            "EMPIRICAL_TEST_READY_NOT_VALIDATED",
            "HYPOTHESIS_ONLY",
            "https://act.princeton.edu/act-dr6-data-products",
            "https://lambda.gsfc.nasa.gov/product/act/act_dr6.02/",
            "https://lambda.gsfc.nasa.gov/product/act/act_dr6.02/act_dr6.02_chains_info.html",
        }
    ):
        assert token in doc, token

    print("ACT_DR6_EMPIRICAL_PAYLOAD_CANDIDATE_OK")

if __name__ == "__main__":
    main()
