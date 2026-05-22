#!/usr/bin/env python3
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

OBJECTS = [
    ("EMPIRICAL_DATA_VALUES", "empirical_data_values_2026_05_22", "EMPIRICAL_DATA_VALUES_BLOCKED_NO_EXTERNAL_PAYLOAD_BOUND", "BLOCKED_NO_EXTERNAL_PAYLOAD_BOUND"),
    ("EXECUTABLE_DFM_PREDICTION_VALUES", "executable_dfm_prediction_values_2026_05_22", "EXECUTABLE_DFM_PREDICTION_VALUES_BLOCKED_NO_NUMERICAL_SOLVER_EXECUTION", "BLOCKED_NO_NUMERICAL_SOLVER_EXECUTION"),
    ("PAYLOAD_BOUND_COVARIANCE_MATRIX", "payload_bound_covariance_matrix_2026_05_22", "PAYLOAD_BOUND_COVARIANCE_MATRIX_BLOCKED_NO_EMPIRICAL_PAYLOAD_BINDING", "BLOCKED_NO_EMPIRICAL_PAYLOAD_BINDING"),
    ("EXECUTED_LIKELIHOOD_RESULT", "executed_likelihood_result_2026_05_22", "EXECUTED_LIKELIHOOD_RESULT_BLOCKED_NO_EMPIRICAL_DATA_OR_PREDICTION_VALUES", "BLOCKED_NO_EMPIRICAL_DATA_OR_PREDICTION_VALUES"),
    ("REPRODUCIBLE_HOLDOUT_REPORT", "reproducible_holdout_report_2026_05_22", "REPRODUCIBLE_HOLDOUT_REPORT_BLOCKED_NO_EXECUTED_LIKELIHOOD_OR_HOLDOUT_PAYLOAD", "BLOCKED_NO_EXECUTED_LIKELIHOOD_OR_HOLDOUT_PAYLOAD"),
]

REQUIRED_INPUTS = [
    "DATA_VECTOR_SCHEMA",
    "COVARIANCE_MATRIX",
    "LIKELIHOOD_RULE",
    "LAMBDA_CDM_BASELINE_VECTOR",
    "INDEPENDENT_EMPIRICAL_VALIDATION",
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
    "empirical_validation_claimed",
    "model_selection_claimed",
    "holdout_survival_claimed",
    "lambda_cdm_failure_claimed",
    "likelihood_executed",
    "empirical_values_supplied",
    "empirical_payload_bound",
    "solver_execution_claimed",
    "executable_prediction_values_supplied",
    "payload_bound_covariance_supplied",
    "empirical_covariance_claimed",
    "dfm_chi_square_supplied",
    "lambda_cdm_chi_square_supplied",
    "delta_chi_square_supplied",
    "reproducible_holdout_report_supplied",
]

def load(path: Path) -> dict:
    if not path.exists():
        raise AssertionError(f"missing file: {path}")
    return json.loads(path.read_text())

def assert_contains(container, required, label):
    missing = [x for x in required if x not in container]
    if missing:
        raise AssertionError(f"{label} missing: {missing}")

def main() -> None:
    for obj in REQUIRED_INPUTS:
        data = load(ROOT / "specs" / f"{obj}.json")
        if data.get("object_id") != obj:
            raise AssertionError(f"input object mismatch: {obj}")

    for obj, artifact_id, status, check in OBJECTS:
        spec = load(ROOT / "specs" / f"{obj}.json")
        artifact = load(ROOT / "artifacts" / "repo_intake" / f"{artifact_id}.json")
        doc = (ROOT / "docs" / "status" / f"{obj}_2026_05_22.md").read_text()

        if spec.get("object_id") != obj:
            raise AssertionError(f"wrong object_id for {obj}")
        if spec.get("status") != status:
            raise AssertionError(f"wrong status for {obj}")
        if spec.get("check_result") != check:
            raise AssertionError(f"wrong check_result for {obj}")

        for flag in FORBIDDEN_TRUE_FLAGS:
            if flag in spec and spec[flag] is not False:
                raise AssertionError(f"{obj}: {flag} must be false")

        assert_contains(spec["does_not_prove"], DNP, f"{obj} does_not_prove")
        if not spec.get("next_missing_objects"):
            raise AssertionError(f"{obj} must keep next missing objects")

        if artifact.get("required_object_blocked") != obj:
            raise AssertionError(f"artifact blocked object mismatch for {obj}")
        if artifact.get("status") != status:
            raise AssertionError(f"artifact status mismatch for {obj}")
        if artifact.get("check_result") != check:
            raise AssertionError(f"artifact check mismatch for {obj}")
        if not artifact.get("boundary"):
            raise AssertionError(f"artifact boundary missing for {obj}")
        assert_contains(artifact["does_not_prove"], DNP, f"{obj} artifact does_not_prove")

        for phrase in [
            f"Status: `{status}`",
            f"`{obj}`",
            f"`{check}`",
            "any Clay problem",
        ]:
            if phrase not in doc:
                raise AssertionError(f"{obj} doc missing phrase: {phrase}")

    terminal = load(ROOT / "specs" / "REPRODUCIBLE_HOLDOUT_REPORT.json")
    if terminal["reproducible_holdout_report_supplied"] is not False:
        raise AssertionError("terminal report must remain unsupplied")
    if terminal["lambda_cdm_failure_claimed"] is not False:
        raise AssertionError("Lambda-CDM failure must remain unclaimed")

    print("Empirical execution terminal chain verification OK.")
    print("Status: TERMINAL_BLOCKED_NO_EMPIRICAL_PAYLOAD_OR_EXECUTION")
    print("Terminal blocker: HOLDOUT_PAYLOAD_AND_EXECUTED_LIKELIHOOD_NOT_SUPPLIED")

if __name__ == "__main__":
    main()
