import importlib.util
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
VERIFY = ROOT / "tools/verify_file_level_multiprobe_input_digest_and_provenance_manifest.py"
ARTIFACT = ROOT / "artifacts/cosmology/file_level_multiprobe_input_digest_and_provenance_manifest_2026_05_22.json"

spec = importlib.util.spec_from_file_location("verify_file_level_multiprobe_input_digest_and_provenance_manifest", VERIFY)
module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(module)

def test_verifier_passes():
    module.main()

def test_required_keys_present():
    data = json.loads(ARTIFACT.read_text())
    assert set(data["input_entries"]) == module.REQUIRED_KEYS

def test_manifest_is_partial_not_certified():
    data = json.loads(ARTIFACT.read_text())
    assert data["status"] == "PARTIAL_DIGEST_AND_PROVENANCE_MANIFEST_ONLY_NOT_CERTIFIED"
    assert data["summary"]["ready_for_executed_likelihood_run"] is False
    assert data["summary"]["certified_likelihood_inputs"] == 0

def test_missing_inputs_are_explicit():
    data = json.loads(ARTIFACT.read_text())
    assert "union3_or_des_sn_crosscheck" in data["missing_inputs"]
    assert "kids_legacy_likelihood_or_chain" in data["missing_inputs"]
    assert "hsc_y3_likelihood_or_chain" in data["missing_inputs"]
    assert "nuisance_prior_table" in data["missing_inputs"]
