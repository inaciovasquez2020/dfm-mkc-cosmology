#!/usr/bin/env python3
from pathlib import Path
import json

ROOT = Path(__file__).resolve().parents[1]
TARGET = ROOT / "artifacts/cosmology/executed_multiprobe_profiled_likelihood_run_2026_05_22.json"
TEMPLATE = ROOT / "artifacts/cosmology/multiprobe_likelihood_input_manifest_template_2026_05_22.json"
DOC = ROOT / "docs/status/EXECUTED_MULTIPROBE_PROFILED_LIKELIHOOD_RUN_2026_05_22.md"
REAL_MANIFEST = ROOT / "data/likelihood_inputs/multiprobe_likelihood_input_manifest.json"

REQUIRED_DOES_NOT_PROVE = {
    "Lambda-CDM failure",
    "six-parameter flat Lambda-CDM rejection",
    "DFM-MKC validation",
    "empirical discovery",
    "any Clay problem",
}

REQUIRED_INPUT_KEYS = {
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

FORBIDDEN_PROMOTION_TOKENS = {
    "LCDM_DISPROVED",
    "LAMBDA_CDM_DISPROVED",
    "EXECUTED_LCDM_REJECTION",
    "DFM_MKC_VALIDATED",
    "EMPIRICAL_DISCOVERY_CLOSED",
    "ALTERNATIVE_MODEL_VALIDATED"
}

def validate_no_promotion(data):
    assert REQUIRED_DOES_NOT_PROVE.issubset(set(data["does_not_prove"]))
    body = json.dumps(data, sort_keys=True)
    for token in FORBIDDEN_PROMOTION_TOKENS:
        assert token not in body, token

def main():
    assert TARGET.exists(), TARGET
    assert TEMPLATE.exists(), TEMPLATE
    assert DOC.exists(), DOC

    target = json.loads(TARGET.read_text())
    assert target["id"] == "EXECUTED_MULTIPROBE_PROFILED_LIKELIHOOD_RUN"
    assert target["status"] == "INPUT_GATED_EXECUTION_TARGET_ONLY_NO_LIKELIHOOD_RUN"
    assert target["required_next_object"] == "MULTIPROBE_LIKELIHOOD_INPUT_MANIFEST_WITH_REAL_DATA_PATHS"
    assert all(value is False for value in target["current_execution_status"].values())
    assert "does not execute a real likelihood" in target["boundary"]
    validate_no_promotion(target)

    template = json.loads(TEMPLATE.read_text())
    assert template["id"] == "MULTIPROBE_LIKELIHOOD_INPUT_MANIFEST_TEMPLATE"
    assert template["status"] == "TEMPLATE_ONLY_REAL_DATA_PATHS_NOT_SUPPLIED"
    assert set(template["inputs"]) == REQUIRED_INPUT_KEYS
    assert all(value is None for value in template["inputs"].values())
    validate_no_promotion(template)

    for block in target["required_probe_inputs"]:
        for key in block["required_files"]:
            assert key in REQUIRED_INPUT_KEYS

    text = DOC.read_text()
    assert target["status"] in text
    assert target["required_next_object"] in text
    assert "Does not prove" in text
    assert "Lambda-CDM failure" in text
    assert "any Clay problem" in text

    if REAL_MANIFEST.exists():
        manifest = json.loads(REAL_MANIFEST.read_text())
        missing = [key for key in REQUIRED_INPUT_KEYS if not manifest.get("inputs", {}).get(key)]
        assert not missing, f"real manifest present but missing inputs: {missing}"

    print("Executed multiprobe profiled likelihood run gate verification OK.")
    print("Status: INPUT_GATED_EXECUTION_TARGET_ONLY_NO_LIKELIHOOD_RUN")
    print("Required next object: MULTIPROBE_LIKELIHOOD_INPUT_MANIFEST_WITH_REAL_DATA_PATHS")

if __name__ == "__main__":
    main()
