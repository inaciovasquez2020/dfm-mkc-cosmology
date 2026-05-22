import importlib.util
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
VERIFY = ROOT / "tools/verify_lcdm_methodological_counter_source_map.py"
ARTIFACT = ROOT / "artifacts/cosmology/lcdm_methodological_counter_source_map_2026_05_22.json"

spec = importlib.util.spec_from_file_location("verify_lcdm_methodological_counter_source_map", VERIFY)
module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(module)

def test_verifier_passes():
    module.main()

def test_blanchard_source_registered_as_methodological_counter_source_only():
    data = json.loads(ARTIFACT.read_text())
    source = data["sources"][0]
    assert source["id"] == "BLANCHARD_2025_FALLACIES_OF_LCDM_FALSIFICATIONS"
    assert source["claim_class"] == "PEER_REVIEWED_METHODOLOGICAL_COUNTER_SOURCE_ONLY"
    assert source["doi"] == "10.5772/intechopen.1010549"

def test_no_lcdm_success_or_failure_promotion():
    data = json.loads(ARTIFACT.read_text())
    assert data["status"] == "METHODOLOGICAL_COUNTER_SOURCE_ONLY_NO_LCDM_REJECTION"
    assert "Lambda-CDM correctness" in data["does_not_prove"]
    assert "Lambda-CDM failure" in data["does_not_prove"]
    assert "six-parameter flat Lambda-CDM rejection" in data["does_not_prove"]
    assert "DFM-MKC validation" in data["does_not_prove"]
    assert "any Clay problem" in data["does_not_prove"]

def test_next_object_is_methodological_claim_audit():
    data = json.loads(ARTIFACT.read_text())
    assert data["required_next_object"] == "METHODOLOGICAL_CLAIM_EXTRACTION_AND_FALSIFICATION_CRITERION_AUDIT"
