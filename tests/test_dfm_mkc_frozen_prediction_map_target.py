import json
import subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
ARTIFACT = ROOT / "artifacts/repo_intake/dfm_mkc_frozen_prediction_map_target_2026_05_21.json"
VERIFIER = ROOT / "tools/verify_dfm_mkc_frozen_prediction_map_target.py"

def test_artifact_exists_and_is_target_only():
    data = json.loads(ARTIFACT.read_text())
    assert data["status"] == "FROZEN_PREDICTION_MAP_TARGET_ONLY_PREDICTIONS_NOT_SUPPLIED"
    assert data["prediction_map_supplied"] is False
    assert data["frozen_predictions_supplied"] is False
    assert data["likelihood_executed"] is False

def test_required_blockers_are_present():
    data = json.loads(ARTIFACT.read_text())
    blockers = set(data["required_missing_objects"])
    assert "DFM_FIELD_EQUATIONS_OR_ACTION_FUNCTIONAL" in blockers
    assert "DFM_FROZEN_PREDICTION_VECTOR" in blockers
    assert "DFM_LIKELIHOOD_RULE" in blockers
    assert "NO_POST_HOC_TUNING_CERTIFICATE" in blockers

def test_boundary_prevents_overclaiming():
    data = json.loads(ARTIFACT.read_text())
    boundary = "\n".join(data["boundary"])
    assert "Does not supply DFM equations." in boundary
    assert "Does not supply frozen DFM predictions." in boundary
    assert "Does not prove DFM." in boundary
    assert "Does not disprove Lambda-CDM." in boundary
    assert "Does not replace CDM." in boundary

def test_verifier_passes():
    result = subprocess.run(
        ["python3", str(VERIFIER)],
        cwd=ROOT,
        check=True,
        text=True,
        capture_output=True,
    )
    assert "verification OK" in result.stdout
