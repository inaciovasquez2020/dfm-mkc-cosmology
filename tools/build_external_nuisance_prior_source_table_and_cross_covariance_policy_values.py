#!/usr/bin/env python3
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / "artifacts/cosmology/supplied_per_probe_nuisance_prior_values_and_cross_covariance_policy_table_2026_05_22.json"
OUT = ROOT / "artifacts/cosmology/external_nuisance_prior_source_table_and_cross_covariance_policy_values_2026_05_22.json"

DOES_NOT_PROVE = [
    "certified nuisance prior values",
    "certified cross-covariance compatibility",
    "complete certified multiprobe likelihood manifest",
    "executed multiprobe likelihood run",
    "Lambda-CDM rejection",
    "six-parameter flat Lambda-CDM rejection",
    "Lambda-CDM failure",
    "alternative-model validation",
    "DFM-MKC validation",
    "dark matter resolution",
    "dark energy resolution",
    "P vs NP",
    "any Clay problem",
]

def main():
    source = json.loads(SOURCE.read_text())

    external_nuisance_source_rows = []
    for row in source["nuisance_prior_rows"]:
        external_nuisance_source_rows.append({
            "probe": row["probe"],
            "parameter_name": row.get("parameter_name"),
            "external_source_reference": None,
            "external_source_digest": None,
            "source_bound": False,
            "value_record_supplied": False,
            "schema_validated": False,
            "certified": False,
        })

    external_covariance_policy_rows = []
    for row in source["cross_covariance_policy_rows"]:
        external_covariance_policy_rows.append({
            "probe_pair": row["probe_pair"],
            "external_source_reference": None,
            "external_source_digest": None,
            "source_bound": False,
            "policy_record_supplied": False,
            "schema_validated": False,
            "compatibility_certified": False,
        })

    nuisance_sources_bound = all(row["source_bound"] for row in external_nuisance_source_rows)
    covariance_sources_bound = all(row["source_bound"] for row in external_covariance_policy_rows)
    nuisance_values_supplied = all(row["value_record_supplied"] for row in external_nuisance_source_rows)
    covariance_policies_supplied = all(row["policy_record_supplied"] for row in external_covariance_policy_rows)
    combined_closed = (
        nuisance_sources_bound
        and covariance_sources_bound
        and nuisance_values_supplied
        and covariance_policies_supplied
        and all(row["certified"] for row in external_nuisance_source_rows)
        and all(row["compatibility_certified"] for row in external_covariance_policy_rows)
    )

    artifact = {
        "object": "EXTERNAL_NUISANCE_PRIOR_SOURCE_TABLE_AND_CROSS_COVARIANCE_POLICY_VALUES",
        "date": "2026-05-22",
        "status": (
            "EXTERNAL_NUISANCE_AND_CROSS_COVARIANCE_VALUES_CERTIFIED"
            if combined_closed else
            "EXTERNAL_SOURCE_VALUE_TABLE_TARGET_MATERIALIZED_VALUES_NOT_SUPPLIED"
        ),
        "source_object": source["object"],
        "external_nuisance_source_rows": external_nuisance_source_rows,
        "external_cross_covariance_policy_rows": external_covariance_policy_rows,
        "nuisance_sources_bound": nuisance_sources_bound,
        "covariance_sources_bound": covariance_sources_bound,
        "nuisance_values_supplied": nuisance_values_supplied,
        "covariance_policies_supplied": covariance_policies_supplied,
        "combined_certification_closed": combined_closed,
        "required_next_object": (
            "MULTIPROBE_LIKELIHOOD_INPUT_MANIFEST_WITH_REAL_DATA_PATHS"
            if combined_closed else
            "BOUND_EXTERNAL_NUISANCE_PRIOR_SOURCES_AND_COVARIANCE_POLICY_RECORDS"
        ),
        "does_not_prove": DOES_NOT_PROVE,
    }

    OUT.write_text(json.dumps(artifact, indent=2, sort_keys=True) + "\n")
    print("External nuisance prior source table and cross-covariance policy values artifact written.")
    print("Status:", artifact["status"])
    print("Required next object:", artifact["required_next_object"])

if __name__ == "__main__":
    main()
