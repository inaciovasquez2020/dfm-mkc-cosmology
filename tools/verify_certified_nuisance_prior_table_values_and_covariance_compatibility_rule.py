#!/usr/bin/env python3
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
ARTIFACT = ROOT / "artifacts/cosmology/certified_nuisance_prior_table_values_and_covariance_compatibility_rule_2026_05_22.json"

PROBES = {
    "ACT_DR6",
    "PANTHEON_PLUS_SHOES",
    "DESI_DR2",
    "PLANCK_2018",
    "DES_Y6",
    "GROWTH_SECTOR",
    "H0_DISTANCE_LADDER",
}

VALID_STATUSES = {
    "CERTIFIED_NUISANCE_AND_COVARIANCE_COMPATIBILITY_RULE_CLOSED",
    "RULE_SURFACE_MATERIALIZED_VALUES_AND_COMPATIBILITY_NOT_CERTIFIED",
}

def main():
    data = json.loads(ARTIFACT.read_text())
    assert data["object"] == "CERTIFIED_NUISANCE_PRIOR_TABLE_VALUES_AND_COVARIANCE_COMPATIBILITY_RULE"
    assert data["status"] in VALID_STATUSES
    assert data["source_object"] == "NUISANCE_PRIOR_TABLE_CERTIFICATION_AND_COVARIANCE_CHAIN_COMPATIBILITY"
    assert set(data["nuisance_prior_slots"]) == PROBES
    assert len(data["covariance_compatibility_slots"]) == 21
    assert data["nuisance_prior_values_certified"] is False
    assert data["covariance_compatibility_rule_certified"] is False
    assert data["combined_certification_closed"] is False
    for probe, slot in data["nuisance_prior_slots"].items():
        assert slot["values_supplied"] is False, probe
        assert slot["certified"] is False, probe
        assert "parameter_name" in slot["required_fields"], probe
        assert "source_reference" in slot["required_fields"], probe
    for pair, slot in data["covariance_compatibility_slots"].items():
        assert slot["rule_supplied"] is False, pair
        assert slot["compatibility_certified"] is False, pair
        assert "cross_covariance_policy" in slot["required_fields"], pair
    assert data["required_next_object"] == "PER_PROBE_NUISANCE_PRIOR_VALUES_AND_CROSS_COVARIANCE_POLICY_TABLE"
    assert "complete certified multiprobe likelihood manifest" in data["does_not_prove"]
    assert "executed multiprobe likelihood run" in data["does_not_prove"]
    assert "Lambda-CDM rejection" in data["does_not_prove"]
    assert "DFM-MKC validation" in data["does_not_prove"]
    assert "any Clay problem" in data["does_not_prove"]
    print("Certified nuisance prior values and covariance compatibility rule verification OK.")
    print("Status:", data["status"])
    print("Required next object:", data["required_next_object"])

if __name__ == "__main__":
    main()
