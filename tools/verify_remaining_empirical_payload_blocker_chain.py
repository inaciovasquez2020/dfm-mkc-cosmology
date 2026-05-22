#!/usr/bin/env python3
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

OBJECTS = [
    "AUTHENTIC_EXTERNAL_DATA_PAYLOAD",
    "PAYLOAD_SLOT_BINDING_MAP",
    "PAYLOAD_DIGEST_LOCK",
    "EMPIRICAL_VALUE_ARRAY",
    "EMPIRICAL_UNCERTAINTY_ARRAY",
    "BACKGROUND_NUMERICAL_SOLVER_RUN",
    "PERTURBATION_NUMERICAL_SOLVER_RUN",
    "TRANSFER_FUNCTION_SOLVER_RUN",
    "PREDICTION_VALUE_ARRAY",
    "PREDICTION_RUN_DIGEST_LOCK",
    "PAYLOAD_COVARIANCE_ARRAY",
    "PAYLOAD_COVARIANCE_SLOT_ORDER",
    "PAYLOAD_COVARIANCE_DIGEST_LOCK",
    "PAYLOAD_COVARIANCE_POSITIVE_DEFINITE_CHECK",
    "DFM_CHI_SQUARE_VALUE",
    "LAMBDA_CDM_CHI_SQUARE_VALUE",
    "DELTA_CHI_SQUARE_VALUE",
    "EXECUTED_LIKELIHOOD_DIGEST_LOCK",
    "HOLDOUT_PAYLOAD_DIGEST_LOCK",
    "REPRODUCTION_COMMANDS",
    "REPRODUCTION_LOG",
    "CLAIM_BOUNDARY_AUDIT",
]

REQUIRED_INPUTS = [
    "DATA_VECTOR_SCHEMA",
    "COVARIANCE_MATRIX",
    "LIKELIHOOD_RULE",
    "LAMBDA_CDM_BASELINE_VECTOR",
    "INDEPENDENT_EMPIRICAL_VALIDATION",
    "EMPIRICAL_DATA_VALUES",
    "EXECUTABLE_DFM_PREDICTION_VALUES",
    "PAYLOAD_BOUND_COVARIANCE_MATRIX",
    "EXECUTED_LIKELIHOOD_RESULT",
    "REPRODUCIBLE_HOLDOUT_REPORT",
]

DNP = [
    "DFM-MKC",
    "Lambda-CDM failure",
    "dark-energy resolution",
    "dark-matter resolution",
    "Nobel-level physical discovery",
    "any Clay problem",
]

FORBIDDEN_TRUE_FLAGS = [
    "authentic_external_data_payload_supplied",
    "external_payload_bound",
    "empirical_validation_claimed",
    "model_selection_claimed",
    "payload_slot_binding_map_supplied",
    "empirical_values_supplied",
    "payload_digest_lock_supplied",
    "empirical_value_array_supplied",
    "empirical_uncertainty_array_supplied",
    "observational_uncertainties_supplied",
    "background_solver_run_supplied",
    "background_numerical_integration_executed",
    "prediction_values_supplied",
    "perturbation_solver_run_supplied",
    "perturbation_numerical_integration_executed",
    "transfer_function_solver_run_supplied",
    "boltzmann_transfer_executed",
    "cmb_prediction_values_supplied",
    "prediction_value_array_supplied",
    "executable_prediction_values_supplied",
    "likelihood_ready_predictions_supplied",
    "prediction_run_digest_lock_supplied",
    "payload_covariance_array_supplied",
    "payload_bound_covariance_supplied",
    "empirical_covariance_claimed",
    "payload_covariance_slot_order_supplied",
    "payload_covariance_digest_lock_supplied",
    "payload_covariance_positive_definite_check_supplied",
    "positive_definite_payload_covariance_claimed",
    "dfm_chi_square_supplied",
    "likelihood_executed",
    "lambda_cdm_chi_square_supplied",
    "lambda_cdm_failure_claimed",
    "delta_chi_square_supplied",
    "executed_likelihood_digest_lock_supplied",
    "holdout_payload_digest_lock_supplied",
    "holdout_payload_bound",
    "holdout_survival_claimed",
    "reproduction_commands_supplied",
    "pipeline_executable_claimed",
    "reproduction_log_supplied",
    "reproduction_executed",
    "dfm_mkc_validated_claimed",
    "nobel_level_discovery_claimed",
]

