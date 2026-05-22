#!/usr/bin/env python3
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
ARTIFACT = ROOT / "artifacts/cosmology/supplied_bound_external_nuisance_prior_source_records_with_digests_2026_05_22.json"
DOC = ROOT / "docs/status/SUPPLIED_BOUND_EXTERNAL_NUISANCE_PRIOR_SOURCE_RECORDS_WITH_DIGESTS_2026_05_22.md"

OBJECT = "SUPPLIED_BOUND_EXTERNAL_NUISANCE_PRIOR_SOURCE_RECORDS_WITH_DIGESTS"
STATUS = "SUPPLIED_BOUND_RECORD_TARGET_MATERIALIZED_RECORD_PAYLOADS_NOT_SUPPLIED"
NEXT = "REAL_EXTERNAL_NUISANCE_PRIOR_SOURCE_RECORDS_DIGESTS_SCHEMA_PATHS_AND_POLICY_VALUES"

probes = [
    "ACT_DR6",
    "Planck_2018",
    "PantheonPlusSH0ES",
    "DESI_DR2_BAO",
    "DES_Y6",
    "GrowthSector",
    "H0DistanceLadder",
]

record_schema = {
    "required_fields": [
        "probe",
        "nuisance_parameter",
        "external_source_identifier",
        "external_source_locator",
        "source_release_or_version",
        "source_digest_sha256",
        "schema_field_path",
        "prior_family",
        "prior_value_or_distribution",
        "cross_covariance_policy",
        "cross_probe_dependency_scope",
        "compatibility_role",
        "certification_status",
    ],
    "digest_requirement": "sha256_required_or_explicit_missing_digest_blocker",
    "source_binding_requirement": "every nuisance record must bind to an external locator and versioned release",
    "schema_binding_requirement": "every nuisance record must map to a likelihood-input schema path",
    "policy_binding_requirement": "every cross-covariance policy must state its cross-probe dependency scope",
}

data = {
    "object": OBJECT,
    "date": "2026-05-22",
    "status": STATUS,
    "upstream_required_object": "BOUND_EXTERNAL_NUISANCE_PRIOR_SOURCES_AND_COVARIANCE_POLICY_RECORDS",
    "required_next_object": NEXT,
    "purpose": "Materialize the supplied-record target for external nuisance-prior source records with digests.",
    "record_schema": record_schema,
    "required_probe_records": [
        {
            "probe": probe,
            "record_status": "payload_not_supplied",
            "required_payload": [
                "source_identifier",
                "source_locator",
                "release_or_version",
                "sha256_digest",
                "schema_field_path",
                "prior_value_or_distribution",
                "cross_covariance_policy_record",
            ],
        }
        for probe in probes
    ],
    "downstream_chain": [
        "CERTIFIED_SUPPLIED_NUISANCE_RECORDS_COMPATIBLE_WITH_PER_PROBE_TABLE",
        "CERTIFIED_SUPPLIED_NUISANCE_RECORDS_COMPATIBLE_WITH_COVARIANCE_CHAIN_POLICY",
        "CERTIFIED_SUPPLIED_NUISANCE_RECORDS_COMPATIBLE_WITH_MULTIPROBE_LIKELIHOOD_INPUT_MANIFEST",
        "COMPLETE_CERTIFIED_MULTIPROBE_LIKELIHOOD_INPUT_MANIFEST_WITH_REAL_DATA_PATHS",
        "EXECUTED_REAL_MULTIPROBE_PROFILED_LIKELIHOOD_RUN",
        "EXECUTED_REAL_DFM_MKC_VS_LAMBDA_CDM_COMPARISON",
        "OUT_OF_SAMPLE_REJECTION_OR_VALIDATION_CERTIFICATE_IF_SUPPORTED",
    ],
    "blocked_until": [
        "real external source identifiers are supplied",
        "real source locators are supplied",
        "release/version metadata is supplied",
        "SHA-256 digests are supplied or explicit digest blockers are recorded",
        "schema field paths are supplied",
        "cross-covariance policy records are supplied",
        "real multiprobe likelihood data paths are supplied",
    ],
    "does_not_prove": [
        "supplied external nuisance records",
        "certified nuisance prior values",
        "certified cross-covariance policies",
        "complete certified multiprobe manifest",
        "likelihood execution",
        "DFM-MKC versus Lambda-CDM comparison",
        "Lambda-CDM rejection",
        "alternative-model validation",
        "DFM-MKC validation",
        "dark matter resolution",
        "dark energy resolution",
        "empirical validation",
        "any Clay problem",
    ],
}

ARTIFACT.write_text(json.dumps(data, indent=2, sort_keys=True) + "\n")
DOC.write_text(
    f"# {OBJECT}\n\n"
    f"Status: `{STATUS}`\n\n"
    f"Required next object: `{NEXT}`\n\n"
    "This materializes the supplied-record target for external nuisance-prior source records with digests.\n\n"
    "Boundary: no real external nuisance record payloads are supplied by this artifact.\n\n"
    "Does not prove:\n"
    "- supplied external nuisance records\n"
    "- certified nuisance prior values\n"
    "- certified cross-covariance policies\n"
    "- complete certified multiprobe manifest\n"
    "- likelihood execution\n"
    "- DFM-MKC versus Lambda-CDM comparison\n"
    "- Lambda-CDM rejection\n"
    "- alternative-model validation\n"
    "- DFM-MKC validation\n"
    "- dark matter resolution\n"
    "- dark energy resolution\n"
    "- empirical validation\n"
    "- any Clay problem\n",
    encoding="utf-8",
)
print("Supplied bound external nuisance-prior source records with digests artifact written.")
print(f"Status: {STATUS}")
print(f"Required next object: {NEXT}")
