import json
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
VALID = ROOT / "specs" / "INDEPENDENT_EMPIRICAL_VALIDATION.json"
ART = ROOT / "artifacts" / "repo_intake" / "independent_empirical_validation_2026_05_22.json"

def test_verifier_passes():
    result = subprocess.run(
        [sys.executable, "tools/verify_independent_empirical_validation.py"],
        cwd=ROOT,
        text=True,
        capture_output=True,
        check=True,
    )
    assert "INDEPENDENT_EMPIRICAL_VALIDATION_BLOCKED_NO_EMPIRICAL_PAYLOAD_OR_EXECUTION" in result.stdout
    assert "EMPIRICAL_PAYLOAD_AND_EXECUTED_LIKELIHOOD_NOT_SUPPLIED" in result.stdout

def test_validation_is_blocked_not_claimed():
    data = json.loads(VALID.read_text())
    assert data["independent_empirical_validation_supplied"] is False
    assert data["empirical_payload_bound"] is False
    assert data["likelihood_executed"] is False
    assert data["holdout_survival_claimed"] is False
    assert data["lambda_cdm_failure_claimed"] is False
    assert data["model_selection_claimed"] is False

def test_artifact_preserves_terminal_blocker():
    data = json.loads(ART.read_text())
    assert data["root_blocker_preserved"] == "INDEPENDENT_EMPIRICAL_VALIDATION_NOT_SUPPLIED"
    assert data["terminal_blocker"] == "EMPIRICAL_PAYLOAD_AND_EXECUTED_LIKELIHOOD_NOT_SUPPLIED"
    boundary = "\n".join(data["boundary"])
    assert "does not claim Lambda-CDM failure" in boundary
    assert "does not supply empirical evidence" in boundary
    assert "any Clay problem" in data["does_not_prove"]
