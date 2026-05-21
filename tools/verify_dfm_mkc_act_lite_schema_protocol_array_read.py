import hashlib
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
ARTIFACT = ROOT / "artifacts/repo_intake/dfm_mkc_act_lite_schema_protocol_array_read_2026_05_21.json"
DOC = ROOT / "docs/status/DFM_MKC_ACT_LITE_SCHEMA_PROTOCOL_ARRAY_READ_2026_05_21.md"

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

def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()

def main():
    data = json.loads(ARTIFACT.read_text())
    doc = DOC.read_text()
    payload = ROOT / data["input_payload"]

    require(data["status"] == "SCHEMA_PROTOCOL_COMPARISON_WITH_ARRAY_READING_NOT_EVIDENCE", "bad status")
    require(payload.exists(), "missing FITS payload")
    require(payload.stat().st_size == data["file_size_bytes"], "bad file size")
    require(sha256(payload) == data["sha256"], "bad sha256")
    require(data["numeric_arrays_read"] is True, "numeric arrays must be read or attempted")
    require(data["numeric_array_read_attempt_columns"] >= 1, "at least one numeric column must be attempted")
    require(data["empty_array_reads_allowed"] is True, "empty array reads must be explicitly allowed")
    require(data["schema_to_protocol_comparison"]["comparison_performed"] is True, "comparison must be performed")
    require(data["schema_to_protocol_comparison"]["full_protocol_execution"] is False, "full protocol must not execute")
    require(data["schema_to_protocol_comparison"]["result"] == "STRUCTURAL_COMPARISON_ONLY_NO_PROTOCOL_RUN", "bad comparison result")
    require(data["numerical_data_vector_extracted"] is False, "numerical vector must not be extracted")
    require(data["covariance_matrix_extracted"] is False, "covariance matrix must not be extracted")
    require(data["schema_validated_against_protocol"] is False, "schema must not be protocol-validated")
    require(data["external_payload_verified"] is False, "external payload must not be verified")
    require(data["protocol_run"] is False, "protocol must not be run")
    require(data["evidence_supplied"] is False, "evidence must not be supplied")
    require(data["slot_promoted"] is False, "slot must not be promoted")
    require(data["does_not_prove"] == BOUNDARIES, "bad boundary list")

    array_read_columns = [
        column
        for hdu in data["array_reads"]
        for column in hdu.get("columns", [])
        if column.get("array_read") is True
    ]
    require(len(array_read_columns) == data["numeric_array_read_attempt_columns"], "bad numeric array attempt count")
    require(data["numeric_columns_read"] <= data["numeric_array_read_attempt_columns"], "positive read count cannot exceed attempts")
    for column in array_read_columns:
        require(column.get("values_read", 0) >= 0, "array-read column must record nonnegative values_read")
        require("summary" in column, "array-read column must include summary")
        require(column.get("classification") in {
            "NUMERIC_ARRAY_READ_SUMMARY_ONLY_NOT_EVIDENCE",
            "NUMERIC_ARRAY_READ_ATTEMPT_EMPTY_COLUMN_NOT_EVIDENCE",
        }, "array-read column must carry non-evidence classification")

    for token in [
        "SCHEMA_PROTOCOL_COMPARISON_WITH_ARRAY_READING_NOT_EVIDENCE",
        "Numeric arrays are read or attempted structurally.",
        "Empty array reads are allowed only as non-evidence structural observations.",
        "Schema-to-protocol comparison is structural only.",
        "Full protocol execution is not performed.",
        "Numerical data vector is not extracted.",
        "Covariance matrix is not extracted.",
        "Schema is not validated against protocol.",
        "External payload is not verified.",
        "No evidence is supplied.",
        "No slot is promoted.",
        *BOUNDARIES,
    ]:
        require(token in doc, f"doc missing token: {token}")

    print("DFM-MKC ACT-lite schema-to-protocol array-read verification OK.")
    print("Status: SCHEMA_PROTOCOL_COMPARISON_WITH_ARRAY_READING_NOT_EVIDENCE")

if __name__ == "__main__":
    main()
