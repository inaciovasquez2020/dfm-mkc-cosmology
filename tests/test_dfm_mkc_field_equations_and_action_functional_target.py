import json
import subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
ARTIFACT = ROOT / "artifacts/repo_intake/dfm_mkc_field_equations_and_action_functional_target_2026_05_21.json"
VERIFIER = ROOT / "tools/verify_dfm_mkc_field_equations_and_action_functional_target.py"

def load():
    return json.loads(ARTIFACT.read_text())

def test_target_status_and_blocker():
    data = load()
    assert data["status"] == "FIELD_EQUATIONS_AND_ACTION_FUNCTIONAL_TARGET_ONLY_NOT_SUPPLIED"
    assert data["claim_level"] == "target_only"
    assert data["root_blocker"] == "DFM_FIELD_EQUATIONS_AND_ACTION_FUNCTIONAL_NOT_SUPPLIED"
    assert data["required_object"] == "DFM_FIELD_EQUATIONS_AND_ACTION_FUNCTIONAL"

def test_required_components_exist():
    required = set(load()["requires"])
    assert "DFM_FIELD_EQUATIONS_SUPPLIED" in required
    assert "DFM_ACTION_FUNCTIONAL_SUPPLIED" in required
    assert "DFM_VARIATIONAL_DERIVATION_MAP" in required
    assert "DFM_EULER_LAGRANGE_CONSISTENCY_CHECK" in required
    assert "DFM_SOURCE_TERMS_SUPPLIED" in required
    assert "DFM_MATTER_COUPLING_RULE_SUPPLIED" in required
    assert "DFM_BOUNDARY_CONDITIONS_SUPPLIED" in required

def test_no_claim_is_promoted():
    data = load()
    assert data["supplied"] is False
    assert data["field_equations_supplied"] is False
    assert data["action_functional_supplied"] is False
    assert data["variational_derivation_supplied"] is False
    assert data["prediction_map_supplied"] is False
    assert data["likelihood_executed"] is False
    assert data["empirical_evidence_supplied"] is False

def test_boundary_forbids_overclaiming():
    boundary = "\n".join(load()["boundary"])
    for token in [
        "Does not supply DFM field equations.",
        "Does not supply DFM action functional.",
        "Does not supply variational derivation.",
        "Does not supply Euler-Lagrange consistency proof.",
        "Does not supply DFM prediction map.",
        "Does not execute any likelihood.",
        "Does not produce empirical evidence.",
        "Does not prove DFM.",
        "Does not disprove Lambda-CDM.",
        "Does not replace CDM.",
        "Does not claim final cosmology closure."
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
