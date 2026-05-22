#!/usr/bin/env python3
import json
import math
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SCHEMA = ROOT / "specs" / "DATA_VECTOR_SCHEMA.json"
LIKE = ROOT / "specs" / "LIKELIHOOD_RULE.json"
BASE = ROOT / "specs" / "LAMBDA_CDM_BASELINE_VECTOR.json"
ART = ROOT / "artifacts" / "repo_intake" / "lambda_cdm_baseline_vector_2026_05_22.json"
DOC = ROOT / "docs" / "status" / "LAMBDA_CDM_BASELINE_VECTOR_2026_05_22.md"

def load(path):
    if not path.exists():
        raise AssertionError(f"missing file: {path}")
    return json.loads(path.read_text())

def main():
    schema = load(SCHEMA)
    like = load(LIKE)
    base = load(BASE)
    art = load(ART)
    doc = DOC.read_text()

    if schema["object_id"] != "DATA_VECTOR_SCHEMA":
        raise AssertionError("missing schema input")
    if like["object_id"] != "LIKELIHOOD_RULE":
        raise AssertionError("missing likelihood input")
    if base["object_id"] != "LAMBDA_CDM_BASELINE_VECTOR":
        raise AssertionError("wrong baseline object")
    if base["status"] != "LAMBDA_CDM_BASELINE_VECTOR_SUPPLIED_REFERENCE_ONLY_NOT_EMPIRICAL":
        raise AssertionError("wrong baseline status")
    if base["check_result"] != "PASS_REFERENCE_BASELINE_ONLY":
        raise AssertionError("wrong check result")

    if base["baseline_slot_order"] != schema["data_vector_slot_order"]:
        raise AssertionError("baseline slot order mismatch")

    if len(base["baseline_values"]) != len(base["baseline_slot_order"]):
        raise AssertionError("baseline dimension mismatch")

    for value in base["baseline_values"]:
        if not isinstance(value, (int, float)) or not math.isfinite(value):
            raise AssertionError("baseline values must be finite")

    policy = base["baseline_policy"]
    for key in ["reference_baseline_only", "slot_order_locked", "matches_data_vector_schema"]:
        if policy[key] is not True:
            raise AssertionError(f"{key} must be true")
    for key in ["fit_to_data", "best_fit_claimed", "external_payload_bound", "model_selection_claimed"]:
        if policy[key] is not False:
            raise AssertionError(f"{key} must be false")

    if base["lambda_cdm_baseline_supplied"] is not True:
        raise AssertionError("lambda baseline must be supplied")
    for flag in ["fit_to_data", "best_fit_claimed", "empirical_validation_claimed", "model_selection_claimed"]:
        if base[flag] is not False:
            raise AssertionError(f"{flag} must be false")

    if art["root_blocker_removed"] != "LAMBDA_CDM_BASELINE_VECTOR_NOT_SUPPLIED":
        raise AssertionError("wrong removed blocker")
    if art["new_root_blocker"] != "INDEPENDENT_EMPIRICAL_VALIDATION_NOT_SUPPLIED":
        raise AssertionError("wrong new blocker")

    for phrase in [
        "does not claim the baseline is fit to data",
        "does not claim a best-fit Lambda-CDM solution",
        "does not execute model selection",
        "does not supply empirical evidence",
    ]:
        if phrase not in art["boundary"]:
            raise AssertionError(f"artifact missing boundary phrase: {phrase}")

    for phrase in [
        "Status: `LAMBDA_CDM_BASELINE_VECTOR_SUPPLIED_REFERENCE_ONLY_NOT_EMPIRICAL`",
        "`LAMBDA_CDM_BASELINE_VECTOR_NOT_SUPPLIED`",
        "`INDEPENDENT_EMPIRICAL_VALIDATION_NOT_SUPPLIED`",
        "any Clay problem",
    ]:
        if phrase not in doc:
            raise AssertionError(f"doc missing phrase: {phrase}")

    print("Lambda-CDM baseline vector verification OK.")
    print("Status: LAMBDA_CDM_BASELINE_VECTOR_SUPPLIED_REFERENCE_ONLY_NOT_EMPIRICAL")
    print("Check result: PASS_REFERENCE_BASELINE_ONLY")
    print("New root blocker: INDEPENDENT_EMPIRICAL_VALIDATION_NOT_SUPPLIED")

if __name__ == "__main__":
    main()
