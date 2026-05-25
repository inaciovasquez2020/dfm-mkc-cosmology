#!/usr/bin/env python3
import json
from pathlib import Path

ART = Path("artifacts/dfm_mkc/residual_eigenspace_empirical_payload_intake_target_2026_05_25.json")
DOC = Path("docs/status/RESIDUAL_EIGENSPACE_EMPIRICAL_PAYLOAD_INTAKE_TARGET_2026_05_25.md")

REQUIRED_FIELDS = {
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

REQUIRED_CHECKS = {
    "data_vector_is_authentic",
    "covariance_matrix_is_authentic",
    "data_covariance_dimensions_match",
    "covariance_is_symmetric",
    "covariance_is_positive_semidefinite_or_regularized_with_certificate",
    "baseline_prediction_dimensions_match",
    "candidate_prediction_dimensions_match",
    "residual_vectors_constructible",
    "residual_covariance_constructible",
    "residual_eigenspace_diagnostic_runnable",
    "boundary_covariance_failure_guard_passed",
    "independent_reproduction_command_supplied",
}

REQUIRED_BOUNDARIES = {
    "authentic empirical data has been supplied",
    "residual eigenspace empirical test has been run",
    "DFM-MKC empirical validation",
    "Lambda-CDM failure",
    "dark matter is liquid",
    "dark matter is solid",
    "dark matter phase transition is physically real",
    "dark matter resolution",
    "dark energy resolution",
    "ACT validation",
    "DES validation",
    "CMB validation",
    "BAO validation",
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

    assert data["id"] == "RESIDUAL_EIGENSPACE_EMPIRICAL_PAYLOAD_INTAKE_TARGET_2026_05_25"
    assert data["status"] == "EMPIRICAL_PAYLOAD_TARGET_ONLY_NO_DATA_BOUND"
    assert data["object_added"]["id"] == "RESIDUAL_EIGENSPACE_EMPIRICAL_PAYLOAD_INTAKE_TARGET"
    assert data["object_added"]["status"] == "OPEN_TARGET"
    assert data["allowed_empirical_promotion_status_after_success"] == "EMPIRICAL_TEST_READY_NOT_VALIDATED"
    assert data["physical_dark_matter_phase_claim_status"] == "HYPOTHESIS_ONLY"

    assert REQUIRED_FIELDS <= set(data["required_payload_fields"])
    assert REQUIRED_CHECKS <= set(data["required_validation_checks"])
    assert REQUIRED_BOUNDARIES <= set(data["does_not_prove"])

    for token in (
        REQUIRED_FIELDS
        | REQUIRED_CHECKS
        | REQUIRED_BOUNDARIES
        | {
            "RESIDUAL_EIGENSPACE_EMPIRICAL_PAYLOAD_INTAKE_TARGET",
            "EMPIRICAL_PAYLOAD_TARGET_ONLY_NO_DATA_BOUND",
            "EMPIRICAL_TEST_READY_NOT_VALIDATED",
            "HYPOTHESIS_ONLY",
        }
    ):
        assert token in doc, token

    print("RESIDUAL_EIGENSPACE_EMPIRICAL_PAYLOAD_INTAKE_TARGET_OK")

if __name__ == "__main__":
    main()
