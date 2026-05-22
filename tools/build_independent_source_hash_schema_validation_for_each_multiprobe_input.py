#!/usr/bin/env python3
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / "artifacts/cosmology/certified_file_level_multiprobe_likelihood_inputs_2026_05_22.json"
OUT = ROOT / "artifacts/cosmology/independent_source_hash_and_schema_validation_for_each_multiprobe_input_2026_05_22.json"

REQUIRED_VALIDATION_FIELDS = [
    "local_path",
    "local_digest_observed",
    "independent_source_url_or_release_id",
    "independent_source_digest",
    "independent_hash_match_verified",
    "schema_validator_or_reader",
    "schema_validation_passed",
    "likelihood_role_verified",
    "certified_for_profiled_likelihood_execution",
]

def main():
    source = json.loads(SOURCE.read_text())
    validations = {}

    for key, entry in source["inputs"].items():
        validations[key] = {
            "local_path": entry["path"],
            "local_digest_observed": entry["sha256_or_tree_sha256"],
            "independent_source_url_or_release_id": None,
            "independent_source_digest": None,
            "independent_hash_match_verified": False,
            "schema_validator_or_reader": None,
            "schema_validation_passed": False,
            "likelihood_role_verified": False,
            "certified_for_profiled_likelihood_execution": False,
        }

    artifact = {
        "object": "INDEPENDENT_SOURCE_HASH_AND_SCHEMA_VALIDATION_FOR_EACH_MULTIPROBE_INPUT",
        "date": "2026-05-22",
        "status": "VALIDATION_GATE_ONLY_NO_INDEPENDENT_HASH_OR_SCHEMA_CERTIFICATION",
        "source_object": source["object"],
        "required_validation_fields": REQUIRED_VALIDATION_FIELDS,
        "validations": validations,
        "summary": {
            "total_inputs": len(validations),
            "inputs_with_local_digest": sum(1 for v in validations.values() if v["local_digest_observed"]),
            "inputs_with_independent_source_digest": 0,
            "inputs_with_hash_match_verified": 0,
            "inputs_with_schema_validation_passed": 0,
            "inputs_certified_for_profiled_likelihood_execution": 0,
            "ready_for_executed_multiprobe_profiled_likelihood_run": False,
        },
        "required_next_object": "PROBE_SPECIFIC_INDEPENDENT_SOURCE_HASHES_AND_SCHEMA_READERS",
        "does_not_prove": [
            "independent source certification",
            "schema certification",
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
