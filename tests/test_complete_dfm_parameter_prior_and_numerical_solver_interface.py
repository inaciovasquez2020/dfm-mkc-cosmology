from pathlib import Path
import json

ROOT = Path(__file__).resolve().parents[1]

def load_artifact():
    return json.loads(
        (ROOT / "artifacts/repo_intake/complete_dfm_parameter_prior_and_numerical_solver_interface_2026_05_22.json").read_text()
    )

def test_complete_dfm_solver_interface_status():
    data = load_artifact()
    assert data["id"] == "COMPLETE_DFM_PARAMETER_PRIOR_AND_NUMERICAL_SOLVER_INTERFACE"
    assert data["status"] == "SOLVER_INTERFACE_ONLY_NO_EXECUTED_VALIDATION"
    assert data["next_admissible_object"] == "EXECUTABLE_DFM_BACKGROUND_SOLVER_WITH_SYNTHETIC_SANITY_CHECK"

def test_complete_dfm_parameter_vector():
    data = load_artifact()
    symbols = {row["symbol"] for row in data["parameter_vector"]}
    assert symbols == {
        "H0",
        "Omega_b0",
        "Omega_c0",
        "Omega_r0",
        "V0",
        "lambda",
        "beta",
        "Phi_i",
        "dot_Phi_i",
    }

def test_complete_dfm_solver_and_observable_interface():
    data = load_artifact()
    assert data["solver_interface"]["independent_variable"] == "N=ln(a)"
    assert "lambda_cdm_limit" in data["solver_interface"]
    assert "H(z)" in data["observable_interface"]["background_outputs"]
    assert "D_M(z)/r_d" in data["observable_interface"]["bao_outputs"]
    assert "ell_A" in data["observable_interface"]["cmb_act_compressed_outputs"]
    assert "mu(z)" in data["observable_interface"]["sne_des_outputs"]
    assert data["observable_interface"]["likelihood_rule"] == "logL(theta)=-(1/2)chi2_total(theta)"

def test_complete_dfm_solver_boundaries():
    data = load_artifact()
    for boundary in [
        "DFM-MKC validation",
        "Lambda-CDM failure",
        "dark matter resolution",
        "dark energy resolution",
        "gravity closure",
        "empirical validation",
        "ACT validation",
        "DESI validation",
        "DES validation",
        "P vs NP",
        "any Clay problem",
    ]:
        assert boundary in data["does_not_prove"]

def test_complete_dfm_solver_status_doc_and_spec():
    doc = (ROOT / "docs/status/COMPLETE_DFM_PARAMETER_PRIOR_AND_NUMERICAL_SOLVER_INTERFACE_2026_05_22.md").read_text()
    spec = (ROOT / "specs/COMPLETE_DFM_PARAMETER_PRIOR_AND_NUMERICAL_SOLVER_INTERFACE.md").read_text()
    for phrase in [
        "SOLVER_INTERFACE_ONLY_NO_EXECUTED_VALIDATION",
        "MINIMAL_INTERACTING_SCALAR_DFM_CORE_V1",
        "EXECUTABLE_DFM_BACKGROUND_SOLVER_WITH_SYNTHETIC_SANITY_CHECK",
        "DFM-MKC validation",
        "any Clay problem",
    ]:
        assert phrase in doc + spec
