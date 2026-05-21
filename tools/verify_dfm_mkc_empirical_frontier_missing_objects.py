import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
ARTIFACT = ROOT / "artifacts/repo_intake/dfm_mkc_empirical_frontier_missing_objects_2026_05_21.json"
DOC = ROOT / "docs/status/DFM_MKC_EMPIRICAL_FRONTIER_MISSING_OBJECTS_2026_05_21.md"

BLOCKERS = [
    "FrozenDFMMKCAxioms",
    "ACTDR6_NumericalData_Unfixed",
    "IndependentPublicData",
]

LEVEL_2 = [
    "FrozenDFMMKCAxioms",
    "ACTDR6_NumericalData_Unfixed",
]

LEVEL_3 = [
    "FrozenDFMMKCAxioms",
    "ACTDR6_NumericalData_Unfixed",
    "IndependentPublicData",
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

    require(data["status"] == "FRONTIER_SHIFT_MISSING_OBJECTS_EXPLICIT", "bad status")
    require(data["blocking_objects"] == BLOCKERS, "bad blocker list")
    require(data["weakest_sufficient_level_2"] == LEVEL_2, "bad level 2 object set")
    require(data["weakest_sufficient_level_3"] == LEVEL_3, "bad level 3 object set")
    require(data["protocol_locked"] is True, "protocol must be locked")
    require(data["protocol_run"] is False, "protocol must not be run")
    require(data["fixture_schema_valid"] is True, "fixture schema must be valid")
    require(data["evidence_supplied"] is False, "must not supply evidence")
    require(data["slot_promoted"] is False, "must not promote slot")
    require(data["does_not_prove"] == BOUNDARIES, "bad boundary list")

    for token in [
        "LOCKED_FROZEN_NOT_RUN",
        "FIXTURE_ONLY_AWAITING_DATA",
        "FRAMEWORK_EXISTS_MISSING_PUBLIC_DATA",
        *BLOCKERS,
        *BOUNDARIES,
        "No evidence is supplied.",
        "No slot is promoted.",
    ]:
        require(token in doc, f"doc missing token: {token}")

    print("DFM-MKC empirical frontier missing objects verification OK.")
    print("Status: FRONTIER_SHIFT_MISSING_OBJECTS_EXPLICIT")

if __name__ == "__main__":
    main()
