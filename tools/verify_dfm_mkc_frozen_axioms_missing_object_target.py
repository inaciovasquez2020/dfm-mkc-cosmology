import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
ARTIFACT = ROOT / "artifacts/repo_intake/dfm_mkc_frozen_axioms_missing_object_target_2026_05_21.json"
DOC = ROOT / "docs/status/DFM_MKC_FROZEN_AXIOMS_MISSING_OBJECT_TARGET_2026_05_21.md"

REQUIRED_FIELDS = [
    "axiom_identifier",
    "formal_statement",
    "allowed_symbols",
    "normalization_convention",
    "parameter_dependency_rule",
    "prediction_derivation_role",
    "freeze_hash",
]

BOUNDARIES = [
    "DFM-MKC",
    "Lambda-CDM failure",
    "ACT/DES holdout survival",
    "independent empirical validation",
    "dark-energy resolution",
    "dark-matter resolution",
    "Nobel-level physical discovery",
    "any Clay problem",
]

def require(condition, message):
    if not condition:
        raise AssertionError(message)

def main():
    data = json.loads(ARTIFACT.read_text())
    doc = DOC.read_text()

    require(data["status"] == "ROOT_BLOCKER_TARGET_ONLY_AXIOMS_NOT_SUPPLIED", "bad status")
    require(data["target_object"] == "FrozenDFMMKCAxioms", "bad target object")
    require(data["logical_position"] == "root_blocker_for_prediction_generation", "bad logical position")
    require(data["required_downstream_map"] == ["DeterministicDerivationMap", "NonemptyNumericPredictionList"], "bad downstream map")
    require(data["required_axiom_payload_fields"] == REQUIRED_FIELDS, "bad required axiom fields")
    require(data["axioms_supplied"] is False, "axioms must not be supplied")
    require(data["prediction_vector_supplied"] is False, "prediction vector must not be supplied")
    require(data["evidence_supplied"] is False, "evidence must not be supplied")
    require(data["slot_promoted"] is False, "slot must not be promoted")
    require(data["does_not_prove"] == BOUNDARIES, "bad boundary list")

    for token in [
        "ROOT_BLOCKER_TARGET_ONLY_AXIOMS_NOT_SUPPLIED",
        "FrozenDFMMKCAxioms",
        "DeterministicDerivationMap",
        "NonemptyNumericPredictionList",
        *REQUIRED_FIELDS,
        "Axioms are not supplied.",
        "Prediction vector is not supplied.",
        "No evidence is supplied.",
        "No slot is promoted.",
        *BOUNDARIES,
    ]:
        require(token in doc, f"doc missing token: {token}")

    print("DFM-MKC frozen axioms missing object target verification OK.")
    print("Status: ROOT_BLOCKER_TARGET_ONLY_AXIOMS_NOT_SUPPLIED")

if __name__ == "__main__":
    main()
