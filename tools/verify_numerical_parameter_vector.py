#!/usr/bin/env python3
import json
import math
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
ACTION_SPEC = ROOT / "specs" / "SUPPLIED_DFM_FIELD_EQUATIONS_AND_ACTION_FUNCTIONAL.json"
VARIATIONAL_SPEC = ROOT / "specs" / "VARIATIONAL_DERIVATION_CHECK.json"
PARAM_SPEC = ROOT / "specs" / "PARAMETER_DOMAIN_AND_UNITS_TABLE.json"
ANSATZ_SPEC = ROOT / "specs" / "COSMOLOGICAL_REDUCTION_ANSATZ.json"
VECTOR_SPEC = ROOT / "specs" / "FROZEN_PREDICTION_VECTOR.json"
COMPARISON_SPEC = ROOT / "specs" / "EXECUTED_DFM_VS_LAMBDA_CDM_COMPARISON.json"
BACKGROUND_SPEC = ROOT / "specs" / "DERIVED_REDUCED_BACKGROUND_EQUATIONS.json"
PERTURBATION_SPEC = ROOT / "specs" / "PERTURBATION_CLOSURE_EQUATIONS.json"
NUMERIC_SPEC = ROOT / "specs" / "NUMERICAL_PARAMETER_VECTOR.json"
ARTIFACT = ROOT / "artifacts" / "repo_intake" / "numerical_parameter_vector_2026_05_22.json"
DOC = ROOT / "docs" / "status" / "NUMERICAL_PARAMETER_VECTOR_2026_05_22.md"

EXPECTED_ORDER = [
    "M_Pl",
    "Lambda_0",
    "alpha_phi",
    "m_phi",
    "lambda_phi",
    "alpha_A",
    "m_A",
    "beta_phi_A",
    "xi_phi",
    "xi_A",
    "gamma_m",
]

POSITIVE_PARAMETERS = {"M_Pl", "alpha_phi", "alpha_A"}
NONNEGATIVE_PARAMETERS = {"m_phi", "lambda_phi", "m_A"}

