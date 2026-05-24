#!/usr/bin/env python3
import hashlib
import importlib.util
import json
from pathlib import Path

ART = Path("artifacts/cosmology/cobaya_runtime_environment_certification_record_2026_05_24.json")
DOC = Path("docs/status/COBAYA_RUNTIME_ENVIRONMENT_CERTIFICATION_RECORD_2026_05_24.md")

REQUIRED_FIELDS = [
    "python_executable",
    "python_version",
    "platform",
    "cobaya_version",
    "camb_version",
    "numpy_version",
    "scipy_version",
    "pip_freeze_path",
    "pip_freeze_digest",
    "environment_log_path",
    "environment_log_digest"
]

REQUIRED_IMPORTS = [
    "cobaya",
    "camb",
    "numpy",
    "scipy"
]

REQUIRED_LOCK = [
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
]

REQUIRED_BOUNDARY = [
    "does not import the DESI DR2 BAO likelihood",
    "does not execute Lambda-CDM",
    "does not execute DFM-MKC",
    "does not produce posterior chains",
    "does not produce a best-fit value",
    "does not compute delta_chi2",
    "does not compute AICc",
    "does not compute BICc",
    "does not compare Lambda-CDM against DFM-MKC",
    "does not reject Lambda-CDM",
    "does not validate DFM-MKC",
    "does not provide Chronos proof input",
    "does not prove R1/R2/R3",
    "NON_FACTORISATION",
    "Chronos-RR",
    "H4.1/FGL",
    "P vs NP",
    "Clay problem"
]

def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()

def main() -> None:
    data = json.loads(ART.read_text())
    doc = DOC.read_text()

    assert data["record_id"] == "COBAYA_RUNTIME_ENVIRONMENT_CERTIFICATION_RECORD_2026_05_24"
    assert data["status"] == "RUNTIME_ENVIRONMENT_CERTIFIED_NO_LIKELIHOOD_EXECUTION"

    for field in REQUIRED_FIELDS:
        assert field in data, field
        assert data[field] not in ("", None), field
        assert field in doc, field

    for module in REQUIRED_IMPORTS:
        assert module in data["certified_imports"], module
        assert importlib.util.find_spec(module) is not None, module
        assert module in doc, module

    pip_path = Path(data["pip_freeze_path"])
    env_path = Path(data["environment_log_path"])
    assert pip_path.exists(), str(pip_path)
    assert env_path.exists(), str(env_path)
    assert sha256(pip_path) == data["pip_freeze_digest"]
    assert sha256(env_path) == data["environment_log_digest"]

    for token in REQUIRED_LOCK:
        assert token in data["negative_use_lock"], token
        assert token in doc, token

    for token in REQUIRED_BOUNDARY:
        assert token in doc, token

    print("COBAYA_RUNTIME_ENVIRONMENT_CERTIFICATION_RECORD_OK")

if __name__ == "__main__":
    main()
