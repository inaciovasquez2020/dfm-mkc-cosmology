from pathlib import Path
import json
import subprocess
import sys

ARTIFACT = Path("artifacts/repo_intake/dfm_mkc_act_dr6_payload_file_presence_inspection_2026_05_21.json")

def test_act_dr6_authentic_payload_inspection_run_verifier_passes():
    result = subprocess.run(
        [sys.executable, "tools/verify_dfm_mkc_act_dr6_payload_file_presence_inspection.py"],
        check=True,
        text=True,
        capture_output=True,
    )
    assert "DFM-MKC ACT DR6 payload file-presence inspection verification OK." in result.stdout
    assert "ACT_DR6_PAYLOAD_FILE_PRESENCE_INSPECTED_NO_SCHEMA_VALIDATION" in result.stdout

def test_payload_digest_and_size_are_recorded():
    data = json.loads(ARTIFACT.read_text())
    payload = data["inspected_payload"]
    path = Path(payload["path"])
    assert path.exists()
    assert path.is_file()
    assert payload["size_bytes"] == path.stat().st_size
    assert isinstance(payload["sha256"], str)
    assert len(payload["sha256"]) == 64

def test_boundary_preserves_no_evidence_and_no_promotion():
    data = json.loads(ARTIFACT.read_text())
    assert "payload file-presence inspection only" in data["boundary"]
    assert "does not extract a numerical data vector" in data["boundary"]
    assert "does not extract a covariance matrix" in data["boundary"]
    assert "does not bind protocol fields to FITS HDUs" in data["boundary"]
    assert "does not execute the likelihood" in data["boundary"]
    assert "does not supply empirical evidence" in data["boundary"]
    assert "does not promote any empirical slot" in data["boundary"]
    assert "DFM-MKC" in data["does_not_prove"]
    assert "Lambda-CDM failure" in data["does_not_prove"]
    assert "any Clay problem" in data["does_not_prove"]
