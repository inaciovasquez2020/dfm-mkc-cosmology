import hashlib
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
ARTIFACT = ROOT / "artifacts/repo_intake/dfm_mkc_act_lite_numeric_like_extraction_2026_05_21.json"
DOC = ROOT / "docs/status/DFM_MKC_ACT_LITE_NUMERIC_LIKE_EXTRACTION_2026_05_21.md"

ALLOWED_STATUSES = {
    "ACT_LITE_NUMERIC_LIKE_EXTRACTION_ONLY_NOT_EVIDENCE",
    "ACT_LITE_NO_NUMERIC_LIKE_FILES_EXTRACTED",
}

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

    require(data["status"] in ALLOWED_STATUSES, "bad status")
    require(data["input_payload"] == "artifacts/public_payloads/act_dr6_act_lite_main_2026_05_21.zip", "bad input payload")
    require(data["numerical_data_vector_extracted"] is False, "numerical vector must not be extracted")
    require(data["covariance_matrix_extracted"] is False, "covariance matrix must not be extracted")
    require(data["schema_validated"] is False, "schema must not be validated")
    require(data["external_payload_verified"] is False, "external payload must not be verified")
    require(data["protocol_run"] is False, "protocol must not be run")
    require(data["evidence_supplied"] is False, "evidence must not be supplied")
    require(data["slot_promoted"] is False, "slot must not be promoted")
    require(data["does_not_prove"] == BOUNDARIES, "bad boundary list")

    require(data["numeric_like_files_extracted"] == len(data["extracted_files"]), "bad extracted file count")

    for record in data["extracted_files"]:
        path = ROOT / record["local_path"]
        require(path.exists(), f"missing extracted payload: {path}")
        require(sha256(path) == record["sha256"], f"bad sha256: {path}")
        require(record["classification"] == "NUMERIC_LIKE_FILE_EXTRACTED_NOT_SCHEMA_VALIDATED", "bad record classification")
        require(record["numerical_data_vector_extracted"] is False, "record must not extract vector")
        require(record["covariance_matrix_extracted"] is False, "record must not extract covariance")
        require(record["schema_validated"] is False, "record must not validate schema")
        require(record["external_payload_verified"] is False, "record must not verify payload")
        require(record["evidence_supplied"] is False, "record must not supply evidence")
        require(record["slot_promoted"] is False, "record must not promote slot")

    for token in [
        "Numerical data vector is not extracted.",
        "Covariance matrix is not extracted.",
        "Schema is not validated.",
        "External payload is not verified.",
        "No protocol run is performed.",
        "No evidence is supplied.",
        "No slot is promoted.",
        *BOUNDARIES,
    ]:
        require(token in doc, f"doc missing token: {token}")

    print("DFM-MKC ACT-lite numeric-like extraction verification OK.")
    print(f"Status: {data['status']}")

if __name__ == "__main__":
    main()
