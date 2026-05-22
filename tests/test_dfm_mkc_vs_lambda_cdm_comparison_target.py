import json
import subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
ARTIFACT = ROOT / "artifacts/repo_intake/dfm_mkc_vs_lambda_cdm_comparison_target_2026_05_21.json"
VERIFIER = ROOT / "tools/verify_dfm_mkc_vs_lambda_cdm_comparison_target.py"

def test_target_is_not_supplied():
    data = json.loads(ARTIFACT.read_text())
    assert data["status"] == "DFM_VS_LAMBDA_CDM_COMPARISON_TARGET_ONLY_NOT_SUPPLIED"
    assert data["comparison_executed"] is False
    assert data["dfm_metrics_supplied"] is False
    assert data["lambda_cdm_metrics_supplied"] is False
    assert data["holdout_evaluation_executed"] is False
    assert data["empirical_evidence_supplied"] is False
    assert data["dfm_proved"] is False
    assert data["lambda_cdm_disproved"] is False
    assert data["cdm_replaced"] is False

def test_required_upstream_objects_are_present():
    data = json.loads(ARTIFACT.read_text())
    upstream = set(data["upstream_required_objects"])
    assert "DFM_FIELD_EQUATIONS_OR_ACTION_FUNCTIONAL" in upstream
    assert "DFM_PARAMETER_MAP" in upstream
    assert "DFM_OBSERVABLE_PREDICTION_RULES" in upstream
    assert "DFM_FROZEN_PREDICTION_VECTOR" in upstream
    assert "DFM_LIKELIHOOD_RULE" in upstream
    assert "DFM_HOLDOUT_SPLIT" in upstream
    assert "DFM_EXTERNAL_DATA_MANIFEST" in upstream

def test_required_comparison_fields_are_present():
    data = json.loads(ARTIFACT.read_text())
    fields = set(data["required_comparison_fields"])
    assert "dfm_metric_outputs" in fields
    assert "lambda_cdm_metric_outputs" in fields
    assert "delta_chi_square" in fields
    assert "delta_aic" in fields
    assert "delta_bic" in fields
    assert "holdout_survival_status" in fields
    assert "independent_reproduction_status" in fields
    assert "reproduction_command" in fields

def test_probe_comparison_channels_remain_blocked():
    data = json.loads(ARTIFACT.read_text())
    channels = data["required_probe_comparison_channels"]
    for key in [
        "CMB_TT_TE_EE",
        "CMB_LENSING",
        "BAO_DISTANCES",
        "SNIA_DISTANCES",
        "WEAK_LENSING_AND_CLUSTERING",
        "CLUSTER_ABUNDANCE",
    ]:
        assert key in channels
        assert channels[key]["status"] == "blocked_no_comparison_execution"

def test_required_decision_outputs_are_present():
    data = json.loads(ARTIFACT.read_text())
    outputs = set(data["required_decision_outputs"])
    assert "delta_chi_square" in outputs
    assert "delta_aic" in outputs
    assert "delta_bic" in outputs
    assert "holdout_survival_boolean" in outputs
    assert "probe_consistency_table" in outputs
    assert "no_post_hoc_tuning_audit" in outputs

def test_downstream_objects_remain_blocked():
    data = json.loads(ARTIFACT.read_text())
    blocked = set(data["downstream_blocked_objects"])
    assert "DFM_EMPIRICAL_EVIDENCE_CLAIM" in blocked
    assert "DFM_LAMBDA_CDM_FAILURE_CLAIM" in blocked
    assert "DFM_CDM_REPLACEMENT_CLAIM" in blocked
    assert "DFM_FINAL_COSMOLOGY_CLOSURE_CLAIM" in blocked

def test_boundary_forbids_overclaiming():
    data = json.loads(ARTIFACT.read_text())
    boundary = "\n".join(data["boundary"])
    for token in [
        "Does not execute DFM-vs-Lambda-CDM comparison.",
        "Does not supply DFM metrics.",
        "Does not supply Lambda-CDM metrics.",
        "Does not compute delta chi-square.",
        "Does not compute delta AIC.",
        "Does not compute delta BIC.",
        "Does not execute holdout evaluation.",
        "Does not produce empirical evidence.",
        "Does not prove DFM.",
        "Does not disprove Lambda-CDM.",
        "Does not replace CDM.",
        "Does not claim final cosmology closure.",
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
