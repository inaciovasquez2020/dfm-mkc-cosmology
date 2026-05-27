#!/usr/bin/env python3
import importlib.util, json, sys
from pathlib import Path
ART = Path("artifacts/repo_intake/dfm_mkc_production_solver_code_v1_2026_05_27.json")
DOC = Path("docs/status/DFM_MKC_PRODUCTION_SOLVER_CODE_V1_2026_05_27.md")
CODE = Path("src/dfm_mkc_solver/production_solver_v1.py")
PREV = Path("artifacts/repo_intake/dfm_mkc_executable_solver_implementation_v1_2026_05_27.json")
assert ART.exists()
assert DOC.exists()
assert CODE.exists()
assert PREV.exists()
data = json.loads(ART.read_text())
assert data["id"] == "DFM_MKC_PRODUCTION_SOLVER_CODE_V1"
assert data["status"] == "PRODUCTION_SOLVER_CODE_SURFACE_SUPPLIED_NO_NUMERICAL_INTEGRATION"
assert data["acceptance_test_result"]["code_file_present"] is True
assert data["acceptance_test_result"]["entrypoints_present"] is True
assert data["acceptance_test_result"]["numerical_integration_run"] is False
assert data["acceptance_test_result"]["prediction_vector_computed"] is False
for term in ["DFM-MKC empirical validation", "Lambda-CDM failure", "dark matter replacement", "P vs NP", "any Clay problem"]: assert term in data["does_not_prove"]
spec = importlib.util.spec_from_file_location("production_solver_v1", CODE)
module = importlib.util.module_from_spec(spec)
assert spec.loader is not None
sys.modules[spec.name] = module
spec.loader.exec_module(module)
for name in data["entrypoints"]: assert hasattr(module, name)
config = {
"cosmological_parameters": {},
"dfm_mkc_parameters": {},
"grid_parameters": {},
"solver_parameters": {},
"reproducibility_parameters": {}
}
result = module.dfm_mkc_run_prediction_vector(config)
assert result.object_id == "DFM_MKC_PRODUCTION_SOLVER_CODE_V1"
assert result.numerical_integration_run is False
assert result.prediction_vector_computed is False
text = DOC.read_text()
for term in ["DFM_MKC_PRODUCTION_SOLVER_CODE_V1", "PRODUCTION_SOLVER_CODE_SURFACE_SUPPLIED_NO_NUMERICAL_INTEGRATION", "Does not prove DFM-MKC empirical validation", "Does not prove any Clay problem"]: assert term in text
print("DFM_MKC_PRODUCTION_SOLVER_CODE_V1_OK")
