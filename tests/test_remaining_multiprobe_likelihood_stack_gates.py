import importlib.util
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
VERIFY = ROOT / "tools/verify_remaining_multiprobe_likelihood_stack_gates.py"
SUMMARY = ROOT / "artifacts/cosmology/remaining_multiprobe_likelihood_stack_gates_2026_05_22.json"
MANIFEST = ROOT / "artifacts/cosmology/complete_certified_multiprobe_likelihood_input_manifest_2026_05_22.json"
RUN = ROOT / "artifacts/cosmology/executed_multiprobe_profiled_likelihood_run_2026_05_22.json"
OOS = ROOT / "artifacts/cosmology/out_of_sample_multiprobe_lcdm_rejection_certificate_2026_05_22.json"

spec = importlib.util.spec_from_file_location("verify_remaining_multiprobe_likelihood_stack_gates", VERIFY)
module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(module)

def test_verifier_passes():
    module.main()

def test_all_required_objects_materialized():
    data = json.loads(SUMMARY.read_text())
    assert set(data["objects_materialized"]) == module.REQUIRED_OBJECTS

def test_manifest_not_ready_without_nuisance_and_covariance():
    data = json.loads(MANIFEST.read_text())
    assert data["nuisance_prior_table_certified"] is False
    assert data["covariance_chain_compatibility_certified"] is False
    assert data["complete_manifest_ready"] is False

def test_no_execution_or_rejection_claimed():
    run = json.loads(RUN.read_text())
    oos = json.loads(OOS.read_text())
    assert run["execution_performed"] is False
    assert oos["lcdm_rejection_claimed"] is False
    assert oos["dfm_mkc_validation_claimed"] is False

def test_no_overclaim_boundaries():
    data = json.loads(SUMMARY.read_text())
    assert "Lambda-CDM rejection" in data["does_not_prove"]
    assert "DFM-MKC validation" in data["does_not_prove"]
    assert "any Clay problem" in data["does_not_prove"]
