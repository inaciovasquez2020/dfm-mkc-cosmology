#!/usr/bin/env python3
from pathlib import Path
import json

ROOT = Path(__file__).resolve().parents[1]
ARTIFACT = ROOT / "artifacts/cosmology/multiprobe_likelihood_input_manifest_with_real_paths_candidate_2026_05_22.json"
DOC = ROOT / "docs/status/MULTIPROBE_LIKELIHOOD_INPUT_MANIFEST_WITH_REAL_PATHS_CANDIDATE_2026_05_22.md"

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
    "Lambda-CDM failure",
    "six-parameter flat Lambda-CDM rejection",
    "DFM-MKC validation",
    "empirical discovery",
    "any Clay problem",
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
    assert data["id"] == "MULTIPROBE_LIKELIHOOD_INPUT_MANIFEST_WITH_REAL_DATA_PATHS"
    assert data["status"] == "PARTIAL_REAL_PATHS_CANDIDATE_ONLY_INCOMPLETE_LIKELIHOOD_INPUTS"
    assert data["required_next_object"] == "COMPLETE_CERTIFIED_MULTIPROBE_LIKELIHOOD_INPUT_MANIFEST_WITH_REAL_DATA_PATHS"
    assert set(data["inputs"]) == REQUIRED_KEYS
    assert REQUIRED_DOES_NOT_PROVE.issubset(set(data["does_not_prove"]))

    present = []
    missing = []
    for key, entry in data["inputs"].items():
        assert "classification" in entry
        if entry["path"]:
            present.append(key)
            assert (ROOT / entry["path"]).exists(), (key, entry["path"])
        else:
            missing.append(key)
            assert entry["classification"] == "MISSING"

    assert "act_dr6_likelihood_or_chains" in present
    assert "pantheon_plus_data" in present
    assert "desi_dr2_bao_likelihood_or_covariance" in present
    assert "union3_or_des_sn_crosscheck" in missing
    assert "kids_legacy_likelihood_or_chain" in missing
    assert "hsc_y3_likelihood_or_chain" in missing
    assert "nuisance_prior_table" in missing

    assert data["missing_or_uncertified_inputs"]
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

    print("Multiprobe likelihood real-paths candidate manifest verification OK.")
    print("Status: PARTIAL_REAL_PATHS_CANDIDATE_ONLY_INCOMPLETE_LIKELIHOOD_INPUTS")
    print("Required next object: COMPLETE_CERTIFIED_MULTIPROBE_LIKELIHOOD_INPUT_MANIFEST_WITH_REAL_DATA_PATHS")

if __name__ == "__main__":
    main()
