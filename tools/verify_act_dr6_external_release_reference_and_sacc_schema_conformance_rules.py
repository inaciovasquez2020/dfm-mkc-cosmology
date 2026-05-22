#!/usr/bin/env python3
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
ARTIFACT = ROOT / "artifacts/cosmology/act_dr6_external_release_reference_and_sacc_schema_conformance_rules_2026_05_22.json"

REQUIRED_RULES = {
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
    assert data["object"] == "ACT_DR6_EXTERNAL_RELEASE_REFERENCE_AND_SACC_SCHEMA_CONFORMANCE_RULES"
    assert data["status"] == "CONFORMANCE_RULES_DEFINED_EXTERNAL_REFERENCE_MISSING"
    assert data["source_object"] == "ACT_DR6_PUBLIC_RELEASE_DIGEST_AND_FULL_SACC_SCHEMA_READER"
    assert data["input_key"] == "act_dr6_cmb_lite"
    assert set(data["sacc_schema_conformance_rules"]) == REQUIRED_RULES
    assert data["external_release_reference"]["release_url_or_doi"] is None
    assert data["external_release_reference"]["external_digest"] is None
    assert data["external_release_reference"]["external_reference_supplied"] is False
    assert data["external_release_reference"]["external_digest_supplied"] is False
    assert data["external_release_reference"]["external_digest_matches_local_payload"] is False
    assert data["summary"]["rules_defined"] == len(REQUIRED_RULES)
    assert data["summary"]["rules_validated"] == 0
    assert data["summary"]["full_sacc_schema_conformance_established"] is False
    assert data["summary"]["certified_for_profiled_likelihood_execution"] is False
    for rule, entry in data["sacc_schema_conformance_rules"].items():
        assert entry["required"] is True, rule
        assert entry["validated"] is False, rule
        assert entry["validation_status"] == "RULE_DEFINED_NOT_VALIDATED", rule
    assert "ACT DR6 public release digest certification" in data["does_not_prove"]
    assert "ACT DR6 full SACC schema certification" in data["does_not_prove"]
    assert "Lambda-CDM rejection" in data["does_not_prove"]
    assert "DFM-MKC validation" in data["does_not_prove"]
    assert "any Clay problem" in data["does_not_prove"]
    print("ACT DR6 external release reference and SACC schema conformance rules verification OK.")
    print("Status:", data["status"])
    print("Required next object:", data["required_next_object"])

if __name__ == "__main__":
    main()
