import hashlib
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
ARTIFACT = ROOT / "artifacts/repo_intake/dfm_mkc_downloaded_public_payload_manifest_2026_05_21.json"
DOC = ROOT / "docs/status/DFM_MKC_DOWNLOADED_PUBLIC_PAYLOAD_MANIFEST_2026_05_21.md"

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

def sha256(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()

def main():
    data = json.loads(ARTIFACT.read_text())
    doc = DOC.read_text()

    require(data["status"] == "DOWNLOADED_PUBLIC_SOURCE_PAYLOAD_MANIFEST_ONLY_NOT_EVIDENCE", "bad status")
    require(len(data["payloads"]) >= 1, "expected at least one downloaded payload")
    require(data["payload_manifest_created"] is True, "manifest must be created")
    require(data["numerical_data_vector_extracted"] is False, "numerical vector must not be extracted")
    require(data["covariance_matrix_extracted"] is False, "covariance matrix must not be extracted")
    require(data["schema_validated"] is False, "schema must not be validated")
    require(data["external_payload_verified"] is False, "external payload must not be verified")
    require(data["protocol_run"] is False, "protocol must not be run")
    require(data["evidence_supplied"] is False, "evidence must not be supplied")
    require(data["slot_promoted"] is False, "slot must not be promoted")
    require(data["does_not_prove"] == BOUNDARIES, "bad boundary list")

    for payload in data["payloads"]:
        path = ROOT / payload["local_path"]
        require(path.exists(), f"missing payload: {path}")
        require(path.stat().st_size == payload["file_size_bytes"], f"bad file size: {path}")
        require(sha256(path) == payload["sha256"], f"bad sha256: {path}")
        require(payload["checksum_verified"] is True, "checksum must be verified")
        require(payload["schema_validated"] is False, "schema must not be validated")
        require(payload["external_payload_verified"] is False, "external payload must not be verified")

    for token in [
        "DOWNLOADED_PUBLIC_SOURCE_PAYLOAD_MANIFEST_ONLY_NOT_EVIDENCE",
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

    print("DFM-MKC downloaded public payload manifest verification OK.")
    print("Status: DOWNLOADED_PUBLIC_SOURCE_PAYLOAD_MANIFEST_ONLY_NOT_EVIDENCE")

if __name__ == "__main__":
    main()
