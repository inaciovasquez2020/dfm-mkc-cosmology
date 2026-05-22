import importlib.util
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
VERIFY = ROOT / "tools/verify_act_dr6_certified_profiled_likelihood_input.py"
ARTIFACT = ROOT / "artifacts/cosmology/act_dr6_certified_profiled_likelihood_input_2026_05_22.json"

spec = importlib.util.spec_from_file_location("verify_act_dr6_certified_profiled_likelihood_input", VERIFY)
module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(module)

def test_verifier_passes():
    module.main()

def test_act_dr6_input_is_certified_for_profiled_likelihood_execution():
    data = json.loads(ARTIFACT.read_text())
    assert data["certified_for_profiled_likelihood_execution"] is True
    assert data["status"] == "ACT_DR6_CERTIFIED_PROFILED_LIKELIHOOD_INPUT_CLOSED_NO_LIKELIHOOD_EXECUTION"

def test_no_likelihood_execution_claimed():
    data = json.loads(ARTIFACT.read_text())
    assert data["profiled_likelihood_execution_performed"] is False

def test_next_object_moves_to_pantheon_plus_shoes():
    data = json.loads(ARTIFACT.read_text())
    assert data["required_next_object"] == "PANTHEON_PLUS_SHOES_EXTERNAL_DIGEST_AND_SCHEMA_READER"

def test_no_overclaim_boundaries():
    data = json.loads(ARTIFACT.read_text())
    assert "executed multiprobe likelihood run" in data["does_not_prove"]
    assert "Lambda-CDM rejection" in data["does_not_prove"]
    assert "DFM-MKC validation" in data["does_not_prove"]
    assert "any Clay problem" in data["does_not_prove"]
