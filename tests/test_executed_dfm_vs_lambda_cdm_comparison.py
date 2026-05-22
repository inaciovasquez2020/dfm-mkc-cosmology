import json
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
COMPARISON_SPEC = ROOT / "specs" / "EXECUTED_DFM_VS_LAMBDA_CDM_COMPARISON.json"
ARTIFACT = ROOT / "artifacts" / "repo_intake" / "executed_dfm_vs_lambda_cdm_comparison_2026_05_22.json"

REQUIRED_PRECONDITIONS = {
    "DERIVED_REDUCED_BACKGROUND_EQUATIONS",
    "PERTURBATION_CLOSURE_EQUATIONS",
    "NUMERICAL_PARAMETER_VECTOR",
    "INITIAL_CONDITIONS",
    "OBSERVABLE_EVALUATION_GRID",
    "DATA_VECTOR_SCHEMA",
    "COVARIANCE_MATRIX",
    "LIKELIHOOD_RULE",
    "LAMBDA_CDM_BASELINE_VECTOR",
}

def test_verifier_passes():
    result = subprocess.run(
        [sys.executable, "tools/verify_executed_dfm_vs_lambda_cdm_comparison.py"],
        cwd=ROOT,
        text=True,
        capture_output=True,
        check=True,
    )
    assert "EXECUTION_BLOCKED_SYMBOLIC_VECTOR_ONLY_NO_NUMERICAL_COMPARISON" in result.stdout
    assert "NUMERICAL_COMPARISON_EXECUTION_INPUTS_NOT_SUPPLIED" in result.stdout

def test_comparison_is_explicitly_blocked_not_executed():
    data = json.loads(COMPARISON_SPEC.read_text())
    assert data["object_id"] == "EXECUTED_DFM_VS_LAMBDA_CDM_COMPARISON"
    assert data["status"] == "EXECUTION_BLOCKED_SYMBOLIC_VECTOR_ONLY_NO_NUMERICAL_COMPARISON"
    assert data["check_result"] == "BLOCKED_REQUIRED_INPUTS_NOT_SUPPLIED"
    assert data["comparison_executed"] is False
    assert data["numerical_predictions_evaluated"] is False
    assert data["empirical_validation_claimed"] is False
    assert data["model_selection_claimed"] is False

def test_execution_preconditions_are_all_missing():
    data = json.loads(COMPARISON_SPEC.read_text())
    preconditions = data["execution_preconditions"]
    names = {item["object"] for item in preconditions}
    assert names == REQUIRED_PRECONDITIONS
    for item in preconditions:
        assert item["status"] == "missing"
        assert item["required_for"]

def test_artifact_preserves_blocker_without_overclaim():
    data = json.loads(ARTIFACT.read_text())
    assert data["root_blocker_preserved"] == "EXECUTED_DFM_VS_LAMBDA_CDM_COMPARISON_NOT_SUPPLIED"
    assert data["new_root_blocker"] == "NUMERICAL_COMPARISON_EXECUTION_INPUTS_NOT_SUPPLIED"
    assert data["check_result"] == "BLOCKED_REQUIRED_INPUTS_NOT_SUPPLIED"
    boundary = "\n".join(data["boundary"])
    assert "does not execute a numerical comparison" in boundary
    assert "does not evaluate numerical predictions" in boundary
    assert "does not supply a covariance matrix" in boundary
    assert "does not supply a likelihood rule" in boundary
    assert "does not supply empirical evidence" in boundary
    assert "DFM-MKC" in data["does_not_prove"]
    assert "Lambda-CDM failure" in data["does_not_prove"]
    assert "any Clay problem" in data["does_not_prove"]
