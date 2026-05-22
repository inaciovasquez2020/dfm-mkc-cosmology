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
ARTIFACT = ROOT / "artifacts" / "repo_intake" / "perturbation_closure_equations_2026_05_22.json"
DOC = ROOT / "docs" / "status" / "PERTURBATION_CLOSURE_EQUATIONS_2026_05_22.md"

REQUIRED_VARIABLES = {
    "Phi(t,q)",
    "Psi_metric(t,q)",
    "delta_phi(t,q)",
    "delta_A0(t,q)",
    "delta_A_parallel(t,q)",
    "delta_m(t,q)",
    "theta_m(t,q)",
}

REQUIRED_EQUATION_IDS = {
    "scalar_metric_poisson_constraint",
    "gravitational_slip_equation",
    "scalar_field_perturbation_equation",
    "vector_temporal_constraint_perturbation",
    "vector_longitudinal_perturbation_equation",
    "matter_density_contrast_equation",
    "matter_velocity_equation",
    "transfer_function_closure_target",
}

REQUIRED_SOURCE_EQUATIONS = {
    "metric_equation",
    "scalar_equation",
    "vector_equation",
    "matter_equation",
    "combined_linearized_system",
}

REQUIRED_OBSERVABLES = {
    "f_sigma8_DFM(z)",
    "C_ell_TT_DFM",
    "C_ell_TE_DFM",
    "C_ell_EE_DFM",
    "S8_DFM",
}

