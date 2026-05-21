import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
ARTIFACT = ROOT / "artifacts/repo_intake/dfm_mkc_actdr6_numerical_data_missing_object_target_2026_05_21.json"
DOC = ROOT / "docs/status/DFM_MKC_ACTDR6_NUMERICAL_DATA_MISSING_OBJECT_TARGET_2026_05_21.md"

REQUIRED_FIELDS = [
    "data_vector",
    "covariance_matrix",
    "mask",
    "likelihood_rule",
    "statistical_threshold",
    "protocol_hash",
    "actdr6_release_date",
    "data_freeze_lock",
]

DEPENDENCIES = [
    "artifacts/repo_intake/dfm_mkc_frozen_axioms_missing_object_target_2026_05_21.json",
    "artifacts/repo_intake/dfm_mkc_empirical_frontier_missing_objects_2026_05_21.json",
    "artifacts/repo_intake/dfm_mkc_full_closure_blocker_certificate_2026_05_21.json",
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

    require(data["status"] == "LEVEL_2_DATA_TARGET_ONLY_ACTDR6_NUMERICAL_DATA_NOT_SUPPLIED", "bad status")
    require(data["target_object"] == "ACTDR6_NumericalData_Unfixed", "bad target object")
    require(data["logical_position"] == "level_2_empirical_blocker_for_locked_protocol_execution", "bad logical position")
    require(data["depends_on"] == DEPENDENCIES, "bad dependency list")
    require(data["required_data_payload_fields"] == REQUIRED_FIELDS, "bad required field list")
    require(data["must_match_locked_protocol"] is True, "must require locked protocol match")
    require(data["protocol_reference"] == "act_dr6_residual_evaluation_protocol_2026_05_20.json", "bad protocol reference")
    require(data["real_numerical_data_supplied"] is False, "real ACT DR6 numerical data must not be supplied")
    require(data["fixture_only"] is False, "target must not be a fixture")
    require(data["protocol_run"] is False, "protocol must not be run")
    require(data["evidence_supplied"] is False, "evidence must not be supplied")
    require(data["slot_promoted"] is False, "slot must not be promoted")
    require(data["does_not_prove"] == BOUNDARIES, "bad boundary list")

    for dep in DEPENDENCIES:
        require((ROOT / dep).exists(), f"missing dependency: {dep}")
        require(dep in doc, f"doc missing dependency: {dep}")

    for token in [
        "LEVEL_2_DATA_TARGET_ONLY_ACTDR6_NUMERICAL_DATA_NOT_SUPPLIED",
        "ACTDR6_NumericalData_Unfixed",
        "act_dr6_residual_evaluation_protocol_2026_05_20.json",
        *REQUIRED_FIELDS,
        "Real ACT DR6 numerical data is not supplied.",
        "No protocol run is performed.",
        "No evidence is supplied.",
        "No slot is promoted.",
        *BOUNDARIES,
    ]:
        require(token in doc, f"doc missing token: {token}")

    print("DFM-MKC ACT DR6 numerical data missing object target verification OK.")
    print("Status: LEVEL_2_DATA_TARGET_ONLY_ACTDR6_NUMERICAL_DATA_NOT_SUPPLIED")

if __name__ == "__main__":
    main()
