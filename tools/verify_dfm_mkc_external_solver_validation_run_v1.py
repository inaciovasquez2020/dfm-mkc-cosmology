#!/usr/bin/env python3
import importlib.util
import json
import sys
from pathlib import Path

ART = Path("artifacts/repo_intake/dfm_mkc_external_solver_validation_run_v1_2026_05_27.json")
DOC = Path("docs/status/DFM_MKC_EXTERNAL_SOLVER_VALIDATION_RUN_V1_2026_05_27.md")
CODE = Path("src/dfm_mkc_solver/external_solver_validation_run_v1.py")
PREV = Path("artifacts/repo_intake/dfm_mkc_external_solver_adapter_implementation_v1_2026_05_27.json")

assert ART.exists()
assert DOC.exists()
assert CODE.exists()
assert PREV.exists()

data = json.loads(ART.read_text())
assert data["id"] == "DFM_MKC_EXTERNAL_SOLVER_VALIDATION_RUN_V1"
assert data["status"] == "EXTERNAL_SOLVER_VALIDATION_RUN_GATE_SUPPLIED_NO_EXTERNAL_EXECUTION"
assert data["acceptance_test_result"]["code_file_present"] is True
assert data["acceptance_test_result"]["entrypoints_present"] is True
assert data["acceptance_test_result"]["external_solver_executed"] is False
assert data["acceptance_test_result"]["numerical_prediction_vector_computed"] is False

for term in [
    "DFM-MKC empirical validation",
    "Lambda-CDM failure",
    "dark matter replacement",
    "P vs NP",
    "any Clay problem",
]:
    assert term in data["does_not_prove"]

spec = importlib.util.spec_from_file_location("external_solver_validation_run_v1", CODE)
module = importlib.util.module_from_spec(spec)
assert spec.loader is not None
sys.modules[spec.name] = module
spec.loader.exec_module(module)

for name in data["entrypoints"]:
    assert hasattr(module, name)

binding = {
    "external_target": "CLASS-compatible external binding",
    "source_code_commit": "x",
    "environment_lock": "x",
    "input_schema": {},
    "output_schema": {},
    "unit_convention": {},
    "observable_ordering": [],
    "covariance_alignment": {},
    "reproducibility_hashes": {},
}
run_record = {
    "input_hash": "x",
    "output_hash": "x",
    "diagnostic_hash": "x",
    "finite_output_check": True,
    "constraint_residual_check": True,
    "convergence_summary": {},
    "reproducibility_summary": {},
}

result = module.run_external_solver_validation_gate(binding, run_record)
assert result["object_id"] == "DFM_MKC_EXTERNAL_SOLVER_VALIDATION_RUN_V1"
assert result["external_solver_executed"] is False
assert result["numerical_prediction_vector_computed"] is False

text = DOC.read_text()
for term in [
    "DFM_MKC_EXTERNAL_SOLVER_VALIDATION_RUN_V1",
    "EXTERNAL_SOLVER_VALIDATION_RUN_GATE_SUPPLIED_NO_EXTERNAL_EXECUTION",
    "Does not prove DFM-MKC empirical validation",
    "Does not prove any Clay problem",
]:
    assert term in text

print("DFM_MKC_EXTERNAL_SOLVER_VALIDATION_RUN_V1_OK")
