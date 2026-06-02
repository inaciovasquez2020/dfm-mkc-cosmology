import json
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
ARTIFACT = ROOT / "artifacts/repo_status/dfm_mkc_external_validation_dispatch_selection_target_2026_06_02.json"

def test_dispatch_selection_target_artifact():
    data = json.loads(ARTIFACT.read_text(encoding="utf-8"))
    assert data["status"] == "DISPATCH_SELECTION_TARGET_OPEN"
    assert data["missing_input"] == "external_validator_recipient_or_submission_venue"
    assert data["decision"] == "PASS"
    assert data["boundary"] == "TARGET_ONLY_NO_DISPATCH_CLAIM"
    assert "ExternalValidatorRecipient" in data["weakest_sufficient_next_inputs"]
    assert "SubmissionVenue" in data["weakest_sufficient_next_inputs"]

def test_dispatch_selection_template():
    text = (ROOT / "docs/submission/DFM_MKC_DISPATCH_SELECTION_TEMPLATE_2026_06_02.md").read_text(encoding="utf-8")
    assert "DISPATCH_ROUTE=external_validator" in text
    assert "DISPATCH_ROUTE=submission_venue" in text
    assert "DISPATCH_ROUTE=reviewer_or_advisor" in text
    assert "RECIPIENT_EMAIL=" in text
    assert "VENUE_URL=" in text

def test_dispatch_selection_verifier_passes():
    result = subprocess.run(
        [sys.executable, "tools/verify_dfm_mkc_external_validation_dispatch_selection_target.py"],
        cwd=ROOT,
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        check=False,
    )
    assert result.returncode == 0, result.stdout + result.stderr
    assert "DFM_MKC_EXTERNAL_VALIDATION_DISPATCH_SELECTION_TARGET_OK" in result.stdout
