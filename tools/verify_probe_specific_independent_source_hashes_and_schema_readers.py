#!/usr/bin/env python3
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
ARTIFACT = ROOT / "artifacts/cosmology/probe_specific_independent_source_hashes_and_schema_readers_2026_05_22.json"

REQUIRED_KEYS = {
    "act_dr6_cmb_lite",
    "pantheon_plus_shoes",
    "desi_dr2",
    "planck_baseline",
    "des_y6",
    "growth_sector_holdout",
    "h0_distance_ladder",
}

REQUIRED_READER_NAMES = {
    "SACC_FITS_READER",
    "SN_DISTANCE_TABLE_READER",
    "BAO_MEASUREMENT_TABLE_READER",
    "PLANCK_PARAMETER_TABLE_READER",
    "DES_Y6_LIKELIHOOD_OR_DATA_VECTOR_READER",
    "GROWTH_HOLDOUT_SUMMARY_READER",
    "DISTANCE_LADDER_SYSTEMATICS_READER",
}

def main():
    data = json.loads(ARTIFACT.read_text())
    assert data["object"] == "PROBE_SPECIFIC_INDEPENDENT_SOURCE_HASHES_AND_SCHEMA_READERS"
    assert data["status"] == "PROBE_READER_TARGET_REGISTRY_ONLY_NO_CERTIFICATION"
    assert data["source_object"] == "INDEPENDENT_SOURCE_HASH_AND_SCHEMA_VALIDATION_FOR_EACH_MULTIPROBE_INPUT"
    assert set(data["reader_targets"]) == REQUIRED_KEYS
    assert {v["required_reader"] for v in data["reader_targets"].values()} == REQUIRED_READER_NAMES
    assert data["summary"]["external_references_supplied"] == 0
    assert data["summary"]["independent_digests_supplied"] == 0
    assert data["summary"]["readers_implemented"] == 0
    assert data["summary"]["schema_validations_passed"] == 0
    assert data["summary"]["inputs_certified_for_profiled_likelihood_execution"] == 0
    assert data["summary"]["ready_for_executed_multiprobe_profiled_likelihood_run"] is False
    for key, entry in data["reader_targets"].items():
        assert entry["independent_external_reference_supplied"] is False, key
        assert entry["independent_digest_supplied"] is False, key
        assert entry["reader_implemented"] is False, key
        assert entry["reader_executes_on_local_payload"] is False, key
        assert entry["schema_validation_passed"] is False, key
        assert entry["certified_for_profiled_likelihood_execution"] is False, key
    assert "Lambda-CDM rejection" in data["does_not_prove"]
    assert "DFM-MKC validation" in data["does_not_prove"]
    assert "any Clay problem" in data["does_not_prove"]
    print("Probe-specific independent source hashes and schema readers target registry verification OK.")
    print("Status:", data["status"])
    print("Required next object:", data["required_next_object"])

if __name__ == "__main__":
    main()
