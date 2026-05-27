import json
from pathlib import Path

ART = Path("artifacts/repo_intake/dfm_mkc_executable_solver_implementation_v1_2026_05_27.json")
DOC = Path("docs/status/DFM_MKC_EXECUTABLE_SOLVER_IMPLEMENTATION_V1_2026_05_27.md")

def data(): return json.loads(ART.read_text())

def test_executable_solver_contract_status(): assert data()["id"] == "DFM_MKC_EXECUTABLE_SOLVER_IMPLEMENTATION_V1"; assert data()["status"] == "EXECUTABLE_SOLVER_IMPLEMENTATION_CONTRACT_SUPPLIED_NO_NUMERICAL_RUN"; assert "DFM_MKC_NUMERICAL_BOLTZMANN_SOLVER_V1" in data()["source_dependencies"]
def test_implementation_units_and_entrypoints_declared(): blob = json.dumps(data(), sort_keys=True); assert "background_solver_module" in blob; assert "perturbation_solver_module" in blob; assert "constraint_monitor_module" in blob; assert "dfm_mkc_run_prediction_vector(config_path)" in blob
def test_required_schemas_declared(): blob = json.dumps(data(), sort_keys=True); assert "T_Psi(k, eta)" in blob; assert "C_ell_TT_ACT" in blob; assert "D_M_over_r_d" in blob; assert "P_k_linear" in blob; assert "sigma8" in blob; assert "constraint_residuals" in blob
def test_executable_solver_acceptance_blocks_claims(): acceptance = data()["acceptance_test_result"]; assert acceptance["implementation_units_present"] is True; assert acceptance["entrypoints_present"] is True; assert acceptance["input_schema_present"] is True; assert acceptance["output_schema_present"] is True; assert acceptance["production_code_supplied"] is False; assert acceptance["numerical_integration_run"] is False; assert acceptance["prediction_vector_computed"] is False; assert acceptance["empirical_status_promoted"] is False
def test_executable_solver_boundaries(): blocked = set(data()["does_not_prove"]); assert "DFM-MKC production solver code" in blocked; assert "DFM-MKC numerical integration run" in blocked; assert "DFM-MKC empirical validation" in blocked; assert "Lambda-CDM failure" in blocked; assert "dark matter replacement" in blocked; assert "any Clay problem" in blocked
def test_executable_solver_doc(): text = DOC.read_text(); assert "DFM_MKC_EXECUTABLE_SOLVER_IMPLEMENTATION_V1" in text; assert "EXECUTABLE_SOLVER_IMPLEMENTATION_CONTRACT_SUPPLIED_NO_NUMERICAL_RUN" in text; assert "Does not prove" in text
