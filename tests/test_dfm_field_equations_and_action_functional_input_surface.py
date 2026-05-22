import json
import subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
ARTIFACT = ROOT / "artifacts/repo_intake/dfm_field_equations_and_action_functional_input_surface_2026_05_21.json"
VERIFIER = ROOT / "tools/verify_dfm_field_equations_and_action_functional_input_surface.py"

def load():
    return json.loads(ARTIFACT.read_text())

def test_status_and_required_object():
    data = load()
    assert data["status"] == "INPUT_SURFACE_ONLY_OBJECT_NOT_SUPPLIED"
    assert data["claim_level"] == "schema_only"
    assert data["required_object"] == "DFM_FIELD_EQUATIONS_AND_ACTION_FUNCTIONAL"
    assert data["root_blocker"] == "DFM_FIELD_EQUATIONS_AND_ACTION_FUNCTIONAL_NOT_SUPPLIED"
    assert data["next_missing_object"] == "SUPPLIED_DFM_FIELD_EQUATIONS_AND_ACTION_FUNCTIONAL"

def test_required_sections_exist():
    sections = set(load()["required_sections"])
    assert "primitive_fields" in sections
    assert "geometry_assumptions" in sections
    assert "action_functional" in sections
    assert "variation_variables" in sections
    assert "euler_lagrange_derivation" in sections
    assert "field_equations" in sections
    assert "source_terms" in sections
    assert "matter_coupling_rule" in sections
    assert "boundary_conditions" in sections
    assert "parameter_definitions" in sections
    assert "observable_map_hooks" in sections
    assert "no_post_hoc_freeze_statement" in sections

def test_object_is_not_supplied():
    data = load()
    assert data["object_supplied"] is False
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
