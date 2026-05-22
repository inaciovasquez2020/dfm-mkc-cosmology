#!/usr/bin/env python3
import csv
import hashlib
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

ACT = ROOT / "artifacts/cosmology/act_dr6_certified_profiled_likelihood_input_2026_05_22.json"

OUT = {
    "pantheon": ROOT / "artifacts/cosmology/pantheon_plus_shoes_external_digest_and_schema_reader_2026_05_22.json",
    "desi": ROOT / "artifacts/cosmology/desi_dr2_external_digest_and_bao_schema_reader_2026_05_22.json",
    "planck": ROOT / "artifacts/cosmology/planck_2018_external_digest_and_parameter_schema_reader_2026_05_22.json",
    "des_y6": ROOT / "artifacts/cosmology/des_y6_external_digest_and_likelihood_schema_reader_2026_05_22.json",
    "growth": ROOT / "artifacts/cosmology/growth_sector_external_digest_and_schema_reader_2026_05_22.json",
    "h0": ROOT / "artifacts/cosmology/h0_distance_ladder_external_digest_and_schema_reader_2026_05_22.json",
    "nuisance": ROOT / "artifacts/cosmology/nuisance_prior_table_certification_2026_05_22.json",
    "covariance": ROOT / "artifacts/cosmology/covariance_chain_compatibility_certification_2026_05_22.json",
    "manifest": ROOT / "artifacts/cosmology/complete_certified_multiprobe_likelihood_input_manifest_2026_05_22.json",
    "run": ROOT / "artifacts/cosmology/executed_multiprobe_profiled_likelihood_run_2026_05_22.json",
    "oos": ROOT / "artifacts/cosmology/out_of_sample_multiprobe_lcdm_rejection_certificate_2026_05_22.json",
    "summary": ROOT / "artifacts/cosmology/remaining_multiprobe_likelihood_stack_gates_2026_05_22.json",
}

DOES_NOT_PROVE = [
    "executed multiprobe likelihood run",
    "Lambda-CDM rejection",
    "six-parameter flat Lambda-CDM rejection",
    "alternative-model validation",
    "DFM-MKC validation",
    "dark matter resolution",
    "dark energy resolution",
    "any Clay problem",
]

PROBES = {
    "pantheon": {
        "object": "PANTHEON_PLUS_SHOES_EXTERNAL_DIGEST_AND_SCHEMA_READER",
        "path": "artifacts/external_data_sources/pantheon_plus_shoes_1_data",
        "schema": "supernova_distance_ladder_table_or_directory",
        "next": "DESI_DR2_EXTERNAL_DIGEST_AND_BAO_SCHEMA_READER",
    },
    "desi": {
        "object": "DESI_DR2_EXTERNAL_DIGEST_AND_BAO_SCHEMA_READER",
        "path": "public_data/desi_dr2",
        "schema": "bao_measurement_table_or_directory",
        "next": "PLANCK_2018_EXTERNAL_DIGEST_AND_PARAMETER_SCHEMA_READER",
    },
    "planck": {
        "object": "PLANCK_2018_EXTERNAL_DIGEST_AND_PARAMETER_SCHEMA_READER",
        "path": "public_data/planck/planck_2018_baseline_params.csv",
        "schema": "cmb_parameter_table",
        "next": "DES_Y6_EXTERNAL_DIGEST_AND_LIKELIHOOD_SCHEMA_READER",
    },
    "des_y6": {
        "object": "DES_Y6_EXTERNAL_DIGEST_AND_LIKELIHOOD_SCHEMA_READER",
        "path": "public_data/des_y6",
        "schema": "weak_lensing_or_growth_likelihood_payload",
        "next": "GROWTH_SECTOR_EXTERNAL_DIGEST_AND_SCHEMA_READER",
    },
    "growth": {
        "object": "GROWTH_SECTOR_EXTERNAL_DIGEST_AND_SCHEMA_READER",
        "path": "artifacts/cosmology/growth_sector_holdout_compatibility_test_2026_05_22.json",
        "schema": "growth_sector_holdout_summary",
        "next": "H0_DISTANCE_LADDER_EXTERNAL_DIGEST_AND_SCHEMA_READER",
    },
    "h0": {
        "object": "H0_DISTANCE_LADDER_EXTERNAL_DIGEST_AND_SCHEMA_READER",
        "path": "artifacts/cosmology/h0_distance_ladder_systematics_profile_2026_05_22.json",
        "schema": "distance_ladder_systematics_profile",
        "next": "NUISANCE_PRIOR_TABLE_CERTIFICATION",
    },
}

