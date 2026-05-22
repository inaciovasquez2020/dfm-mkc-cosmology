#!/usr/bin/env python3
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SCHEMA = ROOT / "specs" / "DATA_VECTOR_SCHEMA.json"
COV = ROOT / "specs" / "COVARIANCE_MATRIX.json"
LIKE = ROOT / "specs" / "LIKELIHOOD_RULE.json"
BASE = ROOT / "specs" / "LAMBDA_CDM_BASELINE_VECTOR.json"
VALID = ROOT / "specs" / "INDEPENDENT_EMPIRICAL_VALIDATION.json"
ART = ROOT / "artifacts" / "repo_intake" / "independent_empirical_validation_2026_05_22.json"
DOC = ROOT / "docs" / "status" / "INDEPENDENT_EMPIRICAL_VALIDATION_2026_05_22.md"

def load(path):
    if not path.exists():
        raise AssertionError(f"missing file: {path}")
    return json.loads(path.read_text())

def main():
    schema = load(SCHEMA)
    cov = load(COV)
    like = load(LIKE)
    base = load(BASE)
    valid = load(VALID)
    art = load(ART)
    doc = DOC.read_text()

    if schema["object_id"] != "DATA_VECTOR_SCHEMA":
        raise AssertionError("missing schema input")
    if cov["object_id"] != "COVARIANCE_MATRIX":
        raise AssertionError("missing covariance input")
    if like["object_id"] != "LIKELIHOOD_RULE":
        raise AssertionError("missing likelihood input")
    if base["object_id"] != "LAMBDA_CDM_BASELINE_VECTOR":
        raise AssertionError("missing baseline input")

    if valid["object_id"] != "INDEPENDENT_EMPIRICAL_VALIDATION":
        raise AssertionError("wrong validation object")
    if valid["status"] != "INDEPENDENT_EMPIRICAL_VALIDATION_BLOCKED_NO_EMPIRICAL_PAYLOAD_OR_EXECUTION":
        raise AssertionError("wrong validation status")
    if valid["check_result"] != "BLOCKED_NO_EMPIRICAL_PAYLOAD_OR_EXECUTION":
        raise AssertionError("wrong validation check result")

    policy = valid["validation_policy"]
    for key in [
        "independent_payload_required",
        "external_data_values_required",
        "executed_prediction_pipeline_required",
        "likelihood_execution_required",
        "claim_blocked",
    ]:
        if policy[key] is not True:
            raise AssertionError(f"{key} must be true")
    if policy["validation_executed"] is not False:
        raise AssertionError("validation_executed must be false")

    for flag in [
        "independent_empirical_validation_supplied",
        "empirical_payload_bound",
        "likelihood_executed",
        "holdout_survival_claimed",
        "lambda_cdm_failure_claimed",
        "model_selection_claimed",
    ]:
        if valid[flag] is not False:
            raise AssertionError(f"{flag} must be false")

    for required in [
        "EMPIRICAL_DATA_VALUES",
        "EXECUTABLE_DFM_PREDICTION_VALUES",
        "PAYLOAD_BOUND_COVARIANCE_MATRIX",
        "EXECUTED_LIKELIHOOD_RESULT",
        "REPRODUCIBLE_HOLDOUT_REPORT",
    ]:
        if required not in valid["blocking_missing_objects"]:
            raise AssertionError(f"missing blocker: {required}")

    if art["root_blocker_preserved"] != "INDEPENDENT_EMPIRICAL_VALIDATION_NOT_SUPPLIED":
        raise AssertionError("wrong preserved blocker")
    if art["terminal_blocker"] != "EMPIRICAL_PAYLOAD_AND_EXECUTED_LIKELIHOOD_NOT_SUPPLIED":
        raise AssertionError("wrong terminal blocker")

    for phrase in [
        "does not supply empirical data values",
        "does not execute DFM-MKC predictions",
        "does not execute a likelihood comparison",
        "does not claim holdout survival",
        "does not claim Lambda-CDM failure",
        "does not supply empirical evidence",
    ]:
        if phrase not in art["boundary"]:
            raise AssertionError(f"artifact missing boundary phrase: {phrase}")

    for phrase in [
        "Status: `INDEPENDENT_EMPIRICAL_VALIDATION_BLOCKED_NO_EMPIRICAL_PAYLOAD_OR_EXECUTION`",
        "`INDEPENDENT_EMPIRICAL_VALIDATION_NOT_SUPPLIED`",
        "`EMPIRICAL_PAYLOAD_AND_EXECUTED_LIKELIHOOD_NOT_SUPPLIED`",
        "any Clay problem",
    ]:
        if phrase not in doc:
            raise AssertionError(f"doc missing phrase: {phrase}")

    print("Independent empirical validation gate verification OK.")
    print("Status: INDEPENDENT_EMPIRICAL_VALIDATION_BLOCKED_NO_EMPIRICAL_PAYLOAD_OR_EXECUTION")
    print("Check result: BLOCKED_NO_EMPIRICAL_PAYLOAD_OR_EXECUTION")
    print("Terminal blocker: EMPIRICAL_PAYLOAD_AND_EXECUTED_LIKELIHOOD_NOT_SUPPLIED")

if __name__ == "__main__":
    main()
