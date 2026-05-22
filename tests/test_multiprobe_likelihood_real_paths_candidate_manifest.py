import importlib.util
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
VERIFY = ROOT / "tools/verify_multiprobe_likelihood_real_paths_candidate_manifest.py"
ARTIFACT = ROOT / "artifacts/cosmology/multiprobe_likelihood_input_manifest_with_real_paths_candidate_2026_05_22.json"

spec = importlib.util.spec_from_file_location("verify_multiprobe_likelihood_real_paths_candidate_manifest", VERIFY)
module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(module)

def test_verifier_passes():
    module.main()

def test_required_keys_present():
    data = json.loads(ARTIFACT.read_text())
    assert set(data["inputs"]) == module.REQUIRED_KEYS

def test_manifest_is_partial_not_certified():
    data = json.loads(ARTIFACT.read_text())
    assert data["status"] == "PARTIAL_REAL_PATHS_CANDIDATE_ONLY_INCOMPLETE_LIKELIHOOD_INPUTS"
    assert data["required_next_object"] == "COMPLETE_CERTIFIED_MULTIPROBE_LIKELIHOOD_INPUT_MANIFEST_WITH_REAL_DATA_PATHS"
    assert "complete multiprobe likelihood input availability" in data["does_not_prove"]

def test_candidate_paths_exist_when_non_null():
    data = json.loads(ARTIFACT.read_text())
    for entry in data["inputs"].values():
        if entry["path"]:
            assert (ROOT / entry["path"]).exists()
