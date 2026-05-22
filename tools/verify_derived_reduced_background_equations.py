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
BACKGROUND_SPEC = ROOT / "specs" / "DERIVED_REDUCED_BACKGROUND_EQUATIONS.json"
ARTIFACT = ROOT / "artifacts" / "repo_intake" / "derived_reduced_background_equations_2026_05_22.json"
DOC = ROOT / "docs" / "status" / "DERIVED_REDUCED_BACKGROUND_EQUATIONS_2026_05_22.md"

REQUIRED_EQUATION_IDS = {
    "friedmann_constraint",
    "acceleration_equation",
    "scalar_background_equation",
    "vector_background_constraint",
    "matter_background_continuity",
}

REQUIRED_SOURCE_TARGETS = {
    "friedmann_constraint_target",
    "acceleration_equation_target",
    "scalar_background_equation_target",
    "vector_background_constraint_target",
    "matter_background_equation_target",
}

REQUIRED_SOURCE_EQUATIONS = {
    "metric_equation",
    "scalar_equation",
    "vector_equation",
    "matter_equation",
}

REQUIRED_BOUNDARY = [
    "does not prove a full symbolic derivation",
    "does not supply numerical integration",
    "does not supply perturbation closure equations",
    "does not supply numerical parameter values",
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
    "PERTURBATION_CLOSURE_EQUATIONS",
    "NUMERICAL_PARAMETER_VECTOR",
    "INITIAL_CONDITIONS",
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
    }
    for object_id, data in expected_inputs.items():
        if data.get("object_id") != object_id:
            raise AssertionError(f"input object mismatch for {object_id}")

    if background.get("object_id") != "DERIVED_REDUCED_BACKGROUND_EQUATIONS":
        raise AssertionError("wrong background object_id")

    if background.get("status") != "DERIVED_REDUCED_BACKGROUND_EQUATIONS_SUPPLIED_STRUCTURAL_ONLY_NOT_NUMERICAL":
        raise AssertionError("wrong background status")

    if background.get("check_result") != "PASS_STRUCTURAL_ONLY":
        raise AssertionError("wrong background check_result")

    ansatz_targets = {item["target_id"] for item in ansatz.get("background_equation_targets", [])}
    assert_contains_all(ansatz_targets, REQUIRED_SOURCE_TARGETS, "ansatz background targets")

    supplied_source_equations = set(action.get("field_equations", {}).keys())
    assert_contains_all(supplied_source_equations, REQUIRED_SOURCE_EQUATIONS, "supplied source equations")

    equations = background.get("derived_background_equations", [])
    if len(equations) != 5:
        raise AssertionError("expected five reduced background equation candidates")

    equation_ids = {item.get("equation_id") for item in equations}
    source_targets = {item.get("source_target") for item in equations}
    source_equations = {item.get("source_equation") for item in equations}

    assert_contains_all(equation_ids, REQUIRED_EQUATION_IDS, "reduced equation ids")
    assert_contains_all(source_targets, REQUIRED_SOURCE_TARGETS, "reduced source targets")
    assert_contains_all(source_equations, REQUIRED_SOURCE_EQUATIONS, "reduced source equations")

    for item in equations:
        if item.get("status") != "structural_candidate":
            raise AssertionError(f"equation status must be structural_candidate: {item}")
        if item["source_target"] not in ansatz_targets:
            raise AssertionError(f"source target absent from ansatz: {item}")
        if item["source_equation"] not in supplied_source_equations:
            raise AssertionError(f"source equation absent from action spec: {item}")
        if "= 0" not in item.get("structural_equation", ""):
            raise AssertionError(f"structural equation must contain '= 0': {item}")
        if not item.get("principal_variables"):
            raise AssertionError(f"principal variables missing: {item}")

    auxiliary_symbols = {item["symbol"] for item in background.get("auxiliary_definitions", [])}
    assert_contains_all(auxiliary_symbols, ["H", "R_FLRW", "R00_FLRW", "T_matter", "A_mu_A_mu"], "auxiliary definitions")

    closure_observables = {item["observable"] for item in background.get("closure_for_prediction_vector", [])}
    assert_contains_all(closure_observables, ["E_DFM(z)", "D_A_DFM(z)", "D_L_DFM(z)", "mu_DFM(z)", "r_d_DFM"], "prediction closure observables")

    for flag in [
        "symbolic_derivation_proved",
        "numerical_integration_supplied",
        "perturbation_closure_supplied",
        "parameter_values_supplied",
        "initial_conditions_supplied",
        "empirical_validation_claimed",
        "likelihood_execution_claimed",
    ]:
        if background.get(flag) is not False:
            raise AssertionError(f"{flag} must be false")

    assert_contains_all(background["does_not_prove"], REQUIRED_DOES_NOT_PROVE, "background does_not_prove")
    assert_contains_all(background["next_missing_objects"], REQUIRED_NEXT, "background next_missing_objects")

    if artifact.get("required_object_filled") != "DERIVED_REDUCED_BACKGROUND_EQUATIONS":
        raise AssertionError("artifact required object mismatch")

    if artifact.get("root_blocker_partially_reduced") != "NUMERICAL_COMPARISON_EXECUTION_INPUTS_NOT_SUPPLIED":
        raise AssertionError("wrong partially reduced blocker")

    if artifact.get("new_root_blocker") != "PERTURBATION_CLOSURE_EQUATIONS_NOT_SUPPLIED":
        raise AssertionError("wrong new blocker")

    if artifact.get("check_result") != "PASS_STRUCTURAL_ONLY":
        raise AssertionError("artifact check result mismatch")

    assert_contains_all(artifact["boundary"], REQUIRED_BOUNDARY, "artifact boundary")
    assert_contains_all(artifact["does_not_prove"], REQUIRED_DOES_NOT_PROVE, "artifact does_not_prove")
    assert_contains_all(artifact["next_missing_objects"], REQUIRED_NEXT, "artifact next_missing_objects")

    for phrase in [
        "Status: `DERIVED_REDUCED_BACKGROUND_EQUATIONS_SUPPLIED_STRUCTURAL_ONLY_NOT_NUMERICAL`",
        "`DERIVED_REDUCED_BACKGROUND_EQUATIONS`",
        "`NUMERICAL_COMPARISON_EXECUTION_INPUTS_NOT_SUPPLIED`",
        "`PERTURBATION_CLOSURE_EQUATIONS_NOT_SUPPLIED`",
        "`PASS_STRUCTURAL_ONLY`",
        "does not supply numerical integration",
        "does not supply empirical evidence",
        "any Clay problem",
    ]:
        if phrase not in doc:
            raise AssertionError(f"doc missing phrase: {phrase}")

    print("Derived reduced background equations verification OK.")
    print("Status: DERIVED_REDUCED_BACKGROUND_EQUATIONS_SUPPLIED_STRUCTURAL_ONLY_NOT_NUMERICAL")
    print("Check result: PASS_STRUCTURAL_ONLY")
    print("New root blocker: PERTURBATION_CLOSURE_EQUATIONS_NOT_SUPPLIED")

if __name__ == "__main__":
    main()