def load(path: Path) -> dict:
    if not path.exists():
        raise AssertionError(f"missing file: {path}")
    return json.loads(path.read_text())

def contains_all(container, required, label):
    missing = [x for x in required if x not in container]
    if missing:
        raise AssertionError(f"{label} missing: {missing}")

def main() -> None:
    for obj in REQUIRED_INPUTS:
        data = load(ROOT / "specs" / f"{obj}.json")
        if data.get("object_id") != obj:
            raise AssertionError(f"required input object mismatch: {obj}")

    for obj in OBJECTS:
        slug = obj.lower()
        spec = load(ROOT / "specs" / f"{obj}.json")
        artifact = load(ROOT / "artifacts" / "repo_intake" / f"{slug}_2026_05_22.json")
        doc = (ROOT / "docs" / "status" / f"{obj}_2026_05_22.md").read_text()

        if spec.get("object_id") != obj:
            raise AssertionError(f"{obj}: wrong object_id")
        if not spec.get("status"):
            raise AssertionError(f"{obj}: missing status")
        if not spec.get("check_result"):
            raise AssertionError(f"{obj}: missing check_result")
        if not spec.get("blocking_missing_objects"):
            raise AssertionError(f"{obj}: missing blocking_missing_objects")
        contains_all(spec["does_not_prove"], DNP, f"{obj} does_not_prove")

        for flag in FORBIDDEN_TRUE_FLAGS:
            if flag in spec and spec[flag] is not False:
                raise AssertionError(f"{obj}: {flag} must be false")

        if artifact.get("required_object_blocked") != obj:
            raise AssertionError(f"{obj}: artifact blocked-object mismatch")
        if artifact.get("status") != spec["status"]:
            raise AssertionError(f"{obj}: artifact status mismatch")
        if artifact.get("check_result") != spec["check_result"]:
            raise AssertionError(f"{obj}: artifact check mismatch")
        if not artifact.get("terminal_blocker"):
            raise AssertionError(f"{obj}: artifact missing terminal blocker")
        if not artifact.get("boundary"):
            raise AssertionError(f"{obj}: artifact missing boundary")
        contains_all(artifact["does_not_prove"], DNP, f"{obj} artifact does_not_prove")

        joined_boundary = "\n".join(artifact["boundary"])
        for forbidden in [
            "claims Lambda-CDM failure",
            "claims holdout survival",
            "supplies empirical evidence",
            "executes the likelihood",
            "validates DFM-MKC",
        ]:
            if forbidden in joined_boundary:
                raise AssertionError(f"{obj}: forbidden positive claim in boundary: {forbidden}")

        for phrase in [
            f"Status: `{spec['status']}`",
            f"`{obj}`",
            f"`{spec['check_result']}`",
            "any Clay problem",
        ]:
            if phrase not in doc:
                raise AssertionError(f"{obj}: doc missing phrase {phrase}")

    audit = load(ROOT / "specs" / "CLAIM_BOUNDARY_AUDIT.json")
    for flag in [
        "dfm_mkc_validated_claimed",
        "lambda_cdm_failure_claimed",
        "holdout_survival_claimed",
        "empirical_validation_claimed",
        "model_selection_claimed",
        "nobel_level_discovery_claimed",
    ]:
        if audit[flag] is not False:
            raise AssertionError(f"claim audit flag must remain false: {flag}")

    print("Remaining empirical payload blocker chain verification OK.")
    print("Status: TERMINAL_NO_EMPIRICAL_PAYLOAD_EXECUTION_OR_VALIDATION")
    print("Terminal object: CLAIM_BOUNDARY_AUDIT_SUPPLIED_TERMINAL_NO_EMPIRICAL_CLAIM")

if __name__ == "__main__":
    main()
