#!/usr/bin/env python3
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
ARTIFACT = ROOT / "artifacts/cosmology/act_dr6_reproducible_download_execution_and_local_sha256_comparison_2026_05_22.json"

VALID_STATUSES = {
    "REPRODUCIBLE_DOWNLOAD_EXECUTED_LOCAL_SHA256_MATCHED",
    "REPRODUCIBLE_DOWNLOAD_EXECUTED_LOCAL_SHA256_NOT_MATCHED",
    "REPRODUCIBLE_DOWNLOAD_EXECUTION_FAILED_OR_NO_PAYLOAD_FOUND",
    "DOWNLOAD_EXECUTION_ATTEMPTED_NOT_CERTIFIED",
}

def main():
    data = json.loads(ARTIFACT.read_text())
    assert data["object"] == "ACT_DR6_REPRODUCIBLE_DOWNLOAD_EXECUTION_AND_LOCAL_SHA256_COMPARISON"
    assert data["status"] in VALID_STATUSES
    assert data["source_object"] == "ACT_DR6_REPRODUCIBLE_DOWNLOAD_COMMAND_OR_EXTERNAL_SHA256_DIGEST"
    assert data["local_sha256"]
    assert data["execution_attempted"] is True
    assert isinstance(data["downloaded_payloads"], list)
    assert isinstance(data["matching_payloads"], list)
    assert isinstance(data["download_reproduces_local_sha256"], bool)
    assert isinstance(data["executed_steps"], list)
    assert len(data["executed_steps"]) >= 1
    assert data["certified_for_profiled_likelihood_execution"] is False
    assert "ACT DR6 full SACC schema certification" in data["does_not_prove"]
    assert "Lambda-CDM rejection" in data["does_not_prove"]
    assert "DFM-MKC validation" in data["does_not_prove"]
    assert "any Clay problem" in data["does_not_prove"]
    print("ACT DR6 reproducible download execution and local sha256 comparison verification OK.")
    print("Status:", data["status"])
    print("Required next object:", data["required_next_object"])

if __name__ == "__main__":
    main()
