#!/usr/bin/env python3
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
ARTIFACT = ROOT / "artifacts/cosmology/act_dr6_public_release_digest_and_full_sacc_schema_reader_2026_05_22.json"

def main():
    data = json.loads(ARTIFACT.read_text())
    assert data["object"] == "ACT_DR6_PUBLIC_RELEASE_DIGEST_AND_FULL_SACC_SCHEMA_READER"
    assert data["status"] == "LOCAL_FITS_HEADER_ENUMERATOR_ONLY_PUBLIC_DIGEST_AND_FULL_SACC_SCHEMA_OPEN"
    assert data["source_object"] == "ACT_DR6_SACC_READER_AND_INDEPENDENT_RELEASE_HASH_VALIDATION"
    assert data["input_key"] == "act_dr6_cmb_lite"
    assert data["local_payload"]["exists"] is True
    assert data["local_payload"]["sha256"]
    assert data["local_payload"]["fits_hdu_headers_observed"] >= 1
    assert data["reader"]["name"] == "LOCAL_FITS_HEADER_ENUMERATOR"
    assert data["reader"]["executes_on_local_payload"] is True
    assert data["reader"]["full_sacc_schema_reader_implemented"] is False
    assert data["reader"]["full_sacc_schema_validation_passed"] is False
    assert data["public_release_digest"]["external_release_url_or_doi"] is None
    assert data["public_release_digest"]["external_release_digest"] is None
    assert data["public_release_digest"]["independent_hash_match_verified"] is False
    assert data["public_release_digest"]["release_provenance_certified"] is False
    assert data["certified_for_profiled_likelihood_execution"] is False
    assert "ACT DR6 public release digest certification" in data["does_not_prove"]
    assert "ACT DR6 full SACC schema certification" in data["does_not_prove"]
    assert "Lambda-CDM rejection" in data["does_not_prove"]
    assert "DFM-MKC validation" in data["does_not_prove"]
    assert "any Clay problem" in data["does_not_prove"]
    print("ACT DR6 public release digest and full SACC schema reader gate verification OK.")
    print("Status:", data["status"])
    print("Required next object:", data["required_next_object"])

if __name__ == "__main__":
    main()
