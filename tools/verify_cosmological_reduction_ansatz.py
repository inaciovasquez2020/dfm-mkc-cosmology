#!/usr/bin/env python3
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
ACTION_SPEC = ROOT / "specs" / "SUPPLIED_DFM_FIELD_EQUATIONS_AND_ACTION_FUNCTIONAL.json"
VARIATIONAL_SPEC = ROOT / "specs" / "VARIATIONAL_DERIVATION_CHECK.json"
PARAM_SPEC = ROOT / "specs" / "PARAMETER_DOMAIN_AND_UNITS_TABLE.json"
ANSATZ_SPEC = ROOT / "specs" / "COSMOLOGICAL_REDUCTION_ANSATZ.json"
ARTIFACT = ROOT / "artifacts" / "repo_intake" / "cosmological_reduction_ansatz_2026_05_22.json"
DOC = ROOT / "docs" / "status" / "COSMOLOGICAL_REDUCTION_ANSATZ_2026_05_22.md"

REQUIRED_SOURCE_EQUATIONS = {
    "metric_equation",
    "scalar_equation",
    "vector_equation",
    "matter_equation",
}

REQUIRED_TARGET_IDS = {
    "friedmann_constraint_target",
    "acceleration_equation_target",
    "scalar_background_equation_target",
    "vector_background_constraint_target",
    "matter_background_equation_target",
}

REQUIRED_REDUCED_VARIABLES = {
    "N(t)",
    "a(t)",
    "H(t)",
    "phi(t)",
    "A_0(t)",
    "rho_m(t)",
    "p_m(t)",
}

