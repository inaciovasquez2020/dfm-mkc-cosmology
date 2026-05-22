#!/usr/bin/env python3
import json
import math
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SCHEMA = ROOT / "specs" / "DATA_VECTOR_SCHEMA.json"
COV = ROOT / "specs" / "COVARIANCE_MATRIX.json"
ART = ROOT / "artifacts" / "repo_intake" / "covariance_matrix_2026_05_22.json"
DOC = ROOT / "docs" / "status" / "COVARIANCE_MATRIX_2026_05_22.md"

REQUIRED_BOUNDARY = [
    "does not supply empirical covariance",
    "does not bind covariance to an external payload",
    "does not supply a likelihood rule",
    "does not execute a likelihood comparison",
    "does not supply empirical evidence",
]

REQUIRED_DNP = [
    "DFM-MKC",
    "Lambda-CDM failure",
    "dark-energy resolution",
    "dark-matter resolution",
    "Nobel-level physical discovery",
    "any Clay problem",
]

def load(path):
    if not path.exists():
        raise AssertionError(f"missing file: {path}")
    return json.loads(path.read_text())

def contains_all(container, required, label):
    missing = [x for x in required if x not in container]
    if missing:
        raise AssertionError(f"{label} missing: {missing}")

def main():
    schema = load(SCHEMA)
    cov = load(COV)
    art = load(ART)
    doc = DOC.read_text()

    if schema["object_id"] != "DATA_VECTOR_SCHEMA":
        raise AssertionError("missing data vector schema input")

    if cov["object_id"] != "COVARIANCE_MATRIX":
        raise AssertionError("wrong covariance object")

    if cov["status"] != "COVARIANCE_MATRIX_SUPPLIED_REFERENCE_DIAGONAL_ONLY_NOT_EMPIRICAL":
        raise AssertionError("wrong covariance status")

    if cov["check_result"] != "PASS_REFERENCE_DIAGONAL_MATRIX_ONLY":
        raise AssertionError("wrong check result")

    slot_order = schema["data_vector_slot_order"]
    if cov["covariance_slot_order"] != slot_order:
        raise AssertionError("covariance slot order mismatch")

    variances = cov["diagonal_variances"]
    if len(variances) != len(slot_order):
        raise AssertionError("variance dimension mismatch")

    if cov["matrix_dimension"] != len(slot_order):
        raise AssertionError("matrix dimension mismatch")

    for value in variances:
        if not isinstance(value, (int, float)) or not math.isfinite(value) or value <= 0:
            raise AssertionError("all variances must be finite positive numbers")

    policy = cov["matrix_policy"]
    if policy["reference_diagonal_only"] is not True:
        raise AssertionError("reference diagonal policy must be true")
    if policy["empirical_covariance"] is not False:
        raise AssertionError("empirical covariance must be false")
    if policy["payload_bound"] is not False:
        raise AssertionError("payload bound must be false")
    if policy["likelihood_ready"] is not False:
        raise AssertionError("likelihood ready must be false")

    for flag in [
        "covariance_matrix_supplied"
    ]:
        if cov[flag] is not True:
            raise AssertionError(f"{flag} must be true")

    for flag in [
        "empirical_covariance_claimed",
        "likelihood_rule_supplied",
        "lambda_cdm_baseline_supplied",
        "empirical_validation_claimed",
        "model_selection_claimed",
    ]:
        if cov[flag] is not False:
            raise AssertionError(f"{flag} must be false")

    if art["root_blocker_removed"] != "COVARIANCE_MATRIX_NOT_SUPPLIED":
        raise AssertionError("wrong removed blocker")
    if art["new_root_blocker"] != "LIKELIHOOD_RULE_NOT_SUPPLIED":
        raise AssertionError("wrong new blocker")

    contains_all(art["boundary"], REQUIRED_BOUNDARY, "artifact boundary")
    contains_all(art["does_not_prove"], REQUIRED_DNP, "artifact does_not_prove")
    contains_all(cov["does_not_prove"], REQUIRED_DNP, "spec does_not_prove")

    for phrase in [
        "Status: `COVARIANCE_MATRIX_SUPPLIED_REFERENCE_DIAGONAL_ONLY_NOT_EMPIRICAL`",
        "`COVARIANCE_MATRIX_NOT_SUPPLIED`",
        "`LIKELIHOOD_RULE_NOT_SUPPLIED`",
        "does not supply empirical covariance",
        "any Clay problem",
    ]:
        if phrase not in doc:
            raise AssertionError(f"doc missing phrase: {phrase}")

    print("Covariance matrix verification OK.")
    print("Status: COVARIANCE_MATRIX_SUPPLIED_REFERENCE_DIAGONAL_ONLY_NOT_EMPIRICAL")
    print("Check result: PASS_REFERENCE_DIAGONAL_MATRIX_ONLY")
    print("New root blocker: LIKELIHOOD_RULE_NOT_SUPPLIED")

if __name__ == "__main__":
    main()