REQUIRED_BOUNDARY = [
    "does not claim the vector is fit to data",
    "does not claim physical calibration",
    "does not supply initial conditions",
    "does not supply an observable evaluation grid",
    "does not supply a data vector",
    "does not supply a covariance matrix",
    "does not supply a likelihood rule",
    "does not execute a likelihood comparison",
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
    "INITIAL_CONDITIONS",
    "OBSERVABLE_EVALUATION_GRID",
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
    background = load_json(BACKGROUND_SPEC)
    perturbation = load_json(PERTURBATION_SPEC)
    numeric = load_json(NUMERIC_SPEC)
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
        "EXECUTED_DFM_VS_LAMBDA_CDM_COMPARISON": comparison,
        "DERIVED_REDUCED_BACKGROUND_EQUATIONS": background,
        "PERTURBATION_CLOSURE_EQUATIONS": perturbation,
    }
    for object_id, data in expected_inputs.items():
        if data.get("object_id") != object_id:
            raise AssertionError(f"input object mismatch for {object_id}")

    if numeric.get("object_id") != "NUMERICAL_PARAMETER_VECTOR":
        raise AssertionError("wrong numeric object_id")

    if numeric.get("status") != "NUMERICAL_PARAMETER_VECTOR_SUPPLIED_REFERENCE_CANDIDATE_ONLY_NOT_FIT":
        raise AssertionError("wrong numeric status")

    if numeric.get("check_result") != "PASS_REFERENCE_VECTOR_ONLY":
        raise AssertionError("wrong numeric check_result")

    policy = numeric.get("vector_policy", {})
    for key in [
        "parameter_order_locked",
        "numerical_values_supplied",
        "reference_candidate_only",
    ]:
        if policy.get(key) is not True:
            raise AssertionError(f"{key} must be true")

    for key in [
        "fit_to_data",
        "posterior_sample",
        "best_fit_claimed",
        "physical_calibration_claimed",
    ]:
        if policy.get(key) is not False:
            raise AssertionError(f"{key} must be false")

    if numeric.get("parameter_vector_order") != EXPECTED_ORDER:
        raise AssertionError("parameter vector order mismatch")

    parameter_table = params.get("parameter_table", [])
    table_by_symbol = {item["symbol"]: item for item in parameter_table}
    if set(table_by_symbol) != set(EXPECTED_ORDER):
        raise AssertionError("parameter-domain table symbols mismatch expected order")

    values = numeric.get("parameter_values", [])
    if len(values) != len(EXPECTED_ORDER):
        raise AssertionError("parameter value count mismatch")

    for index, symbol in enumerate(EXPECTED_ORDER):
        item = values[index]
        if item.get("index") != index:
            raise AssertionError(f"wrong index for {symbol}")
        if item.get("symbol") != symbol:
            raise AssertionError(f"wrong symbol at index {index}")
        if item.get("mass_dimension") != table_by_symbol[symbol].get("mass_dimension"):
            raise AssertionError(f"mass dimension mismatch for {symbol}")
        value = item.get("value")
        if not isinstance(value, (int, float)) or not math.isfinite(value):
            raise AssertionError(f"value must be finite numeric for {symbol}")
        if symbol in POSITIVE_PARAMETERS and not value > 0:
            raise AssertionError(f"{symbol} must be positive")
        if symbol in NONNEGATIVE_PARAMETERS and not value >= 0:
            raise AssertionError(f"{symbol} must be nonnegative")
        if not item.get("constraint_status"):
            raise AssertionError(f"missing constraint_status for {symbol}")
        if not item.get("selection_rule"):
            raise AssertionError(f"missing selection_rule for {symbol}")

    for flag in [
        "numerical_parameter_vector_supplied",
    ]:
        if numeric.get(flag) is not True:
            raise AssertionError(f"{flag} must be true")

    for flag in [
        "initial_conditions_supplied",
        "observable_evaluation_grid_supplied",
        "data_vector_supplied",
        "covariance_matrix_supplied",
        "likelihood_rule_supplied",
        "lambda_cdm_baseline_supplied",
        "empirical_validation_claimed",
        "model_selection_claimed",
    ]:
        if numeric.get(flag) is not False:
            raise AssertionError(f"{flag} must be false")

    assert_contains_all(numeric["does_not_prove"], REQUIRED_DOES_NOT_PROVE, "numeric does_not_prove")
    assert_contains_all(numeric["next_missing_objects"], REQUIRED_NEXT, "numeric next_missing_objects")

    if artifact.get("required_object_filled") != "NUMERICAL_PARAMETER_VECTOR":
        raise AssertionError("artifact required object mismatch")

    if artifact.get("root_blocker_removed") != "NUMERICAL_PARAMETER_VECTOR_NOT_SUPPLIED":
        raise AssertionError("wrong removed blocker")

    if artifact.get("new_root_blocker") != "INITIAL_CONDITIONS_NOT_SUPPLIED":
        raise AssertionError("wrong new blocker")

    if artifact.get("check_result") != "PASS_REFERENCE_VECTOR_ONLY":
        raise AssertionError("artifact check result mismatch")

    assert_contains_all(artifact["boundary"], REQUIRED_BOUNDARY, "artifact boundary")
    assert_contains_all(artifact["does_not_prove"], REQUIRED_DOES_NOT_PROVE, "artifact does_not_prove")
    assert_contains_all(artifact["next_missing_objects"], REQUIRED_NEXT, "artifact next_missing_objects")

    for phrase in [
        "Status: `NUMERICAL_PARAMETER_VECTOR_SUPPLIED_REFERENCE_CANDIDATE_ONLY_NOT_FIT`",
        "`NUMERICAL_PARAMETER_VECTOR`",
        "`NUMERICAL_PARAMETER_VECTOR_NOT_SUPPLIED`",
        "`INITIAL_CONDITIONS_NOT_SUPPLIED`",
        "`PASS_REFERENCE_VECTOR_ONLY`",
        "does not claim the vector is fit to data",
        "does not supply empirical evidence",
        "any Clay problem",
    ]:
        if phrase not in doc:
            raise AssertionError(f"doc missing phrase: {phrase}")

    print("Numerical parameter vector verification OK.")
    print("Status: NUMERICAL_PARAMETER_VECTOR_SUPPLIED_REFERENCE_CANDIDATE_ONLY_NOT_FIT")
    print("Check result: PASS_REFERENCE_VECTOR_ONLY")
    print("New root blocker: INITIAL_CONDITIONS_NOT_SUPPLIED")

if __name__ == "__main__":
    main()
