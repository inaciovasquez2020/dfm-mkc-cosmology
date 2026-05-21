import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
ARTIFACT = ROOT / "artifacts/repo_intake/dfm_mkc_schema_validation_blocker_certificate_2026_05_21.json"
DOC = ROOT / "docs/status/DFM_MKC_SCHEMA_VALIDATION_BLOCKER_CERTIFICATE_2026_05_21.md"

BLOCKING_REASONS = [
    "protocol_fields_not_validated",
    "schema_not_validated_against_protocol",
    "external_payload_not_verified",
    "numerical_data_vector_not_extracted",
    "covariance_matrix_not_extracted",
    "full_protocol_not_executed",
    "evidence_not_supplied",
    "slot_not_promoted",
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

    require(data["status"] == "SCHEMA_VALIDATION_BLOCKED_CANDIDATE_MAP_EXISTS", "bad status")
    require(data["candidate_map_exists"] is True, "candidate map must exist")
    require(data["candidate_field_record_count"] == data["required_protocol_field_count"], "candidate field count must match required field count")
    require(data["schema_validation_blocked"] is True, "schema validation must be blocked")
    require(data["blocking_reasons"] == BLOCKING_REASONS, "bad blocking reasons")
    require(data["numeric_arrays_read_or_attempted"] is True, "numeric arrays must be read or attempted upstream")
    require(data["protocol_gated_extraction_map_status"] == "PROTOCOL_GATED_EXTRACTION_MAP_ONLY_NOT_VALIDATION", "bad extraction map status")
    require(data["array_read_status"] == "SCHEMA_PROTOCOL_COMPARISON_WITH_ARRAY_READING_NOT_EVIDENCE", "bad array read status")
    require(data["target_status"] == "LEVEL_2_DATA_TARGET_ONLY_ACTDR6_NUMERICAL_DATA_NOT_SUPPLIED", "bad target status")
    require(data["protocol_fields_validated"] is False, "protocol fields must not be validated")
    require(data["schema_validated_against_protocol"] is False, "schema must not be protocol-validated")
    require(data["external_payload_verified"] is False, "external payload must not be verified")
    require(data["numerical_data_vector_extracted"] is False, "numerical vector must not be extracted")
    require(data["covariance_matrix_extracted"] is False, "covariance matrix must not be extracted")
    require(data["protocol_run"] is False, "protocol must not be run")
    require(data["evidence_supplied"] is False, "evidence must not be supplied")
    require(data["slot_promoted"] is False, "slot must not be promoted")
    require(data["does_not_prove"] == BOUNDARIES, "bad boundary list")

    for dep in data["depends_on"]:
        require((ROOT / dep).exists(), f"missing dependency: {dep}")

    for record in data["candidate_field_records"]:
        require(record["promotion_status"] == "CANDIDATE_ONLY_NOT_VALIDATED_NOT_EVIDENCE", "bad promotion status")
        require(record["validation_status"] == "NOT_SCHEMA_VALIDATED_AGAINST_PROTOCOL", "bad validation status")

    for token in [
        "SCHEMA_VALIDATION_BLOCKED_CANDIDATE_MAP_EXISTS",
        "Candidate protocol field map exists.",
        "Schema validation remains blocked.",
        *BLOCKING_REASONS,
        "Protocol fields are not validated.",
        "Schema is not validated against protocol.",
        "External payload is not verified.",
        "Numerical data vector is not extracted.",
        "Covariance matrix is not extracted.",
        "Full protocol execution is not performed.",
        "No evidence is supplied.",
        "No slot is promoted.",
        *BOUNDARIES,
    ]:
        require(token in doc, f"doc missing token: {token}")

    print("DFM-MKC schema validation blocker certificate verification OK.")
    print("Status: SCHEMA_VALIDATION_BLOCKED_CANDIDATE_MAP_EXISTS")

if __name__ == "__main__":
    main()
