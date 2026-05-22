import json
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
LIKE = ROOT / "specs" / "LIKELIHOOD_RULE.json"
ART = ROOT / "artifacts" / "repo_intake" / "likelihood_rule_2026_05_22.json"

def test_verifier_passes():
    result = subprocess.run(
        [sys.executable, "tools/verify_likelihood_rule.py"],
        cwd=ROOT,
        text=True,
        capture_output=True,
        check=True,
    )
    assert "LIKELIHOOD_RULE_SUPPLIED_FORMAL_ONLY_NOT_EXECUTED" in result.stdout
    assert "LAMBDA_CDM_BASELINE_VECTOR_NOT_SUPPLIED" in result.stdout

def test_formal_rule_supplied_not_executed():
    data = json.loads(LIKE.read_text())
    assert data["likelihood_rule_supplied"] is True
    assert data["likelihood_executed"] is False
    assert data["empirical_values_supplied"] is False
    assert data["lambda_cdm_baseline_supplied"] is False
    assert "chi_square" in data["rule"]
    assert "log_likelihood" in data["rule"]

def test_artifact_advances_without_overclaim():
    data = json.loads(ART.read_text())
    assert data["root_blocker_removed"] == "LIKELIHOOD_RULE_NOT_SUPPLIED"
    assert data["new_root_blocker"] == "LAMBDA_CDM_BASELINE_VECTOR_NOT_SUPPLIED"
    boundary = "\n".join(data["boundary"])
    assert "does not execute the likelihood rule" in boundary
    assert "does not supply empirical evidence" in boundary
    assert "any Clay problem" in data["does_not_prove"]
