#!/usr/bin/env python3
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
ARTIFACT = ROOT / "artifacts/cosmology/act_dr6_full_sacc_schema_validation_2026_05_22.json"

VALID_STATUSES = {
    "FULL_SACC_SCHEMA_VALIDATION_PASSED_NOT_LIKELIHOOD_EXECUTION",
    "FULL_SACC_SCHEMA_VALIDATION_BLOCKED_OR_PARTIAL",
}

REQUIRED_CHECKS = {
    "local_payload_exists",
    "reproducible_download_sha256_matched",
    "sacc_module_importable",
    "sacc_load_fits_available",
    "sacc_payload_loads",
    "data_vector_present",
    "covariance_present",
    "tracers_present",
}

def main():
    data = json.loads(ARTIFACT.read_text())
    assert data["object"] == "ACT_DR6_FULL_SACC_SCHEMA_VALIDATION"
    assert data["status"] in VALID_STATUSES
    assert data["source_object"] == "ACT_DR6_REPRODUCIBLE_DOWNLOAD_EXECUTION_AND_LOCAL_SHA256_COMPARISON"
    assert data["local_sha256"]
    assert set(data["checks"]) == REQUIRED_CHECKS
    assert data["checks"]["local_payload_exists"] is True
    assert data["checks"]["reproducible_download_sha256_matched"] is True
    assert isinstance(data["full_sacc_schema_validation_passed"], bool)
    assert data["certified_for_profiled_likelihood_execution"] == data["full_sacc_schema_validation_passed"]
    if data["full_sacc_schema_validation_passed"]:
        assert data["status"] == "FULL_SACC_SCHEMA_VALIDATION_PASSED_NOT_LIKELIHOOD_EXECUTION"
        assert data["required_next_object"] == "ACT_DR6_CERTIFIED_PROFILED_LIKELIHOOD_INPUT"
    else:
        assert data["status"] == "FULL_SACC_SCHEMA_VALIDATION_BLOCKED_OR_PARTIAL"
        assert data["required_next_object"] == "INSTALL_SACC_READER_OR_REPAIR_ACT_DR6_SACC_SCHEMA_LOAD"
    assert "executed multiprobe likelihood run" in data["does_not_prove"]
    assert "Lambda-CDM rejection" in data["does_not_prove"]
    assert "DFM-MKC validation" in data["does_not_prove"]
    assert "any Clay problem" in data["does_not_prove"]
    print("ACT DR6 full SACC schema validation verification OK.")
    print("Status:", data["status"])
    print("Required next object:", data["required_next_object"])

if __name__ == "__main__":
    main()
