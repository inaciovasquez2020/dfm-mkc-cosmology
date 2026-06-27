import json
import subprocess
import sys
from pathlib import Path

ART = Path("artifacts/cosmology/cobaya_runtime_environment_certification_record_2026_05_24.json")
DOC = Path("docs/status/COBAYA_RUNTIME_ENVIRONMENT_CERTIFICATION_RECORD_2026_05_24.md")

def test_cobaya_runtime_environment_record_status():
    data = json.loads(ART.read_text())
    assert data["record_id"] == "COBAYA_RUNTIME_ENVIRONMENT_CERTIFICATION_RECORD_2026_05_24"
    assert data["status"] == "RUNTIME_ENVIRONMENT_CERTIFIED_NO_LIKELIHOOD_EXECUTION"
    for token in ["cobaya", "camb", "numpy", "scipy"]:
        assert token in data["certified_imports"]

def test_cobaya_runtime_environment_record_paths_exist():
    data = json.loads(ART.read_text())
    assert Path(data["pip_freeze_path"]).exists()
    assert Path(data["environment_log_path"]).exists()
    assert len(data["pip_freeze_digest"]) == 64
    assert len(data["environment_log_digest"]) == 64

def test_cobaya_runtime_environment_negative_lock():
    text = DOC.read_text()
    for token in [
        "runtime environment certification only",
        "no DESI DR2 BAO likelihood import smoke test",
        "no likelihood execution",
        "no posterior chains",
        "no best-fit value",
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
        "not evidence for any Clay problem"
    ]:
        assert token in text

def test_cobaya_runtime_environment_verifier_passes():
    out = subprocess.check_output(
        [sys.executable, "tools/verify_cobaya_runtime_environment_certification_record.py"],
        text=True
    )
    assert "COBAYA_RUNTIME_ENVIRONMENT_CERTIFICATION_RECORD_OK" in out
