#!/usr/bin/env python3
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
ARTIFACT = ROOT / "artifacts/cosmology/act_dr6_external_reference_sacc_conformance_validator_2026_05_22.json"

REQUIRED_CHECKS = {
    "fits_payload_opens",
    "required_hdus_present",
    "tracers_table_present",
    "data_vector_present",
    "covariance_matrix_present",
    "metadata_consistent",
    "likelihood_reader_maps_payload_to_numeric_arrays",
    "external_release_digest_matches_local_payload",
}

def main():
    data = json.loads(ARTIFACT.read_text())
    assert data["object"] == "ACT_DR6_EXTERNAL_RELEASE_DIGEST_SUPPLIED_AND_SACC_CONFORMANCE_VALIDATOR"
    assert data["status"] == "OFFICIAL_REFERENCE_BOUND_VALIDATOR_PARTIAL_DIGEST_NOT_SUPPLIED"
    assert data["source_object"] == "ACT_DR6_EXTERNAL_RELEASE_REFERENCE_AND_SACC_SCHEMA_CONFORMANCE_RULES"
    assert data["official_external_references"]["act_dr6_data_products"].startswith("https://act.princeton.edu/")
    assert data["official_external_references"]["act_dr6_lite_repository"].startswith("https://github.com/ACTCollaboration/")
    assert data["local_sha256"]
    assert data["external_digest"] is None
    assert data["external_digest_supplied"] is False
    assert data["external_digest_matches_local_payload"] is False
    checks = data["sacc_conformance_validator"]["checks"]
    assert set(checks) == REQUIRED_CHECKS
    assert checks["fits_payload_opens"] is True
    assert checks["required_hdus_present"] is True
    assert checks["external_release_digest_matches_local_payload"] is False
    assert data["sacc_conformance_validator"]["full_sacc_schema_conformance_established"] is False
    assert data["certified_for_profiled_likelihood_execution"] is False
    assert "ACT DR6 public release digest certification" in data["does_not_prove"]
    assert "ACT DR6 full SACC schema certification" in data["does_not_prove"]
    assert "Lambda-CDM rejection" in data["does_not_prove"]
    assert "DFM-MKC validation" in data["does_not_prove"]
    assert "any Clay problem" in data["does_not_prove"]
    print("ACT DR6 external reference SACC conformance validator verification OK.")
    print("Status:", data["status"])
    print("Required next object:", data["required_next_object"])

if __name__ == "__main__":
    main()
