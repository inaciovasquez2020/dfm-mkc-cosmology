import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
ARTIFACT = ROOT / "artifacts/repo_intake/dfm_mkc_payload_extraction_classifier_2026_05_21.json"
DOC = ROOT / "docs/status/DFM_MKC_PAYLOAD_EXTRACTION_CLASSIFIER_2026_05_21.md"

DOMAIN = [
    "SOURCE_PAYLOAD",
    "NUMERICAL_DATA_VECTOR",
    "COVARIANCE_MATRIX",
    "INDEX_ONLY",
    "UNUSABLE",
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

    require(data["status"] == "PAYLOAD_CLASSIFIER_ONLY_NO_NUMERICAL_EXTRACTION", "bad status")
    require(data["classification_domain"] == DOMAIN, "bad classification domain")
    require(len(data["classifications"]) >= 1, "expected at least one classification")
    require(data["numerical_data_vector_extracted"] is False, "numerical vector must not be extracted")
    require(data["covariance_matrix_extracted"] is False, "covariance matrix must not be extracted")
    require(data["schema_validated"] is False, "schema must not be validated")
    require(data["external_payload_verified"] is False, "external payload must not be verified")
    require(data["protocol_run"] is False, "protocol must not be run")
    require(data["evidence_supplied"] is False, "evidence must not be supplied")
    require(data["slot_promoted"] is False, "slot must not be promoted")
    require(data["does_not_prove"] == BOUNDARIES, "bad boundary list")

    allowed = set(DOMAIN)
    for record in data["classifications"]:
        require(record["classification"] in allowed, f"bad classification: {record['classification']}")
        require(record["classification"] not in {"NUMERICAL_DATA_VECTOR", "COVARIANCE_MATRIX"}, "must not promote extracted numeric data")
        require(record["numerical_data_vector_extracted"] is False, "record must not extract vector")
        require(record["covariance_matrix_extracted"] is False, "record must not extract covariance")
        require(record["schema_validated"] is False, "record must not validate schema")
        require(record["external_payload_verified"] is False, "record must not verify external payload")
        require(record["slot_promoted"] is False, "record must not promote slot")

    for token in [
        "PAYLOAD_CLASSIFIER_ONLY_NO_NUMERICAL_EXTRACTION",
        *DOMAIN,
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

    print("DFM-MKC payload extraction classifier verification OK.")
    print("Status: PAYLOAD_CLASSIFIER_ONLY_NO_NUMERICAL_EXTRACTION")

if __name__ == "__main__":
    main()
