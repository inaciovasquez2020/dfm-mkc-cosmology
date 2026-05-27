import json
from pathlib import Path

ART = Path("artifacts/repo_intake/dark_matter_replacement_validation_toolkit_2026_05_27.json")
DOC = Path("docs/status/DARK_MATTER_REPLACEMENT_VALIDATION_TOOLKIT_2026_05_27.md")

def data():
    return json.loads(ART.read_text())

def test_status_is_toolkit_only_not_validation_claim():
    assert data()["status"] == "VALIDATION_TOOLKIT_ONLY_NOT_EXPERIMENTALLY_VALIDATED"

def test_required_dark_matter_observables_are_present():
    observables = set(data()["required_observables"])
    assert "galaxy_rotation_curves" in observables
    assert "bullet_cluster_type_separation" in observables
    assert "cmb_tt_te_ee_spectra" in observables
    assert "bao_distance_ladder" in observables
    assert "matter_power_spectrum" in observables
    assert "cosmic_shear" in observables

def test_required_closed_objects_are_present():
    objects = set(data()["required_closed_objects"])
    assert "closed_action_functional_or_field_equations" in objects
    assert "matter_coupling_rule" in objects
    assert "linear_perturbation_system" in objects
    assert "prediction_vector_generator" in objects
    assert "likelihood_rule" in objects
    assert "blind_forecast_protocol" in objects

def test_boundary_blocks_overclaim():
    blocked = set(data()["does_not_prove"])
    assert "DFM-MKC empirical validation" in blocked
    assert "Lambda-CDM failure" in blocked
    assert "dark matter replacement" in blocked
    assert "dark matter is liquid" in blocked
    assert "dark matter is solid" in blocked
    assert "dark matter is a phase" in blocked
    assert "any Clay problem" in blocked

def test_next_admissible_objects_are_concrete():
    nxt = set(data()["next_admissible_objects"])
    assert "DFM_MKC_CLOSED_ACTION_FUNCTIONAL_V1" in nxt
    assert "DFM_MKC_FIELD_EQUATIONS_V1" in nxt
    assert "DFM_MKC_MATTER_COUPLING_RULE_V1" in nxt
    assert "DFM_MKC_LINEAR_PERTURBATION_SYSTEM_V1" in nxt
    assert "DFM_MKC_ACT_PLANCK_DESI_PREDICTION_VECTOR_V1" in nxt

def test_status_doc_contains_boundary_and_victory_condition():
    text = DOC.read_text()
    assert "Minimum victory condition" in text
    assert "Does not prove" in text
    assert "DFM-MKC empirical validation" in text
    assert "Lambda-CDM failure" in text
    assert "Dark matter replacement" in text or "dark matter replacement" in text
