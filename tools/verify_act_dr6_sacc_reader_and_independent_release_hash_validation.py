#!/usr/bin/env python3
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
ARTIFACT = ROOT / "artifacts/cosmology/act_dr6_sacc_reader_and_independent_release_hash_validation_2026_05_22.json"

def main():
    data = json.loads(ARTIFACT.read_text())
    assert data["object"] == "ACT_DR6_SACC_READER_AND_INDEPENDENT_RELEASE_HASH_VALIDATION"
    assert data["status"] == "LOCAL_FITS_HEADER_READER_ONLY_NO_INDEPENDENT_RELEASE_HASH"
    assert data["source_object"] == "PROBE_SPECIFIC_INDEPENDENT_SOURCE_HASHES_AND_SCHEMA_READERS"
    assert data["input_key"] == "act_dr6_cmb_lite"
    assert data["reader"]["name"] == "LOCAL_FITS_HEADER_PROBE"
    assert data["reader"]["target_reader"] == "SACC_FITS_READER"
    assert data["reader"]["executes_on_local_payload"] is True
    assert data["reader"]["fits_header_observed"] is True
    assert data["reader"]["full_sacc_schema_validation_passed"] is False
    assert data["local_payload"]["exists"] is True
    assert data["local_payload"]["local_sha256"]
    assert data["independent_release_validation"]["external_release_url_or_doi"] is None
    assert data["independent_release_validation"]["external_release_digest"] is None
    assert data["independent_release_validation"]["independent_hash_match_verified"] is False
    assert data["independent_release_validation"]["release_provenance_certified"] is False
    assert data["certified_for_profiled_likelihood_execution"] is False
    assert "ACT DR6 independent source certification" in data["does_not_prove"]
    assert "ACT DR6 full SACC schema certification" in data["does_not_prove"]
    assert "Lambda-CDM rejection" in data["does_not_prove"]
    assert "DFM-MKC validation" in data["does_not_prove"]
    assert "any Clay problem" in data["does_not_prove"]
    print("ACT DR6 SACC reader and independent release hash validation gate verification OK.")
    print("Status:", data["status"])
    print("Required next object:", data["required_next_object"])

if __name__ == "__main__":
    main()
