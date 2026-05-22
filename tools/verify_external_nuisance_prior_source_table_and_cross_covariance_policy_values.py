#!/usr/bin/env python3
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
ARTIFACT = ROOT / "artifacts/cosmology/external_nuisance_prior_source_table_and_cross_covariance_policy_values_2026_05_22.json"

def main():
    data = json.loads(ARTIFACT.read_text())
    assert data["object"] == "EXTERNAL_NUISANCE_PRIOR_SOURCE_TABLE_AND_CROSS_COVARIANCE_POLICY_VALUES"
    assert data["source_object"] == "SUPPLIED_PER_PROBE_NUISANCE_PRIOR_VALUES_AND_CROSS_COVARIANCE_POLICY_TABLE"
    assert data["status"] == "EXTERNAL_SOURCE_VALUE_TABLE_TARGET_MATERIALIZED_VALUES_NOT_SUPPLIED"
    assert len(data["external_nuisance_source_rows"]) == 7
    assert len(data["external_cross_covariance_policy_rows"]) == 21
    assert data["nuisance_sources_bound"] is False
    assert data["covariance_sources_bound"] is False
    assert data["nuisance_values_supplied"] is False
    assert data["covariance_policies_supplied"] is False
    assert data["combined_certification_closed"] is False
    for row in data["external_nuisance_source_rows"]:
        assert row["external_source_reference"] is None
        assert row["external_source_digest"] is None
        assert row["source_bound"] is False
        assert row["value_record_supplied"] is False
        assert row["schema_validated"] is False
        assert row["certified"] is False
    for row in data["external_cross_covariance_policy_rows"]:
        assert row["external_source_reference"] is None
        assert row["external_source_digest"] is None
        assert row["source_bound"] is False
        assert row["policy_record_supplied"] is False
        assert row["schema_validated"] is False
        assert row["compatibility_certified"] is False
    assert data["required_next_object"] == "BOUND_EXTERNAL_NUISANCE_PRIOR_SOURCES_AND_COVARIANCE_POLICY_RECORDS"
    assert "complete certified multiprobe likelihood manifest" in data["does_not_prove"]
    assert "executed multiprobe likelihood run" in data["does_not_prove"]
    assert "Lambda-CDM rejection" in data["does_not_prove"]
    assert "DFM-MKC validation" in data["does_not_prove"]
    assert "any Clay problem" in data["does_not_prove"]
    print("External nuisance prior source table and cross-covariance policy values verification OK.")
    print("Status:", data["status"])
    print("Required next object:", data["required_next_object"])

if __name__ == "__main__":
    main()
