import importlib.util
import json
import sys
from pathlib import Path

ART = Path("artifacts/repo_intake/dfm_mkc_validated_numerical_integrator_v1_2026_05_27.json")
CODE = Path("src/dfm_mkc_solver/validated_integrator_v1.py")

spec = importlib.util.spec_from_file_location("validated_integrator_v1", CODE)
module = importlib.util.module_from_spec(spec)
assert spec.loader is not None
sys.modules[spec.name] = module
spec.loader.exec_module(module)

data = json.loads(ART.read_text())

config = {
    "cosmological_parameters": {},
    "dfm_mkc_parameters": {},
    "grid_parameters": {},
    "solver_parameters": {},
    "reproducibility_parameters": {},
}

diagnostics = {
    "finite_output_check": True,
    "constraint_residual_check": True,
    "grid_convergence_check": True,
    "ell_max_convergence_check": True,
    "hash_reproducibility_check": True,
}


def test_integrator_artifact_status():
    assert data["id"] == "DFM_MKC_VALIDATED_NUMERICAL_INTEGRATOR_V1"
    assert data["status"] == "VALIDATED_NUMERICAL_INTEGRATOR_GATE_SUPPLIED_NO_NUMERICAL_RUN"


def test_integrator_entrypoints_importable():
    assert hasattr(module, "validate_integrator_config")
    assert hasattr(module, "run_validated_integrator_gate")


def test_integrator_run_is_gated():
    result = module.run_validated_integrator_gate(config, diagnostics)
    assert result["numerical_integration_run"] is False
    assert result["prediction_vector_computed"] is False


def test_integrator_boundaries():
    blocked = set(data["does_not_prove"])
    assert "DFM-MKC empirical validation" in blocked
    assert "Lambda-CDM failure" in blocked
    assert "any Clay problem" in blocked
