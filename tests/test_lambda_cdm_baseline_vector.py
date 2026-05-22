import json
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
BASE = ROOT / "specs" / "LAMBDA_CDM_BASELINE_VECTOR.json"
SCHEMA = ROOT / "specs" / "DATA_VECTOR_SCHEMA.json"
ART = ROOT / "artifacts" / "repo_intake" / "lambda_cdm_baseline_vector_2026_05_22.json"

def test_verifier_passes():
    result = subprocess.run(
        [sys.executable, "tools/verify_lambda_cdm_baseline_vector.py"],
        cwd=ROOT,
        text=True,
        capture_output=True,
        check=True,
    )
    assert "LAMBDA_CDM_BASELINE_VECTOR_SUPPLIED_REFERENCE_ONLY_NOT_EMPIRICAL" in result.stdout
    assert "INDEPENDENT_EMPIRICAL_VALIDATION_NOT_SUPPLIED" in result.stdout

def test_baseline_matches_schema_order():
    base = json.loads(BASE.read_text())
    schema = json.loads(SCHEMA.read_text())
    assert base["baseline_slot_order"] == schema["data_vector_slot_order"]
    assert len(base["baseline_values"]) == len(schema["data_vector_slot_order"])

def test_baseline_is_reference_only():
    base = json.loads(BASE.read_text())
    assert base["lambda_cdm_baseline_supplied"] is True
    assert base["fit_to_data"] is False
    assert base["best_fit_claimed"] is False
    assert base["empirical_validation_claimed"] is False
    assert base["model_selection_claimed"] is False

def test_artifact_advances_without_overclaim():
    data = json.loads(ART.read_text())
    assert data["root_blocker_removed"] == "LAMBDA_CDM_BASELINE_VECTOR_NOT_SUPPLIED"
    assert data["new_root_blocker"] == "INDEPENDENT_EMPIRICAL_VALIDATION_NOT_SUPPLIED"
    boundary = "\n".join(data["boundary"])
    assert "does not claim the baseline is fit to data" in boundary
    assert "does not execute model selection" in boundary
    assert "does not supply empirical evidence" in boundary
    assert "any Clay problem" in data["does_not_prove"]
