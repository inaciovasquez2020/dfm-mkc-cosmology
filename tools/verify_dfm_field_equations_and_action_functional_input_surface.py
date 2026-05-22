#!/usr/bin/env python3
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
ARTIFACT = ROOT / "artifacts/repo_intake/dfm_field_equations_and_action_functional_input_surface_2026_05_21.json"
DOC = ROOT / "docs/status/DFM_FIELD_EQUATIONS_AND_ACTION_FUNCTIONAL_INPUT_SURFACE_2026_05_21.md"
TEMPLATE = ROOT / "specs/DFM_FIELD_EQUATIONS_AND_ACTION_FUNCTIONAL.SUPPLIED_TEMPLATE.md"

REQUIRED_SECTIONS = {
    "primitive_fields",
    "geometry_assumptions",
    "action_functional",
    "variation_variables",
    "euler_lagrange_derivation",
    "field_equations",
    "source_terms",
    "matter_coupling_rule",
    "boundary_conditions",
    "parameter_definitions",
    "observable_map_hooks",
    "no_post_hoc_freeze_statement",
}

BOUNDARY = [
    "Does not supply DFM field equations.",
    "Does not supply DFM action functional.",
    "Does not supply variational derivation.",
    "Does not supply Euler-Lagrange consistency proof.",
    "Does not supply DFM source terms.",
    "Does not supply DFM matter coupling rule.",
    "Does not supply DFM boundary conditions.",
    "Does not supply DFM prediction map.",
    "Does not execute any likelihood.",
    "Does not produce empirical evidence.",
    "Does not prove DFM.",
    "Does not disprove Lambda-CDM.",
    "Does not replace CDM.",
    "Does not claim final cosmology closure.",
]

def main():
    data = json.loads(ARTIFACT.read_text())
    doc = DOC.read_text()
    template = TEMPLATE.read_text()

    assert data["artifact"] == "DFM_FIELD_EQUATIONS_AND_ACTION_FUNCTIONAL_INPUT_SURFACE"
    assert data["status"] == "INPUT_SURFACE_ONLY_OBJECT_NOT_SUPPLIED"
    assert data["claim_level"] == "schema_only"
    assert data["required_object"] == "DFM_FIELD_EQUATIONS_AND_ACTION_FUNCTIONAL"
    assert data["root_blocker"] == "DFM_FIELD_EQUATIONS_AND_ACTION_FUNCTIONAL_NOT_SUPPLIED"
    assert data["next_missing_object"] == "SUPPLIED_DFM_FIELD_EQUATIONS_AND_ACTION_FUNCTIONAL"

    assert data["object_supplied"] is False
    assert data["field_equations_supplied"] is False
    assert data["action_functional_supplied"] is False
    assert data["variational_derivation_supplied"] is False
    assert data["euler_lagrange_consistency_supplied"] is False
    assert data["source_terms_supplied"] is False
    assert data["matter_coupling_rule_supplied"] is False
    assert data["boundary_conditions_supplied"] is False
    assert data["prediction_map_supplied"] is False
    assert data["likelihood_executed"] is False
    assert data["empirical_evidence_supplied"] is False

    assert REQUIRED_SECTIONS <= set(data["required_sections"])

    boundary = "\n".join(data["boundary"])
    for token in BOUNDARY:
        assert token in boundary
        assert token in doc
        assert token in template

    does_not_prove = set(data["does_not_prove"])
    assert "DFM" in does_not_prove
    assert "Lambda-CDM failure" in does_not_prove
    assert "CDM replacement" in does_not_prove
    assert "final cosmology closure" in does_not_prove
    assert "any Clay problem" in does_not_prove

    print("DFM field equations and action functional input surface verification OK.")
    print(f"Status: {data['status']}")
    print(f"Required object: {data['required_object']}")
    print(f"Root blocker: {data['root_blocker']}")
    print(f"Next missing object: {data['next_missing_object']}")

if __name__ == "__main__":
    main()
