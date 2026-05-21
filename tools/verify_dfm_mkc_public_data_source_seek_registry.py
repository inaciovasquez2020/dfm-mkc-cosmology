import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
ARTIFACT = ROOT / "artifacts/repo_intake/dfm_mkc_public_data_source_seek_registry_2026_05_21.json"
DOC = ROOT / "docs/status/DFM_MKC_PUBLIC_DATA_SOURCE_SEEK_REGISTRY_2026_05_21.md"

TARGET_BLOCKERS = [
    "ACTDR6_NumericalData_Unfixed",
    "IndependentPublicData",
]

REQUIRED_SOURCE_NAMES = [
    "ACT DR6 official data products page",
    "NASA LAMBDA ACT DR6.02 release",
    "ACT DR6 CMB-only lite likelihood",
    "ACT DR6 multi-frequency likelihood",
    "ACT DR6 lensing likelihood data",
    "Planck Legacy Archive / Planck 2018 likelihood",
    "Planck PR3 ancillary data at IRSA",
    "WMAP LAMBDA data products",
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

    require(data["status"] == "SOURCE_POINTERS_ONLY_DATA_NOT_IMPORTED", "bad status")
    require(data["target_blockers"] == TARGET_BLOCKERS, "bad target blockers")
    require(data["data_imported"] is False, "data must not be imported")
    require(data["external_payload_verified"] is False, "external payload must not be verified")
    require(data["protocol_run"] is False, "protocol must not be run")
    require(data["evidence_supplied"] is False, "evidence must not be supplied")
    require(data["slot_promoted"] is False, "slot must not be promoted")
    require(data["does_not_prove"] == BOUNDARIES, "bad boundary list")

    source_names = [x["name"] for x in data["actdr6_source_candidates"]] + [
        x["name"] for x in data["independent_public_data_candidates"]
    ]
    for name in REQUIRED_SOURCE_NAMES:
        require(name in source_names, f"missing source candidate: {name}")
        require(name in doc, f"doc missing source candidate: {name}")

    for token in [
        "SOURCE_POINTERS_ONLY_DATA_NOT_IMPORTED",
        *TARGET_BLOCKERS,
        "Data is not imported.",
        "External payload is not verified.",
        "No protocol run is performed.",
        "No evidence is supplied.",
        "No slot is promoted.",
        *BOUNDARIES,
    ]:
        require(token in doc, f"doc missing token: {token}")

    print("DFM-MKC public data source seek registry verification OK.")
    print("Status: SOURCE_POINTERS_ONLY_DATA_NOT_IMPORTED")

if __name__ == "__main__":
    main()
