#!/usr/bin/env python3
import json
from pathlib import Path

ART = Path("artifacts/repo_intake/dfm_mkc_trusted_external_solver_binding_v1_2026_05_27.json")
DOC = Path("docs/status/DFM_MKC_TRUSTED_EXTERNAL_SOLVER_BINDING_V1_2026_05_27.md")
SOURCE_SOLVER = Path("artifacts/repo_intake/dfm_mkc_numerical_boltzmann_solver_v1_2026_05_27.json")
SOURCE_EXEC = Path("artifacts/repo_intake/dfm_mkc_executable_solver_implementation_v1_2026_05_27.json")

REQUIRED_BOUNDARIES = {
    "DFM-MKC external solver adapter implementation",
    "DFM-MKC trusted external solver execution",
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
assert SOURCE_SOLVER.exists(), f"missing source solver artifact: {SOURCE_SOLVER}"
assert SOURCE_EXEC.exists(), f"missing source executable artifact: {SOURCE_EXEC}"

data = json.loads(ART.read_text())
assert data["id"] == "DFM_MKC_TRUSTED_EXTERNAL_SOLVER_BINDING_V1"
assert data["status"] == "TRUSTED_EXTERNAL_SOLVER_BINDING_CONTRACT_SUPPLIED_NO_EXTERNAL_RUN"

blob = json.dumps(data, sort_keys=True)
for term in ["CLASS-compatible external binding", "CAMB-compatible external binding", "custom first-party DFM-MKC solver", "source_code_commit", "environment_lock", "input_schema", "output_schema", "observable_ordering", "covariance_alignment", "reproducibility_hashes", "dfm_mkc_background_adapter", "dfm_mkc_perturbation_adapter", "schema_gate", "hash_gate", "diagnostic_gate"]: assert term in blob, f"missing term: {term}"

acceptance = data["acceptance_test_result"]
for key in ["source_dependencies_present", "allowed_external_targets_present", "binding_contract_present", "adapter_requirements_present", "trust_gates_present"]: assert acceptance.get(key) is True, f"acceptance flag not true: {key}"
for key in ["external_solver_selected", "external_solver_executed", "adapter_implemented", "numerical_prediction_vector_computed", "likelihood_run_supplied", "data_comparison_run_supplied", "empirical_status_promoted"]: assert acceptance.get(key) is False, f"acceptance flag not false: {key}"

missing = REQUIRED_BOUNDARIES - set(data["does_not_prove"])
assert not missing, f"missing boundaries: {sorted(missing)}"

text = DOC.read_text()
for term in ["DFM_MKC_TRUSTED_EXTERNAL_SOLVER_BINDING_V1", "TRUSTED_EXTERNAL_SOLVER_BINDING_CONTRACT_SUPPLIED_NO_EXTERNAL_RUN", "Does not prove", "DFM-MKC empirical validation", "Lambda-CDM failure", "any Clay problem"]: assert term in text, f"doc missing term: {term}"

print("DFM_MKC_TRUSTED_EXTERNAL_SOLVER_BINDING_V1_OK")
print(json.dumps({"status": data["status"], "object": data["id"], "downstream_objects_still_required": data["downstream_objects_still_required"], "next_admissible_step": data["next_admissible_step"]}, indent=2))
