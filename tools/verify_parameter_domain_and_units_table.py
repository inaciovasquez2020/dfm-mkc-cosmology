#!/usr/bin/env python3
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
ACTION_SPEC = ROOT / "specs" / "SUPPLIED_DFM_FIELD_EQUATIONS_AND_ACTION_FUNCTIONAL.json"
VARIATIONAL_SPEC = ROOT / "specs" / "VARIATIONAL_DERIVATION_CHECK.json"
PARAM_SPEC = ROOT / "specs" / "PARAMETER_DOMAIN_AND_UNITS_TABLE.json"
ARTIFACT = ROOT / "artifacts" / "repo_intake" / "parameter_domain_and_units_table_2026_05_22.json"
DOC = ROOT / "docs" / "status" / "PARAMETER_DOMAIN_AND_UNITS_TABLE_2026_05_22.md"

REQUIRED_BOUNDARY = [
    "does not prove physical correctness of the parameter choices",
    "does not supply numerical parameter values",
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
    "COSMOLOGICAL_REDUCTION_ANSATZ",
    "FROZEN_PREDICTION_VECTOR",
    "EXECUTED_DFM_VS_LAMBDA_CDM_COMPARISON",
    "INDEPENDENT_EMPIRICAL_VALIDATION",
]

REQUIRED_FIELDS = {
    "g_{mu nu}": 0,
    "phi": 1,
    "A_mu": 1,
    "Psi": "sector-dependent",
}

EXPECTED_PARAMETER_DIMENSIONS = {
    "M_Pl": 1,
    "Lambda_0": 4,
    "alpha_phi": 0,
    "m_phi": 1,
    "lambda_phi": 0,
    "alpha_A": 0,
    "m_A": 1,
    "beta_phi_A": 0,
    "xi_phi": 0,
    "xi_A": 0,
    "gamma_m": -1,
}

POSITIVE_PARAMETERS = {"M_Pl", "alpha_phi", "alpha_A"}
NONNEGATIVE_PARAMETERS = {"m_phi", "lambda_phi", "m_A"}

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
    artifact = load_json(ARTIFACT)

    if not DOC.exists():
        raise AssertionError(f"missing file: {DOC}")
    doc = DOC.read_text()

    if action.get("object_id") != "FILLED_SUPPLIED_DFM_FIELD_EQUATIONS_AND_ACTION_FUNCTIONAL":
        raise AssertionError("action input object mismatch")

    if variation.get("object_id") != "VARIATIONAL_DERIVATION_CHECK":
        raise AssertionError("variational input object mismatch")

    if params.get("object_id") != "PARAMETER_DOMAIN_AND_UNITS_TABLE":
        raise AssertionError("wrong parameter object_id")

    if params.get("status") != "PARAMETER_DOMAIN_AND_UNITS_TABLE_SUPPLIED_STRUCTURAL_ONLY":
        raise AssertionError("wrong parameter status")

    if params.get("check_result") != "PASS_STRUCTURAL_ONLY":
        raise AssertionError("wrong parameter check_result")

    unit_system = params.get("unit_system", {})
    if unit_system.get("name") != "natural_units":
        raise AssertionError("unit system must be natural_units")

    assert_contains_all(unit_system.get("assumptions", []), [
        "c = 1",
        "hbar = 1",
        "spacetime_dimension = 4",
        "action_dimension = 0",
        "lagrangian_density_mass_dimension = 4",
    ], "unit assumptions")

    field_dims = {item["symbol"]: item["mass_dimension"] for item in params.get("field_dimensions", [])}
    if field_dims != REQUIRED_FIELDS:
        raise AssertionError(f"field dimension mismatch: {field_dims}")

    action_couplings = set(action.get("coupling_constants", []))
    table = params.get("parameter_table", [])
    table_symbols = [item.get("symbol") for item in table]

    if len(table_symbols) != len(set(table_symbols)):
        raise AssertionError("duplicate parameter symbol in table")

    if set(table_symbols) != action_couplings:
        raise AssertionError(f"parameter table does not match action couplings: table={sorted(table_symbols)} action={sorted(action_couplings)}")

    for item in table:
        symbol = item["symbol"]
        if item.get("mass_dimension") != EXPECTED_PARAMETER_DIMENSIONS[symbol]:
            raise AssertionError(f"wrong mass dimension for {symbol}")
        if not item.get("domain"):
            raise AssertionError(f"missing domain for {symbol}")
        if not item.get("constraint"):
            raise AssertionError(f"missing constraint for {symbol}")
        if not item.get("appears_in"):
            raise AssertionError(f"missing appears_in for {symbol}")

    constraints = {item["symbol"]: item["constraint"] for item in table}
    for symbol in POSITIVE_PARAMETERS:
        if ">" not in constraints[symbol]:
            raise AssertionError(f"{symbol} must have a positive constraint")
    for symbol in NONNEGATIVE_PARAMETERS:
        if ">=" not in constraints[symbol]:
            raise AssertionError(f"{symbol} must have a nonnegative constraint")

    for flag in [
        "physical_correctness_claimed",
        "empirical_validation_claimed",
        "prediction_vector_claimed",
        "likelihood_execution_claimed",
    ]:
        if params.get(flag) is not False:
            raise AssertionError(f"{flag} must be false")

    assert_contains_all(params["does_not_prove"], REQUIRED_DOES_NOT_PROVE, "params does_not_prove")
    assert_contains_all(params["next_missing_objects"], REQUIRED_NEXT, "params next_missing_objects")

    if artifact.get("required_object_filled") != "PARAMETER_DOMAIN_AND_UNITS_TABLE":
        raise AssertionError("artifact required object mismatch")

    if artifact.get("root_blocker_removed") != "PARAMETER_DOMAIN_AND_UNITS_TABLE_NOT_SUPPLIED":
        raise AssertionError("wrong removed blocker")

    if artifact.get("new_root_blocker") != "COSMOLOGICAL_REDUCTION_ANSATZ_NOT_SUPPLIED":
        raise AssertionError("wrong new blocker")

    if artifact.get("check_result") != "PASS_STRUCTURAL_ONLY":
        raise AssertionError("artifact check result mismatch")

    assert_contains_all(artifact["boundary"], REQUIRED_BOUNDARY, "artifact boundary")
    assert_contains_all(artifact["does_not_prove"], REQUIRED_DOES_NOT_PROVE, "artifact does_not_prove")
    assert_contains_all(artifact["next_missing_objects"], REQUIRED_NEXT, "artifact next_missing_objects")

    for phrase in [
        "Status: `PARAMETER_DOMAIN_AND_UNITS_TABLE_SUPPLIED_STRUCTURAL_ONLY`",
        "`PARAMETER_DOMAIN_AND_UNITS_TABLE`",
        "`PARAMETER_DOMAIN_AND_UNITS_TABLE_NOT_SUPPLIED`",
        "`COSMOLOGICAL_REDUCTION_ANSATZ_NOT_SUPPLIED`",
        "`PASS_STRUCTURAL_ONLY`",
        "does not prove physical correctness of the parameter choices",
        "does not supply empirical evidence",
        "any Clay problem",
    ]:
        if phrase not in doc:
            raise AssertionError(f"doc missing phrase: {phrase}")

    print("Parameter domain and units table verification OK.")
    print("Status: PARAMETER_DOMAIN_AND_UNITS_TABLE_SUPPLIED_STRUCTURAL_ONLY")
    print("Check result: PASS_STRUCTURAL_ONLY")
    print("New root blocker: COSMOLOGICAL_REDUCTION_ANSATZ_NOT_SUPPLIED")

if __name__ == "__main__":
    main()
