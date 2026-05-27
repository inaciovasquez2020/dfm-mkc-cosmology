import json
from pathlib import Path

ART = Path("artifacts/repo_intake/dfm_mkc_linear_perturbation_system_v1_2026_05_27.json")
DOC = Path("docs/status/DFM_MKC_LINEAR_PERTURBATION_SYSTEM_V1_2026_05_27.md")
SOURCE_FIELD = Path("artifacts/repo_intake/dfm_mkc_field_equations_v1_2026_05_27.json")
SOURCE_COUPLING = Path("artifacts/repo_intake/dfm_mkc_matter_coupling_rule_v1_2026_05_27.json")


def data():
    return json.loads(ART.read_text())


def test_status_supplies_linear_perturbation_system_only():
    assert data()["id"] == "DFM_MKC_LINEAR_PERTURBATION_SYSTEM_V1"
    assert data()["status"] == "CONCRETE_LINEAR_PERTURBATION_SYSTEM_SUPPLIED_PHENOMENOLOGICAL_ONLY"
    assert "DFM_MKC_FIELD_EQUATIONS_V1" in data()["source_dependencies"]
    assert "DFM_MKC_MATTER_COUPLING_RULE_V1" in data()["source_dependencies"]
    assert SOURCE_FIELD.exists()
    assert SOURCE_COUPLING.exists()


def test_background_and_gauge_are_present():
    background = "\n".join(str(v) for v in data()["background_solution"].values())
    gauge = "\n".join(str(v) for v in data()["gauge_choice"].values())
    assert "FLRW" in background
    assert "phi_bar" in background
    assert "theta_bar" in background
    assert "Newtonian gauge" in gauge
    assert "Psi" in gauge
    assert "Phi" in gauge


def test_perturbation_variables_are_present():
    variables = "\n".join(str(v) for v in data()["perturbation_variables"].values())
    assert "delta_phi" in variables
    assert "delta_theta" in variables
    assert "delta_b" in variables
    assert "v_b" in variables
    assert "delta_gamma" in variables
    assert "v_gamma" in variables


def test_linearized_equations_are_present():
    equations = "\n".join(str(v) for v in data()["linearized_equations"].values())
    assert "k^2 Phi" in equations
    assert "alpha[delta_phi_double_prime" in equations
    assert "beta phi_bar^2 delta_theta_prime" in equations
    assert "delta_b_prime" in equations
    assert "v_gamma_prime" in equations


def test_transfer_growth_and_stability_are_present():
    transfers = "\n".join(str(v) for v in data()["transfer_functions"].values())
    growth = "\n".join(str(v) for v in data()["growth_equation"].values())
    stability = data()["stability_conditions"]
    assert "T_Psi" in transfers
    assert "T_delta_phi" in transfers
    assert "S_DFM_MKC" in growth
    assert "alpha > 0" in stability["kinetic_signs"]
    assert "beta > 0" in stability["kinetic_signs"]
    assert stability["full_well_posedness_proved"] is False


def test_observable_mappings_are_deferred():
    cmb = data()["cmb_observable_mapping"]
    matter = data()["matter_power_mapping"]
    assert cmb["no_cmb_fit_claim"] is True
    assert matter["no_matter_power_fit_claim"] is True
    assert "DFM_MKC_ACT_PLANCK_DESI_PREDICTION_VECTOR_V1" in cmb["temperature_source_status"]
    assert "DFM_MKC_ACT_PLANCK_DESI_PREDICTION_VECTOR_V1" in matter["linear_matter_power_status"]


def test_acceptance_flags_are_locked():
    acceptance = data()["acceptance_test_result"]
    assert acceptance["target"] == "DFM_MKC_LINEAR_PERTURBATION_SYSTEM_V1"
    assert acceptance["background_solution_present"] is True
    assert acceptance["linearized_equations_present"] is True
    assert acceptance["transfer_functions_present"] is True
    assert acceptance["prediction_vector_supplied"] is False
    assert acceptance["data_comparison_supplied"] is False
    assert acceptance["empirical_status_promoted"] is False


def test_downstream_objects_remain_required():
    downstream = set(data()["downstream_objects_still_required"])
    assert "DFM_MKC_ACT_PLANCK_DESI_PREDICTION_VECTOR_V1" in downstream
    assert "DFM_MKC_DATA_COMPARISON_PROTOCOL_V1" in downstream


def test_boundary_blocks_overclaim():
    blocked = set(data()["does_not_prove"])
    assert "DFM-MKC ACT Planck DESI prediction vector" in blocked
    assert "DFM-MKC data comparison" in blocked
    assert "DFM-MKC empirical validation" in blocked
    assert "Lambda-CDM failure" in blocked
    assert "dark matter replacement" in blocked
    assert "CMB fit" in blocked
    assert "matter power spectrum fit" in blocked
    assert "Boltzmann solver implementation" in blocked
    assert "any Clay problem" in blocked


def test_status_doc_contains_linear_system_and_boundaries():
    text = DOC.read_text()
    assert "DFM_MKC_LINEAR_PERTURBATION_SYSTEM_V1" in text
    assert "Newtonian gauge" in text
    assert "delta_phi" in text
    assert "delta_theta" in text
    assert "S_DFM_MKC" in text
    assert "Does not prove" in text
    assert "DFM_MKC_ACT_PLANCK_DESI_PREDICTION_VECTOR_V1" in text
    assert "DFM_MKC_DATA_COMPARISON_PROTOCOL_V1" in text
