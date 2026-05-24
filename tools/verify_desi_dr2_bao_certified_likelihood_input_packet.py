#!/usr/bin/env python3
import hashlib
import json
import subprocess
from pathlib import Path

ROOT = Path.cwd()

def ensure_external_source(data: dict) -> None:
    source_root = ROOT / data["local_source_root"]
    repo_root = ROOT / "external_data/desi_dr2_bao/bao_data"
    if source_root.exists():
        return
    repo_root.parent.mkdir(parents=True, exist_ok=True)
    if repo_root.exists():
        return
    subprocess.check_call([
        "git",
        "clone",
        "--depth",
        "1",
        "--branch",
        data["release_version"],
        data["source_url"] + ".git",
        str(repo_root),
    ])
ART = ROOT / "artifacts/cosmology/desi_dr2_bao_certified_likelihood_input_packet_2026_05_24.json"
DOC = ROOT / "docs/status/DESI_DR2_BAO_CERTIFIED_LIKELIHOOD_INPUT_PACKET_2026_05_24.md"

REQUIRED_STATUS = "DIGEST_CERTIFIED_INPUT_PACKET_ONLY_NO_LIKELIHOOD_EXECUTION"

REQUIRED_NEGATIVE_LOCK = [
    "digest-certified input packet only",
    "no likelihood execution",
    "no posterior chains",
    "no Lambda-CDM rejection",
    "no DFM-MKC validation",
    "not Chronos proof input",
    "not evidence for R1",
    "not evidence for R2",
    "not evidence for R3",
    "not evidence for NON_FACTORISATION",
    "not evidence for Chronos-RR",
    "not evidence for H4.1/FGL",
    "not evidence for P vs NP",
    "not evidence for any Clay problem",
]

REQUIRED_PENDING = [
    "Cobaya environment version",
    "CAMB or CLASS backend version",
    "exact ΛCDM YAML",
    "exact DFM-MKC YAML",
    "likelihood execution",
    "posterior chains",
    "delta_chi2",
    "AICc",
    "BICc",
    "posterior_predictive_distribution_p",
]

REQUIRED_BOUNDARY = [
    "does not run Cobaya",
    "does not certify a Python environment",
    "does not certify CAMB or CLASS",
    "does not define the DFM-MKC likelihood",
    "does not execute ΛCDM",
    "does not execute DFM-MKC",
    "does not compare ΛCDM against DFM-MKC",
    "does not reject Lambda-CDM",
    "does not validate DFM-MKC",
    "does not provide Chronos proof input",
    "does not prove R1/R2/R3",
    "NON_FACTORISATION",
    "Chronos-RR",
    "H4.1/FGL",
    "P vs NP",
    "Clay problem",
]

def main() -> None:
    data = json.loads(ART.read_text())
    doc = DOC.read_text()

    assert data["record_id"] == "DESI_DR2_BAO_CERTIFIED_EXTERNAL_COSMOLOGY_LIKELIHOOD_INPUT_PACKET_2026_05_24"
    assert data["status"] == REQUIRED_STATUS
    assert data["dataset_id"] == "DESI_DR2_BAO"
    assert data["source_url"] == "https://github.com/CobayaSampler/bao_data"
    assert data["source_subdir"] == "desi_bao_dr2"
    assert data["release_version"] == "v2.6"
    assert len(data["source_commit_sha"]) == 40
    assert data["file_count"] == len(data["file_manifest"])
    assert data["file_count"] > 0

    ensure_external_source(data)

    roles = {entry["role"] for entry in data["file_manifest"]}
    assert "covariance" in roles
    assert "data_vector_or_likelihood_table" in roles

    for entry in data["file_manifest"]:
        p = ROOT / entry["path"]
        assert p.exists(), entry["path"]
        assert p.is_file(), entry["path"]
        assert hashlib.sha256(p.read_bytes()).hexdigest() == entry["sha256"], entry["path"]
        assert p.stat().st_size == entry["size_bytes"], entry["path"]

    for token in REQUIRED_NEGATIVE_LOCK:
        assert token in data["negative_use_lock"], token
        assert token in doc, token

    for token in REQUIRED_PENDING:
        assert token in data["pending_fields"], token
        assert token in doc, token

    for token in REQUIRED_BOUNDARY:
        assert token in doc, token

    print("DESI_DR2_BAO_CERTIFIED_LIKELIHOOD_INPUT_PACKET_OK")

if __name__ == "__main__":
    main()
