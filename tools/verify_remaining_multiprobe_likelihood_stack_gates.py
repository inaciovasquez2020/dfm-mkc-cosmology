#!/usr/bin/env python3
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

FILES = {
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

REQUIRED_OBJECTS = {
    "PANTHEON_PLUS_SHOES_EXTERNAL_DIGEST_AND_SCHEMA_READER",
    "DESI_DR2_EXTERNAL_DIGEST_AND_BAO_SCHEMA_READER",
    "PLANCK_2018_EXTERNAL_DIGEST_AND_PARAMETER_SCHEMA_READER",
    "DES_Y6_EXTERNAL_DIGEST_AND_LIKELIHOOD_SCHEMA_READER",
    "GROWTH_SECTOR_EXTERNAL_DIGEST_AND_SCHEMA_READER",
    "H0_DISTANCE_LADDER_EXTERNAL_DIGEST_AND_SCHEMA_READER",
    "NUISANCE_PRIOR_TABLE_CERTIFICATION",
    "COVARIANCE_CHAIN_COMPATIBILITY_CERTIFICATION",
    "COMPLETE_CERTIFIED_MULTIPROBE_LIKELIHOOD_INPUT_MANIFEST",
    "EXECUTED_MULTIPROBE_PROFILED_LIKELIHOOD_RUN",
    "OUT_OF_SAMPLE_MULTIPROBE_LCDM_REJECTION_CERTIFICATE",
}

def load(name):
    return json.loads(FILES[name].read_text())

def main():
    data = {k: load(k) for k in FILES}

    assert {data[k]["object"] for k in data if k != "summary"} == REQUIRED_OBJECTS
    assert data["summary"]["object"] == "REMAINING_MULTIPROBE_LIKELIHOOD_STACK_GATES_2026_05_22"
    assert data["summary"]["status"] == "ALL_REMAINING_GATE_OBJECTS_MATERIALIZED_NO_EMPIRICAL_CLAIM"

    for key in ["pantheon", "desi", "planck", "des_y6", "growth", "h0"]:
        assert "local_path_exists" in data[key]
        assert "local_digest" in data[key]
        assert data[key]["external_digest_supplied"] is False
        assert data[key]["external_digest_matches_local_payload"] is False
        assert data[key]["profiled_likelihood_execution_performed"] is False

    assert data["nuisance"]["certified"] is False
    assert data["covariance"]["certified"] is False
    assert data["manifest"]["complete_manifest_ready"] is False
    assert data["run"]["execution_performed"] is False
    assert data["oos"]["lcdm_rejection_claimed"] is False
    assert data["oos"]["dfm_mkc_validation_claimed"] is False

    for key in data:
        assert "Lambda-CDM rejection" in data[key]["does_not_prove"]
        assert "DFM-MKC validation" in data[key]["does_not_prove"]
        assert "any Clay problem" in data[key]["does_not_prove"]

    print("Remaining multiprobe likelihood stack gates verification OK.")
    print("Status:", data["summary"]["status"])
    print("Required next object:", data["summary"]["required_next_object"])

if __name__ == "__main__":
    main()
