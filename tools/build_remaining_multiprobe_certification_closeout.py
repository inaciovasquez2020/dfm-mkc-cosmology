#!/usr/bin/env python3
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / "artifacts/cosmology/act_dr6_external_reference_sacc_conformance_validator_2026_05_22.json"
OUT_ACT = ROOT / "artifacts/cosmology/act_dr6_external_digest_or_reproducible_download_lock_2026_05_22.json"
OUT_ALL = ROOT / "artifacts/cosmology/remaining_multiprobe_certification_closeout_2026_05_22.json"

REMAINING_OBJECTS = [
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
    "OUT_OF_SAMPLE_MULTIPROBE_LCDM_REJECTION_CERTIFICATE"
]

DOES_NOT_PROVE = [
    "ACT DR6 public release digest certification",
    "ACT DR6 full SACC schema certification",
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

def main():
    source = json.loads(SOURCE.read_text())

    act_lock = {
        "object": "ACT_DR6_EXTERNAL_DIGEST_OR_REPRODUCIBLE_DOWNLOAD_LOCK",
        "date": "2026-05-22",
        "status": "LOCK_ONLY_EXTERNAL_DIGEST_OR_REPRODUCIBLE_DOWNLOAD_NOT_SUPPLIED",
        "source_object": source["object"],
        "local_path": source["local_path"],
        "local_sha256": source["local_sha256"],
        "official_external_references": source["official_external_references"],
        "external_digest": None,
        "external_digest_supplied": False,
        "reproducible_download_command_supplied": False,
        "download_reproduces_local_sha256": False,
        "act_dr6_certified_for_profiled_likelihood_execution": False,
        "required_next_object": "ACT_DR6_REPRODUCIBLE_DOWNLOAD_COMMAND_OR_EXTERNAL_SHA256_DIGEST",
        "does_not_prove": DOES_NOT_PROVE,
    }

    closeout = {
        "object": "REMAINING_MULTIPROBE_CERTIFICATION_CLOSEOUT_2026_05_22",
        "date": "2026-05-22",
        "status": "DAY_CLOSEOUT_REMAINING_OBJECTS_EXPLICIT_NO_EMPIRICAL_CLAIM",
        "source_object": act_lock["object"],
        "remaining_objects": REMAINING_OBJECTS,
        "terminal_for_today": True,
        "next_required_object": "ACT_DR6_REPRODUCIBLE_DOWNLOAD_COMMAND_OR_EXTERNAL_SHA256_DIGEST",
        "proof_status": {
            "mathematical_proof": False,
            "mathematical_disproof": False,
            "empirical_validation": False,
            "lambda_cdm_rejection": False,
            "dfm_mkc_validation": False,
            "pipeline_state": "AUDITABLE_VALIDATION_PIPELINE_ADVANCED_BUT_NOT_CLOSED"
        },
        "does_not_prove": DOES_NOT_PROVE,
    }

    OUT_ACT.write_text(json.dumps(act_lock, indent=2) + "\n")
    OUT_ALL.write_text(json.dumps(closeout, indent=2) + "\n")

if __name__ == "__main__":
    main()
