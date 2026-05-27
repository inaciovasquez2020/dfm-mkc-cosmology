#!/usr/bin/env python3
import json
from pathlib import Path

ART = Path("artifacts/repo_intake/dfm_mkc_executable_solver_implementation_v1_2026_05_27.json")
DOC = Path("docs/status/DFM_MKC_EXECUTABLE_SOLVER_IMPLEMENTATION_V1_2026_05_27.md")

SOURCE_ARTIFACTS = [
    Path("artifacts/repo_intake/dfm_mkc_closed_action_functional_v1_2026_05_27.json"),
    Path("artifacts/repo_intake/dfm_mkc_field_equations_v1_2026_05_27.json"),
    Path("artifacts/repo_intake/dfm_mkc_matter_coupling_rule_v1_2026_05_27.json"),
    Path("artifacts/repo_intake/dfm_mkc_linear_perturbation_system_v1_2026_05_27.json"),
    Path("artifacts/repo_intake/dfm_mkc_act_planck_desi_prediction_vector_v1_2026_05_27.json"),
    Path("artifacts/repo_intake/dfm_mkc_data_comparison_protocol_v1_2026_05_27.json"),
    Path("artifacts/repo_intake/dfm_mkc_numerical_boltzmann_solver_v1_2026_05_27.json"),
]

REQUIRED_BOUNDARIES = {
    "DFM-MKC production solver code",
    "DFM-MKC numerical integration run",
    "DFM-MKC numerical prediction vector",
    "DFM-MKC data comparison run",
    "DFM-MKC likelihood improvement",
    "DFM-MKC empirical validation",
    "Lambda-CDM failure",
    "dark matter replacement",
    "dark matter is liquid",
    "dark matter is solid",
    "dark matter is a phase",
    "CMB fit",
    "ACT fit",
    "Planck fit",
    "DESI fit",
    "BAO fit",
    "weak lensing fit",
    "matter power spectrum fit",
    "gravity closure",
    "Chronos-RR",
    "unrestricted H4.1/FGL",
    "P vs NP",
    "any Clay problem",
}

assert ART.exists(), f"missing artifact: {ART}"
assert DOC.exists(), f"missing doc: {DOC}"
for source in SOURCE_ARTIFACTS: assert source.exists(), f"missing source artifact: {source}"

data = json.loads(ART.read_text())
assert data["id"] == "DFM_MKC_EXECUTABLE_SOLVER_IMPLEMENTATION_V1"
assert data["status"] == "EXECUTABLE_SOLVER_IMPLEMENTATION_CONTRACT_SUPPLIED_NO_NUMERICAL_RUN"

blob = json.dumps(data, sort_keys=True)
for term in ["DFM_MKC_NUMERICAL_BOLTZMANN_SOLVER_V1", "background_solver_module", "perturbation_solver_module", "constraint_monitor_module", "dfm_mkc_run_prediction_vector(config_path)", "T_Psi(k, eta)", "C_ell_TT_ACT", "D_M_over_r_d", "P_k_linear", "sigma8", "constraint_residuals"]: assert term in blob, f"missing term: {term}"

acceptance = data["acceptance_test_result"]
for key in ["source_dependencies_present", "implementation_units_present", "entrypoints_present", "input_schema_present", "output_schema_present", "execution_gates_present"]: assert acceptance.get(key) is True, f"acceptance flag not true: {key}"
for key in ["production_code_supplied", "numerical_integration_run", "prediction_vector_computed", "likelihood_run_supplied", "data_comparison_run_supplied", "empirical_status_promoted"]: assert acceptance.get(key) is False, f"acceptance flag not false: {key}"

missing = REQUIRED_BOUNDARIES - set(data["does_not_prove"])
assert not missing, f"missing boundaries: {sorted(missing)}"

text = DOC.read_text()
for term in ["DFM_MKC_EXECUTABLE_SOLVER_IMPLEMENTATION_V1", "EXECUTABLE_SOLVER_IMPLEMENTATION_CONTRACT_SUPPLIED_NO_NUMERICAL_RUN", "Does not prove", "DFM-MKC empirical validation", "Lambda-CDM failure", "any Clay problem"]: assert term in text, f"doc missing term: {term}"

print("DFM_MKC_EXECUTABLE_SOLVER_IMPLEMENTATION_V1_OK")
print(json.dumps({"status": data["status"], "object": data["id"], "downstream_objects_still_required": data["downstream_objects_still_required"], "next_admissible_step": data["next_admissible_step"]}, indent=2))
