#!/usr/bin/env python3
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
ARTIFACT = ROOT / "artifacts/cosmology/supplied_per_probe_nuisance_prior_values_and_cross_covariance_policy_table_2026_05_22.json"

def main():
    data = json.loads(ARTIFACT.read_text())
    assert data["object"] == "SUPPLIED_PER_PROBE_NUISANCE_PRIOR_VALUES_AND_CROSS_COVARIANCE_POLICY_TABLE"
    assert data["source_object"] == "PER_PROBE_NUISANCE_PRIOR_VALUES_AND_CROSS_COVARIANCE_POLICY_TABLE"
    assert data["status"] == "SUPPLIED_TABLE_TARGET_MATERIALIZED_VALUES_AND_POLICIES_NOT_SUPPLIED"
    assert len(data["nuisance_prior_rows"]) == 7
    assert len(data["cross_covariance_policy_rows"]) == 21
    assert data["nuisance_prior_values_supplied"] is False
    assert data["cross_covariance_policies_supplied"] is False
    assert data["nuisance_prior_values_certified"] is False
    assert data["cross_covariance_policy_certified"] is False
    assert data["table_certified"] is False
    for row in data["nuisance_prior_rows"]:
        assert row["supplied_value_record"] is None
        assert row["external_source_bound"] is False
        assert row["schema_validated"] is False
        assert row["value_supplied"] is False
        assert row["certified"] is False
    for row in data["cross_covariance_policy_rows"]:
        assert row["supplied_policy_record"] is None
        assert row["external_source_bound"] is False
        assert row["schema_validated"] is False
        assert row["rule_supplied"] is False
        assert row["compatibility_certified"] is False
    assert data["required_next_object"] == "EXTERNAL_NUISANCE_PRIOR_SOURCE_TABLE_AND_CROSS_COVARIANCE_POLICY_VALUES"
    assert "complete certified multiprobe likelihood manifest" in data["does_not_prove"]
    assert "executed multiprobe likelihood run" in data["does_not_prove"]
    assert "Lambda-CDM rejection" in data["does_not_prove"]
    assert "DFM-MKC validation" in data["does_not_prove"]
    assert "any Clay problem" in data["does_not_prove"]
    print("Supplied per-probe nuisance prior values and cross-covariance policy table verification OK.")
    print("Status:", data["status"])
    print("Required next object:", data["required_next_object"])

if __name__ == "__main__":
    main()
