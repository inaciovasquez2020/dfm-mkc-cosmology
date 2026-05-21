import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
ARTIFACT = ROOT / "artifacts/repo_intake/dfm_mkc_public_data_payload_verification_layer_2026_05_21.json"
DOC = ROOT / "docs/status/DFM_MKC_PUBLIC_DATA_PAYLOAD_VERIFICATION_LAYER_2026_05_21.md"

DEPENDENCIES = [
    "artifacts/repo_intake/dfm_mkc_public_data_source_seek_registry_2026_05_21.json",
    "artifacts/repo_intake/dfm_mkc_terminal_blocker_exhaustion_certificate_2026_05_21.json",
    "artifacts/repo_intake/dfm_mkc_actdr6_numerical_data_missing_object_target_2026_05_21.json",
    "artifacts/repo_intake/dfm_mkc_independent_public_data_missing_object_target_2026_05_21.json",
]

PAYLOAD_CLASSES = [
    "ACTDR6_NumericalData_Unfixed",
    "IndependentPublicData",
]

REQUIRED_FIELDS = [
    "source_name",
    "source_url",
    "download_timestamp_utc",
    "local_path",
    "file_size_bytes",
    "sha256",
    "license_or_terms_reference",
    "payload_role",
    "expected_schema",
    "checksum_verified",
    "schema_validated",
    "external_payload_verified",
]

PROMOTION_REQUIREMENTS = [
    "payload_exists_locally",
    "sha256_recorded",
    "file_size_recorded",
    "source_url_recorded",
    "checksum_verified_true",
    "schema_validated_true",
    "external_payload_verified_true",
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

    require(data["status"] == "PAYLOAD_VERIFICATION_LAYER_ONLY_NO_DATA_IMPORTED", "bad status")
    require(data["depends_on"] == DEPENDENCIES, "bad dependency list")
    require(data["payload_classes"] == PAYLOAD_CLASSES, "bad payload classes")
    require(data["required_verification_fields"] == REQUIRED_FIELDS, "bad required verification fields")
    require(data["promotion_requirements"] == PROMOTION_REQUIREMENTS, "bad promotion requirements")
    require(data["data_imported"] is False, "data must not be imported")
    require(data["payload_verified"] is False, "payload must not be verified")
    require(data["protocol_run"] is False, "protocol must not be run")
    require(data["evidence_supplied"] is False, "evidence must not be supplied")
    require(data["slot_promoted"] is False, "slot must not be promoted")
    require(data["does_not_prove"] == BOUNDARIES, "bad boundary list")

    for dep in DEPENDENCIES:
        require((ROOT / dep).exists(), f"missing dependency: {dep}")
        require(dep in doc, f"doc missing dependency: {dep}")

    for token in [
        "PAYLOAD_VERIFICATION_LAYER_ONLY_NO_DATA_IMPORTED",
        *PAYLOAD_CLASSES,
        *REQUIRED_FIELDS,
        *PROMOTION_REQUIREMENTS,
        "Data is not imported.",
        "Payload is not verified.",
        "No protocol run is performed.",
        "No evidence is supplied.",
        "No slot is promoted.",
        *BOUNDARIES,
    ]:
        require(token in doc, f"doc missing token: {token}")

    print("DFM-MKC public data payload verification layer verification OK.")
    print("Status: PAYLOAD_VERIFICATION_LAYER_ONLY_NO_DATA_IMPORTED")

if __name__ == "__main__":
    main()
