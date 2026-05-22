import json
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
NUMERIC_SPEC = ROOT / "specs" / "NUMERICAL_PARAMETER_VECTOR.json"
ARTIFACT = ROOT / "artifacts" / "repo_intake" / "numerical_parameter_vector_2026_05_22.json"

EXPECTED_ORDER = [
    "M_Pl",
    "Lambda_0",
    "alpha_phi",
    "m_phi",
    "lambda_phi",
    "alpha_A",
    "m_A",
    "beta_phi_A",
    "xi_phi",
    "xi_A",
    "gamma_m",
]

def test_verifier_passes():
    result = subprocess.run(
        [sys.executable, "tools/verify_numerical_parameter_vector.py"],
        cwd=ROOT,
        text=True,
        capture_output=True,
        check=True,
    )
    assert "NUMERICAL_PARAMETER_VECTOR_SUPPLIED_REFERENCE_CANDIDATE_ONLY_NOT_FIT" in result.stdout
    assert "INITIAL_CONDITIONS_NOT_SUPPLIED" in result.stdout

def test_parameter_vector_order_and_values_are_supplied():
    data = json.loads(NUMERIC_SPEC.read_text())
    assert data["object_id"] == "NUMERICAL_PARAMETER_VECTOR"
    assert data["parameter_vector_order"] == EXPECTED_ORDER
    assert data["vector_policy"]["parameter_order_locked"] is True
    assert data["vector_policy"]["numerical_values_supplied"] is True
    assert len(data["parameter_values"]) == len(EXPECTED_ORDER)
    for index, symbol in enumerate(EXPECTED_ORDER):
        item = data["parameter_values"][index]
        assert item["index"] == index
        assert item["symbol"] == symbol
        assert isinstance(item["value"], (int, float))
        assert item["constraint_status"]
        assert item["selection_rule"]

def test_parameter_vector_is_reference_candidate_not_fit():
    data = json.loads(NUMERIC_SPEC.read_text())
    assert data["vector_policy"]["reference_candidate_only"] is True
    assert data["vector_policy"]["fit_to_data"] is False
    assert data["vector_policy"]["posterior_sample"] is False
    assert data["vector_policy"]["best_fit_claimed"] is False
    assert data["vector_policy"]["physical_calibration_claimed"] is False
    assert data["empirical_validation_claimed"] is False
    assert data["model_selection_claimed"] is False

def test_domain_constraints_are_respected():
    data = json.loads(NUMERIC_SPEC.read_text())
    values = {item["symbol"]: item["value"] for item in data["parameter_values"]}
    assert values["M_Pl"] > 0
    assert values["alpha_phi"] > 0
    assert values["alpha_A"] > 0
    assert values["m_phi"] >= 0
    assert values["lambda_phi"] >= 0
    assert values["m_A"] >= 0

def test_artifact_advances_root_blocker_without_overclaim():
    data = json.loads(ARTIFACT.read_text())
    assert data["root_blocker_removed"] == "NUMERICAL_PARAMETER_VECTOR_NOT_SUPPLIED"
    assert data["new_root_blocker"] == "INITIAL_CONDITIONS_NOT_SUPPLIED"
    assert data["check_result"] == "PASS_REFERENCE_VECTOR_ONLY"
    boundary = "\n".join(data["boundary"])
    assert "does not claim the vector is fit to data" in boundary
    assert "does not claim physical calibration" in boundary
    assert "does not supply initial conditions" in boundary
    assert "does not execute a likelihood comparison" in boundary
    assert "does not supply empirical evidence" in boundary
    assert "DFM-MKC" in data["does_not_prove"]
    assert "Lambda-CDM failure" in data["does_not_prove"]
    assert "any Clay problem" in data["does_not_prove"]
