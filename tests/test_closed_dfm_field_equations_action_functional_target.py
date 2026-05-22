from pathlib import Path
import json

ROOT = Path(__file__).resolve().parents[1]

def test_closed_dfm_field_equations_action_functional_target():
    data = json.loads(
        (ROOT / "artifacts/repo_intake/closed_dfm_field_equations_action_functional_target_2026_05_22.json").read_text()
    )
    assert data["status"] == "TARGET_ONLY_OBJECT_NOT_SUPPLIED"
    assert data["minimal_missing_object"] == "CLOSED_DFM_FIELD_EQUATIONS_OR_ACTION_FUNCTIONAL"
    assert "prediction map to observables" in data["required_payload"]
    assert "DFM-MKC validation" in data["does_not_prove"]
    assert "any Clay problem" in data["does_not_prove"]

def test_closed_dfm_status_doc_boundaries():
    doc = (ROOT / "docs/status/CLOSED_DFM_FIELD_EQUATIONS_OR_ACTION_FUNCTIONAL_TARGET_2026_05_22.md").read_text()
    for phrase in [
        "TARGET_ONLY_OBJECT_NOT_SUPPLIED",
        "CLOSED_DFM_FIELD_EQUATIONS_OR_ACTION_FUNCTIONAL",
        "primitive fields",
        "dynamical equations or variational action",
        "prediction map to observables",
        "DFM-MKC validation",
        "Lambda-CDM failure",
        "dark matter resolution",
        "dark energy resolution",
        "gravity closure",
        "empirical validation",
        "P vs NP",
        "any Clay problem",
    ]:
        assert phrase in doc
