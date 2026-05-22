#!/usr/bin/env python3
import hashlib
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / "artifacts/cosmology/probe_specific_independent_source_hashes_and_schema_readers_2026_05_22.json"
OUT = ROOT / "artifacts/cosmology/act_dr6_sacc_reader_and_independent_release_hash_validation_2026_05_22.json"

def sha256_file(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()

def fits_header_probe(path: Path):
    if not path.exists() or not path.is_file():
        return {
            "exists": False,
            "fits_magic_present": False,
            "size_bytes": None,
            "local_sha256": None,
        }

    first_block = path.read_bytes()[:2880]
    return {
        "exists": True,
        "fits_magic_present": first_block.startswith(b"SIMPLE"),
        "size_bytes": path.stat().st_size,
        "local_sha256": sha256_file(path),
    }

def main():
    source = json.loads(SOURCE.read_text())
    act = source["reader_targets"]["act_dr6_cmb_lite"]
    rel = act["local_path"]
    path = ROOT / rel
    probe = fits_header_probe(path)

    artifact = {
        "object": "ACT_DR6_SACC_READER_AND_INDEPENDENT_RELEASE_HASH_VALIDATION",
        "date": "2026-05-22",
        "status": "LOCAL_FITS_HEADER_READER_ONLY_NO_INDEPENDENT_RELEASE_HASH",
        "source_object": source["object"],
        "input_key": "act_dr6_cmb_lite",
        "local_path": rel,
        "reader": {
            "name": "LOCAL_FITS_HEADER_PROBE",
            "target_reader": "SACC_FITS_READER",
            "fits_header_observed": probe["fits_magic_present"],
            "executes_on_local_payload": probe["exists"],
            "full_sacc_schema_validation_passed": False,
        },
        "local_payload": probe,
        "independent_release_validation": {
            "required_external_reference": act["required_external_reference"],
            "external_release_url_or_doi": None,
            "external_release_digest": None,
            "independent_hash_match_verified": False,
            "release_provenance_certified": False,
        },
        "certified_for_profiled_likelihood_execution": False,
        "required_next_object": "ACT_DR6_PUBLIC_RELEASE_DIGEST_AND_FULL_SACC_SCHEMA_READER",
        "does_not_prove": [
            "ACT DR6 independent source certification",
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