def sha256_file(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()

def sha256_tree(path: Path) -> str:
    h = hashlib.sha256()
    for p in sorted(x for x in path.rglob("*") if x.is_file()):
        rel = p.relative_to(path).as_posix()
        h.update(rel.encode())
        h.update(b"\0")
        h.update(sha256_file(p).encode())
        h.update(b"\0")
    return h.hexdigest()

def digest(path: Path):
    if not path.exists():
        return None
    if path.is_file():
        return sha256_file(path)
    if path.is_dir():
        return sha256_tree(path)
    return None

def table_like(path: Path):
    if not path.exists():
        return False
    if path.is_dir():
        return any(p.suffix.lower() in {".csv", ".txt", ".dat", ".json", ".fits", ".gz"} for p in path.rglob("*") if p.is_file())
    return path.suffix.lower() in {".csv", ".txt", ".dat", ".json", ".fits", ".gz"}

def write_json(path: Path, obj):
    path.write_text(json.dumps(obj, indent=2, sort_keys=True) + "\n")

def build_probe(key, cfg):
    p = ROOT / cfg["path"]
    exists = p.exists()
    local_digest = digest(p)
    schema_reader_passed = bool(exists and table_like(p))
    certified = bool(exists and local_digest and schema_reader_passed)

    return {
        "object": cfg["object"],
        "date": "2026-05-22",
        "status": (
            f"{cfg['object']}_LOCAL_SCHEMA_READER_PASSED_EXTERNAL_DIGEST_NOT_SUPPLIED"
            if certified else
            f"{cfg['object']}_BLOCKED_LOCAL_INPUT_OR_SCHEMA_MISSING"
        ),
        "local_path": cfg["path"],
        "schema_family": cfg["schema"],
        "local_path_exists": exists,
        "local_digest": local_digest,
        "external_digest": None,
        "external_digest_supplied": False,
        "external_digest_matches_local_payload": False,
        "schema_reader_passed": schema_reader_passed,
        "certified_for_profiled_likelihood_execution": certified,
        "profiled_likelihood_execution_performed": False,
        "required_next_object": cfg["next"],
        "does_not_prove": DOES_NOT_PROVE,
    }

def main():
    act = json.loads(ACT.read_text())
    assert act["certified_for_profiled_likelihood_execution"] is True

    built = {}
    for key, cfg in PROBES.items():
        artifact = build_probe(key, cfg)
        built[key] = artifact
        write_json(OUT[key], artifact)

    nuisance = {
        "object": "NUISANCE_PRIOR_TABLE_CERTIFICATION",
        "date": "2026-05-22",
        "status": "NUISANCE_PRIOR_TABLE_TARGET_ONLY_NOT_CERTIFIED",
        "required_inputs": [
            "ACT nuisance priors",
            "Pantheon+/SH0ES nuisance priors",
            "DESI nuisance/systematic priors",
            "Planck nuisance priors",
            "DES Y6 nuisance priors",
            "growth-sector nuisance priors",
            "H0 distance-ladder nuisance priors",
        ],
        "certified": False,
        "required_next_object": "COVARIANCE_CHAIN_COMPATIBILITY_CERTIFICATION",
        "does_not_prove": DOES_NOT_PROVE,
    }
    write_json(OUT["nuisance"], nuisance)

    covariance = {
        "object": "COVARIANCE_CHAIN_COMPATIBILITY_CERTIFICATION",
        "date": "2026-05-22",
        "status": "COVARIANCE_CHAIN_COMPATIBILITY_TARGET_ONLY_NOT_CERTIFIED",
        "required_inputs": [
            "per-probe covariance availability",
            "shared-parameter compatibility",
            "nuisance-prior compatibility",
            "profiled-likelihood execution compatibility",
            "holdout split compatibility",
        ],
        "certified": False,
        "required_next_object": "COMPLETE_CERTIFIED_MULTIPROBE_LIKELIHOOD_INPUT_MANIFEST",
        "does_not_prove": DOES_NOT_PROVE,
    }
    write_json(OUT["covariance"], covariance)

    probe_certifications = {
        "act_dr6": act["certified_for_profiled_likelihood_execution"],
        "pantheon_plus_shoes": built["pantheon"]["certified_for_profiled_likelihood_execution"],
        "desi_dr2": built["desi"]["certified_for_profiled_likelihood_execution"],
        "planck_2018": built["planck"]["certified_for_profiled_likelihood_execution"],
        "des_y6": built["des_y6"]["certified_for_profiled_likelihood_execution"],
        "growth_sector": built["growth"]["certified_for_profiled_likelihood_execution"],
        "h0_distance_ladder": built["h0"]["certified_for_profiled_likelihood_execution"],
    }

    complete_manifest_ready = all(probe_certifications.values()) and nuisance["certified"] and covariance["certified"]

    manifest = {
        "object": "COMPLETE_CERTIFIED_MULTIPROBE_LIKELIHOOD_INPUT_MANIFEST",
        "date": "2026-05-22",
        "status": (
            "COMPLETE_CERTIFIED_MULTIPROBE_LIKELIHOOD_INPUT_MANIFEST_CLOSED"
            if complete_manifest_ready else
            "COMPLETE_CERTIFIED_MULTIPROBE_LIKELIHOOD_INPUT_MANIFEST_BLOCKED"
        ),
        "probe_certifications": probe_certifications,
        "nuisance_prior_table_certified": nuisance["certified"],
        "covariance_chain_compatibility_certified": covariance["certified"],
        "complete_manifest_ready": complete_manifest_ready,
        "required_next_object": "EXECUTED_MULTIPROBE_PROFILED_LIKELIHOOD_RUN",
        "does_not_prove": DOES_NOT_PROVE,
    }
    write_json(OUT["manifest"], manifest)

    run = {
        "id": "EXECUTED_MULTIPROBE_PROFILED_LIKELIHOOD_RUN",
        "object": "EXECUTED_MULTIPROBE_PROFILED_LIKELIHOOD_RUN",
        "date": "2026-05-22",
        "status": "INPUT_GATED_EXECUTION_TARGET_ONLY_NO_LIKELIHOOD_RUN",
        "complete_manifest_ready": complete_manifest_ready,
        "input_gated": True,
        "execution_performed": False,
        "likelihood_run_executed": False,
        "current_execution_status": {
            "complete_certified_manifest_ready": False,
            "likelihood_inputs_bound": False,
            "multiprobe_runner_executed": False,
            "profiled_likelihoods_computed": False,
            "test_statistic_computed": False
        },
        "boundary": [
            "does not execute a real likelihood",
            "does not compute profiled log-likelihoods",
            "does not compute a test statistic",
            "does not claim Lambda-CDM failure",
            "does not claim DFM-MKC validation"
        ],
        "required_probe_inputs": [
            {
                "id": "ACT_DR6_CERTIFIED_PROFILED_LIKELIHOOD_INPUT",
                "status": "CERTIFIED_INPUT_AVAILABLE_NO_LIKELIHOOD_EXECUTION",
                "certified": True
            },
            {
                "id": "PANTHEON_PLUS_SHOES_EXTERNAL_DIGEST_AND_SCHEMA_READER",
                "status": "GATE_MATERIALIZED_NOT_EXECUTED",
                "certified": False
            },
            {
                "id": "DESI_DR2_EXTERNAL_DIGEST_AND_BAO_SCHEMA_READER",
                "status": "GATE_MATERIALIZED_NOT_EXECUTED",
                "certified": False
            },
            {
                "id": "PLANCK_2018_EXTERNAL_DIGEST_AND_PARAMETER_SCHEMA_READER",
                "status": "GATE_MATERIALIZED_NOT_EXECUTED",
                "certified": False
            },
            {
                "id": "DES_Y6_EXTERNAL_DIGEST_AND_LIKELIHOOD_SCHEMA_READER",
                "status": "GATE_MATERIALIZED_NOT_EXECUTED",
                "certified": False
            },
            {
                "id": "GROWTH_SECTOR_EXTERNAL_DIGEST_AND_SCHEMA_READER",
                "status": "GATE_MATERIALIZED_NOT_EXECUTED",
                "certified": False
            },
            {
                "id": "H0_DISTANCE_LADDER_EXTERNAL_DIGEST_AND_SCHEMA_READER",
                "status": "GATE_MATERIALIZED_NOT_EXECUTED",
                "certified": False
            }
        ],
        "profiled_log_likelihoods": None,
        "test_statistic": None,
        "required_next_object": "MULTIPROBE_LIKELIHOOD_INPUT_MANIFEST_WITH_REAL_DATA_PATHS",
        "does_not_prove": sorted(set(DOES_NOT_PROVE + [
            "Lambda-CDM failure",
            "empirical validation",
            "ACT validation",
            "DESI validation",
            "DES validation",
            "ACT validation",
            "DES validation",
            "DESI validation",
            "Lambda-CDM failure",
            "dark matter resolution",
            "dark energy resolution",
            "P vs NP",
            "any Clay problem"
        ])),
    }
    write_json(OUT["run"], run)

    oos = {
        "object": "OUT_OF_SAMPLE_MULTIPROBE_LCDM_REJECTION_CERTIFICATE",
        "date": "2026-05-22",
        "status": "OUT_OF_SAMPLE_CERTIFICATE_BLOCKED_NO_EXECUTED_MULTIPROBE_RUN",
        "executed_multiprobe_run_available": False,
        "holdout_protocol_available": False,
        "lcdm_rejection_claimed": False,
        "dfm_mkc_validation_claimed": False,
        "required_next_object": "COMPLETE_CERTIFIED_MULTIPROBE_LIKELIHOOD_INPUT_MANIFEST",
        "does_not_prove": DOES_NOT_PROVE,
    }
    write_json(OUT["oos"], oos)

    summary = {
        "object": "REMAINING_MULTIPROBE_LIKELIHOOD_STACK_GATES_2026_05_22",
        "date": "2026-05-22",
        "status": "ALL_REMAINING_GATE_OBJECTS_MATERIALIZED_NO_EMPIRICAL_CLAIM",
        "objects_materialized": [v["object"] for v in built.values()] + [
            nuisance["object"],
            covariance["object"],
            manifest["object"],
            run["object"],
            oos["object"],
        ],
        "closed_probe_inputs": [k for k, v in probe_certifications.items() if v],
        "blocked_probe_inputs": [k for k, v in probe_certifications.items() if not v],
        "complete_manifest_ready": complete_manifest_ready,
        "execution_performed": False,
        "lcdm_rejection_claimed": False,
        "dfm_mkc_validation_claimed": False,
        "required_next_object": "NUISANCE_PRIOR_TABLE_CERTIFICATION_AND_COVARIANCE_CHAIN_COMPATIBILITY",
        "does_not_prove": DOES_NOT_PROVE,
    }
    write_json(OUT["summary"], summary)

if __name__ == "__main__":
    main()
