import json
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SCHEMA_SPEC = ROOT / "specs" / "DATA_VECTOR_SCHEMA.json"
VECTOR_SPEC = ROOT / "specs" / "FROZEN_PREDICTION_VECTOR.json"
ARTIFACT = ROOT / "artifacts" / "repo_intake" / "data_vector_schema_2026_05_22.json"

def test_verifier_passes():
    result = subprocess.run(
        [sys.executable, "tools/verify_data_vector_schema.py"],
        cwd=ROOT,
        text=True,
        capture_output=True,
        check=True,
    )
    assert "DATA_VECTOR_SCHEMA_SUPPLIED_SCHEMA_ONLY_NO_EMPIRICAL_VALUES" in result.stdout
    assert "COVARIANCE_MATRIX_NOT_SUPPLIED" in result.stdout

def test_data_slots_match_frozen_prediction_vector_order():
    schema = json.loads(SCHEMA_SPEC.read_text())
    vector = json.loads(VECTOR_SPEC.read_text())
    slot_observables = [item["observable"] for item in schema["data_slots"]]
    assert slot_observables == vector["observable_vector_order"]
    assert len(schema["data_slots"]) == 10
    for index, item in enumerate(schema["data_slots"]):
        assert item["index"] == index
        assert item["model_observable"] == vector["observable_vector_order"][index]
        assert item["grid_ids"]

def test_schema_contains_no_empirical_values_or_payload_binding():
    data = json.loads(SCHEMA_SPEC.read_text())
    assert data["schema_policy"]["schema_only"] is True
    assert data["schema_policy"]["empirical_values_supplied"] is False
    assert data["schema_policy"]["bound_to_external_payload"] is False
    assert data["schema_policy"]["covariance_matrix_supplied"] is False
    assert data["schema_policy"]["likelihood_ready"] is False
    for item in data["data_slots"]:
        assert item["data_value_supplied"] is False
        assert item["uncertainty_supplied"] is False
        assert item["payload_binding"] == "unbound"

def test_schema_flags_remain_non_empirical():
    data = json.loads(SCHEMA_SPEC.read_text())
    assert data["data_vector_schema_supplied"] is True
    assert data["empirical_values_supplied"] is False
    assert data["covariance_matrix_supplied"] is False
    assert data["likelihood_rule_supplied"] is False
    assert data["lambda_cdm_baseline_supplied"] is False
    assert data["empirical_validation_claimed"] is False
    assert data["model_selection_claimed"] is False

def test_artifact_advances_root_blocker_without_overclaim():
    data = json.loads(ARTIFACT.read_text())
    assert data["root_blocker_removed"] == "DATA_VECTOR_SCHEMA_NOT_SUPPLIED"
    assert data["new_root_blocker"] == "COVARIANCE_MATRIX_NOT_SUPPLIED"
    assert data["check_result"] == "PASS_SCHEMA_ONLY"
    boundary = "\n".join(data["boundary"])
    assert "does not supply empirical data values" in boundary
    assert "does not supply observational uncertainties" in boundary
    assert "does not bind slots to an external payload" in boundary
    assert "does not supply a covariance matrix" in boundary
    assert "does not execute a likelihood comparison" in boundary
    assert "does not supply empirical evidence" in boundary
    assert "DFM-MKC" in data["does_not_prove"]
    assert "Lambda-CDM failure" in data["does_not_prove"]
    assert "any Clay problem" in data["does_not_prove"]
