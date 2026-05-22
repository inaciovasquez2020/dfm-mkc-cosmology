#!/usr/bin/env python3
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / "artifacts/cosmology/act_dr6_public_release_digest_and_full_sacc_schema_reader_2026_05_22.json"
OUT = ROOT / "artifacts/cosmology/act_dr6_external_release_reference_and_sacc_schema_conformance_rules_2026_05_22.json"

REQUIRED_SACC_CONFORMANCE_RULES = [
    "fits_payload_opens",
    "required_hdus_present",
    "tracers_table_present",
    "data_vector_present",
    "covariance_matrix_present",
    "metadata_consistent",
    "likelihood_reader_maps_payload_to_numeric_arrays",
    "external_release_digest_matches_local_payload",
]

def main():
    source = json.loads(SOURCE.read_text())

    rules = {
        rule: {
            "required": True,
            "validated": False,
            "validation_status": "RULE_DEFINED_NOT_VALIDATED"
        }
        for rule in REQUIRED_SACC_CONFORMANCE_RULES
    }

    artifact = {
        "object": "ACT_DR6_EXTERNAL_RELEASE_REFERENCE_AND_SACC_SCHEMA_CONFORMANCE_RULES",
        "date": "2026-05-22",
        "status": "CONFORMANCE_RULES_DEFINED_EXTERNAL_REFERENCE_MISSING",
        "source_object": source["object"],
        "input_key": "act_dr6_cmb_lite",
        "local_path": source["local_path"],
        "external_release_reference": {
            "release_url_or_doi": None,
            "publisher_or_collaboration": "ACT",
            "release_name": "ACT DR6 lite payload",
            "external_digest": None,
            "digest_algorithm": "sha256",
            "external_reference_supplied": False,
            "external_digest_supplied": False,
            "external_digest_matches_local_payload": False,
        },
        "sacc_schema_conformance_rules": rules,
        "summary": {
            "rules_defined": len(rules),
            "rules_validated": 0,
            "external_reference_supplied": False,
            "external_digest_supplied": False,
            "external_digest_matches_local_payload": False,
            "full_sacc_schema_conformance_established": False,
            "certified_for_profiled_likelihood_execution": False
        },
        "required_next_object": "ACT_DR6_EXTERNAL_RELEASE_DIGEST_SUPPLIED_AND_SACC_CONFORMANCE_VALIDATOR",
        "does_not_prove": [
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
    }

    OUT.write_text(json.dumps(artifact, indent=2) + "\n")

if __name__ == "__main__":
    main()
