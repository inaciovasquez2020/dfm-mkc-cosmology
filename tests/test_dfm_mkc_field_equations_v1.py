import json
from pathlib import Path

ART = Path("artifacts/repo_intake/dfm_mkc_field_equations_v1_2026_05_27.json")
DOC = Path("docs/status/DFM_MKC_FIELD_EQUATIONS_V1_2026_05_27.md")
SOURCE = Path("artifacts/repo_intake/dfm_mkc_closed_action_functional_v1_2026_05_27.json")

def data():
    return json.loads(ART.read_text())

def test_status_supplies_field_equations_only():
    assert data()["id"] == "DFM_MKC_FIELD_EQUATIONS_V1"
    assert data()["status"] == "CONCRETE_FIELD_EQUATIONS_DERIVED_PHENOMENOLOGICAL_ONLY"
    assert data()["source_dependency"] == "DFM_MKC_CLOSED_ACTION_FUNCTIONAL_V1"
    assert SOURCE.exists()

def test_metric_equation_contains_einstein_and_stress_energy_terms():
    metric = "\n".join(str(v) for v in data()["metric_equation"].values())
    assert "G_{mu nu} + Lambda g_{mu nu}" in metric
    assert "T_vis_{mu nu}" in metric
    assert "T_DFM_MKC_{mu nu}" in metric
    assert data()["metric_equation"]["post_hoc_source_terms_added"] is False

def test_dark_sector_equations_are_present():
    dark = "\n".join(str(v) for v in data()["dark_sector_equations"].values())
    assert "alpha Box_g phi" in dark
    assert "U_prime(phi)" in dark
    assert "nabla_mu(beta phi^2 nabla^mu theta)" in dark
    assert data()["dark_sector_equations"]["post_hoc_force_terms_added"] is False

def test_conservation_and_constraints_are_present():
    constraints = "\n".join(str(v) for v in data()["constraint_equations"].values())
    conservation = "\n".join(str(v) for v in data()["conservation_laws"].values())
    assert "nabla^mu" in constraints
    assert "J_theta" in constraints
    assert "T_vis_{mu nu}" in conservation
    assert "T_DFM_MKC_{mu nu}" in conservation

def test_stress_energy_tensor_contains_all_dark_sector_terms():
    stress = "\n".join(str(v) for v in data()["stress_energy_tensor"].values())
    assert "alpha nabla_mu phi nabla_nu phi" in stress
    assert "beta phi^2 nabla_mu theta nabla_nu theta" in stress
    assert "U(phi)" in stress

def test_derivation_and_acceptance_flags_are_locked():
    derivation = data()["derivation_status"]
    assert derivation["metric_variation_performed"] is True
    assert derivation["phi_variation_performed"] is True
    assert derivation["theta_variation_performed"] is True
    assert derivation["derived_without_post_hoc_terms"] is True
    assert derivation["derived_from_closed_action_functional_v1"] is True

    acceptance = data()["acceptance_test_result"]
    assert acceptance["target"] == "DFM_MKC_FIELD_EQUATIONS_V1"
    assert acceptance["metric_equation_present"] is True
    assert acceptance["dark_sector_equations_present"] is True
    assert acceptance["empirical_status_promoted"] is False

def test_downstream_objects_remain_required():
    downstream = set(data()["downstream_objects_still_required"])
    assert "DFM_MKC_MATTER_COUPLING_RULE_V1" in downstream
    assert "DFM_MKC_LINEAR_PERTURBATION_SYSTEM_V1" in downstream
    assert "DFM_MKC_ACT_PLANCK_DESI_PREDICTION_VECTOR_V1" in downstream

def test_boundary_blocks_overclaim():
    blocked = set(data()["does_not_prove"])
    assert "DFM-MKC matter coupling law" in blocked
    assert "DFM-MKC linear perturbation system" in blocked
    assert "DFM-MKC ACT Planck DESI prediction vector" in blocked
    assert "DFM-MKC empirical validation" in blocked
    assert "Lambda-CDM failure" in blocked
    assert "dark matter replacement" in blocked
    assert "dark matter is a phase" in blocked
    assert "any Clay problem" in blocked

def test_status_doc_contains_equations_and_boundary():
    text = DOC.read_text()
    assert "DFM_MKC_FIELD_EQUATIONS_V1" in text
    assert "G_{mu nu} + Lambda g_{mu nu}" in text
    assert "alpha Box_g phi" in text
    assert "nabla_mu(beta phi^2 nabla^mu theta)" in text
    assert "Does not prove" in text
    assert "DFM_MKC_MATTER_COUPLING_RULE_V1" in text
