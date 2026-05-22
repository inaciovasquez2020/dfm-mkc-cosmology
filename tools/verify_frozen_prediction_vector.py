#!/usr/bin/env python3
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
ACTION_SPEC = ROOT / "specs" / "SUPPLIED_DFM_FIELD_EQUATIONS_AND_ACTION_FUNCTIONAL.json"
VARIATIONAL_SPEC = ROOT / "specs" / "VARIATIONAL_DERIVATION_CHECK.json"
PARAM_SPEC = ROOT / "specs" / "PARAMETER_DOMAIN_AND_UNITS_TABLE.json"
ANSATZ_SPEC = ROOT / "specs" / "COSMOLOGICAL_REDUCTION_ANSATZ.json"
VECTOR_SPEC = ROOT / "specs" / "FROZEN_PREDICTION_VECTOR.json"
ARTIFACT = ROOT / "artifacts" / "repo_intake" / "frozen_prediction_vector_2026_05_22.json"
DOC = ROOT / "docs" / "status" / "FROZEN_PREDICTION_VECTOR_2026_05_22.md"

EXPECTED_VECTOR_ORDER = [
    "E_DFM(z)",
    "D_A_DFM(z)",
    "D_L_DFM(z)",
    "mu_DFM(z)",
    "f_sigma8_DFM(z)",
    "C_ell_TT_DFM",
    "C_ell_TE_DFM",
    "C_ell_EE_DFM",
    "S8_DFM",
    "r_d_DFM",
]

REQUIRED_EXECUTION_INPUTS = [
    "DERIVED_REDUCED_BACKGROUND_EQUATIONS",
    "PERTURBATION_CLOSURE_EQUATIONS",
    "NUMERICAL_PARAMETER_VECTOR",
    "INITIAL_CONDITIONS",
    "OBSERVABLE_EVALUATION_GRID",
    "DATA_VECTOR_SCHEMA",
    "COVARIANCE_MATRIX",
    "LIKELIHOOD_RULE",
]

