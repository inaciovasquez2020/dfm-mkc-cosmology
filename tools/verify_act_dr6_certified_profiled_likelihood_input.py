#!/usr/bin/env python3
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
ARTIFACT = ROOT / "artifacts/cosmology/act_dr6_certified_profiled_likelihood_input_2026_05_22.json"

def main():
    data = json.loads(ARTIFACT.read_text())
    assert data["object"] == "ACT_DR6_CERTIFIED_PROFILED_LIKELIHOOD_INPUT"
    assert data["source_object"] == "ACT_DR6_FULL_SACC_SCHEMA_VALIDATION"
    assert data["local_sha256"]
    assert data["preconditions"]["local_payload_exists"] is True
    assert data["preconditions"]["reproducible_download_sha256_matched"] is True
    assert data["preconditions"]["full_sacc_schema_validation_passed"] is True
    assert data["preconditions"]["data_vector_present"] is True
    assert data["preconditions"]["covariance_present"] is True
    assert data["preconditions"]["tracers_present"] is True
    assert data["certified_for_profiled_likelihood_execution"] is True
    assert data["profiled_likelihood_execution_performed"] is False
    assert data["status"] == "ACT_DR6_CERTIFIED_PROFILED_LIKELIHOOD_INPUT_CLOSED_NO_LIKELIHOOD_EXECUTION"
    assert data["required_next_object"] == "PANTHEON_PLUS_SHOES_EXTERNAL_DIGEST_AND_SCHEMA_READER"
    assert "executed multiprobe likelihood run" in data["does_not_prove"]
    assert "complete certified multiprobe likelihood manifest" in data["does_not_prove"]
    assert "Lambda-CDM rejection" in data["does_not_prove"]
    assert "DFM-MKC validation" in data["does_not_prove"]
    assert "any Clay problem" in data["does_not_prove"]
    print("ACT DR6 certified profiled likelihood input verification OK.")
    print("Status:", data["status"])
    print("Required next object:", data["required_next_object"])

if __name__ == "__main__":
    main()
