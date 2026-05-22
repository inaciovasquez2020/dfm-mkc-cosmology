#!/usr/bin/env python3
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
ARTIFACT = ROOT / "artifacts/cosmology/independent_source_hash_and_schema_validation_for_each_multiprobe_input_2026_05_22.json"

REQUIRED_KEYS = {
    "act_dr6_cmb_lite",
    "pantheon_plus_shoes",
    "desi_dr2",
    "planck_baseline",
    "des_y6",
    "growth_sector_holdout",
    "h0_distance_ladder",
}

def main():
    data = json.loads(ARTIFACT.read_text())
    assert data["object"] == "INDEPENDENT_SOURCE_HASH_AND_SCHEMA_VALIDATION_FOR_EACH_MULTIPROBE_INPUT"
    assert data["status"] == "VALIDATION_GATE_ONLY_NO_INDEPENDENT_HASH_OR_SCHEMA_CERTIFICATION"
    assert data["source_object"] == "CERTIFIED_FILE_LEVEL_MULTIPROBE_LIKELIHOOD_INPUTS"
    assert set(data["validations"]) == REQUIRED_KEYS
    assert data["summary"]["inputs_with_independent_source_digest"] == 0
    assert data["summary"]["inputs_with_hash_match_verified"] == 0
    assert data["summary"]["inputs_with_schema_validation_passed"] == 0
    assert data["summary"]["inputs_certified_for_profiled_likelihood_execution"] == 0
    assert data["summary"]["ready_for_executed_multiprobe_profiled_likelihood_run"] is False
    for key, entry in data["validations"].items():
        assert entry["independent_source_url_or_release_id"] is None, key
        assert entry["independent_source_digest"] is None, key
        assert entry["independent_hash_match_verified"] is False, key
        assert entry["schema_validator_or_reader"] is None, key
        assert entry["schema_validation_passed"] is False, key
        assert entry["likelihood_role_verified"] is False, key
        assert entry["certified_for_profiled_likelihood_execution"] is False, key
    assert "Lambda-CDM rejection" in data["does_not_prove"]
    assert "DFM-MKC validation" in data["does_not_prove"]
    assert "any Clay problem" in data["does_not_prove"]
    print("Independent source hash and schema validation gate verification OK.")
    print("Status:", data["status"])
    print("Required next object:", data["required_next_object"])

if __name__ == "__main__":
    main()
