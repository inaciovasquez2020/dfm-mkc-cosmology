import json
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
ARTIFACT = ROOT / "artifacts/repo_status/dfm_mkc_post_closure_external_validation_packet_2026_06_02.json"

def test_post_closure_external_validation_packet_artifact():
    data = json.loads(ARTIFACT.read_text(encoding="utf-8"))
    assert data["status"] == "POST_CLOSURE_EXTERNAL_VALIDATION_PACKET"
    assert data["repository_surface"] == "CLOSED_REPRODUCIBILITY_SURFACE_ONLY"
    assert data["decision"] == "PASS"
    assert data["boundary"] == "NO_NEW_PHYSICS_CLAIM"
    assert "ExternalIndependentLikelihoodValidation" in data["next_admissible_objects"]
    assert "IdentifiabilityGuaranteeOrDegeneracyTheorem" in data["next_admissible_objects"]

def test_status_files_reconciled():
    next_text = (ROOT / "docs/status/NEXT_CLOSURE_MOVE.md").read_text(encoding="utf-8")
    readiness_text = (ROOT / "docs/REAL_DATA_INTEGRATION_READINESS.md").read_text(encoding="utf-8")
    assert "Canonical Remaining Repository Object" in next_text
    assert "None" in next_text
    assert "## Status" in readiness_text
    assert "Closed" in readiness_text
    assert "final cosmological truth claim" in readiness_text

def test_verifier_passes():
    result = subprocess.run(
        [sys.executable, "tools/verify_dfm_mkc_post_closure_external_validation_packet.py"],
        cwd=ROOT,
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        check=False,
    )
    assert result.returncode == 0, result.stdout + result.stderr
    assert "DFM_MKC_POST_CLOSURE_EXTERNAL_VALIDATION_PACKET_OK" in result.stdout
