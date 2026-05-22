import importlib.util
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
VERIFY = ROOT / "tools/verify_independent_source_hash_schema_validation_for_each_multiprobe_input.py"
ARTIFACT = ROOT / "artifacts/cosmology/independent_source_hash_and_schema_validation_for_each_multiprobe_input_2026_05_22.json"

spec = importlib.util.spec_from_file_location("verify_independent_source_hash_schema_validation_for_each_multiprobe_input", VERIFY)
module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(module)

def test_verifier_passes():
    module.main()

def test_required_inputs_are_present():
    data = json.loads(ARTIFACT.read_text())
    assert set(data["validations"]) == module.REQUIRED_KEYS

def test_gate_does_not_certify_any_input():
    data = json.loads(ARTIFACT.read_text())
    assert data["summary"]["inputs_certified_for_profiled_likelihood_execution"] == 0
    assert data["summary"]["ready_for_executed_multiprobe_profiled_likelihood_run"] is False

def test_hash_and_schema_fields_are_unfilled():
    data = json.loads(ARTIFACT.read_text())
    for entry in data["validations"].values():
        assert entry["independent_source_digest"] is None
        assert entry["independent_hash_match_verified"] is False
        assert entry["schema_validator_or_reader"] is None
        assert entry["schema_validation_passed"] is False

def test_no_overclaim_boundaries():
    data = json.loads(ARTIFACT.read_text())
    assert "Lambda-CDM rejection" in data["does_not_prove"]
    assert "DFM-MKC validation" in data["does_not_prove"]
    assert "any Clay problem" in data["does_not_prove"]
