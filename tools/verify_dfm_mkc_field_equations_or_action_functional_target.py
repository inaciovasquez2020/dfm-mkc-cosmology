#!/usr/bin/env python3
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
ARTIFACT = ROOT / "artifacts/repo_intake/dfm_mkc_field_equations_or_action_functional_target_2026_05_21.json"
DOC = ROOT / "docs/status/DFM_MKC_FIELD_EQUATIONS_OR_ACTION_FUNCTIONAL_TARGET_2026_05_21.md"

EXPECTED_STATUS = "FIELD_EQUATIONS_OR_ACTION_FUNCTIONAL_TARGET_ONLY_NOT_SUPPLIED"

EXPECTED_FIELDS = {
    "primitive_fields",
    "background_geometry",
    "action_functional_or_closed_field_equations",
    "variational_derivation_or_direct_dynamical_law",
    "matter_coupling_rule",
    "dark_sector_coupling_rule",
    "stress_energy_tensor_rule",
    "gauge_or_constraint_structure",
    "conservation_laws",
    "initial_boundary_conditions",
    "parameter_table",
    "dimensional_units",
    "lambda_cdm_limit_or_explicit_nonlimit",
    "observable_projection_rules",
}

EXPECTED_DOWNSTREAM = {
    "DFM_PARAMETER_MAP",
    "DFM_OBSERVABLE_PREDICTION_RULES",
    "DFM_FROZEN_PREDICTION_VECTOR",
    "DFM_LIKELIHOOD_RULE",
    "DFM_HOLDOUT_SPLIT",
    "DFM_VS_LAMBDA_CDM_COMPARISON",
}

EXPECTED_BOUNDARY = [
    "Target schema only.",
    "Does not supply DFM field equations.",
    "Does not supply DFM action functional.",
    "Does not supply Euler-Lagrange equations.",
    "Does not supply matter coupling.",
    "Does not supply dark-sector coupling.",
    "Does not supply stress-energy tensor.",
    "Does not supply conservation law proof.",
    "Does not supply observable prediction rules.",
    "Does not supply frozen predictions.",
    "Does not execute any likelihood.",
    "Does not produce empirical evidence.",
    "Does not prove DFM.",
    "Does not disprove Lambda-CDM.",
    "Does not replace CDM.",
]

EXPECTED_DOES_NOT_PROVE = {
    "DFM",
    "Lambda-CDM failure",
    "CDM replacement",
    "dark-energy resolution",
    "dark-matter resolution",
    "Nobel-level physical discovery",
    "any Clay problem",
}

def load_json(path: Path) -> dict:
    if not path.exists():
        raise SystemExit(f"missing file: {path}")
    return json.loads(path.read_text())

def verify_artifact(data: dict) -> None:
    assert data["artifact"] == "DFM_MKC_FIELD_EQUATIONS_OR_ACTION_FUNCTIONAL_TARGET"
    assert data["date"] == "2026-05-21"
    assert data["status"] == EXPECTED_STATUS
    assert data["claim_level"] == "target_schema_only"
    assert data["field_equations_supplied"] is False
    assert data["action_functional_supplied"] is False
    assert data["euler_lagrange_derivation_supplied"] is False
    assert data["stress_energy_rule_supplied"] is False
    assert data["observable_prediction_map_enabled"] is False
    assert data["root_blocker"] == "DFM_FIELD_EQUATIONS_OR_ACTION_FUNCTIONAL_NOT_SUPPLIED"

    assert EXPECTED_FIELDS <= set(data["required_equation_object_fields"])
    assert EXPECTED_DOWNSTREAM <= set(data["downstream_blocked_objects"])

    boundary = "\n".join(data["boundary"])
    for token in EXPECTED_BOUNDARY:
        assert token in boundary

    assert EXPECTED_DOES_NOT_PROVE <= set(data["does_not_prove"])

def verify_doc() -> None:
    if not DOC.exists():
        raise SystemExit(f"missing status doc: {DOC}")
    doc = DOC.read_text()
    assert EXPECTED_STATUS in doc
    assert "DFM_FIELD_EQUATIONS_OR_ACTION_FUNCTIONAL_NOT_SUPPLIED" in doc
    for token in EXPECTED_BOUNDARY:
        assert token in doc

def main() -> None:
    data = load_json(ARTIFACT)
    verify_artifact(data)
    verify_doc()
    print("DFM-MKC field equations or action functional target verification OK.")
    print(f"Status: {data['status']}")
    print(f"Root blocker: {data['root_blocker']}")

if __name__ == "__main__":
    main()
