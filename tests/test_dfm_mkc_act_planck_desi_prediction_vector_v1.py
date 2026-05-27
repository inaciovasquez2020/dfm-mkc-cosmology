import json
from pathlib import Path

ART = Path("artifacts/repo_intake/dfm_mkc_act_planck_desi_prediction_vector_v1_2026_05_27.json")
DOC = Path("docs/status/DFM_MKC_ACT_PLANCK_DESI_PREDICTION_VECTOR_V1_2026_05_27.md")


def data():
    return json.loads(ART.read_text())


def test_prediction_vector_interface_status():
    assert data()["id"] == "DFM_MKC_ACT_PLANCK_DESI_PREDICTION_VECTOR_V1"
    assert data()["status"] == "PREDICTION_VECTOR_INTERFACE_SUPPLIED_NO_NUMERICAL_EVALUATION"
    assert "DFM_MKC_LINEAR_PERTURBATION_SYSTEM_V1" in data()["source_dependencies"]


def test_prediction_slots_declared():
    slots = data()["prediction_vector_slots"]
    assert "C_ell_TT_ACT" in slots["act_dr6_cmb"]
    assert "C_ell_TT_Planck" in slots["planck_cmb"]
    assert "D_M_over_r_d" in slots["desi_bao"]
    assert "P_k_linear" in slots["matter_power"]
    assert "C_ell_shear" in slots["weak_lensing"]


def test_prediction_acceptance_blocks_empirical_promotion():
    acceptance = data()["acceptance_test_result"]
    assert acceptance["act_slots_present"] is True
    assert acceptance["planck_slots_present"] is True
    assert acceptance["desi_slots_present"] is True
    assert acceptance["numerical_prediction_vector_supplied"] is False
    assert acceptance["likelihood_supplied"] is False
    assert acceptance["empirical_status_promoted"] is False


def test_prediction_boundaries():
    blocked = set(data()["does_not_prove"])
    assert "DFM-MKC numerical prediction vector" in blocked
    assert "DFM-MKC empirical validation" in blocked
    assert "Lambda-CDM failure" in blocked
    assert "dark matter replacement" in blocked
    assert "Boltzmann solver implementation" in blocked
    assert "any Clay problem" in blocked


def test_prediction_doc():
    text = DOC.read_text()
    assert "DFM_MKC_ACT_PLANCK_DESI_PREDICTION_VECTOR_V1" in text
    assert "PREDICTION_VECTOR_INTERFACE_SUPPLIED_NO_NUMERICAL_EVALUATION" in text
    assert "Does not prove" in text
