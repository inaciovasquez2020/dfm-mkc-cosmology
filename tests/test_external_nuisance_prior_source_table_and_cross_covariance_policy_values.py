import importlib.util
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
VERIFY = ROOT / "tools/verify_external_nuisance_prior_source_table_and_cross_covariance_policy_values.py"
ARTIFACT = ROOT / "artifacts/cosmology/external_nuisance_prior_source_table_and_cross_covariance_policy_values_2026_05_22.json"

spec = importlib.util.spec_from_file_location("verify_external_nuisance_prior_source_table_and_cross_covariance_policy_values", VERIFY)
module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(module)

def test_verifier_passes():
    module.main()

def test_rows_materialized():
    data = json.loads(ARTIFACT.read_text())
    assert len(data["external_nuisance_source_rows"]) == 7
    assert len(data["external_cross_covariance_policy_rows"]) == 21

def test_external_values_not_supplied():
    data = json.loads(ARTIFACT.read_text())
    assert data["nuisance_sources_bound"] is False
    assert data["covariance_sources_bound"] is False
    assert data["nuisance_values_supplied"] is False
    assert data["covariance_policies_supplied"] is False
    assert data["combined_certification_closed"] is False

def test_next_object_is_bound_external_sources():
    data = json.loads(ARTIFACT.read_text())
    assert data["required_next_object"] == "BOUND_EXTERNAL_NUISANCE_PRIOR_SOURCES_AND_COVARIANCE_POLICY_RECORDS"

def test_no_overclaim_boundaries():
    data = json.loads(ARTIFACT.read_text())
    assert "complete certified multiprobe likelihood manifest" in data["does_not_prove"]
    assert "executed multiprobe likelihood run" in data["does_not_prove"]
    assert "Lambda-CDM rejection" in data["does_not_prove"]
    assert "DFM-MKC validation" in data["does_not_prove"]
    assert "any Clay problem" in data["does_not_prove"]
