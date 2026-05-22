import json
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

OBJECTS = [
    "AUTHENTIC_EXTERNAL_DATA_PAYLOAD",
    "PAYLOAD_SLOT_BINDING_MAP",
    "PAYLOAD_DIGEST_LOCK",
    "EMPIRICAL_VALUE_ARRAY",
    "EMPIRICAL_UNCERTAINTY_ARRAY",
    "BACKGROUND_NUMERICAL_SOLVER_RUN",
    "PERTURBATION_NUMERICAL_SOLVER_RUN",
    "TRANSFER_FUNCTION_SOLVER_RUN",
    "PREDICTION_VALUE_ARRAY",
    "PREDICTION_RUN_DIGEST_LOCK",
    "PAYLOAD_COVARIANCE_ARRAY",
    "PAYLOAD_COVARIANCE_SLOT_ORDER",
    "PAYLOAD_COVARIANCE_DIGEST_LOCK",
    "PAYLOAD_COVARIANCE_POSITIVE_DEFINITE_CHECK",
    "DFM_CHI_SQUARE_VALUE",
    "LAMBDA_CDM_CHI_SQUARE_VALUE",
    "DELTA_CHI_SQUARE_VALUE",
    "EXECUTED_LIKELIHOOD_DIGEST_LOCK",
    "HOLDOUT_PAYLOAD_DIGEST_LOCK",
    "REPRODUCTION_COMMANDS",
    "REPRODUCTION_LOG",
    "CLAIM_BOUNDARY_AUDIT",
]

def test_verifier_passes():
    result = subprocess.run(
        [sys.executable, "tools/verify_remaining_empirical_payload_blocker_chain.py"],
        cwd=ROOT,
        text=True,
        capture_output=True,
        check=True,
    )
    assert "TERMINAL_NO_EMPIRICAL_PAYLOAD_EXECUTION_OR_VALIDATION" in result.stdout
    assert "CLAIM_BOUNDARY_AUDIT_SUPPLIED_TERMINAL_NO_EMPIRICAL_CLAIM" in result.stdout

def test_all_remaining_objects_exist():
    for obj in OBJECTS:
        spec = json.loads((ROOT / "specs" / f"{obj}.json").read_text())
        assert spec["object_id"] == obj
        assert spec["status"]
        assert spec["check_result"]
        assert spec["blocking_missing_objects"]
        assert "any Clay problem" in spec["does_not_prove"]

def test_all_remaining_artifacts_exist_with_boundaries():
    for obj in OBJECTS:
        artifact = json.loads((ROOT / "artifacts" / "repo_intake" / f"{obj.lower()}_2026_05_22.json").read_text())
        assert artifact["required_object_blocked"] == obj
        assert artifact["terminal_blocker"]
        assert artifact["boundary"]
        assert "any Clay problem" in artifact["does_not_prove"]

def test_terminal_audit_preserves_no_claims():
    audit = json.loads((ROOT / "specs" / "CLAIM_BOUNDARY_AUDIT.json").read_text())
    assert audit["status"] == "CLAIM_BOUNDARY_AUDIT_SUPPLIED_TERMINAL_NO_EMPIRICAL_CLAIM"
    assert audit["dfm_mkc_validated_claimed"] is False
    assert audit["lambda_cdm_failure_claimed"] is False
    assert audit["holdout_survival_claimed"] is False
    assert audit["empirical_validation_claimed"] is False
    assert audit["model_selection_claimed"] is False
    assert audit["nobel_level_discovery_claimed"] is False
