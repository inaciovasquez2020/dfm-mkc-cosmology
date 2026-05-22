import importlib.util
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
VERIFY = ROOT / "tools/verify_executed_multiprobe_profiled_likelihood_run_gate.py"
TARGET = ROOT / "artifacts/cosmology/executed_multiprobe_profiled_likelihood_run_2026_05_22.json"
TEMPLATE = ROOT / "artifacts/cosmology/multiprobe_likelihood_input_manifest_template_2026_05_22.json"

spec = importlib.util.spec_from_file_location("verify_executed_multiprobe_profiled_likelihood_run_gate", VERIFY)
module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(module)

def test_verifier_passes():
    module.main()

def test_target_is_input_gated_not_executed():
    data = json.loads(TARGET.read_text())
    assert data["status"] == "INPUT_GATED_EXECUTION_TARGET_ONLY_NO_LIKELIHOOD_RUN"
    assert all(value is False for value in data["current_execution_status"].values())
    assert data["required_next_object"] == "MULTIPROBE_LIKELIHOOD_INPUT_MANIFEST_WITH_REAL_DATA_PATHS"

def test_manifest_template_has_all_required_inputs_empty():
    data = json.loads(TEMPLATE.read_text())
    assert data["status"] == "TEMPLATE_ONLY_REAL_DATA_PATHS_NOT_SUPPLIED"
    assert set(data["inputs"]) == module.REQUIRED_INPUT_KEYS
    assert all(value is None for value in data["inputs"].values())

def test_no_overclaim_boundary():
    data = json.loads(TARGET.read_text())
    assert "Lambda-CDM failure" in data["does_not_prove"]
    assert "six-parameter flat Lambda-CDM rejection" in data["does_not_prove"]
    assert "DFM-MKC validation" in data["does_not_prove"]
    assert "any Clay problem" in data["does_not_prove"]
    assert "does not execute a real likelihood" in data["boundary"]
