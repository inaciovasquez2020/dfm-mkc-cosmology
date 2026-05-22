import json
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PERTURBATION_SPEC = ROOT / "specs" / "PERTURBATION_CLOSURE_EQUATIONS.json"
ARTIFACT = ROOT / "artifacts" / "repo_intake" / "perturbation_closure_equations_2026_05_22.json"

REQUIRED_EQUATION_IDS = {
    "scalar_metric_poisson_constraint",
    "gravitational_slip_equation",
    "scalar_field_perturbation_equation",
    "vector_temporal_constraint_perturbation",
    "vector_longitudinal_perturbation_equation",
    "matter_density_contrast_equation",
    "matter_velocity_equation",
    "transfer_function_closure_target",
}

def test_verifier_passes():
    result = subprocess.run(
        [sys.executable, "tools/verify_perturbation_closure_equations.py"],
        cwd=ROOT,
        text=True,
        capture_output=True,
        check=True,
    )
    assert "PERTURBATION_CLOSURE_EQUATIONS_SUPPLIED_STRUCTURAL_ONLY_NOT_NUMERICAL" in result.stdout
    assert "NUMERICAL_PARAMETER_VECTOR_NOT_SUPPLIED" in result.stdout

def test_perturbation_equations_cover_growth_and_cmb_closure():
    data = json.loads(PERTURBATION_SPEC.read_text())
    equations = data["closure_equations"]
    assert {item["equation_id"] for item in equations} == REQUIRED_EQUATION_IDS
    assert len(equations) == 8
    for item in equations:
        assert item["status"] == "structural_candidate"
        assert item["structural_equation"]
        assert item["coefficient_policy"]
        assert item["observable_role"]

def test_observable_map_links_to_closure_equations():
    data = json.loads(PERTURBATION_SPEC.read_text())
    equation_ids = {item["equation_id"] for item in data["closure_equations"]}
    observable_names = {item["observable"] for item in data["observable_closure_map"]}
    assert "f_sigma8_DFM(z)" in observable_names
    assert "C_ell_TT_DFM" in observable_names
    assert "C_ell_TE_DFM" in observable_names
    assert "C_ell_EE_DFM" in observable_names
    assert "S8_DFM" in observable_names
    for item in data["observable_closure_map"]:
        assert item["required_equations"]
        assert set(item["required_equations"]).issubset(equation_ids)
        assert item["status"]

def test_perturbation_closure_remains_non_numerical():
    data = json.loads(PERTURBATION_SPEC.read_text())
    assert data["symbolic_linearization_proved"] is False
    assert data["numerical_integration_supplied"] is False
    assert data["boltzmann_solver_supplied"] is False
    assert data["recombination_closure_supplied"] is False
    assert data["parameter_values_supplied"] is False
    assert data["initial_conditions_supplied"] is False
    assert data["empirical_validation_claimed"] is False
    assert data["likelihood_execution_claimed"] is False

def test_artifact_advances_root_blocker_without_overclaim():
    data = json.loads(ARTIFACT.read_text())
    assert data["root_blocker_removed"] == "PERTURBATION_CLOSURE_EQUATIONS_NOT_SUPPLIED"
    assert data["new_root_blocker"] == "NUMERICAL_PARAMETER_VECTOR_NOT_SUPPLIED"
    assert data["check_result"] == "PASS_STRUCTURAL_ONLY"
    boundary = "\n".join(data["boundary"])
    assert "does not prove a full symbolic linearization" in boundary
    assert "does not supply numerical integration" in boundary
    assert "does not supply a Boltzmann solver" in boundary
    assert "does not execute a likelihood comparison" in boundary
    assert "does not supply empirical evidence" in boundary
    assert "DFM-MKC" in data["does_not_prove"]
    assert "Lambda-CDM failure" in data["does_not_prove"]
    assert "any Clay problem" in data["does_not_prove"]
