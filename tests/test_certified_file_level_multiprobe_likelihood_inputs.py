import importlib.util
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
VERIFY = ROOT / "tools/verify_certified_file_level_multiprobe_likelihood_inputs.py"
ARTIFACT = ROOT / "artifacts/cosmology/certified_file_level_multiprobe_likelihood_inputs_2026_05_22.json"

spec = importlib.util.spec_from_file_location("verify_certified_file_level_multiprobe_likelihood_inputs", VERIFY)
module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(module)

def test_verifier_passes():
    module.main()

def test_required_inputs_are_present():
    data = json.loads(ARTIFACT.read_text())
    assert set(data["inputs"]) == module.REQUIRED_KEYS

def test_no_input_is_certified_by_gate_only_object():
    data = json.loads(ARTIFACT.read_text())
    assert data["summary"]["certified_inputs"] == 0
    assert data["summary"]["ready_for_executed_multiprobe_profiled_likelihood_run"] is False
    for entry in data["inputs"].values():
        assert entry["certified_for_profiled_likelihood_execution"] is False

def test_certification_blockers_are_explicit():
    data = json.loads(ARTIFACT.read_text())
    assert "independent source hash verification for every input" in data["remaining_missing_certifications"]
    assert "schema or likelihood-reader validation for every input" in data["remaining_missing_certifications"]
    assert "profiled likelihood execution harness binding" in data["remaining_missing_certifications"]

def test_no_overclaim_boundaries():
    data = json.loads(ARTIFACT.read_text())
    assert "Lambda-CDM rejection" in data["does_not_prove"]
    assert "DFM-MKC validation" in data["does_not_prove"]
    assert "any Clay problem" in data["does_not_prove"]
