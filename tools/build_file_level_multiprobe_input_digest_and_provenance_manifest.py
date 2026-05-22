#!/usr/bin/env python3
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "artifacts/cosmology/file_level_multiprobe_input_digest_and_provenance_manifest_2026_05_22.json"

REQUIRED_KEYS = {
    "act_dr6_cmb_lite": "artifacts/public_payloads/act_lite_numeric_like_extracted_2026_05_21/DR6-ACT-lite-main__act_dr6_cmbonly__data__act_dr6_cmb_sacc.fits",
    "pantheon_plus_shoes": "artifacts/external_data_sources/pantheon_plus_shoes_1_data",
    "desi_dr2": "public_data/desi_dr2",
    "planck_baseline": "public_data/planck/planck_2018_baseline_params.csv",
    "des_y6": "public_data/des_y6",
    "growth_sector_holdout": "artifacts/cosmology/growth_sector_holdout_compatibility_test_2026_05_22.json",
    "h0_distance_ladder": "artifacts/cosmology/h0_distance_ladder_systematics_profile_2026_05_22.json",
}

MISSING_INPUTS = [
    "union3_or_des_sn_crosscheck",
    "kids_legacy_likelihood_or_chain",
    "hsc_y3_likelihood_or_chain",
    "nuisance_prior_table",
]

def exists_status(rel):
    path = ROOT / rel
    return {
        "path": rel,
        "exists": path.exists(),
        "is_file": path.is_file(),
        "is_dir": path.is_dir(),
    }

def main():
    entries = {key: exists_status(path) for key, path in REQUIRED_KEYS.items()}
    artifact = {
        "object": "FILE_LEVEL_MULTIPROBE_INPUT_DIGEST_AND_PROVENANCE_MANIFEST",
        "date": "2026-05-22",
        "status": "PARTIAL_DIGEST_AND_PROVENANCE_MANIFEST_ONLY_NOT_CERTIFIED",
        "input_entries": entries,
        "missing_inputs": MISSING_INPUTS,
        "summary": {
            "candidate_inputs_found": sum(1 for v in entries.values() if v["exists"]),
            "candidate_inputs_required": len(entries),
            "certified_likelihood_inputs": 0,
            "ready_for_executed_likelihood_run": False
        },
        "required_next_object": "CERTIFIED_FILE_LEVEL_MULTIPROBE_LIKELIHOOD_INPUTS",
        "does_not_prove": [
            "complete certified likelihood manifest",
            "executed multiprobe likelihood run",
            "Lambda-CDM rejection",
            "six-parameter flat Lambda-CDM rejection",
            "alternative-model validation",
            "DFM-MKC validation",
            "dark matter resolution",
            "dark energy resolution",
            "any Clay problem"
        ]
    }
    OUT.write_text(json.dumps(artifact, indent=2) + "\n")

if __name__ == "__main__":
    main()
