import json
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
COV = ROOT / "specs" / "COVARIANCE_MATRIX.json"
SCHEMA = ROOT / "specs" / "DATA_VECTOR_SCHEMA.json"
ART = ROOT / "artifacts" / "repo_intake" / "covariance_matrix_2026_05_22.json"

def test_verifier_passes():
    result = subprocess.run(
        [sys.executable, "tools/verify_covariance_matrix.py"],
        cwd=ROOT,
        text=True,
        capture_output=True,
        check=True,
    )
    assert "COVARIANCE_MATRIX_SUPPLIED_REFERENCE_DIAGONAL_ONLY_NOT_EMPIRICAL" in result.stdout
    assert "LIKELIHOOD_RULE_NOT_SUPPLIED" in result.stdout

def test_covariance_matches_data_schema_order():
    cov = json.loads(COV.read_text())
    schema = json.loads(SCHEMA.read_text())
    assert cov["covariance_slot_order"] == schema["data_vector_slot_order"]
    assert cov["matrix_dimension"] == len(schema["data_vector_slot_order"])
    assert len(cov["diagonal_variances"]) == cov["matrix_dimension"]
    assert all(v > 0 for v in cov["diagonal_variances"])

def test_covariance_is_reference_only():
    cov = json.loads(COV.read_text())
    assert cov["covariance_matrix_supplied"] is True
    assert cov["matrix_policy"]["reference_diagonal_only"] is True
    assert cov["empirical_covariance_claimed"] is False
    assert cov["likelihood_rule_supplied"] is False
    assert cov["empirical_validation_claimed"] is False

def test_artifact_advances_without_overclaim():
    data = json.loads(ART.read_text())
    assert data["root_blocker_removed"] == "COVARIANCE_MATRIX_NOT_SUPPLIED"
    assert data["new_root_blocker"] == "LIKELIHOOD_RULE_NOT_SUPPLIED"
    boundary = "\n".join(data["boundary"])
    assert "does not supply empirical covariance" in boundary
    assert "does not execute a likelihood comparison" in boundary
    assert "does not supply empirical evidence" in boundary
    assert "any Clay problem" in data["does_not_prove"]
