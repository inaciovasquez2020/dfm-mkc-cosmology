import json
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SPEC = ROOT / "specs" / "SUPPLIED_DFM_FIELD_EQUATIONS_AND_ACTION_FUNCTIONAL.json"
ARTIFACT = ROOT / "artifacts" / "repo_intake" / "filled_supplied_dfm_field_equations_and_action_functional_2026_05_22.json"

def test_verifier_passes():
    result = subprocess.run(
        [sys.executable, "tools/verify_filled_supplied_dfm_field_equations_and_action_functional.py"],
        cwd=ROOT,
        text=True,
        capture_output=True,
        check=True,
    )
    assert "FILLED_STRUCTURAL_CANDIDATE_ONLY_NOT_VALIDATED" in result.stdout
    assert "VARIATIONAL_DERIVATION_CHECK_NOT_SUPPLIED" in result.stdout

def test_spec_supplies_action_and_equations_without_claiming_validation():
    data = json.loads(SPEC.read_text())
    assert data["object_id"] == "FILLED_SUPPLIED_DFM_FIELD_EQUATIONS_AND_ACTION_FUNCTIONAL"
    assert data["status"] == "FILLED_STRUCTURAL_CANDIDATE_ONLY_NOT_VALIDATED"
    assert data["mathematical_closure_claimed"] is False
    assert data["empirical_validation_claimed"] is False
    assert data["prediction_vector_claimed"] is False
    assert data["likelihood_execution_claimed"] is False
    assert "S[g,phi,A,Psi]" in data["action_functional"]["definition"]
    assert "metric_equation" in data["field_equations"]
    assert "scalar_equation" in data["field_equations"]
    assert "vector_equation" in data["field_equations"]

def test_artifact_boundary_preserves_no_overclaim():
    data = json.loads(ARTIFACT.read_text())
    boundary = "\n".join(data["boundary"])
    assert "does not verify the variational derivation" in boundary
    assert "does not validate physical correctness" in boundary
    assert "does not supply a frozen prediction vector" in boundary
    assert "does not execute a likelihood comparison" in boundary
    assert "does not supply empirical evidence" in boundary
    assert "DFM-MKC" in data["does_not_prove"]
    assert "Lambda-CDM failure" in data["does_not_prove"]
    assert "any Clay problem" in data["does_not_prove"]

def test_next_root_blocker_is_variational_derivation_check():
    data = json.loads(ARTIFACT.read_text())
    assert data["root_blocker_removed"] == "SUPPLIED_DFM_FIELD_EQUATIONS_AND_ACTION_FUNCTIONAL_NOT_FILLED"
    assert data["new_root_blocker"] == "VARIATIONAL_DERIVATION_CHECK_NOT_SUPPLIED"
    assert "VARIATIONAL_DERIVATION_CHECK" in data["next_missing_objects"]
