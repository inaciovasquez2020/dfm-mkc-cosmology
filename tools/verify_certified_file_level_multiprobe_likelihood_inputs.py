#!/usr/bin/env python3
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
ARTIFACT = ROOT / "artifacts/cosmology/certified_file_level_multiprobe_likelihood_inputs_2026_05_22.json"

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
    assert data["object"] == "CERTIFIED_FILE_LEVEL_MULTIPROBE_LIKELIHOOD_INPUTS"
    assert data["status"] == "CERTIFICATION_GATE_ONLY_NO_INPUT_CERTIFIED"
    assert data["source_object"] == "FILE_LEVEL_MULTIPROBE_INPUT_DIGEST_AND_PROVENANCE_MANIFEST"
    assert set(data["inputs"]) == REQUIRED_KEYS
    assert data["summary"]["certified_inputs"] == 0
    assert data["summary"]["ready_for_executed_multiprobe_profiled_likelihood_run"] is False
    for key, entry in data["inputs"].items():
        assert entry["likelihood_role"] != "unassigned", key
        assert entry["source_provenance_status"] == "LOCAL_CANDIDATE_ONLY_NOT_INDEPENDENTLY_CERTIFIED"
        assert entry["format_validation_status"] == "OBSERVED_PATH_ONLY_SCHEMA_NOT_CERTIFIED"
        assert entry["independent_source_hash_verified"] is False
        assert entry["schema_or_likelihood_reader_verified"] is False
        assert entry["certified_for_profiled_likelihood_execution"] is False
    assert "independent source hash verification for every input" in data["remaining_missing_certifications"]
    assert "schema or likelihood-reader validation for every input" in data["remaining_missing_certifications"]
    assert "Lambda-CDM rejection" in data["does_not_prove"]
    assert "DFM-MKC validation" in data["does_not_prove"]
    assert "any Clay problem" in data["does_not_prove"]
    print("Certified file-level multiprobe likelihood inputs gate verification OK.")
    print("Status:", data["status"])
    print("Required next object:", data["required_next_object"])

if __name__ == "__main__":
    main()
