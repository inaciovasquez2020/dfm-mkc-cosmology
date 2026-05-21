import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
ARTIFACT = ROOT / "artifacts/repo_intake/dfm_mkc_terminal_blocker_exhaustion_certificate_2026_05_21.json"
DOC = ROOT / "docs/status/DFM_MKC_TERMINAL_BLOCKER_EXHAUSTION_CERTIFICATE_2026_05_21.md"

TERMINAL_BLOCKERS = [
    "FrozenDFMMKCAxioms",
    "ACTDR6_NumericalData_Unfixed",
    "IndependentPublicData",
]

TARGET_ARTIFACTS = [
    "artifacts/repo_intake/dfm_mkc_frozen_axioms_missing_object_target_2026_05_21.json",
    "artifacts/repo_intake/dfm_mkc_actdr6_numerical_data_missing_object_target_2026_05_21.json",
    "artifacts/repo_intake/dfm_mkc_independent_public_data_missing_object_target_2026_05_21.json",
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

    require(data["status"] == "TERMINAL_BLOCKERS_EXPLICIT_NO_SUPPLIED_OBJECTS", "bad status")
    require(data["terminal_blockers"] == TERMINAL_BLOCKERS, "bad terminal blocker list")
    require(data["target_artifacts"] == TARGET_ARTIFACTS, "bad target artifact list")
    require(data["exhaustion_claim"] == "all_current_logical_missing_objects_have_target_artifacts", "bad exhaustion claim")
    require(data["remaining_progress_requires_supplied_object"] is True, "remaining progress must require supplied object")
    require(data["schema_only_progress_exhausted"] is True, "schema-only progress must be exhausted")
    require(data["frozen_axioms_supplied"] is False, "frozen axioms must not be supplied")
    require(data["actdr6_numerical_data_supplied"] is False, "ACT DR6 numerical data must not be supplied")
    require(data["independent_public_data_supplied"] is False, "independent public data must not be supplied")
    require(data["evidence_supplied"] is False, "evidence must not be supplied")
    require(data["slot_promoted"] is False, "slot must not be promoted")
    require(data["does_not_prove"] == BOUNDARIES, "bad boundary list")

    for artifact in TARGET_ARTIFACTS:
        require((ROOT / artifact).exists(), f"missing target artifact: {artifact}")
        require(artifact in doc, f"doc missing target artifact: {artifact}")

    for token in [
        "TERMINAL_BLOCKERS_EXPLICIT_NO_SUPPLIED_OBJECTS",
        *TERMINAL_BLOCKERS,
        "all current logical missing objects have target artifacts",
        "Remaining progress requires supplied object: true.",
        "Schema-only progress exhausted: true.",
        "Frozen axioms are not supplied.",
        "ACT DR6 numerical data is not supplied.",
        "Independent public data is not supplied.",
        "No evidence is supplied.",
        "No slot is promoted.",
        *BOUNDARIES,
    ]:
        require(token in doc, f"doc missing token: {token}")

    print("DFM-MKC terminal blocker exhaustion certificate verification OK.")
    print("Status: TERMINAL_BLOCKERS_EXPLICIT_NO_SUPPLIED_OBJECTS")

if __name__ == "__main__":
    main()
