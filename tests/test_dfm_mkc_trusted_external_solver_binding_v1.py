import json
from pathlib import Path

ART = Path("artifacts/repo_intake/dfm_mkc_trusted_external_solver_binding_v1_2026_05_27.json")
DOC = Path("docs/status/DFM_MKC_TRUSTED_EXTERNAL_SOLVER_BINDING_V1_2026_05_27.md")

def data(): return json.loads(ART.read_text())

def test_trusted_binding_contract_status(): assert data()["id"] == "DFM_MKC_TRUSTED_EXTERNAL_SOLVER_BINDING_V1"; assert data()["status"] == "TRUSTED_EXTERNAL_SOLVER_BINDING_CONTRACT_SUPPLIED_NO_EXTERNAL_RUN"; assert "DFM_MKC_NUMERICAL_BOLTZMANN_SOLVER_V1" in data()["source_dependencies"]; assert "DFM_MKC_EXECUTABLE_SOLVER_IMPLEMENTATION_V1" in data()["source_dependencies"]
def test_allowed_targets_and_binding_fields_declared(): blob = json.dumps(data(), sort_keys=True); assert "CLASS-compatible external binding" in blob; assert "CAMB-compatible external binding" in blob; assert "source_code_commit" in blob; assert "environment_lock" in blob; assert "reproducibility_hashes" in blob
def test_adapter_requirements_and_trust_gates_declared(): blob = json.dumps(data(), sort_keys=True); assert "dfm_mkc_background_adapter" in blob; assert "dfm_mkc_perturbation_adapter" in blob; assert "observable_adapter" in blob; assert "schema_gate" in blob; assert "hash_gate" in blob; assert "diagnostic_gate" in blob
def test_trusted_binding_acceptance_blocks_claims(): acceptance = data()["acceptance_test_result"]; assert acceptance["binding_contract_present"] is True; assert acceptance["adapter_requirements_present"] is True; assert acceptance["trust_gates_present"] is True; assert acceptance["external_solver_selected"] is False; assert acceptance["external_solver_executed"] is False; assert acceptance["adapter_implemented"] is False; assert acceptance["empirical_status_promoted"] is False
def test_trusted_binding_boundaries(): blocked = set(data()["does_not_prove"]); assert "DFM-MKC external solver adapter implementation" in blocked; assert "DFM-MKC trusted external solver execution" in blocked; assert "DFM-MKC empirical validation" in blocked; assert "Lambda-CDM failure" in blocked; assert "dark matter replacement" in blocked; assert "any Clay problem" in blocked
def test_trusted_binding_doc(): text = DOC.read_text(); assert "DFM_MKC_TRUSTED_EXTERNAL_SOLVER_BINDING_V1" in text; assert "TRUSTED_EXTERNAL_SOLVER_BINDING_CONTRACT_SUPPLIED_NO_EXTERNAL_RUN" in text; assert "Does not prove" in text
