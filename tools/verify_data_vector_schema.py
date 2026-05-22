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
PERTURBATION_SPEC = ROOT / "specs" / "PERTURBATION_CLOSURE_EQUATIONS.json"
NUMERIC_SPEC = ROOT / "specs" / "NUMERICAL_PARAMETER_VECTOR.json"
INITIAL_SPEC = ROOT / "specs" / "INITIAL_CONDITIONS.json"
GRID_SPEC = ROOT / "specs" / "OBSERVABLE_EVALUATION_GRID.json"
SCHEMA_SPEC = ROOT / "specs" / "DATA_VECTOR_SCHEMA.json"
ARTIFACT = ROOT / "artifacts" / "repo_intake" / "data_vector_schema_2026_05_22.json"
DOC = ROOT / "docs" / "status" / "DATA_VECTOR_SCHEMA_2026_05_22.md"

EXPECTED_SLOT_ORDER = [
    "slot_E_DFM",
    "slot_D_A_DFM",
    "slot_D_L_DFM",
    "slot_mu_DFM",
    "slot_f_sigma8_DFM",
    "slot_C_ell_TT_DFM",
    "slot_C_ell_TE_DFM",
    "slot_C_ell_EE_DFM",
    "slot_S8_DFM",
    "slot_r_d_DFM",
]

