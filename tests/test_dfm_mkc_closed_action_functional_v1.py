import json
from pathlib import Path

ART = Path("artifacts/repo_intake/dfm_mkc_closed_action_functional_v1_2026_05_27.json")
DOC = Path("docs/status/DFM_MKC_CLOSED_ACTION_FUNCTIONAL_V1_2026_05_27.md")

def data():
    return json.loads(ART.read_text())

def test_status_supplies_closed_action_only():
    assert data()["id"] == "DFM_MKC_CLOSED_ACTION_FUNCTIONAL_V1"
    assert data()["status"] == "CONCRETE_ACTION_FUNCTIONAL_SUPPLIED_PHENOMENOLOGICAL_ONLY"
    assert data()["object_type"] == "closed covariant action functional"

def test_required_target_contents_are_present():
    d = data()
    for key in [
        "spacetime_domain",
        "field_inventory",
        "dynamical_variables",
        "action_integral",
        "lagrangian_density",
        "allowed_parameters",
        "variation_rules",
        "boundary_terms",
        "units_and_dimensions",
        "reduction_to_known_limits",
    ]:
        assert key in d
        assert d[key]

def test_action_is_closed_and_forbids_post_hoc_terms():
    action = data()["action_integral"]
    assert action["closed_action"] is True
    assert action["post_hoc_terms_allowed"] is False
    assert "S_GHY" in action["definition"] or "S_GHY" in action["boundary_term"]

def test_lagrangian_contains_gravity_dark_sector_and_visible_terms():
    lag = "\n".join(str(v) for v in data()["lagrangian_density"].values())
    assert "(R - 2 Lambda)/(16 pi G)" in lag
    assert "nabla_mu phi" in lag
    assert "nabla_mu theta" in lag
    assert "U(phi)" in lag
    assert "L_vis(psi_vis, g)" in lag

def test_acceptance_result_is_action_only_not_empirical_promotion():
    acc = data()["acceptance_test_result"]
    assert acc["target"] == "DFM_MKC_CLOSED_ACTION_FUNCTIONAL_V1"
    assert acc["required_contents_present"] is True
    assert acc["closed_variational_principle_present"] is True
    assert acc["field_equations_derivable_without_post_hoc_terms"] is True
    assert acc["empirical_status_promoted"] is False

def test_downstream_objects_remain_required():
    downstream = set(data()["downstream_objects_still_required"])
    assert "DFM_MKC_FIELD_EQUATIONS_V1" in downstream
    assert "DFM_MKC_MATTER_COUPLING_RULE_V1" in downstream
    assert "DFM_MKC_LINEAR_PERTURBATION_SYSTEM_V1" in downstream
    assert "DFM_MKC_ACT_PLANCK_DESI_PREDICTION_VECTOR_V1" in downstream

def test_boundary_blocks_overclaim():
    blocked = set(data()["does_not_prove"])
    assert "DFM-MKC field equations" in blocked
    assert "DFM-MKC matter coupling law" in blocked
    assert "DFM-MKC linear perturbation system" in blocked
    assert "DFM-MKC ACT Planck DESI prediction vector" in blocked
    assert "DFM-MKC empirical validation" in blocked
    assert "Lambda-CDM failure" in blocked
    assert "dark matter replacement" in blocked
    assert "dark matter is a phase" in blocked
    assert "any Clay problem" in blocked

def test_status_doc_contains_action_and_boundary():
    text = DOC.read_text()
    assert "DFM_MKC_CLOSED_ACTION_FUNCTIONAL_V1" in text
    assert "S_DFM_MKC_V1" in text
    assert "L_total" in text
    assert "Does not prove" in text
    assert "Dark matter replacement" in text
    assert "DFM_MKC_FIELD_EQUATIONS_V1" in text
