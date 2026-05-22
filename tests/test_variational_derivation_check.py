import json
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CHECK_SPEC = ROOT / "specs" / "VARIATIONAL_DERIVATION_CHECK.json"
ARTIFACT = ROOT / "artifacts" / "repo_intake" / "variational_derivation_check_2026_05_22.json"

def test_verifier_passes():
    result = subprocess.run(
        [sys.executable, "tools/verify_variational_derivation_check.py"],
        cwd=ROOT,
        text=True,
        capture_output=True,
        check=True,
    )
    assert "STRUCTURAL_VARIATIONAL_DERIVATION_CHECK_SUPPLIED_NOT_SYMBOLICALLY_PROVED" in result.stdout
    assert "PARAMETER_DOMAIN_AND_UNITS_TABLE_NOT_SUPPLIED" in result.stdout

def test_variational_check_fills_required_object():
    data = json.loads(CHECK_SPEC.read_text())
    assert data["object_id"] == "VARIATIONAL_DERIVATION_CHECK"
    assert data["input_object"] == "FILLED_SUPPLIED_DFM_FIELD_EQUATIONS_AND_ACTION_FUNCTIONAL"
    assert data["check_result"] == "PASS_STRUCTURAL_ONLY"
    assert data["symbolic_variation_proved"] is False
    assert data["physical_correctness_claimed"] is False
    assert data["empirical_validation_claimed"] is False
    assert data["likelihood_execution_claimed"] is False

def test_checked_variations_cover_supplied_equation_targets():
    data = json.loads(CHECK_SPEC.read_text())
    targets = {item["equation_target"] for item in data["checked_variations"]}
    assert targets == {
        "metric_equation",
        "scalar_equation",
        "vector_equation",
        "matter_equation",
    }
    for item in data["checked_variations"]:
        assert item["structural_result"] == "matched"
        assert item["required_sources"]

def test_artifact_advances_root_blocker_without_overclaim():
    data = json.loads(ARTIFACT.read_text())
    assert data["root_blocker_removed"] == "VARIATIONAL_DERIVATION_CHECK_NOT_SUPPLIED"
    assert data["new_root_blocker"] == "PARAMETER_DOMAIN_AND_UNITS_TABLE_NOT_SUPPLIED"
    assert data["check_result"] == "PASS_STRUCTURAL_ONLY"
    boundary = "\n".join(data["boundary"])
    assert "does not prove a full symbolic variational derivation" in boundary
    assert "does not validate physical correctness" in boundary
    assert "does not supply empirical evidence" in boundary
    assert "DFM-MKC" in data["does_not_prove"]
    assert "Lambda-CDM failure" in data["does_not_prove"]
    assert "any Clay problem" in data["does_not_prove"]
