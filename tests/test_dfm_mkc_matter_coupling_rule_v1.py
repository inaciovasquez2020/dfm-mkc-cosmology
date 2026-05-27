import json
from pathlib import Path

ART = Path("artifacts/repo_intake/dfm_mkc_matter_coupling_rule_v1_2026_05_27.json")
DOC = Path("docs/status/DFM_MKC_MATTER_COUPLING_RULE_V1_2026_05_27.md")
SOURCE = Path("artifacts/repo_intake/dfm_mkc_field_equations_v1_2026_05_27.json")

def data():
    return json.loads(ART.read_text())

def test_status_supplies_matter_coupling_only():
    assert data()["id"] == "DFM_MKC_MATTER_COUPLING_RULE_V1"
    assert data()["status"] == "CONCRETE_MATTER_COUPLING_RULE_SUPPLIED_PHENOMENOLOGICAL_ONLY"
    assert data()["source_dependency"] == "DFM_MKC_FIELD_EQUATIONS_V1"
    assert SOURCE.exists()

def test_metric_only_coupling_blocks_direct_dark_visible_terms():
    principle = data()["coupling_principle"]
    assert "metric" in principle["statement"].lower()
    assert principle["direct_phi_visible_coupling"] is False
    assert principle["direct_theta_visible_coupling"] is False
    assert principle["dataset_tuned_couplings_allowed"] is False

def test_ordinary_matter_coupling_is_present():
    ordinary = "\n".join(str(v) for v in data()["ordinary_matter_coupling"].values())
    assert "S_vis" in ordinary
    assert "L_vis(psi_vis, g)" in ordinary
    assert "T_vis_{mu nu}" in ordinary
    assert "u^mu nabla_mu u^nu = 0" in ordinary

def test_photon_coupling_and_lensing_rule_are_present():
    photon = "\n".join(str(v) for v in data()["photon_coupling"].values())
    lensing = "\n".join(str(v) for v in data()["lensing_prediction_rule"].values())
    assert "S_EM" in photon
    assert "F_{mu nu}" in photon
    assert "k^mu k_mu = 0" in photon
    assert "k^mu nabla_mu k^nu = 0" in photon
    assert "null geodesics" in lensing.lower()
    assert data()["photon_coupling"]["direct_phi_photon_coupling"] is False
    assert data()["photon_coupling"]["direct_theta_photon_coupling"] is False

def test_stress_energy_exchange_rule_sets_zero_direct_exchange():
    exchange = data()["stress_energy_exchange_rule"]
    exchange_text = "\n".join(str(v) for v in exchange.values())
    assert "T_vis_{mu nu}" in exchange_text
    assert "T_DFM_MKC_{mu nu}" in exchange_text
    assert exchange["direct_exchange_current"] == "Q_nu = 0 in V1"

def test_acceptance_flags_are_locked():
    acceptance = data()["acceptance_test_result"]
    assert acceptance["target"] == "DFM_MKC_MATTER_COUPLING_RULE_V1"
    assert acceptance["ordinary_matter_coupling_present"] is True
    assert acceptance["photon_coupling_present"] is True
    assert acceptance["lensing_prediction_rule_present"] is True
    assert acceptance["direct_visible_dark_couplings_introduced"] is False
    assert acceptance["dataset_tuned_couplings_introduced"] is False
    assert acceptance["empirical_status_promoted"] is False

def test_downstream_pipeline_targets_remain_locked():
    targets = {target["id"]: target["status"] for target in data()["downstream_pipeline_targets"]}
    assert targets["DFM_MKC_LINEAR_PERTURBATION_SYSTEM_V1"] == "DOWNSTREAM_TARGET_NOT_SUPPLIED"
    assert targets["DFM_MKC_ACT_PLANCK_DESI_PREDICTION_VECTOR_V1"] == "DOWNSTREAM_TARGET_NOT_SUPPLIED"
    assert targets["DFM_MKC_DATA_COMPARISON_PROTOCOL_V1"] == "DOWNSTREAM_TARGET_NOT_SUPPLIED"

def test_boundary_blocks_overclaim():
    blocked = set(data()["does_not_prove"])
    assert "DFM-MKC linear perturbation system" in blocked
    assert "DFM-MKC ACT Planck DESI prediction vector" in blocked
    assert "DFM-MKC data comparison" in blocked
    assert "DFM-MKC empirical validation" in blocked
    assert "Lambda-CDM failure" in blocked
    assert "dark matter replacement" in blocked
    assert "galaxy rotation curve fit" in blocked
    assert "CMB fit" in blocked
    assert "BAO fit" in blocked
    assert "Bullet Cluster explanation" in blocked
    assert "any Clay problem" in blocked

def test_status_doc_contains_coupling_rule_and_boundaries():
    text = DOC.read_text()
    assert "DFM_MKC_MATTER_COUPLING_RULE_V1" in text
    assert "Visible matter and photons couple to the spacetime metric" in text
    assert "S_vis" in text
    assert "S_EM" in text
    assert "Q_nu = 0" in text
    assert "Does not prove" in text
    assert "DFM_MKC_LINEAR_PERTURBATION_SYSTEM_V1" in text
    assert "DFM_MKC_ACT_PLANCK_DESI_PREDICTION_VECTOR_V1" in text
    assert "DFM_MKC_DATA_COMPARISON_PROTOCOL_V1" in text
