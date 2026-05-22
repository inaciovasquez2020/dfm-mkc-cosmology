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
GRID_SPEC = ROOT / "specs" / "OBSERVABLE_EVALUATION_GRID.json"
ARTIFACT = ROOT / "artifacts" / "repo_intake" / "observable_evaluation_grid_2026_05_22.json"
DOC = ROOT / "docs" / "status" / "OBSERVABLE_EVALUATION_GRID_2026_05_22.md"

REQUIRED_GRID_IDS = {
    "background_redshift_grid",
    "growth_redshift_grid",
    "cmb_multipole_grid",
    "perturbation_wavenumber_grid",
    "sound_horizon_epoch_grid",
}

REQUIRED_BOUNDARY = [
    "does not bind grids to an empirical data vector",
    "does not supply a data vector",
    "does not supply covariance alignment",
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

def assert_strictly_increasing(values, label):
    for value in values:
        if not isinstance(value, (int, float)) or not math.isfinite(value):
            raise AssertionError(f"{label} contains non-finite value: {value}")
    if any(values[i] >= values[i + 1] for i in range(len(values) - 1)):
        raise AssertionError(f"{label} must be strictly increasing")

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
    }
    for object_id, data in expected_inputs.items():
        if data.get("object_id") != object_id:
            raise AssertionError(f"input object mismatch for {object_id}")

    if initial.get("initial_conditions_supplied") is not True:
        raise AssertionError("initial conditions must already be supplied")

    if grid.get("object_id") != "OBSERVABLE_EVALUATION_GRID":
        raise AssertionError("wrong grid object_id")

    if grid.get("status") != "OBSERVABLE_EVALUATION_GRID_SUPPLIED_REFERENCE_ONLY_NOT_DATA_BOUND":
        raise AssertionError("wrong grid status")

    if grid.get("check_result") != "PASS_REFERENCE_GRID_ONLY":
        raise AssertionError("wrong grid check_result")

    policy = grid.get("grid_policy", {})
    for key in [
        "reference_grid_only",
        "observable_order_locked",
    ]:
        if policy.get(key) is not True:
            raise AssertionError(f"{key} must be true")

    for key in [
        "bound_to_data_vector",
        "covariance_aligned",
        "likelihood_ready",
        "fit_to_data",
        "physical_calibration_claimed",
    ]:
        if policy.get(key) is not False:
            raise AssertionError(f"{key} must be false")

    grids = grid.get("evaluation_grids", [])
    grid_ids = {item.get("grid_id") for item in grids}
    assert_contains_all(grid_ids, REQUIRED_GRID_IDS, "evaluation grid ids")

    for item in grids:
        values = item.get("values", [])
        if not values:
            raise AssertionError(f"grid has no values: {item}")
        assert_strictly_increasing(values, item["grid_id"])
        if item["grid_id"] in {"background_redshift_grid", "growth_redshift_grid"}:
            if values[0] < 0:
                raise AssertionError(f"redshift grid must be nonnegative: {item}")
        if item["grid_id"] == "sound_horizon_epoch_grid":
            if values[0] <= 0:
                raise AssertionError("sound horizon redshift grid must be positive")
        if item["grid_id"] == "perturbation_wavenumber_grid":
            if values[0] <= 0:
                raise AssertionError("wavenumber grid must be positive")
        if item["grid_id"] == "cmb_multipole_grid":
            for value in values:
                if not isinstance(value, int):
                    raise AssertionError("multipole grid values must be integers")
                if value < 2:
                    raise AssertionError("multipole grid values must be at least 2")
        if item.get("status") != "reference_grid_not_data_bound":
            raise AssertionError(f"grid status must be reference_grid_not_data_bound: {item}")
        if not item.get("applies_to"):
            raise AssertionError(f"grid missing applies_to: {item}")

    frozen_order = vector.get("observable_vector_order", [])
    if not frozen_order:
        raise AssertionError("frozen vector order missing")

    coverage = grid.get("observable_coverage", [])
    covered_observables = {item.get("observable") for item in coverage}
    assert_contains_all(covered_observables, frozen_order, "observable coverage")

    grid_id_set = set(grid_ids)
    for item in coverage:
        if item.get("observable") not in frozen_order:
            raise AssertionError(f"coverage includes non-frozen observable: {item}")
        if not item.get("grid_ids"):
            raise AssertionError(f"coverage missing grid ids: {item}")
        for grid_id in item["grid_ids"]:
            if grid_id not in grid_id_set:
                raise AssertionError(f"coverage references absent grid id: {item}")
        if item.get("coverage_status") != "covered_by_reference_grid":
            raise AssertionError(f"wrong coverage status: {item}")

    for flag in [
        "observable_evaluation_grid_supplied",
    ]:
        if grid.get(flag) is not True:
            raise AssertionError(f"{flag} must be true")

    for flag in [
        "data_vector_supplied",
        "covariance_matrix_supplied",
        "likelihood_rule_supplied",
        "lambda_cdm_baseline_supplied",
        "empirical_validation_claimed",
        "model_selection_claimed",
    ]:
        if grid.get(flag) is not False:
            raise AssertionError(f"{flag} must be false")

    assert_contains_all(grid["does_not_prove"], REQUIRED_DOES_NOT_PROVE, "grid does_not_prove")
    assert_contains_all(grid["next_missing_objects"], REQUIRED_NEXT, "grid next_missing_objects")

    if artifact.get("required_object_filled") != "OBSERVABLE_EVALUATION_GRID":
        raise AssertionError("artifact required object mismatch")

    if artifact.get("root_blocker_removed") != "OBSERVABLE_EVALUATION_GRID_NOT_SUPPLIED":
        raise AssertionError("wrong removed blocker")

    if artifact.get("new_root_blocker") != "DATA_VECTOR_SCHEMA_NOT_SUPPLIED":
        raise AssertionError("wrong new blocker")

    if artifact.get("check_result") != "PASS_REFERENCE_GRID_ONLY":
        raise AssertionError("artifact check result mismatch")

    assert_contains_all(artifact["boundary"], REQUIRED_BOUNDARY, "artifact boundary")
    assert_contains_all(artifact["does_not_prove"], REQUIRED_DOES_NOT_PROVE, "artifact does_not_prove")
    assert_contains_all(artifact["next_missing_objects"], REQUIRED_NEXT, "artifact next_missing_objects")

    for phrase in [
        "Status: `OBSERVABLE_EVALUATION_GRID_SUPPLIED_REFERENCE_ONLY_NOT_DATA_BOUND`",
        "`OBSERVABLE_EVALUATION_GRID`",
        "`OBSERVABLE_EVALUATION_GRID_NOT_SUPPLIED`",
        "`DATA_VECTOR_SCHEMA_NOT_SUPPLIED`",
        "`PASS_REFERENCE_GRID_ONLY`",
        "does not bind grids to an empirical data vector",
        "does not supply empirical evidence",
        "any Clay problem",
    ]:
        if phrase not in doc:
            raise AssertionError(f"doc missing phrase: {phrase}")

    print("Observable evaluation grid verification OK.")
    print("Status: OBSERVABLE_EVALUATION_GRID_SUPPLIED_REFERENCE_ONLY_NOT_DATA_BOUND")
    print("Check result: PASS_REFERENCE_GRID_ONLY")
    print("New root blocker: DATA_VECTOR_SCHEMA_NOT_SUPPLIED")

if __name__ == "__main__":
    main()