REQUIRED_BOUNDARY = [
    "does not prove a full symbolic linearization",
    "does not supply numerical integration",
    "does not supply a Boltzmann solver",
    "does not supply recombination closure",
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
    perturbation = load_json(PERTURBATION_SPEC)
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
    }
    for object_id, data in expected_inputs.items():
        if data.get("object_id") != object_id:
            raise AssertionError(f"input object mismatch for {object_id}")

    if perturbation.get("object_id") != "PERTURBATION_CLOSURE_EQUATIONS":
        raise AssertionError("wrong perturbation object_id")

    if perturbation.get("status") != "PERTURBATION_CLOSURE_EQUATIONS_SUPPLIED_STRUCTURAL_ONLY_NOT_NUMERICAL":
        raise AssertionError("wrong perturbation status")

    if perturbation.get("check_result") != "PASS_STRUCTURAL_ONLY":
        raise AssertionError("wrong perturbation check_result")

    domain = perturbation.get("perturbation_domain", {})
    if domain.get("perturbation_sector") != "linear_scalar_perturbations":
        raise AssertionError("wrong perturbation sector")
    if domain.get("gauge") != "Newtonian gauge structural closure":
        raise AssertionError("wrong perturbation gauge")

    variables = {item["symbol"] for item in perturbation.get("perturbation_variables", [])}
    assert_contains_all(variables, REQUIRED_VARIABLES, "perturbation variables")

    supplied_source_equations = set(action.get("field_equations", {}).keys())
    assert_contains_all(supplied_source_equations, ["metric_equation", "scalar_equation", "vector_equation", "matter_equation"], "source equations")

    equations = perturbation.get("closure_equations", [])
    if len(equations) != 8:
        raise AssertionError("expected eight perturbation closure equation candidates")

    equation_ids = {item.get("equation_id") for item in equations}
    source_equations = {item.get("source_equation") for item in equations}
    assert_contains_all(equation_ids, REQUIRED_EQUATION_IDS, "closure equation ids")
    assert_contains_all(source_equations, REQUIRED_SOURCE_EQUATIONS, "closure source equations")

    for item in equations:
        if item.get("status") != "structural_candidate":
            raise AssertionError(f"equation status must be structural_candidate: {item}")
        if item.get("source_equation") != "combined_linearized_system" and item.get("source_equation") not in supplied_source_equations:
            raise AssertionError(f"source equation absent from action spec: {item}")
        if not item.get("structural_equation"):
            raise AssertionError(f"structural equation missing: {item}")
        if not item.get("coefficient_policy"):
            raise AssertionError(f"coefficient policy missing: {item}")
        if not item.get("observable_role"):
            raise AssertionError(f"observable role missing: {item}")

    observable_map = perturbation.get("observable_closure_map", [])
    observable_names = {item["observable"] for item in observable_map}
    assert_contains_all(observable_names, REQUIRED_OBSERVABLES, "observable closure map")

    vector_order = set(vector.get("observable_vector_order", []))
    for observable in REQUIRED_OBSERVABLES:
        if observable not in vector_order:
            raise AssertionError(f"observable not present in frozen vector order: {observable}")

    for item in observable_map:
        if not item.get("required_equations"):
            raise AssertionError(f"observable map missing required equations: {item}")
        for equation_id in item["required_equations"]:
            if equation_id not in equation_ids:
                raise AssertionError(f"observable references absent equation: {item}")
        if not item.get("status"):
            raise AssertionError(f"observable map missing status: {item}")

    background_equations = {item["equation_id"] for item in background.get("derived_background_equations", [])}
    assert_contains_all(background_equations, [
        "friedmann_constraint",
        "acceleration_equation",
        "scalar_background_equation",
        "vector_background_constraint",
        "matter_background_continuity",
    ], "background equations")

    for flag in [
        "symbolic_linearization_proved",
        "numerical_integration_supplied",
        "boltzmann_solver_supplied",
        "recombination_closure_supplied",
        "parameter_values_supplied",
        "initial_conditions_supplied",
        "empirical_validation_claimed",
        "likelihood_execution_claimed",
    ]:
        if perturbation.get(flag) is not False:
            raise AssertionError(f"{flag} must be false")

    assert_contains_all(perturbation["does_not_prove"], REQUIRED_DOES_NOT_PROVE, "perturbation does_not_prove")
    assert_contains_all(perturbation["next_missing_objects"], REQUIRED_NEXT, "perturbation next_missing_objects")

    if artifact.get("required_object_filled") != "PERTURBATION_CLOSURE_EQUATIONS":
        raise AssertionError("artifact required object mismatch")

    if artifact.get("root_blocker_removed") != "PERTURBATION_CLOSURE_EQUATIONS_NOT_SUPPLIED":
        raise AssertionError("wrong removed blocker")

    if artifact.get("new_root_blocker") != "NUMERICAL_PARAMETER_VECTOR_NOT_SUPPLIED":
        raise AssertionError("wrong new blocker")

    if artifact.get("check_result") != "PASS_STRUCTURAL_ONLY":
        raise AssertionError("artifact check result mismatch")

    assert_contains_all(artifact["boundary"], REQUIRED_BOUNDARY, "artifact boundary")
    assert_contains_all(artifact["does_not_prove"], REQUIRED_DOES_NOT_PROVE, "artifact does_not_prove")
    assert_contains_all(artifact["next_missing_objects"], REQUIRED_NEXT, "artifact next_missing_objects")

    for phrase in [
        "Status: `PERTURBATION_CLOSURE_EQUATIONS_SUPPLIED_STRUCTURAL_ONLY_NOT_NUMERICAL`",
        "`PERTURBATION_CLOSURE_EQUATIONS`",
        "`PERTURBATION_CLOSURE_EQUATIONS_NOT_SUPPLIED`",
        "`NUMERICAL_PARAMETER_VECTOR_NOT_SUPPLIED`",
        "`PASS_STRUCTURAL_ONLY`",
        "does not prove a full symbolic linearization",
        "does not supply empirical evidence",
        "any Clay problem",
    ]:
        if phrase not in doc:
            raise AssertionError(f"doc missing phrase: {phrase}")

    print("Perturbation closure equations verification OK.")
    print("Status: PERTURBATION_CLOSURE_EQUATIONS_SUPPLIED_STRUCTURAL_ONLY_NOT_NUMERICAL")
    print("Check result: PASS_STRUCTURAL_ONLY")
    print("New root blocker: NUMERICAL_PARAMETER_VECTOR_NOT_SUPPLIED")

if __name__ == "__main__":
    main()
