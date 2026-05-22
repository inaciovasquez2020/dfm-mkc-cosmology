#!/usr/bin/env python3
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
ACTION_SPEC = ROOT / "specs" / "SUPPLIED_DFM_FIELD_EQUATIONS_AND_ACTION_FUNCTIONAL.json"
VARIATIONAL_SPEC = ROOT / "specs" / "VARIATIONAL_DERIVATION_CHECK.json"
PARAM_SPEC = ROOT / "specs" / "PARAMETER_DOMAIN_AND_UNITS_TABLE.json"
ANSATZ_SPEC = ROOT / "specs" / "COSMOLOGICAL_REDUCTION_ANSATZ.json"
VECTOR_SPEC = ROOT / "specs" / "FROZEN_PREDICTION_VECTOR.json"
COMPARISON_SPEC = ROOT / "specs" / "EXECUTED_DFM_VS_LAMBDA_CDM_COMPARISON.json"
ARTIFACT = ROOT / "artifacts" / "repo_intake" / "executed_dfm_vs_lambda_cdm_comparison_2026_05_22.json"
DOC = ROOT / "docs" / "status" / "EXECUTED_DFM_VS_LAMBDA_CDM_COMPARISON_2026_05_22.md"

REQUIRED_PRECONDITIONS = [
    "DERIVED_REDUCED_BACKGROUND_EQUATIONS",
    "PERTURBATION_CLOSURE_EQUATIONS",
    "NUMERICAL_PARAMETER_VECTOR",
    "INITIAL_CONDITIONS",
    "OBSERVABLE_EVALUATION_GRID",
    "DATA_VECTOR_SCHEMA",
    "COVARIANCE_MATRIX",
    "LIKELIHOOD_RULE",
    "LAMBDA_CDM_BASELINE_VECTOR",
]

REQUIRED_BOUNDARY = [
    "does not execute a numerical comparison",
    "does not evaluate numerical predictions",
    "does not supply a data vector",
    "does not supply a covariance matrix",
    "does not supply a likelihood rule",
    "does not supply a Lambda-CDM baseline vector",
    "does not supply empirical evidence",
]

REQUIRED_DOES_NOT_PROVE = [
    "DFM-MKC",
    "Lambda-CDM failure",
    "dark-energy resolution",
    "dark-matter resolution",
    "Nobel-level physical discovery",
    "any Clay problem",
]

REQUIRED_NEXT = [
    "DERIVED_REDUCED_BACKGROUND_EQUATIONS",
    "PERTURBATION_CLOSURE_EQUATIONS",
    "NUMERICAL_PARAMETER_VECTOR",
    "DATA_VECTOR_SCHEMA",
    "COVARIANCE_MATRIX",
    "LIKELIHOOD_RULE",
    "LAMBDA_CDM_BASELINE_VECTOR",
    "INDEPENDENT_EMPIRICAL_VALIDATION",
]

def load_json(path: Path) -> dict:
    if not path.exists():
        raise AssertionError(f"missing file: {path}")
    return json.loads(path.read_text())

def assert_contains_all(container, required, label):
    missing = [item for item in required if item not in container]
    if missing:
        raise AssertionError(f"{label} missing: {missing}")

