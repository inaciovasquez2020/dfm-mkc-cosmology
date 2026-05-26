#!/usr/bin/env python3
import hashlib
import json
from pathlib import Path

ART = Path("artifacts/dfm_mkc/act_dr6_authentic_payload_binding_attempt_2026_05_25.json")
DOC = Path("docs/status/ACT_DR6_AUTHENTIC_PAYLOAD_BINDING_ATTEMPT_2026_05_25.md")
SCHEMA = Path("artifacts/dfm_mkc/act_dr6_cmbonly_fits_schema_summary_2026_05_25.json")

REQUIRED_BOUNDARIES = {
    "DFM-MKC empirical validation",
    "Lambda-CDM failure",
    "DFM-MKC prediction vector exists",
    "baseline LCDM prediction vector has been reduced to a repository artifact",
    "residual eigenspace empirical comparison has been run",
    "dark matter is liquid",
    "dark matter is solid",
    "dark matter phase transition is physically real",
    "dark matter resolution",
    "dark energy resolution",
    "ACT validation of DFM-MKC",
    "CMB validation of DFM-MKC",
    "independent empirical replication",
    "gravity closure",
    "Chronos proof input",
    "Chronos-RR",
    "H4.1/FGL",
    "P vs NP",
    "any Clay problem",
}

def sha256(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()

def main() -> None:
    assert ART.exists(), ART
    assert DOC.exists(), DOC
    assert SCHEMA.exists(), SCHEMA

    data = json.loads(ART.read_text())
    doc = DOC.read_text()
    schema = json.loads(SCHEMA.read_text())

    assert data["id"] == "ACT_DR6_AUTHENTIC_PAYLOAD_BINDING_ATTEMPT_2026_05_25"
    assert data["status"] in {
        "ACT_DR6_CMBONLY_LCDM_LIKELIHOOD_EXECUTED",
        "ACT_DR6_CMBONLY_DATA_BOUND_LIKELIHOOD_NOT_EXECUTED",
    }
    assert data["actual_data_file_bound"] is True
    assert data["actual_sha256_verified_payload"] is True
    assert data["physical_dark_matter_phase_claim_status"] == "HYPOTHESIS_ONLY"
    assert REQUIRED_BOUNDARIES <= set(data["does_not_prove"])

    payload = Path(data["bound_payload"]["data_payload_path"])
    sha_file = Path(data["bound_payload"]["payload_sha256_path"])
    assert payload.exists(), payload
    assert sha_file.exists(), sha_file

    recorded = sha_file.read_text().split()[0]
    assert sha256(payload) == recorded

    assert schema["status"] == "ACT_DR6_CMBONLY_FITS_SCHEMA_SUMMARY"
    assert schema["hdu_count"] >= 1

    for token in REQUIRED_BOUNDARIES | {
        "HYPOTHESIS_ONLY",
        "actual ACT DR6 CMB-only data file bound: true",
        "actual SHA-256 payload record: true",
    }:
        assert token in doc, token

    print("ACT_DR6_AUTHENTIC_PAYLOAD_BINDING_ATTEMPT_OK")

if __name__ == "__main__":
    main()
