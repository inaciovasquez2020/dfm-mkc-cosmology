import json
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
ANSATZ_SPEC = ROOT / "specs" / "COSMOLOGICAL_REDUCTION_ANSATZ.json"
ARTIFACT = ROOT / "artifacts" / "repo_intake" / "cosmological_reduction_ansatz_2026_05_22.json"

def test_verifier_passes():
    result = subprocess.run(
        [sys.executable, "tools/verify_cosmological_reduction_ansatz.py"],
        cwd=ROOT,
        text=True,
        capture_output=True,
        check=True,
    )
    assert "COSMOLOGICAL_REDUCTION_ANSATZ_SUPPLIED_STRUCTURAL_ONLY" in result.stdout
    assert "FROZEN_PREDICTION_VECTOR_NOT_SUPPLIED" in result.stdout

def test_ansatz_supplies_flrw_background_structure():
    data = json.loads(ANSATZ_SPEC.read_text())
    assert data["object_id"] == "COSMOLOGICAL_REDUCTION_ANSATZ"
    assert data["ansatz_class"] == "homogeneous_isotropic_FLRW_background"
    assert "N(t)" in data["metric_ansatz"]["line_element"]
    assert "a(t)" in data["metric_ansatz"]["line_element"]
    assert "gamma_ij" in data["metric_ansatz"]["line_element"]
    assert data["metric_ansatz"]["lapse"] == "N(t) > 0"
    assert data["metric_ansatz"]["scale_factor"] == "a(t) > 0"

def test_background_targets_cover_supplied_field_equations():
    data = json.loads(ANSATZ_SPEC.read_text())
    targets = data["background_equation_targets"]
    source_equations = {item["source_equation"] for item in targets}
    assert source_equations == {
        "metric_equation",
        "scalar_equation",
        "vector_equation",
        "matter_equation",
    }
    assert len(targets) == 5
    assert all(item["structural_form"] for item in targets)
    assert all(item["role"] for item in targets)

def test_artifact_advances_root_blocker_without_overclaim():
    data = json.loads(ARTIFACT.read_text())
    assert data["root_blocker_removed"] == "COSMOLOGICAL_REDUCTION_ANSATZ_NOT_SUPPLIED"
    assert data["new_root_blocker"] == "FROZEN_PREDICTION_VECTOR_NOT_SUPPLIED"
    assert data["check_result"] == "PASS_STRUCTURAL_ONLY"
    boundary = "\n".join(data["boundary"])
    assert "does not derive the reduced equations" in boundary
    assert "does not supply numerical parameter values" in boundary
    assert "does not supply empirical evidence" in boundary
    assert "DFM-MKC" in data["does_not_prove"]
    assert "Lambda-CDM failure" in data["does_not_prove"]
    assert "any Clay problem" in data["does_not_prove"]
