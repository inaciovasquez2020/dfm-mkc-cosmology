import hashlib
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
ARTIFACT = ROOT / "artifacts/repo_intake/dfm_mkc_act_lite_fits_schema_inspection_2026_05_21.json"
DOC = ROOT / "docs/status/DFM_MKC_ACT_LITE_FITS_SCHEMA_INSPECTION_2026_05_21.md"

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

    require(data["status"] == "FITS_SCHEMA_INSPECTION_ONLY_NO_NUMERICAL_EXTRACTION", "bad status")
    require(payload.exists(), "missing FITS payload")
    require(payload.stat().st_size == data["file_size_bytes"], "bad file size")
    require(sha256(payload) == data["sha256"], "bad sha256")
    require(data["hdu_count"] == len(data["hdus"]), "bad HDU count")
    require(data["hdu_count"] >= 1, "must inspect at least one HDU")
    require(data["fits_header_parsed"] is True, "FITS header must be parsed")
    require(data["schema_inspected"] is True, "schema must be inspected")
    require(data["numerical_data_vector_extracted"] is False, "numerical vector must not be extracted")
    require(data["covariance_matrix_extracted"] is False, "covariance matrix must not be extracted")
    require(data["numeric_arrays_read"] is False, "numeric arrays must not be read")
    require(data["schema_validated_against_protocol"] is False, "schema must not be protocol-validated")
    require(data["external_payload_verified"] is False, "external payload must not be verified")
    require(data["protocol_run"] is False, "protocol must not be run")
    require(data["evidence_supplied"] is False, "evidence must not be supplied")
    require(data["slot_promoted"] is False, "slot must not be promoted")
    require(data["does_not_prove"] == BOUNDARIES, "bad boundary list")

    for hdu in data["hdus"]:
        require(hdu["schema_classification"] == "FITS_HDU_SCHEMA_ONLY_NO_NUMERIC_ARRAY_EXTRACTION", "bad HDU schema classification")
        require("hdu_index" in hdu, "missing hdu index")
        require("xtension" in hdu, "missing xtension")
        require("columns" in hdu, "missing columns")

    for token in [
        "FITS_SCHEMA_INSPECTION_ONLY_NO_NUMERICAL_EXTRACTION",
        "FITS header is parsed.",
        "HDU schema is inspected.",
        "Numerical data vector is not extracted.",
        "Covariance matrix is not extracted.",
        "Numeric arrays are not read.",
        "Schema is not validated against protocol.",
        "External payload is not verified.",
        "No protocol run is performed.",
        "No evidence is supplied.",
        "No slot is promoted.",
        *BOUNDARIES,
    ]:
        require(token in doc, f"doc missing token: {token}")

    print("DFM-MKC ACT-lite FITS schema inspection verification OK.")
    print("Status: FITS_SCHEMA_INSPECTION_ONLY_NO_NUMERICAL_EXTRACTION")

if __name__ == "__main__":
    main()
