import json
import subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
ARTIFACT = ROOT / "artifacts/repo_intake/dfm_mkc_empirical_evidence_claim_blocker_2026_05_21.json"
VERIFIER = ROOT / "tools/verify_dfm_mkc_empirical_evidence_claim_blocker.py"

def test_blocker_is_not_evidence():
    data = json.loads(ARTIFACT.read_text())
    assert data["status"] == "EMPIRICAL_EVIDENCE_CLAIM_BLOCKED_NO_EXECUTED_COMPARISON"
    assert data["claim_level"] == "blocker_certificate_only"
    assert data["empirical_evidence_claim_admissible"] is False
    assert data["empirical_evidence_supplied"] is False
    assert data["comparison_executed"] is False
    assert data["holdout_evaluation_executed"] is False
    assert data["independent_validation_supplied"] is False

def test_blocking_missing_objects_are_present():
    data = json.loads(ARTIFACT.read_text())
    missing = set(data["blocking_missing_objects"])
    assert "DFM_FIELD_EQUATIONS_OR_ACTION_FUNCTIONAL" in missing
    assert "DFM_PARAMETER_MAP" in missing
    assert "DFM_OBSERVABLE_PREDICTION_RULES" in missing
    assert "DFM_FROZEN_PREDICTION_VECTOR" in missing
    assert "DFM_LIKELIHOOD_RULE" in missing
    assert "DFM_HOLDOUT_SPLIT" in missing
    assert "DFM_VS_LAMBDA_CDM_COMPARISON" in missing
    assert "INDEPENDENT_VALIDATION" in missing

def test_blocked_claims_are_explicit():
    data = json.loads(ARTIFACT.read_text())
    claims = {item["claim"]: item["status"] for item in data["blocked_claims"]}
    assert claims["DFM has empirical evidence"] == "blocked"
    assert claims["DFM beats Lambda-CDM"] == "blocked"
    assert claims["Lambda-CDM is empirically disproved"] == "blocked"
    assert claims["CDM is replaced by DFM"] == "blocked"
    assert claims["DFM gives final cosmology closure"] == "blocked"

def test_minimum_unblock_conditions_include_metrics_and_validation():
    data = json.loads(ARTIFACT.read_text())
    conditions = "\n".join(data["minimum_unblock_conditions"])
    assert "execute DFM-vs-Lambda-CDM comparison" in conditions
    assert "report DFM and Lambda-CDM metrics" in conditions
    assert "report delta chi-square, delta AIC, and delta BIC" in conditions
    assert "execute independent validation or reproduction" in conditions

def test_boundary_forbids_overclaiming():
    data = json.loads(ARTIFACT.read_text())
    boundary = "\n".join(data["boundary"])
    for token in [
        "Does not supply empirical evidence.",
        "Does not execute DFM-vs-Lambda-CDM comparison.",
        "Does not execute holdout evaluation.",
        "Does not supply independent validation.",
        "Does not supply DFM metrics.",
        "Does not supply Lambda-CDM metrics.",
        "Does not compute delta chi-square.",
        "Does not compute delta AIC.",
        "Does not compute delta BIC.",
        "Does not prove DFM.",
        "Does not disprove Lambda-CDM.",
        "Does not replace CDM.",
        "Does not claim final cosmology closure.",
    ]:
        assert token in boundary

def test_does_not_prove_list_contains_major_claims():
    data = json.loads(ARTIFACT.read_text())
    does_not_prove = set(data["does_not_prove"])
    assert "DFM" in does_not_prove
    assert "Lambda-CDM failure" in does_not_prove
    assert "CDM replacement" in does_not_prove
    assert "final cosmology closure" in does_not_prove
    assert "any Clay problem" in does_not_prove

def test_verifier_passes():
    result = subprocess.run(
        ["python3", str(VERIFIER)],
        cwd=ROOT,
        check=True,
        text=True,
        capture_output=True,
    )
    assert "verification OK" in result.stdout
