import json
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
GRID_SPEC = ROOT / "specs" / "OBSERVABLE_EVALUATION_GRID.json"
ARTIFACT = ROOT / "artifacts" / "repo_intake" / "observable_evaluation_grid_2026_05_22.json"

def test_verifier_passes():
    result = subprocess.run(
        [sys.executable, "tools/verify_observable_evaluation_grid.py"],
        cwd=ROOT,
        text=True,
        capture_output=True,
        check=True,
    )
    assert "OBSERVABLE_EVALUATION_GRID_SUPPLIED_REFERENCE_ONLY_NOT_DATA_BOUND" in result.stdout
    assert "DATA_VECTOR_SCHEMA_NOT_SUPPLIED" in result.stdout

def test_all_frozen_observables_have_grid_coverage():
    data = json.loads(GRID_SPEC.read_text())
    covered = {item["observable"] for item in data["observable_coverage"]}
    expected = {
        "E_DFM(z)",
        "D_A_DFM(z)",
        "D_L_DFM(z)",
        "mu_DFM(z)",
        "f_sigma8_DFM(z)",
        "C_ell_TT_DFM",
        "C_ell_TE_DFM",
        "C_ell_EE_DFM",
        "S8_DFM",
        "r_d_DFM",
    }
    assert covered == expected

def test_grid_values_are_reference_grids():
    data = json.loads(GRID_SPEC.read_text())
    by_id = {item["grid_id"]: item for item in data["evaluation_grids"]}
    assert by_id["background_redshift_grid"]["values"][0] == 0.0
    assert by_id["growth_redshift_grid"]["values"][0] == 0.0
    assert by_id["cmb_multipole_grid"]["values"][0] == 2
    assert by_id["perturbation_wavenumber_grid"]["values"][0] > 0
    assert by_id["sound_horizon_epoch_grid"]["values"][0] > 0
    for item in data["evaluation_grids"]:
        assert item["status"] == "reference_grid_not_data_bound"
        assert item["applies_to"]

def test_grid_is_not_data_bound_or_likelihood_ready():
    data = json.loads(GRID_SPEC.read_text())
    assert data["grid_policy"]["reference_grid_only"] is True
    assert data["grid_policy"]["bound_to_data_vector"] is False
    assert data["grid_policy"]["covariance_aligned"] is False
    assert data["grid_policy"]["likelihood_ready"] is False
    assert data["data_vector_supplied"] is False
    assert data["covariance_matrix_supplied"] is False
    assert data["likelihood_rule_supplied"] is False
    assert data["empirical_validation_claimed"] is False
    assert data["model_selection_claimed"] is False

def test_artifact_advances_root_blocker_without_overclaim():
    data = json.loads(ARTIFACT.read_text())
    assert data["root_blocker_removed"] == "OBSERVABLE_EVALUATION_GRID_NOT_SUPPLIED"
    assert data["new_root_blocker"] == "DATA_VECTOR_SCHEMA_NOT_SUPPLIED"
    assert data["check_result"] == "PASS_REFERENCE_GRID_ONLY"
    boundary = "\n".join(data["boundary"])
    assert "does not bind grids to an empirical data vector" in boundary
    assert "does not supply a data vector" in boundary
    assert "does not supply a covariance matrix" in boundary
    assert "does not execute a likelihood comparison" in boundary
    assert "does not supply empirical evidence" in boundary
    assert "DFM-MKC" in data["does_not_prove"]
    assert "Lambda-CDM failure" in data["does_not_prove"]
    assert "any Clay problem" in data["does_not_prove"]
