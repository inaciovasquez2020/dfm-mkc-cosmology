import importlib.util, json, sys
from pathlib import Path

ART = Path("artifacts/repo_intake/dfm_mkc_external_solver_adapter_implementation_v1_2026_05_27.json")
CODE = Path("src/dfm_mkc_solver/external_adapter_v1.py")

spec = importlib.util.spec_from_file_location("external_adapter_v1", CODE)
module = importlib.util.module_from_spec(spec)
assert spec.loader is not None
sys.modules[spec.name] = module
spec.loader.exec_module(module)
data = json.loads(ART.read_text())
binding = {"external_target": "CLASS-compatible external binding", "source_code_commit": "x", "environment_lock": "x", "input_schema": {}, "output_schema": {}, "unit_convention": {}, "observable_ordering": [], "covariance_alignment": {}, "reproducibility_hashes": {}}

def test_adapter_artifact_status(): assert data["id"] == "DFM_MKC_EXTERNAL_SOLVER_ADAPTER_IMPLEMENTATION_V1"; assert data["status"] == "EXTERNAL_SOLVER_ADAPTER_IMPLEMENTATION_SURFACE_SUPPLIED_NO_EXTERNAL_RUN"
def test_adapter_entrypoints_importable(): assert hasattr(module, "dfm_mkc_background_adapter"); assert hasattr(module, "dfm_mkc_validate_external_binding")
def test_adapter_run_is_gated(): result = module.dfm_mkc_background_adapter(binding); assert result.external_solver_executed is False; assert result.numerical_prediction_vector_computed is False
def test_adapter_boundaries(): blocked = set(data["does_not_prove"]); assert "DFM-MKC empirical validation" in blocked; assert "Lambda-CDM failure" in blocked; assert "any Clay problem" in blocked