REQUIRED_BOUNDARY = [
    "does not supply empirical data values",
    "does not supply observational uncertainties",
    "does not bind slots to an external payload",
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
    initial = load_json(INITIAL_SPEC)
    grid = load_json(GRID_SPEC)
    schema = load_json(SCHEMA_SPEC)
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
        "INITIAL_CONDITIONS": initial,
        "OBSERVABLE_EVALUATION_GRID": grid,
    }
    for object_id, data in expected_inputs.items():
        if data.get("object_id") != object_id:
            raise AssertionError(f"input object mismatch for {object_id}")

    if grid.get("observable_evaluation_grid_supplied") is not True:
        raise AssertionError("observable evaluation grid must already be supplied")

    if schema.get("object_id") != "DATA_VECTOR_SCHEMA":
        raise AssertionError("wrong schema object_id")

    if schema.get("status") != "DATA_VECTOR_SCHEMA_SUPPLIED_SCHEMA_ONLY_NO_EMPIRICAL_VALUES":
        raise AssertionError("wrong schema status")

    if schema.get("check_result") != "PASS_SCHEMA_ONLY":
        raise AssertionError("wrong schema check_result")

    policy = schema.get("schema_policy", {})
    for key in [
        "schema_only",
        "slot_order_locked",
        "observable_order_matches_frozen_prediction_vector",
    ]:
        if policy.get(key) is not True:
            raise AssertionError(f"{key} must be true")

    for key in [
        "empirical_values_supplied",
        "covariance_matrix_supplied",
        "likelihood_ready",
        "bound_to_external_payload",
        "fit_to_data",
        "model_selection_claimed",
    ]:
        if policy.get(key) is not False:
            raise AssertionError(f"{key} must be false")

    if schema.get("data_vector_slot_order") != EXPECTED_SLOT_ORDER:
        raise AssertionError("slot order mismatch")

    slots = schema.get("data_slots", [])
    if len(slots) != len(EXPECTED_SLOT_ORDER):
        raise AssertionError("data slot count mismatch")

    frozen_order = vector.get("observable_vector_order", [])
    if len(frozen_order) != len(EXPECTED_SLOT_ORDER):
        raise AssertionError("frozen prediction vector size mismatch")

    grid_ids = {item["grid_id"] for item in grid.get("evaluation_grids", [])}
    if not grid_ids:
        raise AssertionError("no observable evaluation grids found")

    coverage_by_observable = {
        item["observable"]: set(item["grid_ids"])
        for item in grid.get("observable_coverage", [])
    }

    slot_observables = []
    for index, slot_id in enumerate(EXPECTED_SLOT_ORDER):
        item = slots[index]
        if item.get("index") != index:
            raise AssertionError(f"wrong slot index at {index}")
        if item.get("slot_id") != slot_id:
            raise AssertionError(f"wrong slot id at {index}")
        if item.get("observable") != frozen_order[index]:
            raise AssertionError(f"slot observable does not match frozen order at {index}")
        if item.get("model_observable") != frozen_order[index]:
            raise AssertionError(f"slot model observable does not match frozen order at {index}")
        if item.get("data_value_supplied") is not False:
            raise AssertionError(f"slot supplies empirical value: {item}")
        if item.get("uncertainty_supplied") is not False:
            raise AssertionError(f"slot supplies uncertainty: {item}")
        if item.get("payload_binding") != "unbound":
            raise AssertionError(f"slot must remain unbound: {item}")
        if not item.get("unit"):
            raise AssertionError(f"slot missing unit: {item}")
        if not item.get("grid_ids"):
            raise AssertionError(f"slot missing grid ids: {item}")
        for grid_id in item["grid_ids"]:
            if grid_id not in grid_ids:
                raise AssertionError(f"slot references absent grid id: {item}")
        expected_grid_ids = coverage_by_observable.get(item["observable"])
        if expected_grid_ids is None:
            raise AssertionError(f"slot observable not covered by observable grid: {item}")
        if not set(item["grid_ids"]).issubset(expected_grid_ids):
            raise AssertionError(f"slot grid ids not subset of observable coverage: {item}")
        slot_observables.append(item["observable"])

    if slot_observables != frozen_order:
        raise AssertionError("slot observables do not exactly match frozen vector order")

    for flag in [
        "data_vector_schema_supplied",
    ]:
        if schema.get(flag) is not True:
            raise AssertionError(f"{flag} must be true")

    for flag in [
        "empirical_values_supplied",
        "covariance_matrix_supplied",
        "likelihood_rule_supplied",
        "lambda_cdm_baseline_supplied",
        "empirical_validation_claimed",
        "model_selection_claimed",
    ]:
        if schema.get(flag) is not False:
            raise AssertionError(f"{flag} must be false")

    assert_contains_all(schema["does_not_prove"], REQUIRED_DOES_NOT_PROVE, "schema does_not_prove")
    assert_contains_all(schema["next_missing_objects"], REQUIRED_NEXT, "schema next_missing_objects")

    if artifact.get("required_object_filled") != "DATA_VECTOR_SCHEMA":
        raise AssertionError("artifact required object mismatch")

    if artifact.get("root_blocker_removed") != "DATA_VECTOR_SCHEMA_NOT_SUPPLIED":
        raise AssertionError("wrong removed blocker")

    if artifact.get("new_root_blocker") != "COVARIANCE_MATRIX_NOT_SUPPLIED":
        raise AssertionError("wrong new blocker")

    if artifact.get("check_result") != "PASS_SCHEMA_ONLY":
        raise AssertionError("artifact check result mismatch")

    assert_contains_all(artifact["boundary"], REQUIRED_BOUNDARY, "artifact boundary")
    assert_contains_all(artifact["does_not_prove"], REQUIRED_DOES_NOT_PROVE, "artifact does_not_prove")
    assert_contains_all(artifact["next_missing_objects"], REQUIRED_NEXT, "artifact next_missing_objects")

    for phrase in [
        "Status: `DATA_VECTOR_SCHEMA_SUPPLIED_SCHEMA_ONLY_NO_EMPIRICAL_VALUES`",
        "`DATA_VECTOR_SCHEMA`",
        "`DATA_VECTOR_SCHEMA_NOT_SUPPLIED`",
        "`COVARIANCE_MATRIX_NOT_SUPPLIED`",
        "`PASS_SCHEMA_ONLY`",
        "does not supply empirical data values",
        "does not supply empirical evidence",
        "any Clay problem",
    ]:
        if phrase not in doc:
            raise AssertionError(f"doc missing phrase: {phrase}")

    print("Data vector schema verification OK.")
    print("Status: DATA_VECTOR_SCHEMA_SUPPLIED_SCHEMA_ONLY_NO_EMPIRICAL_VALUES")
    print("Check result: PASS_SCHEMA_ONLY")
    print("New root blocker: COVARIANCE_MATRIX_NOT_SUPPLIED")

if __name__ == "__main__":
    main()
