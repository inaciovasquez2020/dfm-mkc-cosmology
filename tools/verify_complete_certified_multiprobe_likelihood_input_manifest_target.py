#!/usr/bin/env python3
from pathlib import Path
import json

ROOT = Path(__file__).resolve().parents[1]
ARTIFACT = ROOT / "artifacts/cosmology/complete_certified_multiprobe_likelihood_input_manifest_with_real_data_paths_2026_05_22.json"
DOC = ROOT / "docs/status/COMPLETE_CERTIFIED_MULTIPROBE_LIKELIHOOD_INPUT_MANIFEST_WITH_REAL_DATA_PATHS_2026_05_22.md"

REQUIRED_KEYS = {
    "planck_2018_likelihood",
    "planck_2018_lensing",
    "act_dr6_likelihood_or_chains",
    "desi_dr2_bao_likelihood_or_covariance",
    "desi_dr2_bao_bestfit_or_chain",
    "pantheon_plus_data",
    "pantheon_plus_covariance",
    "sh0es_calibrator_data",
    "union3_or_des_sn_crosscheck",
    "des_y6_3x2pt_likelihood_or_chain",
    "kids_legacy_likelihood_or_chain",
    "hsc_y3_likelihood_or_chain",
    "cmb_lensing_likelihood_or_chain",
    "nuisance_prior_table",
    "systematics_profile_config",
    "holdout_split_manifest",
}

REQUIRED_DOES_NOT_PROVE = {
    "complete multiprobe likelihood input availability",
    "certified multiprobe likelihood execution readiness",
    "Lambda-CDM failure",
    "six-parameter flat Lambda-CDM rejection",
    "DFM-MKC validation",
    "empirical discovery",
    "any Clay problem",
}

REQUIRED_FALSE_FLAGS = {
    "all_required_paths_present",
    "all_required_paths_certified",
    "all_probe_classes_covered",
    "all_checksums_present",
    "all_provenance_records_present",
    "ready_for_executed_likelihood_run",
}

FORBIDDEN_PROMOTION_TOKENS = {
    "LCDM_DISPROVED",
    "LAMBDA_CDM_DISPROVED",
    "EXECUTED_LCDM_REJECTION",
    "DFM_MKC_VALIDATED",
    "EMPIRICAL_DISCOVERY_CLOSED",
    "ALTERNATIVE_MODEL_VALIDATED"
}

def main():
    assert ARTIFACT.exists(), ARTIFACT
    assert DOC.exists(), DOC

    data = json.loads(ARTIFACT.read_text())
    assert data["id"] == "COMPLETE_CERTIFIED_MULTIPROBE_LIKELIHOOD_INPUT_MANIFEST_WITH_REAL_DATA_PATHS"
    assert data["status"] == "CERTIFICATION_TARGET_ONLY_REQUIRED_INPUTS_MISSING"
    assert data["required_next_object"] == "FILE_LEVEL_MULTIPROBE_INPUT_DIGEST_AND_PROVENANCE_MANIFEST"
    assert set(data["required_certified_inputs"]) == REQUIRED_KEYS
    assert REQUIRED_DOES_NOT_PROVE.issubset(set(data["does_not_prove"]))

    for key, entry in data["required_certified_inputs"].items():
        assert entry["required"] is True, key
        assert "current_status" in entry, key
        assert "certification_required" in entry, key

    for flag in REQUIRED_FALSE_FLAGS:
        assert data["current_certification_status"][flag] is False, flag

    assert "candidate paths" in data["blocking_reason"]
    assert "does not certify complete likelihood inputs" in data["boundary"]

    body = json.dumps(data, sort_keys=True)
    for token in FORBIDDEN_PROMOTION_TOKENS:
        assert token not in body, token

    text = DOC.read_text()
    assert data["status"] in text
    assert data["required_next_object"] in text
    assert "Does not prove" in text
    assert "complete multiprobe likelihood input availability" in text
    assert "any Clay problem" in text

    print("Complete certified multiprobe likelihood input manifest target verification OK.")
    print("Status: CERTIFICATION_TARGET_ONLY_REQUIRED_INPUTS_MISSING")
    print("Required next object: FILE_LEVEL_MULTIPROBE_INPUT_DIGEST_AND_PROVENANCE_MANIFEST")

if __name__ == "__main__":
    main()
