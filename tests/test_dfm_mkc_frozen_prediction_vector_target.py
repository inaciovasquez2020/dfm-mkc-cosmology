import json
import subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
ARTIFACT = ROOT / "artifacts/repo_intake/dfm_mkc_frozen_prediction_vector_target_2026_05_21.json"
VERIFIER = ROOT / "tools/verify_dfm_mkc_frozen_prediction_vector_target.py"

def test_target_is_not_supplied():
    data = json.loads(ARTIFACT.read_text())
    assert data["status"] == "FROZEN_PREDICTION_VECTOR_TARGET_ONLY_NOT_SUPPLIED"
    assert data["frozen_prediction_vector_supplied"] is False
    assert data["prediction_values_frozen"] is False
    assert data["parameter_values_frozen"] is False
    assert data["likelihood_ready"] is False

def test_required_upstream_objects_are_present():
    data = json.loads(ARTIFACT.read_text())
    upstream = set(data["upstream_required_objects"])
    assert "DFM_FIELD_EQUATIONS_OR_ACTION_FUNCTIONAL" in upstream
    assert "DFM_PARAMETER_MAP" in upstream
    assert "DFM_OBSERVABLE_PREDICTION_RULES" in upstream

def test_required_frozen_vector_fields_are_present():
    data = json.loads(ARTIFACT.read_text())
    fields = set(data["required_frozen_vector_fields"])
    assert "freeze_identifier" in fields
    assert "source_commit" in fields
    assert "frozen_parameter_values" in fields
    assert "prediction_channel_vectors" in fields
    assert "no_post_hoc_tuning_certificate" in fields
    assert "reproduction_command" in fields

def test_prediction_channels_remain_blocked():
    data = json.loads(ARTIFACT.read_text())
    channels = data["required_prediction_channels"]
    for key in [
        "CMB_TT_TE_EE",
        "CMB_LENSING",
        "BAO_DISTANCES",
        "SNIA_DISTANCES",
        "WEAK_LENSING_AND_CLUSTERING",
        "CLUSTER_ABUNDANCE",
    ]:
        assert key in channels
        assert channels[key]["status"] == "blocked_no_frozen_prediction_vector"

def test_downstream_objects_remain_blocked():
    data = json.loads(ARTIFACT.read_text())
    blocked = set(data["downstream_blocked_objects"])
    assert "DFM_LIKELIHOOD_RULE" in blocked
    assert "DFM_HOLDOUT_SPLIT_EXECUTION" in blocked
    assert "DFM_VS_LAMBDA_CDM_COMPARISON" in blocked
    assert "EMPIRICAL_EVIDENCE_CLAIM" in blocked

def test_boundary_forbids_overclaiming():
    data = json.loads(ARTIFACT.read_text())
    boundary = "\n".join(data["boundary"])
    for token in [
        "Does not supply frozen DFM prediction values.",
        "Does not supply frozen parameter values.",
        "Does not supply holdout split execution.",
        "Does not execute any likelihood.",
        "Does not produce empirical evidence.",
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
