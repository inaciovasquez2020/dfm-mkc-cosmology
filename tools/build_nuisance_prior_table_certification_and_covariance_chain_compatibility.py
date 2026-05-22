#!/usr/bin/env python3
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
NUISANCE = ROOT / "artifacts/cosmology/nuisance_prior_table_certification_2026_05_22.json"
COVARIANCE = ROOT / "artifacts/cosmology/covariance_chain_compatibility_certification_2026_05_22.json"
MANIFEST = ROOT / "artifacts/cosmology/complete_certified_multiprobe_likelihood_input_manifest_2026_05_22.json"
OUT = ROOT / "artifacts/cosmology/nuisance_prior_table_certification_and_covariance_chain_compatibility_2026_05_22.json"

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

def load(path: Path):
    return json.loads(path.read_text())

def main():
    nuisance = load(NUISANCE)
    covariance = load(COVARIANCE)
    manifest = load(MANIFEST)

    nuisance_certified = bool(nuisance.get("certified"))
    covariance_certified = bool(covariance.get("certified"))
    combined_certified = nuisance_certified and covariance_certified

    artifact = {
        "object": "NUISANCE_PRIOR_TABLE_CERTIFICATION_AND_COVARIANCE_CHAIN_COMPATIBILITY",
        "date": "2026-05-22",
        "status": (
            "NUISANCE_PRIOR_AND_COVARIANCE_CHAIN_COMPATIBILITY_CERTIFIED"
            if combined_certified else
            "COMBINED_GATE_MATERIALIZED_CERTIFICATION_NOT_CLOSED"
        ),
        "source_objects": [
            nuisance["object"],
            covariance["object"],
            manifest["object"],
        ],
        "nuisance_prior_table_certified": nuisance_certified,
        "covariance_chain_compatibility_certified": covariance_certified,
        "combined_certification_closed": combined_certified,
        "complete_manifest_ready_before_this_object": bool(manifest.get("complete_manifest_ready")),
        "required_inputs": {
            "nuisance_prior_table": nuisance.get("required_inputs", []),
            "covariance_chain_compatibility": covariance.get("required_inputs", []),
        },
        "missing_certifications": [
            "per-probe nuisance prior table values",
            "shared parameter compatibility map",
            "cross-probe covariance compatibility rule",
            "profiled likelihood nuisance-handling rule",
            "manifest promotion rule from certified nuisance and covariance gates",
        ],
        "required_next_object": (
            "MULTIPROBE_LIKELIHOOD_INPUT_MANIFEST_WITH_REAL_DATA_PATHS"
            if combined_certified else
            "CERTIFIED_NUISANCE_PRIOR_TABLE_VALUES_AND_COVARIANCE_COMPATIBILITY_RULE"
        ),
        "does_not_prove": DOES_NOT_PROVE,
    }

    OUT.write_text(json.dumps(artifact, indent=2, sort_keys=True) + "\n")
    print("Nuisance prior table and covariance-chain compatibility gate verification artifact written.")
    print("Status:", artifact["status"])
    print("Required next object:", artifact["required_next_object"])

if __name__ == "__main__":
    main()
