#!/usr/bin/env python3
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
ARTIFACT = ROOT / "artifacts/cosmology/bound_external_nuisance_prior_sources_and_covariance_policy_records_2026_05_22.json"
DOC = ROOT / "docs/status/BOUND_EXTERNAL_NUISANCE_PRIOR_SOURCES_AND_COVARIANCE_POLICY_RECORDS_2026_05_22.md"

OBJECT = "BOUND_EXTERNAL_NUISANCE_PRIOR_SOURCES_AND_COVARIANCE_POLICY_RECORDS"
STATUS = "BOUND_SOURCE_RECORD_TARGET_MATERIALIZED_RECORDS_NOT_BOUND"
NEXT = "SUPPLIED_BOUND_EXTERNAL_NUISANCE_PRIOR_SOURCE_RECORDS_WITH_DIGESTS"

data = {
    "object": OBJECT,
    "date": "2026-05-22",
    "status": STATUS,
    "upstream_required_object": "EXTERNAL_NUISANCE_PRIOR_SOURCE_TABLE_AND_CROSS_COVARIANCE_POLICY_VALUES",
    "required_next_object": NEXT,
    "purpose": (
        "Materialize the target requiring every external nuisance-prior source and "
        "cross-covariance policy record to be bound to explicit source identifiers, "
        "schema locations, digest records, and compatibility roles before certification."
    ),
    "required_bound_record_fields": [
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
    "probe_record_targets": [
        {
            "probe": "ACT_DR6",
            "required_record_role": "CMB nuisance prior and covariance-policy source binding",
            "record_status": "target_only_record_not_supplied",
        },
        {
            "probe": "Planck_2018",
            "required_record_role": "CMB legacy nuisance prior and covariance-policy source binding",
            "record_status": "target_only_record_not_supplied",
        },
        {
            "probe": "PantheonPlusSH0ES",
            "required_record_role": "supernova nuisance prior and covariance-policy source binding",
            "record_status": "target_only_record_not_supplied",
        },
        {
            "probe": "DESI_DR2_BAO",
            "required_record_role": "BAO nuisance prior and covariance-policy source binding",
            "record_status": "target_only_record_not_supplied",
        },
        {
            "probe": "DES_Y6",
            "required_record_role": "weak-lensing nuisance prior and covariance-policy source binding",
            "record_status": "target_only_record_not_supplied",
        },
        {
            "probe": "GrowthSector",
            "required_record_role": "growth-sector nuisance prior and covariance-policy source binding",
            "record_status": "target_only_record_not_supplied",
        },
        {
            "probe": "H0DistanceLadder",
            "required_record_role": "distance-ladder nuisance prior and covariance-policy source binding",
            "record_status": "target_only_record_not_supplied",
        },
    ],
    "binding_checks_required": [
        "every nuisance prior value must point to an external source identifier",
        "every external source identifier must have a reproducible locator",
        "every locator must have a source release or version tag",
        "every source record must have a SHA-256 digest or explicit missing-digest blocker",
        "every nuisance parameter must map to a schema field path",
        "every cross-covariance policy must state its cross-probe dependency scope",
        "every record must declare whether it is certified, target-only, or blocked",
    ],
    "blocked_until": [
        "external nuisance source records are supplied",
        "source locators are bound to concrete release/version metadata",
        "source digests are supplied or explicitly marked unavailable",
        "schema field paths are mapped to the multiprobe likelihood input manifest",
        "cross-probe covariance policies are linked to concrete nuisance records",
    ],
    "does_not_prove": [
        "certified nuisance prior values",
        "certified cross-covariance policies",
        "complete certified multiprobe manifest",
        "likelihood execution",
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
    "This materializes the binding target for external nuisance-prior source records "
    "and cross-covariance policy records.\n\n"
    "Boundary: this is a target surface only. It does not supply, certify, or validate "
    "the external nuisance values or cross-covariance policies.\n\n"
    "Does not prove:\n"
    "- certified nuisance prior values\n"
    "- certified cross-covariance policies\n"
    "- complete certified multiprobe manifest\n"
    "- likelihood execution\n"
    "- Lambda-CDM rejection\n"
    "- alternative-model validation\n"
    "- DFM-MKC validation\n"
    "- dark matter resolution\n"
    "- dark energy resolution\n"
    "- empirical validation\n"
    "- any Clay problem\n",
    encoding="utf-8",
)

print("Bound external nuisance-prior source and covariance-policy records artifact written.")
print(f"Status: {STATUS}")
print(f"Required next object: {NEXT}")
