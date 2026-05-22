#!/usr/bin/env python3
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
ACT = ROOT / "artifacts/cosmology/act_dr6_external_digest_or_reproducible_download_lock_2026_05_22.json"
ALL = ROOT / "artifacts/cosmology/remaining_multiprobe_certification_closeout_2026_05_22.json"

REQUIRED_REMAINING = {
    "ACT_DR6_EXTERNAL_DIGEST_OR_REPRODUCIBLE_DOWNLOAD_LOCK",
    "PANTHEON_PLUS_SHOES_EXTERNAL_DIGEST_AND_SCHEMA_READER",
    "DESI_DR2_EXTERNAL_DIGEST_AND_BAO_SCHEMA_READER",
    "PLANCK_2018_EXTERNAL_DIGEST_AND_PARAMETER_SCHEMA_READER",
    "DES_Y6_EXTERNAL_DIGEST_AND_LIKELIHOOD_SCHEMA_READER",
    "GROWTH_SECTOR_EXTERNAL_DIGEST_AND_SCHEMA_READER",
    "H0_DISTANCE_LADDER_EXTERNAL_DIGEST_AND_SCHEMA_READER",
    "NUISANCE_PRIOR_TABLE_CERTIFICATION",
    "COVARIANCE_CHAIN_COMPATIBILITY_CERTIFICATION",
    "COMPLETE_CERTIFIED_MULTIPROBE_LIKELIHOOD_INPUT_MANIFEST",
    "EXECUTED_MULTIPROBE_PROFILED_LIKELIHOOD_RUN",
    "OUT_OF_SAMPLE_MULTIPROBE_LCDM_REJECTION_CERTIFICATE",
}

def main():
    act = json.loads(ACT.read_text())
    closeout = json.loads(ALL.read_text())

    assert act["object"] == "ACT_DR6_EXTERNAL_DIGEST_OR_REPRODUCIBLE_DOWNLOAD_LOCK"
    assert act["status"] == "LOCK_ONLY_EXTERNAL_DIGEST_OR_REPRODUCIBLE_DOWNLOAD_NOT_SUPPLIED"
    assert act["external_digest"] is None
    assert act["external_digest_supplied"] is False
    assert act["reproducible_download_command_supplied"] is False
    assert act["download_reproduces_local_sha256"] is False
    assert act["act_dr6_certified_for_profiled_likelihood_execution"] is False

    assert closeout["object"] == "REMAINING_MULTIPROBE_CERTIFICATION_CLOSEOUT_2026_05_22"
    assert closeout["status"] == "DAY_CLOSEOUT_REMAINING_OBJECTS_EXPLICIT_NO_EMPIRICAL_CLAIM"
    assert set(closeout["remaining_objects"]) == REQUIRED_REMAINING
    assert closeout["terminal_for_today"] is True
    assert closeout["proof_status"]["mathematical_proof"] is False
    assert closeout["proof_status"]["mathematical_disproof"] is False
    assert closeout["proof_status"]["empirical_validation"] is False
    assert closeout["proof_status"]["lambda_cdm_rejection"] is False
    assert closeout["proof_status"]["dfm_mkc_validation"] is False

    for boundary in [
        "executed multiprobe likelihood run",
        "Lambda-CDM rejection",
        "DFM-MKC validation",
        "any Clay problem",
    ]:
        assert boundary in act["does_not_prove"]
        assert boundary in closeout["does_not_prove"]

    print("Remaining multiprobe certification closeout verification OK.")
    print("Status:", closeout["status"])
    print("Next required object:", closeout["next_required_object"])

if __name__ == "__main__":
    main()
