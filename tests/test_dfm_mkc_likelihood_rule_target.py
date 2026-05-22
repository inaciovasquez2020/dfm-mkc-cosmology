import json
import subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
ARTIFACT = ROOT / "artifacts/repo_intake/dfm_mkc_likelihood_rule_target_2026_05_21.json"
VERIFIER = ROOT / "tools/verify_dfm_mkc_likelihood_rule_target.py"

def test_target_is_not_supplied():
    data = json.loads(ARTIFACT.read_text())
    assert data["status"] == "LIKELIHOOD_RULE_TARGET_ONLY_NOT_SUPPLIED"
    assert data["likelihood_rule_supplied"] is False
    assert data["joint_likelihood_supplied"] is False
    assert data["probe_likelihoods_supplied"] is False
    assert data["likelihood_executed"] is False
    assert data["empirical_evidence_supplied"] is False

def test_required_upstream_objects_are_present():
    data = json.loads(ARTIFACT.read_text())
    upstream = set(data["upstream_required_objects"])
    assert "DFM_FIELD_EQUATIONS_OR_ACTION_FUNCTIONAL" in upstream
    assert "DFM_PARAMETER_MAP" in upstream
    assert "DFM_OBSERVABLE_PREDICTION_RULES" in upstream
    assert "DFM_FROZEN_PREDICTION_VECTOR" in upstream
    assert "DFM_EXTERNAL_DATA_MANIFEST" in upstream

def test_required_likelihood_fields_are_present():
    data = json.loads(ARTIFACT.read_text())
    fields = set(data["required_likelihood_rule_fields"])
    assert "data_vector_reference" in fields
    assert "frozen_prediction_vector_reference" in fields
    assert "covariance_matrix_reference" in fields
    assert "residual_vector_definition" in fields
    assert "joint_likelihood_composition_rule" in fields
    assert "model_comparison_metrics" in fields
    assert "reproduction_command" in fields

def test_probe_likelihood_channels_remain_blocked():
    data = json.loads(ARTIFACT.read_text())
    channels = data["required_probe_likelihood_channels"]
    for key in [
        "CMB_TT_TE_EE",
        "CMB_LENSING",
        "BAO_DISTANCES",
        "SNIA_DISTANCES",
        "WEAK_LENSING_AND_CLUSTERING",
        "CLUSTER_ABUNDANCE",
    ]:
        assert key in channels
        assert channels[key]["status"] == "blocked_no_dfm_likelihood_rule"

def test_downstream_objects_remain_blocked():
    data = json.loads(ARTIFACT.read_text())
    blocked = set(data["downstream_blocked_objects"])
    assert "DFM_HOLDOUT_SPLIT_EXECUTION" in blocked
    assert "DFM_VS_LAMBDA_CDM_COMPARISON" in blocked
    assert "DFM_EMPIRICAL_EVIDENCE_CLAIM" in blocked
    assert "DFM_CDM_REPLACEMENT_CLAIM" in blocked

def test_boundary_forbids_overclaiming():
    data = json.loads(ARTIFACT.read_text())
    boundary = "\n".join(data["boundary"])
    for token in [
        "Does not supply likelihood equations.",
        "Does not supply covariance matrices.",
        "Does not supply probe likelihoods.",
        "Does not supply joint likelihood.",
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
