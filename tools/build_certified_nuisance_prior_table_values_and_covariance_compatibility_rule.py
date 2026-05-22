#!/usr/bin/env python3
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / "artifacts/cosmology/nuisance_prior_table_certification_and_covariance_chain_compatibility_2026_05_22.json"
OUT = ROOT / "artifacts/cosmology/certified_nuisance_prior_table_values_and_covariance_compatibility_rule_2026_05_22.json"

PROBES = [
    "ACT_DR6",
    "PANTHEON_PLUS_SHOES",
    "DESI_DR2",
    "PLANCK_2018",
    "DES_Y6",
    "GROWTH_SECTOR",
    "H0_DISTANCE_LADDER",
]

REQUIRED_NUISANCE_FIELDS = [
    "parameter_name",
    "probe",
    "prior_family",
    "central_value",
    "lower_bound",
    "upper_bound",
    "source_reference",
    "certified",
]

REQUIRED_COVARIANCE_RULE_FIELDS = [
    "probe_pair",
    "shared_parameters",
    "cross_covariance_policy",
    "independence_assumption_source",
    "compatibility_certified",
]

DOES_NOT_PROVE = [
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

    nuisance_slots = {
        probe: {
            "required_fields": REQUIRED_NUISANCE_FIELDS,
            "values_supplied": False,
            "certified": False,
        }
        for probe in PROBES
    }

    covariance_slots = {
        f"{a}__{b}": {
            "required_fields": REQUIRED_COVARIANCE_RULE_FIELDS,
            "rule_supplied": False,
            "compatibility_certified": False,
        }
        for i, a in enumerate(PROBES)
        for b in PROBES[i + 1:]
    }

    nuisance_closed = all(v["certified"] for v in nuisance_slots.values())
    covariance_closed = all(v["compatibility_certified"] for v in covariance_slots.values())
    combined_closed = nuisance_closed and covariance_closed

    artifact = {
        "object": "CERTIFIED_NUISANCE_PRIOR_TABLE_VALUES_AND_COVARIANCE_COMPATIBILITY_RULE",
        "date": "2026-05-22",
        "status": (
            "CERTIFIED_NUISANCE_AND_COVARIANCE_COMPATIBILITY_RULE_CLOSED"
            if combined_closed else
            "RULE_SURFACE_MATERIALIZED_VALUES_AND_COMPATIBILITY_NOT_CERTIFIED"
        ),
        "source_object": source["object"],
        "nuisance_prior_slots": nuisance_slots,
        "covariance_compatibility_slots": covariance_slots,
        "nuisance_prior_values_certified": nuisance_closed,
        "covariance_compatibility_rule_certified": covariance_closed,
        "combined_certification_closed": combined_closed,
        "required_next_object": (
            "MULTIPROBE_LIKELIHOOD_INPUT_MANIFEST_WITH_REAL_DATA_PATHS"
            if combined_closed else
            "PER_PROBE_NUISANCE_PRIOR_VALUES_AND_CROSS_COVARIANCE_POLICY_TABLE"
        ),
        "does_not_prove": DOES_NOT_PROVE,
    }

    OUT.write_text(json.dumps(artifact, indent=2, sort_keys=True) + "\n")
    print("Certified nuisance prior values and covariance compatibility rule artifact written.")
    print("Status:", artifact["status"])
    print("Required next object:", artifact["required_next_object"])

if __name__ == "__main__":
    main()
