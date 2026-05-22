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
INITIAL_SPEC = ROOT / "specs" / "INITIAL_CONDITIONS.json"
ARTIFACT = ROOT / "artifacts" / "repo_intake" / "initial_conditions_2026_05_22.json"
DOC = ROOT / "docs" / "status" / "INITIAL_CONDITIONS_2026_05_22.md"

REQUIRED_BACKGROUND_SYMBOLS = [
    "N(t_ref)",
    "a(t_ref)",
    "H(t_ref)",
    "phi(t_ref)",
    "dot_phi(t_ref)",
    "A_0(t_ref)",
    "rho_m(t_ref)",
    "p_m(t_ref)",
]

REQUIRED_PERTURBATION_SYMBOLS = [
    "Phi(t_ref,q)",
    "Psi_metric(t_ref,q)",
    "delta_phi(t_ref,q)",
    "dot_delta_phi(t_ref,q)",
    "delta_A0(t_ref,q)",
    "delta_A_parallel(t_ref,q)",
    "dot_delta_A_parallel(t_ref,q)",
    "delta_m(t_ref,q)",
    "theta_m(t_ref,q)",
]

REQUIRED_BOUNDARY = [
    "does not claim the initial conditions solve the background constraints",
    "does not claim the initial conditions solve perturbation mode constraints",
    "does not claim the initial conditions are fit to data",
    "does not claim physical calibration",
    "does not supply numerical integration",
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

def assert_finite_number(value, label):
    if not isinstance(value, (int, float)) or not math.isfinite(value):
        raise AssertionError(f"{label} must be a finite numeric value")

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
    initial = load_json(INITIAL_SPEC)
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
        "NUMERICAL_PARAMETER_VECTOR": numeric,
    }
    for object_id, data in expected_inputs.items():
        if data.get("object_id") != object_id:
            raise AssertionError(f"input object mismatch for {object_id}")

    if numeric.get("numerical_parameter_vector_supplied") is not True:
        raise AssertionError("numerical parameter vector must already be supplied")

    if initial.get("object_id") != "INITIAL_CONDITIONS":
        raise AssertionError("wrong initial object_id")

    if initial.get("status") != "INITIAL_CONDITIONS_SUPPLIED_REFERENCE_CANDIDATE_ONLY_NOT_CONSTRAINT_SOLVED":
        raise AssertionError("wrong initial status")

    if initial.get("check_result") != "PASS_REFERENCE_INITIAL_CONDITIONS_ONLY":
        raise AssertionError("wrong initial check_result")

    policy = initial.get("initial_condition_policy", {})
    for key in [
        "reference_epoch_locked",
        "background_initial_conditions_supplied",
        "perturbation_initial_conditions_supplied",
        "reference_candidate_only",
    ]:
        if policy.get(key) is not True:
            raise AssertionError(f"{key} must be true")

    for key in [
        "constraint_solution_claimed",
        "fit_to_data",
        "posterior_sample",
        "physical_calibration_claimed",
    ]:
        if policy.get(key) is not False:
            raise AssertionError(f"{key} must be false")

    epoch = initial.get("reference_epoch", {})
    assert_finite_number(epoch.get("t_ref"), "t_ref")
    assert_finite_number(epoch.get("z_ref"), "z_ref")

    background_values = initial.get("background_initial_conditions", [])
    if len(background_values) != len(REQUIRED_BACKGROUND_SYMBOLS):
        raise AssertionError("background initial condition count mismatch")

    background_symbols = [item.get("symbol") for item in background_values]
    if background_symbols != REQUIRED_BACKGROUND_SYMBOLS:
        raise AssertionError(f"background symbols mismatch: {background_symbols}")

    for index, item in enumerate(background_values):
        if item.get("index") != index:
            raise AssertionError(f"wrong background index at {index}")
        assert_finite_number(item.get("value"), item.get("symbol"))
        if not item.get("constraint_status"):
            raise AssertionError(f"missing background constraint_status: {item}")
        if not item.get("role"):
            raise AssertionError(f"missing background role: {item}")

    background_by_symbol = {item["symbol"]: item["value"] for item in background_values}
    if background_by_symbol["N(t_ref)"] <= 0:
        raise AssertionError("N(t_ref) must be positive")
    if background_by_symbol["a(t_ref)"] <= 0:
        raise AssertionError("a(t_ref) must be positive")
    if background_by_symbol["rho_m(t_ref)"] < 0:
        raise AssertionError("rho_m(t_ref) must be nonnegative")

    reduced_variables = set(background.get("reduction_domain", {}).values()) | set(background.get("derived_background_equations", [{}])[0].get("principal_variables", []))
    for token in ["N(t)", "a(t)", "H(t)", "phi(t)", "A_0(t)", "rho_m(t)"]:
        if token not in json.dumps(background):
            raise AssertionError(f"background spec missing variable token: {token}")

    perturbation_values = initial.get("perturbation_initial_conditions", [])
    if len(perturbation_values) != len(REQUIRED_PERTURBATION_SYMBOLS):
        raise AssertionError("perturbation initial condition count mismatch")

    perturbation_symbols = [item.get("symbol") for item in perturbation_values]
    if perturbation_symbols != REQUIRED_PERTURBATION_SYMBOLS:
        raise AssertionError(f"perturbation symbols mismatch: {perturbation_symbols}")

    for index, item in enumerate(perturbation_values):
        if item.get("index") != index:
            raise AssertionError(f"wrong perturbation index at {index}")
        assert_finite_number(item.get("value"), item.get("symbol"))
        if not item.get("constraint_status"):
            raise AssertionError(f"missing perturbation constraint_status: {item}")
        if not item.get("role"):
            raise AssertionError(f"missing perturbation role: {item}")

    for token in ["Phi(t,q)", "Psi_metric(t,q)", "delta_phi(t,q)", "delta_A0(t,q)", "delta_A_parallel(t,q)", "delta_m(t,q)", "theta_m(t,q)"]:
        if token not in json.dumps(perturbation):
            raise AssertionError(f"perturbation spec missing variable token: {token}")

    if "dot_delta_phi(t,q)" not in json.dumps(perturbation):
        if "scalar_field_perturbation_equation" not in json.dumps(perturbation):
            raise AssertionError("scalar perturbation velocity lacks structural equation context")

    for flag in [
        "initial_conditions_supplied",
    ]:
        if initial.get(flag) is not True:
            raise AssertionError(f"{flag} must be true")

    for flag in [
        "constraint_solution_claimed",
        "numerical_integration_supplied",
        "observable_evaluation_grid_supplied",
        "data_vector_supplied",
        "covariance_matrix_supplied",
        "likelihood_rule_supplied",
        "lambda_cdm_baseline_supplied",
        "empirical_validation_claimed",
        "model_selection_claimed",
    ]:
        if initial.get(flag) is not False:
            raise AssertionError(f"{flag} must be false")

    assert_contains_all(initial["does_not_prove"], REQUIRED_DOES_NOT_PROVE, "initial does_not_prove")
    assert_contains_all(initial["next_missing_objects"], REQUIRED_NEXT, "initial next_missing_objects")

    if artifact.get("required_object_filled") != "INITIAL_CONDITIONS":
        raise AssertionError("artifact required object mismatch")

    if artifact.get("root_blocker_removed") != "INITIAL_CONDITIONS_NOT_SUPPLIED":
        raise AssertionError("wrong removed blocker")

    if artifact.get("new_root_blocker") != "OBSERVABLE_EVALUATION_GRID_NOT_SUPPLIED":
        raise AssertionError("wrong new blocker")

    if artifact.get("check_result") != "PASS_REFERENCE_INITIAL_CONDITIONS_ONLY":
        raise AssertionError("artifact check result mismatch")

    assert_contains_all(artifact["boundary"], REQUIRED_BOUNDARY, "artifact boundary")
    assert_contains_all(artifact["does_not_prove"], REQUIRED_DOES_NOT_PROVE, "artifact does_not_prove")
    assert_contains_all(artifact["next_missing_objects"], REQUIRED_NEXT, "artifact next_missing_objects")

    for phrase in [
        "Status: `INITIAL_CONDITIONS_SUPPLIED_REFERENCE_CANDIDATE_ONLY_NOT_CONSTRAINT_SOLVED`",
        "`INITIAL_CONDITIONS`",
        "`INITIAL_CONDITIONS_NOT_SUPPLIED`",
        "`OBSERVABLE_EVALUATION_GRID_NOT_SUPPLIED`",
        "`PASS_REFERENCE_INITIAL_CONDITIONS_ONLY`",
        "does not claim the initial conditions solve the background constraints",
        "does not supply empirical evidence",
        "any Clay problem",
    ]:
        if phrase not in doc:
            raise AssertionError(f"doc missing phrase: {phrase}")

    print("Initial conditions verification OK.")
    print("Status: INITIAL_CONDITIONS_SUPPLIED_REFERENCE_CANDIDATE_ONLY_NOT_CONSTRAINT_SOLVED")
    print("Check result: PASS_REFERENCE_INITIAL_CONDITIONS_ONLY")
    print("New root blocker: OBSERVABLE_EVALUATION_GRID_NOT_SUPPLIED")

if __name__ == "__main__":
    main()
