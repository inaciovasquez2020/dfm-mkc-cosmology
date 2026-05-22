import json
import subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
ARTIFACT = ROOT / "artifacts/repo_intake/supplied_dfm_field_equations_and_action_functional_intake_2026_05_21.json"
INTAKE = ROOT / "specs/SUPPLIED_DFM_FIELD_EQUATIONS_AND_ACTION_FUNCTIONAL.INTAKE.md"
VERIFIER = ROOT / "tools/verify_supplied_dfm_field_equations_and_action_functional_intake.py"

def load():
    return json.loads(ARTIFACT.read_text())

def test_status_and_required_object():
    data = load()
    assert data["status"] == "SUPPLIED_OBJECT_INTAKE_SURFACE_ONLY_OBJECT_NOT_FILLED"
    assert data["claim_level"] == "intake_surface_only"
    assert data["required_object"] == "SUPPLIED_DFM_FIELD_EQUATIONS_AND_ACTION_FUNCTIONAL"
    assert data["root_blocker"] == "SUPPLIED_DFM_FIELD_EQUATIONS_AND_ACTION_FUNCTIONAL_NOT_FILLED"
    assert data["next_missing_object"] == "FILLED_SUPPLIED_DFM_FIELD_EQUATIONS_AND_ACTION_FUNCTIONAL"

def test_required_sections_exist_in_intake_template():
    text = INTAKE.read_text()
    for section in load()["required_sections"]:
        assert f"### {section}" in text
    assert "TBD" in text

def test_object_is_not_filled_or_promoted():
    data = load()
    assert data["object_filled"] is False
    assert data["all_tbd_replaced"] is False
    assert data["field_equations_supplied"] is False
    assert data["action_functional_supplied"] is False
    assert data["variational_derivation_supplied"] is False
    assert data["prediction_map_supplied"] is False
    assert data["likelihood_executed"] is False
    assert data["empirical_evidence_supplied"] is False

def test_boundary_forbids_overclaiming():
    boundary = "\n".join(load()["boundary"])
    for token in [
        "Does not supply final DFM field equations.",
        "Does not supply final DFM action functional.",
        "Does not supply final variational derivation.",
        "Does not supply final Euler-Lagrange consistency proof.",
        "Does not supply final DFM prediction map.",
        "Does not execute any likelihood.",
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
