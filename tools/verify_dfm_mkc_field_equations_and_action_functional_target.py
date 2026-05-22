#!/usr/bin/env python3
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
ARTIFACT = ROOT / "artifacts/repo_intake/dfm_mkc_field_equations_and_action_functional_target_2026_05_21.json"
DOC = ROOT / "docs/status/DFM_MKC_FIELD_EQUATIONS_AND_ACTION_FUNCTIONAL_TARGET_2026_05_21.md"

REQUIRED = {
    "DFM_FIELD_EQUATIONS_SUPPLIED",
    "DFM_ACTION_FUNCTIONAL_SUPPLIED",
    "DFM_VARIATIONAL_DERIVATION_MAP",
    "DFM_EULER_LAGRANGE_CONSISTENCY_CHECK",
    "DFM_SOURCE_TERMS_SUPPLIED",
    "DFM_MATTER_COUPLING_RULE_SUPPLIED",
    "DFM_BOUNDARY_CONDITIONS_SUPPLIED"
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
    "Does not claim final cosmology closure."
]

def main():
    data = json.loads(ARTIFACT.read_text())
    doc = DOC.read_text()

    assert data["artifact"] == "DFM_MKC_FIELD_EQUATIONS_AND_ACTION_FUNCTIONAL_TARGET"
    assert data["status"] == "FIELD_EQUATIONS_AND_ACTION_FUNCTIONAL_TARGET_ONLY_NOT_SUPPLIED"
    assert data["claim_level"] == "target_only"
    assert data["root_blocker"] == "DFM_FIELD_EQUATIONS_AND_ACTION_FUNCTIONAL_NOT_SUPPLIED"
    assert data["required_object"] == "DFM_FIELD_EQUATIONS_AND_ACTION_FUNCTIONAL"
    assert REQUIRED <= set(data["requires"])

    assert data["supplied"] is False
    assert data["field_equations_supplied"] is False
    assert data["action_functional_supplied"] is False
    assert data["variational_derivation_supplied"] is False
    assert data["prediction_map_supplied"] is False
    assert data["likelihood_executed"] is False
    assert data["empirical_evidence_supplied"] is False

    boundary = "\n".join(data["boundary"])
    for token in BOUNDARY:
        assert token in boundary
        assert token in doc

    does_not_prove = set(data["does_not_prove"])
    assert "DFM" in does_not_prove
    assert "Lambda-CDM failure" in does_not_prove
    assert "CDM replacement" in does_not_prove
    assert "final cosmology closure" in does_not_prove
    assert "any Clay problem" in does_not_prove

    print("DFM-MKC field equations and action functional target verification OK.")
    print(f"Status: {data['status']}")
    print(f"Root blocker: {data['root_blocker']}")
    print(f"Required object: {data['required_object']}")

if __name__ == "__main__":
    main()