REQUIRED_BOUNDARY = [
    "does not derive the reduced equations",
    "does not supply numerical parameter values",
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
    "FROZEN_PREDICTION_VECTOR",
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
    artifact = load_json(ARTIFACT)

    if not DOC.exists():
        raise AssertionError(f"missing file: {DOC}")
    doc = DOC.read_text()

    if action.get("object_id") != "FILLED_SUPPLIED_DFM_FIELD_EQUATIONS_AND_ACTION_FUNCTIONAL":
        raise AssertionError("action input object mismatch")

    if variation.get("object_id") != "VARIATIONAL_DERIVATION_CHECK":
        raise AssertionError("variational input object mismatch")

    if params.get("object_id") != "PARAMETER_DOMAIN_AND_UNITS_TABLE":
        raise AssertionError("parameter input object mismatch")

    if ansatz.get("object_id") != "COSMOLOGICAL_REDUCTION_ANSATZ":
        raise AssertionError("wrong ansatz object_id")

    if ansatz.get("status") != "COSMOLOGICAL_REDUCTION_ANSATZ_SUPPLIED_STRUCTURAL_ONLY":
        raise AssertionError("wrong ansatz status")

    if ansatz.get("check_result") != "PASS_STRUCTURAL_ONLY":
        raise AssertionError("wrong ansatz check_result")

    if ansatz.get("ansatz_class") != "homogeneous_isotropic_FLRW_background":
        raise AssertionError("wrong ansatz class")

    metric = ansatz.get("metric_ansatz", {})
    for token in ["N(t)", "a(t)", "gamma_ij", "H(t)"]:
        if token not in " ".join(str(value) for value in metric.values()):
            raise AssertionError(f"metric ansatz missing token: {token}")

    field_reductions = {item["symbol"]: item["reduction"] for item in ansatz.get("field_ansatz", [])}
    if field_reductions.get("phi") != "phi = phi(t)":
        raise AssertionError("scalar reduction missing or wrong")
    if field_reductions.get("A_mu") != "A_mu dx^mu = A_0(t) dt":
        raise AssertionError("vector reduction missing or wrong")
    if field_reductions.get("Psi") != "perfect-fluid effective matter sector":
        raise AssertionError("matter reduction missing or wrong")

    targets = ansatz.get("background_equation_targets", [])
    if len(targets) != 5:
        raise AssertionError("expected five background equation targets")

    target_ids = {item["target_id"] for item in targets}
    source_equations = {item["source_equation"] for item in targets}
    assert_contains_all(target_ids, REQUIRED_TARGET_IDS, "background target ids")
    assert_contains_all(source_equations, REQUIRED_SOURCE_EQUATIONS, "background source equations")

    supplied_equations = set(action.get("field_equations", {}).keys())
    assert_contains_all(supplied_equations, REQUIRED_SOURCE_EQUATIONS, "supplied field equations")
    for item in targets:
        if item["source_equation"] not in supplied_equations:
            raise AssertionError(f"target references absent source equation: {item}")
        if not item.get("structural_form"):
            raise AssertionError(f"target missing structural form: {item}")
        if not item.get("role"):
            raise AssertionError(f"target missing role: {item}")

    reduced_variables = set(ansatz.get("reduced_variable_set", []))
    assert_contains_all(reduced_variables, REQUIRED_REDUCED_VARIABLES, "reduced variables")

    gauge_policy = ansatz.get("gauge_policy", {})
    if gauge_policy.get("lapse_gauge") != "unfixed in the structural ansatz":
        raise AssertionError("lapse gauge must remain unfixed")
    if "N(t) = 1" not in gauge_policy.get("cosmic_time_specialization", ""):
        raise AssertionError("cosmic time specialization missing")

    for flag in [
        "reduced_equations_derived",
        "numerical_prediction_claimed",
        "physical_correctness_claimed",
        "empirical_validation_claimed",
        "likelihood_execution_claimed",
    ]:
        if ansatz.get(flag) is not False:
            raise AssertionError(f"{flag} must be false")

    assert_contains_all(ansatz["does_not_prove"], REQUIRED_DOES_NOT_PROVE, "ansatz does_not_prove")
    assert_contains_all(ansatz["next_missing_objects"], REQUIRED_NEXT, "ansatz next_missing_objects")

    if artifact.get("required_object_filled") != "COSMOLOGICAL_REDUCTION_ANSATZ":
        raise AssertionError("artifact required object mismatch")

    if artifact.get("root_blocker_removed") != "COSMOLOGICAL_REDUCTION_ANSATZ_NOT_SUPPLIED":
        raise AssertionError("wrong removed blocker")

    if artifact.get("new_root_blocker") != "FROZEN_PREDICTION_VECTOR_NOT_SUPPLIED":
        raise AssertionError("wrong new blocker")

    if artifact.get("check_result") != "PASS_STRUCTURAL_ONLY":
        raise AssertionError("artifact check result mismatch")

    assert_contains_all(artifact["boundary"], REQUIRED_BOUNDARY, "artifact boundary")
    assert_contains_all(artifact["does_not_prove"], REQUIRED_DOES_NOT_PROVE, "artifact does_not_prove")
    assert_contains_all(artifact["next_missing_objects"], REQUIRED_NEXT, "artifact next_missing_objects")

    for phrase in [
        "Status: `COSMOLOGICAL_REDUCTION_ANSATZ_SUPPLIED_STRUCTURAL_ONLY`",
        "`COSMOLOGICAL_REDUCTION_ANSATZ`",
        "`COSMOLOGICAL_REDUCTION_ANSATZ_NOT_SUPPLIED`",
        "`FROZEN_PREDICTION_VECTOR_NOT_SUPPLIED`",
        "`PASS_STRUCTURAL_ONLY`",
        "does not derive the reduced equations",
        "does not supply empirical evidence",
        "any Clay problem",
    ]:
        if phrase not in doc:
            raise AssertionError(f"doc missing phrase: {phrase}")

    print("Cosmological reduction ansatz verification OK.")
    print("Status: COSMOLOGICAL_REDUCTION_ANSATZ_SUPPLIED_STRUCTURAL_ONLY")
    print("Check result: PASS_STRUCTURAL_ONLY")
    print("New root blocker: FROZEN_PREDICTION_VECTOR_NOT_SUPPLIED")

if __name__ == "__main__":
    main()
