#!/usr/bin/env python3
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / "artifacts/cosmology/act_dr6_external_digest_or_reproducible_download_lock_2026_05_22.json"
PREV = ROOT / "artifacts/cosmology/act_dr6_external_reference_sacc_conformance_validator_2026_05_22.json"
OUT = ROOT / "artifacts/cosmology/act_dr6_reproducible_download_command_or_external_sha256_digest_2026_05_22.json"

OFFICIAL_REFERENCES = {
    "act_dr6_data_products": "https://act.princeton.edu/act-dr6-data-products",
    "dr6_act_lite_repository": "https://github.com/ACTCollaboration/DR6-ACT-lite",
}

REPRODUCIBLE_DOWNLOAD_COMMANDS = [
    "git clone https://github.com/ACTCollaboration/DR6-ACT-lite.git DR6-ACT-lite",
    "cd DR6-ACT-lite",
    "python3 -m pip install -e .",
    "cobaya-install act_dr6_cmbonly",
]

def main():
    source = json.loads(SOURCE.read_text())
    prev = json.loads(PREV.read_text())

    artifact = {
        "object": "ACT_DR6_REPRODUCIBLE_DOWNLOAD_COMMAND_OR_EXTERNAL_SHA256_DIGEST",
        "date": "2026-05-22",
        "status": "REPRODUCIBLE_DOWNLOAD_COMMAND_BOUND_EXTERNAL_DIGEST_NOT_SUPPLIED_NOT_EXECUTED",
        "source_object": source["object"],
        "input_key": "act_dr6_cmb_lite",
        "official_references": OFFICIAL_REFERENCES,
        "local_path": source["local_path"],
        "local_sha256": source["local_sha256"],
        "external_sha256_digest": None,
        "external_sha256_digest_supplied": False,
        "reproducible_download_command_supplied": True,
        "reproducible_download_commands": REPRODUCIBLE_DOWNLOAD_COMMANDS,
        "reproducible_download_executed": False,
        "downloaded_payload_sha256": None,
        "download_reproduces_local_sha256": False,
        "prior_partial_validator_status": prev["status"],
        "act_dr6_certified_for_profiled_likelihood_execution": False,
        "required_next_object": "ACT_DR6_REPRODUCIBLE_DOWNLOAD_EXECUTION_AND_LOCAL_SHA256_COMPARISON",
        "does_not_prove": [
            "ACT DR6 public release digest certification",
            "ACT DR6 reproducible download execution",
            "ACT DR6 downloaded payload hash match",
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
    }

    OUT.write_text(json.dumps(artifact, indent=2) + "\n")

if __name__ == "__main__":
    main()
