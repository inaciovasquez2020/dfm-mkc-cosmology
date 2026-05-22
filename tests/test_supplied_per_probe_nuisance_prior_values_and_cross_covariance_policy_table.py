import importlib.util
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
VERIFY = ROOT / "tools/verify_supplied_per_probe_nuisance_prior_values_and_cross_covariance_policy_table.py"
ARTIFACT = ROOT / "artifacts/cosmology/supplied_per_probe_nuisance_prior_values_and_cross_covariance_policy_table_2026_05_22.json"

spec = importlib.util.spec_from_file_location("verify_supplied_per_probe_nuisance_prior_values_and_cross_covariance_policy_table", VERIFY)
module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(module)

def test_verifier_passes():
    module.main()

def test_rows_materialized():
    data = json.loads(ARTIFACT.read_text())
    assert len(data["nuisance_prior_rows"]) == 7
    assert len(data["cross_covariance_policy_rows"]) == 21

def test_values_not_overclaimed():
    data = json.loads(ARTIFACT.read_text())
    assert data["nuisance_prior_values_supplied"] is False
    assert data["cross_covariance_policies_supplied"] is False
    assert data["table_certified"] is False

def test_next_object_is_external_source_values():
    data = json.loads(ARTIFACT.read_text())
    assert data["required_next_object"] == "EXTERNAL_NUISANCE_PRIOR_SOURCE_TABLE_AND_CROSS_COVARIANCE_POLICY_VALUES"

def test_no_overclaim_boundaries():
    data = json.loads(ARTIFACT.read_text())
    assert "complete certified multiprobe likelihood manifest" in data["does_not_prove"]
    assert "executed multiprobe likelihood run" in data["does_not_prove"]
    assert "Lambda-CDM rejection" in data["does_not_prove"]
    assert "DFM-MKC validation" in data["does_not_prove"]
    assert "any Clay problem" in data["does_not_prove"]
