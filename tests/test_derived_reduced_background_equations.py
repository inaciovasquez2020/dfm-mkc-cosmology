import json
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
BACKGROUND_SPEC = ROOT / "specs" / "DERIVED_REDUCED_BACKGROUND_EQUATIONS.json"
ARTIFACT = ROOT / "artifacts" / "repo_intake" / "derived_reduced_background_equations_2026_05_22.json"

REQUIRED_EQUATION_IDS = {
    "friedmann_constraint",
    "acceleration_equation",
    "scalar_background_equation",
    "vector_background_constraint",
    "matter_background_continuity",
}

def test_verifier_passes():
    result = subprocess.run(
        [sys.executable, "tools/verify_derived_reduced_background_equations.py"],
        cwd=ROOT,
        text=True,
        capture_output=True,
        check=True,
    )
    assert "DERIVED_REDUCED_BACKGROUND_EQUATIONS_SUPPLIED_STRUCTURAL_ONLY_NOT_NUMERICAL" in result.stdout
    assert "PERTURBATION_CLOSURE_EQUATIONS_NOT_SUPPLIED" in result.stdout

def test_background_equations_cover_required_targets():
    data = json.loads(BACKGROUND_SPEC.read_text())
    equations = data["derived_background_equations"]
    assert {item["equation_id"] for item in equations} == REQUIRED_EQUATION_IDS
    assert len(equations) == 5
    for item in equations:
        assert item["status"] == "structural_candidate"
        assert "= 0" in item["structural_equation"]
        assert item["principal_variables"]

def test_background_equations_remain_non_numerical():
    data = json.loads(BACKGROUND_SPEC.read_text())
    assert data["symbolic_derivation_proved"] is False
    assert data["numerical_integration_supplied"] is False
    assert data["perturbation_closure_supplied"] is False
    assert data["parameter_values_supplied"] is False
    assert data["initial_conditions_supplied"] is False
    assert data["empirical_validation_claimed"] is False
    assert data["likelihood_execution_claimed"] is False

def test_artifact_advances_one_execution_input_without_overclaim():
    data = json.loads(ARTIFACT.read_text())
    assert data["root_blocker_partially_reduced"] == "NUMERICAL_COMPARISON_EXECUTION_INPUTS_NOT_SUPPLIED"
    assert data["new_root_blocker"] == "PERTURBATION_CLOSURE_EQUATIONS_NOT_SUPPLIED"
    assert data["check_result"] == "PASS_STRUCTURAL_ONLY"
    boundary = "\n".join(data["boundary"])
    assert "does not prove a full symbolic derivation" in boundary
    assert "does not supply numerical integration" in boundary
    assert "does not supply perturbation closure equations" in boundary
    assert "does not execute a likelihood comparison" in boundary
    assert "does not supply empirical evidence" in boundary
    assert "DFM-MKC" in data["does_not_prove"]
    assert "Lambda-CDM failure" in data["does_not_prove"]
    assert "any Clay problem" in data["does_not_prove"]
