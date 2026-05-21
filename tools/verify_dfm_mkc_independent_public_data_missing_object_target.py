import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
ARTIFACT = ROOT / "artifacts/repo_intake/dfm_mkc_independent_public_data_missing_object_target_2026_05_21.json"
DOC = ROOT / "docs/status/DFM_MKC_INDEPENDENT_PUBLIC_DATA_MISSING_OBJECT_TARGET_2026_05_21.md"

REQUIRED_FIELDS = [
    "dataset_name",
    "data_vector",
    "covariance_matrix",
    "mask",
    "publication_date",
    "source_reference",
    "independent_team",
    "independence_witness",
    "not_actdr6_duplicate_witness",
    "data_freeze_lock",
]

DEPENDENCIES = [
    "artifacts/repo_intake/dfm_mkc_actdr6_numerical_data_missing_object_target_2026_05_21.json",
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

    require(data["status"] == "LEVEL_3_DATA_TARGET_ONLY_INDEPENDENT_PUBLIC_DATA_NOT_SUPPLIED", "bad status")
    require(data["target_object"] == "IndependentPublicData", "bad target object")
    require(data["logical_position"] == "level_3_independent_validation_blocker_for_multi_dataset_survival", "bad logical position")
    require(data["depends_on"] == DEPENDENCIES, "bad dependency list")
    require(data["required_data_payload_fields"] == REQUIRED_FIELDS, "bad required field list")
    require(data["must_be_public"] is True, "must require public data")
    require(data["must_be_independent_from_actdr6"] is True, "must require ACT DR6 independence")
    require(data["must_use_same_frozen_prediction_vector"] is True, "must require same frozen vector")
    require(data["must_use_locked_or_predeclared_protocol"] is True, "must require locked/predeclared protocol")
    require(data["independent_public_data_supplied"] is False, "independent public data must not be supplied")
    require(data["protocol_run"] is False, "protocol must not be run")
    require(data["evidence_supplied"] is False, "evidence must not be supplied")
    require(data["slot_promoted"] is False, "slot must not be promoted")
    require(data["does_not_prove"] == BOUNDARIES, "bad boundary list")

    for dep in DEPENDENCIES:
        require((ROOT / dep).exists(), f"missing dependency: {dep}")
        require(dep in doc, f"doc missing dependency: {dep}")

    for token in [
        "LEVEL_3_DATA_TARGET_ONLY_INDEPENDENT_PUBLIC_DATA_NOT_SUPPLIED",
        "IndependentPublicData",
        *REQUIRED_FIELDS,
        "Planck",
        "WMAP",
        "SPT-3G",
        "Independent public data is not supplied.",
        "No protocol run is performed.",
        "No evidence is supplied.",
        "No slot is promoted.",
        *BOUNDARIES,
    ]:
        require(token in doc, f"doc missing token: {token}")

    print("DFM-MKC independent public data missing object target verification OK.")
    print("Status: LEVEL_3_DATA_TARGET_ONLY_INDEPENDENT_PUBLIC_DATA_NOT_SUPPLIED")

if __name__ == "__main__":
    main()
