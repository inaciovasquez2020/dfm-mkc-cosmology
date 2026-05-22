#!/usr/bin/env python3
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
ARTIFACT = ROOT / "artifacts/cosmology/file_level_multiprobe_input_digest_and_provenance_manifest_2026_05_22.json"

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
    assert data["object"] == "FILE_LEVEL_MULTIPROBE_INPUT_DIGEST_AND_PROVENANCE_MANIFEST"
    assert data["status"] == "PARTIAL_DIGEST_AND_PROVENANCE_MANIFEST_ONLY_NOT_CERTIFIED"
    assert set(data["input_entries"]) == REQUIRED_KEYS
    assert data["summary"]["ready_for_executed_likelihood_run"] is False
    assert data["summary"]["certified_likelihood_inputs"] == 0
    assert "union3_or_des_sn_crosscheck" in data["missing_inputs"]
    assert "kids_legacy_likelihood_or_chain" in data["missing_inputs"]
    assert "hsc_y3_likelihood_or_chain" in data["missing_inputs"]
    assert "nuisance_prior_table" in data["missing_inputs"]
    assert "Lambda-CDM rejection" in data["does_not_prove"]
    assert "DFM-MKC validation" in data["does_not_prove"]
    assert "any Clay problem" in data["does_not_prove"]
    for entry in data["input_entries"].values():
        assert "path" in entry
        assert "exists" in entry
    print("File-level multiprobe input digest and provenance manifest verification OK.")
    print("Status:", data["status"])
    print("Required next object:", data["required_next_object"])

if __name__ == "__main__":
    main()
