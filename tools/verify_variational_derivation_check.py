#!/usr/bin/env python3
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
INPUT_SPEC = ROOT / "specs" / "SUPPLIED_DFM_FIELD_EQUATIONS_AND_ACTION_FUNCTIONAL.json"
CHECK_SPEC = ROOT / "specs" / "VARIATIONAL_DERIVATION_CHECK.json"
ARTIFACT = ROOT / "artifacts" / "repo_intake" / "variational_derivation_check_2026_05_22.json"
DOC = ROOT / "docs" / "status" / "VARIATIONAL_DERIVATION_CHECK_2026_05_22.md"

REQUIRED_EQUATION_TARGETS = {
    "metric_equation",
    "scalar_equation",
    "vector_equation",
    "matter_equation",
}

REQUIRED_VARIATIONS = {
    "delta S / delta g^{mu nu}",
    "delta S / delta phi",
    "delta S / delta A_mu",
    "delta S_m / delta Psi",
}

REQUIRED_BOUNDARY = [
    "does not prove a full symbolic variational derivation",
    "does not validate physical correctness",
    "does not supply parameter domains or units",
    "does not supply a cosmological reduction ansatz",
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
    "PARAMETER_DOMAIN_AND_UNITS_TABLE",
    "COSMOLOGICAL_REDUCTION_ANSATZ",
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
    input_spec = load_json(INPUT_SPEC)
    check = load_json(CHECK_SPEC)
    artifact = load_json(ARTIFACT)

    if not DOC.exists():
        raise AssertionError(f"missing file: {DOC}")
    doc = DOC.read_text()

    if input_spec.get("object_id") != "FILLED_SUPPLIED_DFM_FIELD_EQUATIONS_AND_ACTION_FUNCTIONAL":
        raise AssertionError("input spec object mismatch")

    if input_spec.get("status") != "FILLED_STRUCTURAL_CANDIDATE_ONLY_NOT_VALIDATED":
        raise AssertionError("input spec status mismatch")

    if check.get("object_id") != "VARIATIONAL_DERIVATION_CHECK":
        raise AssertionError("wrong check object_id")

    if check.get("status") != "STRUCTURAL_VARIATIONAL_DERIVATION_CHECK_SUPPLIED_NOT_SYMBOLICALLY_PROVED":
        raise AssertionError("wrong check status")

    if check.get("input_spec") != "specs/SUPPLIED_DFM_FIELD_EQUATIONS_AND_ACTION_FUNCTIONAL.json":
        raise AssertionError("wrong check input_spec")

    if check.get("check_result") != "PASS_STRUCTURAL_ONLY":
        raise AssertionError("wrong check_result")

    for flag in [
        "symbolic_variation_proved",
        "physical_correctness_claimed",
        "empirical_validation_claimed",
        "likelihood_execution_claimed",
    ]:
        if check.get(flag) is not False:
            raise AssertionError(f"{flag} must be false")

    supplied_equations = set(input_spec.get("field_equations", {}).keys())
    assert_contains_all(supplied_equations, REQUIRED_EQUATION_TARGETS, "input field equations")

    variations = check.get("checked_variations", [])
    if len(variations) != 4:
        raise AssertionError("expected exactly four checked variations")

    seen_variations = {item.get("variation") for item in variations}
    seen_targets = {item.get("equation_target") for item in variations}
    assert_contains_all(seen_variations, REQUIRED_VARIATIONS, "checked variations")
    assert_contains_all(seen_targets, REQUIRED_EQUATION_TARGETS, "checked equation targets")

    for item in variations:
        if item.get("structural_result") != "matched":
            raise AssertionError(f"variation not matched: {item}")
        if not item.get("required_sources"):
            raise AssertionError(f"variation missing required_sources: {item}")
        if item.get("equation_target") not in supplied_equations:
            raise AssertionError(f"target not present in input equations: {item}")

    action_definition = input_spec["action_functional"]["definition"]
    required_action_tokens = [
        "R",
        "Lambda_0",
        "phi",
        "A_mu",
        "F_{mu nu}",
        "beta_phi_A",
        "xi_phi",
        "xi_A",
        "S_m",
    ]
    for token in required_action_tokens:
        if token not in action_definition:
            raise AssertionError(f"input action missing token required by check: {token}")

    assert_contains_all(check["does_not_prove"], REQUIRED_DOES_NOT_PROVE, "check does_not_prove")
    assert_contains_all(check["next_missing_objects"], REQUIRED_NEXT, "check next_missing_objects")

    if artifact.get("required_object_filled") != "VARIATIONAL_DERIVATION_CHECK":
        raise AssertionError("artifact required object mismatch")

    if artifact.get("root_blocker_removed") != "VARIATIONAL_DERIVATION_CHECK_NOT_SUPPLIED":
        raise AssertionError("wrong removed blocker")

    if artifact.get("new_root_blocker") != "PARAMETER_DOMAIN_AND_UNITS_TABLE_NOT_SUPPLIED":
        raise AssertionError("wrong new blocker")

    if artifact.get("check_result") != "PASS_STRUCTURAL_ONLY":
        raise AssertionError("artifact check result mismatch")

    assert_contains_all(artifact["boundary"], REQUIRED_BOUNDARY, "artifact boundary")
    assert_contains_all(artifact["does_not_prove"], REQUIRED_DOES_NOT_PROVE, "artifact does_not_prove")
    assert_contains_all(artifact["next_missing_objects"], REQUIRED_NEXT, "artifact next_missing_objects")

    for phrase in [
        "Status: `STRUCTURAL_VARIATIONAL_DERIVATION_CHECK_SUPPLIED_NOT_SYMBOLICALLY_PROVED`",
        "`VARIATIONAL_DERIVATION_CHECK`",
        "`VARIATIONAL_DERIVATION_CHECK_NOT_SUPPLIED`",
        "`PARAMETER_DOMAIN_AND_UNITS_TABLE_NOT_SUPPLIED`",
        "`PASS_STRUCTURAL_ONLY`",
        "does not prove a full symbolic variational derivation",
        "does not supply empirical evidence",
        "any Clay problem",
    ]:
        if phrase not in doc:
            raise AssertionError(f"doc missing phrase: {phrase}")

    print("Variational derivation check verification OK.")
    print("Status: STRUCTURAL_VARIATIONAL_DERIVATION_CHECK_SUPPLIED_NOT_SYMBOLICALLY_PROVED")
    print("Check result: PASS_STRUCTURAL_ONLY")
    print("New root blocker: PARAMETER_DOMAIN_AND_UNITS_TABLE_NOT_SUPPLIED")

if __name__ == "__main__":
    main()
