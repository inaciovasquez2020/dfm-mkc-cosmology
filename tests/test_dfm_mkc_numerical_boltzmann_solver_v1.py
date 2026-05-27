import json
from pathlib import Path

ART = Path("artifacts/repo_intake/dfm_mkc_numerical_boltzmann_solver_v1_2026_05_27.json")
DOC = Path("docs/status/DFM_MKC_NUMERICAL_BOLTZMANN_SOLVER_V1_2026_05_27.md")


def data():
    return json.loads(ART.read_text())


def test_solver_interface_status():
    assert data()["id"] == "DFM_MKC_NUMERICAL_BOLTZMANN_SOLVER_V1"
    assert data()["status"] == "SOLVER_INTERFACE_SUPPLIED_NO_NUMERICAL_INTEGRATION"
    assert "DFM_MKC_LINEAR_PERTURBATION_SYSTEM_V1" in data()["source_dependencies"]
    assert "DFM_MKC_ACT_PLANCK_DESI_PREDICTION_VECTOR_V1" in data()["source_dependencies"]
    assert "DFM_MKC_DATA_COMPARISON_PROTOCOL_V1" in data()["source_dependencies"]


def test_solver_inputs_and_outputs_declared():
    blob = json.dumps(data(), sort_keys=True)
    assert "T_Psi(k, eta)" in blob
    assert "T_delta_phi(k, eta)" in blob
    assert "C_ell_TT_ACT" in blob
    assert "C_ell_TT_Planck" in blob
    assert "D_M_over_r_d" in blob
    assert "P_k_linear" in blob
    assert "sigma8" in blob
    assert "constraint_residuals" in blob


def test_numerical_methods_declared_without_execution():
    methods = data()["required_numerical_methods"]
    assert "Adaptive ODE integrator" in methods["time_integrator"]
    assert "Track Einstein constraint residuals" in methods["constraint_monitoring"]
    assert "finite output checks" in methods["stability_checks"]
    assert "grid refinement stability" in methods["stability_checks"]
    assert "no executable solver is supplied" in methods["implementation_status"]


def test_external_solver_binding_option_declared():
    option = data()["external_solver_binding_option"]
    assert option["allowed"] is True
    assert "CLASS-compatible external binding" in option["allowed_targets"]
    assert "CAMB-compatible external binding" in option["allowed_targets"]
    assert "source_code_commit" in option["required_binding_fields"]
    assert "reproducibility_hashes" in option["required_binding_fields"]
    assert "No trusted external solver binding" in option["binding_status"]


def test_acceptance_blocks_numerical_claims():
    acceptance = data()["acceptance_test_result"]
    assert acceptance["solver_inputs_present"] is True
    assert acceptance["equation_blocks_present"] is True
    assert acceptance["required_solver_outputs_present"] is True
    assert acceptance["numerical_integration_supplied"] is False
    assert acceptance["executable_solver_supplied"] is False
    assert acceptance["trusted_external_binding_supplied"] is False
    assert acceptance["prediction_vector_computed"] is False
    assert acceptance["likelihood_run_supplied"] is False
    assert acceptance["empirical_status_promoted"] is False


def test_solver_boundaries():
    blocked = set(data()["does_not_prove"])
    assert "DFM-MKC executable Boltzmann solver" in blocked
    assert "DFM-MKC trusted external solver binding" in blocked
    assert "DFM-MKC numerical prediction vector" in blocked
    assert "DFM-MKC empirical validation" in blocked
    assert "Lambda-CDM failure" in blocked
    assert "dark matter replacement" in blocked
    assert "Boltzmann solver implementation" in blocked
    assert "any Clay problem" in blocked


def test_solver_doc():
    text = DOC.read_text()
    assert "DFM_MKC_NUMERICAL_BOLTZMANN_SOLVER_V1" in text
    assert "SOLVER_INTERFACE_SUPPLIED_NO_NUMERICAL_INTEGRATION" in text
    assert "Does not prove" in text
    assert "DFM-MKC executable Boltzmann solver" in text
