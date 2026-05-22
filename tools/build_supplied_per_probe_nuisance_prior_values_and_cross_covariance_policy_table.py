#!/usr/bin/env python3
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / "artifacts/cosmology/per_probe_nuisance_prior_values_and_cross_covariance_policy_table_2026_05_22.json"
OUT = ROOT / "artifacts/cosmology/supplied_per_probe_nuisance_prior_values_and_cross_covariance_policy_table_2026_05_22.json"

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

    supplied_nuisance_rows = []
    for row in source["nuisance_prior_rows"]:
        supplied_nuisance_rows.append({
            **row,
            "supplied_value_record": None,
            "external_source_bound": False,
            "schema_validated": False,
            "value_supplied": False,
            "certified": False,
        })

    supplied_covariance_rows = []
    for row in source["cross_covariance_policy_rows"]:
        supplied_covariance_rows.append({
            **row,
            "supplied_policy_record": None,
            "external_source_bound": False,
            "schema_validated": False,
            "rule_supplied": False,
            "compatibility_certified": False,
        })

    nuisance_closed = all(row["certified"] for row in supplied_nuisance_rows)
    covariance_closed = all(row["compatibility_certified"] for row in supplied_covariance_rows)
    table_closed = nuisance_closed and covariance_closed

    artifact = {
        "object": "SUPPLIED_PER_PROBE_NUISANCE_PRIOR_VALUES_AND_CROSS_COVARIANCE_POLICY_TABLE",
        "date": "2026-05-22",
        "status": (
            "SUPPLIED_PER_PROBE_NUISANCE_AND_CROSS_COVARIANCE_TABLE_CERTIFIED"
            if table_closed else
            "SUPPLIED_TABLE_TARGET_MATERIALIZED_VALUES_AND_POLICIES_NOT_SUPPLIED"
        ),
        "source_object": source["object"],
        "nuisance_prior_rows": supplied_nuisance_rows,
        "cross_covariance_policy_rows": supplied_covariance_rows,
        "nuisance_prior_values_supplied": any(row["value_supplied"] for row in supplied_nuisance_rows),
        "cross_covariance_policies_supplied": any(row["rule_supplied"] for row in supplied_covariance_rows),
        "nuisance_prior_values_certified": nuisance_closed,
        "cross_covariance_policy_certified": covariance_closed,
        "table_certified": table_closed,
        "required_next_object": (
            "MULTIPROBE_LIKELIHOOD_INPUT_MANIFEST_WITH_REAL_DATA_PATHS"
            if table_closed else
            "EXTERNAL_NUISANCE_PRIOR_SOURCE_TABLE_AND_CROSS_COVARIANCE_POLICY_VALUES"
        ),
        "does_not_prove": DOES_NOT_PROVE,
    }

    OUT.write_text(json.dumps(artifact, indent=2, sort_keys=True) + "\n")
    print("Supplied per-probe nuisance prior values and cross-covariance policy table artifact written.")
    print("Status:", artifact["status"])
    print("Required next object:", artifact["required_next_object"])

if __name__ == "__main__":
    main()
