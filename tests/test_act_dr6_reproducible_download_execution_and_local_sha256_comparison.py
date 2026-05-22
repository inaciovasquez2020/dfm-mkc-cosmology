import importlib.util
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
VERIFY = ROOT / "tools/verify_act_dr6_reproducible_download_execution_and_local_sha256_comparison.py"
ARTIFACT = ROOT / "artifacts/cosmology/act_dr6_reproducible_download_execution_and_local_sha256_comparison_2026_05_22.json"

spec = importlib.util.spec_from_file_location("verify_act_dr6_reproducible_download_execution_and_local_sha256_comparison", VERIFY)
module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(module)

def test_verifier_passes():
    module.main()

def test_execution_was_attempted():
    data = json.loads(ARTIFACT.read_text())
    assert data["execution_attempted"] is True
    assert isinstance(data["executed_steps"], list)
    assert len(data["executed_steps"]) >= 1

def test_sha256_comparison_fields_exist():
    data = json.loads(ARTIFACT.read_text())
    assert data["local_sha256"]
    assert isinstance(data["download_reproduces_local_sha256"], bool)
    assert isinstance(data["matching_payloads"], list)

def test_not_profiled_likelihood_certified():
    data = json.loads(ARTIFACT.read_text())
    assert data["certified_for_profiled_likelihood_execution"] is False

def test_no_overclaim_boundaries():
    data = json.loads(ARTIFACT.read_text())
    assert "ACT DR6 full SACC schema certification" in data["does_not_prove"]
    assert "Lambda-CDM rejection" in data["does_not_prove"]
    assert "DFM-MKC validation" in data["does_not_prove"]
    assert "any Clay problem" in data["does_not_prove"]
