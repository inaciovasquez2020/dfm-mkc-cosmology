#!/usr/bin/env python3
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
ARTIFACT = ROOT / "artifacts/cosmology/act_dr6_reproducible_download_command_or_external_sha256_digest_2026_05_22.json"

def main():
    data = json.loads(ARTIFACT.read_text())
    assert data["object"] == "ACT_DR6_REPRODUCIBLE_DOWNLOAD_COMMAND_OR_EXTERNAL_SHA256_DIGEST"
    assert data["status"] == "REPRODUCIBLE_DOWNLOAD_COMMAND_BOUND_EXTERNAL_DIGEST_NOT_SUPPLIED_NOT_EXECUTED"
    assert data["source_object"] == "ACT_DR6_EXTERNAL_DIGEST_OR_REPRODUCIBLE_DOWNLOAD_LOCK"
    assert data["official_references"]["act_dr6_data_products"].startswith("https://act.princeton.edu/")
    assert data["official_references"]["dr6_act_lite_repository"].startswith("https://github.com/ACTCollaboration/")
    assert data["local_sha256"]
    assert data["external_sha256_digest"] is None
    assert data["external_sha256_digest_supplied"] is False
    assert data["reproducible_download_command_supplied"] is True
    assert "cobaya-install act_dr6_cmbonly" in data["reproducible_download_commands"]
    assert data["reproducible_download_executed"] is False
    assert data["downloaded_payload_sha256"] is None
    assert data["download_reproduces_local_sha256"] is False
    assert data["act_dr6_certified_for_profiled_likelihood_execution"] is False
    assert "ACT DR6 reproducible download execution" in data["does_not_prove"]
    assert "ACT DR6 downloaded payload hash match" in data["does_not_prove"]
    assert "Lambda-CDM rejection" in data["does_not_prove"]
    assert "DFM-MKC validation" in data["does_not_prove"]
    assert "any Clay problem" in data["does_not_prove"]
    print("ACT DR6 reproducible download command or external sha256 digest verification OK.")
    print("Status:", data["status"])
    print("Required next object:", data["required_next_object"])

if __name__ == "__main__":
    main()
