import importlib.util
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
VERIFY = ROOT / "tools/verify_certified_nuisance_prior_table_values_and_covariance_compatibility_rule.py"
ARTIFACT = ROOT / "artifacts/cosmology/certified_nuisance_prior_table_values_and_covariance_compatibility_rule_2026_05_22.json"

spec = importlib.util.spec_from_file_location("verify_certified_nuisance_prior_table_values_and_covariance_compatibility_rule", VERIFY)
module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(module)

def test_verifier_passes():
    module.main()

def test_all_probe_slots_exist():
    data = json.loads(ARTIFACT.read_text())
    assert set(data["nuisance_prior_slots"]) == module.PROBES

def test_covariance_pair_slots_exist():
    data = json.loads(ARTIFACT.read_text())
    assert len(data["covariance_compatibility_slots"]) == 21

def test_not_certified_without_values_and_rules():
    data = json.loads(ARTIFACT.read_text())
    assert data["nuisance_prior_values_certified"] is False
    assert data["covariance_compatibility_rule_certified"] is False
    assert data["combined_certification_closed"] is False

def test_no_overclaim_boundaries():
    data = json.loads(ARTIFACT.read_text())
    assert "complete certified multiprobe likelihood manifest" in data["does_not_prove"]
    assert "executed multiprobe likelihood run" in data["does_not_prove"]
    assert "Lambda-CDM rejection" in data["does_not_prove"]
    assert "DFM-MKC validation" in data["does_not_prove"]
    assert "any Clay problem" in data["does_not_prove"]
