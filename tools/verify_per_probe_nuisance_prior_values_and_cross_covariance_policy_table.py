#!/usr/bin/env python3
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
ARTIFACT = ROOT / "artifacts/cosmology/per_probe_nuisance_prior_values_and_cross_covariance_policy_table_2026_05_22.json"

PROBES = {
    "ACT_DR6",
    "PANTHEON_PLUS_SHOES",
    "DESI_DR2",
    "PLANCK_2018",
    "DES_Y6",
    "GROWTH_SECTOR",
    "H0_DISTANCE_LADDER",
}

def main():
    data = json.loads(ARTIFACT.read_text())
    assert data["object"] == "PER_PROBE_NUISANCE_PRIOR_VALUES_AND_CROSS_COVARIANCE_POLICY_TABLE"
    assert data["source_object"] == "CERTIFIED_NUISANCE_PRIOR_TABLE_VALUES_AND_COVARIANCE_COMPATIBILITY_RULE"
    assert data["status"] == "TABLE_SURFACE_MATERIALIZED_VALUES_AND_POLICY_NOT_SUPPLIED"
    assert {row["probe"] for row in data["nuisance_prior_rows"]} == PROBES
    assert len(data["nuisance_prior_rows"]) == 7
    assert len(data["cross_covariance_policy_rows"]) == 21
    assert data["nuisance_prior_values_certified"] is False
    assert data["cross_covariance_policy_certified"] is False
    assert data["table_certified"] is False
    for row in data["nuisance_prior_rows"]:
        assert row["value_supplied"] is False
        assert row["certified"] is False
        assert row["source_reference"] is None
    for row in data["cross_covariance_policy_rows"]:
        assert row["rule_supplied"] is False
        assert row["compatibility_certified"] is False
        assert row["cross_covariance_policy"] is None
    assert data["required_next_object"] == "SUPPLIED_PER_PROBE_NUISANCE_PRIOR_VALUES_AND_CROSS_COVARIANCE_POLICY_TABLE"
    assert "complete certified multiprobe likelihood manifest" in data["does_not_prove"]
    assert "executed multiprobe likelihood run" in data["does_not_prove"]
    assert "Lambda-CDM rejection" in data["does_not_prove"]
    assert "DFM-MKC validation" in data["does_not_prove"]
    assert "any Clay problem" in data["does_not_prove"]
    print("Per-probe nuisance prior values and cross-covariance policy table verification OK.")
    print("Status:", data["status"])
    print("Required next object:", data["required_next_object"])

if __name__ == "__main__":
    main()
