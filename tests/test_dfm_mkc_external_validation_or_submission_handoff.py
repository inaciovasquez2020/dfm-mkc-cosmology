import json
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
ARTIFACT = ROOT / "artifacts/repo_status/dfm_mkc_external_validation_or_submission_handoff_2026_06_02.json"

def test_external_validation_or_submission_handoff_artifact():
    data = json.loads(ARTIFACT.read_text(encoding="utf-8"))
    assert data["status"] == "EXTERNAL_VALIDATION_OR_SUBMISSION_HANDOFF_READY"
    assert data["input_status"] == "POST_CLOSURE_EXTERNAL_VALIDATION_PACKET_OK"
    assert data["decision"] == "PASS"
    assert data["boundary"] == "HANDOFF_ONLY_NO_EXTERNAL_VALIDATION_CLAIM"
    assert "ExternalIndependentLikelihoodValidation" in data["next_admissible_objects"]
    assert "SubmissionToReviewerOrJournal" in data["next_admissible_objects"]
    assert "completed_external_validation" in data["not_claimed"]

def test_external_validation_request_doc():
    text = (ROOT / "docs/submission/DFM_MKC_EXTERNAL_VALIDATION_REQUEST_2026_06_02.md").read_text(encoding="utf-8")
    assert "Please independently validate the DFM-MKC cosmology repository" in text
    assert "commit hash" in text
    assert "commands run" in text
    assert "reproducibility conclusion" in text

def test_external_validation_or_submission_handoff_verifier_passes():
    result = subprocess.run(
        [sys.executable, "tools/verify_dfm_mkc_external_validation_or_submission_handoff.py"],
        cwd=ROOT,
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        check=False,
    )
    assert result.returncode == 0, result.stdout + result.stderr
    assert "DFM_MKC_EXTERNAL_VALIDATION_OR_SUBMISSION_HANDOFF_OK" in result.stdout
