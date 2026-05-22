import json
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

OBJECTS = [
    "EMPIRICAL_DATA_VALUES",
    "EXECUTABLE_DFM_PREDICTION_VALUES",
    "PAYLOAD_BOUND_COVARIANCE_MATRIX",
    "EXECUTED_LIKELIHOOD_RESULT",
    "REPRODUCIBLE_HOLDOUT_REPORT",
]

def test_verifier_passes():
    result = subprocess.run(
        [sys.executable, "tools/verify_empirical_execution_terminal_chain.py"],
        cwd=ROOT,
        text=True,
        capture_output=True,
        check=True,
    )
    assert "TERMINAL_BLOCKED_NO_EMPIRICAL_PAYLOAD_OR_EXECUTION" in result.stdout
    assert "HOLDOUT_PAYLOAD_AND_EXECUTED_LIKELIHOOD_NOT_SUPPLIED" in result.stdout

def test_all_terminal_objects_exist_and_are_blocked():
    for obj in OBJECTS:
        data = json.loads((ROOT / "specs" / f"{obj}.json").read_text())
        assert data["object_id"] == obj
        assert "BLOCKED" in data["status"]
        assert data["does_not_prove"]
        assert "any Clay problem" in data["does_not_prove"]
        assert data["next_missing_objects"]

def test_no_empirical_or_model_selection_claims_are_made():
    for obj in OBJECTS:
        data = json.loads((ROOT / "specs" / f"{obj}.json").read_text())
        for flag in [
            "empirical_validation_claimed",
            "model_selection_claimed",
            "holdout_survival_claimed",
            "lambda_cdm_failure_claimed",
            "likelihood_executed",
            "empirical_values_supplied",
            "empirical_payload_bound",
            "solver_execution_claimed",
            "executable_prediction_values_supplied",
            "payload_bound_covariance_supplied",
            "empirical_covariance_claimed",
            "reproducible_holdout_report_supplied",
        ]:
            if flag in data:
                assert data[flag] is False

def test_terminal_report_preserves_exact_blocker():
    data = json.loads((ROOT / "artifacts" / "repo_intake" / "reproducible_holdout_report_2026_05_22.json").read_text())
    assert data["terminal_blocker"] == "HOLDOUT_PAYLOAD_AND_EXECUTED_LIKELIHOOD_NOT_SUPPLIED"
    boundary = "\n".join(data["boundary"])
    assert "does not claim holdout survival" in boundary
    assert "does not claim Lambda-CDM failure" in boundary
    assert "does not supply empirical evidence" in boundary
