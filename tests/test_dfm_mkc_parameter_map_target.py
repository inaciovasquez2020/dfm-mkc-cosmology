import json
import subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
ARTIFACT = ROOT / "artifacts/repo_intake/dfm_mkc_parameter_map_target_2026_05_21.json"
VERIFIER = ROOT / "tools/verify_dfm_mkc_parameter_map_target.py"

def test_target_is_not_supplied():
    data = json.loads(ARTIFACT.read_text())
    assert data["status"] == "PARAMETER_MAP_TARGET_ONLY_NOT_SUPPLIED"
    assert data["parameter_map_supplied"] is False
    assert data["parameter_values_frozen"] is False
    assert data["prior_ranges_supplied"] is False
    assert data["observable_parameter_projection_enabled"] is False

def test_required_parameter_fields_are_present():
    data = json.loads(ARTIFACT.read_text())
    fields = set(data["required_parameter_object_fields"])
    assert "primitive_parameter_names" in fields
    assert "parameter_definitions" in fields
    assert "dimensional_units" in fields
    assert "prior_ranges" in fields
    assert "observable_channel_dependencies" in fields
    assert "holdout_freeze_certificate" in fields

def test_prediction_channels_remain_blocked():
    data = json.loads(ARTIFACT.read_text())
    channels = set(data["required_prediction_channels_blocked"])
    assert "CMB_TT_TE_EE" in channels
    assert "BAO_DISTANCES" in channels
    assert "SNIA_DISTANCES" in channels
    assert "WEAK_LENSING_AND_CLUSTERING" in channels

def test_downstream_objects_remain_blocked():
    data = json.loads(ARTIFACT.read_text())
    blocked = set(data["downstream_blocked_objects"])
    assert "DFM_OBSERVABLE_PREDICTION_RULES" in blocked
    assert "DFM_FROZEN_PREDICTION_VECTOR" in blocked
    assert "DFM_LIKELIHOOD_RULE" in blocked
    assert "DFM_VS_LAMBDA_CDM_COMPARISON" in blocked

def test_boundary_forbids_overclaiming():
    data = json.loads(ARTIFACT.read_text())
    boundary = "\n".join(data["boundary"])
    for token in [
        "Does not supply DFM parameter map.",
        "Does not supply parameter values.",
        "Does not supply prior ranges.",
        "Does not freeze DFM parameters.",
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
