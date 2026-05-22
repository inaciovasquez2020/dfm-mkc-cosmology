import importlib.util
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
VERIFY = ROOT / "tools/verify_probe_specific_independent_source_hashes_and_schema_readers.py"
ARTIFACT = ROOT / "artifacts/cosmology/probe_specific_independent_source_hashes_and_schema_readers_2026_05_22.json"

spec = importlib.util.spec_from_file_location("verify_probe_specific_independent_source_hashes_and_schema_readers", VERIFY)
module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(module)

def test_verifier_passes():
    module.main()

def test_required_probe_targets_are_present():
    data = json.loads(ARTIFACT.read_text())
    assert set(data["reader_targets"]) == module.REQUIRED_KEYS

def test_reader_targets_are_registry_only():
    data = json.loads(ARTIFACT.read_text())
    assert data["status"] == "PROBE_READER_TARGET_REGISTRY_ONLY_NO_CERTIFICATION"
    assert data["summary"]["readers_implemented"] == 0
    assert data["summary"]["schema_validations_passed"] == 0

def test_no_target_is_certified():
    data = json.loads(ARTIFACT.read_text())
    for entry in data["reader_targets"].values():
        assert entry["independent_digest_supplied"] is False
        assert entry["reader_implemented"] is False
        assert entry["schema_validation_passed"] is False
        assert entry["certified_for_profiled_likelihood_execution"] is False

def test_no_overclaim_boundaries():
    data = json.loads(ARTIFACT.read_text())
    assert "Lambda-CDM rejection" in data["does_not_prove"]
    assert "DFM-MKC validation" in data["does_not_prove"]
    assert "any Clay problem" in data["does_not_prove"]
