import json
import zipfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
ARTIFACT = ROOT / "artifacts/repo_intake/dfm_mkc_act_lite_payload_inventory_2026_05_21.json"
DOC = ROOT / "docs/status/DFM_MKC_ACT_LITE_PAYLOAD_INVENTORY_2026_05_21.md"
ZIP_PATH = ROOT / "artifacts/public_payloads/act_dr6_act_lite_main_2026_05_21.zip"

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

    require(data["status"] == "ACT_LITE_PAYLOAD_INVENTORY_ONLY_NO_NUMERICAL_EXTRACTION", "bad status")
    require(data["input_payload"] == "artifacts/public_payloads/act_dr6_act_lite_main_2026_05_21.zip", "bad input payload")
    require(ZIP_PATH.exists(), "missing ACT-lite zip payload")
    require(zipfile.is_zipfile(ZIP_PATH), "ACT-lite payload must be a zip archive")
    require(data["archive_read_success"] is True, "archive read must succeed")
    require(data["archive_extracted"] is False, "archive must not be extracted")
    require(data["numerical_data_vector_extracted"] is False, "numerical vector must not be extracted")
    require(data["covariance_matrix_extracted"] is False, "covariance matrix must not be extracted")
    require(data["schema_validated"] is False, "schema must not be validated")
    require(data["external_payload_verified"] is False, "external payload must not be verified")
    require(data["protocol_run"] is False, "protocol must not be run")
    require(data["evidence_supplied"] is False, "evidence must not be supplied")
    require(data["slot_promoted"] is False, "slot must not be promoted")
    require(data["does_not_prove"] == BOUNDARIES, "bad boundary list")

    with zipfile.ZipFile(ZIP_PATH) as zf:
        actual_entries = len(zf.infolist())

    require(data["inventory_counts"]["total_entries"] == actual_entries, "bad entry count")
    require(len(data["entries"]) == actual_entries, "entry list length mismatch")
    require(actual_entries > 0, "archive must contain entries")

    for record in data["entries"]:
        require(record["classification"] in {
            "DIRECTORY",
            "SOURCE_OR_CONFIG",
            "NUMERIC_LIKE_FILE_PRESENT_NOT_EXTRACTED",
            "OTHER",
        }, f"bad entry classification: {record['classification']}")

    for token in [
        "ACT_LITE_PAYLOAD_INVENTORY_ONLY_NO_NUMERICAL_EXTRACTION",
        "Archive is not extracted.",
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

    print("DFM-MKC ACT-lite payload inventory verification OK.")
    print("Status: ACT_LITE_PAYLOAD_INVENTORY_ONLY_NO_NUMERICAL_EXTRACTION")

if __name__ == "__main__":
    main()
