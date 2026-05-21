import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
ARTIFACT = ROOT / "artifacts/repo_intake/dfm_mkc_protocol_gated_extraction_map_2026_05_21.json"
DOC = ROOT / "docs/status/DFM_MKC_PROTOCOL_GATED_EXTRACTION_MAP_2026_05_21.md"

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

    require(data["status"] == "PROTOCOL_GATED_EXTRACTION_MAP_ONLY_NOT_VALIDATION", "bad status")
    require(data["candidate_mapping_performed"] is True, "candidate mapping must be performed")
    require(data["protocol_required_fields"] == REQUIRED_FIELDS, "bad required fields")
    require(len(data["protocol_field_candidate_map"]) == len(REQUIRED_FIELDS), "bad field-map length")
    require(data["mapped_field_count"] + data["unmapped_field_count"] == len(REQUIRED_FIELDS), "bad mapped/unmapped count")
    require(data["numeric_arrays_read"] is True, "numeric arrays must have been read or attempted upstream")
    require(data["numerical_data_vector_extracted"] is False, "numerical vector must not be extracted")
    require(data["covariance_matrix_extracted"] is False, "covariance matrix must not be extracted")
    require(data["protocol_fields_validated"] is False, "protocol fields must not be validated")
    require(data["schema_validated_against_protocol"] is False, "schema must not be protocol-validated")
    require(data["external_payload_verified"] is False, "external payload must not be verified")
    require(data["protocol_run"] is False, "protocol must not be run")
    require(data["evidence_supplied"] is False, "evidence must not be supplied")
    require(data["slot_promoted"] is False, "slot must not be promoted")
    require(data["does_not_prove"] == BOUNDARIES, "bad boundary list")

    for dep in data["depends_on"]:
        require((ROOT / dep).exists(), f"missing dependency: {dep}")

    for row in data["protocol_field_candidate_map"]:
        require(row["protocol_field"] in REQUIRED_FIELDS, f"bad protocol field: {row['protocol_field']}")
        require(row["promotion_status"] == "CANDIDATE_ONLY_NOT_VALIDATED_NOT_EVIDENCE", "bad promotion status")
        require(row["validation_status"] == "NOT_SCHEMA_VALIDATED_AGAINST_PROTOCOL", "bad validation status")

    for token in [
        "PROTOCOL_GATED_EXTRACTION_MAP_ONLY_NOT_VALIDATION",
        "Protocol-gated candidate mapping is performed.",
        "Mapped objects are candidates only.",
        "Protocol fields are not validated.",
        "Numerical data vector is not extracted.",
        "Covariance matrix is not extracted.",
        "Schema is not validated against protocol.",
        "External payload is not verified.",
        "Full protocol execution is not performed.",
        "No evidence is supplied.",
        "No slot is promoted.",
        *BOUNDARIES,
    ]:
        require(token in doc, f"doc missing token: {token}")

    print("DFM-MKC protocol-gated extraction map verification OK.")
    print("Status: PROTOCOL_GATED_EXTRACTION_MAP_ONLY_NOT_VALIDATION")

if __name__ == "__main__":
    main()
