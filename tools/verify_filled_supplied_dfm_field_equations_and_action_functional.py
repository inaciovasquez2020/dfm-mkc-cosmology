#!/usr/bin/env python3
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SPEC = ROOT / "specs" / "SUPPLIED_DFM_FIELD_EQUATIONS_AND_ACTION_FUNCTIONAL.json"
ARTIFACT = ROOT / "artifacts" / "repo_intake" / "filled_supplied_dfm_field_equations_and_action_functional_2026_05_22.json"
DOC = ROOT / "docs" / "status" / "FILLED_SUPPLIED_DFM_FIELD_EQUATIONS_AND_ACTION_FUNCTIONAL_2026_05_22.md"

REQUIRED_SPEC_KEYS = {
    "object_id",
    "status",
    "primitive_fields",
    "coupling_constants",
    "action_functional",
    "field_equations",
    "mathematical_closure_claimed",
    "empirical_validation_claimed",
    "prediction_vector_claimed",
    "likelihood_execution_claimed",
    "does_not_prove",
    "next_missing_objects",
}

REQUIRED_EQUATIONS = {
    "metric_equation",
    "scalar_equation",
    "vector_equation",
    "matter_equation",
    "stress_energy_definition",
}

FORBIDDEN_TRUE_FLAGS = {
    "mathematical_closure_claimed",
    "empirical_validation_claimed",
    "prediction_vector_claimed",
    "likelihood_execution_claimed",
}

REQUIRED_BOUNDARY_PHRASES = [
    "does not verify the variational derivation",
    "does not validate physical correctness",
    "does not supply a frozen prediction vector",
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
    "VARIATIONAL_DERIVATION_CHECK",
    "PARAMETER_DOMAIN_AND_UNITS_TABLE",
    "COSMOLOGICAL_REDUCTION_ANSATZ",
    "FROZEN_PREDICTION_VECTOR",
    "EXECUTED_DFM_VS_LAMBDA_CDM_COMPARISON",
]

def load_json(path: Path) -> dict:
    if not path.exists():
        raise AssertionError(f"missing file: {path}")
    return json.loads(path.read_text())

def assert_contains_all(container, required, label):
    missing = [x for x in required if x not in container]
    if missing:
        raise AssertionError(f"{label} missing: {missing}")

def main() -> None:
    spec = load_json(SPEC)
    artifact = load_json(ARTIFACT)
    doc = DOC.read_text() if DOC.exists() else ""

    missing_keys = REQUIRED_SPEC_KEYS - set(spec)
    if missing_keys:
        raise AssertionError(f"spec missing keys: {sorted(missing_keys)}")

    if spec["object_id"] != "FILLED_SUPPLIED_DFM_FIELD_EQUATIONS_AND_ACTION_FUNCTIONAL":
        raise AssertionError("wrong object_id")

    if spec["status"] != "FILLED_STRUCTURAL_CANDIDATE_ONLY_NOT_VALIDATED":
        raise AssertionError("wrong spec status")

    for flag in FORBIDDEN_TRUE_FLAGS:
        if spec.get(flag) is not False:
            raise AssertionError(f"{flag} must be false")

    if len(spec["primitive_fields"]) < 4:
        raise AssertionError("primitive field surface is incomplete")

    if len(spec["coupling_constants"]) < 8:
        raise AssertionError("coupling constant surface is incomplete")

    action = spec["action_functional"]
    for token in ["R", "phi", "A_mu", "F_{mu nu}", "S_m", "sqrt(-g)"]:
        if token not in action["definition"]:
            raise AssertionError(f"action functional missing token: {token}")

    assert_contains_all(spec["field_equations"], REQUIRED_EQUATIONS, "field equations")
    assert_contains_all(spec["does_not_prove"], REQUIRED_DOES_NOT_PROVE, "spec does_not_prove")
    assert_contains_all(spec["next_missing_objects"], REQUIRED_NEXT, "spec next_missing_objects")

    if artifact["status"] != spec["status"]:
        raise AssertionError("artifact status mismatch")

    if artifact["required_object_filled"] != spec["object_id"]:
        raise AssertionError("artifact required object mismatch")

    if artifact["new_root_blocker"] != "VARIATIONAL_DERIVATION_CHECK_NOT_SUPPLIED":
        raise AssertionError("wrong new root blocker")

    assert_contains_all(artifact["boundary"], REQUIRED_BOUNDARY_PHRASES, "artifact boundary")
    assert_contains_all(artifact["does_not_prove"], REQUIRED_DOES_NOT_PROVE, "artifact does_not_prove")
    assert_contains_all(artifact["next_missing_objects"], REQUIRED_NEXT, "artifact next_missing_objects")

    for phrase in [
        "Status: `FILLED_STRUCTURAL_CANDIDATE_ONLY_NOT_VALIDATED`",
        "`FILLED_SUPPLIED_DFM_FIELD_EQUATIONS_AND_ACTION_FUNCTIONAL`",
        "`VARIATIONAL_DERIVATION_CHECK_NOT_SUPPLIED`",
        "does not verify the variational derivation",
        "does not supply empirical evidence",
        "any Clay problem",
    ]:
        if phrase not in doc:
            raise AssertionError(f"doc missing phrase: {phrase}")

    print("Filled supplied DFM field equations and action functional verification OK.")
    print("Status: FILLED_STRUCTURAL_CANDIDATE_ONLY_NOT_VALIDATED")
    print("New root blocker: VARIATIONAL_DERIVATION_CHECK_NOT_SUPPLIED")

if __name__ == "__main__":
    main()
