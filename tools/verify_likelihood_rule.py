#!/usr/bin/env python3
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SCHEMA = ROOT / "specs" / "DATA_VECTOR_SCHEMA.json"
COV = ROOT / "specs" / "COVARIANCE_MATRIX.json"
LIKE = ROOT / "specs" / "LIKELIHOOD_RULE.json"
ART = ROOT / "artifacts" / "repo_intake" / "likelihood_rule_2026_05_22.json"
DOC = ROOT / "docs" / "status" / "LIKELIHOOD_RULE_2026_05_22.md"

def load(path):
    if not path.exists():
        raise AssertionError(f"missing file: {path}")
    return json.loads(path.read_text())

def main():
    schema = load(SCHEMA)
    cov = load(COV)
    like = load(LIKE)
    art = load(ART)
    doc = DOC.read_text()

    if schema["object_id"] != "DATA_VECTOR_SCHEMA":
        raise AssertionError("missing schema input")
    if cov["object_id"] != "COVARIANCE_MATRIX":
        raise AssertionError("missing covariance input")
    if like["object_id"] != "LIKELIHOOD_RULE":
        raise AssertionError("wrong likelihood object")
    if like["status"] != "LIKELIHOOD_RULE_SUPPLIED_FORMAL_ONLY_NOT_EXECUTED":
        raise AssertionError("wrong likelihood status")
    if like["check_result"] != "PASS_FORMAL_RULE_ONLY":
        raise AssertionError("wrong check result")

    policy = like["likelihood_policy"]
    if policy["formal_rule_supplied"] is not True:
        raise AssertionError("formal rule must be supplied")
    if policy["gaussian_chi_square_rule"] is not True:
        raise AssertionError("Gaussian chi-square rule must be true")
    for key in ["executed", "empirical_data_bound", "lambda_cdm_baseline_bound", "model_selection_claimed"]:
        if policy[key] is not False:
            raise AssertionError(f"{key} must be false")

    for key in ["residual", "chi_square", "log_likelihood", "comparison_statistic"]:
        if key not in like["rule"]:
            raise AssertionError(f"missing rule key: {key}")

    if "C^{-1}" not in like["rule"]["chi_square"]:
        raise AssertionError("chi-square rule missing inverse covariance")

    if like["likelihood_rule_supplied"] is not True:
        raise AssertionError("likelihood_rule_supplied must be true")

    for flag in [
        "likelihood_executed",
        "empirical_values_supplied",
        "lambda_cdm_baseline_supplied",
        "empirical_validation_claimed",
        "model_selection_claimed",
    ]:
        if like[flag] is not False:
            raise AssertionError(f"{flag} must be false")

    if art["root_blocker_removed"] != "LIKELIHOOD_RULE_NOT_SUPPLIED":
        raise AssertionError("wrong removed blocker")
    if art["new_root_blocker"] != "LAMBDA_CDM_BASELINE_VECTOR_NOT_SUPPLIED":
        raise AssertionError("wrong new blocker")

    for phrase in [
        "does not execute the likelihood rule",
        "does not bind empirical data values",
        "does not bind a Lambda-CDM baseline vector",
        "does not supply empirical evidence",
    ]:
        if phrase not in art["boundary"]:
            raise AssertionError(f"artifact missing boundary phrase: {phrase}")

    for phrase in [
        "Status: `LIKELIHOOD_RULE_SUPPLIED_FORMAL_ONLY_NOT_EXECUTED`",
        "`LIKELIHOOD_RULE_NOT_SUPPLIED`",
        "`LAMBDA_CDM_BASELINE_VECTOR_NOT_SUPPLIED`",
        "any Clay problem",
    ]:
        if phrase not in doc:
            raise AssertionError(f"doc missing phrase: {phrase}")

    print("Likelihood rule verification OK.")
    print("Status: LIKELIHOOD_RULE_SUPPLIED_FORMAL_ONLY_NOT_EXECUTED")
    print("Check result: PASS_FORMAL_RULE_ONLY")
    print("New root blocker: LAMBDA_CDM_BASELINE_VECTOR_NOT_SUPPLIED")

if __name__ == "__main__":
    main()
