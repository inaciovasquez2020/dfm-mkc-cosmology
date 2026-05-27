import importlib.util
import json
import sys
from pathlib import Path

ART = Path("artifacts/repo_intake/dfm_mkc_external_solver_validation_run_v1_2026_05_27.json")
CODE = Path("src/dfm_mkc_solver/external_solver_validation_run_v1.py")

spec = importlib.util.spec_from_file_location("external_solver_validation_run_v1", CODE)
module = importlib.util.module_from_spec(spec)
assert spec.loader is not None
sys.modules[spec.name] = module
spec.loader.exec_module(module)

data = json.loads(ART.read_text())

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


def test_validation_artifact_status():
    assert data["id"] == "DFM_MKC_EXTERNAL_SOLVER_VALIDATION_RUN_V1"
    assert data["status"] == "EXTERNAL_SOLVER_VALIDATION_RUN_GATE_SUPPLIED_NO_EXTERNAL_EXECUTION"


def test_validation_entrypoints_importable():
    assert hasattr(module, "validate_external_solver_binding")
    assert hasattr(module, "run_external_solver_validation_gate")


def test_validation_run_is_gated():
    result = module.run_external_solver_validation_gate(binding, run_record)
    assert result["external_solver_executed"] is False
    assert result["numerical_prediction_vector_computed"] is False


def test_validation_boundaries():
    blocked = set(data["does_not_prove"])
    assert "DFM-MKC empirical validation" in blocked
    assert "Lambda-CDM failure" in blocked
    assert "any Clay problem" in blocked
