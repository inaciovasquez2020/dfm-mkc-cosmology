from pathlib import Path
import json

ROOT = Path(__file__).resolve().parents[1]

def load_artifact():
    return json.loads(
        (ROOT / "artifacts/repo_intake/filled_closed_dfm_field_equations_action_functional_2026_05_22.json").read_text()
    )

def test_filled_closed_dfm_core_status_and_model():
    data = load_artifact()
    assert data["id"] == "FILLED_CLOSED_DFM_FIELD_EQUATIONS_OR_ACTION_FUNCTIONAL"
    assert data["status"] == "SUPPLIED_CANDIDATE_DYNAMICAL_CORE_ONLY_NO_VALIDATION"
    assert data["model_name"] == "MINIMAL_INTERACTING_SCALAR_DFM_CORE_V1"

def test_filled_closed_dfm_core_sections_present():
    data = load_artifact()
    for key in [
        "primitive_fields",
        "action_functional",
        "closed_equations",
        "flrw_reduction",
        "parameters",
        "observable_prediction_map",
        "lambda_cdm_embedding",
    ]:
        assert key in data
    assert len(data["parameters"]) == 9
    assert data["observable_prediction_map"]["likelihood"] == "logL(theta)=-(1/2)chi2_total(theta)"

def test_filled_closed_dfm_core_boundaries():
    data = load_artifact()
    for boundary in [
        "DFM-MKC validation",
        "Lambda-CDM failure",
        "dark matter resolution",
        "dark energy resolution",
        "gravity closure",
        "empirical validation",
        "P vs NP",
        "any Clay problem",
    ]:
        assert boundary in data["does_not_prove"]

def test_filled_closed_dfm_status_doc():
    doc = (ROOT / "docs/status/FILLED_CLOSED_DFM_FIELD_EQUATIONS_OR_ACTION_FUNCTIONAL_2026_05_22.md").read_text()
    for phrase in [
        "SUPPLIED_CANDIDATE_DYNAMICAL_CORE_ONLY_NO_VALIDATION",
        "MINIMAL_INTERACTING_SCALAR_DFM_CORE_V1",
        "A(Phi)=exp(beta Phi/M_Pl)",
        "Lambda-CDM embedding",
        "COMPLETE_DFM_PARAMETER_PRIOR_AND_NUMERICAL_SOLVER_INTERFACE",
        "DFM-MKC validation",
        "any Clay problem",
    ]:
        assert phrase in doc
