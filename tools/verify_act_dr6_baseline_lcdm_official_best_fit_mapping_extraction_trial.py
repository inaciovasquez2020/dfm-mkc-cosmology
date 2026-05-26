#!/usr/bin/env python3
import json
from pathlib import Path

ART = Path("artifacts/dfm_mkc/act_dr6_baseline_lcdm_official_best_fit_mapping_extraction_trial_2026_05_25.json")
DOC = Path("docs/status/ACT_DR6_BASELINE_LCDM_OFFICIAL_BEST_FIT_MAPPING_EXTRACTION_TRIAL_2026_05_25.md")
TRIAL = Path("tools/materialize_act_dr6_baseline_lcdm_official_best_fit_mapping_extraction_trial.py")
PAYLOAD_DIR = Path("artifacts/dfm_mkc/act_dr6_official_best_fits_dr6_lcdm_payload_2026_05_25")

REQUIRED_BOUNDARIES = {
    "baseline LCDM prediction vector exists",
    "baseline LCDM prediction vector has been promoted",
    "baseline LCDM prediction vector is fully row-audited",
    "baseline LCDM prediction vector is physically correct",
    "DFM-MKC prediction vector exists",
    "DFM-MKC prediction vector is correct",
    "ACT DR6 residual eigenspace empirical comparison has been run",
    "DFM-MKC empirical validation",
    "Lambda-CDM failure",
    "dark matter resolution",
    "dark energy resolution",
    "dark matter is liquid",
    "dark matter is solid",
    "dark matter phase transition is physically real",
    "ACT validation of DFM-MKC",
    "CMB validation of DFM-MKC",
    "independent empirical replication",
    "gravity closure",
    "Chronos-RR",
    "H4.1/FGL",
    "P vs NP",
    "any Clay problem",
}

VALID_STATUSES = {
    "OFFICIAL_BEST_FIT_MAPPING_EXTRACTION_TRIAL_BLOCKED_NO_CERTIFIED_ROW_MAPPING",
    "OFFICIAL_BEST_FIT_MAPPING_EXTRACTION_TRIAL_RAN_VECTOR_CANDIDATE_NOT_PROMOTED",
}

def main() -> None:
    for p in [ART, DOC, TRIAL, PAYLOAD_DIR]:
        assert p.exists(), p

    data = json.loads(ART.read_text())
    doc = DOC.read_text()
    trial = TRIAL.read_text()

    assert data["id"] == "ACT_DR6_BASELINE_LCDM_OFFICIAL_BEST_FIT_MAPPING_EXTRACTION_TRIAL_2026_05_25"
    assert data["status"] in VALID_STATUSES
    assert data["official_best_fit_spectra_file"]["bytes"] > 0
    assert len(data["official_best_fit_spectra_file"]["sha256"]) == 64
    assert data["official_best_fit_spectra_file"]["url"].endswith("act_dr6.02_best_fits_dr6_lcdm.tar.gz")
    assert data["combined_numeric_table_sha256"]
    assert data["row_order_metadata"]["path"]
    assert data["row_mapping"]["path"]
    assert data["extraction_audit"]["path"]
    assert data["promotion_decision"] == "DO_NOT_PROMOTE_TO_ACT_DR6_BASELINE_LCDM_PREDICTION_VECTOR"
    assert data["still_missing_objects_after_this_trial"] == [
        "ACT_DR6_BASELINE_LCDM_PREDICTION_VECTOR",
        "ACT_DR6_DFM_MKC_PREDICTION_VECTOR",
    ]
    assert data["physical_dark_matter_phase_claim_status"] == "HYPOTHESIS_ONLY"
    assert REQUIRED_BOUNDARIES <= set(data["does_not_prove"])

    for path_key in [
        data["row_order_metadata"]["path"],
        data["row_mapping"]["path"],
        data["extraction_audit"]["path"],
        data["combined_numeric_table"],
    ]:
        assert Path(path_key).exists(), path_key

    for token in [
        "download_official_tar",
        "safe_extract_tar",
        "build_combined_table",
        "load_sacc_metadata",
        "construct_mapping",
        "run_extraction_if_possible",
        "DO_NOT_PROMOTE_TO_ACT_DR6_BASELINE_LCDM_PREDICTION_VECTOR",
    ]:
        assert token in trial, token

    for token in (
        REQUIRED_BOUNDARIES
        | {
            "ACT_DR6_BASELINE_LCDM_OFFICIAL_BEST_FIT_MAPPING_EXTRACTION_TRIAL",
            "ACT_DR6_BASELINE_LCDM_PREDICTION_VECTOR",
            "HYPOTHESIS_ONLY",
        }
    ):
        assert token in doc, token

    print("ACT_DR6_BASELINE_LCDM_OFFICIAL_BEST_FIT_MAPPING_EXTRACTION_TRIAL_OK")

if __name__ == "__main__":
    main()
