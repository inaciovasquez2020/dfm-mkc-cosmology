#!/usr/bin/env python3
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / "artifacts/cosmology/independent_source_hash_and_schema_validation_for_each_multiprobe_input_2026_05_22.json"
OUT = ROOT / "artifacts/cosmology/probe_specific_independent_source_hashes_and_schema_readers_2026_05_22.json"

PROBE_READER_TARGETS = {
    "act_dr6_cmb_lite": {
        "probe": "ACT_DR6_CMB_LITE",
        "required_reader": "SACC_FITS_READER",
        "required_external_reference": "ACT_DR6_LITE_PUBLIC_RELEASE_HASH_OR_DOI",
        "schema_family": "sacc_fits",
    },
    "pantheon_plus_shoes": {
        "probe": "PANTHEON_PLUS_SHOES",
        "required_reader": "SN_DISTANCE_TABLE_READER",
        "required_external_reference": "PANTHEON_PLUS_SHOES_PUBLIC_RELEASE_HASH_OR_DOI",
        "schema_family": "supernova_distance_table",
    },
    "desi_dr2": {
        "probe": "DESI_DR2",
        "required_reader": "BAO_MEASUREMENT_TABLE_READER",
        "required_external_reference": "DESI_DR2_PUBLIC_RELEASE_HASH_OR_DOI",
        "schema_family": "bao_measurement_table",
    },
    "planck_baseline": {
        "probe": "PLANCK_2018_BASELINE",
        "required_reader": "PLANCK_PARAMETER_TABLE_READER",
        "required_external_reference": "PLANCK_2018_PUBLIC_RELEASE_HASH_OR_DOI",
        "schema_family": "cmb_parameter_table",
    },
    "des_y6": {
        "probe": "DES_Y6",
        "required_reader": "DES_Y6_LIKELIHOOD_OR_DATA_VECTOR_READER",
        "required_external_reference": "DES_Y6_PUBLIC_RELEASE_HASH_OR_DOI",
        "schema_family": "weak_lensing_or_bao_release_payload",
    },
    "growth_sector_holdout": {
        "probe": "GROWTH_SECTOR_HOLDOUT",
        "required_reader": "GROWTH_HOLDOUT_SUMMARY_READER",
        "required_external_reference": "GROWTH_HOLDOUT_SOURCE_HASH_OR_DOI",
        "schema_family": "growth_summary_payload",
    },
    "h0_distance_ladder": {
        "probe": "H0_DISTANCE_LADDER",
        "required_reader": "DISTANCE_LADDER_SYSTEMATICS_READER",
        "required_external_reference": "DISTANCE_LADDER_SOURCE_HASH_OR_DOI",
        "schema_family": "distance_ladder_systematics_payload",
    },
}

def main():
    source = json.loads(SOURCE.read_text())
    targets = {}

    for key, validation in source["validations"].items():
        target = PROBE_READER_TARGETS[key]
        targets[key] = {
            "local_path": validation["local_path"],
            "local_digest_observed": validation["local_digest_observed"],
            "probe": target["probe"],
            "schema_family": target["schema_family"],
            "required_reader": target["required_reader"],
            "required_external_reference": target["required_external_reference"],
            "independent_external_reference_supplied": False,
            "independent_digest_supplied": False,
            "reader_implemented": False,
            "reader_executes_on_local_payload": False,
            "schema_validation_passed": False,
            "certified_for_profiled_likelihood_execution": False,
        }

    artifact = {
        "object": "PROBE_SPECIFIC_INDEPENDENT_SOURCE_HASHES_AND_SCHEMA_READERS",
        "date": "2026-05-22",
        "status": "PROBE_READER_TARGET_REGISTRY_ONLY_NO_CERTIFICATION",
        "source_object": source["object"],
        "reader_targets": targets,
        "summary": {
            "total_probe_targets": len(targets),
            "external_references_supplied": 0,
            "independent_digests_supplied": 0,
            "readers_implemented": 0,
            "readers_executing_on_local_payloads": 0,
            "schema_validations_passed": 0,
            "inputs_certified_for_profiled_likelihood_execution": 0,
            "ready_for_executed_multiprobe_profiled_likelihood_run": False
        },
        "required_next_object": "ACT_DR6_SACC_READER_AND_INDEPENDENT_RELEASE_HASH_VALIDATION",
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
