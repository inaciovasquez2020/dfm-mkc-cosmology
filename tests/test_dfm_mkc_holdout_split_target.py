import json
import subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
ARTIFACT = ROOT / "artifacts/repo_intake/dfm_mkc_holdout_split_target_2026_05_21.json"
VERIFIER = ROOT / "tools/verify_dfm_mkc_holdout_split_target.py"

def test_target_is_not_supplied():
    data = json.loads(ARTIFACT.read_text())
    assert data["status"] == "HOLDOUT_SPLIT_TARGET_ONLY_NOT_SUPPLIED"
    assert data["holdout_split_supplied"] is False
    assert data["holdout_execution_supplied"] is False
    assert data["blind_protocol_supplied"] is False
    assert data["likelihood_executed"] is False
    assert data["empirical_evidence_supplied"] is False

def test_required_upstream_objects_are_present():
    data = json.loads(ARTIFACT.read_text())
    upstream = set(data["upstream_required_objects"])
    assert "DFM_FIELD_EQUATIONS_OR_ACTION_FUNCTIONAL" in upstream
    assert "DFM_PARAMETER_MAP" in upstream
    assert "DFM_OBSERVABLE_PREDICTION_RULES" in upstream
    assert "DFM_FROZEN_PREDICTION_VECTOR" in upstream
    assert "DFM_LIKELIHOOD_RULE" in upstream
    assert "DFM_EXTERNAL_DATA_MANIFEST" in upstream

def test_required_holdout_fields_are_present():
    data = json.loads(ARTIFACT.read_text())
    fields = set(data["required_holdout_split_fields"])
    assert "training_data_sources" in fields
    assert "validation_data_sources" in fields
    assert "holdout_data_sources" in fields
    assert "blind_data_sources" in fields
    assert "no_post_hoc_tuning_certificate" in fields
    assert "reproduction_command" in fields

def test_candidate_roles_remain_blocked():
    data = json.loads(ARTIFACT.read_text())
    roles = data["candidate_data_source_roles"]
    assert roles["training_or_calibration"]["status"] == "blocked_no_holdout_split"
    assert roles["validation"]["status"] == "blocked_no_holdout_split"
    assert roles["blind_holdout"]["status"] == "blocked_no_holdout_split"

def test_probe_coverage_remains_blocked():
    data = json.loads(ARTIFACT.read_text())
    probes = data["required_probe_coverage"]
    for key in [
        "CMB_TT_TE_EE",
        "CMB_LENSING",
        "BAO_DISTANCES",
        "SNIA_DISTANCES",
        "WEAK_LENSING_AND_CLUSTERING",
        "CLUSTER_ABUNDANCE",
    ]:
        assert key in probes
        assert probes[key]["status"] == "blocked_no_holdout_assignment"

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
        "Does not assign training data.",
        "Does not assign validation data.",
        "Does not assign blind holdout data.",
        "Does not execute holdout evaluation.",
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
