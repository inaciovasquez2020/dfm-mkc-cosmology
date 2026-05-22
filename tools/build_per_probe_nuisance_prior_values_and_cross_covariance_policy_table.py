#!/usr/bin/env python3
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / "artifacts/cosmology/certified_nuisance_prior_table_values_and_covariance_compatibility_rule_2026_05_22.json"
OUT = ROOT / "artifacts/cosmology/per_probe_nuisance_prior_values_and_cross_covariance_policy_table_2026_05_22.json"

PROBES = [
    "ACT_DR6",
    "PANTHEON_PLUS_SHOES",
    "DESI_DR2",
    "PLANCK_2018",
    "DES_Y6",
    "GROWTH_SECTOR",
    "H0_DISTANCE_LADDER",
]

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

    nuisance_rows = [
        {
            "probe": probe,
            "parameter_name": None,
            "prior_family": None,
            "central_value": None,
            "lower_bound": None,
            "upper_bound": None,
            "source_reference": None,
            "value_supplied": False,
            "certified": False,
        }
        for probe in PROBES
    ]

    covariance_rows = [
        {
            "probe_pair": [a, b],
            "shared_parameters": [],
            "cross_covariance_policy": None,
            "independence_assumption_source": None,
            "rule_supplied": False,
            "compatibility_certified": False,
        }
        for i, a in enumerate(PROBES)
        for b in PROBES[i + 1:]
    ]

    nuisance_closed = all(row["certified"] for row in nuisance_rows)
    covariance_closed = all(row["compatibility_certified"] for row in covariance_rows)
    table_closed = nuisance_closed and covariance_closed

    artifact = {
        "object": "PER_PROBE_NUISANCE_PRIOR_VALUES_AND_CROSS_COVARIANCE_POLICY_TABLE",
        "date": "2026-05-22",
        "status": (
            "PER_PROBE_NUISANCE_AND_CROSS_COVARIANCE_TABLE_CERTIFIED"
            if table_closed else
            "TABLE_SURFACE_MATERIALIZED_VALUES_AND_POLICY_NOT_SUPPLIED"
        ),
        "source_object": source["object"],
        "nuisance_prior_rows": nuisance_rows,
        "cross_covariance_policy_rows": covariance_rows,
        "nuisance_prior_values_certified": nuisance_closed,
        "cross_covariance_policy_certified": covariance_closed,
        "table_certified": table_closed,
        "required_next_object": (
            "MULTIPROBE_LIKELIHOOD_INPUT_MANIFEST_WITH_REAL_DATA_PATHS"
            if table_closed else
            "SUPPLIED_PER_PROBE_NUISANCE_PRIOR_VALUES_AND_CROSS_COVARIANCE_POLICY_TABLE"
        ),
        "does_not_prove": DOES_NOT_PROVE,
    }

    OUT.write_text(json.dumps(artifact, indent=2, sort_keys=True) + "\n")
    print("Per-probe nuisance prior values and cross-covariance policy table artifact written.")
    print("Status:", artifact["status"])
    print("Required next object:", artifact["required_next_object"])

if __name__ == "__main__":
    main()
