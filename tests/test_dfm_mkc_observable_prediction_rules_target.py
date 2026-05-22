import json
import subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
ARTIFACT = ROOT / "artifacts/repo_intake/dfm_mkc_observable_prediction_rules_target_2026_05_21.json"
VERIFIER = ROOT / "tools/verify_dfm_mkc_observable_prediction_rules_target.py"

def test_target_is_not_supplied():
    data = json.loads(ARTIFACT.read_text())
    assert data["status"] == "OBSERVABLE_PREDICTION_RULES_TARGET_ONLY_NOT_SUPPLIED"
    assert data["observable_prediction_rules_supplied"] is False
    assert data["channel_projection_rules_supplied"] is False
    assert data["residual_vector_rules_supplied"] is False
    assert data["covariance_compatibility_supplied"] is False
    assert data["likelihood_ready"] is False

def test_required_prediction_rule_fields_are_present():
    data = json.loads(ARTIFACT.read_text())
    fields = set(data["required_prediction_rule_fields"])
    assert "forward_model_equations" in fields
    assert "projection_from_dfm_state_to_observable" in fields
    assert "covariance_compatibility_rule" in fields
    assert "residual_vector_definition" in fields
    assert "holdout_freeze_rule" in fields

def test_observable_channels_remain_blocked():
    data = json.loads(ARTIFACT.read_text())
    channels = data["required_observable_channels"]
    for key in [
        "CMB_TT_TE_EE",
        "CMB_LENSING",
        "BAO_DISTANCES",
        "SNIA_DISTANCES",
        "WEAK_LENSING_AND_CLUSTERING",
        "CLUSTER_ABUNDANCE",
    ]:
        assert key in channels
        assert channels[key]["status"] == "blocked_no_dfm_observable_prediction_rule"

def test_downstream_objects_remain_blocked():
    data = json.loads(ARTIFACT.read_text())
    blocked = set(data["downstream_blocked_objects"])
    assert "DFM_FROZEN_PREDICTION_VECTOR" in blocked
    assert "DFM_LIKELIHOOD_RULE" in blocked
    assert "DFM_HOLDOUT_SPLIT" in blocked
    assert "DFM_VS_LAMBDA_CDM_COMPARISON" in blocked

def test_boundary_forbids_overclaiming():
    data = json.loads(ARTIFACT.read_text())
    boundary = "\n".join(data["boundary"])
    for token in [
        "Does not supply DFM observable prediction rules.",
        "Does not supply channel projection rules.",
        "Does not supply residual vector rules.",
        "Does not supply covariance compatibility rules.",
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
