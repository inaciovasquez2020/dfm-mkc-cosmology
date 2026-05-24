import json
import subprocess
from pathlib import Path

ART = Path("artifacts/cosmology/desi_dr2_bao_certified_likelihood_input_packet_2026_05_24.json")
DOC = Path("docs/status/DESI_DR2_BAO_CERTIFIED_LIKELIHOOD_INPUT_PACKET_2026_05_24.md")

def test_desi_dr2_bao_packet_status():
    data = json.loads(ART.read_text())
    assert data["status"] == "DIGEST_CERTIFIED_INPUT_PACKET_ONLY_NO_LIKELIHOOD_EXECUTION"
    assert data["dataset_id"] == "DESI_DR2_BAO"
    assert data["source_subdir"] == "desi_bao_dr2"
    assert data["release_version"] == "v2.6"
    assert len(data["source_commit_sha"]) == 40

def test_desi_dr2_bao_packet_has_files_and_roles():
    data = json.loads(ART.read_text())
    assert data["file_count"] == len(data["file_manifest"])
    assert data["file_count"] > 0
    roles = {entry["role"] for entry in data["file_manifest"]}
    assert "covariance" in roles
    assert "data_vector_or_likelihood_table" in roles

def test_desi_dr2_bao_packet_pending_fields():
    data = json.loads(ART.read_text())
    for token in [
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
    ]:
        assert token in data["pending_fields"]

def test_desi_dr2_bao_packet_negative_lock():
    text = DOC.read_text()
    for token in [
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
    ]:
        assert token in text

def test_desi_dr2_bao_packet_verifier_passes():
    out = subprocess.check_output(
        ["python3", "tools/verify_desi_dr2_bao_certified_likelihood_input_packet.py"],
        text=True,
    )
    assert "DESI_DR2_BAO_CERTIFIED_LIKELIHOOD_INPUT_PACKET_OK" in out
