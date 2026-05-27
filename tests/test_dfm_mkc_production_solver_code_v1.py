import importlib.util, json, sys
from pathlib import Path

ART = Path("artifacts/repo_intake/dfm_mkc_production_solver_code_v1_2026_05_27.json")
CODE = Path("src/dfm_mkc_solver/production_solver_v1.py")

spec = importlib.util.spec_from_file_location("production_solver_v1", CODE)
module = importlib.util.module_from_spec(spec)
assert spec.loader is not None
sys.modules[spec.name] = module
spec.loader.exec_module(module)
data = json.loads(ART.read_text())
config = {"cosmological_parameters": {}, "dfm_mkc_parameters": {}, "grid_parameters": {}, "solver_parameters": {}, "reproducibility_parameters": {}}

def test_solver_artifact_status(): assert data["id"] == "DFM_MKC_PRODUCTION_SOLVER_CODE_V1"; assert data["status"] == "PRODUCTION_SOLVER_CODE_SURFACE_SUPPLIED_NO_NUMERICAL_INTEGRATION"
def test_solver_entrypoints_importable(): assert hasattr(module, "dfm_mkc_run_prediction_vector"); assert hasattr(module, "dfm_mkc_solve_background")
def test_solver_run_is_gated(): result = module.dfm_mkc_run_prediction_vector(config); assert result.numerical_integration_run is False; assert result.prediction_vector_computed is False
def test_solver_boundaries(): blocked = set(data["does_not_prove"]); assert "DFM-MKC empirical validation" in blocked; assert "Lambda-CDM failure" in blocked; assert "any Clay problem" in blocked
