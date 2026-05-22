import json
import subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
ARTIFACT = ROOT / "artifacts/repo_intake/dfm_mkc_remaining_structure_actions_registry_2026_05_21.json"
VERIFIER = ROOT / "tools/verify_dfm_mkc_remaining_structure_actions_registry.py"

def load():
    return json.loads(ARTIFACT.read_text())

def test_registry_surface():
    data = load()
    assert data["status"] == "REMAINING_STRUCTURE_ACTIONS_REGISTRY_ONLY"
    assert data["claim_level"] == "registry_only"
    assert data["phase_count"] == 16
    assert data["action_count"] >= 100
    assert data["likelihood_executed"] is False
    assert data["empirical_evidence_supplied"] is False
    assert data["dfm_proved"] is False
    assert data["lambda_cdm_disproved"] is False

def test_required_actions_exist():
    actions = {item["name"] for phase in load()["phases"] for item in phase["actions"]}
    assert "DFM_MKC_TERMINAL_BLOCKER_EXHAUSTION_CERTIFICATE" in actions
    assert "PLANCK_2018_CMB_SOURCE_POINTER" in actions
    assert "DFM_FIELD_EQUATIONS_SUPPLIED_TARGET" in actions
    assert "DFM_LIKELIHOOD_EXECUTION_TARGET" in actions
    assert "INDEPENDENT_REPRODUCTION_TARGET" in actions
    assert "FINAL_COSMOLOGY_CLOSURE_DECISION_LOCK" in actions

def test_verifier_passes():
    result = subprocess.run(
        ["python3", str(VERIFIER)],
        cwd=ROOT,
        check=True,
        text=True,
        capture_output=True,
    )
    assert "verification OK" in result.stdout
