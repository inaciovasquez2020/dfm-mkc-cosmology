#!/usr/bin/env python3
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / "artifacts/cosmology/act_dr6_full_sacc_schema_validation_2026_05_22.json"
OUT = ROOT / "artifacts/cosmology/act_dr6_certified_profiled_likelihood_input_2026_05_22.json"

def main():
    source = json.loads(SOURCE.read_text())
    preconditions = {
        "local_payload_exists": source["checks"]["local_payload_exists"],
        "reproducible_download_sha256_matched": source["checks"]["reproducible_download_sha256_matched"],
        "full_sacc_schema_validation_passed": source["full_sacc_schema_validation_passed"],
        "data_vector_present": source["checks"]["data_vector_present"],
        "covariance_present": source["checks"]["covariance_present"],
        "tracers_present": source["checks"]["tracers_present"],
    }
    certified = all(preconditions.values())

    artifact = {
        "object": "ACT_DR6_CERTIFIED_PROFILED_LIKELIHOOD_INPUT",
        "date": "2026-05-22",
        "status": (
            "ACT_DR6_CERTIFIED_PROFILED_LIKELIHOOD_INPUT_CLOSED_NO_LIKELIHOOD_EXECUTION"
            if certified else
            "ACT_DR6_CERTIFIED_PROFILED_LIKELIHOOD_INPUT_BLOCKED"
        ),
        "source_object": source["object"],
        "local_path": source["local_path"],
        "local_sha256": source["local_sha256"],
        "preconditions": preconditions,
        "certified_for_profiled_likelihood_execution": certified,
        "profiled_likelihood_execution_performed": False,
        "required_next_object": (
            "PANTHEON_PLUS_SHOES_EXTERNAL_DIGEST_AND_SCHEMA_READER"
            if certified else
            "REPAIR_ACT_DR6_FULL_SACC_SCHEMA_VALIDATION"
        ),
        "does_not_prove": [
            "executed ACT DR6 likelihood run",
            "executed multiprobe likelihood run",
            "complete certified multiprobe likelihood manifest",
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
    print("ACT DR6 certified profiled likelihood input artifact written.")
    print("Status:", artifact["status"])
    print("Required next object:", artifact["required_next_object"])

if __name__ == "__main__":
    main()
