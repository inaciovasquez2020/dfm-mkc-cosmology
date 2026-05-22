import json
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
VECTOR_SPEC = ROOT / "specs" / "FROZEN_PREDICTION_VECTOR.json"
ARTIFACT = ROOT / "artifacts" / "repo_intake" / "frozen_prediction_vector_2026_05_22.json"

EXPECTED_VECTOR_ORDER = [
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
]

def test_verifier_passes():
    result = subprocess.run(
        [sys.executable, "tools/verify_frozen_prediction_vector.py"],
        cwd=ROOT,
        text=True,
        capture_output=True,
        check=True,
    )
    assert "FROZEN_PREDICTION_VECTOR_SUPPLIED_SYMBOLIC_ONLY_NOT_EXECUTABLE" in result.stdout
    assert "EXECUTED_DFM_VS_LAMBDA_CDM_COMPARISON_NOT_SUPPLIED" in result.stdout

def test_vector_order_and_definitions_are_locked():
    data = json.loads(VECTOR_SPEC.read_text())
    assert data["object_id"] == "FROZEN_PREDICTION_VECTOR"
    assert data["observable_vector_order"] == EXPECTED_VECTOR_ORDER
    assert data["freeze_policy"]["vector_order_locked"] is True
    assert data["freeze_policy"]["observable_names_locked"] is True
    assert data["freeze_policy"]["symbolic_definitions_locked"] is True
    assert len(data["observable_definitions"]) == len(EXPECTED_VECTOR_ORDER)
    for index, name in enumerate(EXPECTED_VECTOR_ORDER):
        item = data["observable_definitions"][index]
        assert item["index"] == index
        assert item["name"] == name
        assert item["definition"]
        assert item["depends_on"]
        assert item["numerical_value_supplied"] is False

def test_vector_remains_non_executable_and_non_empirical():
    data = json.loads(VECTOR_SPEC.read_text())
    assert data["freeze_policy"]["numerical_values_supplied"] is False
    assert data["freeze_policy"]["covariance_matrix_supplied"] is False
    assert data["freeze_policy"]["likelihood_rule_supplied"] is False
    assert data["numerical_prediction_claimed"] is False
    assert data["covariance_matrix_claimed"] is False
    assert data["likelihood_execution_claimed"] is False
    assert data["empirical_validation_claimed"] is False
    assert data["physical_correctness_claimed"] is False

def test_artifact_advances_root_blocker_without_overclaim():
    data = json.loads(ARTIFACT.read_text())
    assert data["root_blocker_removed"] == "FROZEN_PREDICTION_VECTOR_NOT_SUPPLIED"
    assert data["new_root_blocker"] == "EXECUTED_DFM_VS_LAMBDA_CDM_COMPARISON_NOT_SUPPLIED"
    assert data["check_result"] == "PASS_STRUCTURAL_ONLY"
    boundary = "\n".join(data["boundary"])
    assert "does not supply numerical prediction values" in boundary
    assert "does not supply a covariance matrix" in boundary
    assert "does not supply a likelihood rule" in boundary
    assert "does not execute a likelihood comparison" in boundary
    assert "does not supply empirical evidence" in boundary
    assert "DFM-MKC" in data["does_not_prove"]
    assert "Lambda-CDM failure" in data["does_not_prove"]
    assert "any Clay problem" in data["does_not_prove"]
