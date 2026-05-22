import json
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
INITIAL_SPEC = ROOT / "specs" / "INITIAL_CONDITIONS.json"
ARTIFACT = ROOT / "artifacts" / "repo_intake" / "initial_conditions_2026_05_22.json"

def test_verifier_passes():
    result = subprocess.run(
        [sys.executable, "tools/verify_initial_conditions.py"],
        cwd=ROOT,
        text=True,
        capture_output=True,
        check=True,
    )
    assert "INITIAL_CONDITIONS_SUPPLIED_REFERENCE_CANDIDATE_ONLY_NOT_CONSTRAINT_SOLVED" in result.stdout
    assert "OBSERVABLE_EVALUATION_GRID_NOT_SUPPLIED" in result.stdout

def test_background_initial_conditions_are_supplied():
    data = json.loads(INITIAL_SPEC.read_text())
    values = {item["symbol"]: item["value"] for item in data["background_initial_conditions"]}
    assert values["N(t_ref)"] > 0
    assert values["a(t_ref)"] > 0
    assert values["rho_m(t_ref)"] >= 0
    assert "H(t_ref)" in values
    assert "phi(t_ref)" in values
    assert "A_0(t_ref)" in values
    assert data["initial_conditions_supplied"] is True

def test_perturbation_initial_conditions_are_supplied():
    data = json.loads(INITIAL_SPEC.read_text())
    symbols = {item["symbol"] for item in data["perturbation_initial_conditions"]}
    assert "Phi(t_ref,q)" in symbols
    assert "Psi_metric(t_ref,q)" in symbols
    assert "delta_phi(t_ref,q)" in symbols
    assert "dot_delta_phi(t_ref,q)" in symbols
    assert "delta_A0(t_ref,q)" in symbols
    assert "delta_A_parallel(t_ref,q)" in symbols
    assert "dot_delta_A_parallel(t_ref,q)" in symbols
    assert "delta_m(t_ref,q)" in symbols
    assert "theta_m(t_ref,q)" in symbols

def test_initial_conditions_are_reference_only_not_constraint_solved():
    data = json.loads(INITIAL_SPEC.read_text())
    assert data["initial_condition_policy"]["reference_candidate_only"] is True
    assert data["initial_condition_policy"]["constraint_solution_claimed"] is False
    assert data["initial_condition_policy"]["fit_to_data"] is False
    assert data["initial_condition_policy"]["physical_calibration_claimed"] is False
    assert data["constraint_solution_claimed"] is False
    assert data["numerical_integration_supplied"] is False
    assert data["empirical_validation_claimed"] is False
    assert data["model_selection_claimed"] is False

def test_artifact_advances_root_blocker_without_overclaim():
    data = json.loads(ARTIFACT.read_text())
    assert data["root_blocker_removed"] == "INITIAL_CONDITIONS_NOT_SUPPLIED"
    assert data["new_root_blocker"] == "OBSERVABLE_EVALUATION_GRID_NOT_SUPPLIED"
    assert data["check_result"] == "PASS_REFERENCE_INITIAL_CONDITIONS_ONLY"
    boundary = "\n".join(data["boundary"])
    assert "does not claim the initial conditions solve the background constraints" in boundary
    assert "does not claim the initial conditions solve perturbation mode constraints" in boundary
    assert "does not supply numerical integration" in boundary
    assert "does not execute a likelihood comparison" in boundary
    assert "does not supply empirical evidence" in boundary
    assert "DFM-MKC" in data["does_not_prove"]
    assert "Lambda-CDM failure" in data["does_not_prove"]
    assert "any Clay problem" in data["does_not_prove"]