def main() -> None:
    action = load_json(ACTION_SPEC)
    variation = load_json(VARIATIONAL_SPEC)
    params = load_json(PARAM_SPEC)
    ansatz = load_json(ANSATZ_SPEC)
    vector = load_json(VECTOR_SPEC)
    comparison = load_json(COMPARISON_SPEC)
    artifact = load_json(ARTIFACT)

    if not DOC.exists():
        raise AssertionError(f"missing file: {DOC}")
    doc = DOC.read_text()

    expected_inputs = {
        "FILLED_SUPPLIED_DFM_FIELD_EQUATIONS_AND_ACTION_FUNCTIONAL": action,
        "VARIATIONAL_DERIVATION_CHECK": variation,
        "PARAMETER_DOMAIN_AND_UNITS_TABLE": params,
        "COSMOLOGICAL_REDUCTION_ANSATZ": ansatz,
        "FROZEN_PREDICTION_VECTOR": vector,
    }
    for object_id, data in expected_inputs.items():
        if data.get("object_id") != object_id:
            raise AssertionError(f"input object mismatch for {object_id}")

    if vector.get("status") != "FROZEN_PREDICTION_VECTOR_SUPPLIED_SYMBOLIC_ONLY_NOT_EXECUTABLE":
        raise AssertionError("frozen vector must remain symbolic-only")

    freeze = vector.get("freeze_policy", {})
    for key in [
        "numerical_values_supplied",
        "covariance_matrix_supplied",
        "likelihood_rule_supplied",
    ]:
        if freeze.get(key) is not False:
            raise AssertionError(f"frozen vector incorrectly supplies {key}")

    if comparison.get("object_id") != "EXECUTED_DFM_VS_LAMBDA_CDM_COMPARISON":
        raise AssertionError("wrong comparison object_id")

    if comparison.get("status") != "EXECUTION_BLOCKED_SYMBOLIC_VECTOR_ONLY_NO_NUMERICAL_COMPARISON":
        raise AssertionError("wrong comparison status")

    if comparison.get("check_result") != "BLOCKED_REQUIRED_INPUTS_NOT_SUPPLIED":
        raise AssertionError("wrong comparison check_result")

    target = comparison.get("comparison_target", {})
    if target.get("model_a") != "DFM-MKC":
        raise AssertionError("model_a mismatch")
    if target.get("model_b") != "Lambda-CDM":
        raise AssertionError("model_b mismatch")

    preconditions = comparison.get("execution_preconditions", [])
    precondition_names = [item.get("object") for item in preconditions]
    assert_contains_all(precondition_names, REQUIRED_PRECONDITIONS, "execution preconditions")

    for item in preconditions:
        if item.get("status") != "missing":
            raise AssertionError(f"precondition must remain missing: {item}")
        if not item.get("required_for"):
            raise AssertionError(f"precondition missing required_for: {item}")

    for flag in [
        "comparison_executed",
        "numerical_predictions_evaluated",
        "data_vector_supplied",
        "covariance_matrix_supplied",
        "likelihood_rule_supplied",
        "lambda_cdm_baseline_supplied",
        "empirical_validation_claimed",
        "model_selection_claimed",
    ]:
        if comparison.get(flag) is not False:
            raise AssertionError(f"{flag} must be false")

    blocked_statement = comparison.get("blocked_execution_statement", "")
    for token in [
        "cannot be executed",
        "symbolic-only",
        "covariance matrix",
        "likelihood rule",
        "Lambda-CDM baseline vector",
    ]:
        if token not in blocked_statement:
            raise AssertionError(f"blocked statement missing token: {token}")

    assert_contains_all(comparison["does_not_prove"], REQUIRED_DOES_NOT_PROVE, "comparison does_not_prove")
    assert_contains_all(comparison["next_missing_objects"], REQUIRED_NEXT, "comparison next_missing_objects")

    if artifact.get("required_object_blocked") != "EXECUTED_DFM_VS_LAMBDA_CDM_COMPARISON":
        raise AssertionError("artifact blocked object mismatch")

    if artifact.get("root_blocker_preserved") != "EXECUTED_DFM_VS_LAMBDA_CDM_COMPARISON_NOT_SUPPLIED":
        raise AssertionError("wrong preserved blocker")

    if artifact.get("new_root_blocker") != "NUMERICAL_COMPARISON_EXECUTION_INPUTS_NOT_SUPPLIED":
        raise AssertionError("wrong new blocker")

    if artifact.get("check_result") != "BLOCKED_REQUIRED_INPUTS_NOT_SUPPLIED":
        raise AssertionError("artifact check result mismatch")

    assert_contains_all(artifact["boundary"], REQUIRED_BOUNDARY, "artifact boundary")
    assert_contains_all(artifact["does_not_prove"], REQUIRED_DOES_NOT_PROVE, "artifact does_not_prove")
    assert_contains_all(artifact["next_missing_objects"], REQUIRED_NEXT, "artifact next_missing_objects")

    for phrase in [
        "Status: `EXECUTION_BLOCKED_SYMBOLIC_VECTOR_ONLY_NO_NUMERICAL_COMPARISON`",
        "`EXECUTED_DFM_VS_LAMBDA_CDM_COMPARISON`",
        "`EXECUTED_DFM_VS_LAMBDA_CDM_COMPARISON_NOT_SUPPLIED`",
        "`NUMERICAL_COMPARISON_EXECUTION_INPUTS_NOT_SUPPLIED`",
        "`BLOCKED_REQUIRED_INPUTS_NOT_SUPPLIED`",
        "does not execute a numerical comparison",
        "does not supply empirical evidence",
        "any Clay problem",
    ]:
        if phrase not in doc:
            raise AssertionError(f"doc missing phrase: {phrase}")

    print("Executed DFM-MKC vs Lambda-CDM comparison gate verification OK.")
    print("Status: EXECUTION_BLOCKED_SYMBOLIC_VECTOR_ONLY_NO_NUMERICAL_COMPARISON")
    print("Check result: BLOCKED_REQUIRED_INPUTS_NOT_SUPPLIED")
    print("New root blocker: NUMERICAL_COMPARISON_EXECUTION_INPUTS_NOT_SUPPLIED")

if __name__ == "__main__":
    main()
