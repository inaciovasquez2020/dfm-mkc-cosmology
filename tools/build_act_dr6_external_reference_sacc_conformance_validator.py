#!/usr/bin/env python3
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / "artifacts/cosmology/act_dr6_external_release_reference_and_sacc_schema_conformance_rules_2026_05_22.json"
PREV = ROOT / "artifacts/cosmology/act_dr6_public_release_digest_and_full_sacc_schema_reader_2026_05_22.json"
OUT = ROOT / "artifacts/cosmology/act_dr6_external_reference_sacc_conformance_validator_2026_05_22.json"

OFFICIAL_REFERENCES = {
    "act_dr6_data_products": "https://act.princeton.edu/act-dr6-data-products",
    "act_dr6_lite_repository": "https://github.com/ACTCollaboration/DR6-ACT-lite",
}

def main():
    source = json.loads(SOURCE.read_text())
    prev = json.loads(PREV.read_text())
    extnames = set(prev["local_payload"].get("fits_extnames_observed", []))

    checks = {
        "fits_payload_opens": bool(prev["reader"]["executes_on_local_payload"]),
        "required_hdus_present": prev["local_payload"]["fits_hdu_headers_observed"] >= 1,
        "tracers_table_present": any("tracer" in str(x).lower() for x in extnames),
        "data_vector_present": any(str(x).lower() in {"mean", "data", "data_vector"} for x in extnames),
        "covariance_matrix_present": any("cov" in str(x).lower() for x in extnames),
        "metadata_consistent": False,
        "likelihood_reader_maps_payload_to_numeric_arrays": False,
        "external_release_digest_matches_local_payload": False,
    }

    artifact = {
        "object": "ACT_DR6_EXTERNAL_RELEASE_DIGEST_SUPPLIED_AND_SACC_CONFORMANCE_VALIDATOR",
        "date": "2026-05-22",
        "status": "OFFICIAL_REFERENCE_BOUND_VALIDATOR_PARTIAL_DIGEST_NOT_SUPPLIED",
        "source_object": source["object"],
        "input_key": "act_dr6_cmb_lite",
        "official_external_references": OFFICIAL_REFERENCES,
        "local_path": source["local_path"],
        "local_sha256": prev["local_payload"]["sha256"],
        "external_digest": None,
        "external_digest_supplied": False,
        "external_digest_matches_local_payload": False,
        "sacc_conformance_validator": {
            "validator_name": "ACT_DR6_LOCAL_FITS_SACC_CONFORMANCE_PARTIAL_VALIDATOR",
            "checks": checks,
            "checks_passed": sum(1 for v in checks.values() if v is True),
            "checks_total": len(checks),
            "full_sacc_schema_conformance_established": all(checks.values()),
        },
        "certified_for_profiled_likelihood_execution": False,
        "required_next_object": "ACT_DR6_EXTERNAL_DIGEST_OR_REPRODUCIBLE_DOWNLOAD_LOCK",
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
