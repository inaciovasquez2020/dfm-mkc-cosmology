import json
import subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
ARTIFACT = ROOT / "artifacts/repo_intake/dfm_mkc_field_equations_or_action_functional_target_2026_05_21.json"
VERIFIER = ROOT / "tools/verify_dfm_mkc_field_equations_or_action_functional_target.py"

def test_target_is_not_supplied():
    data = json.loads(ARTIFACT.read_text())
    assert data["status"] == "FIELD_EQUATIONS_OR_ACTION_FUNCTIONAL_TARGET_ONLY_NOT_SUPPLIED"
    assert data["field_equations_supplied"] is False
    assert data["action_functional_supplied"] is False
    assert data["observable_prediction_map_enabled"] is False

def test_required_fields_are_present():
    data = json.loads(ARTIFACT.read_text())
    fields = set(data["required_equation_object_fields"])
    assert "action_functional_or_closed_field_equations" in fields
    assert "matter_coupling_rule" in fields
    assert "dark_sector_coupling_rule" in fields
    assert "stress_energy_tensor_rule" in fields
    assert "observable_projection_rules" in fields

def test_downstream_objects_remain_blocked():
    data = json.loads(ARTIFACT.read_text())
    blocked = set(data["downstream_blocked_objects"])
    assert "DFM_FROZEN_PREDICTION_VECTOR" in blocked
    assert "DFM_LIKELIHOOD_RULE" in blocked
    assert "DFM_VS_LAMBDA_CDM_COMPARISON" in blocked

def test_boundary_forbids_overclaiming():
    data = json.loads(ARTIFACT.read_text())
    boundary = "\n".join(data["boundary"])
    for token in [
        "Does not supply DFM field equations.",
        "Does not supply DFM action functional.",
        "Does not supply observable prediction rules.",
        "Does not supply frozen predictions.",
        "Does not execute any likelihood.",
        "Does not prove DFM.",
        "Does not disprove Lambda-CDM.",
        "Does not replace CDM.",
    ]:
        assert token in boundary

def test_verifier_passes():
    result = subprocess.run(
        ["python3", str(VERIFIER)],
        cwd=ROOT,
        check=True,
        text=True,
        capture_output=True,
    )
    assert "verification OK" in result.stdout