REQUIRED_BOUNDARY = [
    "does not supply numerical prediction values",
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
    "EXECUTED_DFM_VS_LAMBDA_CDM_COMPARISON",
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
    artifact = load_json(ARTIFACT)

    if not DOC.exists():
        raise AssertionError(f"missing file: {DOC}")
    doc = DOC.read_text()

    expected_inputs = {
        "FILLED_SUPPLIED_DFM_FIELD_EQUATIONS_AND_ACTION_FUNCTIONAL": action,
        "VARIATIONAL_DERIVATION_CHECK": variation,
        "PARAMETER_DOMAIN_AND_UNITS_TABLE": params,
        "COSMOLOGICAL_REDUCTION_ANSATZ": ansatz,
    }
    for object_id, data in expected_inputs.items():
        if data.get("object_id") != object_id:
            raise AssertionError(f"input object mismatch for {object_id}")

    if vector.get("object_id") != "FROZEN_PREDICTION_VECTOR":
        raise AssertionError("wrong vector object_id")

    if vector.get("status") != "FROZEN_PREDICTION_VECTOR_SUPPLIED_SYMBOLIC_ONLY_NOT_EXECUTABLE":
        raise AssertionError("wrong vector status")

    if vector.get("check_result") != "PASS_STRUCTURAL_ONLY":
        raise AssertionError("wrong vector check_result")

    freeze = vector.get("freeze_policy", {})
    for key in [
        "vector_order_locked",
        "observable_names_locked",
        "symbolic_definitions_locked",
    ]:
        if freeze.get(key) is not True:
            raise AssertionError(f"{key} must be true")

    for key in [
        "numerical_values_supplied",
        "covariance_matrix_supplied",
        "likelihood_rule_supplied",
    ]:
        if freeze.get(key) is not False:
            raise AssertionError(f"{key} must be false")

    if vector.get("observable_vector_order") != EXPECTED_VECTOR_ORDER:
        raise AssertionError("observable vector order mismatch")

    definitions = vector.get("observable_definitions", [])
    if len(definitions) != len(EXPECTED_VECTOR_ORDER):
        raise AssertionError("observable definition count mismatch")

    for expected_index, expected_name in enumerate(EXPECTED_VECTOR_ORDER):
        item = definitions[expected_index]
        if item.get("index") != expected_index:
            raise AssertionError(f"wrong index at position {expected_index}")
        if item.get("name") != expected_name:
            raise AssertionError(f"wrong name at position {expected_index}")
        if not item.get("definition"):
            raise AssertionError(f"missing definition at position {expected_index}")
        if not item.get("depends_on"):
            raise AssertionError(f"missing dependencies at position {expected_index}")
        if item.get("numerical_value_supplied") is not False:
            raise AssertionError(f"numerical value supplied at position {expected_index}")

    assert_contains_all(vector.get("required_execution_inputs", []), REQUIRED_EXECUTION_INPUTS, "required execution inputs")

    for flag in [
        "numerical_prediction_claimed",
        "covariance_matrix_claimed",
        "likelihood_execution_claimed",
        "empirical_validation_claimed",
        "physical_correctness_claimed",
    ]:
        if vector.get(flag) is not False:
            raise AssertionError(f"{flag} must be false")

    ansatz_targets = {item["target_id"] for item in ansatz.get("background_equation_targets", [])}
    for required_target in [
        "friedmann_constraint_target",
        "acceleration_equation_target",
        "scalar_background_equation_target",
        "vector_background_constraint_target",
        "matter_background_equation_target",
    ]:
        if required_target not in ansatz_targets:
            raise AssertionError(f"ansatz missing target needed before prediction vector: {required_target}")

    assert_contains_all(vector["does_not_prove"], REQUIRED_DOES_NOT_PROVE, "vector does_not_prove")
    assert_contains_all(vector["next_missing_objects"], REQUIRED_NEXT, "vector next_missing_objects")

    if artifact.get("required_object_filled") != "FROZEN_PREDICTION_VECTOR":
        raise AssertionError("artifact required object mismatch")

    if artifact.get("root_blocker_removed") != "FROZEN_PREDICTION_VECTOR_NOT_SUPPLIED":
        raise AssertionError("wrong removed blocker")

    if artifact.get("new_root_blocker") != "EXECUTED_DFM_VS_LAMBDA_CDM_COMPARISON_NOT_SUPPLIED":
        raise AssertionError("wrong new blocker")

    if artifact.get("check_result") != "PASS_STRUCTURAL_ONLY":
        raise AssertionError("artifact check result mismatch")

    assert_contains_all(artifact["boundary"], REQUIRED_BOUNDARY, "artifact boundary")
    assert_contains_all(artifact["does_not_prove"], REQUIRED_DOES_NOT_PROVE, "artifact does_not_prove")
    assert_contains_all(artifact["next_missing_objects"], REQUIRED_NEXT, "artifact next_missing_objects")

    for phrase in [
        "Status: `FROZEN_PREDICTION_VECTOR_SUPPLIED_SYMBOLIC_ONLY_NOT_EXECUTABLE`",
        "`FROZEN_PREDICTION_VECTOR`",
        "`FROZEN_PREDICTION_VECTOR_NOT_SUPPLIED`",
        "`EXECUTED_DFM_VS_LAMBDA_CDM_COMPARISON_NOT_SUPPLIED`",
        "`PASS_STRUCTURAL_ONLY`",
        "does not supply numerical prediction values",
        "does not supply empirical evidence",
        "any Clay problem",
    ]:
        if phrase not in doc:
            raise AssertionError(f"doc missing phrase: {phrase}")

    print("Frozen prediction vector verification OK.")
    print("Status: FROZEN_PREDICTION_VECTOR_SUPPLIED_SYMBOLIC_ONLY_NOT_EXECUTABLE")
    print("Check result: PASS_STRUCTURAL_ONLY")
    print("New root blocker: EXECUTED_DFM_VS_LAMBDA_CDM_COMPARISON_NOT_SUPPLIED")

if __name__ == "__main__":
    main()
