#!/usr/bin/env python3
import hashlib
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / "artifacts/cosmology/file_level_multiprobe_input_digest_and_provenance_manifest_2026_05_22.json"
OUT = ROOT / "artifacts/cosmology/certified_file_level_multiprobe_likelihood_inputs_2026_05_22.json"

LIKELIHOOD_ROLES = {
    "act_dr6_cmb_lite": "cmb_lite_sacc_likelihood_input_candidate",
    "pantheon_plus_shoes": "supernova_distance_ladder_input_candidate",
    "desi_dr2": "bao_expansion_history_input_candidate",
    "planck_baseline": "cmb_baseline_parameter_anchor_candidate",
    "des_y6": "growth_lensing_holdout_input_candidate",
    "growth_sector_holdout": "growth_sector_holdout_summary_candidate",
    "h0_distance_ladder": "local_distance_ladder_systematics_candidate",
}

REQUIRED_CERTIFICATION_FIELDS = [
    "exists",
    "sha256_or_tree_sha256",
    "source_provenance_status",
    "format_validation_status",
    "likelihood_role",
    "independent_source_hash_verified",
    "schema_or_likelihood_reader_verified",
    "certified_for_profiled_likelihood_execution",
]

def sha256_file(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()

def sha256_tree(path: Path) -> str:
    h = hashlib.sha256()
    files = sorted(p for p in path.rglob("*") if p.is_file())
    for p in files:
        rel = p.relative_to(path).as_posix().encode()
        h.update(rel)
        h.update(b"\0")
        h.update(str(p.stat().st_size).encode())
        h.update(b"\0")
        h.update(sha256_file(p).encode())
        h.update(b"\0")
    return h.hexdigest()

def digest_entry(rel: str):
    if not rel:
        return None
    path = ROOT / rel
    if not path.exists():
        return None
    if path.is_file():
        return sha256_file(path)
    if path.is_dir():
        return sha256_tree(path)
    return None

def main():
    source = json.loads(SOURCE.read_text())
    entries = {}

    for key, src in source["input_entries"].items():
        rel = src["path"]
        exists = bool(src["exists"]) and (ROOT / rel).exists()
        digest = digest_entry(rel) if exists else None
        entries[key] = {
            "path": rel,
            "exists": exists,
            "sha256_or_tree_sha256": digest,
            "source_provenance_status": "LOCAL_CANDIDATE_ONLY_NOT_INDEPENDENTLY_CERTIFIED",
            "format_validation_status": "OBSERVED_PATH_ONLY_SCHEMA_NOT_CERTIFIED",
            "likelihood_role": LIKELIHOOD_ROLES.get(key, "unassigned"),
            "independent_source_hash_verified": False,
            "schema_or_likelihood_reader_verified": False,
            "certified_for_profiled_likelihood_execution": False,
        }

    certified_count = sum(
        1 for entry in entries.values()
        if entry["certified_for_profiled_likelihood_execution"] is True
    )

    artifact = {
        "object": "CERTIFIED_FILE_LEVEL_MULTIPROBE_LIKELIHOOD_INPUTS",
        "date": "2026-05-22",
        "status": "CERTIFICATION_GATE_ONLY_NO_INPUT_CERTIFIED",
        "source_object": source["object"],
        "required_certification_fields": REQUIRED_CERTIFICATION_FIELDS,
        "inputs": entries,
        "summary": {
            "total_inputs": len(entries),
            "inputs_with_existing_local_paths": sum(1 for e in entries.values() if e["exists"]),
            "inputs_with_digest": sum(1 for e in entries.values() if e["sha256_or_tree_sha256"]),
            "certified_inputs": certified_count,
            "ready_for_executed_multiprobe_profiled_likelihood_run": certified_count == len(entries) and len(entries) > 0,
        },
        "remaining_missing_certifications": [
            "independent source hash verification for every input",
            "schema or likelihood-reader validation for every input",
            "nuisance prior table certification",
            "covariance or chain compatibility certification",
            "profiled likelihood execution harness binding"
        ],
        "required_next_object": "INDEPENDENT_SOURCE_HASH_AND_SCHEMA_VALIDATION_FOR_EACH_MULTIPROBE_INPUT",
        "does_not_prove": [
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
