import importlib.util
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
VERIFY = ROOT / "tools/verify_complete_certified_multiprobe_likelihood_input_manifest_target.py"
ARTIFACT = ROOT / "artifacts/cosmology/complete_certified_multiprobe_likelihood_input_manifest_with_real_data_paths_2026_05_22.json"

spec = importlib.util.spec_from_file_location("verify_complete_certified_multiprobe_likelihood_input_manifest_target", VERIFY)
module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(module)

def test_verifier_passes():
    module.main()

def test_required_keys_present():
    data = json.loads(ARTIFACT.read_text())
    assert set(data["required_certified_inputs"]) == module.REQUIRED_KEYS

def test_certification_status_blocks_promotion():
    data = json.loads(ARTIFACT.read_text())
    assert data["status"] == "CERTIFICATION_TARGET_ONLY_REQUIRED_INPUTS_MISSING"
    assert data["required_next_object"] == "FILE_LEVEL_MULTIPROBE_INPUT_DIGEST_AND_PROVENANCE_MANIFEST"
    assert all(value is False for value in data["current_certification_status"].values())

def test_boundaries_preserve_no_overclaim():
    data = json.loads(ARTIFACT.read_text())
    assert "complete multiprobe likelihood input availability" in data["does_not_prove"]
    assert "certified multiprobe likelihood execution readiness" in data["does_not_prove"]
    assert "Lambda-CDM failure" in data["does_not_prove"]
    assert "six-parameter flat Lambda-CDM rejection" in data["does_not_prove"]
    assert "DFM-MKC validation" in data["does_not_prove"]
    assert "any Clay problem" in data["does_not_prove"]
