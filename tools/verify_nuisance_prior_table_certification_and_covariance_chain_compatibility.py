#!/usr/bin/env python3
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
ARTIFACT = ROOT / "artifacts/cosmology/nuisance_prior_table_certification_and_covariance_chain_compatibility_2026_05_22.json"

VALID_STATUSES = {
    "NUISANCE_PRIOR_AND_COVARIANCE_CHAIN_COMPATIBILITY_CERTIFIED",
    "COMBINED_GATE_MATERIALIZED_CERTIFICATION_NOT_CLOSED",
}

def main():
    data = json.loads(ARTIFACT.read_text())
    assert data["object"] == "NUISANCE_PRIOR_TABLE_CERTIFICATION_AND_COVARIANCE_CHAIN_COMPATIBILITY"
    assert data["status"] in VALID_STATUSES
    assert "NUISANCE_PRIOR_TABLE_CERTIFICATION" in data["source_objects"]
    assert "COVARIANCE_CHAIN_COMPATIBILITY_CERTIFICATION" in data["source_objects"]
    assert isinstance(data["nuisance_prior_table_certified"], bool)
    assert isinstance(data["covariance_chain_compatibility_certified"], bool)
    assert data["combined_certification_closed"] == (
        data["nuisance_prior_table_certified"] and data["covariance_chain_compatibility_certified"]
    )
    assert isinstance(data["missing_certifications"], list)
    assert "complete certified multiprobe likelihood manifest" in data["does_not_prove"]
    assert "executed multiprobe likelihood run" in data["does_not_prove"]
    assert "Lambda-CDM rejection" in data["does_not_prove"]
    assert "DFM-MKC validation" in data["does_not_prove"]
    assert "any Clay problem" in data["does_not_prove"]
    print("Nuisance prior table and covariance-chain compatibility verification OK.")
    print("Status:", data["status"])
    print("Required next object:", data["required_next_object"])

if __name__ == "__main__":
    main()
